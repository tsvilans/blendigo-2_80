import bpy

from .. core import IndigoRenderEngine
class INDIGO_PT_render_settings(bpy.types.Panel):
    #bl_idname = "view3d.indigo_render_engine_settings"
    bl_label = "Indigo Engine"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "render"

    @classmethod
    def poll(cls, context):
        return context.scene.render.engine == IndigoRenderEngine.bl_idname
    
    def draw(self, context):
        indigo_engine = context.scene.indigo_engine
        layout = self.layout
        col = layout.column()
        #col.prop(indigo_engine, 'render_mode')
        
        #if indigo_engine.render_mode == 'custom':

        col.label(text="Custom Options:")
        box = col.box()
        sub = box.column()
        row = sub.row()
        
        sc = row.column()
        #sc.prop(indigo_engine, 'gpu')
        sc.prop(indigo_engine, 'bidirectional')
        sc.prop(indigo_engine, 'metropolis')
        
        #sc = row.column()
        #sc.prop(indigo_engine, 'depth_pass')
        #sc.prop(indigo_engine, 'material_id')
        #sc.prop(indigo_engine, 'shadow')
            
        col.separator()
        
        #### TODO clamping, max contrib
        #box = col.box()
        #row = box.row()
        #row.prop(indigo_engine, 'clamp_contributions')
        #sub = row.row()
        #if not indigo_engine.clamp_contributions:
        #    sub.active = False
        #sub.prop(indigo_engine, 'max_contribution')
        
        
        col.label(text="Filter Settings:")
        box = col.box()
        sub = box.column()
        sub.prop(indigo_engine, 'supersampling')
        sub.prop(indigo_engine, 'splat_filter')
        sub.prop(indigo_engine, 'downsize_filter')
        '''
        sub.prop(indigo_engine, 'filter_preset')
        if indigo_engine.filter_preset == 'custom':
            sub.prop(indigo_engine, 'splat_filter')
            if indigo_engine.splat_filter == 'mitchell':
                sb = sub.row(align=True)
                sb.prop(indigo_engine, 'splat_filter_blur')
                sb.prop(indigo_engine, 'splat_filter_ring')
            sub.prop(indigo_engine, 'ds_filter')
            if indigo_engine.ds_filter == 'mitchell':
                sb = sub.row(align=True)
                sb.prop(indigo_engine, 'ds_filter_blur', text="Blur")
                sb.prop(indigo_engine, 'ds_filter_ring', text="Ring")
                sb.prop(indigo_engine, 'ds_filter_radius', text="Radius")
        '''
        
        row = layout.row()
        row.prop(indigo_engine, 'motionblur')
        row.prop(indigo_engine, 'foreground_alpha')
        
        col = layout.column()
        col.separator()
        
        col.label(text="Halt Settings:")
        box = col.box()
        sub = box.column()
        sr = sub.row(align=True)
        sr.prop(indigo_engine, 'halttime')
        sr.prop(indigo_engine, 'haltspp')
        #sr = sub.row()
        #sr.prop(indigo_engine, 'period_save')
        
        col = layout.column()
        col.separator()
        
        col.label(text="System Settings:")
        box = col.box()
        sub = box.column()
        sr = sub.row()
        sr.prop(indigo_engine, 'buffer_multiplier')
        sr.prop(indigo_engine, 'write_to_xml')
        #rc = sr.column()
        #rc.prop(indigo_engine, 'threads')
        #rc.enabled = not indigo_engine.threads_auto
        #sub.prop(indigo_engine, 'network_mode')
        #if indigo_engine.network_mode != 'off':
        #    sub.prop(indigo_engine, 'network_port')
        
        #col.separator()
        #row = col.row()
        #row.prop(indigo_engine, 'auto_start')
        #row.prop(indigo_engine, 'console_output', text="Print to console")
        
        ##
        #from .. properties.render_settings import IndigoDevice
        #
        #col = col.column(align=True)
        #col.label("Render Devices:")
        #for d in indigo_engine.render_devices:
        #    col.prop(d, 'use', text=d.platform+' '+d.device, toggle=True)
        #col.operator('indigo.refresh_computing_devices')
            
class RefreshComputingDevices(bpy.types.Operator):
    bl_idname = "indigo.refresh_computing_devices"
    bl_label = "Refresh Computing Devices"
    bl_description = ""
    bl_options = {"INTERNAL"}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        from .. properties.render_settings import get_render_devices
        get_render_devices(True)
        context.scene.indigo_engine.refresh_device_collection()
        return {"FINISHED"}
        
            
        
        
class INDIGO_PT_export_settings(bpy.types.Panel):
    bl_idname = "view3d.indigo_render_export_settings"
    bl_label = "Export Settings"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "render"

    @classmethod
    def poll(cls, context):
        return context.scene.render.engine == BL_IDNAME
    
    def draw(self, context):
        indigo_engine = context.scene.indigo_engine
        layout = self.layout
        col = layout.column()
        col.prop(indigo_engine, 'use_output_path')
        col = layout.column()
        col.prop(indigo_engine, 'export_path')
        col.enabled = not indigo_engine.use_output_path
        col = layout.column()
        col.prop(indigo_engine, 'install_path')
        col.prop(indigo_engine, 'skip_existing_meshes')
        
        col.separator()
        
        col.label("Output Settings:")
        box = col.box()
        sub = box.column()
        row = sub.row()
        
        sc = row.column()
        sc.prop(indigo_engine, 'save_exr_utm')
        sc.prop(indigo_engine, 'save_exr_tm')
        sc.prop(indigo_engine, 'save_igi')
        
        sc = row.column()
        sc.prop(indigo_engine, 'ov_watermark')
        sc.prop(indigo_engine, 'ov_info')
        sc.prop(indigo_engine, 'logging')
        