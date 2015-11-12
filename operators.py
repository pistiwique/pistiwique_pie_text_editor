import bpy
from bpy.types import Operator


class customComment(Operator):
    bl_idname = "text.custom_comment"
    bl_label = "Custom comment"

    def execute(self, context):
        
        start_selection = bpy.context.space_data.text.current_character
        end_selection = bpy.context.space_data.text.select_end_character
        txt_name = bpy.context.space_data.text.name
        txt = bpy.data.texts[txt_name]
        line_begin = txt.current_line_index

        for line_end, line_obj in enumerate(txt.lines):
            if line_obj == txt.select_end_line:
                break

        selection = [i for i in range(line_begin + 1, line_end + 2)]       
               
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

    
class customUncomment(Operator):
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

        #select_end_line_index missing - iterate over txt.lines
        for line_end, line_obj in enumerate(txt.lines):
            if line_obj == txt.select_end_line:
                break

        selection = [i for i in range(line_begin + 1, line_end + 2)]  
              
        if line_begin != line_end:
            bpy.ops.text.uncomment() 
                             
        else:            
            uncommented_line = bpy.context.space_data.text.current_line.body.split("#")
            bpy.ops.text.select_line()
            bpy.ops.text.delete()
            bpy.ops.text.insert(text=''.join(uncommented_line))   
                          
        return {'FINISHED'}  

        
class customCopy(Operator):
    bl_idname = "text.custom_copy"
    bl_label = "Custom copy"
    
    def execute(self, context):
        
        start_selection = bpy.context.space_data.text.current_character
        end_selection = bpy.context.space_data.text.select_end_character                
        if start_selection != end_selection:
            bpy.ops.text.copy()
            
        else:
            base = context.space_data.text.current_line.body                       
            if "    " in base:
                bpy.ops.text.move(type='LINE_BEGIN')
                bpy.ops.text.move(type='NEXT_WORD')
                indent_value = bpy.context.space_data.text.select_end_character
                count_charactere = end_selection - indent_value
                for charactere in range(count_charactere):
                    bpy.ops.text.move_select(type='NEXT_CHARACTER')   
                             
            else:
                bpy.ops.text.move(type='LINE_BEGIN')
                for charactere in range(end_selection):
                    bpy.ops.text.move_select(type='NEXT_CHARACTER')
            bpy.ops.text.copy()      
        
        return {'FINISHED'}

    
class customCut(Operator):
    bl_idname = "text.custom_cut"
    bl_label = "Custom cut"
    
    def execute(self, context):

        start_selection = bpy.context.space_data.text.current_character
        end_selection = bpy.context.space_data.text.select_end_character                
        if start_selection != end_selection:
            bpy.ops.text.cut()
            
        else:
            base = context.space_data.text.current_line.body
            bpy.ops.text.select_line()                        
            if "    " in base:
                bpy.ops.text.move(type='LINE_BEGIN')
                bpy.ops.text.move(type='NEXT_WORD')
                indent_value = bpy.context.space_data.text.select_end_character
                count_charactere = end_selection - indent_value
                for charactere in range(count_charactere):
                    bpy.ops.text.move_select(type='NEXT_CHARACTER')
                               
            else:
                bpy.ops.text.move(type='LINE_BEGIN')
                for charactere in range(end_selection):
                    bpy.ops.text.move_select(type='NEXT_CHARACTER')
            bpy.ops.text.cut()
            
        return {'FINISHED'}

    
class customInvertedComma(Operator):
    bl_idname = "text.custom_inverted_comma"
    bl_label = "Custom Inverted Comma"
    
    def execute(self, context):
        start_selection = bpy.context.space_data.text.current_character
        end_selection = bpy.context.space_data.text.select_end_character
        txt_name = bpy.context.space_data.text.name
        txt = bpy.data.texts[txt_name]
        line_begin = txt.current_line_index

        for line_end, line_obj in enumerate(txt.lines):
            if line_obj == txt.select_end_line:
                break

        selection = [i for i in range(line_begin + 1, line_end + 2)]        
               
        if start_selection != end_selection or len(selection) > 1:
            bpy.ops.text.cut()
            bpy.ops.text.insert(text='""')
            bpy.ops.text.move(type='PREVIOUS_CHARACTER')
            bpy.ops.text.paste()
                
        else:   
            bpy.ops.text.insert(text='""')
            bpy.ops.text.move(type='PREVIOUS_CHARACTER')
        
        return {'FINISHED'}


class customApostrophe(Operator):
    bl_idname = "text.custom_apostrophe"
    bl_label = "Custom Apostrophe"
   
    def execute(self, context):
        start_selection = bpy.context.space_data.text.current_character
        end_selection = bpy.context.space_data.text.select_end_character
        txt_name = bpy.context.space_data.text.name
        txt = bpy.data.texts[txt_name]
        line_begin = txt.current_line_index

        for line_end, line_obj in enumerate(txt.lines):
            if line_obj == txt.select_end_line:
                break

        selection = [i for i in range(line_begin + 1, line_end + 2)]        
               
        if start_selection != end_selection or len(selection) > 1:
            bpy.ops.text.cut()
            bpy.ops.text.insert(text="''")
            bpy.ops.text.move(type='PREVIOUS_CHARACTER')
            bpy.ops.text.paste()
                
        else:   
            bpy.ops.text.insert(text="''")
            bpy.ops.text.move(type='PREVIOUS_CHARACTER')
        
        return {'FINISHED'}


class customBracket(Operator):
    bl_idname = "text.custom_bracket"
    bl_label = "Custom Bracket"
    
    def execute(self, context):
        start_selection = bpy.context.space_data.text.current_character
        end_selection = bpy.context.space_data.text.select_end_character
        txt_name = bpy.context.space_data.text.name
        txt = bpy.data.texts[txt_name]
        line_begin = txt.current_line_index

        for line_end, line_obj in enumerate(txt.lines):
            if line_obj == txt.select_end_line:
                break

        selection = [i for i in range(line_begin + 1, line_end + 2)]        
               
        if start_selection != end_selection or len(selection) > 1:
            bpy.ops.text.cut()
            bpy.ops.text.insert(text="()")
            bpy.ops.text.move(type='PREVIOUS_CHARACTER')
            bpy.ops.text.paste()
                
        else:   
            bpy.ops.text.insert(text="()")
            bpy.ops.text.move(type='PREVIOUS_CHARACTER')
        
        return {'FINISHED'}        
    

class customBrace(Operator):
    bl_idname = "text.custom_brace"
    bl_label = "Custom Brace"
    
    def execute(self, context):
        start_selection = bpy.context.space_data.text.current_character
        end_selection = bpy.context.space_data.text.select_end_character
        txt_name = bpy.context.space_data.text.name
        txt = bpy.data.texts[txt_name]
        line_begin = txt.current_line_index

        for line_end, line_obj in enumerate(txt.lines):
            if line_obj == txt.select_end_line:
                break

        selection = [i for i in range(line_begin + 1, line_end + 2)]        
               
        if start_selection != end_selection or len(selection) > 1:
            bpy.ops.text.cut()
            bpy.ops.text.insert(text="{}")
            bpy.ops.text.move(type='PREVIOUS_CHARACTER')
            bpy.ops.text.paste()
                
        else:   
            bpy.ops.text.insert(text="{}")
            bpy.ops.text.move(type='PREVIOUS_CHARACTER')
        
        return {'FINISHED'}
    
    
class customSquareBracket(Operator):
    bl_idname = "text.custom_square_bracket"
    bl_label = "Custom Square Bracket"
    
    def execute(self, context):
        start_selection = bpy.context.space_data.text.current_character
        end_selection = bpy.context.space_data.text.select_end_character
        txt_name = bpy.context.space_data.text.name
        txt = bpy.data.texts[txt_name]
        line_begin = txt.current_line_index

        for line_end, line_obj in enumerate(txt.lines):
            if line_obj == txt.select_end_line:
                break

        selection = [i for i in range(line_begin + 1, line_end + 2)]        
               
        if start_selection != end_selection or len(selection) > 1:
            bpy.ops.text.cut()
            bpy.ops.text.insert(text="[]")
            bpy.ops.text.move(type='PREVIOUS_CHARACTER')
            bpy.ops.text.paste()
                
        else:   
            bpy.ops.text.insert(text="[]")
            bpy.ops.text.move(type='PREVIOUS_CHARACTER')
        
        return {'FINISHED'}