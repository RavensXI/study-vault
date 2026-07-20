# -*- coding: utf-8 -*-
"""Build Geography Skills L14 'Map Interpretation' practice_data from scratch.

Every map fact below was read off the real OS extract pixels (see notes in the
agent report). Nothing here is invented.
"""
import io, json, os, sys
from _svg14 import OPENER, TEACH_BRONZE, TEACH_SILVER, TEACH_GOLD

R2 = "https://pub-aeb94e100e5a48f4a133be5bf206aecb.r2.dev/geography/os-maps/"
PENDLE = R2 + "pendle-hill-z16-final.jpg"
YORKS  = R2 + "yorkshire-dales-z15-final.jpg"
LAKES  = R2 + "lake-district-z16-final.jpg"
NORTH  = R2 + "northumberland-z15-final.jpg"


def box(pre, answer, hint, done=None, phase=None, post=None):
    s = {"pre": pre, "answer": answer, "hint": hint}
    if post:
        s["post"] = post
    if done:
        s["done"] = done
    if phase:
        s["phase"] = phase
    return s


def say(t):
    return {"say": t}


def mis(pattern, message, expect, note=None):
    m = {"pattern": pattern, "message": message, "expect": expect}
    if note:
        m["note"] = note
    return m


# ---------------------------------------------------------------- BRONZE ----
bronze = []

bronze.append({
    "image": PENDLE,
    "display": "The village of <strong>Worston</strong> is named near the middle "
               "of this map. Which grid square is it in? Give the four figures.",
    "solutions": [7642],
    "input_type": "single_value",
    "calculator": False,
    "hint": "Read the easting off the numbered line to the left of the village, "
            "then the northing off the numbered line below it.",
    "guided_steps": [
        say("A grid square is named by the two lines that meet at its <strong>bottom-left corner</strong>."),
        box("Find the word Worston. Run your finger straight down to the bottom edge. "
            "Type the easting of the nearest numbered vertical line to the left of the village.",
            76, "Eastings are the numbers printed along the top and bottom edges of the map.",
            done="Locating comes first. A square cannot be named until you know which lines the place sits between."),
        box("Now run your finger straight across to the left edge. Type the northing "
            "of the nearest numbered horizontal line below the village.",
            42, "Northings are printed up the left and right edges and get bigger going up the page."),
        box("Write the easting pair first and the northing pair second. Type the four figures with no space.",
            7642, "Along the corridor before up the stairs: the easting digits always come first.",
            phase="substitute"),
        box("Check by looking one square further east. Type the easting of that neighbouring column.",
            77, "Eastings rise by 1 for every square you move to the right.",
            done="Worston lies west of that line, so it is not in the neighbouring square. Checking the "
                 "square next door is the quickest way to catch a slip of one square."),
    ],
    "misconceptions": [
        mis("northing_before_easting",
            "The two pairs have been written the wrong way round. A grid reference always runs "
            "along the bottom edge before it runs up the side.", 4276),
        mis("top_right_corner",
            "You read the lines above and to the right of the village. A square takes its name "
            "from the lines at its bottom-left corner.", 7743),
    ],
})

bronze.append({
    "image": NORTH,
    "display": "Look at grid square <strong>9893</strong> on this map. Almost the whole "
               "square is one land use. Which one?",
    "options": ["A built-up town", "Coniferous forest",
                "Open moorland with no trees", "A large reservoir"],
    "solutions": [1],
    "input_type": "multiple_choice",
    "calculator": False,
    "hint": "Find the square first, then decide what the colour filling most of it stands for.",
    "guided_steps": [
        say("Name the square before you judge it: eastings first, then northings."),
        box("Find the vertical line labelled 98 along the bottom edge. Type the easting "
            "of the next numbered vertical line to its right.",
            99, "Eastings go up by 1 for every square you move right.",
            done="The square sits between those two vertical lines, so that is the strip you are working in."),
        box("Now find the horizontal line labelled 93. Type the northing of the line that forms "
            "the top edge of the square.",
            94, "Northings go up by 1 for every square you move up the page."),
        box("Pale green shading on this map stands for woodland. Type 1 if it covers most of "
            "that square, 2 if it covers only a small corner.",
            1, "Look at how much of the square is left white or another colour.",
            phase="substitute"),
        box("Check the alternatives. Type the number of towns drawn inside that square.",
            0, "Towns show as tight blocks of orange buildings with named streets.",
            done="No town and no large blue water body, so the shading that covers nearly all "
                 "the square is what names the land use."),
        say("The option describing that cover is <strong>Coniferous forest</strong>."),
    ],
    "misconceptions": [
        mis("green_read_as_builtup",
            "The pale green has been read as buildings. Check whether any orange building blocks "
            "appear inside the square at all.", 0),
        mis("shading_ignored",
            "Open moorland is left white or very pale on this map. Look again at what colour "
            "actually fills the square.", 2),
    ],
})

bronze.append({
    "image": LAKES,
    "display": "The words <strong>Heron Pike</strong> are printed on the fell in the east of "
               "this extract. Read the height printed on the thick contour line just below "
               "them. Give your answer in metres.",
    "solutions": [550],
    "input_type": "single_value",
    "calculator": False,
    "unit": "m",
    "hint": "Index contours are the thicker brown lines, and the number is printed inside a small "
            "gap in the line itself.",
    "guided_steps": [
        say("Find the words on the map first. The number you want sits right beside them."),
        box("Heron Pike is east of the line labelled 35. Type the easting of the numbered vertical "
            "line immediately to its left.",
            35, "Look along the bottom edge for the numbered vertical lines.",
            done="Locating the words fixes which part of the fell you are reading, so you cannot "
                 "pick up a label from a different slope."),
        box("Contour numbers are printed in a break in the line. Type 1 if the number below the "
            "words breaks a thick line, 2 if it sits on a thin one.",
            1, "Compare the width of that line with the thin lines on either side of it."),
        box("Read the number printed in that break and type it. It is the height of the contour in metres.",
            550, "The number is printed in full, so read all three digits.",
            phase="substitute"),
        box("Check it against its neighbour. Lower down and to the south-east the next labelled thick "
            "contour reads 500. Type the difference between the two labelled heights, in metres.",
            50, "Take the smaller labelled height away from the larger one.",
            done="Thick index contours on this map are drawn every 50 m, so two neighbouring labels "
                 "must differ by exactly that much. That is the check that the digits were read right."),
    ],
    "misconceptions": [
        mis("read_neighbouring_label",
            "That is the next labelled contour further downhill, not the one printed beside the words. "
            "Check which label the name actually sits against.", 500),
        mis("digit_dropped",
            "A digit has been dropped. Contour labels on this map are printed as full heights in metres.", 55),
    ],
})

bronze.append({
    "image": YORKS,
    "display": "The village of <strong>Litton</strong> sits in the north-east of this extract, "
               "just north of a numbered horizontal grid line. Type the number on that line.",
    "solutions": [74],
    "input_type": "single_value",
    "calculator": False,
    "hint": "Northings are the numbers printed up the left and right edges of the map.",
    "guided_steps": [
        say("Northings run across the map and are numbered up both sides."),
        box("Find the word Litton. Type the easting of the numbered vertical line immediately to its left.",
            90, "Eastings are the numbers along the top and bottom edges.",
            done="Pinning the village against a vertical line first stops you reading a number "
                 "off the wrong part of the map."),
        box("Now find the blue horizontal line that passes just below the village. Follow it to the "
            "edge of the map and type the number printed on it.",
            74, "Follow the line straight out to the left or right edge and read the number there.",
            phase="substitute"),
        box("Type the number on the next horizontal line below that one.",
            73, "Northings drop by 1 for every square you move down the page."),
        box("Check which side of the line the village is on. Type 1 if Litton is above the line you "
            "named, 2 if it is below it.",
            1, "Compare how far up the page the village sits against the line.",
            done="The village is on the higher side, so that line runs along the bottom of its row. "
                 "That is what makes it the right northing rather than the one below."),
    ],
    "misconceptions": [
        mis("one_square_too_far",
            "That is the next line down, a whole square too far south. Look for the line running "
            "closest below the village itself.", 73),
        mis("easting_given_for_northing",
            "That number was read from the bottom edge, so it is an easting. Northings are printed "
            "up the sides of the map.", 90),
    ],
})

bronze.append({
    "image": PENDLE,
    "display": "<strong>Worsaw Hill</strong>, in the north-east of this extract, is ringed by a "
               "thicker contour line with a number printed on it. Type that height in metres.",
    "solutions": [200],
    "input_type": "single_value",
    "calculator": False,
    "unit": "m",
    "hint": "The number is printed in a small gap in the thicker brown ring drawn round the hill.",
    "guided_steps": [
        say("Find the hill first. The label sits in a break in the ring around it."),
        box("Worsaw Hill is east of the line labelled 77. Type the easting of the numbered vertical "
            "line immediately to its right.",
            78, "Eastings rise by 1 for each square you move right.",
            done="The hill sits between eastings 77 and 78, which is where to hunt for the ring."),
        box("Type the northing of the numbered horizontal line that runs south of the hill.",
            43, "Northings are read up the left and right edges of the map."),
        box("Now read the number printed in the break in the thick ring, just above and right of the "
            "hill's name. Type it.",
            200, "The label sits in a gap in the ring, in the same brown as the contour.",
            phase="substitute"),
        box("Check it is a sensible index contour. These are drawn every 50 m. Type the remainder "
            "when your number is divided by 50.",
            0, "Divide by 50 and see what is left over.",
            done="An index contour must be a whole number of 50 m steps, so leaving nothing over "
                 "shows the label was read correctly and not misread by a digit."),
    ],
    "misconceptions": [
        mis("digit_dropped",
            "A digit has been dropped. Contour labels are printed as full heights in metres, not in tens.", 20),
        mis("grid_line_read_as_height",
            "That is the number on a blue grid line, not a height. Contour numbers are printed in "
            "brown inside a break in the contour itself.", 43),
    ],
})

bronze.append({
    "image": LAKES,
    "display": "In grid square <strong>3508</strong> one thick contour is labelled 550 and the next "
               "one downhill is labelled 500. Four thin contour lines are drawn between them. "
               "What is the contour interval on this map, in metres?",
    "solutions": [10],
    "input_type": "single_value",
    "calculator": False,
    "unit": "m",
    "hint": "Count the gaps between the lines, not the lines themselves, then share the height "
            "drop out between those gaps.",
    "guided_steps": [
        say("Two labelled heights and the lines between them are all you need."),
        box("Find the label 550 beside the words Heron Pike, then the label 500 lower down. Type the "
            "easting of the numbered vertical line that forms the western edge of square 3508.",
            35, "The first pair of digits in a square's name is its western easting.",
            done="Both labels sit inside the same square, so you are reading one continuous slope "
                 "rather than two different hillsides."),
        box("Type the drop in height between the two labelled contours, in metres.",
            50, "Take the smaller labelled height away from the larger one."),
        box("Four thin lines lie between them. Type how many gaps that makes between the higher "
            "labelled line and the lower one.",
            5, "A run of lines always leaves one more gap than there are lines inside it.",
            phase="substitute"),
        box("Share the drop out between those gaps. Type the height change across one gap, in metres.",
            10, "Divide the total drop by the number of gaps."),
        box("Check by climbing back up. Type the height you reach starting at the 500 contour and "
            "going up five gaps.",
            550, "Add five of your one-gap steps onto 500.",
            done="Five steps of that size lands exactly on the higher printed label, so the interval "
                 "must be right. If it overshot or fell short, the count of gaps would be wrong."),
    ],
    "misconceptions": [
        mis("divided_by_lines",
            "You divided by the number of lines rather than the number of gaps. Four lines inside a "
            "run leave one more gap than that.", 12.5),
        mis("gave_index_spacing",
            "That is the drop between the two labelled thick contours, not the step between "
            "neighbouring lines.", 50),
    ],
})

bronze.append({
    "image": PENDLE,
    "display": "The houses of <strong>Worston</strong> are drawn in a line either side of one "
               "minor road, rather than gathered into a block or scattered across the fields. "
               "What settlement shape is that?",
    "options": ["Nucleated", "Linear", "Dispersed", "A planned grid"],
    "solutions": [1],
    "input_type": "multiple_choice",
    "calculator": False,
    "hint": "Look at whether the buildings follow one line or spread out in every direction.",
    "guided_steps": [
        say("Shape questions are answered by how the buildings are arranged, not by how many there are."),
        box("Find Worston, west of the line labelled 77. Type the northing of the numbered horizontal "
            "line immediately above the village.",
            43, "Northings are read up the sides and rise going up the page.",
            done="Pinning the village to a square first makes sure you are describing the right cluster."),
        box("Type the number of roads the buildings are strung along.",
            1, "Trace the yellow road through the village and see whether the houses leave it."),
        box("Type 1 if the buildings follow that road in a line, 2 if they spread out equally in "
            "all directions.",
            1, "Look at how far the buildings reach away from the road on either side.",
            phase="substitute"),
        box("Check the alternative. Type the number of Worston's houses that stand out in the open "
            "fields with no road beside them.",
            0, "A scattered pattern would show houses stranded away from any road.",
            done="No detached block, and the houses hug one road, which is what fixes the shape."),
        say("That arrangement is the one named <strong>Linear</strong>."),
    ],
    "misconceptions": [
        mis("nucleated_confusion",
            "Nucleated means clustered tightly round a central point in a block. Look again at how "
            "far the buildings stretch along the road.", 0),
        mis("dispersed_confusion",
            "Dispersed means isolated farms with fields between them. Check how close together "
            "these buildings are drawn.", 2),
    ],
})

bronze.append({
    "image": YORKS,
    "display": "Litton stands in grid square <strong>9074</strong>. How many contour lines cross "
               "that square?",
    "solutions": [0],
    "input_type": "single_value",
    "calculator": False,
    "hint": "Contour lines are the thin brown ones; look right across the whole square before answering.",
    "guided_steps": [
        say("Draw the square in your head first: the lines meeting at its bottom-left corner are 90 and 74."),
        box("Type the easting of the numbered vertical line that forms the eastern edge of that square.",
            91, "Eastings rise by 1 for every square you move right.",
            done="The square runs from easting 90 across to 91 and upwards from northing 74, which "
                 "is the patch of ground to search."),
        box("Type the northing of the numbered horizontal line that forms the southern edge of the square.",
            74, "The first pair of digits is the easting, the second pair the northing."),
        box("Now look inside that square. Type how many brown contour lines you can find in it.",
            0, "Brown lines only: the blue lines are water and the yellow one is a road.",
            phase="substitute"),
        box("Type 1 if ground with no contour lines across it must be close to flat, 2 if it must be steep.",
            1, "A contour line only appears where the land climbs a whole step in height.",
            done="With no height step anywhere inside it, this valley floor is close to level, "
                 "which is exactly why the road and the village are here and not up on the fell."),
    ],
    "misconceptions": [
        mis("counted_non_contours",
            "You may have counted a road casing or a field boundary. Contour lines are brown and "
            "run in long smooth curves right across the ground.", 1),
        mis("interval_typed_as_count",
            "That is the contour interval, not a count of lines. The question asks how many lines "
            "are drawn inside the square.", 10),
    ],
})

# ---------------------------------------------------------------- SILVER ----
silver = []

silver.append({
    "image": PENDLE,
    "display": "Find <strong>Worston</strong> village and <strong>Worsaw Hill</strong>. In which "
               "compass direction does Worsaw Hill lie from Worston?",
    "options": ["North-east", "South-west", "Due west", "South-east"],
    "solutions": [0],
    "input_type": "multiple_choice",
    "calculator": False,
    "hint": "Settle east or west from the eastings first, then north or south from the page.",
    "guided_steps": [
        say("Direction always runs from the place named first, so you are standing at the village."),
        box("Type the easting of the numbered vertical line immediately to the left of Worston.",
            76, "Run your finger straight down from the village to the bottom edge.",
            done="Both places have to be pinned to the grid before a direction means anything at all."),
        box("Type the easting of the numbered vertical line immediately to the left of Worsaw Hill.",
            77, "Run your finger straight down from the hill to the bottom edge."),
        box("A larger easting means further east. Type 1 if the hill is east of the village, 2 if it is west.",
            1, "Compare the two eastings you have just typed.",
            phase="substitute"),
        box("Now compare their heights on the page. Type 1 if the hill is higher up the map than the "
            "village, 2 if it is lower down.",
            1, "Up the page is north on every map."),
        box("Check by turning round. Using N=1, NE=2, E=3, SE=4, S=5, SW=6, W=7, NW=8, type the number "
            "for the direction of the village from the hill.",
            6, "Opposite directions sit four places apart on that list.",
            done="The return direction sits four places along the list from the outward one, which "
                 "is what a half turn must give. If it did not, one of the two would be wrong."),
        say("East and north together give <strong>North-east</strong>."),
    ],
    "misconceptions": [
        mis("direction_reversed",
            "That is the direction of the village from the hill, not the hill from the village. "
            "Start at the place named first.", 1),
        mis("north_south_flipped",
            "The east is right but north and south have been swapped. Up the page is north.", 3),
    ],
})

silver.append({
    "image": LAKES,
    "display": "Find the words <strong>Greenhead Gill</strong> on this map. Which four-figure grid "
               "square are they printed in?",
    "solutions": [3408],
    "input_type": "single_value",
    "calculator": False,
    "hint": "Name the square from the two lines that meet at its bottom-left corner.",
    "guided_steps": [
        say("Find the words first, then name the square that holds them."),
        box("The words sit west of the line labelled 35. Type the easting of the numbered vertical "
            "line immediately to their left.",
            34, "Look along the bottom edge for the numbered vertical lines.",
            done="The words lie between eastings 34 and 35, so the easting half of the reference is settled."),
        box("Now find the numbered horizontal line immediately below the words. Type the number "
            "printed on it, ignoring any leading zero.",
            8, "Northings are read up the left and right edges of the map."),
        box("A four-figure square is the easting pair then the northing pair, and this map's northings "
            "are printed with a leading zero. Type the four figures with no space.",
            3408, "Keep the leading zero in the middle of the four figures.",
            phase="substitute"),
        box("Check the neighbour. Type the four figures of the square immediately to the east.",
            3508, "Add 1 to the easting pair and leave the northing pair alone.",
            done="The words sit west of that line, so they are not in the neighbouring square. "
                 "Naming the neighbour is the fastest way to prove you are one square out or not."),
    ],
    "misconceptions": [
        mis("northing_first",
            "The northing has been written first. A grid reference runs along the bottom edge "
            "before it runs up the side.", 834),
        mis("square_above",
            "You named the square above. A square takes its numbers from the lines at its "
            "bottom-left corner.", 3409),
    ],
})

silver.append({
    "image": YORKS,
    "display": "Look at every patch of green woodland shading on this extract, from the dale in the "
               "north-east to the narrow strips in the south. What do they all have in common?",
    "options": ["They all lie beside a river or a stream",
                "They all sit on the highest fell tops",
                "They all ring the summit contours",
                "They are spread evenly across the whole map"],
    "solutions": [0],
    "input_type": "multiple_choice",
    "calculator": False,
    "hint": "Trace a blue line through each patch of green before you decide.",
    "guided_steps": [
        say("Take the patches one at a time and see what runs through each of them."),
        box("Start in the north-east. Find the words Fosse Wood. Type the easting of the numbered "
            "vertical line immediately to their west.",
            90, "Eastings are numbered along the top and bottom edges.",
            done="Fixing one patch on the grid gives you somewhere solid to start the comparison."),
        box("Type 1 if a blue line runs through or along that patch, 2 if there is no water near it.",
            1, "The wide pale blue line running down the dale is the river."),
        box("Now drop to the south of the map, near Darnbrook Fell. Type 1 if the narrow green strips "
            "there also follow blue lines down the hillside, 2 if they sit on the open tops.",
            1, "The blue lines in the south are small streams, called gills on this map.",
            phase="substitute"),
        box("Type the number of green patches drawn inside grid square 8972, up on Cow Close Fell.",
            0, "That square is open fell: check whether any green appears in it at all."),
        box("Check the pattern holds at both ends of the map. Type 1 if every patch you checked had "
            "water beside it, 2 if some did not.",
            1, "Go back over the two you tested and the tops you searched.",
            done="Valley woods and hillside strips alike follow the water, because sheltered, wetter "
                 "ground in a gill is where trees survive on a grazed fell."),
        say("The option matching that pattern is <strong>They all lie beside a river or a stream</strong>."),
    ],
    "misconceptions": [
        mis("green_placed_on_tops",
            "The fell tops on this extract are left blank. Look again at what colour fills the ground "
            "around the summit contours.", 1),
        mis("no_pattern_seen",
            "The green is not spread evenly: it is concentrated into narrow strips. Follow one strip "
            "and see what runs along its length.", 3),
    ],
})

silver.append({
    "image": NORTH,
    "display": "Find <strong>King's Dod</strong> in the north-west corner and the words "
               "<strong>Harwood Forest</strong> in the north-east. In which direction do the words "
               "Harwood Forest lie from King's Dod?",
    "options": ["East", "West", "South", "North"],
    "solutions": [0],
    "input_type": "multiple_choice",
    "calculator": False,
    "hint": "Compare the eastings first, then check whether the two sit on nearly the same row.",
    "guided_steps": [
        say("You are standing at King's Dod, so the direction runs outwards from there."),
        box("Type the easting of the numbered vertical line immediately to the right of King's Dod.",
            97, "Eastings are numbered along the top and bottom edges of the map.",
            done="Both places need a grid line beside them before a direction can be judged fairly."),
        box("Type the easting of the numbered vertical line immediately to the left of the words "
            "Harwood Forest.",
            99, "Look for the last numbered vertical line before the words begin."),
        box("Type how many whole eastings apart those two lines are.",
            2, "Take the smaller easting away from the larger one.",
            phase="substitute"),
        box("Now compare the rows. Type 1 if the two are almost level on the page, 2 if one is far "
            "higher up than the other.",
            1, "Both sit only a little above the horizontal line labelled 94."),
        box("Type the number of numbered horizontal lines a straight line between the two would cross.",
            0, "A crossing only happens if one place is above a numbered line and the other below it.",
            done="Nearly three kilometres across and not one numbered line crossed up or down means "
                 "the route runs almost straight sideways, so a single compass point describes it, "
                 "not a diagonal."),
        say("Moving right across the map with almost no change up or down is <strong>East</strong>."),
    ],
    "misconceptions": [
        mis("direction_reversed",
            "That is the direction of King's Dod from the forest. Direction runs from the place "
            "named first.", 1),
        mis("minor_drop_overweighted",
            "The small drop down the page is far smaller than the move across it, so an up-or-down "
            "point on its own cannot describe this line.", 2),
    ],
})

silver.append({
    "image": PENDLE,
    "display": "A straight footpath is to be built from <strong>Worston</strong> village to the "
               "summit of <strong>Worsaw Hill</strong>. How many numbered grid lines would it "
               "cross altogether, counting eastings and northings together?",
    "solutions": [2],
    "input_type": "single_value",
    "calculator": False,
    "hint": "Work out the crossings across the map and the crossings up the map separately, "
            "then add them.",
    "guided_steps": [
        say("Locate both ends before you count anything at all."),
        box("Type the easting of the numbered vertical line immediately east of Worston.",
            77, "Run your finger down from the village to the bottom edge, then look one line right.",
            done="That line lies between the two places, so the path has to cross it."),
        box("Type the easting of the numbered vertical line immediately east of Worsaw Hill.",
            78, "Look for the last numbered vertical line before the eastern edge of the map."),
        box("The path stops at the hill, so it never reaches that far line. Type how many numbered "
            "vertical lines the path actually crosses.",
            1, "Only lines lying between the two places get crossed.",
            phase="substitute"),
        box("Now the horizontal lines. Worston is south of the line labelled 43 and the hill is north "
            "of it. Type how many numbered horizontal lines the path crosses.",
            1, "Again, count only the numbered lines that lie between the two places."),
        box("Add the two counts. Type the total number of numbered grid lines crossed.",
            2, "Add the vertical crossings to the horizontal crossings.",
            done="One vertical and one horizontal crossing is exactly what a route running north-east "
                 "into the next square along and the next square up must give."),
    ],
    "misconceptions": [
        mis("endpoints_counted",
            "The lines at the two ends have been counted as well. Only lines lying between the "
            "places are crossed.", 4),
        mis("one_direction_only",
            "Only one direction has been counted. A diagonal path crosses lines running both ways.", 1),
    ],
})

silver.append({
    "image": YORKS,
    "display": "In the south of this extract two thick contours are labelled 500 and 450. Further "
               "west another thick contour is labelled 600. How much higher is the 600 contour "
               "than the 450 one? Give your answer in metres.",
    "solutions": [150],
    "input_type": "single_value",
    "calculator": False,
    "unit": "m",
    "hint": "Take the lower labelled height away from the higher one.",
    "guided_steps": [
        say("Both numbers are printed on the map, so this is a reading job before it is a sum."),
        box("Find the label 450 in the south of the map. Type the easting of the numbered vertical "
            "line immediately to its west.",
            89, "Look along the bottom edge for the numbered vertical lines.",
            done="Locating each label first stops you pairing up two numbers from opposite ends "
                 "of the map by accident."),
        box("Now find the label 600 further west and higher up. Type the easting of the numbered "
            "vertical line immediately to its west.",
            88, "It sits one whole column further west than the other label."),
        box("Type the higher of the two labelled heights, in metres.",
            600, "Compare the two numbers you have just found.",
            phase="substitute"),
        box("Type the difference between the two labelled heights, in metres.",
            150, "Take the smaller labelled height away from the larger one."),
        box("Thick index contours here are drawn every 50 m. Type how many 50 m steps fit into "
            "your answer.",
            3, "Divide your difference by 50.",
            done="A whole number of index steps is what the difference between two index contours "
                 "must always come to, so the reading and the subtraction agree."),
    ],
    "misconceptions": [
        mis("wrong_pair_used",
            "The wrong pair of labels has been used. Check which two heights the question names.", 100),
        mis("index_step_given",
            "That is the gap between two neighbouring thick contours, not the gap between the two "
            "heights named in the question.", 50),
    ],
})

silver.append({
    "image": YORKS,
    "display": "The main road on this extract runs the length of the dale and never climbs over the "
               "fells. Which piece of map evidence best explains that route?",
    "options": ["No contour lines cross the valley floor square the road runs through, so it is almost level",
                "The fells are covered in forest, so no road could be cut through them",
                "The valley is the only part of the map with a river in it",
                "The road is drawn in yellow, and yellow always means a valley road"],
    "solutions": [0],
    "input_type": "multiple_choice",
    "calculator": False,
    "hint": "Compare the contour lines the road would meet in the valley with those it would meet "
            "on the fell.",
    "guided_steps": [
        say("Judge a route by what the map shows along each possible line, not by what sounds likely."),
        box("Follow the yellow road to Litton. Type the easting of the numbered vertical line "
            "immediately west of the village.",
            90, "Eastings are numbered along the top and bottom edges.",
            done="Fixing the road on the grid lets you compare its square with a fell square fairly."),
        box("Type the number of brown contour lines crossing grid square 9074, the square the road "
            "and the village share.",
            0, "Brown lines only: ignore the blue water and the yellow road itself."),
        box("Now look at grid square 8972 up on the fell. Type 1 if it carries many contour lines, "
            "2 if it carries none.",
            1, "Put the two squares side by side and compare them.",
            phase="substitute"),
        box("Type 1 if the valley square is the flatter of the two, 2 if the fell square is.",
            1, "Contour lines packed close together mean the ground changes height quickly."),
        box("Check what that means for people. Type the number of villages drawn up on the fell "
            "in square 8972.",
            0, "A village shows as a named cluster of orange buildings.",
            done="The level, contour-free square carries the road and the village, and the steep "
                 "square carries neither. That pairing is the evidence tying the route to the relief."),
        say("The option resting on that evidence is <strong>No contour lines cross the valley floor "
            "square the road runs through, so it is almost level</strong>."),
    ],
    "misconceptions": [
        mis("forest_assumed",
            "There is almost no woodland on these fells. Check what colour actually fills the "
            "fell squares.", 1),
        mis("colour_read_as_relief",
            "Road colour shows the class of road, not the shape of the land. Evidence about a route "
            "has to come from the contours.", 3),
    ],
})

# ------------------------------------------------------------------ GOLD ----
gold = []

gold.append({
    "image": LAKES,
    "display": "Every building on this extract is drawn in the west, and grid square "
               "<strong>3508</strong> has none at all. Which explanation is best supported by the "
               "map evidence?",
    "options": [
        "The west is low, near the contour labelled 100 m, with widely spaced contours and a main "
        "road along the valley floor, while the land eastwards climbs steeply past the contour "
        "labelled 550 m",
        "The west is the highest ground on the extract, and people build high for the view",
        "The eastern half is covered in forest, so there is no room to build there",
        "The eastern half is under water, so nothing can be built on it"],
    "solutions": [0],
    "input_type": "multiple_choice",
    "calculator": False,
    "hint": "Read the labelled contour beside the buildings and the labelled contour on the fell, "
            "then look at how tightly the lines are packed in each place.",
    "guided_steps": [
        say("A judgement question is still a reading question first. Collect the evidence, then choose."),
        box("Find the buildings in the west. Type the easting of the numbered vertical line that "
            "runs through them.",
            34, "It is the first numbered vertical line in from the western edge.",
            done="All the settlement sits around that line, which is the fact the whole judgement "
                 "rests on."),
        box("Type the height, in metres, printed on the thick contour just east of those buildings.",
            100, "The number is printed in a break in a thicker brown line."),
        box("Now cross to square 3508. Type the height, in metres, printed on the thick contour "
            "just below the words Heron Pike.",
            550, "Find the words on the fell, then read the number sitting under them.",
            phase="substitute"),
        box("Type the rise in height, in metres, between those two labelled contours.",
            450, "Take the lower labelled height away from the higher one."),
        box("Check where that climb leaves people. Type the number of buildings drawn inside "
            "square 3508.",
            0, "Buildings show as small orange blocks; that square carries contours and streams only.",
            done="A climb of that size across roughly a kilometre and a half, with not one building "
                 "on the steep side, is the map evidence that people here build on the low, "
                 "gently sloping valley floor."),
        say("The option built on that evidence is the <strong>first</strong> one."),
    ],
    "misconceptions": [
        mis("high_low_inverted",
            "The labelled contour beside the buildings is far lower than the one up on the fell, "
            "so the west cannot be the high ground. Compare the two printed heights.", 1),
        mis("forest_assumed",
            "There is no woodland shading in that square at all. Look again at what fills the "
            "eastern half of the map.", 2),
    ],
})

gold.append({
    "image": PENDLE,
    "display": "The green A road runs diagonally across the western half of this extract and stays "
               "well away from Worsaw Hill. Which explanation is best supported by the map?",
    "options": [
        "It keeps to lower, gently sloping ground where the contour lines are widely spaced, rather "
        "than climbing the hill ringed by the 200 m contour",
        "It follows Worston Brook along its whole length, because main roads are always built "
        "beside rivers",
        "It follows the 200 m contour round the hill, staying at the same height the whole way",
        "It hugs the woodland strips, which shelter it from the wind"],
    "solutions": [0],
    "input_type": "multiple_choice",
    "calculator": False,
    "hint": "Every option is a claim: test each one against the map before choosing.",
    "guided_steps": [
        say("Do not pick the option that sounds sensible. Pick the one the map can actually prove."),
        box("Find where the green A road crosses the horizontal line labelled 43. Type the easting "
            "of the numbered vertical line immediately west of that crossing point.",
            76, "Eastings are numbered along the top and bottom edges of the map.",
            done="That crossing fixes the road on the grid, so its ground can be compared with the "
                 "hill's ground."),
        box("Type the height, in metres, printed on the thick ring drawn round Worsaw Hill.",
            200, "The number sits in a break in the ring, beside the hill's name."),
        box("Type 1 if the green A road ever runs inside that ring, 2 if it stays outside it all "
            "the way across the map.",
            2, "Trace the road from the top edge to the bottom and watch how close it comes to the hill.",
            phase="substitute"),
        box("Type 1 if the contour lines along the road's route are widely spaced, 2 if they are "
            "packed as tightly as those on the hill.",
            1, "Wide gaps between contours mean the ground is rising only gently."),
        box("Test the claim about the brook. Type 1 if the road follows Worston Brook the whole way "
            "across the map, 2 if the two cross once and then part.",
            2, "Follow the brook east to west and the road north to south and see where they meet.",
            done="The road never enters the ring, keeps to widely spaced contours and only clips the "
                 "brook once, which knocks out every option but one."),
        say("The option resting on that evidence is the <strong>first</strong> one."),
    ],
    "misconceptions": [
        mis("road_follows_river",
            "The road and the brook meet at one point and then run apart in different directions. "
            "Trace both across the whole map.", 1),
        mis("contour_hugging_assumed",
            "Roads that stay at a constant height run parallel to a contour. Check whether this "
            "road goes anywhere near the ring at all.", 2),
    ],
})

gold.append({
    "image": YORKS,
    "display": "The village of <strong>Litton</strong> lies in grid square 9074. Which combination "
               "of map evidence best explains why a village grew on this spot?",
    "options": [
        "Level land on the valley floor with no contour lines crossing the square, a river alongside "
        "for water, and a road running the length of the dale",
        "High, exposed ground with steep contours packed on every side and wide views over the fells",
        "Thick woodland covering the whole square, giving timber and shelter on all sides",
        "A sheltered coastal inlet with a harbour for fishing boats"],
    "solutions": [0],
    "input_type": "multiple_choice",
    "calculator": False,
    "hint": "Check three things inside the square: contour lines, blue water and roads.",
    "guided_steps": [
        say("Site questions are answered by listing what the square actually contains."),
        box("Type the easting of the numbered vertical line that forms the western edge of square 9074.",
            90, "The first pair of digits in a square's name is its western easting.",
            done="Naming the edges first makes sure the evidence you gather comes from the right square."),
        box("Type the number of contour lines crossing that square.",
            0, "Brown lines only: ignore the blue water and the yellow road."),
        box("Type 1 if a river runs through or along the square, 2 if there is no water in it.",
            1, "The wide pale blue line running down the dale is the river.",
            phase="substitute"),
        box("Type 1 if a road runs through the square, 2 if it does not.",
            1, "The yellow line running the length of the dale is the road."),
        box("Test an alternative. Type the number of contour rings marking high ground inside the square.",
            0, "High ground shows as closed rings of brown contour lines.",
            done="Level ground, water and a road, and no high ground at all, is the exact combination "
                 "that puts a village on a valley floor rather than up on the fell."),
        say("The option listing that evidence is the <strong>first</strong> one."),
    ],
    "misconceptions": [
        mis("steep_site_assumed",
            "Steep ground shows as contour lines packed close together. Check whether any contour "
            "lines are drawn inside that square at all.", 1),
        mis("woodland_assumed",
            "Woodland shows as green shading. Check how much of that square is actually coloured green.", 2),
    ],
})

gold.append({
    "image": NORTH,
    "display": "A student claims this land is managed for commercial forestry rather than sheep "
               "farming. Which square gives the strongest evidence for that claim?",
    "options": [
        "Square 9893: woodland shading covers roughly four fifths of it and straight tracks run "
        "through the trees, with almost no buildings",
        "Square 9693: it carries more contour lines than 9893 does",
        "Square 9694: a hilltop there is ringed by the contour labelled 350 m",
        "Square 9893: a small pond is drawn near its eastern edge"],
    "solutions": [0],
    "input_type": "multiple_choice",
    "calculator": False,
    "hint": "Evidence has to point at the claim: a true fact about the wrong thing is not evidence.",
    "guided_steps": [
        say("Pick the option that shows the land use itself, not just something true about the land."),
        box("Type the easting of the numbered vertical line that forms the western edge of square 9893.",
            98, "The first pair of digits in a square's name is its western easting.",
            done="Squares are named from their bottom-left corner, so 98 and 93 fix the one to inspect."),
        box("Type 1 if woodland shading covers most of that square, 2 if it covers only a small part.",
            1, "Look at how much of the square is left white."),
        box("Type the number of villages or towns drawn inside that square.",
            0, "Settlements appear as clusters of orange buildings with names.",
            phase="substitute"),
        box("Straight pale lines run through the trees. Type 1 if they are tracks laid out for working "
            "the forest, 2 if they are rivers.",
            1, "Rivers are drawn in blue and wander; these lines are pale and run dead straight."),
        box("Now test the third option. Type the height, in metres, printed on the contour ringing "
            "the hilltop in square 9694.",
            350, "The number is printed in a break in the ring, beside the hilltop's name.",
            done="That height is a real reading, but a hilltop's height says nothing about how the "
                 "land is used. Only the tree cover and the working tracks answer the question asked."),
        say("The square carrying the land-use evidence is <strong>9893</strong>, described in the "
            "first option."),
    ],
    "misconceptions": [
        mis("slope_treated_as_landuse",
            "That comparison is true, but how steep a square is says nothing about what the land is "
            "used for. Look for evidence about cover and access instead.", 1),
        mis("trivial_evidence_chosen",
            "A pond is a real feature, but one small pond cannot show how a whole area is managed. "
            "Weigh how much of the square each option describes.", 3),
    ],
})

gold.append({
    "image": PENDLE,
    "display": "A landowner will open a small campsite in one of two squares: <strong>7642</strong>, "
               "which holds Worston, or <strong>7743</strong>, which holds Worsaw Hill. Which "
               "choice, with its reason, is best supported by the map?",
    "options": [
        "7642: it has a road for access, a named brook for water, and contour lines spaced more "
        "widely than those on the hill",
        "7743: the ring of contours shows the highest ground, and campers want the best view",
        "7743: it holds far more buildings than 7642, so services would be close by",
        "7642: it has no roads at all, so the site would be completely quiet"],
    "solutions": [0],
    "input_type": "multiple_choice",
    "calculator": False,
    "hint": "Score each square on access, water and how flat it is, then throw out any option the "
            "map contradicts.",
    "guided_steps": [
        say("Two squares, three tests: can you get there, is there water, and is it flat enough to "
            "pitch on."),
        box("Type the northing of the numbered horizontal line that forms the top edge of square 7642.",
            43, "The second pair of digits in a square's name is the northing along its bottom edge.",
            done="Fixing that line puts the two squares in their places, so the comparison runs "
                 "across it fairly."),
        box("Look inside square 7642. Type 1 if a road runs through it, 2 if it has none.",
            1, "Roads on this map are drawn in green, pink, yellow or grey."),
        box("Type 1 if a named brook runs through square 7642, 2 if there is no water in it.",
            1, "Worston Brook is labelled in blue lettering.",
            phase="substitute"),
        box("Now square 7743. Type the height, in metres, printed on the contour ringing Worsaw Hill.",
            200, "The number sits in a break in the thick ring."),
        box("Type 1 if the contour lines in square 7743 are packed more tightly than those around "
            "Worston, 2 if they are more widely spaced.",
            1, "Tightly packed lines mean the ground rises quickly."),
        box("Test the third option. Type the number of villages drawn inside square 7743.",
            0, "A village is a named cluster of buildings; a single farmhouse is not one.",
            done="The hill square has the steep ground and no village, and the valley square has road, "
                 "water and gentler slopes. That settles the choice on evidence rather than on what "
                 "sounds appealing."),
        say("The choice and reason the map supports is the <strong>first</strong> option."),
    ],
    "misconceptions": [
        mis("view_over_practicality",
            "Height and a view are not the only tests. Check how tightly the contours are packed "
            "where a tent would have to be pitched.", 1),
        mis("services_claim_unchecked",
            "Count the buildings drawn in each square before accepting a claim about which has more.", 2),
    ],
})

# ------------------------------------------------------------------ GUIDED --
guided = {
    "opener": {
        "display": OPENER,
        "steps": [
            say("No method yet. Just look and count."),
            {"pre": "Count the contour rings drawn round the hill.",
             "answer": 4,
             "hint": "Each ring is a separate loop, one inside the next.",
             "done": "Rings inside rings mean the ground rises to a point. That is a hill."},
            {"pre": "Now look at Site 1, on the flat ground between the road and the river. "
                    "Type how many contour rings cross it.",
             "answer": 0,
             "hint": "Follow each ring right round and see whether any of them touches the box.",
             "done": "Nothing crosses it, so nothing changes height across it."},
            {"pre": "Site 2 sits between the rings on the hillside. Type the number of the site you "
                    "would pitch a tent on.",
             "answer": 1,
             "hint": "Think about sleeping on a slope, and about carrying water and bags from the road.",
             "done": "You weighed flat ground, water and road access against each other without "
                     "being told to. That is the whole skill."},
            say("<strong>That is map interpretation.</strong> You did not read one thing off the map, "
                "you read several and put them together into a decision: flat ground, water nearby, "
                "a road to reach it. Every question in this lesson works the same way. Find the "
                "evidence on the map first, then say what it means."),
        ],
    },
    "teach": {
        "bronze": {
            "display": TEACH_BRONZE,
            "steps": [
                say("Bronze work is one reading at a time, and you are told where to look."),
                box("Find the block of woodland. Type the easting of the numbered vertical line "
                    "immediately to its left.",
                    53, "Eastings are numbered along the bottom edge.",
                    done="Locating before naming. Every map answer starts by finding the thing on "
                         "the sheet."),
                box("Type the northing of the numbered horizontal line immediately below the woodland.",
                    27, "Northings are numbered up the left edge."),
                box("Put the easting pair first. Type the four figures of the woodland's square, "
                    "with no space.",
                    5327, "Easting digits, then northing digits.",
                    phase="substitute"),
                box("Now the village of Kirkby, in the square to the west. Type how many buildings "
                    "are drawn there.",
                    5, "Buildings are the small orange blocks."),
                box("Check the village's square. Type its four figures.",
                    5227, "Same rule: the lines meeting at its bottom-left corner.",
                    done="Two squares side by side, one wooded and one built on, named the same way. "
                         "The method never changes, only what you find inside."),
                say("<strong>Bronze move:</strong> locate the feature, read the easting and the "
                    "northing that meet below and to its left, and name what the colour or symbol "
                    "shows."),
            ],
        },
        "silver": {
            "display": TEACH_SILVER,
            "steps": [
                say("Silver work asks you to find things yourself and put two facts together."),
                box("Type the easting of the numbered vertical line immediately to the left of the "
                    "words Nether Aln.",
                    61, "Eastings are numbered along the bottom edge.",
                    done="Pinning the village to a square is the set-up for describing it."),
                box("Type how many buildings are drawn above the road.",
                    4, "Count only the blocks sitting on the upper side of the thick grey line."),
                box("Type how many buildings are drawn below the road.",
                    5, "Count only the blocks sitting on the lower side of the road.",
                    phase="substitute"),
                box("Type the total number of buildings in the village.",
                    9, "Add the two counts together."),
                box("Type 1 if every one of them lies along the road, 2 if some sit out in the fields "
                    "away from it.",
                    1, "Look at how far any building strays from the grey line."),
                box("Now the site. Type 1 if the village sits on the low ground between the hill and "
                    "the river, 2 if it sits up on the hill itself.",
                    1, "The contour lines mark the hill; see which side of them the buildings are on.",
                    done="Buildings hugging one road on low ground between a hill and a river is both "
                         "a shape and a site, and the map proves each of them separately."),
                say("<strong>Silver move:</strong> find the feature without being told where, then "
                    "combine two pieces of evidence, such as the shape of the settlement and the "
                    "ground it stands on."),
            ],
        },
        "gold": {
            "display": TEACH_GOLD,
            "steps": [
                say("Gold work turns evidence into a decision, and the decision has to be justified."),
                box("Find site A. Type how many contour lines cross it.",
                    0, "Follow each brown line across the map and see whether it enters the box.",
                    done="Locating both sites and counting the lines through them is the evidence "
                         "gathering. The judgement comes after."),
                box("Type how many contour lines cross site B.",
                    3, "Count the brown lines that pass inside the shaded box on the fell."),
                box("Type 1 if site A has a road running past it, 2 if it does not.",
                    1, "The thick grey line is the road.",
                    phase="substitute"),
                box("Type 1 if site A has water beside it, 2 if it does not.",
                    1, "The blue line is the stream."),
                box("Score them. Give each site 1 point for flat ground, 1 for road access and 1 for "
                    "water. Type site A's score.",
                    3, "Site A has all three, so add them up."),
                box("Type site B's score on the same three tests.",
                    0, "Contour lines crossing a site mean it is not flat, and no road or stream "
                       "reaches it.",
                    done="Three tests passed against none is not an opinion, it is a count of map "
                         "evidence. That is what turns a preference into a justification."),
                say("<strong>Gold move:</strong> pick your criteria first, test both options against "
                    "each one, then quote the map evidence, not your instinct, as the reason."),
            ],
        },
    },
}

# ------------------------------------------------------------- TIER GUIDES --
tier_guides = {
    "bronze": {
        "title": "Bronze: one piece of map evidence",
        "steps": [
            "Find the feature on the map before you read anything: run down to the bottom edge for "
            "the easting, across to the side for the northing.",
            "Name a square from the two lines meeting at its <strong>bottom-left</strong> corner, "
            "easting pair first.",
            "For land use, read the colour or symbol. For height, read the number printed in the "
            "break in a thick contour line.",
        ],
        "example": {
            "question": "Which grid square holds the block of woodland lying east of easting 53 and "
                        "north of northing 27?",
            "steps": [
                {"label": "Locate it", "content": "<p>Woodland block found; run down to the bottom "
                                                  "edge and across to the side</p>"},
                {"label": "Read the two lines", "content": "<p>Easting 53, northing 27</p>"},
                {"label": "Check it makes sense", "content": "<p>Both lines meet at the bottom-left "
                                                             "corner of the wooded square, so they "
                                                             "are the right pair</p>"},
                {"label": "Answer", "content": "<p><strong>5327</strong></p>",
                 "isAnswer": True, "is_answer": True},
            ],
        },
    },
    "silver": {
        "title": "Silver: two pieces of evidence together",
        "steps": [
            "Nothing is pointed out for you, so locate both features yourself before comparing them.",
            "Direction runs from the place named first: compare eastings for east or west, then "
            "compare positions up the page for north or south.",
            "For settlement, describe the <strong>shape</strong> (linear, nucleated, dispersed) and "
            "the <strong>site</strong> (the ground it stands on) as two separate things.",
        ],
        "example": {
            "question": "Describe the shape and the site of a village of nine buildings strung along "
                        "one road on low ground between a hill and a river.",
            "steps": [
                {"label": "Shape", "content": "<p>All nine buildings follow one road, none out in "
                                              "the fields</p>"},
                {"label": "Site", "content": "<p>Low ground, below the contour lines of the hill and "
                                             "above the river</p>"},
                {"label": "Check it makes sense", "content": "<p>Shape describes the arrangement, "
                                                             "site describes the ground, so the two "
                                                             "answers do not overlap</p>"},
                {"label": "Answer", "content": "<p><strong>Linear in shape, on a low valley-floor "
                                               "site beside a river</strong></p>",
                 "isAnswer": True, "is_answer": True},
            ],
        },
    },
    "gold": {
        "title": "Gold: a judgement backed by map evidence",
        "steps": [
            "Decide your tests before you look: usually flat ground (contour spacing), water, and "
            "access by road or track.",
            "Test <strong>both</strong> options against every one of them, and write down what the "
            "map actually shows for each.",
            "Quote the evidence as your reason, and say why the losing option fails. An answer with "
            "no map evidence in it scores nothing.",
        ],
        "example": {
            "question": "Site A has no contour lines across it, a road past it and a stream beside "
                        "it. Site B has three contours across it and neither road nor stream. Which "
                        "is the better campsite, and why?",
            "steps": [
                {"label": "Flat ground", "content": "<p>A: no contours crossing. B: three crossing, "
                                                    "so it slopes</p>"},
                {"label": "Access and water", "content": "<p>A: road and stream. B: neither</p>"},
                {"label": "Check it makes sense", "content": "<p>A wins all three tests, so the "
                                                             "reason does not rest on a single "
                                                             "piece of evidence</p>"},
                {"label": "Answer", "content": "<p><strong>Site A, because it is flat, reached by "
                                               "road and has water beside it</strong></p>",
                 "isAnswer": True, "is_answer": True},
            ],
        },
    },
}

# ------------------------------------------------------------- METHOD CARD --
method_card = {
    "title": "Interpreting a Whole Map",
    "steps": [
        "Locate first: easting along the bottom, northing up the side",
        "Read the land use from colours and symbols",
        "Read the relief from contour spacing and the labelled heights",
        "Put the pieces together into one judgement, quoting the evidence",
    ],
    "content": "<p><strong>Land use.</strong> Green shading is woodland, orange blocks are buildings, "
               "blue is water. White or pale ground with no field pattern on high land is usually "
               "open moor.</p>"
               "<p><strong>Relief.</strong> Contours packed close together mean steep ground; wide "
               "gaps mean gentle ground; no contours at all in a square means it is close to level. "
               "Thick index contours carry the printed heights.</p>"
               "<p><strong>Settlement.</strong> Describe the shape (linear along a road, nucleated in "
               "a block, dispersed as scattered farms) and the site (valley floor, hilltop, river "
               "crossing) separately.</p>"
               "<p><strong>Judgement.</strong> Choose your tests, apply them to every option, and "
               "give the map evidence as the reason.</p>",
    "example": "<p><strong>Question:</strong> Why did a village grow in a square with no contour "
               "lines, a river and a road?</p>"
               "<p>No contours means level building land. The river gives water. The road gives "
               "access along the valley.</p>"
               "<p><strong>Answer:</strong> A valley-floor site: flat, watered and reachable.</p>",
}

# ------------------------------------------------------------------ EXTRAS --
topic_links = {
    "prerequisites": [
        {"slug": "geographical-skills/11", "title": "Grid References"},
        {"slug": "geographical-skills/12", "title": "Distance & Direction"},
        {"slug": "geographical-skills/13", "title": "Contours & Relief"},
    ]
}

exam_context = {
    "paper": "Paper 3: Geographical Applications",
    "frequency": "Very common: the longest map question on the paper is usually an interpretation one",
    "marks": "Longer answers: name the evidence on the map (a grid square, a contour height, a "
             "symbol) and then say what it means. Evidence with no explanation, or explanation with "
             "no evidence, only earns half the credit.",
}

worked_examples = [
    {
        "question": "Describe the site of the village of Litton, in grid square 9074.",
        "difficulty": "Bronze",
        "steps": [
            {"label": "Step 1: Locate the square",
             "content": '<img src="' + YORKS + '" alt="OS map extract: Littondale in the Yorkshire '
                        'Dales" style="max-width:100%;border-radius:8px;margin-bottom:0.5rem;">'
                        "<p>Run along the bottom edge to easting 90, then up the side to northing 74. "
                        "The village sits in the square above and to the right of where they meet.</p>"},
            {"label": "Step 2: List what the square contains",
             "content": "<p>No contour lines cross it, so the ground is close to level. A wide river "
                        "runs along it. A road runs the length of the dale through it.</p>"},
            {"label": "Answer",
             "content": "<p><strong>A valley-floor site: level ground beside a river, with a road "
                        "running along the dale.</strong></p>",
             "is_answer": True},
        ],
    },
    {
        "question": "How can you tell that the fell in grid square 3508 is much steeper than the "
                    "ground the village stands on?",
        "difficulty": "Silver",
        "steps": [
            {"label": "Step 1: Find the labelled heights",
             "content": '<img src="' + LAKES + '" alt="OS map extract: Greenhead Gill and Heron Pike '
                        'in the Lake District" style="max-width:100%;border-radius:8px;'
                        'margin-bottom:0.5rem;">'
                        "<p>A thick contour beside the village is labelled 100 m. A thick contour "
                        "beside the words Heron Pike is labelled 550 m.</p>"},
            {"label": "Step 2: Compare the spacing",
             "content": "<p>The rise is 450 m across roughly a kilometre and a half, and the lines "
                        "in the east are drawn almost touching, while those by the village are "
                        "widely spaced.</p>"},
            {"label": "Answer",
             "content": "<p><strong>Contours packed tightly and a 450 m rise over a short distance "
                        "both show steep ground; wide spacing by the village shows gentle "
                        "ground.</strong></p>",
             "is_answer": True},
        ],
    },
    {
        "question": "A campsite is to be opened in either square 7642 or square 7743. Justify a "
                    "choice using map evidence.",
        "difficulty": "Gold",
        "steps": [
            {"label": "Step 1: Choose the tests",
             "content": '<img src="' + PENDLE + '" alt="OS map extract: Worston and Worsaw Hill '
                        'below Pendle" style="max-width:100%;border-radius:8px;margin-bottom:0.5rem;">'
                        "<p>Flat ground, water and road access.</p>"},
            {"label": "Step 2: Test both squares",
             "content": "<p>7642 has Worston Brook, a minor road, an A road and widely spaced "
                        "contours. 7743 is ringed by the 200 m contour with lines packed close "
                        "together, and holds no village.</p>"},
            {"label": "Answer",
             "content": "<p><strong>Square 7642, because it is flatter, has a named brook for water "
                        "and roads for access, while 7743 is steep hillside with no road to "
                        "it.</strong></p>",
             "is_answer": True},
        ],
    },
]

practice_data = {
    "guided": guided,
    "method_card": method_card,
    "tier_guides": tier_guides,
    "topic_links": topic_links,
    "exam_context": exam_context,
    "problem_bank": {
        "bronze": bronze,
        "silver": silver,
        "gold": gold,
        "bronze_description": "One piece of map evidence at a time, and you are told where to look: "
                              "name a square, read a symbol, read a printed height.",
        "silver_description": "Find the features yourself, then put two pieces of evidence together: "
                              "a square and a direction, a shape and a site, two heights and a difference.",
        "gold_description": "Weigh several pieces of map evidence and justify a decision, saying why "
                            "the other option fails.",
    },
    "worked_examples": worked_examples,
}

HERE = os.path.dirname(os.path.abspath(__file__))
out = os.path.join(HERE, "lesson_L14.json")
with io.open(out, "w", encoding="utf-8") as f:
    json.dump(practice_data, f, ensure_ascii=False, indent=1)
print("wrote", out)
print("bronze", len(bronze), "silver", len(silver), "gold", len(gold))
