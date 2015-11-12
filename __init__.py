'''
Copyright (C) 2015 Pistiwique
YOUR@MAIL.com

Created by Pistiwique

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
    "name": "Pistiwique_pie_text_editor",
    "description": "",
    "author": "Pistiwique",
    "version": (0, 1, 0),
    "blender": (2, 74, 0),
    "location": "View3D",
    "wiki_url": "",
    "category": "Text Editor" }
    
    
import bpy      
from . pie_utils import initPieTextEditor, initPieTextPlus
from . operators import *


addon_keymaps = []

def register_keymaps():
    global addon_keymaps    
    wm = bpy.context.window_manager
    
    km = wm.keyconfigs.addon.keymaps.new(name="Text Generic", space_type='TEXT_EDITOR')
    kmi = km.keymap_items.new(initPieTextEditor.bl_idname, 'RIGHTMOUSE', 'PRESS')
    kmi = km.keymap_items.new(initPieTextPlus.bl_idname, 'RIGHTMOUSE', 'PRESS', shift=True)
    kmi = km.keymap_items.new("text.custom_inverted_comma", 'THREE', 'PRESS')
    kmi = km.keymap_items.new("text.custom_apostrophe", 'FOUR', 'PRESS')
    kmi = km.keymap_items.new("text.custom_bracket", 'FIVE', 'PRESS')
    kmi = km.keymap_items.new("text.custom_brace", 'FOUR', 'PRESS', alt=True)
    kmi = km.keymap_items.new("text.custom_square_bracket", 'FIVE', 'PRESS', alt=True)

    addon_keymaps.append(km)

def unregister_keymaps():

    wm = bpy.context.window_manager
    for km in addon_keymaps:
        for kmi in km.keymap_items:
            km.keymap_items.remove(kmi)
        wm.keyconfigs.addon.keymaps.remove(km)
    addon_keymaps.clear()
    

def register():
    bpy.utils.register_module(__name__)
    register_keymaps()


def unregister():
    bpy.utils.unregister_module(__name__)
    unregister_keymaps()