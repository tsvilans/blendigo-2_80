import bpy

def export_indigo_object(obj, indigo_mesh, matrix=None):

    if obj.type == 'MESH' and obj.name not in self.exported_objects.keys():
        print("Exporting object {}...".format(obj.name))
        
        if obj.data.name not in self.exported_meshes.keys():
            if not self.export_mesh(obj):
                print("Error exporting mesh {}".format(obj.data.name))
                return False
        
        
        indigo_model = Model.New(obj.name, indigo_mesh)
        #print ("   mesh name: %s" % obj.data.name)
        #print ("   mesh ptr : %s" % self.exported_meshes[obj.data.name].Ptr)
        if matrix == None:
            indigo_model.SetTransformation(obj.matrix_world, 0)
        else:
            indigo_model.SetTransformation(matrix, 0)
        
        materials = []
        emission_scales = []
        for mat in obj.data.materials:
            if mat == None:
                continue

            if mat.name in self.material_exporter.exported_materials.keys():
                materials.append(self.material_exporter.exported_materials[mat.name])

            '''
            if mat.indigo_material.indigo_material_emission.emission_scale:
                em = mat.indigo_material.indigo_material_emission
                value = em.emission_scale_value * 10 ** em.emission_scale_exp

                if em.emission_scale_measure == 'luminous_flux':
                    measure = Measure.LUMINOUS_FLUX
                elif em.emission_scale_measure == 'luminous_intensity':
                    measure = Measure.LUMINOUS_INTENSITY
                elif em.emission_scale_measure == 'luminance':
                    measure = Measure.LUMINANCE
                elif em.emission_scale_measure == 'luminous_emittance':
                    measure = Measure.LUMINOUS_EMITTANCE
                else:
                    measure = Measure.NONE

                emission_scales.append(EmissionScale(measure, value, self.material_exporter.exported_materials[mat.name]))

        '''
        indigo_model.SetMaterials(materials)
        indigo_model.SetEmissionScales(emission_scales)

        self.exported_objects[obj.name] = indigo_model
        #print("Added model %s..." % obj.name)

        return indigo_model
    return None