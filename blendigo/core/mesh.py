from blendigo.pyIndigo import Mesh

def export_indigo_mesh(mesh):
        #print("Exporting mesh {}...".format(mesh.name), end =" ")
        print("Exporting mesh {}...".format(mesh.name))

        indigo_mesh = Mesh(mesh.name)

        mesh.calc_loop_triangles()
        #if len(mesh.loop_triangles) < 1:
        #    return False

        num_uv_layers = len(mesh.uv_layers)
        if num_uv_layers < 1:
            uv_ptr = 0
            num_uv = 0
        else:
            uv_ptr = mesh.uv_layers[0].data[0].as_pointer()
            num_uv = len(mesh.uv_layers[0].data)

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
        
        
        #print("Vertices...", end =" ")
        print("    Vertices...")

        # Add vertex data - way faster with pointer to data!
        indigo_mesh.AddVerticesViaPointer(len(mesh.vertices), mesh.vertices[0].as_pointer(), 5)
        print("        done.")
        #print("done.", end =" ")

        # Old mesh vertex export operation
        #indigo_mesh.AddVertices(len(mesh.vertices), [x for v in mesh.vertices for x in v.co])

        print("    Faces...")
        #print("Faces...", end =" ")

        print(mesh.loop_triangles[0].__class__)

        if True:
            if (len(mesh.uv_layers) > 0):
                indigo_mesh.AddFacesWithUvs(len(mesh.loop_triangles), mesh.loop_triangles[0].as_pointer(), mesh.uv_layers[0].data[0].as_pointer(), 4, 12)
            else:
                indigo_mesh.AddFacesWithoutUvs(len(mesh.loop_triangles), mesh.loop_triangles[0].as_pointer(), 4)

            for f in mesh.loop_triangles:
                if f.use_smooth:
                    indigo_mesh.normal_smoothing = True
                    break

        else:
            # Get UV data, if any
            num_uv_sets = len(mesh.uv_layers)
            uv_data = []
            uv_indices = []
            uv_counter = 0

            #uv_pointer = mesh.tessface_uv_textures.data[0].as_pointer()
            
            if num_uv_sets > 0:
                for uv_layer in mesh.uv_layers:
                    for face in mesh.loop_triangles: # For each face
                        for loop_index in face.loops:
                            #face_uvs = layer_uvs.data[face.index]
                            #if len(face.vertices) == 3:
                            uv_data.extend(uv_layer.data[loop_index].uv)
                            #    uv_indices.append(uv_counter)
                            #    uv_counter += 3
                            #else:
                           #     uv_data.extend([face_uvs[0], face_uvs[1], face_uvs[2], face_uvs[3]])
                            #    uv_indices.append(uv_counter)
                            #    uv_counter += 4

                        uv_indices.append(uv_counter)
                        uv_counter += 3

                indigo_mesh.AddTextureCoordinates(uv_data)

            # Add faces with texture and material data

            faces = []

            num_smooth = 0

            if num_uv_sets > 0:
                for f in mesh.loop_triangles:
                    if f.use_smooth:
                        num_smooth += 1
                    uv_idx = uv_indices[f.index]
                    if len(f.vertices) == 4:
                        faces.append(1)
                        faces.extend(f.vertices[:4])
                        faces.extend([uv_idx, uv_idx + 1, uv_idx + 2, uv_idx + 3])
                        faces.append(f.material_index)
                    else:
                        faces.append(0)
                        faces.extend(f.vertices[:3])
                        faces.extend([uv_idx, uv_idx + 1, uv_idx + 2])
                        faces.append(f.material_index)

            else:
                for f in mesh.loop_triangles:
                    if f.use_smooth:
                        num_smooth += 1                    
                    if len(f.vertices) == 4:
                        faces.append(1)
                        faces.extend(f.vertices[:4])
                        faces.extend([0,0,0,0])
                        faces.append(f.material_index)
                    else:
                        faces.append(0)
                        faces.extend(f.vertices[:3])
                        faces.extend([0,0,0])
                        faces.append(f.material_index)
            indigo_mesh.AddFaces(len(mesh.loop_triangles), faces)
            indigo_mesh.normal_smoothing = num_smooth > 0

        print("        done.")

        
        for mat in mesh.materials:
            if mat is not None:
                indigo_mesh.AddMaterialUsed(mat.name)
        
        indigo_mesh.Finalize()

        # Remove render mesh
        #if mesh: bpy.data.meshes.remove(mesh)

        return indigo_mesh