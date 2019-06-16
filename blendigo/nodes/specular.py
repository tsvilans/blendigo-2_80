import bpy
from bpy.types import NodeTree, Node, NodeSocket, ShaderNodeTree, BoolProperty

from ..pyIndigo.Materials import SpecularMaterial, Medium, SceneNodeMedium
from ..pyIndigo.Param import * 

from .base import IndigoShaderNode

class IndigoSpecularShaderNode(Node, IndigoShaderNode):

    bl_idname = 'IndigoSpecularShaderNode'
    bl_label = 'Indigo Specular'
    bl_icon = 'SOUND'

    
    arch_glass: bpy.props.BoolProperty()
    transparent: bpy.props.BoolProperty()

    indigo_type = 'INDIGO_SPECULAR'

    def init(self, context):
        self.inputs.new('NodeSocketShader', "Medium")
        self.inputs.new('NodeSocketShader', "Absorption")

        self._create_common_inputs()

        self.outputs.new('NodeSocketShader', "Specular")

    def convert(self, name, exporter):
        print("Converting {} (IndigoSpecularShaderNode)".format(name))


        medium = Medium.Basic("DefaultMedium", 1.5, 10)
        medium_node = SceneNodeMedium("DefaultMedium", medium)

        indigo_material = SpecularMaterial(name, medium_node)

        indigo_material.arch_glass = self.arch_glass
        indigo_material.transparent = self.transparent

        '''
        inp = self.inputs['Medium']
        
        inp = self.inputs['Absorption']

        if len(inp.links) < 1:
            pass
            #indigo_material.bump = WavelengthIndependentParam.Uniform(inp.default_value)
        elif inp.links[0].from_node.type == 'TEX_IMAGE':
            tex = inp.links[0].from_node
            if tex.image:
                indigo_material.bump = WavelengthIndependentParam.Texture(bpy.path.abspath(tex.image.filepath), 2.2, 0, 1.0, 0)
        '''

        return indigo_material


    def copy(self, node):
        print("Copying from node ", node)

    def free(self):
        print("Removing node ", self, ", Goodbye!")

    def draw_buttons(self, context, layout):
        #layout.label(text="Node settings")
        layout.prop(self, "arch_glass")
        layout.prop(self, "transparent")

    def draw_buttons_ext(self, context, layout):
        pass

    def draw_label(self):
        return "Indigo Specular"

