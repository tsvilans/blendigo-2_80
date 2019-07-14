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
from blendigo.export import *
from blendigo.pyIndigo.ToneMapper import ChannelID

TONEMAPPING_TYPE = {'Linear':1000, 'Reinhard':1001, 'Camera':1002, 'Filmic':1003}

class RenderChannel:
    def __init__(self, name, num_components, channel_ids, channel_type, indigo_id, scale_values=False):
        self.name = name
        self.num_components = num_components
        self.channel_ids = channel_ids
        self.channel_type = channel_type
        self.indigo_id = indigo_id
        self.scale_values = scale_values

indigo_aovs = {
    "foreground_channel": RenderChannel("Foreground", 4, 'RGBA', 'COLOR', ChannelID.CHANNEL_ALPHA, True),

    "normals_channel": RenderChannel("Normals", 4, 'RGBA', 'COLOR', ChannelID.CHANNEL_NORMALS),
    "normals_pre_bump_channel": RenderChannel("Normals pre bump", 3, 'XYZ', 'VECTOR', ChannelID.CHANNEL_NORMALS_PRE_BUMP),
    "depth_channel": RenderChannel("Depth", 1, 'X', 'VALUE', ChannelID.CHANNEL_DEPTH),
    "position_channel": RenderChannel("Position", 4, 'RGBA', 'COLOR', ChannelID.CHANNEL_POSITION),
    "material_id_channel": RenderChannel("Material id", 1, 'X', 'VALUE', ChannelID.CHANNEL_NORMALS),
    "object_id_channel": RenderChannel("Object id", 1, 'X', 'VALUE', ChannelID.CHANNEL_OBJECT_ID),

    "direct_lighting_channel": RenderChannel("Direct lighting", 4, 'RGBA', 'COLOR', ChannelID.CHANNEL_DIRECT_LIGHTING, True),
    "indirect_lighting_channel": RenderChannel("Indirect lighting", 4, 'RGBA', 'COLOR', ChannelID.CHANNEL_INDIRECT_LIGHTING, True),
    "specular_reflection_lighting_channel": RenderChannel("Specular reflection lighting", 4, 'RGBA', 'COLOR', ChannelID.CHANNEL_SPECULAR_REFLECTION_LIGHTING, True),
    "refraction_lighting_channel": RenderChannel("Refraction lighting", 4, 'RGBA', 'COLOR', ChannelID.CHANNEL_REFRACTION_LIGHTING, True),
    "transmission_lighting_channel": RenderChannel("Transmission lighting", 4, 'RGBA', 'COLOR', ChannelID.CHANNEL_TRANSMISSION_LIGHTING, True),
    "emission_lighting_channel": RenderChannel("Emission lighting", 4, 'RGBA', 'COLOR', ChannelID.CHANNEL_EMISSION_LIGHTING, True),
    "participating_media_lighting_channel": RenderChannel("Participating media lighting", 4, 'RGBA', 'COLOR', ChannelID.CHANNEL_PARTICIPATING_MEDIA_LIGHTING, True),

    "sss_lighting_channel": RenderChannel("Sss lighting", 4, 'RGBA', 'COLOR', ChannelID.CHANNEL_SSS_LIGHTING, True),
}


class IndigoRenderEngine(bpy.types.RenderEngine):
    bl_idname = 'IndigoAPI'
    bl_label = "IndigoAPI"
    bl_use_preview = True
    bl_use_shading_nodes = True
    bl_use_shading_nodes_custom = False
    bl_use_eevee_viewport = True
    bl_use_postprocess = True

    def export_object(self, obj, matrix = None, name = ""):
        if obj.type not in {'MESH', 'CURVE', 'SURFACE', 'FONT', 'META'}:
            return False

        if name == "":
            name = obj.name

        if name not in self.exported_objects.keys():
            #print("Exporting object {}...".format(name))
            
            if obj.data.name not in self.exported_meshes.keys():
                temp = obj.to_mesh()
                indigo_mesh = export_indigo_mesh(temp)
                if not indigo_mesh:
                    print("Error exporting mesh {}".format(obj.data.name))
                    return False
                self.exported_meshes[obj.data.name] = indigo_mesh
                obj.to_mesh_clear()

            else:
                indigo_mesh = self.exported_meshes[obj.data.name]
            
            
            indigo_model = Model.New(name, indigo_mesh)

            if matrix == None:
                indigo_model.SetTransformation(obj.matrix_world, 0)
            else:
                indigo_model.SetTransformation(matrix, 0)
            
            materials = []
            emission_scales = []
            for mat in obj.data.materials:
                if mat == None:
                    continue

                if mat.name not in self.material_exporter.exported_materials.keys():
                    self.material_exporter.export(mat)

                if mat.name in self.material_exporter.exported_materials.keys():
                    materials.append(self.material_exporter.exported_materials[mat.name])

                    if mat.name in self.material_exporter.emission_scales.keys():
                        em = self.material_exporter.emission_scales[mat.name]

                        if em[0] == 'luminous_flux':
                            measure = Measure.LUMINOUS_FLUX
                        elif em[0] == 'luminous_intensity':
                            measure = Measure.LUMINOUS_INTENSITY
                        elif em[0] == 'luminance':
                            measure = Measure.LUMINANCE
                        elif em[0] == 'luminous_emittance':
                            measure = Measure.LUMINOUS_EMITTANCE
                        else:
                            measure = Measure.NONE

                        emission_scales.append(EmissionScale(measure, em[1], self.material_exporter.exported_materials[mat.name]))

            
            indigo_model.SetMaterials(materials)
            indigo_model.SetEmissionScales(emission_scales)

            self.exported_objects[name] = indigo_model
            #print("Added model %s..." % obj.name)

            return True
        return False

    def update_render_passes(self, scene=None, renderlayer=None):
        self.register_pass(scene, renderlayer, "Combined", 4, "RGBA", 'COLOR')
        
        if scene:
            aovs = scene.indigo_engine.aovs
            for aov in indigo_aovs.keys():
                if getattr(aovs, aov):
                    self.register_pass(scene, renderlayer, indigo_aovs[aov].name, indigo_aovs[aov].num_components, indigo_aovs[aov].channel_ids, indigo_aovs[aov].channel_type)

    def __init__(self):

        self.ctx = None

        if self.ctx is None:
            self.ctx = Context()
            '''
            Find Indigo binaries and data
            '''
            directory = os.path.dirname(os.path.realpath(blendigo.pyIndigo.__file__))
            indigo_dll_path = os.path.join(directory, 'bin')
            appdata_path = os.path.join(directory, 'bin')

            res = self.ctx.Initialize(indigo_dll_path, appdata_path)
            if res == -1:
                print ("Indigo Context failed to initialize. Check paths.")
                return

        '''
        Load preview scene
        '''
        self.indigo_preview_scene = None
        self.indigo_preview_sphere = None
        self.indigo_preview_base = None
        self.indigo_preview_material = None

        scene_path = r"C:\git\pyIndigo\pyIndigo\bin\data\preview_scenes\mat_db\matpreviewscene_igmesh.igs"
        scene_dir = r"C:\git\pyIndigo\pyIndigo\bin\data\preview_scenes\mat_db"
        indigo_dir = r"C:\git\pyIndigo\pyIndigo\bin"

        self.indigo_preview_scene = Scene.FromFile(scene_path, scene_dir, indigo_dir)

        self.preview_sphere = self.indigo_preview_scene.GetModel("preview_sphere instance")
        self.preview_base = self.indigo_preview_scene.GetModel("preview_base instance")

        self.scene = None
        self.exported_meshes = {}
        self.exported_objects = {}
        #self.cancel_token = False
        self.is_initialized = False

        self.scene_data = None
        self.draw_data = None        

    def chunks(self, l, n):
        for i in range(0, len(l), n):
            yield l[i:i+n]        

    def update(self, data, scene):
        pass

    def render(self, depsgraph):

        self.scene = depsgraph.scene
        render_settings = self.scene.indigo_engine
        scale = render_settings.buffer_multiplier
        active_aovs = {}
        logs = True

        region = (0, self.resolution_x, 0, self.resolution_y)
        render_size = (self.resolution_x, self.resolution_y)        

        self.exported_meshes = {}
        self.exported_objects = {}
        self.material_exporter = ShaderNodeExporter()

        if self.is_preview:
            logs = False
            material = None
            for instance in depsgraph.object_instances:
                if instance.object.name == "preview_sphere":
                    material = instance.object.data.materials[0]
                    break

            self.material_exporter.export(material)
            
            indigo_material = self.material_exporter.exported_materials[material.name]

            self.indigo_preview_scene.AddMaterial(indigo_material)
            self.preview_base.SetMaterials([indigo_material])    
            self.preview_sphere.SetMaterials([indigo_material])

            indigo_render_settings = self.indigo_preview_scene.GetRenderSettings()
            indigo_render_settings.width = self.resolution_x
            indigo_render_settings.height = self.resolution_y

            tm = self.indigo_preview_scene.GetTonemapping()
            tm.type = TONEMAPPING_TYPE['Linear']
            tm.scale = 3 / scale

            indigo_scene = self.indigo_preview_scene

        else:
            '''
            Set Indigo render settings
            '''
            indigo_render_settings = RenderSettings()
            indigo_render_settings.width = self.resolution_x
            indigo_render_settings.height = self.resolution_y

            if self.scene.render.use_border:

                x1 = int(bpy.context.scene.render.border_min_x * self.resolution_x)
                x2 = int(bpy.context.scene.render.border_max_x * self.resolution_x)
                y1 = int(bpy.context.scene.render.border_min_y * self.resolution_y)
                y2 = int(bpy.context.scene.render.border_max_y * self.resolution_y)
                indigo_render_settings.set_render_region(x1, x2, y1, y2)

                print("Render region: {0} {1} {2} {3}".format(x1, x2, y1, y2))
                region = (x1, x2, y1, y2)
                render_size = (x2-x1, y2-y1)

            indigo_render_settings.metropolis = render_settings.metropolis
            indigo_render_settings.bidirectional = render_settings.bidirectional
            indigo_render_settings.vignetting = self.scene.camera.data.indigo_camera.vignetting
            indigo_render_settings.halt_samples = render_settings.haltspp
            indigo_render_settings.halt_time = render_settings.halttime
            indigo_render_settings.supersampling = render_settings.supersampling
            indigo_render_settings.foreground_alpha = render_settings.foreground_alpha
            indigo_render_settings.splat_filter = render_settings.splat_filter
            indigo_render_settings.downsize_filter = render_settings.downsize_filter

            #indigo_render_settings.use_subres_rendering = True


            '''
            Add render channels
            '''
            aovs = self.scene.indigo_engine.aovs

            for aov in indigo_aovs.keys():
                # TODO: Add special cases for Object and Material IDs
                if getattr(aovs, aov):
                    if indigo_aovs[aov].name == "Depth":
                        active_aovs[aov] = indigo_aovs[aov]
                        indigo_render_settings.depth_channel = True
                        continue                
                    self.add_pass(indigo_aovs[aov].name, indigo_aovs[aov].num_components, indigo_aovs[aov].channel_ids)
                    if hasattr(indigo_render_settings, aov):
                        setattr(indigo_render_settings, aov, True)
                        active_aovs[aov] = indigo_aovs[aov]

            '''
            Create Indigo Scene
            '''
            indigo_scene = Scene.New()
            indigo_scene.AddRenderSettings(indigo_render_settings)
            

            '''
            Export materials, objects, and mediums
            '''

            '''
            for medium in self.scene.indigo_material_medium.medium:
               print (medium.name)
               indigo_medium = SceneNodeMedium(medium.name, Medium.Basic(medium.name, medium.medium_ior, medium.precedence))
               self.material_exporter.exported_mediums[medium.name] = indigo_medium
            '''
               
            for instance in depsgraph.object_instances:
                if self.test_break():
                    return

                if instance.is_instance:
                    self.export_object(instance.object, instance.matrix_world, instance.object.name + "_({})".format(instance.random_id))
                else:
                    self.export_object(instance.object, instance.matrix_world)

            for mesh in self.exported_meshes:
                indigo_scene.AddMesh(self.exported_meshes[mesh])

            for obj in self.exported_objects:
                indigo_scene.AddModel(self.exported_objects[obj])

            for med in self.material_exporter.exported_mediums:
                indigo_scene.AddMedium(self.material_exporter.exported_mediums[med])

            for mat in self.material_exporter.exported_materials:
                indigo_scene.AddMaterial(self.material_exporter.exported_materials[mat])

            '''
            Export tonemapping
            '''
            tm = Tonemapping()
            tm.type = TONEMAPPING_TYPE['Linear']
            tm.iso = self.scene.camera.data.indigo_camera.iso
            #tm.ev = self.scene.camera.data.indigo_tonemapping.camera_ev

            tm.scale = 1 / scale

            '''
            Export camera
            '''            
            cam = export_camera(bpy.context.scene.camera)
            indigo_scene.AddCamera(cam)

            '''
            Export background
            '''
            bg = export_background(depsgraph)
            if bg is not None:
                indigo_scene.AddBackground(bg)

            indigo_scene.AddTonemapping(tm)

            '''
            Launch Indigo externally
            '''
            if render_settings.write_to_xml:
                igs_name = "Blendigo280_test"
                igs_path = os.path.join("C:/tmp", igs_name + ".igs")
                print ("Writing to XML...")
                indigo_scene.WriteToXML(igs_path)

                if render_settings.external:
                    import subprocess
                    tm.scale = 1.0

                    subprocess.run(["C:\\Program Files\\Indigo Renderer\\indigo.exe", igs_path])
                    return

        '''
        Launch Indigo internally
        '''
        self.indigo_renderer = Renderer(self.ctx, self.resolution_x, self.resolution_y)

        float_buffer = FloatBuffer()
        uint8_buffer = UInt8Buffer()
        render_buffer = RenderBuffer(indigo_scene)

        tone_mapper = ToneMapper(self.ctx, render_buffer, uint8_buffer, float_buffer)
        tone_mapper.SetSourceRenderChannel(0)

        tone_mapper.Update(indigo_scene)


        self.indigo_renderer.InitializeWithScene(self.ctx, indigo_scene, render_buffer, tone_mapper)
        self.indigo_renderer.Start()
        #self.indigo_renderer.realtime = True

        max_pass = 20
        current_pass = 0

        float_buffer.create_dummy( self.resolution_x, self.resolution_y, 4)
        uint8_buffer.create_dummy( self.resolution_x, self.resolution_y, 4)

        shape = int(self.resolution_x * self.resolution_y)
        shape_x = int(self.resolution_x)
        shape_y = int(self.resolution_y)

        interval = 1.0

        if render_settings.haltspp < 1:
            haltspp = 1000
        else:
            haltspp = render_settings.haltspp

        print ("Region: ", region)

        while self.test_break() is False:

            start = time.time()
            self.indigo_renderer.Poll(logs)

            if tone_mapper.IsImageFresh():

                result = self.begin_result(0, 0, self.resolution_x, self.resolution_y)
                #result = self.begin_result(region[0], region[2], region[1], region[3])

                '''
                Get master channel
                '''

                tone_mapper.SetSourceRenderChannel(0)
                tone_mapper.TonemapBlocking()

                if float_buffer.width > 0 and float_buffer.height > 0:

                    #raw_pixels = np.ctypeslib.as_array(float_buffer.get_flipped(), (shape_x, shape_y, 4))
                    #raw_pixels = np.ctypeslib.as_array(float_buffer.get_flipped(), (float_buffer.width, float_buffer.height, float_buffer.num_components))

                    #pixels = np.multiply(raw_pixels, np.array([scale, scale, scale, 1]))

                    pixels = np.ctypeslib.as_array(float_buffer.get_data_pointer(), (float_buffer.width, float_buffer.height, float_buffer.num_components))
                    #pixels = pixels[region[0]:region[1], region[2]:region[3],:]

                    #pixels.shape = ((region[1] - region[0]) * (region[3] - region[2]), float_buffer.num_components)
                    pixels.shape = (float_buffer.width * float_buffer.height, float_buffer.num_components)
                    pixels = np.multiply(pixels, np.array([scale, scale, scale, 1]))

                    result.layers[0].passes["Combined"].rect = pixels
                    

                    '''
                    Get other channels
                    '''
                    for aov in active_aovs.keys():
                        if self.test_break():
                            break

                        #print ("Channel: {0}, {1}".format(active_aovs[aov].name, active_aovs[aov].indigo_id.value))

                        tone_mapper.SetSourceRenderChannel(active_aovs[aov].indigo_id.value)
                        tone_mapper.TonemapBlocking()
                      
                        #raw_pixels = np.ctypeslib.as_array(float_buffer.get_flipped(), (float_buffer.width, float_buffer.height, float_buffer.num_components))
                        #raw_pixels = np.ctypeslib.as_array(float_buffer.get_flipped(), (shape_x, shape_y, active_aovs[aov].num_components))

                        #if active_aovs[aov].channel_type == 'RGBA':
                        #    pixels = np.multiply(raw_pixels, np.array([scale, scale, scale, 1]))

                        pixels = np.ctypeslib.as_array(float_buffer.get_data_pointer(), (float_buffer.width, float_buffer.height, float_buffer.num_components))
                        #pixels = pixels[region[0]:region[1], region[2]:region[3],:]

                        #pixels.shape = ((region[1] - region[0]) * (region[3] - region[2]), float_buffer.num_components)
                        pixels.shape = (shape, float_buffer.num_components)

                        if active_aovs[aov].scale_values:
                            pixels = np.multiply(pixels, np.array([scale, scale, scale, 1]))

                        result.layers[0].passes[active_aovs[aov].name].rect = pixels
                    

                self.end_result(result)
                self.update_stats("SPP: %.2f" % self.indigo_renderer.samples_per_pixel, "Num. passes: %i" % current_pass)


            if self.indigo_renderer.samples_per_pixel > haltspp:
                break
                
            current_pass += 1

            while time.time()-start < interval and self.test_break() is False:
                time.sleep(0.03)
                if self.indigo_renderer.samples_per_pixel > haltspp:
                   break

            if (interval < 90):
                interval *= 1.25
        if logs:
            print("Stopping...")    
            print("Num passes: %i" % current_pass)
        
        self.indigo_renderer.Stop()
        self.indigo_renderer.Poll()
        self.indigo_renderer.Shutdown()        
        return

    # For viewport renders, this method gets called once at the start and
    # whenever the scene or 3D viewport changes. This method is where data
    # should be read from Blender in the same thread. Typically a render
    # thread will be started to do the work while keeping Blender responsive.
    def view_update(self, context, depsgraph):
        region = context.region
        view3d = context.space_data
        scene = depsgraph.scene

        print(scene.camera)

        # Get viewport dimensions
        dimensions = region.width, region.height

        if not self.scene_data:
            # First time initialization
            self.scene_data = []
            first_time = True

            # Loop over all datablocks used in the scene.
            for datablock in depsgraph.ids:
                pass
        else:
            first_time = False

            # Test which datablocks changed
            for update in depsgraph.updates:
                print("Datablock updated: ", update.id.name)

            # Test if any material was added, removed or changed.
            if depsgraph.id_type_updated('MATERIAL'):
                print("Materials updated")

        # Loop over all object instances in the scene.
        if first_time or depsgraph.id_type_updated('OBJECT'):
            for instance in depsgraph.object_instances:
                pass

    # For viewport renders, this method is called whenever Blender redraws
    # the 3D viewport. The renderer is expected to quickly draw the render
    # with OpenGL, and not perform other expensive work.
    # Blender will draw overlays for selection and editing on top of the
    # rendered image automatically.
    def view_draw(self, context, depsgraph):
        region = context.region
        scene = depsgraph.scene

        # Get viewport dimensions
        dimensions = region.width, region.height

        # Bind shader that converts from scene linear to display space,
        bgl.glEnable(bgl.GL_BLEND)
        bgl.glBlendFunc(bgl.GL_ONE, bgl.GL_ONE_MINUS_SRC_ALPHA);
        self.bind_display_space_shader(scene)

        if not self.draw_data or self.draw_data.dimensions != dimensions:
            self.draw_data = CustomDrawData(dimensions)

        self.draw_data.draw()

        self.unbind_display_space_shader()
        bgl.glDisable(bgl.GL_BLEND)

    def __del__(self):
        pass


class CustomDrawData:
    def __init__(self, dimensions):
        # Generate dummy float image buffer
        self.dimensions = dimensions
        width, height = dimensions

        pixels = [0.1, 0.2, 0.1, 1.0] * width * height
        pixels = bgl.Buffer(bgl.GL_FLOAT, width * height * 4, pixels)

        # Generate texture
        self.texture = bgl.Buffer(bgl.GL_INT, 1)
        bgl.glGenTextures(1, self.texture)
        bgl.glActiveTexture(bgl.GL_TEXTURE0)
        bgl.glBindTexture(bgl.GL_TEXTURE_2D, self.texture[0])
        bgl.glTexImage2D(bgl.GL_TEXTURE_2D, 0, bgl.GL_RGBA16F, width, height, 0, bgl.GL_RGBA, bgl.GL_FLOAT, pixels)
        bgl.glTexParameteri(bgl.GL_TEXTURE_2D, bgl.GL_TEXTURE_MIN_FILTER, bgl.GL_LINEAR)
        bgl.glTexParameteri(bgl.GL_TEXTURE_2D, bgl.GL_TEXTURE_MAG_FILTER, bgl.GL_LINEAR)
        bgl.glBindTexture(bgl.GL_TEXTURE_2D, 0)

        # Bind shader that converts from scene linear to display space,
        # use the scene's color management settings.
        shader_program = bgl.Buffer(bgl.GL_INT, 1)
        bgl.glGetIntegerv(bgl.GL_CURRENT_PROGRAM, shader_program);

        # Generate vertex array
        self.vertex_array = bgl.Buffer(bgl.GL_INT, 1)
        bgl.glGenVertexArrays(1, self.vertex_array)
        bgl.glBindVertexArray(self.vertex_array[0])

        texturecoord_location = bgl.glGetAttribLocation(shader_program[0], "texCoord");
        position_location = bgl.glGetAttribLocation(shader_program[0], "pos");

        bgl.glEnableVertexAttribArray(texturecoord_location);
        bgl.glEnableVertexAttribArray(position_location);

        # Generate geometry buffers for drawing textured quad
        position = [0.0, 0.0, width, 0.0, width, height, 0.0, height]
        position = bgl.Buffer(bgl.GL_FLOAT, len(position), position)
        texcoord = [0.0, 0.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0]
        texcoord = bgl.Buffer(bgl.GL_FLOAT, len(texcoord), texcoord)

        self.vertex_buffer = bgl.Buffer(bgl.GL_INT, 2)

        bgl.glGenBuffers(2, self.vertex_buffer)
        bgl.glBindBuffer(bgl.GL_ARRAY_BUFFER, self.vertex_buffer[0])
        bgl.glBufferData(bgl.GL_ARRAY_BUFFER, 32, position, bgl.GL_STATIC_DRAW)
        bgl.glVertexAttribPointer(position_location, 2, bgl.GL_FLOAT, bgl.GL_FALSE, 0, None)

        bgl.glBindBuffer(bgl.GL_ARRAY_BUFFER, self.vertex_buffer[1])
        bgl.glBufferData(bgl.GL_ARRAY_BUFFER, 32, texcoord, bgl.GL_STATIC_DRAW)
        bgl.glVertexAttribPointer(texturecoord_location, 2, bgl.GL_FLOAT, bgl.GL_FALSE, 0, None)

        bgl.glBindBuffer(bgl.GL_ARRAY_BUFFER, 0)
        bgl.glBindVertexArray(0)

    def __del__(self):
        bgl.glDeleteBuffers(2, self.vertex_buffer)
        bgl.glDeleteVertexArrays(1, self.vertex_array)
        bgl.glBindTexture(bgl.GL_TEXTURE_2D, 0)
        bgl.glDeleteTextures(1, self.texture)

    def draw(self):
        bgl.glActiveTexture(bgl.GL_TEXTURE0)
        bgl.glBindTexture(bgl.GL_TEXTURE_2D, self.texture[0])
        bgl.glBindVertexArray(self.vertex_array[0])
        bgl.glDrawArrays(bgl.GL_TRIANGLE_FAN, 0, 4);
        bgl.glBindVertexArray(0)
        bgl.glBindTexture(bgl.GL_TEXTURE_2D, 0)