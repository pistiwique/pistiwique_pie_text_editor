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

from collections import defaultdict
from bpy.types import Panel, Operator
from bpy.props import StringProperty, BoolProperty
from .utils import *
from ..icons.icons import load_icons


class_visibility = defaultdict(bool)

class IDELikeToolsStructurePanel(Panel):
    bl_idname = 'ide_like_tools_structure_panel'
    bl_label = "Structure"
    bl_space_type = 'TEXT_EDITOR'
    bl_region_type = 'UI'
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        return context.space_data.text

    def draw(self, context):
        current_text = context.space_data.text
        layout = self.layout
        structure_name = get_main_structure(current_text)
        if structure_name:
            for name in structure_name['ORDER']:
                value = structure_name[name]
                self.draw_tree(layout, current_text, name, value[0], value[1])
        else:
            layout.label("Not yet class or function")

    def draw_tree(self, layout, current_text, name, type, line):
        icons = load_icons()
        class_icon = icons.get("class_icon")
        function_icon = icons.get("function_icon")
        method_icon = icons.get("method_icon")
        variable_icon = icons.get("variable_icon")
        class_function = icons.get("class_function_icon")

        operator_selector = {
            'C': ["ide_like_tools.copy_class_identifier", class_icon],
            'F': ["ide_like_tools.copy_function_name", function_icon],
            'V': ["ide_like_tools.copy_variable_name", variable_icon],
            }

        is_visible = self.is_class_visible(name)

        row = layout.row(align=True)
        row.alignment = 'LEFT'

        if type == 'V':
            row.label(icon='BLANK1')

        else:
            icon = 'TRIA_DOWN' if is_visible else 'TRIA_RIGHT'
            props = row.operator('ide_like_tools.set_tree_visible', text="",
                                 icon=icon, emboss=False)
            props.class_name = name
            props.visibility = not is_visible

        row.operator_context = 'EXEC_DEFAULT'
        row.operator('text.jump', text=name,
                      icon_value=operator_selector[type][1].icon_id,
                      emboss=False).line=line + 1

        subrow = row.row(align=True)
        subrow.alignment = 'RIGHT'
        subrow.operator(operator_selector[type][0], text="",
                        icon='GHOST', emboss=False).line_index=line


        if is_visible:
            end_line = get_end_structure_line_index(current_text, line)
            methods = get_structure_methods(current_text, line, end_line)
            properties = get_properties(current_text, line, end_line)

            for p in sorted(properties):
                row = layout.row(align=True)
                row.alignment = 'LEFT'
                row.label(" " * 3)
                row.operator_context = 'EXEC_DEFAULT'
                row.operator('text.jump', text=p,
                             icon_value=class_function.icon_id,
                             emboss=False).line = properties[p] + 1
                row.operator('ide_like_tools.copy_operator_property_name',
                             text="", icon='GHOST',
                             emboss=False).line_index = properties[p]

            for m in methods['ORDER']:
                row = layout.row(align=True)
                row.alignment = 'LEFT'
                row.label(" "*3)
                row.operator_context = 'EXEC_DEFAULT'
                row.operator('text.jump', text=m,
                              icon_value=method_icon.icon_id,
                              emboss=False).line = methods[m] + 1
                row.operator('ide_like_tools.copy_function_name',
                               text="", icon='GHOST',
                               emboss=False).line_index=methods[m]


    def is_class_visible(self, name):
        return class_visibility[name]


class IDELikeToolsSetTreeVisibility(Operator):
    '''  '''
    bl_idname = 'ide_like_tools.set_tree_visible'
    bl_label = "Toggle Tree Visibility"
    bl_options = {'REGISTER'}

    class_name = StringProperty(
            name="Class Name",
            default="",
            )
    visibility = BoolProperty(
            name="Visibility",
            default=True,
            )

    def execute(self, context):
        global class_visibility
        class_visibility[self.class_name] = self.visibility
        return {'FINISHED'}