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
 

    ior: bpy.props.FloatProperty(
        name="IOR", 
        min=1.0, 
        default=1.3,
        )

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


    def convert(self, name, exporter):
        #print("Converting {} (IndigoPhongShaderNode)".format(name))

        indigo_material = PhongMaterial(name, self.ior)

        albedo = self._process_input('Albedo', WavelengthDependentParam, WavelengthDependentParam.Uniform(0.7), False)
        if albedo:
            indigo_material.albedo = albedo

        fresnel_scale = self._process_input('Fresnel Scale', WavelengthIndependentParam, WavelengthIndependentParam.Uniform(0.7), False)
        if fresnel_scale:
            indigo_material.fresnel_scale = fresnel_scale            

        roughness = self._process_input('Roughness', WavelengthIndependentParam, WavelengthIndependentParam.Uniform(0.7), False)
        if roughness:
            indigo_material.roughness = roughness   
            
        self._convert_common_inputs(indigo_material, name, exporter)

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