import bpy
from bpy.types import NodeTree, Node, NodeSocket, ShaderNodeTree

from .base import IndigoShaderNode, IndigoShaderTree

from .diffuse import IndigoDiffuseShaderNode
from .phong import IndigoPhongShaderNode
from .double_sided_thin import IndigoDoubleSidedThinShaderNode
from .specular import IndigoSpecularShaderNode
from .texture import IndigoTextureNode
from .emission import IndigoEmissionShaderNode#, IndigoEmissionScaleProperties
from .exit_portal import IndigoExitPortalShaderNode
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
    IndigoNodeCategory("INDIGO_SHADERS", "Indigo Shaders", items=[
        # our basic node
        NodeItem("IndigoDiffuseShaderNode"),
        NodeItem("IndigoPhongShaderNode"),
        NodeItem("IndigoSpecularShaderNode"),
        NodeItem("IndigoDoubleSidedThinShaderNode"),
        NodeItem("IndigoTextureNode"),
        NodeItem("IndigoEmissionShaderNode"),
        NodeItem("IndigoExitPortalShaderNode"),
        ]),

    IndigoNodeCategory("INDIGO_PARAMS", "Indigo Params", items=[
        # our basic node
        NodeItem("IndigoParamRGBShaderNode"),
        NodeItem("IndigoParamUniformShaderNode"),
        NodeItem("IndigoParamBlackbodyShaderNode"),
        ]),    
    ]
