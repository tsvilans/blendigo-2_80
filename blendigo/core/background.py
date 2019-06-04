from mathutils import Vector
from blendigo.pyIndigo import Background

def export_background(depsgraph):

    flag = False

    for obj in depsgraph.objects:
        if obj.type == 'LIGHT':
            if obj.data.type == 'SUN':
                indigo_sun = obj.data.indigo_light_sun
                direction = obj.matrix_world.to_quaternion() @ Vector((0.0, 0.0, 1.0))
                indigo_background = Background.MakeSunSky(direction, indigo_sun.model)
                return indigo_background

    if not flag:
        for obj in depsgraph.objects:
            if obj.type == 'LIGHT':
                if obj.data.type == 'HEMI':
                    if obj.data.indigo_lamp_hemi.type == 'env_map':
                        indigo_hemi = obj.data.indigo_light_hemi

                        gain = indigo_hemi.env_map_gain_val * (10 ** indigo_hemi.env_map_gain_exp)
                        indigo_background = Background.MakeEnvMap(bpy.path.abspath(indigo_hemi.env_map_path), gain, obj.matrix_world.to_3x3().inverted())
                        return indigo_background
    if not flag:
        print("No background found.")

    return None
