#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4 ft=python

import os

if os.getenv('COLORTERM') is None:
    raise RuntimeError('Not a truecolor terminal - use termcolor module instead')


def _gamut(component):
    """keeps color components in the proper range"""
    return min(max(int(abs(component)), 0), 255)


def hex_to_rgb(hex_string):
    """Return a tuple of red, green and blue components for the color
    given as #rrggbb.
    """
    return tuple(int(hex_string[i:i + 2], 16)
                 for i in range(1, len(hex_string), 2))


def rgb_to_hex(c_red=None, c_green=None, c_blue=None):
    """Return color as #rrggbb for the given color tuple or component
    values. Can be called as

    TUPLE VERSION:
        rgb_to_hex(COLORS['white']) or rgb_to_hex((128, 63, 96))

    COMPONENT VERSION
        rgb_to_hex(64, 183, 22)

    """
    if isinstance(c_red, tuple):
        c_red, c_green, c_blue = c_red
    return '#{:02X}{:02X}{:02X}'.format(
        c_red, c_green, c_blue)


def brighten(color, amount=.2):
    return (color * amount) + color


def dim(color, amount=.2):
    return (color / amount) + color


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
        color.c_red,
        color.c_green,
        color.c_blue)


def _r():
    """Return reset sequence"""
    return '\x01\x1b[0m\x02'


class Color:
    def __init__(self, c_red, c_green=None, c_blue=None):
        if isinstance(c_red, str) and c_red.startswith('#'):
            c_red, c_green, c_blue = hex_to_rgb(c_red)
        if isinstance(c_red, tuple):
            c_red, c_green, c_blue = c_red
        self.c_red = _gamut(c_red)
        self.c_green = _gamut(c_green)
        self.c_blue = _gamut(c_blue)

    def __str__(self):
        return '({}, {}, {})'.format(
            self.c_red, self.c_green, self.c_blue)

    def __add__(self, other):
        if isinstance(other, Color):
            return Color(
                _gamut(self.c_red + other.c_red),
                _gamut(self.c_green + other.c_red),
                _gamut(self.c_blue + other.c_red))
        else:
            return Color(
                _gamut(self.c_red + other),
                _gamut(self.c_green + other),
                _gamut(self.c_blue + other))

    def __sub__(self, other):
        return Color(
            _gamut(self.c_red - other.c_red),
            _gamut(self.c_green - other.c_green),
            _gamut(self.c_blue - other.c_blue))

    def __mul__(self, other):
        return Color(
            _gamut(self.c_red * other),
            _gamut(self.c_green * other),
            _gamut(self.c_blue * other))

    def __rmul__(self, other):
        return self.__mul__(other)

    def __floordiv__(self, other):
        return Color(
            _gamut(self.c_red // other),
            _gamut(self.c_green // other),
            _gamut(self.c_blue // other))

    def __truediv__(self, other):
        return Color(
            _gamut(self.c_red / other),
            _gamut(self.c_green / other),
            _gamut(self.c_blue / other))

    def __eq__(self, other):
        if isinstance(other, str) and other.startswith('#'):
            c_red, c_green, c_blue = hex_to_rgb(c_red)
            other = Color(c_red, c_green, c_blue)
        if isinstance(other, tuple):
            c_red, c_green, c_blue = c_red
            other = Color(c_red, c_green, c_blue)
        if self.c_red == other.c_red and self.c_green == other.c_green and self.c_blue == other.c_blue:
            return True
        return False


"""
This is an opinionated palette. Most colors are defined as 96% of their standard HTML value to give them some headroom
when they are brightened. Black is raised a bit to give it some floorspace when dimmed. Non-standard colors are listed
at the bottom.
"""
PALETTE = {
    'white': Color('#FFFFFF') * .93,
    'silver': Color('#C0C0C0') * .93,
    'gray': Color('#808080') * .93,
    'black': Color('#000000') + 25,
    'red': Color('#FF0000') * .93,
    'maroon': Color('#800000') * .96,
    'yellow': Color('#FFFF00') * .93,
    'olive': Color('#808000') * .93,
    'lime': Color('#00FF00') * .93,
    'green': Color('#008000') * .93,
    'aqua': Color('#00FFFF') * .93,
    'teal': Color('#008080') * .93,
    'blue': Color('#0000FF') * .93,
    'navy': Color('#000080') * .93,
    'fuschia': Color('#FF00FF') * .93,
    'purple': Color('#800080') * .93,

    # Non-standard colors
    'brown': Color((127, 64, 0)) * .93,
    'full_white': Color('#FFFFFF'),
    'full_black': Color('#000000'),
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
        print('{} {} {}'.format(c_demo, c_name, dim(PALETTE[fg], 4)))
    print()
    color_print('Text Attributes', PALETTE['white'], PALETTE['black'], bold=True, underline=True)
    fore_print('NOTE: Some of the following codes may not be implemented in your terminal software', PALETTE['white'])
    fore_print('Bold text', PALETTE['white'], bold=True)
    fore_print('Underline text', PALETTE['white'], underline=True)
    fore_print('Strikethru text', PALETTE['white'], strikethru=True)
    fore_print('Italic text', PALETTE['white'], italic=True)
    print()
    color_print('Color Functions', PALETTE['white'], PALETTE['black'], bold=True, underline=True)
    for fg in PALETTE:
        print('{} {} {}'.format(fore_text('{:<12}:'.format(fg, str(PALETTE[fg])), PALETTE[fg], bold=True),
                                            fore_text('Brighten', brighten(PALETTE[fg])),
                                            fore_text('Dimmed', dim(PALETTE[fg]))))
