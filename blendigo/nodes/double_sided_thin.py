import bpy
from bpy.types import NodeTree, Node, NodeSocket, ShaderNodeTree

from ..pyIndigo.Materials import DoubleSidedThinMaterial, SceneNodeMaterial
from ..pyIndigo.Param import * 

from .base import IndigoShaderNode

class IndigoDoubleSidedThinShaderNode(Node, IndigoShaderNode):

    bl_idname = 'IndigoDoubleSidedThinShaderNode'
    bl_label = 'Indigo Double-Sided Thin'
    bl_icon = 'SOUND'

    
    front_roughness: bpy.props.FloatProperty(
        name="Front roughness",
        description="Front roughness.",
        default=0.8,
        min=0.0,
        max=1.0
        )

    back_roughness: bpy.props.FloatProperty(
        name="Back roughness",
        description="Back roughness.",
        default=0.8,
        min=0.0,
        max=1.0
        )

    reflectance_fraction: bpy.props.FloatProperty(
        name="Reflectance fraction",
        description="Reflectance fraction.",
        default=0.8,
        min=0.0,
        max=1.0
        )

    front_fresnel_scale: bpy.props.FloatProperty(
        name="Front fresnel scale",
        description="Front fresnel scale.",
        default=1.0,
        min=0.0,
        max=1.0
        )

    back_fresnel_scale: bpy.props.FloatProperty(
        name="Back fresnel scale",
        description="Back fresnel scale.",
        default=1.0,
        min=0.0,
        max=1.0
        )

    ior: bpy.props.FloatProperty(
        name="IOR", 
        min=1.0, 
        default=1.3,
        )

    indigo_type = 'INDIGO_DOUBLE_SIDED_THIN'

    def init(self, context):
        socket = self.inputs.new('NodeSocketShader', "Front material")  

        socket = self.inputs.new('NodeSocketShader', "Back material") 

        socket = self.inputs.new('NodeSocketShader', "Transmittance")  

        self._create_common_inputs()

        self.outputs.new('NodeSocketShader', "Double-Sided Thin")


    def convert(self, name, exporter):
        #print("Converting {} (IndigoDoubleSidedThinShaderNode)".format(name))

        indigo_material = DoubleSidedThinMaterial(name)
        indigo_material.back_roughness = WavelengthIndependentParam.Uniform(self.back_roughness)
        indigo_material.back_fresnel_scale = WavelengthIndependentParam.Uniform(self.back_fresnel_scale)
        indigo_material.front_roughness = WavelengthIndependentParam.Uniform(self.front_roughness)
        indigo_material.front_fresnel_scale = WavelengthIndependentParam.Uniform(self.front_fresnel_scale)
        indigo_material.ior = self.ior
        indigo_material.r_f = WavelengthIndependentParam.Uniform(self.reflectance_fraction)

        transmittance = self._process_input('Transmittance', WavelengthIndependentParam, WavelengthDependentParam.Uniform(0.7), False)
        if transmittance:
            indigo_material.transmittance = transmittance

        front_name = name+"_front"
        front_material = self._get_submaterial('Front material', front_name, exporter)
        if front_material:
            mat_node = SceneNodeMaterial(front_name, front_material)
            exporter.exported_materials[front_name] = mat_node
            indigo_material.front_material = mat_node
        else:
            print("          FRONT_MATERIAL FAILED")

        back_name = name+"_back"
        back_material = self._get_submaterial('Back material', back_name, exporter)
        if back_material:
            mat_node = SceneNodeMaterial(back_name, back_material)
            exporter.exported_materials[back_name] = mat_node
            indigo_material.back_material = mat_node
        else:
            print("          BACK_MATERIAL FAILED")

        self._convert_common_inputs(indigo_material, name, exporter)

        return indigo_material


    def copy(self, node):
        print("Copying from node ", node)

    def free(self):
        print("Removing node ", self, ", Goodbye!")

    def draw_buttons(self, context, layout):
        layout.prop(self, "front_roughness")
        layout.prop(self, "back_roughness")
        layout.prop(self, "reflectance_fraction")
        layout.prop(self, "front_fresnel_scale")
        layout.prop(self, "back_fresnel_scale")
        layout.prop(self, "ior")

    def draw_buttons_ext(self, context, layout):
        pass

    def draw_label(self):
        return "Indigo Double-Sided Thin"

