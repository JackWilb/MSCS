from paraview.simple import *

# Set up render view
renderView1 = GetActiveViewOrCreate('RenderView')

# Load in vti data
vti_data = XMLImageDataReader(FileName=['/home/jwilburn/Projects/MSCS/2021-spring/6635-sci-vis/assignment2/data02/2d.vti'])

# set active source
SetActiveSource(vti_data)

# get active view
renderView1 = GetActiveViewOrCreate('RenderView')

# get layout
layout1 = GetLayout()

# show data in view
vti_dataDisplay = Show(vti_data, renderView1)



# create a new 'Warp By Scalar'
warpByScalar = WarpByScalar(Input=vti_data)
warpByScalar.Scalars = ['POINTS', 'Scalars_']

# Properties modified on warpByScalar (2.35 was recommended by paraview)
warpByScalar.ScaleFactor = 2.35

# show data in view
warpByScalarDisplay = Show(warpByScalar, renderView1)

# hide data in view
Hide(vti_data, renderView1)

# show color bar/color legend
warpByScalarDisplay.SetScalarBarVisibility(renderView1, True)

# update the view to ensure updated data information
renderView1.Update()