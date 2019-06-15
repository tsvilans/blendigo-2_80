import bpy

import numpy as np
import ctypes
import os

import time
from mathutils import Vector

import bgl
import time

import blendigo.pyIndigo
from blendigo.pyIndigo import *
from blendigo.export import MaterialExporter,ShaderNodeExporter

from .camera import export_camera
from .background import export_background
from .mesh import export_indigo_mesh

class IndigoRenderEngine(bpy.types.RenderEngine):
    bl_idname = 'IndigoAPI'
    bl_label = "IndigoAPI"
    bl_use_preview = False
    bl_use_shading_nodes = True
    bl_use_shading_nodes_custom = False

    def export_object(self, obj, matrix = None, name = ""):
        if obj.type not in {'MESH', 'CURVE', 'SURFACE', 'FONT', 'META'}:
            return False

        if name == "":
            name = obj.name

        if name not in self.exported_objects.keys():
            print("Exporting object {}...".format(name))
            
            if obj.data.name not in self.exported_meshes.keys():
                indigo_mesh = export_indigo_mesh(obj.data)
                if not indigo_mesh:
                    print("Error exporting mesh {}".format(obj.data.name))
                    return False
                self.exported_meshes[obj.data.name] = indigo_mesh

            else:
                indigo_mesh = self.exported_meshes[obj.data.name]
            
            
            indigo_model = Model(name, indigo_mesh)

            if matrix == None:
                indigo_model.SetTransformation(obj.matrix_world, 0)
            else:
                indigo_model.SetTransformation(matrix, 0)
            
            materials = []
            emission_scales = []
            for mat in obj.data.materials:
                if mat == None:
                    continue

                if mat.name in self.material_exporter.exported_materials.keys():
                    materials.append(self.material_exporter.exported_materials[mat.name])

                '''
                if mat.indigo_material.indigo_material_emission.emission_scale:
                    em = mat.indigo_material.indigo_material_emission
                    value = em.emission_scale_value * 10 ** em.emission_scale_exp

                    if em.emission_scale_measure == 'luminous_flux':
                        measure = Measure.LUMINOUS_FLUX
                    elif em.emission_scale_measure == 'luminous_intensity':
                        measure = Measure.LUMINOUS_INTENSITY
                    elif em.emission_scale_measure == 'luminance':
                        measure = Measure.LUMINANCE
                    elif em.emission_scale_measure == 'luminous_emittance':
                        measure = Measure.LUMINOUS_EMITTANCE
                    else:
                        measure = Measure.NONE

                    emission_scales.append(EmissionScale(measure, value, self.material_exporter.exported_materials[mat.name]))
                '''
            
            indigo_model.SetMaterials(materials)
            indigo_model.SetEmissionScales(emission_scales)

            self.exported_objects[name] = indigo_model
            #print("Added model %s..." % obj.name)

            return True
        return False


    def __init__(self):

        directory = os.path.dirname(os.path.realpath(blendigo.pyIndigo.__file__))
        dll_path = os.path.join(directory, 'bin')
        appdata_path = os.path.join(directory, 'bin')

        self.ctx = Context()
        self.renderer = None
        self.scene = None

        self.exported_meshes = {}
        self.exported_objects = {}

        #self.material_exporter = MaterialExporter()

        self.cancel_token = False

        self.is_initialized = False


        res = self.ctx.Initialize(dll_path, appdata_path)
        if res == -1:
            raise Exception("Indigo Context failed to initialize. Check paths.")

        self.is_initialized = True

    def chunks(self, l, n):
        for i in range(0, len(l), n):
            yield l[i:i+n]        

    def update(self, data, scene):
        pass

    def render(self, depsgraph):

        if not self.is_initialized:
            print("Indigo is not initialized.")
            return

        self.scene = depsgraph.scene

        self.exported_meshes = {}
        self.exported_objects = {}

        self.material_exporter = ShaderNodeExporter()
        '''
        if self.is_preview:
            self.render_preview(scene)
        else:
            self.render_scene(scene)
        '''

        rs = RenderSettings()
        rs.width = self.resolution_x
        rs.height = self.resolution_y

        render_settings = self.scene.indigo_engine

        rs.metropolis = render_settings.metropolis
        rs.bidirectional = render_settings.bidirectional
        rs.vignetting = self.scene.camera.data.indigo_camera.vignetting
        rs.halt_samples = render_settings.haltspp
        rs.halt_time = render_settings.halttime
        rs.supersampling = render_settings.supersampling
        rs.foreground_alpha = render_settings.foreground_alpha

        scn = Scene()
        scn.AddRenderSettings(rs)
        
        #for medium in self.scene.indigo_material_medium.medium:
        #    print (medium.name)
        #    indigo_medium = SceneNodeMedium(medium.name, Medium.Basic(medium.name, medium.medium_ior, medium.precedence))
        #    self.material_exporter.exported_mediums[medium.name] = indigo_medium

        for material in bpy.data.materials:
            if material.name not in self.material_exporter.exported_materials:
                pass
                self.material_exporter.export(material);
                scn.AddMaterial(self.material_exporter.exported_materials[material.name])
           
        for instance in depsgraph.object_instances:
            if self.test_break():
                return

            if instance.is_instance:
                self.export_object(instance.object, instance.matrix_world, instance.object.name + "_({})".format(instance.random_id))
            else:
                self.export_object(instance.object, instance.matrix_world)

        for mesh in self.exported_meshes:
            scn.AddMesh(self.exported_meshes[mesh])

        for obj in self.exported_objects:
            scn.AddModel(self.exported_objects[obj])

        for med in self.material_exporter.exported_mediums:
            scn.AddMedium(self.material_exporter.exported_mediums[med])
            #break


        print ("Exporting tonemapping...")
        tonemapping_type = {'Linear':1000, 'Reinhard':1001, 'Camera':1002, 'Filmic':1003}
        tm = Tonemapping()
        tm.type = tonemapping_type['Linear']
        tm.iso = self.scene.camera.data.indigo_camera.iso
        #tm.ev = self.scene.camera.data.indigo_tonemapping.camera_ev

        scale = render_settings.buffer_multiplier
        tm.scale = 1 / scale
        
        print ("Exporting camera...")
        cam = export_camera(bpy.context.scene.camera)
        scn.AddCamera(cam)

        print("Exporting background...")
        bg = export_background(depsgraph)
        if bg is not None:
            scn.AddBackground(bg)

        scn.AddTonemapping(tm)

        self.renderer = Renderer(self.ctx, self.resolution_x, self.resolution_y)

        float_buffer = FloatBuffer()
        uint8_buffer = UInt8Buffer()
        render_buffer = RenderBuffer(scn)

        tone_mapper = ToneMapper(self.ctx, render_buffer, uint8_buffer, float_buffer)
        tone_mapper.Update(scn)

        self.renderer.InitializeWithScene(self.ctx, scn, render_buffer, tone_mapper)

        if render_settings.write_to_xml:
            print ("Writing to XML...")
            scn.WriteToXML("C:/tmp/Blendigo280_test.igs")

        #import subprocess
        #subprocess.run(["C:\\Program Files\\Indigo Renderer\\indigo.exe", "C:/tmp/PyIndigoTest2.igs"])

        self.renderer.Start()

        pixels = []
        #pixels = [None] * (self.resolution_y * self.resolution_x)

        max_pass = 20
        current_pass = 0

        raw_buffer = float_buffer.get_data_pointer()

        float_buffer.create_dummy()


        shape = int(self.resolution_y * self.resolution_x)
        shape_x = int(self.resolution_x)
        shape_y = int(self.resolution_y)

        pixels = [[0,0,0,0]] * shape

        #raw_pixels = np.ctypeslib.as_array(raw_buffer, (shape_x, shape_y, 4))

        print("Entering rendering loop...")

        interval = 1.0

        if render_settings.haltspp < 1:
            haltspp = 100
        else:
            haltspp = render_settings.haltspp

        while self.test_break() is False:

            start = time.time()
            result = self.begin_result(0, 0, self.resolution_x, self.resolution_y)
            self.renderer.Poll()

            tone_mapper.TonemapBlocking()

            #raw_pixels = np.ctypeslib.as_array(raw_buffer, (shape_x, shape_y, 4))
            raw_pixels = np.ctypeslib.as_array(float_buffer.get_flipped(), (shape_x, shape_y, 4))

            pixels = np.multiply(raw_pixels, np.array([scale, scale, scale, 1]))
            pixels.shape = (shape, 4)

            result.layers[0].passes["Combined"].rect = pixels
            
            self.end_result(result)
            self.update_stats("SPP: %.2f" % self.renderer.samples_per_pixel, "Num. passes: %i" % current_pass)


            if self.renderer.samples_per_pixel > haltspp:
                break
                
            current_pass += 1

            while time.time()-start < interval and self.test_break() is False:
                time.sleep(0.03)
                if self.renderer.samples_per_pixel > haltspp:
                   break

            #time.sleep(max(interval, end-start))
            interval *= 1.25

        print("Stopping...")    

        #self.end_result(result)
        
        self.renderer.Stop()
        self.renderer.Poll()
        self.renderer.Shutdown()        

        print("Exiting rendering loop...")
        print("Num passes: %i" % current_pass)
        return

    def __del__(self):
        pass
