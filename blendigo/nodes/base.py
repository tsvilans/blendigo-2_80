import bpy
from bpy.types import NodeTree, Node, NodeSocket, ShaderNodeTree

from ..pyIndigo.Param import * 


# Implementation of custom nodes from Python

class IndigoShaderTree(ShaderNodeTree):
    bl_idname = "IndigoShaderTree"
    bl_label = "Indigo Shader Tree"
    bl_icon = "NODETREE"
    COMPAT_ENGINES = {'INDIGO'}

# Mix-in class for all custom nodes in this tree type.
# Defines a poll function to enable instantiation.
class IndigoShaderNode:
    def _create_common_inputs(self):
        self.inputs.new('NodeSocketShader', "Emission")
        self.inputs.new('NodeSocketShader', "Bump")
        self.inputs.new('NodeSocketShader', "Displacement")

    def _convert_common_inputs(self, indigo_material):
        inp = self.inputs['Bump']
        if len(inp.links) > 0:
            node = inp.links[0].from_node

            if node.type == 'TEX_IMAGE':
                if node.image:
                    indigo_material.bump = WavelengthIndependentParam.Texture(bpy.path.abspath(node.image.filepath), 2.2, 0, 1.0, 0)
            elif hasattr(node, 'indigo_type') and node.indigo_type == 'INDIGO_TEXTURE':
                node = inp.links[0].from_node
                indigo_material.bump = WavelengthIndependentParam.Texture(node._texture_path(), node.gamma, node.a, node.b, node.c)

        inp = self.inputs['Displacement']
        if len(inp.links) > 0:
            node = inp.links[0].from_node

            if node.type == 'TEX_IMAGE':
                if node.image:
                    indigo_material.displacement = WavelengthIndependentParam.Texture(bpy.path.abspath(node.image.filepath), 2.2, 0, 1.0, 0)
            elif hasattr(node, 'indigo_type') and node.indigo_type == 'INDIGO_TEXTURE':
                indigo_material.displacement = WavelengthIndependentParam.Texture(node._texture_path(), node.gamma, node.a, node.b, node.c)

        inp = self.inputs['Emission']
        if len(inp.links) > 0:
            node = inp.links[0].from_node
            if hasattr(node, 'indigo_type') and node.indigo_type == 'INDIGO_EMISSION':

                print ("FOUND EMISSION")

                emission, base_emission = node.convert()

                if emission:
                    print("SETTING EMISSION")
                    indigo_material.emission = emission
                if base_emission:
                    indigo_material.base_emission = base_emission
                else:
                    indigo_material.base_emission = WavelengthDependentParam.Uniform(1.0)

        '''
        if len(inp.links) < 1:
            indigo_material.bump = WavelengthIndependentParam.Uniform(inp.default_value)
        elif node.type == 'TEX_IMAGE':
            if node.image:
                indigo_material.bump = WavelengthIndependentParam.Texture(bpy.path.abspath(node.image.filepath), 2.2, 0, 1.0, 0)
        elif hasattr(node, 'indigo_type') and node.indigo_type == 'INDIGO_TEXTURE':
                indigo_material.bump = WavelengthIndependentParam.Texture(bpy.path.abspath(node.filepath), node.gamma, node.a, node.b, node.c)
        '''


    indigo_type = "INDIGO_BASE_NODE"

    @classmethod
    def poll(cls, ntree):
        return (ntree.bl_idname == 'ShaderNodeTree' and
        ntree.shader_type == 'OBJECT')

