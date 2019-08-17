'''
Copyright (C) 2015 Legigan Jeremy AKA Pistiwique
 
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
import bpy.utils.previews
from os.path import join, dirname
 
ide_like_tools_collections = {}
ide_like_tools_icons_loaded = False
 
def load_icons():
    global ide_like_tools_collections
    global ide_like_tools_icons_loaded
 
    if ide_like_tools_icons_loaded: return ide_like_tools_collections["main"]
 
    custom_icons = bpy.utils.previews.new()
 
    icons_dir = join(dirname(__file__))
 
    custom_icons.load("class_icon", join(icons_dir, "class.png"), 'IMAGE')
    custom_icons.load("function_icon", join(icons_dir, "function.png"),
                      'IMAGE')
    custom_icons.load("method_icon", join(icons_dir, "method.png"), 'IMAGE')
    custom_icons.load("variable_icon", join(icons_dir, "variable.png"),
                      'IMAGE')
    custom_icons.load("class_function_icon", join(icons_dir,
                      "class_function.png"), 'IMAGE')


    ide_like_tools_collections["main"] = custom_icons
    ide_like_tools_icons_loaded = True
 
    return ide_like_tools_collections["main"]
 
def clear_icons():
    global ide_like_tools_icons_loaded
    for icon in ide_like_tools_collections.values():
        bpy.utils.previews.remove(icon)
        ide_like_tools_collections.clear()
    ide_like_tools_icons_loaded = False
