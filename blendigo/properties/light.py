import bpy

from bpy.props import StringProperty, BoolProperty, FloatProperty, CollectionProperty, EnumProperty, IntProperty


class IndigoLightSunProperties(bpy.types.PropertyGroup):

    turbidity: FloatProperty(
        name="Turbidity",
        description="Turbidity",
        min=1.0,
        max=10.0,
        default=2.0,
        )

    model: EnumProperty(
        items = [
                ('original', 'Original', 'Use original model'),
                ('extra_atmospheric', 'Extra-Atmospheric', 'Use extra-atmospheric ("space") model'),
                ('captured-simulation', 'Captured simulation', 'Use realistic data')
            ],
        name="SunSky Model",
        description="SunSky Model",
        default="captured-simulation",
        )

    use_layers: BoolProperty(
        name="Use light layers",
        description="Place sun and sky on separate light layers",
        default=False,
        )

class IndigoLightHemiProperties(bpy.types.PropertyGroup):
    type: EnumProperty(
        items=[
                ('background', 'Background colour', 'A non-directional, uniform background colour'),
                ('env_map', 'HDRI environment map', 'Use image based lighting')
            ],
        name="Background type",
        description="Background type",
        default="background",
        )

    env_map_path: StringProperty(
        name="Env Map",
        description="Image to use as environment map",
        )

    env_map_type: EnumProperty(
        items=[
                ('spherical', 'Spherical', 'spherical'),
                ('spherical_environment', 'Spherical Environment', 'spherical_environment')
            ],
        name="Env map type",
        description="The type of the environment map",
        default="spherical",  
        )

    env_map_gain_value: FloatProperty(
        name="Gain",
        description="Gain value to apply to environment",
        min=0.0,
        max=10.0,
        default=1.0,
        )

    env_map_gain_exp: FloatProperty(
        name="*10^",
        description="Gain exponent to apply to environment",
        min=-30.0,
        max=30,
        default=7.0,
        )
