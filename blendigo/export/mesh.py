from blendigo.pyIndigo import Mesh

'''
Export Blender mesh using pointer to data
'''
def export_indigo_mesh(mesh):
        print("    Exporting mesh {}...".format(mesh.name))

        indigo_mesh = Mesh(mesh.name)

        mesh.calc_loop_triangles()

        if len(mesh.loop_triangles) < 1 or len(mesh.vertices) < 1:
            return None

        num_uv_layers = len(mesh.uv_layers)
        if num_uv_layers > 0 and len(mesh.uv_layers[0].data) > 0:
            uv_ptr = mesh.uv_layers[0].data[0].as_pointer()
            num_uv = len(mesh.uv_layers[0].data) 
        else:
            uv_ptr = 0
            num_uv = 0

        indigo_mesh.fromBlenderMesh( 
            len(mesh.vertices), mesh.vertices[0].as_pointer(),
            len(mesh.loop_triangles), mesh.loop_triangles[0].as_pointer(),
            num_uv, uv_ptr,
            mesh.loops[0].as_pointer(),
            mesh.polygons[0].as_pointer())

        for mat in mesh.materials:
            if mat is not None:
                indigo_mesh.AddMaterialUsed(mat.name)
        
        indigo_mesh.Finalize()

        return indigo_mesh