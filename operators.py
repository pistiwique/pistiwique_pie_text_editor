import bpy
from bpy.types import Operator


class CustomComment(Operator):
    bl_idname = "text.custom_comment"
    bl_label = "Custom comment"

    def execute(self, context):
        
        start_selection = bpy.context.space_data.text.current_character
        end_selection = bpy.context.space_data.text.select_end_character
        txt_name = bpy.context.space_data.text.name
        txt = bpy.data.texts[txt_name]
        line_begin = txt.current_line_index
        
        #select_end_line_index missing - iterate over txt.lines
        for line_end, line_obj in enumerate(txt.lines):
            if line_obj == txt.select_end_line:
                break

        selection = [i for i in range(line_begin, line_end)]       
               
        if line_begin != line_end:
            bpy.ops.text.comment()
 
        elif start_selection != end_selection:
            bpy.ops.text.cut()
            bpy.ops.text.insert(text="#")
            bpy.ops.text.paste()
                                        
        else:
            bpy.ops.text.select_line()
            bpy.ops.text.comment()                                            
                                           
        return {'FINISHED'}

    
class CustomUncomment(Operator):
    ''' Uncomment and delete space after the # '''
    bl_idname = "text.custom_uncomment"
    bl_label = "Custom uncomment"

    def execute(self, context):
        txt_name = bpy.context.space_data.text.name
        txt = bpy.data.texts[txt_name]
        line_begin = txt.current_line_index
        start_selection = bpy.context.space_data.text.current_character
        end_selection = bpy.context.space_data.text.select_end_character
        base = context.space_data.text.current_line.body 
        
        for line_end, line_obj in enumerate(txt.lines):
            if line_obj == txt.select_end_line:
                break

        selection = [i for i in range(line_begin, line_end)]  
              
        if line_begin != line_end:
            bpy.ops.text.uncomment() 
                             
        else:            
            uncommented_line = bpy.context.space_data.text.current_line.body.split("#")
            bpy.ops.text.select_line()
            bpy.ops.text.delete()
            bpy.ops.text.insert(text=''.join(uncommented_line))   
                          
        return {'FINISHED'}  

        
class CustomCopy(Operator):
    bl_idname = "text.custom_copy"
    bl_label = "Custom copy"
    
    def execute(self, context):
        select_loc = bpy.context.space_data.text.select_end_character
        cursor_loc = bpy.context.space_data.text.current_character
        txt_name = bpy.context.space_data.text.name
        txt = bpy.data.texts[txt_name]
        line_begin = txt.current_line_index

        for line_end, line_obj in enumerate(txt.lines):
            if line_obj == txt.select_end_line:
                break

        selection = [i for i in range(line_begin, line_end)] 
        
        if cursor_loc != select_loc or line_begin != line_end:
            bpy.ops.text.copy()
            
        else:
            base = context.space_data.text.current_line.body                       
            if "    " in base:
                bpy.ops.text.move(type='LINE_BEGIN')
                bpy.ops.text.move(type='NEXT_WORD')
                indent_value = bpy.context.space_data.text.select_end_character
                count_charactere = select_loc - indent_value
                for charactere in range(count_charactere):
                    bpy.ops.text.move_select(type='NEXT_CHARACTER')   
                             
            else:
                bpy.ops.text.move(type='LINE_BEGIN')
                for charactere in range(select_loc):
                    bpy.ops.text.move_select(type='NEXT_CHARACTER')
            bpy.ops.text.copy()      
        
        return {'FINISHED'}

    
class CustomCut(Operator):
    bl_idname = "text.custom_cut"
    bl_label = "Custom cut"
    
    def execute(self, context):
        select_loc = bpy.context.space_data.text.select_end_character
        cursor_loc = bpy.context.space_data.text.current_character
        txt_name = bpy.context.space_data.text.name
        txt = bpy.data.texts[txt_name]
        line_begin = txt.current_line_index

        for line_end, line_obj in enumerate(txt.lines):
            if line_obj == txt.select_end_line:
                break

        selection = [i for i in range(line_begin, line_end)] 
        
        if cursor_loc != select_loc or line_begin != line_end:
            bpy.ops.text.cut()
            
        else:
            base = context.space_data.text.current_line.body
            bpy.ops.text.select_line()                        
            if "    " in base:
                bpy.ops.text.move(type='LINE_BEGIN')
                bpy.ops.text.move(type='NEXT_WORD')
                indent_value = bpy.context.space_data.text.select_end_character
                count_charactere = select_loc - indent_value
                for charactere in range(count_charactere):
                    bpy.ops.text.move_select(type='NEXT_CHARACTER')
                               
            else:
                bpy.ops.text.move(type='LINE_BEGIN')
                for charactere in range(select_loc):
                    bpy.ops.text.move_select(type='NEXT_CHARACTER')
            bpy.ops.text.cut()
            
        return {'FINISHED'}


def run_custom_punctuation(self, context):
    bpy.ops.text.custom_punctuation('INVOKE_DEFAULT')
    

def custom_puncuation_function(punctuation):
    select_loc = bpy.context.space_data.text.select_end_character
    cursor_loc = bpy.context.space_data.text.current_character
    txt_name = bpy.context.space_data.text.name
    txt = bpy.data.texts[txt_name]
    line_begin = txt.current_line_index

    for line_end, line_obj in enumerate(txt.lines):
        if line_obj == txt.select_end_line:
            break

    selection = [i for i in range(line_begin, line_end)] 
    
    if cursor_loc != select_loc or line_begin != line_end:
        bpy.ops.text.cut()
        bpy.ops.text.insert(text=punctuation)
        bpy.ops.text.move(type='PREVIOUS_CHARACTER')
        bpy.ops.text.paste()                                
    else:   
        bpy.ops.text.insert(text=punctuation)
        bpy.ops.text.move(type='PREVIOUS_CHARACTER')
    
        
class CustomPunctuation(Operator):
    bl_idname = "text.custom_punctuation"
    bl_label = "Custom punctuation"
    
    def modal(self, context, event):
        wm = context.window_manager
        if wm.custom_punctuation_enabled:
            if context.space_data.type == 'TEXT_EDITOR':
                if event.unicode in ['(', '"', "'", '[', '{'] and event.value == 'PRESS':
                    select_loc = context.space_data.text.select_end_character
                    cursor_loc = context.space_data.text.current_character
                    line = context.space_data.text.current_line.body
                    
#                    if cursor_loc == select_loc and cursor_loc < len(line) and line[cursor_loc] not in "\n\t\r )]},.+-*/":
#                        return {'PASS_THROUGH'}
                    
                    if event.unicode == '"':
                        custom_puncuation_function('""')
                            
                    if event.unicode == "'":
                        custom_puncuation_function("''")
                            
                    if event.unicode == '(':
                        custom_puncuation_function("()")
                            
                    if event.unicode == "{":
                        custom_puncuation_function("{}")
                        
                    if event.unicode == "[":
                        custom_puncuation_function("[]")
                        
                    return {'RUNNING_MODAL'}
            
        else:
            return {'FINISHED'}
        
        return {'PASS_THROUGH'}
        
        
    def invoke(self, context, event):

        if context.area.type != 'TEXT_EDITOR':
            self.report({'WARNING'}, "Text Editor not found, cannot run operator")
            return {'CANCELLED'}
        context.window_manager.modal_handler_add(self)
        
        return {'RUNNING_MODAL'}       