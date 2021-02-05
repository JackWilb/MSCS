## Introduction to Vis

Goal:
> Categorize algorithms according to the structure and type of transformation

Basic algorithm types for scientific visualization:
- Structural
    - Geometric transformations alter input geometry but do not change the topology (e.g. rotation)
    - Topological transformations alter input top-ology but do not change geometry and attribute data (e.g. convert dataset from polygonal to unstructured grid)
    - Attribute transformations convert data attributes from one form to another, or create new attributes from the input data
    - Combined transformations change both dataset structure and attribute data (e.g. computing contour lines)
- Categorical 
    - Scalar algorithms operate on scalar data. (e.g. contour lines of temperature on a weather map)
    - Vector algorithms operate on vector data. (e.g. showing oriented arrows of airflow)
    - Tensor algorithms operate on tensor matrices (e.g. show the components of stress or strain)
    - Modeling algorithms generate dataset topology or geometry, or surface normals or texture data (e.g. For example, generating glyphs oriented according to the vector direction and then scaled according to the scalar value is a combined scalar/vector algorithm)

