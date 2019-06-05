import bpy
from bpy.types import NodeTree, Node, NodeSocket, ShaderNodeTree

from .base import IndigoShaderNode, IndigoShaderTree

from .diffuse import IndigoDiffuseShaderNode
from .phong import IndigoPhongShaderNode
from .specular import IndigoSpecularShaderNode
from .texture import IndigoTextureNode
from .emission import IndigoEmissionShaderNode
from .param_rgb import IndigoParamRGBShaderNode
from .param_uniform import IndigoParamUniformShaderNode
from .param_blackbody import IndigoParamBlackbodyShaderNode
#from .blend import IndigoBlendNode

import nodeitems_utils
from nodeitems_utils import NodeCategory, NodeItem

class IndigoNodeCategory(NodeCategory):
    @classmethod
    def poll(cls, context):
        return context.space_data.tree_type == 'ShaderNodeTree'
        #return context.space_data.tree_type == 'IndigoShaderTree'

# all categories in a list
node_categories = [
    # identifier, label, items list
    IndigoNodeCategory("INDIGONODES", "Indigo Renderer", items=[
        # our basic node
        NodeItem("IndigoDiffuseShaderNode"),
        NodeItem("IndigoPhongShaderNode"),
        NodeItem("IndigoSpecularShaderNode"),
        NodeItem("IndigoTextureNode"),
        NodeItem("IndigoEmissionShaderNode"),
        NodeItem("IndigoParamRGBShaderNode"),
        NodeItem("IndigoParamUniformShaderNode"),
        NodeItem("IndigoParamBlackbodyShaderNode"),
        ]),
    ]
