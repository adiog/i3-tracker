# This file is a part of i3-tracker project.
# Copyright (c) 2017 Aleksander Gajewski <adiog@brainfuck.pl>.

import random
import re

import svgwrite


svgcolors = [
  "aliceblue",        "antiquewhite",       "aqua",                  "aquamarine",
  "azure",            "beige",              "bisque",                #"black",
  "blanchedalmond",   #"blue",               "blueviolet",            "brown",
  "burlywood",        "cadetblue",          "chartreuse",            "chocolate",
  "coral",            "cornflowerblue",     "cornsilk",              #"crimson",
  "cyan",             #"darkblue",
 # "darkcyan",
    "darkgoldenrod",
#  "darkgray",
  #"darkgreen",
  #"darkgrey",
    "darkkhaki",
 # "darkmagenta",      "darkolivegreen",
    "darkorange",        #    "darkorchid",
  #"darkred",
  "darksalmon",         "darkseagreen",          #"darkslateblue",
  #"darkslategray",    "darkslategrey",
  "darkturquoise",      #"darkviolet",
  #"deeppink",
    "deepskyblue",        #"dimgray",               "dimgrey",
  #"dodgerblue",
    #"firebrick",
    "floralwhite",    #       "forestgreen",
  #"fuchsia",
    "gainsboro",          "ghostwhite",            "gold",
  "goldenrod",        #"gray",               "green",                 "greenyellow",
  #"grey",
    "honeydew",           "hotpink",              # "indianred",
 # "indigo",
    "ivory",              "khaki",                 "lavender",
  "lavenderblush",    "lawngreen",          "lemonchiffon",          "lightblue",
  "lightcoral",       "lightcyan",          "lightgoldenrodyellow",  "lightgray",
  "lightgreen",       "lightgrey",          "lightpink",             "lightsalmon",
  "lightseagreen",    "lightskyblue",       "lightslategray",        "lightslategrey",
  "lightsteelblue",   "lightyellow",        "lime",                  "limegreen",
  "linen",
    #"magenta",            "maroon",
    "mediumaquamarine",
#  "mediumblue",
    #"mediumorchid",       "mediumpurple",
    "mediumseagreen",
  #"mediumslateblue",
    "mediumspringgreen",  "mediumturquoise",       #"mediumvioletred",
  #"midnightblue",
    "mintcream",          "mistyrose",             "moccasin",
  "navajowhite",
    #"navy",
    "oldlace",               "olive",
  "olivedrab",        "orange",           #  "orangered",             "orchid",
  "palegoldenrod",    "palegreen",          "paleturquoise",      #   "palevioletred",
  "papayawhip",       "peachpuff",          "peru",                  "pink",
  "plum",             "powderblue",         #"purple",                "red",
  "rosybrown",        #"royalblue",         # "saddlebrown",
        "salmon",
  "sandybrown",       #"seagreen",
    "seashell",         #     "sienna",
  "silver",           "skyblue",            #"slateblue",             "slategray",
  #"slategrey",
    "snow",               "springgreen",
   # "steelblue",
  "tan",            #  "teal",
    "thistle",               "tomato",
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


def duration_to_pixels(canvas_width, duration):
    return seconds_to_pixel(canvas_width, duration.total_seconds())


def printsvg_legend():
    height = 35
    width = 1920
    dwg = svgwrite.Drawing('static/test.svg', width='100%')
    canvas_width = 1700
    canvas_offset = 210
    dwg.add(dwg.line(start=(0,30), end=(width,30), stroke_width=1, stroke='black'))
    dwg.add(dwg.line(start=(canvas_offset,0), end=(canvas_offset,30), stroke_width=2, stroke='black'))
    #dwg.add(dwg.line(start=(canvas_offset+canvas_width,0), end=(canvas_offset+canvas_width,30), stroke_width=2, stroke='black'))
    for hour in range(24):
        box_start = seconds_to_pixel(canvas_width, 3600*hour)
        box_width = seconds_to_pixel(canvas_width, 3600)
        dwg.add(dwg.line(start=(canvas_offset+box_start,0), end=(canvas_offset+box_start,30), stroke_width=2, stroke='black'))
        dwg.add(dwg.line(start=(canvas_offset+box_start+box_width*0.5,20), end=(canvas_offset+box_start+box_width*0.5,30), stroke_width=1, stroke='black'))
        dwg.add(dwg.line(start=(canvas_offset+box_start+box_width*0.25,25), end=(canvas_offset+box_start+box_width*0.25,30), stroke_width=1, stroke='black'))
        dwg.add(dwg.line(start=(canvas_offset+box_start+box_width*0.75,25), end=(canvas_offset+box_start+box_width*0.75,30), stroke_width=1, stroke='black'))
        dwg.add(dwg.line(start=(canvas_offset+box_start+box_width,0), end=(canvas_offset+box_start+box_width,30), stroke_width=2, stroke='black'))
#        dwg.add(dwg.line(start=(canvas_offset+box_start+box_width*0.05,25), end=(canvas_offset+box_start+box_width*0.95,25), stroke_width=1, stroke='black'))
#        dwg.add(dwg.line(start=(canvas_offset+box_start+box_width*0.05,125),end=(canvas_offset+box_start+box_width*0.95,125), stroke_width=1, stroke='black'))
        if hour < 10:
            scale = 0.45
            hour = '0' + str(hour) + ':00'
        else:
            scale = 0.40
            hour = str(hour) + ':00'
        scale = 0.23
        #if hour > 0:
        dwg.add(dwg.text(str(hour),x=[canvas_offset+box_start+box_width*scale],y=[10], font_size="0.8em"))

    svg = dwg.tostring()
    svg = re.sub(r'<svg', f'<svg viewBox="0 0 {width} {height}"', svg)

    return svg

def printsvg(event_list, class_list):
    colors = get_colors(class_list)
    height = 100
    width = 1920
    canvas_width = 1700
    canvas_offset = 210
    svgs = {}
    for class_type in class_list + ['']:
        dwg = svgwrite.Drawing('static/test.svg', width='100%')
        dwg.add(dwg.line(start=(0,100), end=(width,100), stroke_width=1, stroke='lightgray'))
        dwg.add(dwg.line(start=(0,0), end=(width,0), stroke_width=1, stroke='lightgray'))
        for hour in range(25):
            box_start = seconds_to_pixel(canvas_width, 3600*hour)
            dwg.add(dwg.line(start=(canvas_offset+box_start,0), end=(canvas_offset+box_start,100), stroke_width=1, stroke='lightgray'))
            svgs[class_type] = dwg

    for event in event_list:
        box_start = timepoint_to_pixels(canvas_width, canvas_offset, event.datetime_point)
        box_width = duration_to_pixels(canvas_width, event.duration)
        box_vertical_margin = 5
        box_height = 90
        box_lower_left = (box_start, box_vertical_margin)
        box_upper_right = (box_width, box_height)
        box_color = colors[event.window_class]

        dwg = svgs['']
        link = dwg.add(dwg.a("#" + event.id_hash))
        link.add(dwg.rect(box_lower_left, box_upper_right, fill=box_color))

        dwg = svgs[event.window_class]
        link = dwg.add(dwg.a("#" + event.id_hash))
        if box_width > 5:
            link.add(dwg.rect(box_lower_left, box_upper_right, fill=box_color))
        else:
            box_lower_left = (box_start, box_vertical_margin)
            box_upper_right = (box_start, box_vertical_margin+box_height)
            link.add(dwg.line(start=box_lower_left, end=box_upper_right, stroke=box_color, stroke_width=2))

    output = {}
    for class_type in svgs:
        output[class_type] = re.sub(r'<svg', f'<svg id="svg_{class_type}" class="svg_sheet" style="display:none;" viewBox="0 0 {width} {height}"', svgs[class_type].tostring())

    return output, colors
