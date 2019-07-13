from ..pyIndigo.Materials import * 
from ..pyIndigo.Param import * 

import queue

class ShaderNodeExporter(object):

    def __init__(self):
        self.exported_materials = {}
        self.exported_mediums = {}
        self.emission_scales = {}

        default_material = DiffuseMaterial("Default")
        default_material.albedo = WavelengthDependentParam.RGB(0.7, 0.7, 0.7, 1.0)

        #self.default_material = SceneNodeMaterial("Default", default_material)
        #self.indigo_scene = indigo_scene

    def _default_material(self, name):
        indigo_material = DiffuseMaterial(name)
        indigo_material.albedo = WavelengthDependentParam.RGB(0.7, 0.7, 0.7, 1.0)

        return SceneNodeMaterial(name, indigo_material)

    def export(self, material):
        if material.name in self.exported_materials.keys():
            print("Already exported material {}".format(material.name))
            return

        tree = material.node_tree
        if tree is None:
            self.exported_materials[material.name] = self._default_material(material.name)
            return

        # Find Indigo output
        outputs = [n for n in tree.nodes if n.type == 'OUTPUT_MATERIAL']

        if len(outputs) < 1:
            self.exported_materials[material.name] = self._default_material(material.name)
            return

        indigo_output = outputs[0]

        for o in outputs:
            conn = o.inputs['Surface'].links[0].from_node
            if hasattr(conn, 'indigo_type'):
                indigo_output = o
                break

        main = None
        submats = []

        for l in indigo_output.inputs['Surface'].links:
            if hasattr(l.from_node, 'indigo_type'):

                name = "{}".format(material.name)
                indigo_material = l.from_node.convert(name, self)
                mat_node = SceneNodeMaterial(name, indigo_material)

                self.exported_materials[name] = mat_node
                return
            else:
                self.exported_materials[material.name] = self._default_material(material.name)

class MaterialExporter(object):

    def __init__(self):
        self.exported_mediums = {}
        self.exported_materials = {}

        self.handle_material = {}
        self.handle_material["specular"] = self.handle_specular
        self.handle_material["phong"] = self.handle_phong
        self.handle_material["diffuse"] = self.handle_diffuse
        self.handle_material["coating"] = self.handle_diffuse
        self.handle_material["doublesidedthin"] = self.handle_diffuse
        self.handle_material["blended"] = self.handle_diffuse
        self.handle_material["null"] = self.handle_null
        self.handle_material["fastsss"] = self.handle_diffuse

    def export(self, material):
        if material.name in self.exported_materials.keys():
            print("Duplicate material found... overwriting {}".format(material.name))

        print("Exporting {} ({})".format(material.name, material.indigo_material.type))

        if material.indigo_material.type in self.handle_material:
            indigo_material = self.handle_material[material.indigo_material.type](material)
        else:
            indigo_material = DiffuseMaterial(material.name)
            indigo_material.albedo = WavelengthDependentParam.RGB(col[0], col[1], col[2], 1.0)

        '''
        Handle emission
        '''

        if material.indigo_material.indigo_material_emission.emission_enabled:
            print("Exporting light!")
            if material.indigo_material.indigo_material_emission.emission_SP_type == 'blackbody':
                indigo_material.emission = WavelengthDependentParam.Blackbody(material.indigo_material.indigo_material_emission.emission_SP_blackbody_temp, material.indigo_material.indigo_material_emission.emission_SP_blackbody_gain)
                indigo_material.base_emission = WavelengthDependentParam.Uniform(1.0)
            else:
                emission_color = material.indigo_material.indigo_material_emission.emission_SP_rgb
                indigo_material.emission = WavelengthDependentParam.RGB(emission_color[0], emission_color[1], emission_color[2], 1.0)
                indigo_material.base_emission = WavelengthDependentParam.Uniform(1.0)

        mat_node = SceneNodeMaterial(material.name, indigo_material)
        
        self.exported_materials[material.name] = mat_node  

    def handle_specular(self, material):
            medium_name = material.indigo_material.indigo_material_specular.medium_chooser
            if medium_name == '' or medium_name not in self.exported_mediums:
                if "DefaultMedium" not in self.exported_mediums:
                    medium = SceneNodeMedium("DefaultMedium", Medium.Basic("DefaultMedium", 1.0, 10))
                    self.exported_mediums["DefaultMedium"] = medium
                    indigo_material = SpecularMaterial(material.name, medium)
                else:
                    indigo_material = SpecularMaterial(material.name, self.exported_mediums["DefaultMedium"])
            else:                    
                indigo_material = SpecularMaterial(material.name, self.exported_mediums[medium_name])

            indigo_material.transparent = material.indigo_material.indigo_material_specular.transparent
            indigo_material.arch_glass = material.indigo_material.indigo_material_specular.arch_glass

            return indigo_material

    def handle_phong(self, material):
            indigo_material = PhongMaterial(material.name, material.indigo_material.indigo_material_phong.ior)

            if material.indigo_material.indigo_material_roughness.roughness_enabled:
                texname = material.indigo_material.indigo_material_roughness.roughness_TX_texture
                if texname:                    
                    tex = bpy.data.textures[texname].indigo_texture
                    indigo_material.roughness = WavelengthIndependentParam.Texture(bpy.path.abspath(tex.path), tex.gamma, tex.A, tex.B, tex.C)
            else:
                indigo_material.roughness = WavelengthIndependentParam.Uniform(material.indigo_material.indigo_material_phong.roughness)
                #print ("   phong roughness {}".format(material.indigo_material.indigo_material_phong.roughness))

            if material.indigo_material.indigo_material_colour.colour_type == "spectrum":
                col = material.indigo_material.indigo_material_colour.colour_SP_rgb
                indigo_material.albedo = WavelengthDependentParam.RGB(col[0], col[1], col[2], 1.0)
            elif material.indigo_material.indigo_material_colour.colour_type == "texture":
                texname = material.indigo_material.indigo_material_colour.colour_TX_texture
                if texname:
                    print ("   albedo texture: " + texname)
                    tex = bpy.data.textures[texname].indigo_texture
                    print ("   " + bpy.path.abspath(tex.path))
                    print ("   gamma %f a %f b %f c %f" % (tex.gamma, tex.A, tex.B, tex.C))
                    indigo_material.albedo = WavelengthDependentParam.Texture(bpy.path.abspath(tex.path), tex.gamma, tex.A, tex.B, tex.C)
                else:
                    #print("   albedo texture failed: " + material.name)
                    col = material.indigo_material.indigo_material_colour.colour_SP_rgb
                    indigo_material.albedo = WavelengthDependentParam.RGB(col[0], col[1], col[2], 1.0)                

            return indigo_material

    def handle_diffuse(self, material):
            indigo_material = DiffuseMaterial(material.name)

            if material.indigo_material.indigo_material_colour.colour_type == "spectrum":
                col = material.indigo_material.indigo_material_colour.colour_SP_rgb
                indigo_material.albedo = WavelengthDependentParam.RGB(col[0], col[1], col[2], 1.0)
            elif material.indigo_material.indigo_material_colour.colour_type == "texture":
                texname = material.indigo_material.indigo_material_colour.colour_TX_texture
                if texname:
                    print ("   albedo texture: " + texname)
                    tex = bpy.data.textures[texname].indigo_texture
                    print ("   " + bpy.path.abspath(tex.path))
                    print ("   gamma %f a %f b %f c %f" % (tex.gamma, tex.A, tex.B, tex.C))
                    indigo_material.albedo = WavelengthDependentParam.Texture(bpy.path.abspath(tex.path), tex.gamma, tex.A, tex.B, tex.C)
                else:
                    print("   albedo texture failed: " + material.name)
                    col = material.indigo_material.indigo_material_colour.colour_SP_rgb
                    indigo_material.albedo = WavelengthDependentParam.RGB(col[0], col[1], col[2], 1.0)

            return indigo_material

    def handle_blend(self, material):
        if material.indigo_material.indigo_material_blended.a_index in self.exported_materials and material.indigo_material.indigo_material_blended.b_index:
            indigo_material = BlendMaterial(material.name, self.exported_materials[material.indigo_material.indigo_material_blended.a_index], self.exported_materials[material.indigo_material.indigo_material_blended.b_index])
            indigo_material.step_blend = material.indigo_material.indigo_material_blended.step
            if material.indigo_material.indigo_material_blendmap.blendmap_enabled:
                texname = material.indigo_material.indigo_material_blendmap.blendmap_TX_texture
                if texname:                    
                    tex = bpy.data.textures[texname].indigo_texture
                    indigo_material.blend = WavelengthIndependentParam.Texture(bpy.path.abspath(tex.path), tex.gamma, tex.A, tex.B, tex.C)

            return indigo_material

    def handle_doublesidedthin(self, material):
        pass

    def handle_null(self, material):
        indigo_material = NullMaterial(material.name)
        return indigo_material

    def handle_exit_portal(self, material):
        indigo_material = ExitPortalMaterial(material.name)
        return indigo_material

class MaterialExporter2(object):
    def __init__(self):
        self.node_exports = {}
        self.node_exports["DIFFUSE_BSDF"] = self.handle_diffuse

    def export(self, material):
        if material.use_nodes:
            self.export_shader_nodes(material)
        else:
            pass

    def export_shader_nodes(self, material):
        tree = material.node_tree

        # Find root node
        root = None
        for node in tree.nodes:
            if node.type == 'OUTPUT_MATERIAL':
                root = node
                break

        if root == None:
            raise Exception("Node tree has no material output.")

        # Build node tree

        indigo_material = self.handle_node(node.inputs['Surface'].links[0].from_node)

    def handle_node(self, node):

        
        if node.type in self.node_exports:
            self.node_exports[node.type](node)
        else:
            # If unsupported node, return default material
            return None

    def handle_diffuse(self, node):
        indigo_material = DiffuseMaterial(node.name)

        # Set diffuse albedo
        input_albedo = node.inputs["Albedo"]
        if len(input_albedo) < 1:
            col = input_albedo.default_value
            indigo_material.albedo = WavelengthDependentParam.RGB(col[0], col[1], col[2], 1.0)
        else:
            # Get albedo input
            pass

        return indigo_material
