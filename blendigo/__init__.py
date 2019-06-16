import bpy



bl_info = {
    "name": "Blendigo 2.80",
    "author": "Tom Svilans",
    "version": (0,1,0,0),
    "blender": (2, 80, 0),
    "category": "Render",
    "location": "Render > Engine > Indigo Renderer",
    "warning": '', 
    "wiki_url": '',
    "tracker_url": '',
    "description": "This uses a Python wrapper for the Indigo API to have Indigo functionality within Blender." #edit
}

import nodeitems_utils
from nodeitems_utils import NodeCategory, NodeItem
from .nodes import *
#from .nodes import IndigoPhongShaderNode, IndigoDiffuseShaderNode, IndigoSpecularShaderNode, IndigoShaderTree, IndigoTextureNode, IndigoEmissionShaderNode, IndigoEmissionScaleProperties
#from .nodes import IndigoParamRGBShaderNode, IndigoParamUniformShaderNode, IndigoParamBlackbodyShaderNode, IndigoTextureNode
#from .nodes import IndigoNodeCategory, node_categories

from .core import IndigoRenderEngine

from .properties.render_settings import IndigoRendererProperties
from .properties.camera import IndigoCameraProperties
from .properties.light import IndigoLightSunProperties, IndigoLightHemiProperties
from .properties.material import IndigoMaterialProperties, IndigoTextureProperties

from .ui.camera import INDIGO_PT_camera
from .ui.render_settings import INDIGO_PT_render_settings
from .ui.light import INDIGO_PT_lights, INDIGO_PT_light_sun, INDIGO_PT_light_hemi


classes = [
    IndigoRenderEngine, 
    IndigoRendererProperties,
    IndigoCameraProperties,

    IndigoMaterialProperties, 
    IndigoTextureProperties,
    #IndigoEmissionScaleProperties,

    IndigoPhongShaderNode, 
    IndigoDiffuseShaderNode,
    IndigoDoubleSidedThinShaderNode,
    IndigoSpecularShaderNode,
    IndigoEmissionShaderNode,
    IndigoParamRGBShaderNode, 
    IndigoParamUniformShaderNode, 
    IndigoParamBlackbodyShaderNode, 
    IndigoTextureNode,
    IndigoShaderTree,

    IndigoLightSunProperties,
    IndigoLightHemiProperties,


    INDIGO_PT_camera,
    INDIGO_PT_render_settings,
    INDIGO_PT_lights, 
    INDIGO_PT_light_sun, 
    INDIGO_PT_light_hemi,


    #IndigoNodeCategory,
]

import bl_ui
'''
ui_elements = [
    bl_ui.properties_data_armature.DATA_PT_custom_props_arm,
    bl_ui.properties_data_bone.BONE_PT_custom_props,
    bl_ui.properties_data_camera.CAMERA_PT_presets,
    bl_ui.properties_data_camera.DATA_PT_camera,
    bl_ui.properties_data_camera.DATA_PT_camera_background_image,
    bl_ui.properties_data_camera.DATA_PT_camera_display,
    bl_ui.properties_data_camera.DATA_PT_camera_display_composition_guides,
    bl_ui.properties_data_camera.DATA_PT_camera_display_passepartout,
    bl_ui.properties_data_camera.DATA_PT_camera_safe_areas,
    bl_ui.properties_data_camera.DATA_PT_camera_safe_areas_center_cut,
    bl_ui.properties_data_camera.DATA_PT_camera_stereoscopy,
    bl_ui.properties_data_camera.DATA_PT_context_camera,
    bl_ui.properties_data_camera.DATA_PT_custom_props_camera,
    bl_ui.properties_data_camera.DATA_PT_lens,
    bl_ui.properties_data_camera.SAFE_AREAS_PT_presets,
    bl_ui.properties_data_curve.DATA_PT_curve_texture_space,
    bl_ui.properties_data_curve.DATA_PT_custom_props_curve,
    bl_ui.properties_data_lattice.DATA_PT_custom_props_lattice,
    bl_ui.properties_data_light.DATA_PT_context_light,
    bl_ui.properties_data_light.DATA_PT_custom_props_light,
    bl_ui.properties_data_lightprobe.DATA_PT_context_lightprobe,
    bl_ui.properties_data_lightprobe.DATA_PT_lightprobe,
    bl_ui.properties_data_lightprobe.DATA_PT_lightprobe_display,
    bl_ui.properties_data_lightprobe.DATA_PT_lightprobe_parallax,
    bl_ui.properties_data_lightprobe.DATA_PT_lightprobe_visibility,
    bl_ui.properties_data_mesh.DATA_PT_context_mesh,
    bl_ui.properties_data_mesh.DATA_PT_custom_props_mesh,
    bl_ui.properties_data_mesh.DATA_PT_customdata,
    bl_ui.properties_data_mesh.DATA_PT_face_maps,
    bl_ui.properties_data_mesh.DATA_PT_normals,
    bl_ui.properties_data_mesh.DATA_PT_normals_auto_smooth,
    bl_ui.properties_data_mesh.DATA_PT_shape_keys,
    bl_ui.properties_data_mesh.DATA_PT_texture_space,
    bl_ui.properties_data_mesh.DATA_PT_uv_texture,
    bl_ui.properties_data_mesh.DATA_PT_vertex_colors,
    bl_ui.properties_data_mesh.DATA_PT_vertex_groups,
    bl_ui.properties_data_metaball.DATA_PT_custom_props_metaball,
    bl_ui.properties_data_metaball.DATA_PT_mball_texture_space,
    bl_ui.properties_data_speaker.DATA_PT_cone,
    bl_ui.properties_data_speaker.DATA_PT_context_speaker,
    bl_ui.properties_data_speaker.DATA_PT_custom_props_speaker,
    bl_ui.properties_data_speaker.DATA_PT_distance,
    bl_ui.properties_data_speaker.DATA_PT_speaker,
    #bl_ui.properties_freestyle.MATERIAL_PT_freestyle_line,
    #bl_ui.properties_freestyle.RENDER_PT_freestyle,
    #bl_ui.properties_freestyle.VIEWLAYER_PT_freestyle,
    #bl_ui.properties_freestyle.VIEWLAYER_PT_freestyle_lineset,
    #bl_ui.properties_freestyle.VIEWLAYER_PT_freestyle_linestyle,
    bl_ui.properties_object.OBJECT_PT_custom_props,
    bl_ui.properties_output.RENDER_PT_dimensions,
    bl_ui.properties_output.RENDER_PT_encoding,
    bl_ui.properties_output.RENDER_PT_encoding_audio,
    bl_ui.properties_output.RENDER_PT_encoding_video,
    bl_ui.properties_output.RENDER_PT_frame_remapping,
    bl_ui.properties_output.RENDER_PT_output,
    bl_ui.properties_output.RENDER_PT_output_views,
    bl_ui.properties_output.RENDER_PT_stamp,
    bl_ui.properties_output.RENDER_PT_stamp_burn,
    bl_ui.properties_output.RENDER_PT_stamp_note,
    bl_ui.properties_output.RENDER_PT_stereoscopy,
    bl_ui.properties_particle.PARTICLE_PT_boidbrain,
    bl_ui.properties_particle.PARTICLE_PT_cache,
    bl_ui.properties_particle.PARTICLE_PT_children,
    bl_ui.properties_particle.PARTICLE_PT_children_clumping,
    bl_ui.properties_particle.PARTICLE_PT_children_clumping_noise,
    bl_ui.properties_particle.PARTICLE_PT_children_kink,
    bl_ui.properties_particle.PARTICLE_PT_children_parting,
    bl_ui.properties_particle.PARTICLE_PT_children_roughness,
    bl_ui.properties_particle.PARTICLE_PT_context_particles,
    bl_ui.properties_particle.PARTICLE_PT_custom_props,
    bl_ui.properties_particle.PARTICLE_PT_draw,
    bl_ui.properties_particle.PARTICLE_PT_emission,
    bl_ui.properties_particle.PARTICLE_PT_emission_source,
    bl_ui.properties_particle.PARTICLE_PT_field_weights,
    bl_ui.properties_particle.PARTICLE_PT_force_fields,
    bl_ui.properties_particle.PARTICLE_PT_force_fields_type1,
    bl_ui.properties_particle.PARTICLE_PT_force_fields_type1_falloff,
    bl_ui.properties_particle.PARTICLE_PT_force_fields_type2,
    bl_ui.properties_particle.PARTICLE_PT_force_fields_type2_falloff,
    bl_ui.properties_particle.PARTICLE_PT_hair_dynamics,
    bl_ui.properties_particle.PARTICLE_PT_hair_dynamics_presets,
    bl_ui.properties_particle.PARTICLE_PT_hair_dynamics_structure,
    bl_ui.properties_particle.PARTICLE_PT_hair_dynamics_volume,
    bl_ui.properties_particle.PARTICLE_PT_hair_shape,
    bl_ui.properties_particle.PARTICLE_PT_physics,
    bl_ui.properties_particle.PARTICLE_PT_physics_boids_battle,
    bl_ui.properties_particle.PARTICLE_PT_physics_boids_misc,
    bl_ui.properties_particle.PARTICLE_PT_physics_boids_movement,
    bl_ui.properties_particle.PARTICLE_PT_physics_deflection,
    bl_ui.properties_particle.PARTICLE_PT_physics_fluid_advanced,
    bl_ui.properties_particle.PARTICLE_PT_physics_fluid_interaction,
    bl_ui.properties_particle.PARTICLE_PT_physics_fluid_springs,
    bl_ui.properties_particle.PARTICLE_PT_physics_fluid_springs_advanced,
    bl_ui.properties_particle.PARTICLE_PT_physics_fluid_springs_viscoelastic,
    bl_ui.properties_particle.PARTICLE_PT_physics_forces,
    bl_ui.properties_particle.PARTICLE_PT_physics_integration,
    bl_ui.properties_particle.PARTICLE_PT_physics_relations,
    bl_ui.properties_particle.PARTICLE_PT_render,
    bl_ui.properties_particle.PARTICLE_PT_render_collection,
    bl_ui.properties_particle.PARTICLE_PT_render_collection_use_count,
    bl_ui.properties_particle.PARTICLE_PT_render_extra,
    #bl_ui.properties_particle.PARTICLE_PT_render_line,
    bl_ui.properties_particle.PARTICLE_PT_render_object,
    bl_ui.properties_particle.PARTICLE_PT_render_path,
    bl_ui.properties_particle.PARTICLE_PT_render_path_timing,
    bl_ui.properties_particle.PARTICLE_PT_render_trails,
    bl_ui.properties_particle.PARTICLE_PT_rotation,
    bl_ui.properties_particle.PARTICLE_PT_rotation_angular_velocity,
    bl_ui.properties_particle.PARTICLE_PT_textures,
    bl_ui.properties_particle.PARTICLE_PT_velocity,
    bl_ui.properties_particle.PARTICLE_PT_vertexgroups,
    bl_ui.properties_physics_cloth.PHYSICS_PT_cloth,
    bl_ui.properties_physics_cloth.PHYSICS_PT_cloth_cache,
    bl_ui.properties_physics_cloth.PHYSICS_PT_cloth_collision,
    bl_ui.properties_physics_cloth.PHYSICS_PT_cloth_damping,
    bl_ui.properties_physics_cloth.PHYSICS_PT_cloth_field_weights,
    bl_ui.properties_physics_cloth.PHYSICS_PT_cloth_object_collision,
    bl_ui.properties_physics_cloth.PHYSICS_PT_cloth_physical_properties,
    bl_ui.properties_physics_cloth.PHYSICS_PT_cloth_property_weights,
    bl_ui.properties_physics_cloth.PHYSICS_PT_cloth_self_collision,
    bl_ui.properties_physics_cloth.PHYSICS_PT_cloth_shape,
    bl_ui.properties_physics_cloth.PHYSICS_PT_cloth_stiffness,
    bl_ui.properties_physics_field.PHYSICS_PT_collision,
    bl_ui.properties_physics_field.PHYSICS_PT_collision_particle,
    bl_ui.properties_physics_field.PHYSICS_PT_collision_softbody,
    bl_ui.properties_physics_field.PHYSICS_PT_field,
    bl_ui.properties_physics_field.PHYSICS_PT_field_falloff,
    bl_ui.properties_physics_field.PHYSICS_PT_field_falloff_angular,
    bl_ui.properties_physics_field.PHYSICS_PT_field_falloff_radial,
    bl_ui.properties_physics_field.PHYSICS_PT_field_settings,
    bl_ui.properties_physics_field.PHYSICS_PT_field_settings_kink,
    bl_ui.properties_physics_field.PHYSICS_PT_field_settings_texture_select,
    bl_ui.properties_physics_fluid.PHYSICS_PT_domain_bake,
    bl_ui.properties_physics_fluid.PHYSICS_PT_domain_boundary,
    bl_ui.properties_physics_fluid.PHYSICS_PT_domain_gravity,
    bl_ui.properties_physics_fluid.PHYSICS_PT_domain_particles,
    bl_ui.properties_physics_fluid.PHYSICS_PT_domain_viscosity,
    bl_ui.properties_physics_fluid.PHYSICS_PT_fluid,
    bl_ui.properties_physics_fluid.PHYSICS_PT_fluid_flow,
    bl_ui.properties_physics_fluid.PHYSICS_PT_fluid_particle_cache,
    bl_ui.properties_physics_fluid.PHYSICS_PT_fluid_settings,
    bl_ui.properties_physics_rigidbody.PHYSICS_PT_rigid_body,
    bl_ui.properties_physics_rigidbody.PHYSICS_PT_rigid_body_collisions,
    bl_ui.properties_physics_rigidbody.PHYSICS_PT_rigid_body_collisions_collections,
    bl_ui.properties_physics_rigidbody.PHYSICS_PT_rigid_body_collisions_sensitivity,
    bl_ui.properties_physics_rigidbody.PHYSICS_PT_rigid_body_collisions_surface,
    bl_ui.properties_physics_rigidbody.PHYSICS_PT_rigid_body_dynamics,
    bl_ui.properties_physics_rigidbody.PHYSICS_PT_rigid_body_dynamics_deactivation,
    bl_ui.properties_physics_rigidbody.PHYSICS_PT_rigid_body_settings,
    bl_ui.properties_physics_rigidbody_constraint.PHYSICS_PT_rigid_body_constraint,
    bl_ui.properties_physics_rigidbody_constraint.PHYSICS_PT_rigid_body_constraint_limits,
    bl_ui.properties_physics_rigidbody_constraint.PHYSICS_PT_rigid_body_constraint_limits_angular,
    bl_ui.properties_physics_rigidbody_constraint.PHYSICS_PT_rigid_body_constraint_limits_linear,
    bl_ui.properties_physics_rigidbody_constraint.PHYSICS_PT_rigid_body_constraint_motor,
    bl_ui.properties_physics_rigidbody_constraint.PHYSICS_PT_rigid_body_constraint_motor_angular,
    bl_ui.properties_physics_rigidbody_constraint.PHYSICS_PT_rigid_body_constraint_motor_linear,
    bl_ui.properties_physics_rigidbody_constraint.PHYSICS_PT_rigid_body_constraint_objects,
    bl_ui.properties_physics_rigidbody_constraint.PHYSICS_PT_rigid_body_constraint_override_iterations,
    bl_ui.properties_physics_rigidbody_constraint.PHYSICS_PT_rigid_body_constraint_settings,
    bl_ui.properties_physics_rigidbody_constraint.PHYSICS_PT_rigid_body_constraint_springs,
    bl_ui.properties_physics_rigidbody_constraint.PHYSICS_PT_rigid_body_constraint_springs_angular,
    bl_ui.properties_physics_rigidbody_constraint.PHYSICS_PT_rigid_body_constraint_springs_linear,
    bl_ui.properties_physics_smoke.PHYSICS_PT_smoke,
    bl_ui.properties_physics_smoke.PHYSICS_PT_smoke_adaptive_domain,
    bl_ui.properties_physics_smoke.PHYSICS_PT_smoke_behavior,
    bl_ui.properties_physics_smoke.PHYSICS_PT_smoke_behavior_dissolve,
    bl_ui.properties_physics_smoke.PHYSICS_PT_smoke_cache,
    bl_ui.properties_physics_smoke.PHYSICS_PT_smoke_collections,
    bl_ui.properties_physics_smoke.PHYSICS_PT_smoke_field_weights,
    bl_ui.properties_physics_smoke.PHYSICS_PT_smoke_fire,
    bl_ui.properties_physics_smoke.PHYSICS_PT_smoke_flow_texture,
    bl_ui.properties_physics_smoke.PHYSICS_PT_smoke_highres,
    bl_ui.properties_physics_smoke.PHYSICS_PT_smoke_settings,
    bl_ui.properties_physics_smoke.PHYSICS_PT_smoke_settings_initial_velocity,
    bl_ui.properties_physics_smoke.PHYSICS_PT_smoke_settings_particle_size,
    bl_ui.properties_physics_softbody.PHYSICS_PT_softbody,
    bl_ui.properties_physics_softbody.PHYSICS_PT_softbody_cache,
    bl_ui.properties_physics_softbody.PHYSICS_PT_softbody_collision,
    bl_ui.properties_physics_softbody.PHYSICS_PT_softbody_edge,
    bl_ui.properties_physics_softbody.PHYSICS_PT_softbody_edge_aerodynamics,
    bl_ui.properties_physics_softbody.PHYSICS_PT_softbody_edge_stiffness,
    bl_ui.properties_physics_softbody.PHYSICS_PT_softbody_field_weights,
    bl_ui.properties_physics_softbody.PHYSICS_PT_softbody_goal,
    bl_ui.properties_physics_softbody.PHYSICS_PT_softbody_goal_settings,
    bl_ui.properties_physics_softbody.PHYSICS_PT_softbody_goal_strengths,
    bl_ui.properties_physics_softbody.PHYSICS_PT_softbody_object,
    bl_ui.properties_physics_softbody.PHYSICS_PT_softbody_simulation,
    bl_ui.properties_physics_softbody.PHYSICS_PT_softbody_solver,
    bl_ui.properties_physics_softbody.PHYSICS_PT_softbody_solver_diagnostics,
    bl_ui.properties_physics_softbody.PHYSICS_PT_softbody_solver_helpers,
    bl_ui.properties_render.RENDER_PT_color_management,
    bl_ui.properties_render.RENDER_PT_color_management_curves,
    bl_ui.properties_render.RENDER_PT_simplify_greasepencil,
    bl_ui.properties_render.RENDER_PT_simplify_render,
    bl_ui.properties_render.RENDER_PT_simplify_viewport,
    bl_ui.properties_texture.TEXTURE_PT_blend,
    bl_ui.properties_texture.TEXTURE_PT_clouds,
    bl_ui.properties_texture.TEXTURE_PT_colors,
    bl_ui.properties_texture.TEXTURE_PT_colors_ramp,
    bl_ui.properties_texture.TEXTURE_PT_context,
    bl_ui.properties_texture.TEXTURE_PT_custom_props,
    bl_ui.properties_texture.TEXTURE_PT_distortednoise,
    bl_ui.properties_texture.TEXTURE_PT_image,
    bl_ui.properties_texture.TEXTURE_PT_image_alpha,
    bl_ui.properties_texture.TEXTURE_PT_image_mapping,
    bl_ui.properties_texture.TEXTURE_PT_image_mapping_crop,
    bl_ui.properties_texture.TEXTURE_PT_image_sampling,
    bl_ui.properties_texture.TEXTURE_PT_image_settings,
    bl_ui.properties_texture.TEXTURE_PT_influence,
    bl_ui.properties_texture.TEXTURE_PT_magic,
    bl_ui.properties_texture.TEXTURE_PT_mapping,
    bl_ui.properties_texture.TEXTURE_PT_marble,
    bl_ui.properties_texture.TEXTURE_PT_musgrave,
    bl_ui.properties_texture.TEXTURE_PT_node,
    bl_ui.properties_texture.TEXTURE_PT_preview,
    bl_ui.properties_texture.TEXTURE_PT_stucci,
    bl_ui.properties_texture.TEXTURE_PT_voronoi,
    bl_ui.properties_texture.TEXTURE_PT_voronoi_feature_weights,
    bl_ui.properties_texture.TEXTURE_PT_wood,
    bl_ui.properties_view_layer.VIEWLAYER_PT_layer,
    bl_ui.properties_world.WORLD_PT_context_world,
    bl_ui.properties_world.WORLD_PT_custom_props,
    bl_ui.space_node.NODE_PT_texture_mapping,
    bl_ui.space_sequencer.SEQUENCER_PT_custom_props,
]
'''
def get_panels():
    exclude_panels = {
        'VIEWLAYER_PT_filter',
        'VIEWLAYER_PT_layer_passes',
    }

    panels = []
    for panel in bpy.types.Panel.__subclasses__():
        if hasattr(panel, 'COMPAT_ENGINES') and 'CYCLES' in panel.COMPAT_ENGINES:
            if panel.__name__ not in exclude_panels:
                panels.append(panel)

    return panels

def register():
    # Register  classes
    from bpy.utils import register_class, unregister_class
    for cls in classes:
        #print("class: {} class_name: {}".format(cls, cls.__name__))

        if hasattr(bpy.types, cls.__name__):
            print("   already registered")
            unregister_class(cls)
        register_class(cls)


    # Add properties
    bpy.types.Scene.indigo_engine = bpy.props.PointerProperty(type=IndigoRendererProperties)
    bpy.types.Camera.indigo_camera = bpy.props.PointerProperty(type=IndigoCameraProperties)
    bpy.types.Light.indigo_light_sun = bpy.props.PointerProperty(type=IndigoLightSunProperties)
    bpy.types.Light.indigo_light_hemi = bpy.props.PointerProperty(type=IndigoLightHemiProperties)

    bpy.types.Material.indigo_material = bpy.props.PointerProperty(name="Indigo Material Properties", type = IndigoMaterialProperties)
    bpy.types.Texture.indigo_texture = bpy.props.PointerProperty(name="Indigo Texture Properties", type = IndigoTextureProperties)


    nodeitems_utils.register_node_categories(IndigoRenderEngine.bl_idname, node_categories)

    # Add Indigo to all relevant UI elements
    for panel in get_panels():
    #for panel in ui_elements:
        panel.COMPAT_ENGINES.add(IndigoRenderEngine.bl_idname)

def unregister():

    # Remove Indigo from all relevant UI elements
    for panel in get_panels():
        if IndigoRenderEngine.bl_idname in panel.COMPAT_ENGINES:
            panel.COMPAT_ENGINES.remove(IndigoRenderEngine.bl_idname)        
    
    nodeitems_utils.unregister_node_categories(IndigoRenderEngine.bl_idname)

    # Unregister classes
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        if hasattr(bpy.types, cls.__name__):
            unregister_class(cls)

if __name__ == "__main__":
    unregister()
    print("\nRELOADING\n")
    register()




