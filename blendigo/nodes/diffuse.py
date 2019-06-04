import bpy
from bpy.types import NodeTree, Node, NodeSocket, ShaderNodeTree

from ..pyIndigo.Materials import DiffuseMaterial
from ..pyIndigo.Param import * 

from .base import IndigoShaderNode

class IndigoDiffuseShaderNode(Node, IndigoShaderNode):

    bl_idname = 'IndigoDiffuseShaderNode'
    bl_label = 'Indigo Diffuse'
    bl_icon = 'SOUND'

    
    albedo: bpy.props.FloatVectorProperty()

    indigo_type = 'INDIGO_DIFFUSE'

    def init(self, context):
        socket = self.inputs.new('NodeSocketColor', "Albedo")  
        socket.default_value = (0.8, 0.8, 0.8, 1.0)

        self._create_common_inputs()

        self.outputs.new('NodeSocketShader', "Diffuse")


    def convert(self, name):
        print("Converting {} (IndigoDiffuseShaderNode)".format(name))

        indigo_material = DiffuseMaterial(name)

        inp = self.inputs['Albedo']

        if len(inp.links) < 1:
            indigo_material.albedo = WavelengthDependentParam.RGB(inp.default_value[0], inp.default_value[1], inp.default_value[2], 1.0)
        else:
            node = inp.links[0].from_node
            if node.type == 'TEX_IMAGE':
                if node.image:
                    indigo_material.albedo = WavelengthDependentParam.Texture(bpy.path.abspath(node.image.filepath), 2.2, 0, 1.0, 0)
            elif hasattr(node, 'indigo_type') and node.indigo_type == 'INDIGO_TEXTURE':
                print("  GOT TEXTURE PATH ({}): {}".format(self.name, node._texture_path()))
                node = inp.links[0].from_node
                indigo_material.albedo = WavelengthDependentParam.Texture(node._texture_path(), node.gamma, node.a, node.b, node.c)

        self._convert_common_inputs(indigo_material)

        return indigo_material


    def copy(self, node):
        print("Copying from node ", node)

    def free(self):
        print("Removing node ", self, ", Goodbye!")

    def draw_buttons(self, context, layout):
        pass

    def draw_buttons_ext(self, context, layout):
        pass

    def draw_label(self):
        return "Indigo Diffuse"

