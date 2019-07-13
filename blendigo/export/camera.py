import bpy
from mathutils import Vector
from blendigo.pyIndigo import Camera

def aspect_ratio():
    return bpy.context.scene.render.resolution_x / bpy.context.scene.render.resolution_y

def lens_sensor_dist(sensor_width, FOV):
    import math
    
    aspect = aspect_ratio()
    #print("aspect is {}".format(aspect))
    
    film = 0.001 * sensor_width
    
    if aspect < 1.0:
        FOV = FOV*aspect
    
    lsd = film/( 2.0*math.tan( FOV/2.0 ))
    #print('Lens Sensor Distance: %f'%lsd)
    return lsd

def aperture_radius(context, p):
    ar = lens_sensor_dist / (2.0*f_stop)
    return ar

def export_preview_camera():
    indigo_camera = Camera()
    indigo_camera.position = (0,-1, 0)
    indigo_camera.forwards = (0, 1, 0)
    indigo_camera.up = (0, 0, 1)
    indigo_camera.sensor_width = 0.035
    indigo_camera.exposure_duration = 1/30
    indigo_camera.focus_distance = 1.0
    lsd = lens_sensor_dist(0.035, 0.57)
    indigo_camera.lens_sensor_dist = lsd
    indigo_camera.set_aperature(11, lsd)
    indigo_camera.autofocus = True
    indigo_camera.vignetting = False

    return indigo_camera


def export_camera(blender_camera):

    up = blender_camera.matrix_world.to_quaternion() @ Vector((0.0, 1.0, 0.0))
    fwd = blender_camera.matrix_world.to_quaternion() @ Vector((0.0, 0.0, -1.0))
    pos = blender_camera.matrix_world.to_translation()

    indigo_camera = Camera()
    indigo_camera.position = pos        
    indigo_camera.forwards = fwd
    indigo_camera.up = up
    indigo_camera.sensor_width = 0.001 * blender_camera.data.sensor_width
    indigo_camera.exposure_duration = 1/blender_camera.data.indigo_camera.exposure

    indigo_camera.focus_distance = blender_camera.data.indigo_camera.focus_distance

    lsd = lens_sensor_dist(blender_camera.data.sensor_width, blender_camera.data.angle)
    #print ("lens sensor distance is {}".format(lsd))
    #print ("fstop is {}".format(blender_camera.data.indigo_camera.fstop))

    indigo_camera.lens_sensor_dist = lsd
    indigo_camera.set_aperature(blender_camera.data.indigo_camera.fstop, lsd)

    shift_x = blender_camera.data.shift_x * blender_camera.data.sensor_width * 0.001
    shift_y = blender_camera.data.shift_y * blender_camera.data.sensor_width * 0.001

    #print("Shift x: %f   y: %f" % (shift_x, shift_y))
    indigo_camera.shift_x = shift_x
    indigo_camera.shift_y = shift_y

    indigo_camera.vignetting = blender_camera.data.indigo_camera.vignetting
    indigo_camera.autofocus = blender_camera.data.indigo_camera.autofocus

    return indigo_camera