# This file is a part of [[$]] project.
# Copyright (c) 2017 Aleksander Gajewski <adiog@brainfuck.pl>.
import random

import svgwrite

#dwg = svgwrite.Drawing('static/test.svg')
#dwg.add(dwg.line((0, 0), (10, 0), stroke=svgwrite.rgb(10, 10, 16, '%')))
#dwg.add(dwg.text('Test', insert=(100, 200), fill='red'))
#dwg.save()
svgcolors = [
  "aliceblue",        "antiquewhite",       "aqua",                  "aquamarine",
  "azure",            "beige",              "bisque",                "black",
  "blanchedalmond",   "blue",               "blueviolet",            "brown",
  "burlywood",        "cadetblue",          "chartreuse",            "chocolate",
  "coral",            "cornflowerblue",     "cornsilk",              "crimson",
  "cyan",             "darkblue",           "darkcyan",              "darkgoldenrod",
  "darkgray",         "darkgreen",          "darkgrey",              "darkkhaki",
  "darkmagenta",      "darkolivegreen",     "darkorange",            "darkorchid",
  "darkred",          "darksalmon",         "darkseagreen",          "darkslateblue",
  "darkslategray",    "darkslategrey",      "darkturquoise",         "darkviolet",
  "deeppink",         "deepskyblue",        "dimgray",               "dimgrey",
  "dodgerblue",       "firebrick",          "floralwhite",           "forestgreen",
  "fuchsia",          "gainsboro",          "ghostwhite",            "gold",
  "goldenrod",        "gray",               "green",                 "greenyellow",
  "grey",             "honeydew",           "hotpink",               "indianred",
  "indigo",           "ivory",              "khaki",                 "lavender",
  "lavenderblush",    "lawngreen",          "lemonchiffon",          "lightblue",
  "lightcoral",       "lightcyan",          "lightgoldenrodyellow",  "lightgray",
  "lightgreen",       "lightgrey",          "lightpink",             "lightsalmon",
  "lightseagreen",    "lightskyblue",       "lightslategray",        "lightslategrey",
  "lightsteelblue",   "lightyellow",        "lime",                  "limegreen",
  "linen",            "magenta",            "maroon",                "mediumaquamarine",
  "mediumblue",       "mediumorchid",       "mediumpurple",          "mediumseagreen",
  "mediumslateblue",  "mediumspringgreen",  "mediumturquoise",       "mediumvioletred",
  "midnightblue",     "mintcream",          "mistyrose",             "moccasin",
  "navajowhite",      "navy",               "oldlace",               "olive",
  "olivedrab",        "orange",             "orangered",             "orchid",
  "palegoldenrod",    "palegreen",          "paleturquoise",         "palevioletred",
  "papayawhip",       "peachpuff",          "peru",                  "pink",
  "plum",             "powderblue",         "purple",                "red",
  "rosybrown",        "royalblue",          "saddlebrown",           "salmon",
  "sandybrown",       "seagreen",           "seashell",              "sienna",
  "silver",           "skyblue",            "slateblue",             "slategray",
  "slategrey",        "snow",               "springgreen",           "steelblue",
  "tan",              "teal",               "thistle",               "tomato",
  "turquoise",        "violet",             "wheat",                 "white",
  "whitesmoke",       "yellow",             "yellowgreen"]


def get_colors(class_list):
    colors = {}
    colors_to_assign = random.sample(svgcolors, len(class_list))
    for i,k in enumerate(class_list):
        colors[k] = colors_to_assign[i]
    return colors


def seconds_from_midnight(timepoint):
    return (timepoint - timepoint.replace(hour=0, minute=0, second=0, microsecond=0)).total_seconds()


def seconds_to_pixel(canvas_width, seconds):
    seconds_width = 24*60*60
    return seconds * canvas_width / seconds_width


def timepoint_to_pixels(canvas_width, canvas_offset, timepoint):
    return canvas_offset + seconds_to_pixel(canvas_width, seconds_from_midnight(timepoint))


def duration_to_pixels(canvas_width, canvas_offset, duration):
    return seconds_to_pixel(canvas_width, duration.total_seconds())


def printsvg(event_list, class_list):
    colors = get_colors(class_list)
    height = 130
    width = 1850
    dwg = svgwrite.Drawing('static/test.svg', height=height, width=width)
    canvas_width = 1830
    canvas_offset = 10
    for hour in range(24):
        box_start = seconds_to_pixel(canvas_width, 3600*hour)
        box_width = seconds_to_pixel(canvas_width, 3600)
        dwg.add(dwg.rect(insert=(canvas_offset+box_start+box_width*0.05,25),size=(box_width*0.95,5),style='color: black;'))
        dwg.add(dwg.rect(insert=(canvas_offset+box_start+box_width*0.05,125),size=(box_width*0.95,5),style='color: black;'))
        if hour < 10:
            scale = 0.45
        else:
            scale = 0.40
        if hour > 0:
            dwg.add(dwg.text(str(hour),x=[int(canvas_offset+box_start+box_width*scale)],y=[int(15)]))
    for event in event_list:
        box_start = timepoint_to_pixels(canvas_width, canvas_offset, event.datetime_point)
        box_width = duration_to_pixels(canvas_width, canvas_offset, event.duration)
        box_vertical_margin = 35
        box_height = 85
        box_lower_left = (canvas_offset+box_start, box_vertical_margin)
        box_upper_right = (box_width, box_height)
        box_color = colors[event.window_class]
        link = dwg.add(dwg.a("#" + event.id_hash))
        link.add(dwg.rect(box_lower_left, box_upper_right, fill=box_color))
    #dwg.save()
    return dwg.tostring(), colors
