from mathutils import Vector
from blendigo.pyIndigo import Camera


def export_camera(blender_camera):

    up = blender_camera.matrix_world.to_quaternion() @ Vector((0.0, 1.0, 0.0))
    fwd = blender_camera.matrix_world.to_quaternion() @ Vector((0.0, 0.0, -1.0))
    pos = blender_camera.matrix_world.to_translation()

    indigo_camera = Camera()
    indigo_camera.position = pos        
    indigo_camera.forwards = fwd
    indigo_camera.up = up
    indigo_camera.sensor_width = blender_camera.data.sensor_width * 0.001
    indigo_camera.exposure_duration = 1/blender_camera.data.indigo_camera.exposure
    indigo_camera.lens_sensor_dist = blender_camera.data.lens * 0.001
    indigo_camera.aperature = blender_camera.data.indigo_camera.fstop

    shift_x = blender_camera.data.shift_x * blender_camera.data.sensor_width * 0.001
    shift_y = blender_camera.data.shift_y * blender_camera.data.sensor_width * 0.001

    #print("Shift x: %f   y: %f" % (shift_x, shift_y))
    indigo_camera.shift_x = shift_x
    indigo_camera.shift_y = shift_y

    indigo_camera.vignetting = blender_camera.data.indigo_camera.vignetting
    indigo_camera.autofocus = blender_camera.data.indigo_camera.autofocus

    return indigo_camera