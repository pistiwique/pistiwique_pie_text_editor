'''
Copyright (C) 2017 Legigan Jeremy AKA Pistiwique

Created by Legigan Jeremy AKA Pistiwique

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import bpy
import os

ADDON_PATH = bpy.utils.user_resource("SCRIPTS", "addons")


def get_addon_name():
    return __package__.split(".")[0]


def get_current_addon_path():
    return os.path.join(ADDON_PATH, get_addon_name()) + os.sep


def current_addon_exists():
    return os.path.exists(get_current_addon_path())


def save_text_block(text_block):
    if not text_block:
        return
    if not os.path.exists(text_block.filepath):
        return

    with open(text_block.filepath, mode="w") as file:
        file.write(text_block.as_string())


def get_current_text():
    """ Return the current text """

    return bpy.context.space_data.text


def get_selection(current_text):
    """ Return the index position of the start and the end of the selection """

    start_selection = current_text.current_character
    end_selection = current_text.select_end_character

    return start_selection, end_selection


def get_lines_selection(current_text):
    """ Return the index of the first and last selected lines """

    line_begin = current_text.current_line_index

    for line_end, line_obj in enumerate(current_text.lines):
        if line_obj == current_text.select_end_line:
            break

    return line_begin, line_end


def remap_line_index(line_begin, line_end):
    return line_end, line_begin


def remap_selection(start_index, end_index):
    return end_index, start_index


def clean_end_lines(current_text, start_line, end_line):
    """ Remove useless space and tabs at the end lines """

    for idx in range(start_line, end_line):
        current_text.lines[idx].body = current_text.lines[idx].body.rstrip()