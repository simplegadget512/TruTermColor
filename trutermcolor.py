#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4 ft=python

import os
import colorutils


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


def _e(color, z_level=Z_FORE, attr_bold=False, attr_italic=False, attr_underlined=False, attr_strikethru=False):
    """Return escaped background color sequence"""
    return '\x01{}{}{}{}\x1b[{};2;{};{};{}m\x02'.format(
        '\x1b[1m' if attr_bold else '',
        '\x1b[3m' if attr_italic else '',
        '\x1b[4m' if attr_underlined else '',
        '\x1b[9m' if attr_strikethru else '',
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
    'white': Color(hex='#FFFFFF') * .95,
    'silver': Color(hex='#C0C0C0'),
    'gray': Color(hex='#808080'),
    'black': Color(rgb=(30, 30, 30)),
    'red': Color(hex='#FF0000'),
    'maroon': Color(hex='#800000'),
    'yellow': Color(hex='#FFFF00'),
    'olive': Color(hex='#808000'),
    'lime': Color(hex='#00FF00'),
    'green': Color(hex='#008000'),
    'aqua': Color(hex='#00FFFF'),
    'teal': Color(hex='#008080'),
    'blue': Color(hex='#0000FF'),
    'navy': Color(hex='#000080'),
    'fuschia': Color(hex='#FF00FF'),
    'purple': Color(hex='#800080'),

    # Non-standard colors
    'brown': Color((127, 64, 0)),
    'full_white': Color(hex='#FFFFFF'),
    'full_black': Color(hex='#000000'),
}


def fore_text(txt, fore_color=PALETTE['white'], bold=False, italic=False, underline=False, strikethru=False):
    return '{}{}{}'.format(
        _e(fore_color, Z_FORE, bold, italic, underline, strikethru),
        txt,
        _r())


def fore_print(txt, fore_color=PALETTE['white'], bold=False, italic=False, underline=False, strikethru=False):
    print(fore_text(
        txt,
        fore_color,
        bold,
        italic,
        underline,
        strikethru))


def color_text(txt, fore_color=PALETTE['white'], back_color=PALETTE['black'],
               bold=False, italic=False, underline=False, strikethru=False):
    return '{}{}{}{}'.format(
        _e(fore_color, Z_FORE, bold, italic, underline, strikethru),
        _e(back_color, Z_BACK),
        txt,
        _r())


def color_print(txt, fore_color=PALETTE['white'], back_color=PALETTE['black'],
                bold=False, italic=False, underline=False, strikethru=False):
    print(color_text(
        txt,
        fore_color,
        back_color,
        bold,
        italic,
        underline,
        strikethru))


if __name__ == '__main__':
    color_print('TruTermColor w/ An Opinionated Palette', PALETTE['white'], PALETTE['black'], bold=True, underline=True)
    for fg in PALETTE:
        # print the color names and their components
        c_demo = ''.join([color_text(' \u25CF ', PALETTE[fg], PALETTE[bg]) for bg in PALETTE])
        c_name = fore_text('{:<12}:'.format(fg, str(PALETTE[fg])), PALETTE[fg], bold=True)
        print('{} {} {}'.format(c_demo, c_name, PALETTE[fg]))
    print()
    color_print('Text Attributes', PALETTE['white'], PALETTE['black'], bold=True, underline=True)
    fore_print('NOTE: Some of the following codes may not be implemented in your terminal software', PALETTE['white'])
    fore_print('Bold text', PALETTE['white'], bold=True)
    fore_print('Underline text', PALETTE['white'], underline=True)
    fore_print('Strikethru text', PALETTE['white'], strikethru=True)
    fore_print('Italic text', PALETTE['white'], italic=True)
