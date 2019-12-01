"""SCAD.

# Introduction

This module provides a Python interface to OpenSCAD.

"""

# MIT License
#
# Copyright (c) 2019 Wayne C. Gramlich (Wayne@Gramlich.Net)
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

# <----------------------------------------100 Characters----------------------------------------> #

from math import atan2, ceil, cos, degrees, pi, sin, sqrt
from typing import Any, IO, List
# import io


# P:
class P:
    """Represents a 3 dimensional point."""

    # P.__init__():
    def __init__(self, x: float = 0.0, y: float = 0.0, z: float = 0.0) -> None:
        """Initialize the point contents."""
        self.x: float = x
        self.y: float = y
        self.z: float = z

    # P.__add__():
    def __add__(self, point2: "P") -> "P":
        """Add two points together."""
        point1: P = self
        return P(point1.x + point2.x, point1.y + point2.y, point1.z + point2.z)

    # P.__mul__():
    def __mul__(self, scale: float) -> "P":
        """Multiply a point by a scale factor."""
        point: P = self
        return P(point.x * scale, point.y * scale, point.z * scale)

    # P.__rmul__():
    def __rmul__(self, scale: float) -> "P":
        """Multiply a point by a scale factor."""
        point: P = self
        return P(point.x * scale, point.y * scale, point.z * scale)

    # P.__sub__():
    def __sub__(self, point2: "P") -> "P":
        """Subtract two points from one another."""
        point1: P = self
        return P(point1.x - point2.x, point1.y - point2.y, point1.z - point2.z)

    # P.__str__():
    def __str__(self) -> str:
        """Convert a point to a string."""
        point: P = self
        x_text: str = "{0:.3f}".format(point.x)
        y_text: str = "{0:.3f}".format(point.y)
        z_text: str = "{0:.3f}".format(point.z)
        x_text = "0.000" if x_text == "-0.000" else x_text
        y_text = "0.000" if y_text == "-0.000" else y_text
        z_text = "0.000" if z_text == "-0.000" else z_text
        return f"P({x_text}, {y_text}, {z_text})"

    # P.__truediv__():
    def __truediv__(self, scale: float) -> "P":
        """Divide a point by a scale factor."""
        point: P = self
        return P(point.x / scale, point.y / scale, point.z / scale)

    # P.distance():
    def distance(self, point2) -> float:
        """Compute the distance between two points."""
        point1: P = self
        dx: float = point1.x - point2.x
        dy: float = point1.y - point2.y
        dz: float = point1.z - point2.z
        return sqrt(dx * dx + dy * dy + dz * dz)

    # P.rotate2d():
    def rotate2d(self, angle: float):
        """Rotate a point by angle around the origin."""
        # To rotate a point (x, y) around the origin, use the following formula:
        #
        #   x' = x * cos(angle) - y * sin(angle)
        #   y' = y * cos(angle) + x * sin(angle)
        point: P = self
        x: float = point.x
        y: float = point.y
        sin_angle: float = sin(angle)
        cos_angle: float = cos(angle)
        rotated_point: P = P(x * cos_angle - y * sin_angle, y * cos_angle + x * sin_angle, 0.0)
        return rotated_point

    # P.y_mirror():
    def y_mirror(self) -> "P":
        """Return the point mirrored across the Y axis."""
        point: P = self
        return P(-point.x, point.y, -point.z)


# Polygon:
class Polygon:
    """Represents a closed polygon of points."""

    # Polygon.__init__():
    def __init__(self, name: str, points: List[P] = []) -> None:
        """Initialize a Polygon.

        Args:
            *name* (*str*): The name for the polygon.
            *points* (*List*[*P*]): The list of points to initialize
                *polygon* (i.e. *self* with.)

        """
        # Stuff values into *polygon* (i.e. *self*):
        self.name: str = name
        self.points: List[P] = points[:]  # Copy the contents of *points*

    # Polygon.__getitem__():
    def __getitem__(self, index: int) -> P:
        """Fetch a Point from the Polygon.

        Args:
            *index* (*int*): Index into the polygon (i.e. *self*)
                points list.

        Returns:
            (*P*): Return the *index*'th *Point* from *polygon*

        """
        # Grab some values from *polygon* (i.e. *self*):
        polygon: Polygon = self
        name: str = polygon.name
        points: List[P] = polygon.points
        points_size: int = len(points)
        assert 0 <= index < points_size, (f"There are {points_size} Points in Polygon '{name}' "
                                          f"and index={index} is either negative or too big.")
        point: P = points[index]
        return point

    # Polygon.__len__():
    def __len__(self) -> int:
        """Return the number of points currently in the Polygon."""
        # Grab some values from *polygon* (i.e. *self*):
        polygon: Polygon = self
        points: List[P] = polygon.points
        size: int = len(points)
        return size

    # Polygon.__str__():
    def __str__(self):
        """Return a short string representation of a Polygon."""
        # Grab some values from *polygon* (i.e. *self*):
        polygon: Polygon = self
        name: str = polygon.name
        points: List[P] = polygon.points
        selected_points: List[P] = points if len(points) <= 2 else [points[0]] + [points[-1]]
        join_text: str = ", " if len(points) <= 2 else ", ..., "
        selected_point: P
        selected_point_texts: List[str] = ["P[{0:.3f}, {1:.3f}]".format(selected_point.x,
                                                                        selected_point.y)
                                           for selected_point in selected_points]
        selected_points_text = join_text.join(selected_point_texts)
        return f"Polygon('{name}', [{selected_points_text}])"

    # Polygon.arc():
    def arc_append(self, center: P, radius: float, start_angle: float, end_angle: float,
                   points_count: int) -> None:
        """Append an arc of points to a Polygon.

        Args:
            *origin* (*P*): The center of the arc.
            *radius* (*float*): The arc radius.
            *start_angle* (*float*): The starting angle for the arc.
            *end_angle* (*float*): The ending angle for the arc.
            *points_count* (*int*): The number of points along the arc.

        """
        # Grab some values from *polygon*:
        polygon: Polygon = self
        points: List[P] = polygon.points

        # Compute the total angle spanned and the delta angle increments:
        span_angle: float = end_angle - start_angle
        delta_angle: float = span_angle / float(points_count - 1)
        # print(f"start_angle={start_angle}={degrees(start_angle)}deg")
        # print(f"end_angle={end_angle}={degrees(end_angle}deg")
        # print(f"span_angle={span_angle}={degrees(span_angle)}deg")
        # print(f"delta_angle={delta_angle}={degrees(delta_angle}deg")
        center_x: float = center.x
        center_y: float = center.y
        index: int
        for index in range(points_count):
            angle: float = start_angle + index * delta_angle
            x: float = center_x + radius * cos(angle)
            y: float = center_y + radius * sin(angle)
            # print(f"[{index}]angle={degrees(angle} x={x} y={y}")
            points.append(P(x, y))

    # Polygon.circle():
    def circle_append(self, center: P, diameter: float, points_count: int) -> None:
        """Append a circle to Polygon.

        Args:
            *center*)

        """
        # Grab some values from *polygon* (i.e. *self*):
        polygon: Polygon = self
        points: List[P] = polygon.points

        # Compute some values that do not change over the loop iterations:
        delta_angle: float = (2 * pi) / points_count
        radius: float = diameter / 2.0
        center_x: float = center.x
        center_y: float = center.y

        # Append each circle *point* to the *polygon* *points*:
        index: int
        for index in range(points_count):
            # Compute the *x* and *y* coordinate from *center*, *radius*, and *angle*:
            angle: float = index * delta_angle
            x: float = center_x + radius * cos(angle)
            y: float = center_y + radius * sin(angle)
            point: P = P(x, y)
            points.append(point)

    # Polygon.indices_scad_lines_append():
    def indices_scad_lines_append(self, scad_lines: List[str],
                                  indent: str, start_index: int) -> int:
        """Append the list of Polygon point indices a lines list.

        Args:
            *scad_lines* (*List*[*str*]): The list of OpenSCAD lines to
                append to.
            *indent (*str): The indentation text to prefix to each line.
            *start_index* (*int*): The starting index for points.

        Returns:
            (*int*) Returns the *end_index* after the indices have been
                output.

        """
        # Grab some values from *polygon* (i.e. *self*):
        polygon: Polygon = self
        name: str = polygon.name
        points: List[P] = polygon.points

        # Compute *end_index* from *start_index* and *points_size*:
        points_size: int = len(points)
        end_index: int = start_index + points_size

        # Figure out how many slices to output (i.e. *slice_count*):
        slice_size: int = 25
        slices_count: int = int(ceil(float(points_size) / float(slice_size)))

        # Output some debugging information:
        scad_lines.append(f"{indent} // Polygon '{name}' {start_index}:{end_index-1}")

        # Now output each slice:
        slice_index: int
        for slice_index in range(slices_count):
            # Compute the *start_slice_index* and *end_slice_index* for this *slice_index*.
            # The last *slice_index* may be less the *slice_size* in size:
            start_slice_index: int = slice_index * slice_size
            end_slice_index: int = min((slice_index + 1) * slice_size, points_size)

            # Compute *indices* for the slice and convert the into a comma separated *line_text*:
            indices: List[int] = list(range(start_slice_index, end_slice_index))
            index: int
            line_text: str = ", ".join([str(start_index + index) for index in indices])

            # Compute the *front_text* and *end_text*, glue it together and append the line:
            front_text: str = "  [" if slice_index == 0 else "  "
            end_text: str = "]," if end_slice_index == points_size else ","
            scad_lines.append(f"{indent}{front_text}{line_text}{end_text}")
        return end_index

    # Polygon.point_append():
    def point_append(self, point: P) -> None:
        """Append a point to a Polygon."""
        # Grab *points* from *polygon* (i.e. *self*) and tack *point* onto the end:
        polygon: Polygon = self
        points: List[P] = polygon.points
        points.append(point)

    # Polygon.points_scad_lines_append():
    def points_scad_lines_append(self, scad_lines: List[str], indent: str, start_index: int) -> int:
        """Append the Polygon points to a list of lines.

        Args:
            *scad_lines* (*List*[*str*]): The list of OpenSCAD lines to
                append to.
            *indent (*str): The indentation text to prefix to each line.
            *start_index* (*int*): The starting index for points.

        Returns:
            (*int*) Returns the *end_index* after the points have been
                output.

        """
        # Grab some values from *polygon* (i.e. *self*):
        polygon: Polygon = self
        name: str = polygon.name
        points: List[P] = polygon.points

        # Compute *end_index* from *start_index* and *points_size*:
        points_size: int = len(points)
        end_index: int = start_index + points_size

        # Figure out the number of *slice_points* to output:
        slice_size: int = 4
        slices_count: int = int(ceil(float(points_size) / float(slice_size)))

        # Append a debugging line:
        scad_lines.append(f"{indent} // Polygon '{name}' {start_index}:{end_index-1}")

        # Sweep through *points* and output chunks of *slice_points*:
        slice_index: int
        for slice_index in range(slices_count):
            # Extract the next chunk of *slice_points*:
            slice_start: int = slice_index * slice_size
            slice_end: int = min((slice_index + 1) * slice_size, points_size)
            slice_points: List[P] = points[slice_start:slice_end]

            # Just to be paranoid, make sure we actually have at least one point:
            if slice_points:
                # Splice *splice_point* together as a comma separated list:
                point_texts: List[str] = []
                slice_point: P
                for slice_point in slice_points:
                    x_text: str = "{0:.3f}".format(slice_point.x)
                    y_text: str = "{0:.3f}".format(slice_point.y)
                    x_text = "0.000" if x_text == "-0.000" else x_text
                    y_text = "0.000" if y_text == "-0.000" else y_text
                    point_texts.append(f"[{x_text}, {y_text}]")
                slice_text: str = ', '.join(point_texts)
                scad_lines.append(f"{indent}  {slice_text}, "
                                  f"// {start_index + slice_start}:"
                                  f"{start_index + slice_end - 1}")
        return end_index

    def rotated_rectangle_append(self, center: P, dx: float, dy: float, angle: float):
        """Append a rotated rectangle to Polygon."""
        # Grab some values from *polygon* (i.e. *self*):
        polygon: Polygon = self
        points: List[P] = polygon.points

        # Compute some useful values:
        half_dx: float = dx / 2.0
        half_dy: float = dy / 2.0
        upper_right_corner: P = P(half_dx, half_dy)
        lower_right_corner: P = P(half_dx, -half_dy)
        upper_left_corner: P = P(-half_dx, half_dy)
        lower_left_corner: P = P(-half_dx, -half_dy)

        # Set *debugging* to *True* to print out some debugging information:
        debugging: bool = False
        if debugging:  # pragma: no cover
            print(f"center={center} dx={dx} dy={dy} angle={degrees(angle)}deg")
            print(f"half_dx={half_dx} half_dy={half_dy}")
            # print(f"4 corners = {upper_right_corner}, {lower_right_corner}, "
            #       f"{upper_left_corner}, {lower_left_corner}")

        # Compute the 4 rotated corners offset by *center*:
        rotated_upper_right_corner: P = upper_right_corner.rotate2d(angle)
        rotated_lower_right_corner: P = lower_right_corner.rotate2d(angle)
        rotated_upper_left_corner: P = upper_left_corner.rotate2d(angle)
        rotated_lower_left_corner: P = lower_left_corner.rotate2d(angle)
        if debugging:  # pragma: no cover
            print(f"4 rotated corners = {rotated_upper_right_corner}, "
                  f"{rotated_lower_right_corner}, "
                  f"{rotated_upper_left_corner}, {rotated_lower_left_corner}")

        # Append the points to the polygon:
        points.append(center + rotated_upper_right_corner)
        points.append(center + rotated_lower_right_corner)
        points.append(center + rotated_lower_left_corner)
        points.append(center + rotated_upper_left_corner)

    def slot_append(self, end_point1: P, end_point2: P,
                    slot_length: float, slot_width: float, points_count: int) -> None:
        """Append a slot to a Polygon.

        *end_point1* and *end_point2* define a line that the slot will
        be alinged with.  The center point between *end_point1* and
        *end_point2* is the center of the slot.  *slot_length* and
        *slot_width* specify the dimensions of the slot.

        Args:
            *end_point1* (*P*): One end point on the center-line of the
                slot.
            *end_point2* (*P*): The other end point on the center-line
                of the slot.
            *slot_length* (*float*): Specifies the overall length of
                the slot.
            *slot_width* (*float*): Specifies the width of the slot.
            *points_count* (*int*): Specifies the number of points
                to use to draw the rounded slot ends.

        """
        # Compute the *center* and *slot_angle* in radians:
        center: P = (end_point1 + end_point2) / 2.0
        slot_angle: float = atan2(end_point1.y - end_point2.y, end_point1.x - end_point2.x)

        # Compute the two arc centers:
        slot_radius: float = slot_width / 2.0
        half_slot_length: float = slot_length / 2.0
        degrees180: float = pi
        center1: P = P(center.x + half_slot_length * cos(slot_angle),
                       center.y + half_slot_length * sin(slot_angle))
        center2: P = P(center.x + half_slot_length * cos(slot_angle + degrees180),
                       center.y + half_slot_length * sin(slot_angle + degrees180))

        # Append the two slot arcs to *polygon* (i.e. *self*):
        polygon: Polygon = self
        degrees90: float = pi / 2.0
        polygon.arc_append(center1, slot_radius,
                           slot_angle - degrees90,
                           slot_angle + degrees90, points_count)
        polygon.arc_append(center2, slot_radius,
                           slot_angle + degrees180 - degrees90,
                           slot_angle + degrees180 + degrees90, points_count)


# Scad:
class Scad:
    """Base class that an OpenSCAD object, transform, etc.

    This base class basically just provides a name and is sub-classed to
    provide all of the functiontality.
    """

    # Scad.__init__()
    def __init__(self, name: str) -> None:
        """Create the base *Scad* object.

        Args:
            *name* (*str*): The name of the *Scad* object.

        """
        # Stuff *name* into the *scad* object (i.e. *self*):
        self.name: str = name

    # Scad.file_write():
    def file_write(self, scad_file: IO[Any]) -> None:
        """Write out a `.scad` file.

        Args:
            *scad_file* (*IO*[*Any*]):
                An IO object (usually to the file system) that can be
                written to.

        """
        # Grab some values from *scad* (i.e. *self*):
        scad: Scad = self
        name: str = scad.name

        # Store the contents of *scad* as a bunch of *scad_lines*:
        scad_lines: List[str] = list()
        scad_lines.append(f"// '{name}' File")
        scad.scad_lines_append(scad_lines, "")

        # Convert *scad_lines* into *scad_text*:
        scad_lines.append("")
        scad_text: str = '\n'.join(scad_lines)

        # Output *scad_text* to *scad_file*:
        assert scad_file.writable(), f"Unable to write out .scad for '{name}'"
        scad_file.write(scad_text)

    # Scad.scad_lines_append():
    def scad_lines_append(self, scad_lines: List[str], indent: str) -> None:  # pragma: no cover
        """Generate OpenSCAD lines (template method).

        This method is a place holder template that is sub-classed
        for generating OpenSCAD output lines.

        Args:
            *scad_lines* (*List*[*str*]): The list of lines to
                 append to.
            *indent* (*str*): The line indentation prefixe.

        """
        scad: Scad = self
        class_name: str = scad.__class__.__name__
        assert False, f"{class_name}.scad_lines_append not implemented yet."


# Scad Polygon:
class ScadPolygon(Scad):
    """Represents an OpenScad `polygon` command."""

    # ScadPolygon.__init__():
    def __init__(self, name: str, polygons: List[Polygon], convexity: int = -1) -> None:
        """Initialize an OpenSCAD polygon command.

        Args:
            *name*: (*str*): The name of OpenSCAD polygon command.
            *polygons*: (*List*[*Polygon*])

        """
        # Intilize the base class and stuff values into *scad_polygon* (i.e. *self*):
        super().__init__(name)
        self.convexity: int = convexity
        self.polygons: List[Polygon] = polygons[:]

    # ScadPolygon.__getitem__():
    def __getitem__(self, index: int) -> Polygon:
        """Return the selected Polygon.

        Args:
            *index* (*int*): The index into the *scad_polygon*
                (i.e. *self*) *Polygon*'s list to fetch.

        Returns:
            (*Polygon*) Returns the selected *Polygon*:

        """
        # Grab some values from *scad_polygon* (i.e. *self*):
        scad_polygon: ScadPolygon = self
        polygons: List[Polygon] = scad_polygon.polygons
        polygons_size: int = len(polygons)
        assert 0 <= index < polygons_size, (f"ScadPolygon '{scad_polygon.name}' only has "
                                            f"{polygons_size} Polygons, and index={index} "
                                            f"is out of range")
        polygon: Polygon = polygons[index]
        return polygon

    # ScadPolygon.__len__()
    def __len__(self):
        """Return the number of polygons in the ScadPolygon.

        Returns:
            (*int*) Returns the number of *Polygon*'s in *scad_polygon*
                (i.e. *self*.)

        """
        # Grab the *polygons* from *scad_polygon* (i.e. *self*):
        scad_polygon: ScadPolygon = self
        polygons: List[Polygon] = scad_polygon.polygons
        polygons_size: int = len(polygons)
        return polygons_size

    # ScadPolygon.append():
    def append(self, polygon: Polygon) -> None:
        """Append a Polygon to the ScadPolygon.

        Args:
            *polygon*: (*Polygon*): The *Polygon* to append to
                *scad_polygon* (i.e. *self*.)

        """
        # Grab some values from *scad_polygon* (i.e. *self*):
        scad_polygon: ScadPolygon = self
        polygons: List[Polygon] = scad_polygon.polygons
        polygons.append(polygon)

    # ScadPolygon.extend():
    def extend(self, new_polygons: List[Polygon]) -> None:
        """Append a list of Polygon's to the ScadPolygon.

        Args:
            *new_polygons*: (*List*[*Polygon*]): The *Polygon* to
                append to *scad_polygon* (i.e. *self*.)

        """
        # Grab some values from *scad_polygon* (i.e. *self*):
        scad_polygon: ScadPolygon = self
        polygons: List[Polygon] = scad_polygon.polygons
        polygons.extend(new_polygons)

    # ScadPolygon.scad_lines_append():
    def scad_lines_append(self, scad_lines: List[str], indent: str) -> None:
        """Append ScadPolygon commands to a lines list.

        Args:
            *scad_lines* (*List*[*str*]): The lines list to append the
                *scad_polygon* (i.e. *self*) to.
            *indent* (*str*): The indentatation prefix for each line.

        """
        # Grab some values from *scad_polygon* (i.e. *self*):
        scad_polygon: ScadPolygon = self
        convexity: int = scad_polygon.convexity
        name: str = scad_polygon.name
        polygons: List[Polygon] = scad_polygon.polygons
        polygons_size: int = len(polygons)

        # Start the polygon command:
        scad_lines.append(f"{indent}// ScadPolygon '{name} [0-{polygons_size-1}]'")
        scad_lines.append(f"{indent}polygon(points = [")

        # Output the polygon point values:
        next_indent: str = indent + " "
        index: int = 0
        for polygon in polygons:
            index = polygon.points_scad_lines_append(scad_lines, next_indent, index)

        # Next output the path indices:
        scad_lines.append(f"{indent} ], paths = [")
        index = 0
        for polygon in polygons:
            index = polygon.indices_scad_lines_append(scad_lines, next_indent, index)

        # Close off the command with the optional *convexity* value*:
        convexity_text: str = "" if convexity < 0 else f", convexity={convexity}"
        scad_lines.append(f"{indent} ]{convexity_text}); "
                          f"// End ScadPolygon '{name}' [0-{polygons_size-1}]")