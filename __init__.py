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

bl_info = {
    "name": "Pistiwique Pie Text Editor",
    "description": "",
    "author": "Legigan Jeremy AKA Pistiwique",
    "version": (0, 0, 1),
    "blender": (2, 7, 0),
    "location": "Text Editor",
    "category": "Development"
    }

import bpy
import sys
import importlib
import rna_keymap_ui

from bpy.types import AddonPreferences, Operator
from bpy.props import BoolProperty, EnumProperty
from . import developer_utils

importlib.reload(developer_utils)
modules = developer_utils.setup_addon_modules(__path__, __name__, "bpy" in locals())

KEYMAP_TOOLS = {
    "Toggle comment/uncomment": ['ide_like_tools.toggle_comment', None,
                                 'Text Generic', 'TEXT_EDITOR', 'WINDOW',
                                 'THREE', 'PRESS', False, False, True
                                 ],

    "Copy": ['ide_like_tools.copy', None, 'Text Generic', 'TEXT_EDITOR',
             'WINDOW', 'C', 'PRESS', True, False, False
             ],

    "Cut": ['ide_like_tools.cut', None, 'Text Generic', 'TEXT_EDITOR',
            'WINDOW', 'X', 'PRESS', True, False, False
            ],

    "Paste": ['ide_like_tools.paste', None, 'Text Generic', 'TEXT_EDITOR',
              'WINDOW', 'V', 'PRESS', True, False, False
              ],

    "Toggle console": ['wm.console_toggle', None, 'Text Generic',
                       'TEXT_EDITOR', 'WINDOW', 'F10', 'PRESS', False,
                       False, False
                       ],

    "Save Files": ['ide_like_tools.save_files', None, 'Text Generic',
                       'TEXT_EDITOR', 'WINDOW', 'S', 'PRESS', False,
                       False, True
                       ],

    "Pie Menu": ['wm.call_menu_pie', 'ide_like_tools.custom_text_editor',
                 'Text Generic', 'TEXT_EDITOR', 'WINDOW', 'RIGHTMOUSE',
                 'PRESS', False, False, False
                 ],
    }

KEYMAP_PUNCTUATION = {
    "Double quote \"\"":['ide_like_tools.double_quote', None,
                         'Text Generic', 'TEXT_EDITOR', 'WINDOW', 'THREE',
                         'PRESS', False, False,False
                         ],

    "Simple quote \'\'": ['ide_like_tools.simple_quote', None, 'Text Generic',
                          'TEXT_EDITOR', 'WINDOW', 'FOUR', 'PRESS', False,
                          False, False
                          ],

    "Bracket ()": ['ide_like_tools.bracket', None, 'Text Generic',
                   'TEXT_EDITOR', 'WINDOW', 'FIVE', 'PRESS', False, False,
                   False
                   ],

    "Square bracket []": ['ide_like_tools.square_bracket', None,
                          'Text Generic', 'TEXT_EDITOR', 'WINDOW', 'FIVE',
                          'PRESS', False, False, True
                          ],

    "Brace {}": ['ide_like_tools.brace', None, 'Text Generic', 'TEXT_EDITOR',
                 'WINDOW', 'FOUR', 'PRESS', False, False, True
                 ],
    }


class IDELikeToolsPreferences(AddonPreferences):
    bl_idname = __name__

    show_keymaps = BoolProperty(
            name="Keymaps",
            default=False,
            description="Display keymaps",
            )

    keymap_selector = EnumProperty(
            items=(('0', "Tools", ""),
                   ('1', "Punctuation", ""),
                   ),
            default='0',
            )

    def draw(self, context):
        wm = context.window_manager
        kc = wm.keyconfigs.user
        keymaps = [KEYMAP_TOOLS, KEYMAP_PUNCTUATION]
        layout = self.layout
        layout.prop(self, 'show_keymaps', toggle=True)
        if self.show_keymaps:
            row = layout.row(align=True)
            row.prop(self, 'keymap_selector', expand=True)
            for name, items in keymaps[int(self.keymap_selector)].items():
                if name == "Toggle console" and sys.platform != "win32":
                    pass

                else:
                    kmi_name, kmi_value, km_name = items[:3]
                    box = layout.box()
                    split = box.split()
                    col = split.column()
                    col.label(name)
                    col.separator()
                    km = kc.keymaps[km_name]
                    kmi = get_hotkey_entry_item(km, kmi_name, kmi_value)
                    if kmi:
                        col.context_pointer_set('keymap', km)
                        rna_keymap_ui.draw_kmi([], kc, km, kmi, col, 0)
                    else:
                        col.label("No hotkey entry found")
                        col.operator(IDELIKETOOLS_OT_AddHotkey.bl_idname, icon='ZOOMIN')


addon_keymaps = []

def get_hotkey_entry_item(km, kmi_name, kmi_value):

    for i, km_item in enumerate(km.keymap_items):
        if km.keymap_items.keys()[i] == kmi_name:
            if kmi_value:
                if km.keymap_items[i].properties.name == kmi_value:
                    return km_item
            return km_item

    return None


def add_hotkey():

    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if not kc:
        return

    for keymap in [KEYMAP_TOOLS, KEYMAP_PUNCTUATION]:
        for items in keymap.values():
            kmi_name, kmi_value, km_name, space_type, region_type = items[:5]
            eventType, eventValue, ctrl, shift, alt = items[5:]
            km = kc.keymaps.new(name=km_name, space_type=space_type,
                                region_type=region_type
                                )

            kmi = km.keymap_items.new(kmi_name, eventType,
                                      eventValue, ctrl=ctrl, shift=shift, alt=alt
                                      )

            if kmi_value:
                kmi.properties.name = kmi_value

            kmi.active = True

    addon_keymaps.append((km, kmi))

class IDELIKETOOLS_OT_AddHotkey(Operator):
    ''' Add hotkey entry '''

    bl_idname = "ide_like_tools.add_hotkey"
    bl_label = "Add hotckey"
    bl_options = {'REGISTER', 'INTERNAL'}

    def execute(self, context):
        add_hotkey()

        self.report({'INFO'},
                    "Hotkey added in User Preferences -> Input -> Screen -> Screen (Global)")
        return {'FINISHED'}


def remove_hotkey():
    ''' clears addon keymap hotkeys stored in addon_keymaps '''

    # kmi_values = [item[1] for item in KEYMAPS_DICT.values() if item]
    #
    # kmi_names = [item[0] for item in KEYMAPS_DICT.values() if item not in ['wm.call_menu', 'wm.call_menu_pie']]

    kmi_values = []
    kmi_names = []

    for keymap in [KEYMAP_TOOLS, KEYMAP_PUNCTUATION]:
        for item in keymap.values():
            if item[0] not in ['wm.call_menu', 'wm.call_menu_pie']:
                kmi_names.append(item[0])

            else:
                if item[1]:
                    kmi_values.append(item[1])


    for km, kmi in addon_keymaps:
        # remove addon keymap for menu and pie menu
        if hasattr(kmi.properties, 'name'):
            if kmi_values:
                if kmi.properties.name in kmi_values:
                    km.keymap_items.remove(kmi)

        # remove addon_keymap for operators
        else:
            if kmi_names:
                if kmi.name in kmi_names:
                    km.keymap_items.remove(kmi)

    addon_keymaps.clear()

# register

def register():
    bpy.utils.register_module(__name__)
    add_hotkey()


def unregister():
    remove_hotkey()

    bpy.utils.unregister_module(__name__)