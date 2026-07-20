# -*- coding: utf-8 -*-
import io

f = "_build_L13.py"
s = io.open(f, encoding="utf-8").read()


def sub1(old, new):
    global s
    assert s.count(old) == 1, (s.count(old), old[:70])
    s = s.replace(old, new)


EASTINGS_YD = 'The eastings run 88 to 91 across this map.'
EASTINGS_SN = 'The eastings on this map read 67 to 71 from left to right.'

sub1(
    '            {"say": "Rings inside rings mean a hill. The smaller the ring, the higher the ground it encloses."},\n'
    '            {"pre": "Find Worsaw Hill in the north-east. Type how many closed rings are drawn inside the labelled contour.",',
    '            {"say": "Rings inside rings mean a hill. The smaller the ring, the higher the ground it encloses."},\n'
    '            {"pre": "Find Worsaw Hill in the north-east. Type the number on the vertical grid line immediately to its left.",\n'
    '             "hint": "The eastings read 76, 77, 78 from left to right.",\n'
    '             "done": "Hill located, so the rings you count next belong to it and not to its neighbour.",\n'
    '             "answer": 77},\n'
    '            {"pre": "Type how many closed rings are drawn inside the labelled contour.",',
)

sub1(
    '            {"say": "Index contours are drawn thicker so you can find a height quickly on a crowded slope."},\n'
    '            {"pre": "Find the labels 650 and 700 to the right of the middle of the map. Type the difference between those two heights, in metres.",',
    '            {"say": "Index contours are drawn thicker so you can find a height quickly on a crowded slope."},\n'
    '            {"pre": "Find the labels 650 and 700 to the right of the middle of the map. Type the number on the vertical grid line immediately to their left.",\n'
    '             "hint": "' + EASTINGS_SN + '",\n'
    '             "done": "Both labels are now pinned to one column of the grid, so you will count on the right slope.",\n'
    '             "answer": 69},\n'
    '            {"pre": "Type the difference between those two heights, in metres.",',
)

sub1(
    '            {"say": "Outwards from a summit is downhill. Inwards is uphill. That is the whole direction rule."},\n'
    '            {"pre": "Type the number printed on the thick ring round the fell, in metres.",',
    '            {"say": "Outwards from a summit is downhill. Inwards is uphill. That is the whole direction rule."},\n'
    '            {"pre": "Type the easting of the vertical grid line immediately to the left of Cow Close Fell.",\n'
    '             "hint": "' + EASTINGS_YD + '",\n'
    '             "done": "Fell located, so the ring you read next is certainly the right one.",\n'
    '             "answer": 88},\n'
    '            {"pre": "Type the number printed on the thick ring round the fell, in metres.",',
)

sub1(
    '            {"say": "The interval is never printed on a map. You work it out from two labelled lines."},\n'
    '            {"pre": "Find the two labels to the right of the middle of the map. Type the higher of the two contour values, in metres.",',
    '            {"say": "The interval is never printed on a map. You work it out from two labelled lines."},\n'
    '            {"pre": "Find the two labels to the right of the middle of the map. Type the number on the vertical grid line immediately to their left.",\n'
    '             "hint": "' + EASTINGS_SN + '",\n'
    '             "done": "Labels located, so the lines you count between are the ones the question means.",\n'
    '             "answer": 69},\n'
    '            {"pre": "Type the higher of the two contour values, in metres.",',
)

sub1(
    '            {"say": "Gradient is height gained divided by ground covered. The units you divide in are the units you answer in."},\n'
    '            {"pre": "Type the lower of the two contour heights named, in metres.",',
    '            {"say": "Gradient is height gained divided by ground covered. The units you divide in are the units you answer in."},\n'
    '            {"pre": "Type the easting of the vertical grid line immediately to the left of Cow Close Fell.",\n'
    '             "hint": "' + EASTINGS_YD + '",\n'
    '             "done": "Fell located, so the slope you measure is the western flank and not another one.",\n'
    '             "answer": 88},\n'
    '            {"pre": "Type the lower of the two contour heights named, in metres.",',
)

sub1('{"pattern": "divided_the_wrong_way", "expect": 0.005,',
     '{"pattern": "divided_the_wrong_way", "expect": 0.01,')

sub1(
    '            {"say": "A ratio gradient compares metres up with metres along, so both have to be in metres."},\n'
    '            {"pre": "Type the height climbed, in metres.",',
    '            {"say": "A ratio gradient compares metres up with metres along, so both have to be in metres."},\n'
    '            {"pre": "Type the easting of the vertical grid line immediately to the left of Cow Close Fell.",\n'
    '             "hint": "' + EASTINGS_YD + '",\n'
    '             "done": "Same slope as before, located the same way, so the two answers can be compared.",\n'
    '             "answer": 88},\n'
    '            {"pre": "Type the height climbed, in metres.",',
)

sub1(
    '            {"say": "A cross section is only the contour values met along a line, plotted in the order you meet them."},\n'
    '            {"pre": "Type the value of the labelled contour the line starts on, in metres.",',
    '            {"say": "A cross section is only the contour values met along a line, plotted in the order you meet them."},\n'
    '            {"pre": "Type the easting of the vertical grid line immediately to the left of Cow Close Fell.",\n'
    '             "hint": "' + EASTINGS_YD + '",\n'
    '             "done": "The line of section now has a fixed place on the map, which is what makes the profile repeatable.",\n'
    '             "answer": 88},\n'
    '            {"pre": "Type the value of the labelled contour the line starts on, in metres.",',
)

sub1(
    '            {"say": "On a crowded slope, arithmetic is safer than counting lines one by one with your eye."},\n'
    '            {"pre": "Type the highest of the labelled index values on the eastern side of the map, in metres.",',
    '            {"say": "On a crowded slope, arithmetic is safer than counting lines one by one with your eye."},\n'
    '            {"pre": "Type the easting of the vertical grid line immediately to the left of those labels.",\n'
    '             "hint": "The eastings run 34, 35, 36 across this map.",\n'
    '             "done": "Labels located, so both ends of the climb sit on the slope the question means.",\n'
    '             "answer": 35},\n'
    '            {"pre": "Type the highest of the labelled index values on the eastern side of the map, in metres.",',
)

sub1(
    'display="In grid square 3508, east of Heron Pike, the brown contour lines are packed so tightly that they almost touch.',
    'display="In grid square 3508, on the slope running east from Heron Pike, the brown contour lines are packed so tightly that they almost touch.',
)

sub1(
    '                {"say": "The interval is almost never printed. Two labelled lines will give it to you."},\n'
    '                {"pre": "Type the height labelled on the left-hand thick line, in metres.",',
    '                {"say": "The interval is almost never printed. Two labelled lines will give it to you."},\n'
    '                {"pre": "Type how many lines are drawn on this slope altogether, thick and thin.",\n'
    '                 "hint": "Count every line from the left-hand edge of the slope across to the right-hand edge.",\n'
    '                 "done": "Knowing how many lines there are stops you losing count part way through.",\n'
    '                 "answer": 6},\n'
    '                {"pre": "Type the height labelled on the left-hand thick line, in metres.",',
)

io.open(f, "w", encoding="utf-8").write(s)
print("patched ok")
