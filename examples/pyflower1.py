# In this example object Pythagoras Flower named pyf1 si created from class PythagorasFlower.
# Left cathetus is 30px long
# Right cathetus is 40px long
# The bigger polygon has 10 sides.
# The animation is activated,
# the lines are blue and the areas are red.
# The flower is saved in the file pyflower1.svg

import pyflower as pyf

pyf1 = pyf.PythagorasFlower(30,
                            40,
                            10,
                            animate=True,
                            fill='red',
                            stroke='blue')

with open('pyflower1.svg', "w") as drawing:
    drawing.write(pyf1.get_flower_svg())