from zope.app.generations.generations import SchemaManager

UVCSchemaManager = SchemaManager(
    minimum_generation = 1,
    generation = 2,
    package_name = __name__
)
