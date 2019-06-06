import bpy
from bpy.types import NodeTree, Node, NodeSocket, ShaderNodeTree

from ..pyIndigo.Param import * 

from .base import IndigoShaderNode

class IndigoParamRGBShaderNode(Node, IndigoShaderNode):

    bl_idname = 'IndigoParamRGBShaderNode'
    bl_label = 'Indigo RGB Parameter'
    bl_icon = 'SOUND'

    indigo_type = 'INDIGO_PARAM'

    gain: bpy.props.FloatProperty(
        name="Gain", 
        default=1.0, 
        min=0.0, 
        max=2.0,
        )

    exp: bpy.props.IntProperty(
        name="10^",
        default=7,
        min=-30,
        max=30,
        )

    def init(self, context):
        self.inputs.new('NodeSocketColor', "Color")

        self.outputs.new('NodeSocketShader', "RGB")

    def convert(self):
        print("Converting (IndigoParamRGBShaderNode)")


        multiplier = self.gain * (10 ** self.exp)

        inp = self.inputs['Color']
        if len(inp.links) > 0:
            node = inp.links[0].from_node
            if node.type == 'TEX_IMAGE':
                if node.image:
                    return WavelengthDependentParam.Texture(bpy.path.abspath(node.image.filepath), 2.2, 0, multiplier, 0)
            elif hasattr(node, 'indigo_type') and node.indigo_type == 'INDIGO_TEXTURE':
                print("  GOT TEXTURE PATH ({}): {}".format(self.name, node._texture_path()))
                node = inp.links[0].from_node
                return WavelengthDependentParam.Texture(node._texture_path(), node.gamma, node.a, node.b * multiplier, node.c)

        col = inp.default_value
        return WavelengthDependentParam.RGB(col[0] * multiplier, col[1] * multiplier, col[2] * multiplier, 1.0)


    def copy(self, node):
        print("Copying from node ", node)

    def free(self):
        print("Removing node ", self, ", Goodbye!")

    def draw_buttons(self, context, layout):
        layout.prop(self, "gain")
        layout.prop(self, "exp")

    def draw_buttons_ext(self, context, layout):
        pass

    def draw_label(self):
        return "Indigo RGB Parameter"

