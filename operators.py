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
        
       # select_end_line_index missing - iterate over txt.lines
        for line_end, line_obj in enumerate(txt.lines):
            if line_obj == txt.select_end_line:
                break

        selection = [i for i in range(line_begin, line_end)]    
               
        if line_begin != line_end:
            bpy.ops.text.comment()
            bpy.ops.text.move(type='NEXT_CHARACTER')
 
        elif start_selection != end_selection:            
            bpy.ops.text.cut()
            bpy.ops.text.insert(text="#")
            bpy.ops.text.paste()
            bpy.ops.text.move(type='NEXT_CHARACTER')

        else:
            bpy.ops.text.select_line()
            bpy.ops.text.comment()
            bpy.ops.text.move(type='NEXT_CHARACTER')

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
            bpy.ops.text.move(type='NEXT_CHARACTER')            

        else:                        
            base = context.space_data.text.current_line.body
            end_copy = context.space_data.text.current_character
            copy_text = base[:end_copy].split("    ")[-1]
            bpy.context.window_manager.clipboard = copy_text                        
            
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
    

def custom_punctuation_function(punctuation):
    base = bpy.context.space_data.text.current_line.body
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
        bpy.ops.text.move(type='NEXT_CHARACTER')                                
    else:
        if punctuation == '"'*2 and cursor_loc < len(base) and base[cursor_loc] == '"':
            bpy.ops.text.insert(text='"')
            
        elif punctuation == "'"*2 and cursor_loc < len(base) and base[cursor_loc] == "'":
            bpy.ops.text.insert(text="'")
            
        else:  
            bpy.ops.text.insert(text=punctuation)
            bpy.ops.text.move(type='PREVIOUS_CHARACTER')

    
class CustomDoubleQuote(Operator):
    bl_idname = "text.custom_double_quote"
    bl_label = "Double quote"
    
    def execute(self, context):

        custom_punctuation_function('"'*2)
   
        return {'FINISHED'}


class CustomSimpleQuote(Operator):
    bl_idname = "text.custom_simple_quote"
    bl_label = "Simple quote"

    def execute(self, context):

        custom_punctuation_function("''")
        
        return {'FINISHED'}
    
    
class CustomBracket(Operator):
    bl_idname = "text.custom_bracket"
    bl_label = "Bracket"
    
    def execute(self, context):
        custom_punctuation_function("()")
        
        return {'FINISHED'}


class CustomSquareBracket(Operator):
    bl_idname = "text.custom_square_bracket"
    bl_label = "Square bracket"
    
    def execute(self, context):
        custom_punctuation_function("[]")
        
        return {'FINISHED'}


class CustomBrace(Operator):
    bl_idname = "text.custom_brace"
    bl_label = "Brace"
    
    def execute(self, context):
        custom_punctuation_function("{}")
        
        return {'FINISHED'}
        