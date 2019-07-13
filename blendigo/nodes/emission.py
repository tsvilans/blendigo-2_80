import bpy
from bpy.types import NodeTree, Node, NodeSocket, ShaderNodeTree
from bpy.props import BoolProperty, FloatProperty, EnumProperty

from ..pyIndigo.Materials import SpecularMaterial, Medium, SceneNodeMedium
from ..pyIndigo.Param import * 

from .base import IndigoShaderNode

'''
class IndigoEmissionScaleProperties(bpy.types.PropertyGroup):
    enabled: bpy.props.BoolProperty(
        name="Enabled",
        description="Use emission scaling.",
        default=False,
        )

    value: bpy.props.FloatProperty(
        name="Value",
        description="Value of emission in specified units.",
        default=1,
        )

    units: bpy.props.EnumProperty(
        name="Units",
        description="Units for emission scale.",
        items={
        ('luminous_flux', 'lm', 'Luminous flux'),
        ('luminous_intensity', 'cd', 'Luminous intensity (lm/sr)'),
        ('luminance', 'nits', 'Luminance (lm/sr/m/m)'),
        ('luminous_emittance', 'lux', 'Luminous emittance (lm/m/m)')},
        default='luminous_emittance')
'''
class IndigoEmissionShaderNode(Node, IndigoShaderNode):

    bl_idname = 'IndigoEmissionShaderNode'
    bl_label = 'Indigo Emission'
    bl_icon = 'SOUND'

    #emission_scale: bpy.props.PointerProperty(type=IndigoEmissionScaleProperties)

    enabled: bpy.props.BoolProperty(
        name="Emission scale",
        description="Use emission scaling.",
        default=False,
        )

    value: bpy.props.FloatProperty(
        name="Value",
        description="Value of emission in specified units.",
        default=1,
        )

    exp: bpy.props.IntProperty(
        name="10^",
        default=5,
        min=-30,
        max=30,
        )    

    units: bpy.props.EnumProperty(
        name="Units",
        description="Units for emission scale.",
        items={
        ('luminous_flux', 'lm', 'Luminous flux (lm)'),
        ('luminous_intensity', 'cd', 'Luminous intensity (lm/sr)'),
        ('luminance', 'nits', 'Luminance (lm/sr/m/m)'),
        ('luminous_emittance', 'lux', 'Luminous emittance (lm/m/m)')},
        default='luminous_emittance')

    indigo_type = 'INDIGO_EMISSION'


    def init(self, context):
        self.inputs.new('NodeSocketShader', "Emission")
        self.inputs.new('NodeSocketShader', "Base Emission")

        self.outputs.new('NodeSocketShader', "Emission")

    def convert(self):
        #print("Converting (IndigoEmissionShaderNode)")

        emission = None
        base_emission = None
        emission_scale = None

        if self.enabled:
            emission_scale = (self.units, self.value * (10 ** self.exp))

        inp = self.inputs['Emission']
        if len(inp.links) < 1:
            pass
        else:
            node = inp.links[0].from_node            
            if hasattr(node, 'indigo_type') and node.indigo_type == 'INDIGO_PARAM':
                node = inp.links[0].from_node
                emission = node.convert()

        inp = self.inputs['Base Emission']
        if len(inp.links) < 1:
            pass
        else:
            node = inp.links[0].from_node               
            if hasattr(node, 'indigo_type') and node.indigo_type == 'INDIGO_PARAM':
                node = inp.links[0].from_node
                base_emission = node.convert()

        return (emission, base_emission, emission_scale)

    def copy(self, node):
        print("Copying from node ", node)

    def free(self):
        print("Removing node ", self, ", Goodbye!")

    def draw_buttons(self, context, layout):
        layout.prop(self, "enabled")
        layout.prop(self, "value")
        layout.prop(self, "exp")
        layout.prop(self, "units")

    def draw_buttons_ext(self, context, layout):
        pass

    def draw_label(self):
        return "Indigo Emission"

