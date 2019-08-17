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

from bpy.types import Operator
from .punctuation_utils import smart_punctuation


class IDELikeToolsDoubleQuote(Operator):
    bl_idname = 'ide_like_tools.double_quote'
    bl_label = "Double quote"

    def execute(self, context):
        smart_punctuation('"' * 2)

        return {'FINISHED'}


class IDELikeToolsSimpleQuote(Operator):
    bl_idname = 'ide_like_tools.simple_quote'
    bl_label = "Simple quote"

    def execute(self, context):
        smart_punctuation("''")

        return {'FINISHED'}


class IDELikeToolsBracket(Operator):
    bl_idname = 'ide_like_tools.bracket'
    bl_label = "Bracket"

    def execute(self, context):
        smart_punctuation("()")

        return {'FINISHED'}


class IDELikeToolsSquareBracket(Operator):
    bl_idname = 'ide_like_tools.square_bracket'
    bl_label = "Square bracket"

    def execute(self, context):
        smart_punctuation("[]")

        return {'FINISHED'}


class IDELikeToolsBrace(Operator):
    bl_idname = 'ide_like_tools.brace'
    bl_label = "Brace"

    def execute(self, context):
        smart_punctuation("{}")

        return {'FINISHED'}