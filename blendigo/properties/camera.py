import bpy

from bpy.props import StringProperty, BoolProperty, FloatProperty, CollectionProperty, EnumProperty, IntProperty

class IndigoCameraProperties(bpy.types.PropertyGroup):
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

    autofocus: BoolProperty(
        name="Autofocus",
        description="Autofocus",
        default=True,
        )

    focus_distance: FloatProperty(
        name="Focus distance",
        description="Camera focus distance",
        default=1.0,
        min=0.0,
        )

    vignetting: BoolProperty(
        name="Vignetting",
        description="Vignetting",
        default=True,
        )

    autoexposure: BoolProperty(
        name="Auto Exposure",
        description="Auto Exposure",
        default=False,
        )


    ad: BoolProperty(
        name="Aperture Diffraction",
        description="Aperture Diffraction",
        default=False,
        )

    ad_post: BoolProperty(
        name="AD Post-Process",
        description="AD Post-Process",
        default=False,
        )

    iso: IntProperty(
        name="Film ISO",
        description="Film ISO",
        default=100,
        min=1,
        soft_min=25,
        max=10000,
        soft_max=10000,
        )

    exposure: FloatProperty(
        name="Exposure 1/",
        description="Exposure 1/",
        default=125,
        min=0.00001,
        soft_min=0.001,
        max=8000,
        soft_max=8000,
        #compute= lambda c, self: 1 / self.exposure,
        )

    fstop: FloatProperty(
        name="f/Stop",
        description="f/Stop",
        default = 8,
        min=1,
        soft_min=1,
        max=128,
        soft_max=128,
        )

    def aspect_ratio(context,p):
        return context.render.resolution_x / context.render.resolution_y

    def f_stop(context, p):
        return p.fstop

    def lens_sensor_dist(context,p):
        import math
        
        aspect = aspect_ratio(context,p)
        
        film = 0.001 * context.camera.data.sensor_width
        
        FOV = context.camera.data.angle
        if aspect < 1.0:
            FOV = FOV*aspect
        
        lsd = film/( 2.0*math.tan( FOV/2.0 ))
        #print('Lens Sensor Distance: %f'%lsd)
        return lsd

    def aperture_radius(context, p):
        ar = lens_sensor_dist(context, p) / (2.0*f_stop(context,p))
        #print('Aperture Radius: %f' % ar)
        return ar


properties = [

    {
        'type': 'enum',
        'attr': 'whitebalance',
        'name': 'White Balance',
        'description': 'White Balance Standard',
        'items': [
            ('E','E','E'),
            ('D50','D50','D50'),
            ('D55','D55','D55'),
            ('D65','D65','D65'),
            ('D75','D75','D75'),
            ('A','A','A'),
            ('B','B','B'),
            ('C','C','C'),
            ('9300','9300','9300'),
            ('F2','F2','F2'),
            ('F7','F7','F7'),
            ('F11','F11','F11'),
            ('Custom','Custom','Custom'),
        ],
    },
    {
        'type': 'float',
        'attr': 'whitebalanceX',
        'name': 'X',
        'description': 'Whitebalance X',
        #'slider': True,
        'precision': 5,
        'default': 0.33333,
        'min': 0.1,
        'soft_min': 0.1,
        'max': 0.5,
        'soft_max': 0.5,
    },
    {
        'type': 'float',
        'attr': 'whitebalanceY',
        'name': 'Y',
        'description': 'Whitebalance Y',
        #'slider': True,
        'precision': 5,
        'default': 0.33333,
        'min': 0.1,
        'soft_min': 0.1,
        'max': 0.5,
        'soft_max': 0.5,
    },
    {
        'type': 'bool',
        'attr': 'motionblur',
        'name': 'Camera MB',
        'description': 'Enable Camera Motion Blur',
        'default': False
    },
    {
        'type': 'enum',
        'attr': 'ad_type',
        'name': 'AD Type',
        'description': 'Aperture Diffraction Type',
        'items': [
            ('image', 'Image', 'image'),
            ('generated', 'Generated', 'generated'),
            ('circular', 'Circular', 'circular'),
        ],
    },
    {
        'type': 'int',
        'attr': 'ad_blades',
        'name': 'Blades',
        'description': 'Number of blades in the aperture',
        'default': 5,
        'min': 3,
        'soft_min': 3,
        'max': 20,
        'soft_max': 20,
    },
    {
        'type': 'float',
        'attr': 'ad_offset',
        'name': 'Offset',
        'description': 'Aperture blade offset',
        'default': 0.4,
        'min': 0,
        'soft_min': 0,
        'max': 0.5,
        'soft_max': 0.5,
    },
    {
        'type': 'int',
        'attr': 'ad_curvature',
        'name': 'Curvature',
        'description': 'Aperture blade curvature',
        'default': 3,
        'min': 0,
        'soft_min': 0,
        'max': 10,
        'soft_max': 10,
    },
    {
        'type': 'float',
        'attr': 'ad_angle',
        'name': 'Angle',
        'description': 'Aperture blade angle',
        'default': 0.2,
        'min': 0,
        'soft_min': 0,
        'max': 2,
        'soft_max': 2,
    },
    {
        'type': 'string',
        'attr': 'ad_image',
        'name': 'Image',
        'description': 'Image to use as the aperture opening. Must be power of two square, >= 512',
        'subtype': 'FILE_PATH',
    },
    {
        'type': 'string',
        'attr': 'ad_obstacle',
        'name': 'Obstacle Map',
        'description': 'Image to use as the aperture obstacle map. Must be power of two square, >= 512',
        'subtype': 'FILE_PATH',
    },
]