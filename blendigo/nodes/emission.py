import bpy
from bpy.types import NodeTree, Node, NodeSocket, ShaderNodeTree, BoolProperty

from ..pyIndigo.Materials import SpecularMaterial, Medium, SceneNodeMedium
from ..pyIndigo.Param import * 

from .base import IndigoShaderNode

class IndigoEmissionShaderNode(Node, IndigoShaderNode):

    bl_idname = 'IndigoEmissionShaderNode'
    bl_label = 'Indigo Emission'
    bl_icon = 'SOUND'

    indigo_type = 'INDIGO_EMISSION'

    def init(self, context):
        self.inputs.new('NodeSocketShader', "Emission")
        self.inputs.new('NodeSocketShader', "Base Emission")

        self.outputs.new('NodeSocketShader', "Emission")

    def convert(self):
        print("Converting (IndigoEmissionShaderNode)")


        emission = None
        base_emission = None

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

        return (emission, base_emission)

    def copy(self, node):
        print("Copying from node ", node)

    def free(self):
        print("Removing node ", self, ", Goodbye!")

    def draw_buttons(self, context, layout):
        pass

    def draw_buttons_ext(self, context, layout):
        pass

    def draw_label(self):
        return "Indigo Emission"

