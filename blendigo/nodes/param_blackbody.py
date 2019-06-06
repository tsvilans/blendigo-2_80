import bpy
from bpy.types import NodeTree, Node, NodeSocket, ShaderNodeTree

from ..pyIndigo.Param import * 

from .base import IndigoShaderNode

class IndigoParamBlackbodyShaderNode(Node, IndigoShaderNode):

    bl_idname = 'IndigoParamBlackbodyShaderNode'
    bl_label = 'Indigo Blackbody Parameter'
    bl_icon = 'SOUND'

    indigo_type = 'INDIGO_PARAM'

    temperature: bpy.props.FloatProperty(
        name="Temperature", 
        default=6500, 
        min=2000, 
        max=20000,
        )

    gain: bpy.props.FloatProperty(
        name="Gain", 
        default=1.0, 
        min=0.0, 
        max=2.0,
        )

    exp: bpy.props.IntProperty(
        name="^10",
        default=1,
        min=-10,
        max=10,
        )

    def init(self, context):

        self.outputs.new('NodeSocketShader', "Blackbody")

    def convert(self):
        print("Converting (IndigoParamBlackbodyShaderNode)")

        return WavelengthDependentParam.Blackbody(self.temperature, self.gain * (10 ** self.exp))

    def copy(self, node):
        print("Copying from node ", node)

    def free(self):
        print("Removing node ", self, ", Goodbye!")

    def draw_buttons(self, context, layout):
        layout.prop(self, "temperature")
        layout.prop(self, "gain")
        layout.prop(self, "exp")

    def draw_buttons_ext(self, context, layout):
        pass

    def draw_label(self):
        return "Indigo Blackbody Parameter"

