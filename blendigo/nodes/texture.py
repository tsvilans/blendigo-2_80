import bpy
from .base import IndigoShaderNode

class IndigoTextureNode(bpy.types.Node, IndigoShaderNode):
    # === Basics ===
    # Description string
    '''A custom node'''
    # Optional identifier string. If not explicitly defined, the python class name is used.
    bl_idname = 'IndigoTextureNode'
    bl_label = 'Indigo Texture'
    bl_icon = 'SOUND'

    filepath: bpy.props.StringProperty()
    gamma: bpy.props.FloatProperty(default=2.2)
    a: bpy.props.FloatProperty(default=0.0)
    b: bpy.props.FloatProperty(default=1.0)
    c: bpy.props.FloatProperty(default=0.0)

    indigo_type = 'INDIGO_TEXTURE'

    def init(self, context):
        self.inputs.new('NodeSocketColor', "Image")

        self.outputs.new('NodeSocketShader', "Texture")


    def _texture_path(self):
        inp = self.inputs['Image']

        if len(inp.links) < 1:
            return ""
        elif inp.links[0].from_node.type == 'TEX_IMAGE':
            tex = inp.links[0].from_node
            if tex.image:
                self.filepath = bpy.path.abspath(tex.image.filepath)             

        return self.filepath


    def copy(self, node):
        print("Copying from node ", node)

    def free(self):
        print("Removing node ", self, ", Goodbye!")

    def draw_buttons(self, context, layout):
        layout.prop(self, "gamma")
        layout.prop(self, "a")
        layout.prop(self, "b")
        layout.prop(self, "c")

    def draw_buttons_ext(self, context, layout):
        pass

    def draw_label(self):
        return "Indigo Texture"