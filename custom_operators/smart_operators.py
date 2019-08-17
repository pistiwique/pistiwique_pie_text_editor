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


import sys
import re
import webbrowser

from bpy.types import Operator
from .utils import *


API_SEARCH = 'https://docs.blender.org/api/current/search.html?q' \
             '=%s&check_keywords=yes&area=default'
API_BROWSER = 'https://docs.blender.org/api/current/'

class IDELikeToolsComment(Operator):
    ''' Custom smart comment '''

    bl_idname = "ide_like_tools.comment"
    bl_label = "Comment"

    def execute(self, context):

        current_text = get_current_text()
        start_selection, end_selection = get_selection(current_text)
        line_begin, line_end = get_lines_selection(current_text)
        if line_begin > line_end:
            line_begin, line_end = remap_line_index(line_begin, line_end)
        if start_selection > end_selection:
            start_selection, end_selection = remap_selection(start_selection, end_selection)

        clean_end_lines(current_text, line_begin, line_end)

        if line_begin != line_end:
            bpy.ops.text.comment()
            bpy.ops.text.move(type='LINE_END')

        elif start_selection != end_selection:
            current_line = current_text.current_line.body
            current_text.current_line.body = "%s#%s" % (current_line[:start_selection], current_line[start_selection:])
            bpy.ops.text.move(type='LINE_END')

        else:
            bpy.ops.text.select_line()
            bpy.ops.text.comment()
            bpy.ops.text.move(type='LINE_END')

        return {'FINISHED'}


class IDELikeToolsUncomment(Operator):
    ''' Custom smart uncomment '''

    bl_idname = "ide_like_tools.uncomment"
    bl_label = "Uncomment"

    def execute(self, context):

        current_text = get_current_text()
        line_begin, line_end = get_lines_selection(current_text)
        if line_begin > line_end:
            line_begin, line_end = remap_line_index(line_begin, line_end)

        clean_end_lines(current_text, line_begin, line_end)

        if line_begin != line_end:
            bpy.ops.text.uncomment()

        else:
            base = current_text.current_line.body
            uncommented_line = base.replace("#", "")
            current_text.current_line.body = uncommented_line
            bpy.ops.text.move(type='LINE_END')

        return {'FINISHED'}


class IDELikeToolsCommentToggle(Operator):
    '''  '''
    bl_idname = 'ide_like_tools.toggle_comment'
    bl_label = "Comment / Uncomment"
    bl_options = {'REGISTER'}

    def execute(self, context):

        if "#" in context.space_data.text.current_line.body:
            bpy.ops.ide_like_tools.uncomment()

        else:
            bpy.ops.ide_like_tools.comment()

        return {'FINISHED'}


class IDELikeToolsCopy(Operator):
    ''' Custom smart copy '''

    bl_idname = "ide_like_tools.copy"
    bl_label = "Copy"

    def execute(self, context):

        current_text = get_current_text()
        start_selection, end_selection = get_selection(current_text)
        line_begin, line_end = get_lines_selection(current_text)
        if line_begin > line_end:
            line_begin, line_end = remap_line_index(line_begin, line_end)
        if start_selection > end_selection:
            start_selection, end_selection = remap_selection(start_selection, end_selection)

        if line_begin != line_end:
            bpy.context.window_manager.clipboard = ""
            for idx in range(line_begin, line_end + 1):
                text = current_text.lines[idx].body
                bpy.context.window_manager.clipboard += text + "\n"

        elif start_selection != end_selection:
            bpy.ops.text.copy()
            bpy.ops.text.move(type='NEXT_CHARACTER')

        else:
            base = current_text.current_line.body
            end_copy = current_text.current_character
            bpy.context.window_manager.clipboard = base[:end_copy].strip()

        return {'FINISHED'}


class IDELikeToolsCut(Operator):
    ''' Custom smart cut '''

    bl_idname = "ide_like_tools.cut"
    bl_label = "Cut"

    def execute(self, context):

        current_text = get_current_text()
        start_selection, end_selection = get_selection(current_text)
        line_begin, line_end = get_lines_selection(current_text)
        if line_begin > line_end:
            line_begin, line_end = remap_line_index(line_begin, line_end)
        if start_selection > end_selection:
            start_selection, end_selection = remap_selection(start_selection, end_selection)

        clean_end_lines(current_text, line_begin, line_end)

        bpy.context.window_manager.clipboard = ""

        if line_begin != line_end:
            for idx in range(line_begin, line_end + 1):
                text = current_text.lines[idx].body
                bpy.context.window_manager.clipboard += text + "\n"

            if current_text.current_line_index == line_end:
                bpy.ops.text.move(type='LINE_END')
                while current_text.current_line_index != line_end:
                    bpy.ops.text.move(type='NEXT_LINE')

            bpy.ops.text.move(type='LINE_END')
            for i in range(line_end - line_begin + 1):
                bpy.ops.text.select_line()
                bpy.ops.text.delete()
                current_line = current_text.current_line.body
                if not re.search("\W", current_line):
                    bpy.ops.text.delete()
                bpy.ops.text.move(type='PREVIOUS_LINE')
                bpy.ops.text.move(type='LINE_END')

            bpy.ops.text.move(type='NEXT_LINE')
            bpy.ops.text.move(type='LINE_BEGIN')


        elif start_selection != end_selection:
            bpy.ops.text.cut()

        else:
            base = current_text.current_line.body
            end_copy = current_text.current_character
            bpy.context.window_manager.clipboard = base[:end_copy].strip()
            current_text.current_line.body = base[end_copy:]
            bpy.ops.text.move(type='LINE_BEGIN')

        return {'FINISHED'}


class IDELikeToolsPaste(Operator):
    ''' Custom smart paste '''
    bl_idname = 'ide_like_tools.paste'
    bl_label = "Paste"
    bl_options = {'REGISTER'}

    def execute(self, context):
        current_text = get_current_text()
        tab_width = context.space_data.tab_width
        line_begin, line_end = get_lines_selection(current_text)
        start_selection, end_selection = get_selection(current_text)
        TAB = "    "

        if len(context.window_manager.clipboard.split("\n")) > 1:
            if line_begin > line_end:
                start_selection = end_selection

            main_tab = start_selection//tab_width
            min_line_tab = 0

            tabs = [line.count(TAB) for line in
                             context.window_manager.clipboard.split("\n")[:-1]
                             if line]

            if tabs:
                min_line_tab = min(tabs)

            lines = [l for l in context.window_manager.clipboard.split("\n")]

            bpy.ops.text.delete()
            bpy.ops.text.move(type='LINE_BEGIN')

            for line in lines:
                bpy.ops.text.insert(text=TAB*main_tab + line[min_line_tab * 4:] + "\n")

            current_text.current_line.body =\
                current_text.current_line.body[4*main_tab:]
      
        else:
            bpy.ops.text.paste()

        return {'FINISHED'}


class IDELikeToolsConsoleToggle(Operator):
    ''' Console toggle. Only for windows '''
    bl_idname = 'ide_like_tools.toggle_console'
    bl_label = "Toggle Console"
    bl_options = {'REGISTER'}

    @classmethod
    def poll(cls, context):
        return sys.platform == "win32"

    def execute(self, context):

        bpy.ops.wm.console_toggle()

        return {'FINISHED'}


class IDELikeToolsAPISearch(Operator):
    '''  '''
    bl_idname = 'ide_like_tools.api_search'
    bl_label = "API Search"
    bl_options = {'REGISTER'}

    test = bpy.props.BoolProperty()

    def execute(self, context):
        current_text = get_current_text()
        line_begin, line_end = get_lines_selection(current_text)
        if line_begin == line_end:
            start_selection, end_selection = get_selection(current_text)
            if start_selection > end_selection:
                start_selection, end_selection = remap_selection(start_selection,
                                                             end_selection)

            research = current_text.current_line.body[start_selection:end_selection]
            research = research.strip().rstrip()

            if not " " in research and re.search("\w", research):
                webbrowser.open(API_SEARCH %research)

            else:
                webbrowser.open(API_BROWSER)

        else:
            webbrowser.open(API_BROWSER)

        return {'FINISHED'}


class IDELikeToolsSaveFiles(Operator):
    bl_idname = "ide_like_tools.save_files"
    bl_label = "Save All Files"
    bl_description = "Save all files which correspond to a file on the hard drive"
    bl_options = {"REGISTER"}

    def execute(self, context):
        for text in bpy.data.texts:
            save_text_block(text)
        try: bpy.ops.text.resolve_conflict(resolution = "IGNORE")
        except: pass
        return {'FINISHED'}


class IDELikeToolsRestartBlender(Operator):
    '''  '''
    bl_idname = 'ide_like_tools.restart_blender'
    bl_label = "Restart Blender"
    bl_options = {'REGISTER'}

    # only works for windows currently
    def open_file(self, path):
        if sys.platform == "win32":
            os.startfile(path)
        else:
            opener = "open" if sys.platform == "darwin" else "xdg-open"
            subprocess.call([opener, path])

    def start_another_blender_instance(self):
        self.open_file(bpy.app.binary_path)

    def execute(self, context):
        self.start_another_blender_instance()

        bpy.ops.wm.quit_blender()
        return {'FINISHED'}


class PrintTest(Operator):
    '''  '''
    bl_idname = 'text.debug'
    bl_label = "DEBUG"
    bl_options = {'REGISTER'}

    addon_key = __package__.split(".")[0]

    def execute(self, context):
        print(self.addon_key)
        return {'FINISHED'}