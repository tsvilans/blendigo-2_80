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

    def _process_input(self, input_id, param_type, default, optional=True):
        if input_id not in self.inputs.keys():
            return None

        inp = self.inputs[input_id]

        if len(inp.links) > 0:
            node = inp.links[0].from_node
            if node.type == 'TEX_IMAGE':
                if node.image:
                    return param_type.Texture(bpy.path.abspath(node.image.filepath), 1.0, 0, 1.0, 0)
            elif hasattr(node, 'indigo_type') and node.indigo_type == 'INDIGO_TEXTURE':
                return param_type.Texture(node._texture_path(), node.gamma, node.a, node.b, node.c)
            elif hasattr(node, 'indigo_type') and node.indigo_type == 'INDIGO_PARAM':
                node = inp.links[0].from_node
                return node.convert()

        if optional:
            #print("returning none for {}".format(input_id))
            return None

        if hasattr(inp, "default_value"):

            col = inp.default_value

            if inp.type == 'RGBA':
                return param_type.RGB(col[0], col[1], col[2], 1.0)
            #elif inp.type == 'VALUE':
            #print("returning {} with value {}".format(input_id, col))
            return param_type.Uniform(col)
        return default

    def _get_submaterial(self, input_id, name, exporter):
        if input_id not in self.inputs.keys():
            return None

        inp = self.inputs[input_id]

        if len(inp.links) > 0:
            node = inp.links[0].from_node
            if hasattr(node, 'indigo_type') and node.indigo_type in ['INDIGO_DIFFUSE', 'INDIGO_PHONG']: # Improve this
                indigo_material = node.convert(name, exporter)
                return indigo_material
        return None


    def _create_common_inputs(self):
        self.inputs.new('NodeSocketShader', "Emission")
        self.inputs.new('NodeSocketShader', "Bump")
        self.inputs.new('NodeSocketShader', "Normal")
        self.inputs.new('NodeSocketShader', "Displacement")

    def _convert_common_inputs(self, indigo_material, name, exporter):

        bump = self._process_input('Bump', WavelengthIndependentParam, WavelengthIndependentParam.Uniform(0.0))
        if bump:
            indigo_material.bump = bump

        normal_map = self._process_input('Normal', WavelengthDependentParam, WavelengthDependentParam.Uniform(0.0))
        if bump:
            indigo_material.normal_map = normal_map

        displacement = self._process_input('Displacement', WavelengthIndependentParam, WavelengthIndependentParam.Uniform(0.0))
        if displacement:
            indigo_material.displacement = displacement

        inp = self.inputs['Emission']
        if len(inp.links) > 0:
            node = inp.links[0].from_node
            if hasattr(node, 'indigo_type') and node.indigo_type == 'INDIGO_EMISSION':

                emission, base_emission, emission_scale = node.convert()

                if emission:
                    indigo_material.emission = emission
                if base_emission:
                    indigo_material.base_emission = base_emission
                else:
                    indigo_material.base_emission = WavelengthDependentParam.Uniform(1.0)

                if emission_scale:
                    exporter.emission_scales[name] = emission_scale

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

