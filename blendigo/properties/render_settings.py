import bpy

from bpy.props import StringProperty, BoolProperty, FloatProperty, CollectionProperty, EnumProperty, IntProperty, PointerProperty

class IndigoRendererChannels(bpy.types.PropertyGroup):

    direct_lighting_channel: BoolProperty(
        name="Direct lighting channel",
        description="Direct lighting channel.",
        default=False,
        )

    position_channel: BoolProperty(
        name="Position channel",
        description="Position channel.",
        default=False,
        )

    depth_channel: BoolProperty(
        name="Depth channel",
        description="Depth channel.",
        default=False,
        )

    emission_lighting_channel: BoolProperty(
        name="Emission lighting channel",
        description="Emission lighting channel.",
        default=False,
        )

    indirect_lighting_channel: BoolProperty(
        name="Indirect lighting channel",
        description="Indirect lighting channel.",
        default=False,
        )

    material_id_channel: BoolProperty(
        name="Material id channel",
        description="Material id channel.",
        default=False,
        )

    normals_channel: BoolProperty(
        name="Normals channel",
        description="Normals channel.",
        default=False,
        )

    normals_pre_bump_channel: BoolProperty(
        name="Normals pre bump channel",
        description="Normals pre bump channel.",
        default=False,
        )

    object_id_channel: BoolProperty(
        name="Object id channel",
        description="Object id channel.",
        default=False,
        )

    refraction_lighting_channel: BoolProperty(
        name="Refraction lighting channel",
        description="Refraction lighting channel.",
        default=False,
        )

    sss_lighting_channel: BoolProperty(
        name="Sss lighting channel",
        description="Sss lighting channel.",
        default=False,
        )

    foreground_channel: BoolProperty(
        name="Foreground channel",
        description="Foreground channel.",
        default=False,
        )

    participating_media_lighting_channel: BoolProperty(
        name="Participating media lighting channel",
        description="Participating media lighting channel.",
        default=False,
        )

    specular_reflection_lighting_channel: BoolProperty(
        name="Specular reflection lighting channel",
        description="Specular reflection lighting channel.",
        default=False,
        )

    transmission_lighting_channel: BoolProperty(
        name="Transmission lighting channel",
        description="Transmission lighting channel.",
        default=False,
        )

    '''
    def draw(self, context):
        layout = self.layout
        col = layout.column()
        col.prop(self, 'direct_lighting_channel')
        col.prop(self, 'position_channel')
        col.prop(self, 'depth_channel')
        col.prop(self, 'emission_lighting_channel')
        col.prop(self, 'indirect_lighting_channel')
        col.prop(self, 'material_id_channel')
        col.prop(self, 'normals_channel')
        col.prop(self, 'normals_pre_bump_channel')
        col.prop(self, 'object_id_channel')
        col.prop(self, 'refraction_lighting_channel')
        col.prop(self, 'sss_lighting_channel')
        col.prop(self, 'foreground_channel')
        col.prop(self, 'participating_media_lighting_channel')
        col.prop(self, 'specular_reflection_lighting_channel')
        col.prop(self, 'transmission_lighting_channel')
    '''


class IndigoRendererProperties(bpy.types.PropertyGroup):
    metropolis: BoolProperty(
        name="Metropolis",
        description="Use Metropolis Light Transport (MLT).",
        default=True,
        )

    bidirectional: BoolProperty(
        name="Bidirectional",
        description="Use Bidirectional Path Tracing (Bidir).",
        default=True,
        )

    haltspp: IntProperty(
        name="Halt SPP",
        description="Halt samples per pixel.",
        default=-1,
        )

    halttime: IntProperty(
        name="Halt Time",
        description="Halt time in seconds.",
        default=-1,
        )

    supersampling: IntProperty(
        name="Supersampling",
        description="Supersampling factor",
        default=2,
        min=1,
        max=10,
        )    

    foreground_alpha: BoolProperty(
        name="Foreground Alpha",
        description="Use foreground alpha.",
        default=False,
        )


    motionblur: BoolProperty(
        name="Motionblur",
        description="Use motioblur.",
        default=False,
        )    

    write_to_xml: BoolProperty(
        name="Write .IGS",
        description="Write to Indigo Scene file.",
        default=False,
        )

    external: BoolProperty(
        name="Standalone",
        description="Launch Indigo externally.",
        default=False,
        )

    buffer_multiplier: FloatProperty(
        name="Buffer mult.",
        description="Amount to augment exposure by to get max pixel values greater than 1.0 (hack).",
        default=10.0,
        min=1.0,
        max=1000.0,
        )

    splat_filter: EnumProperty(
        items = [
                ('box', 'Box', 'Box filter.'),
                ('fastbox', 'Fast Box', 'Fast Box filter.'),
                ('radial', 'Radial', 'Radial filter.'),
                ('mn_cubic', 'Cubic', 'Cubic filter.')
            ],
        name="Splat filter",
        description="Splat filter",
        default="radial",
        )

    downsize_filter: EnumProperty(
        items = [
                ('gaussian', 'Gaussian', 'Gaussian filter.'),
                ('cubic', 'Cubic', 'Cubic filter.'),
                ('sharp', 'Sharp', 'Sharp filter.')
            ],
        name="Downsize filter",
        description="Downsize filter",
        default="sharp",
        )  

    clamp_contributions: BoolProperty(
        name="Clamp contributions",
        description="Launch Indigo externally.",
        default=False,
        )

    max_contributions: FloatProperty(
        name="Max. contributions",
        description="Maximum contribution",
        default=100.0,
        min=1.0,
        )

    aovs: PointerProperty(type=IndigoRendererChannels)

 