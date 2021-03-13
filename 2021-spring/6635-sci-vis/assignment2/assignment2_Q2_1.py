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

# create a new 'Plot Over Line'
plotOverLine = PlotOverLine(Input=vti_data)
plotOverLine.Source.Point2 = [4096.0, 2048.0, 0.0]

# show data in view
plotOverLine1Display = Show(plotOverLine, renderView1)

# Create a new 'Line Chart View'
lineChartView1 = CreateView('XYChartView')

# show data in view
Show(plotOverLine, lineChartView1)

# add view to a layout so it's visible in UI
AssignViewToLayout(view=lineChartView1, layout=layout1)

renderView1.ResetCamera()
renderView1.Update()
