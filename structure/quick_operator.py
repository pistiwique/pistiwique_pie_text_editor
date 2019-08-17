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
import re

from bpy.types import Operator
from ..custom_operators.utils import get_current_text
from .utils import get_end_structure_line_index


class IDELikeToolsCopyClassIdentifier(Operator):
    ''' Copy in the clipboard
        - the bl_idname for a class operator
        - the class name for a class object '''

    bl_idname = 'ide_like_tools.copy_class_identifier'
    bl_label = "Copy Identifier"
    bl_options = {'REGISTER'}

    line_index = bpy.props.IntProperty(
            default=0,
            )

    def execute(self, context):
        current_text = get_current_text()
        end_class = (get_end_structure_line_index(current_text, self.line_index))
        to_clipboard = ""

        for line in current_text.lines[self.line_index:end_class]:
            if re.search("bl_idname(.)*=", line.body):
                idname = line.body.split("=")[-1]
                to_clipboard = idname.replace(" ", "")
                break

        if not to_clipboard:
            to_clipboard = current_text.lines[self.line_index].body[len(
                    "class "):-1]

        bpy.context.window_manager.clipboard = to_clipboard
        return {'FINISHED'}


class IDELikeToolsCopyFunctionName(Operator):
    ''' Copy the function's name with its arguments in the clipboard '''

    bl_idname = 'ide_like_tools.copy_function_name'
    bl_label = "Copy Function's Name"
    bl_options = {'REGISTER'}

    line_index = bpy.props.IntProperty(
            default=0,
            )

    def execute(self, context):
        current_text = get_current_text()
        line = current_text.lines[self.line_index]
        start_name = 4

        for idx, char in enumerate(line.body):
            if char == 'd':
                start_name += idx
                break

        bpy.context.window_manager.clipboard = line.body[start_name:-1]
        return {'FINISHED'}


class IDELikeToolsCopyVariableName(Operator):
    ''' Copy the variable's name in the clipboard '''

    bl_idname = 'ide_like_tools.copy_variable_name'
    bl_label = "Copy Variable's Name"
    bl_options = {'REGISTER'}

    line_index = bpy.props.IntProperty(
            default=0,
            )

    def execute(self, context):
        current_text = get_current_text()

        variable_name = current_text.lines[self.line_index].body.split(
                "=")[0].rstrip()

        bpy.context.window_manager.clipboard = variable_name
        return {'FINISHED'}


class IDELikeToolsCopyOperatorPropertyName(Operator):
    ''' Copy the variable's name in the clipboard '''

    bl_idname = 'ide_like_tools.copy_operator_property_name'
    bl_label = "Copy Properties's Name"
    bl_options = {'REGISTER'}

    line_index = bpy.props.IntProperty(
            default=0,
            )

    def execute(self, context):
        current_text = get_current_text()

        variable_name = current_text.lines[self.line_index].body.split(
                "=")[0].strip().rstrip()

        bpy.context.window_manager.clipboard = variable_name
        return {'FINISHED'}