import bpy
import bl_ui

from .. core import IndigoRenderEngine

narrowui = 180

class INDIGO_PT_lights(bpy.types.Panel):
    #bl_idname = "view3d.indigo_ui_lamps"
    bl_label = "Indigo Lamps"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "data"

    @classmethod
    def poll(cls, context):
        return context.scene.render.engine == IndigoRenderEngine.bl_idname and context.object.type == 'LIGHT'
    
    def draw(self, context):
        if context.light is not None:
            wide_ui = context.region.width > narrowui
            
            if wide_ui:
                self.layout.prop(context.light, "type", expand=True)
            else:
                self.layout.prop(context.light, "type", text="")
            
            if context.light.type not in ('SUN', 'HEMI'):
                self.layout.label(text='Unsupported lamp type')
                
class INDIGO_PT_light_sun(bpy.types.Panel):
    #bl_idname = "view3d.indigo_ui_lamp_sun"
    bl_label = "Indigo Sun+Sky Lamp"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "data"

    @classmethod
    def poll(cls, context):
        return context.scene.render.engine == IndigoRenderEngine.bl_idname and context.object.type == 'LIGHT' and context.object.data.type == 'SUN'
    
    def draw(self, context):
        indigo_engine = context.scene.indigo_engine
        col = self.layout.column()
        
        indigo_lamp = context.object.data.indigo_light_sun
        col.prop(indigo_lamp, 'turbidity')
        col.prop(indigo_lamp, 'model')
        #col.prop(indigo_lamp, 'uselayers')
        #if indigo_lamp.uselayers:
        #    col.prop_search(indigo_lamp, 'sunlayer', context.scene.indigo_lightlayers, 'lightlayers')
        #    col.prop_search(indigo_lamp, 'skylayer', context.scene.indigo_lightlayers, 'lightlayers')

class INDIGO_PT_light_hemi(bpy.types.Panel):
    #bl_idname = "view3d.indigo_ui_lamp_hemi"
    bl_label = "Indigo Hemi Lamp"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "data"
    COMPAT_ENGINES = {IndigoRenderEngine.bl_idname}

    @classmethod
    def poll(cls, context):
        return context.scene.render.engine == IndigoRenderEngine.bl_idname and context.object.type == 'LIGHT' and context.object.data.type == 'HEMI'
    
    def draw(self, context):
        indigo_engine = context.scene.indigo_engine
        col = self.layout.column()
        
        indigo_lamp = context.object.data.indigo_light_hemi
        col.prop(indigo_lamp, 'type')

        #if indigo_lamp.type == 'background':
            #col.prop(indigo_lamp, 'env_bg_SP_type')
            #if indigo_lamp.env_bg_SP_type == 'rgb':
            #    col.prop(indigo_lamp, 'env_bg_SP_rgb')
                #row = col.row(align=True)
                #row.prop(indigo_lamp, 'env_bg_SP_rgb_gain_val')
            #if indigo_lamp.env_bg_SP_type == 'blackbody':
            #    row = col.row(align=True)
            #    row.prop(indigo_lamp, 'env_bg_SP_blackbody_temp')
            #    row.prop(indigo_lamp, 'env_bg_SP_blackbody_gain')
            #if indigo_lamp.env_bg_SP_type == 'uniform':
            #    row = col.row(align=True)
            #    row.prop(indigo_lamp, 'env_bg_SP_uniform_val')
            #    row.prop(indigo_lamp, 'env_bg_SP_uniform_exp')
            #col.prop_search(indigo_lamp, 'layer', context.scene.indigo_lightlayers, 'lightlayers')
        if indigo_lamp.type == 'env_map':
            col.prop(indigo_lamp, 'env_map_path')
            col.prop(indigo_lamp, 'env_map_type')
            row = self.layout.row(align=True)
            row.prop(indigo_lamp, 'env_map_gain_val')
            row.prop(indigo_lamp, 'env_map_gain_exp')
            col = self.layout.column()
            #col.prop_search(indigo_lamp, 'layer', context.scene.indigo_lightlayers, 'lightlayers')
            