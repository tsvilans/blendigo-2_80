import bpy

from bpy.props import StringProperty, BoolProperty, FloatProperty, CollectionProperty, EnumProperty, IntProperty

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
                ('fast_box', 'Fast Box', 'Fast Box filter.'),
                ('radial', 'Radial', 'Radial filter.')
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