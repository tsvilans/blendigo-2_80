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


    def convert(self, name, exporter):
        #print("Converting {} (IndigoDiffuseShaderNode)".format(name))

        indigo_material = DiffuseMaterial(name)

        albedo = self._process_input('Albedo', WavelengthDependentParam, WavelengthDependentParam.Uniform(0.7), False)
        if albedo:
            indigo_material.albedo = albedo

        self._convert_common_inputs(indigo_material, name, exporter)

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

