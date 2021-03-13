from paraview.simple import *

# Set up render view
renderView1 = GetActiveViewOrCreate('RenderView')

# Define arrows
arrows = [Arrow() for x in range(16)]

# Define transforms
transforms = [Transform(Input=arrow) for arrow in arrows]

# Apply tip resolution, rotation, and show
for x in range(16):
    arrows[x].TipResolution = 12
    transforms[x].Transform.Rotate = [0, 0, x * 22.5]
    Show(transforms[x], renderView1)
