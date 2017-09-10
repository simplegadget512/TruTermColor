#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4 ft=python

import os
import colorutils
from enum import Enum


class Attributes(Enum):
    """https://en.wikipedia.org/wiki/ANSI_escape_code#Sequence_elements for reference"""
    BOLD = 1
    DIM = 2
    ITALIC = 3
    UNDERLINED = 4
    BLINK = 5
    FASTBLINK = 6
    REVERSE = 7
    INVISIBLE = 8
    STRIKETHRU = 9


class Color(colorutils.Color):
    def __mul__(self, other):
        if isinstance(other, float):
            r1, g1, b1 = self.rgb
        else:
            raise TypeError("Unsupported operand type(s) for *: '{0}' and '{1}'".format(type(self), type(other)))

        return Color((int(r1 * other), int(g1 * other), int(b1 * other)))


if os.getenv('COLORTERM') is None:
    raise RuntimeError('Not a truecolor terminal - use termcolor module instead')

Z_FORE = 38
Z_BACK = 48


def _e(color, z_level=Z_FORE, attr=set()):
    """Return escaped background color sequence"""
    return '\x01{}\x1b[{};2;{};{};{}m\x02'.format(
        ''.join(['\x1b[{}m'.format(i.value) for i in attr]),
        z_level,
        color.red,
        color.green,
        color.blue)


def _r():
    """Return reset sequence"""
    return '\x01\x1b[0m\x02'


"""
This is an opinionated palette. Most colors are defined as 96% of their standard HTML value to give them some headroom
when they are brightened. Black is raised a bit to give it some floorspace when dimmed. Non-standard colors are listed
at the bottom.
"""
PALETTE = {
    'white': Color(hex='#FFFFFF') * .96,
    'silver': Color(hex='#C0C0C0') * .96,
    'gray': Color(hex='#808080') * .96,
    'black': Color(rgb=(30, 30, 30)),
    'red': Color(hex='#FF0000') * .96,
    'maroon': Color(hex='#800000'),
    'yellow': Color(hex='#FFFF00') * .96,
    'olive': Color(hex='#808000'),
    'lime': Color(hex='#00FF00') * .96,
    'green': Color(hex='#008000'),
    'aqua': Color(hex='#00FFFF') * .96,
    'teal': Color(hex='#008080'),
    'blue': Color(hex='#0000FF'),
    'navy': Color(hex='#000080'),
    'fuschia': Color(hex='#FF00FF') * .96,
    'purple': Color(hex='#800080'),

    # Non-standard colors
    'brown': Color((127, 64, 0)),
    'full_white': Color(hex='#FFFFFF'),
    'full_black': Color(hex='#000000'),
}


def fore_text(txt, fore_color=PALETTE['white'], attr=set()):
    return '{}{}{}'.format(
        _e(fore_color, Z_FORE, attr),
        txt,
        _r())


def fore_print(txt, fore_color=PALETTE['white'], attr=set()):
    print(fore_text(
        txt,
        fore_color,
        attr))


def color_text(txt, fore_color=PALETTE['white'], back_color=PALETTE['black'], attr=set()):
    return '{}{}{}{}'.format(
        _e(fore_color, Z_FORE, attr),
        _e(back_color, Z_BACK),
        txt,
        _r())


def color_print(txt, fore_color=PALETTE['white'], back_color=PALETTE['black'], attr=set()):
    print(color_text(
        txt,
        fore_color,
        back_color,
        attr))


if __name__ == '__main__':
    color_print('TruTermColor w/ An Opinionated Palette', PALETTE['white'], PALETTE['black'],
                {Attributes.BOLD, Attributes.UNDERLINED})
    for fg in PALETTE:
        # print the color names and their components
        c_demo = ''.join([color_text(' \u25CF ', PALETTE[fg], PALETTE[bg]) for bg in PALETTE])
        c_name = fore_text('{:<12}:'.format(fg, str(PALETTE[fg])), PALETTE[fg], {Attributes.BOLD})
        print('{} {} {}/{}'.format(c_demo, c_name, PALETTE[fg].hex, PALETTE[fg]))
    print()
    color_print('Text Attributes', PALETTE['white'], PALETTE['black'], {Attributes.BOLD, Attributes.UNDERLINED})
    fore_print('NOTE: Some of the following codes may not be implemented in your terminal software', PALETTE['white'])
    for a in Attributes:
        fore_print('{}'.format(a.name.capitalize()), PALETTE['white'], {a})
