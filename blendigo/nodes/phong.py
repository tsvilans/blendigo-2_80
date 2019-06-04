import bpy
from bpy.types import NodeTree, Node, NodeSocket, ShaderNodeTree

from ..pyIndigo.Materials import PhongMaterial
from ..pyIndigo.Param import * 

from .base import IndigoShaderNode

class IndigoPhongShaderNode(Node, IndigoShaderNode):
    # === Basics ===
    # Description string
    '''A custom node'''
    # Optional identifier string. If not explicitly defined, the python class name is used.
    bl_idname = 'IndigoPhongShaderNode'
    bl_label = 'Indigo Phong'
    bl_icon = 'SOUND'
 

    ior: bpy.props.FloatProperty(name="IOR", min=1.0, default=1.3)

    indigo_type = 'INDIGO_PHONG'

    def init(self, context):
        socket = self.inputs.new('NodeSocketColor', "Albedo")
        socket.default_value = (0.8, 0.8, 0.8, 1.0)

        socket = self.inputs.new('NodeSocketFloat', "Roughness")
        socket.default_value = 0.3

        socket = self.inputs.new('NodeSocketFloat', "Fresnel Scale")
        socket.default_value = 1.0
        #self.inputs.new('NodeSocketFloat', "IOR")

        self._create_common_inputs()

        self.outputs.new('NodeSocketShader', "Phong")


    def convert(self, name):

        print("Converting {} (IndigoPhongShaderNode)".format(name))

        #indigo_material = PhongMaterial(name, self.inputs['IOR'].default_value)
        indigo_material = PhongMaterial(name, self.ior)

        inp = self.inputs['Roughness']

        if len(inp.links) < 1:
            indigo_material.roughness = WavelengthIndependentParam.Uniform(inp.default_value)
        else:
            node = inp.links[0].from_node
            if node.type == 'TEX_IMAGE':
                if node.image:
                    indigo_material.roughness = WavelengthIndependentParam.Texture(bpy.path.abspath(node.image.filepath), 2.2, 0, 1.0, 0)
            elif hasattr(node, 'indigo_type') and node.indigo_type == 'INDIGO_TEXTURE':
                node = inp.links[0].from_node
                indigo_material.roughness = WavelengthIndependentParam.Texture(node._texture_path(), node.gamma, node.a, node.b, node.c)

        inp = self.inputs['Fresnel Scale']

        if len(inp.links) < 1:
            indigo_material.fresnel_scale = WavelengthIndependentParam.Uniform(inp.default_value)
        else:
            node = inp.links[0].from_node
            if node.type == 'TEX_IMAGE':
                if node.image:
                    indigo_material.fresnel_scale = WavelengthIndependentParam.Texture(bpy.path.abspath(node.image.filepath), 2.2, 0, 1.0, 0)
            elif hasattr(node, 'indigo_type') and node.indigo_type == 'INDIGO_TEXTURE':
                indigo_material.fresnel_scale = WavelengthIndependentParam.Texture(node._texture_path(), node.gamma, node.a, node.b, node.c)            

        inp = self.inputs['Albedo']

        if len(inp.links) < 1:
            indigo_material.albedo = WavelengthDependentParam.RGB(inp.default_value[0], inp.default_value[1], inp.default_value[2], 1.0)
        else:
            node = inp.links[0].from_node

            if node.type == 'TEX_IMAGE':
                if node.image:
                    indigo_material.albedo = WavelengthDependentParam.Texture(bpy.path.abspath(node.image.filepath), 2.2, 0, 1.0, 0)
            elif hasattr(node, 'indigo_type') and node.indigo_type == 'INDIGO_TEXTURE':
                indigo_material.albedo = WavelengthDependentParam.Texture(node._texture_path(), node.gamma, node.a, node.b, node.c)
              

        return indigo_material


    def copy(self, node):
        print("Copying from node ", node)

    def free(self):
        print("Removing node ", self, ", Goodbye!")

    def draw_buttons(self, context, layout):
        layout.prop(self, "ior")

    def draw_buttons_ext(self, context, layout):
        pass

    def draw_label(self):
        return "Indigo Phong"