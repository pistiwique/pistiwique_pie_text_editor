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
from bpy.types import Menu


class PTET_MT_pie_text_editor(Menu):
    bl_idname = "ide_like_tools.custom_text_editor"
    bl_label = "Text Editor"

    def draw(self, context):
        pie = self.layout.menu_pie()

        if context.space_data.text:
            # 4-left
            pie.operator('ide_like_tools.api_search', text="API search")
            # 6-right
            if "#" in context.space_data.text.current_line.body:
                pie.operator('ide_like_tools.toggle_comment', text="Uncomment")

            else:
                pie.operator('ide_like_tools.toggle_comment', text="Comment")

            pie.operator('text.debug')

            pie.operator('ide_like_tools.restart_blender')

        else:
            pie.operator('text.new', text='New', icon='ZOOMIN')