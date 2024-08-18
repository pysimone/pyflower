# The Pythagoras flower is an extension of the Pythagorean theorem:
# The area of the polygon built on the hypotenuse is equal
# to the sum of the areas of the polygons built on the cathets.
#
# By the class PythagorasFlower you can generate svg drawings
# for pythagoras flower with polygon with many sides.
#
# MIT License
#
# Copyright (c) 2024 Simone Bignetti
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import svg  # Install https://github.com/orsinium-labs/svg.py
import math

MARGIN = 10  # Margin for the BoxView
P_MIN = 3  # Minimum sides of the polygons. This shall be >= 3.
P_MAX = 12  # Maximum sides of the polygons


class PythagorasFlower:
    def __init__(self, left_cathetus: float = 30, right_cathetus: float = 40, sides: int = 3,
                 stroke='black', fill='white', animate: bool = False):
        """Initialize the Pythagoras flower

        :param left_cathetus: left cathetus of the triangle
        :param right_cathetus: right cathetus of the triangle
        :param sides: number of sides of the bigger polygon - Minimum is P_MIN - Maximum si P_MAX
        :param stroke: color of the lines
        :param fill: color of the area
        :param animate: activates the animation
        """
        if left_cathetus < 0 or right_cathetus < 0:
            raise Exception("Cathetus must be positive not null")
        self.left_cathetus = left_cathetus
        self.right_cathetus = right_cathetus
        self.sides = self._checked_sides_number(sides)
        self.stroke = stroke
        self.fill = fill
        self.animate = animate
        self.flower_corollas = []
        self.flower = svg.SVG()
        self._draw()

    @staticmethod
    def polygon_points(side_length: float, sides_number: int) -> list:
        """Calculates the points of the polygon

        :param side_length: the length of the side of the polygon
        :param sides_number: number of sides of the polygon
        :return: a list containing x y coordinates for svg.Polygon
        """
        external_angle = 2 * math.pi / sides_number
        points = [0, 0]
        x = 0
        y = 0
        for s in range(sides_number-1):
            x += side_length * math.cos(external_angle * s)
            y += side_length * math.sin(external_angle * s)
            points.append(x)
            points.append(y)
        return points

    @staticmethod
    def _checked_sides_number(sides_number: int) -> int:
        """Normalize the number of sides

        :param sides_number: number of sides from user
        :return: number of sides normalized for the flower
        """
        if sides_number < P_MIN:
            return P_MIN
        elif sides_number > P_MAX:
            return P_MAX
        else:
            return sides_number

    def _draw(self):
        """Draw the Pythagoras flower

        """
        # Calculate the dimension of the box for the flower

        # Some trigonometric stuff
        hypotenuse = self.get_hypotenuse()
        left_angle = math.acos(self.left_cathetus / hypotenuse)  # Angle under cathetus 1 (left)
        right_angle = math.acos(self.right_cathetus / hypotenuse)  # Angle under cathetus 2 (right)
        left_projection = self.left_cathetus * math.cos(left_angle)  # Projection of cathetus 1 to hypotenuse
        right_projection = self.right_cathetus * math.cos(right_angle)  # Projection of cathetus 2 to hypotenuse
        height = self.left_cathetus * self.right_cathetus / hypotenuse  # Height on hypotenuse
        # Width at left
        max_radius1 = self.left_cathetus / (
                2.0 * math.sin(math.pi / self.sides))  # Radius of the circle around the bigger polygon at left
        max_distance1 = max_radius1 * math.sin(
            math.pi / self.sides + left_angle)  # Distance from the vertex of the polygon and the center
        width_left = max_radius1 + max_distance1  # Width of the box to the left
        width_left = MARGIN + math.ceil(width_left / 10) * 10  # Width with margin

        # Width at right
        max_radius2 = self.right_cathetus / (
                2.0 * math.sin(math.pi / self.sides))  # Radius of the circle around the bigger polygon at right
        max_distance2 = max_radius2 * math.sin(
            math.pi / self.sides + right_angle)  # Distance from the vertex of the polygon to center
        width_right = max_radius2 + max_distance2  # Width of the box to the right
        width_right = math.ceil(width_right / 10) * 10 + MARGIN  # Width with margin

        # Width under
        max_radius_hypotenuse = hypotenuse / (2.0 * math.sin(math.pi / self.sides))  # Radius of hypotenuse circle
        max_distance_hypotenuse = max_radius_hypotenuse * math.cos(math.pi / self.sides)  # Apothem of cathetus circle
        width_under = max_radius_hypotenuse + max_distance_hypotenuse + height  # Width of the box to bottom
        width_under = math.ceil(width_under / 10) * 10 + MARGIN  # Width with margin

        # Width over
        angle_smaller = min(left_angle, right_angle)  # Smaller angle of the cathetus
        radius_bigger = max(max_radius1, max_radius2)  # Radius of the bigger circle of the cathetus
        max_distance_over = radius_bigger * math.cos(
            math.pi / self.sides - angle_smaller)  # Distance from hypotenuse to the center
        width_over = radius_bigger + max_distance_over - height  # Width of the box to the top
        width_over = MARGIN + math.ceil(width_over / 10) * 10  # Width with margin

        # Width
        box_width = width_left + width_right
        box_height = width_under + width_over

        # Here start the drawing of the flower

        # The base triangle
        triangle = svg.Polygon(points=[0, 0,
                                       -left_projection, height,
                                       right_projection, height],
                               fill=self.fill,
                               stroke=self.stroke,
                               stroke_width=1,
                               transform=[svg.Translate(width_left, width_over)]
                               )

        # The corolla
        elements = [triangle]
        for c, p in enumerate(range(self.sides, P_MIN - 1, -1)):
            if self.animate:
                animate_transform_elements_x = [svg.AnimateTransform(
                    attributeName="transform",
                    type="skewX",
                    values="-2;2;-2",
                    begin="0s",
                    dur="2s",
                    repeatCount="indefinite",
                    additive="sum"),]
                animate_transform_elements_y = [svg.AnimateTransform(
                    attributeName="transform",
                    type="skewY",
                    values="-2;2;-2",
                    begin="0s",
                    dur="2s",
                    repeatCount="indefinite",
                    additive="sum"), ]
            else:
                animate_transform_elements_x = None
                animate_transform_elements_y = None
            petal_left = svg.Polygon(points=self.polygon_points(self.left_cathetus, p),
                                     stroke=self.stroke,
                                     transform=[svg.Translate(width_left, width_over),
                                                svg.Rotate(180 - 180 / math.pi * left_angle)],
                                     elements=animate_transform_elements_x
                                     )
            petal_right = svg.Polygon(points=self.polygon_points(self.right_cathetus, p),
                                      stroke=self.stroke,
                                      transform=[svg.Translate(width_left, width_over),
                                                 svg.Scale(1, -1),
                                                 svg.Rotate(-180/math.pi*right_angle)],
                                      elements=animate_transform_elements_x
                                      )
            petal_under = svg.Polygon(points=self.polygon_points(hypotenuse, p),
                                      stroke=self.stroke,
                                      transform=[svg.Translate(width_left-left_projection, width_over+height),
                                                 ],
                                      elements=animate_transform_elements_y
                                      )
            corolla = svg.G(id=f"Corolla {self.sides-c-P_MIN}",
                            fill = self.fill,
                            elements=[petal_left, petal_right, petal_under])
            elements.append(corolla)
            self.flower_corollas.append(
                svg.SVG(
                    viewBox=svg.ViewBoxSpec(0, 0, width=box_width, height=box_height),
                    elements=[triangle, corolla])
            )
        self.flower_corollas.reverse()
        self.flower = svg.SVG(
            viewBox=svg.ViewBoxSpec(0, 0, width=box_width, height=box_height),
            elements=elements)

    def get_flower_SVG(self) -> svg.SVG:
        """Return the Pythagoras flower as SVG

        """
        return self.flower

    def get_flower_svg(self) -> str:
        """Return the Pythagoras flower as string

        """
        return str(self.flower)

    def get_corollas_SVG(self) -> list[svg.SVG]:
        """Return the list of the corollas of the Pythagoras flower as SVG

        """
        return self.flower_corollas

    def get_corollas_svg(self) -> list[str]:
        """Return the list of the corollas of the Pythagoras flower as string

        """
        return list(map(str, self.flower_corollas))

    def get_left_cathetus(self):
        """Return the left cathetus

        :return: length of the left cathetus
        """
        return self.left_cathetus

    def get_right_cathetus(self):
        """Return the right cathetus

        :return: length of the right cathetus
        """
        return self.right_cathetus

    def get_hypotenuse(self):
        """Return the hypotenuse

        :return: length of the hypotenuse
        """
        return math.hypot(self.left_cathetus, self.right_cathetus)

    def get_sides(self):
        """Return the number of sides of the bigger polygon

        :return: the number of sides
        """
        return self.sides

    def get_fill(self):
        """Return the fill color

        :return: the color of the fill
        """
        return self.fill

    def get_stroke(self):
        """Return the stroke color

        :return: the color of the stroke
        """
        return self.stroke

    def set_left_cathetus(self, left_cathetus: float):
        """Set the cathetus on the left

        :param left_cathetus: dimension of the left cathetus
        """
        if left_cathetus < 0:
            raise Exception("Cathetus must be positive not null")
        self.left_cathetus = left_cathetus
        self._draw()

    def set_right_cathetus(self, right_cathetus: float):
        """Set the cathetus on the right

        :param right_cathetus: dimension of the right cathetus
        """
        if right_cathetus < 0:
            raise Exception("Cathetus must be positive not null")
        self.right_cathetus = right_cathetus
        self._draw()

    def set_sides(self, sides: int = 3):
        """Set the number of sizes of the bigger polygon

        :param sides: number of sides
        """
        self.sides = self._checked_sides_number(sides)
        self._draw()

    def set_fill(self, fill):
        """Set the fill of the polygons

        :param fill: the fill color
        """
        self.fill = fill
        self._draw()

    def set_stroke(self, stroke):
        """Set the color of the line for the polygons

        :param stroke: the stroke color
        """
        self.stroke = stroke
        self._draw()