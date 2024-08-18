# pyflower
The Pythagoras flower is an extension of the Pythagorean theorem:
the area of the polygon built on the hypotenuse is equal
to the sum of the areas of the polygons built on the cathetes.

By the class PythagorasFlower you can generate svg drawings
for Pythagoras flower with polygons with many sides.

This class is based on the library [svg.py](https://github.com/orsinium-labs/svg.py)
by [Orsinium Labs](https://github.com/orsinium-labs).
You have to install it to make pyflower run. 

## Usage

Import the library:

`import pyflower as pyf`

Create an object of the class PythagorasFlower:

`mypyf = pyf.PythagorasFlower(left_cathetus= 30, right_cathetus = 40, sides =10)`

When you instantiate a PythagorasFlower object you can set
the length of the cathetes, the number of sides of the bigger polygon or
activate the animation and set the colors of the lines and of the areas.
There are specific methods for these settings.

Save the string returned by the method *get_flower_svg*:

`mypyf.get_flower_svg()`

However, you can get the list of the corollas by the method *get_corollas_svg*:

`list_of_corollas = mypyf.get_corollas_svg()`

Look at the examples. Enjoy!