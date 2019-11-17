import bpy
from bpy.types import NodeTree, Node, NodeSocket, ShaderNodeTree

from ..pyIndigo.Materials import ExitPortalMaterial

from .base import IndigoShaderNode

class IndigoExitPortalShaderNode(Node, IndigoShaderNode):
    # === Basics ===
    # Description string
    '''A custom node'''
    # Optional identifier string. If not explicitly defined, the python class name is used.
    bl_idname = 'IndigoExitPortalShaderNode'
    bl_label = 'Indigo Exit Portal'
    bl_icon = 'SOUND'
 

    indigo_type = 'INDIGO_EXIT_PORTAL'

    def init(self, context):


        self.outputs.new('NodeSocketShader', "Exit Portal")


    def convert(self, name, exporter):

        indigo_material = ExitPortalMaterial(name)

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
        return "Indigo Exit Portal"