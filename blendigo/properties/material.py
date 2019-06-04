import bpy

from bpy.props import StringProperty, BoolProperty, FloatProperty, CollectionProperty, EnumProperty, IntProperty

INDIGO_MATERIAL_TYPES = [
	("DIFFUSE", "Diffuse", "Indigo Diffuse material", 0),
	("PHONG", "Phong", "Indigo Phong material", 1),
	]

class IndigoMaterialProperties(bpy.types.PropertyGroup):
	type: EnumProperty(
		items=INDIGO_MATERIAL_TYPES,
		name="Type",
		description="Indigo material type."
		)


class IndigoTextureProperties(bpy.types.PropertyGroup):
	path: StringProperty(
		name="Texture path",
		description="Texture_path")

	a: FloatProperty(
		name="a",
		description="a",
		default=1.0,
		)

	b: FloatProperty(
		name="b",
		description="b",
		default=1.0,
		)

	c: FloatProperty(
		name="c",
		description="c",
		default=1.0,
		)

	gamma: FloatProperty(
		name="Gamma", 
		description="Gamma",
		default=2.2,
		)
