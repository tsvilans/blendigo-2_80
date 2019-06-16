import bpy

from bpy.props import StringProperty, BoolProperty, FloatProperty, CollectionProperty, EnumProperty, IntProperty

class IndigoEmissionScaleProperties(bpy.types.PropertyGroup):

    enabled: BoolProperty(
        name="Enabled",
        description="Use emission scaling.",
        default=False,
        )

    value: FloatProperty(
        name="Value",
        description="Value of emission in specified units.",
        default=60,
        )

    units: EnumProperty(
        name="Units",
        description="Units for emission scale.",
        items={
        ('luminous_flux', 'lm', 'Luminous flux'),
        ('luminous_intensity', 'cd', 'Luminous intensity (lm/sr)'),
        ('luminance', 'nits', 'Luminance (lm/sr/m/m)'),
        ('luminous_emittance', 'lux', 'Luminous emittance (lm/m/m)')},
        default='luminous_flux')


class IndigoObjectProperties(bpy.types.PropertyGroup):
    emission_scale: bpy.props.PointerProperty(type=IndigoEmissionScaleProperties)


    bidirectional: BoolProperty(
        name="Bidirectional",
        description="Use Bidirectional Path Tracing (Bidir).",
        default=True,
        )