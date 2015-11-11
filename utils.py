import bpy
from bpy.types import Operator

custom_class_list = []
custom_fonction_list = []

class initPieTextPlus(Operator):
    bl_idname = "text.init_pie_text_plus"
    bl_label = "Pie text plus"
    
    def execute(self, context):
        bpy.ops.wm.call_menu_pie(name='pie.text_plus')
        
        return {'FINISHED'}
    
    
class initPieTextEditor(Operator): # a way to avoid restricted context  
    bl_idname = "text.init_pie_text_editor"
    bl_label = "Pie text editor"

    launch_count = 0

    def execute(self, context):
        if self.launch_count == 0:
            bpy.types.Scene.lapineigeTools_tmp_text = bpy.props.EnumProperty(items = [(txt.name,txt.name,'','',bpy.data.texts.find(txt.name)) for txt in bpy.data.texts], update=changeText)                         
              
        bpy.ops.wm.call_menu_pie(name='pie.text_editor')
        
        return {'FINISHED'}                        

            
class InitJumpToClass(Operator):
    bl_idname = "text.init_jump_to_class"
    bl_label = "Init jump to class"
    
    def execute(self, context):  
        del(custom_class_list[:])      
        txt = bpy.context.space_data.text.name  
        text = bpy.data.texts[txt] 
        line_count = [line for line in text.lines] 
        current_line = bpy.context.space_data.text.current_line_index
        for i in range(len(line_count)):    
            bpy.context.space_data.text.current_line_index = i
            base = bpy.context.space_data.text.current_line.body
            if "class " == base[:6]:
                custom_class_list.append((base.split("(")[0], bpy.context.space_data.text.current_line_index))

        bpy.context.space_data.text.current_line_index = current_line
                    
        bpy.ops.wm.call_menu(name="text.jump_class_menu")
        
        return {'FINISHED'}


class JumpToClass(Operator):
    bl_idname = "text.jump_to_class"
    bl_label = "Jump to class"
    
    class_index = bpy.props.StringProperty(default="") 
    
    def execute(self, context):
        bpy.ops.text.jump(line=int(self.class_index)+1)
        
        return {'FINISHED'}
    
                
class JumpClassMenu(bpy.types.Menu):
    bl_idname = "text.jump_class_menu"
    bl_label = "Jump to class"    

    def draw(self, context):
        layout = self.layout      
        for item in custom_class_list:
            op = layout.operator("text.jump_to_class", text=item[0])
            op.class_index = str(item[1])
            

class InitJumpToFonction(Operator):
    bl_idname = "text.init_jump_to_fonction"
    bl_label = "Init jump to fonction"
    
    def execute(self, context):  
        del(custom_fonction_list[:])      
        txt = bpy.context.space_data.text.name  
        text = bpy.data.texts[txt] 
        line_count = [line for line in text.lines] 
        current_line = bpy.context.space_data.text.current_line_index
        for i in range(len(line_count)):    
            bpy.context.space_data.text.current_line_index = i
            base = bpy.context.space_data.text.current_line.body
            if "def " == base[:4]:
                custom_fonction_list.append((base.split("(")[0], bpy.context.space_data.text.current_line_index))

        bpy.context.space_data.text.current_line_index = current_line
                    
        bpy.ops.wm.call_menu(name="text.jump_fonction_menu")
        
        return {'FINISHED'}


class JumpToFonction(Operator):
    bl_idname = "text.jump_to_fonction"
    bl_label = "Jump to fontion"
    
    fonction_index = bpy.props.StringProperty(default="") 
    
    def execute(self, context):
        bpy.ops.text.jump(line=int(self.fonction_index)+1)
        
        return {'FINISHED'}
    
                
class JumpFonctionMenu(bpy.types.Menu):
    bl_idname = "text.jump_fonction_menu"
    bl_label = "Jump to fonction"    

    def draw(self, context):
        layout = self.layout     
        for item in custom_fonction_list:
            op = layout.operator("text.jump_to_fonction", text=item[0])
            op.fonction_index = str(item[1])
                
                    
def changeText(self,context):
    bpy.context.space_data.text = bpy.data.texts[bpy.context.scene.lapineigeTools_tmp_text]

    
class textsList(bpy.types.Menu):
    bl_idname = "text.text_list_menu"
    bl_label = "Texts List"    

    def draw(self, context):
        layout = self.layout
        layout.props_enum(context.scene,'lapineigeTools_tmp_text')

    
class customComment(Operator):
    ''' Auto comment with a space after # '''
    bl_idname = "text.custom_comment"
    bl_label = "Custom comment"

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
        if len(selection) > 1:
            for line in selection:               
                bpy.context.space_data.text.current_line_index = line-1    
                base = context.space_data.text.current_line.body                   
                if "    " in base[:5]:
                    bpy.ops.text.move(type='LINE_BEGIN')
                    bpy.ops.text.move(type='NEXT_WORD')        
                    bpy.ops.text.insert(text="# ")
                    
                else:
                    bpy.ops.text.move(type='LINE_BEGIN')        
                    bpy.ops.text.insert(text="# ") 
        
        elif start_selection != end_selection:
            bpy.ops.text.move(type='LINE_BEGIN')
            if "    " in base[:5]:
                bpy.ops.text.move(type='NEXT_WORD')
                new_start = start_selection - bpy.context.space_data.text.select_end_character
                for charactere in range(new_start):   
                    bpy.ops.text.move(type='NEXT_CHARACTER')
                bpy.ops.text.insert(text='# ')

            else:    
                for charactere in range(start_selection):   
                    bpy.ops.text.move(type='NEXT_CHARACTER')
                bpy.ops.text.insert(text='# ')
               
        else:                                  
            if "    " in base[:5]:
                bpy.ops.text.move(type='LINE_BEGIN')
                bpy.ops.text.move(type='NEXT_WORD')        
                bpy.ops.text.insert(text="# ")
                
            else:
                bpy.ops.text.move(type='LINE_BEGIN')        
                bpy.ops.text.insert(text="# ")  
                                           
        return {'FINISHED'}

    
class customUncomment(Operator):
    ''' Uncomment and delete space after the # '''
    bl_idname = "text.custom_uncomment"
    bl_label = "Custom uncomment"

    def execute(self, context):
        txt_name = bpy.context.space_data.text.name
        txt = bpy.data.texts[txt_name]
        line_begin = txt.current_line_index
        base = context.space_data.text.current_line.body 

        #select_end_line_index missing - iterate over txt.lines
        for line_end, line_obj in enumerate(txt.lines):
            if line_obj == txt.select_end_line:
                break

        selection = [i for i in range(line_begin + 1, line_end + 2)]        
        if len(selection) > 1:
            for line in selection:
                bpy.context.space_data.text.current_line_index = line-1   
                base = context.space_data.text.current_line.body                   
                if "    " in base[:5]:
                    bpy.ops.text.move(type='LINE_BEGIN')
                    bpy.ops.text.move(type='NEXT_WORD')
                    bpy.ops.text.move_select(type='NEXT_CHARACTER')
                    bpy.ops.text.move_select(type='NEXT_CHARACTER')
                    bpy.ops.text.delete()
                    
                else:
                    bpy.ops.text.move(type='LINE_BEGIN')
                    bpy.ops.text.move_select(type='NEXT_CHARACTER')
                    bpy.ops.text.move_select(type='NEXT_CHARACTER')
                    bpy.ops.text.delete() 
            
        else:                                    
            if "    " in base[:5]:
                bpy.ops.text.move(type='LINE_BEGIN')
                bpy.ops.text.move(type='NEXT_WORD')
                bpy.ops.text.move_select(type='NEXT_CHARACTER')
                bpy.ops.text.move_select(type='NEXT_CHARACTER')
                bpy.ops.text.delete()
                
            else:
                bpy.ops.text.move(type='LINE_BEGIN')
                bpy.ops.text.move_select(type='NEXT_CHARACTER')
                bpy.ops.text.move_select(type='NEXT_CHARACTER')
                bpy.ops.text.delete()  
                          
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
        base = bpy.context.space_data.text.current_line.body
        start_selection = bpy.context.space_data.text.current_character
        end_selection = bpy.context.space_data.text.select_end_character        
     
        if start_selection < end_selection:
            selection = end_selection - start_selection
            bpy.ops.text.move(type='LINE_BEGIN')            
            if "    " in base[:5]:
                bpy.ops.text.move(type='NEXT_WORD')
                new_start = start_selection - bpy.context.space_data.text.select_end_character
                for charactere in range(new_start):   
                    bpy.ops.text.move(type='NEXT_CHARACTER')
                bpy.ops.text.insert(text='"')
                for charactere in range(selection):
                    bpy.ops.text.move(type='NEXT_CHARACTER')
                bpy.ops.text.insert(text='"')

            else:    
                for charactere in range(start_selection):   
                    bpy.ops.text.move(type='NEXT_CHARACTER')
                bpy.ops.text.insert(text='"')
                for charactere in range(selection):
                    bpy.ops.text.move(type='NEXT_CHARACTER')
                bpy.ops.text.insert(text='"')
                
        elif start_selection > end_selection:
            selection = start_selection - end_selection
            bpy.ops.text.move(type='LINE_BEGIN')            
            if "    " in base[:5]:
                bpy.ops.text.move(type='NEXT_WORD')
                new_start = end_selection - bpy.context.space_data.text.select_end_character
                for charactere in range(new_start):   
                    bpy.ops.text.move(type='NEXT_CHARACTER')
                bpy.ops.text.insert(text='"')
                for charactere in range(selection):
                    bpy.ops.text.move(type='NEXT_CHARACTER')
                bpy.ops.text.insert(text='"')

            else:    
                for charactere in range(end_selection):   
                    bpy.ops.text.move(type='NEXT_CHARACTER')
                bpy.ops.text.insert(text='"')
                for charactere in range(selection):
                    bpy.ops.text.move(type='NEXT_CHARACTER')
                bpy.ops.text.insert(text='"')
                
        else:   
            bpy.ops.text.insert(text='""')
            bpy.ops.text.move(type='PREVIOUS_CHARACTER')
        
        return {'FINISHED'}


class customApostrophe(Operator):
    bl_idname = "text.custom_apostrophe"
    bl_label = "Custom Apostrophe"
   
    def execute(self, context):
        base = bpy.context.space_data.text.current_line.body
        start_selection = bpy.context.space_data.text.current_character
        end_selection = bpy.context.space_data.text.select_end_character        
     
        if start_selection < end_selection:
            selection = end_selection - start_selection
            bpy.ops.text.move(type='LINE_BEGIN')            
            if "    " in base[:5]:
                bpy.ops.text.move(type='NEXT_WORD')
                new_start = start_selection - bpy.context.space_data.text.select_end_character
                for charactere in range(new_start):   
                    bpy.ops.text.move(type='NEXT_CHARACTER')
                bpy.ops.text.insert(text="'")
                for charactere in range(selection):
                    bpy.ops.text.move(type='NEXT_CHARACTER')
                bpy.ops.text.insert(text="'")

            else:    
                for charactere in range(start_selection):   
                    bpy.ops.text.move(type='NEXT_CHARACTER')
                bpy.ops.text.insert(text="'")
                for charactere in range(selection):
                    bpy.ops.text.move(type='NEXT_CHARACTER')
                bpy.ops.text.insert(text="'")
                
        elif start_selection > end_selection:
            selection = start_selection - end_selection
            bpy.ops.text.move(type='LINE_BEGIN')            
            if "    " in base[:5]:
                bpy.ops.text.move(type='NEXT_WORD')
                new_start = end_selection - bpy.context.space_data.text.select_end_character
                for charactere in range(new_start):   
                    bpy.ops.text.move(type='NEXT_CHARACTER')
                bpy.ops.text.insert(text="'")
                for charactere in range(selection):
                    bpy.ops.text.move(type='NEXT_CHARACTER')
                bpy.ops.text.insert(text="'")

            else:    
                for charactere in range(end_selection):   
                    bpy.ops.text.move(type='NEXT_CHARACTER')
                bpy.ops.text.insert(text="'")
                for charactere in range(selection):
                    bpy.ops.text.move(type='NEXT_CHARACTER')
                bpy.ops.text.insert(text="'")
                
        else:   
            bpy.ops.text.insert(text="''")
            bpy.ops.text.move(type='PREVIOUS_CHARACTER')
        
        return {'FINISHED'}


class customBracket(Operator):
    bl_idname = "text.custom_bracket"
    bl_label = "Custom Bracket"
    
    def execute(self, context):
        base = bpy.context.space_data.text.current_line.body
        start_selection = bpy.context.space_data.text.current_character
        end_selection = bpy.context.space_data.text.select_end_character        
     
        if start_selection < end_selection:
            selection = end_selection - start_selection
            bpy.ops.text.move(type='LINE_BEGIN')            
            if "    " in base[:5]:
                bpy.ops.text.move(type='NEXT_WORD')
                new_start = start_selection - bpy.context.space_data.text.select_end_character
                for charactere in range(new_start):   
                    bpy.ops.text.move(type='NEXT_CHARACTER')
                bpy.ops.text.insert(text="(")
                for charactere in range(selection):
                    bpy.ops.text.move(type='NEXT_CHARACTER')
                bpy.ops.text.insert(text=")")

            else:    
                for charactere in range(start_selection):   
                    bpy.ops.text.move(type='NEXT_CHARACTER')
                bpy.ops.text.insert(text="(")
                for charactere in range(selection):
                    bpy.ops.text.move(type='NEXT_CHARACTER')
                bpy.ops.text.insert(text=")")
                
        elif start_selection > end_selection:
            selection = start_selection - end_selection
            bpy.ops.text.move(type='LINE_BEGIN')            
            if "    " in base[:5]:
                bpy.ops.text.move(type='NEXT_WORD')
                new_start = end_selection - bpy.context.space_data.text.select_end_character
                for charactere in range(new_start):   
                    bpy.ops.text.move(type='NEXT_CHARACTER')
                bpy.ops.text.insert(text="(")
                for charactere in range(selection):
                    bpy.ops.text.move(type='NEXT_CHARACTER')
                bpy.ops.text.insert(text=")")

            else:    
                for charactere in range(end_selection):   
                    bpy.ops.text.move(type='NEXT_CHARACTER')
                bpy.ops.text.insert(text="(")
                for charactere in range(selection):
                    bpy.ops.text.move(type='NEXT_CHARACTER')
                bpy.ops.text.insert(text=")")
                
        else:   
            bpy.ops.text.insert(text="()")
            bpy.ops.text.move(type='PREVIOUS_CHARACTER')
        
        return {'FINISHED'}        
    

class customBrace(Operator):
    bl_idname = "text.custom_brace"
    bl_label = "Custom Brace"
    
    def execute(self, context):
        base = bpy.context.space_data.text.current_line.body
        start_selection = bpy.context.space_data.text.current_character
        end_selection = bpy.context.space_data.text.select_end_character        
     
        if start_selection < end_selection:
            selection = end_selection - start_selection
            bpy.ops.text.move(type='LINE_BEGIN')            
            if "    " in base[:5]:
                bpy.ops.text.move(type='NEXT_WORD')
                new_start = start_selection - bpy.context.space_data.text.select_end_character
                for charactere in range(new_start):   
                    bpy.ops.text.move(type='NEXT_CHARACTER')
                bpy.ops.text.insert(text="{")
                for charactere in range(selection):
                    bpy.ops.text.move(type='NEXT_CHARACTER')
                bpy.ops.text.insert(text="}")

            else:    
                for charactere in range(start_selection):   
                    bpy.ops.text.move(type='NEXT_CHARACTER')
                bpy.ops.text.insert(text="{")
                for charactere in range(selection):
                    bpy.ops.text.move(type='NEXT_CHARACTER')
                bpy.ops.text.insert(text="}")
                
        elif start_selection > end_selection:
            selection = start_selection - end_selection
            bpy.ops.text.move(type='LINE_BEGIN')            
            if "    " in base[:5]:
                bpy.ops.text.move(type='NEXT_WORD')
                new_start = end_selection - bpy.context.space_data.text.select_end_character
                for charactere in range(new_start):   
                    bpy.ops.text.move(type='NEXT_CHARACTER')
                bpy.ops.text.insert(text="{")
                for charactere in range(selection):
                    bpy.ops.text.move(type='NEXT_CHARACTER')
                bpy.ops.text.insert(text="}")

            else:    
                for charactere in range(end_selection):   
                    bpy.ops.text.move(type='NEXT_CHARACTER')
                bpy.ops.text.insert(text="{")
                for charactere in range(selection):
                    bpy.ops.text.move(type='NEXT_CHARACTER')
                bpy.ops.text.insert(text="}")
                
        else:   
            bpy.ops.text.insert(text="{}")
            bpy.ops.text.move(type='PREVIOUS_CHARACTER')
        
        return {'FINISHED'}
    
    
class customSquareBracket(Operator):
    bl_idname = "text.custom_square_bracket"
    bl_label = "Custom Square Bracket"
    
    def execute(self, context):
        base = bpy.context.space_data.text.current_line.body
        start_selection = bpy.context.space_data.text.current_character
        end_selection = bpy.context.space_data.text.select_end_character        
     
        if start_selection < end_selection:
            selection = end_selection - start_selection
            bpy.ops.text.move(type='LINE_BEGIN')            
            if "    " in base[:5]:
                bpy.ops.text.move(type='NEXT_WORD')
                new_start = start_selection - bpy.context.space_data.text.select_end_character
                for charactere in range(new_start):   
                    bpy.ops.text.move(type='NEXT_CHARACTER')
                bpy.ops.text.insert(text="[")
                for charactere in range(selection):
                    bpy.ops.text.move(type='NEXT_CHARACTER')
                bpy.ops.text.insert(text="]")

            else:    
                for charactere in range(start_selection):   
                    bpy.ops.text.move(type='NEXT_CHARACTER')
                bpy.ops.text.insert(text="[")
                for charactere in range(selection):
                    bpy.ops.text.move(type='NEXT_CHARACTER')
                bpy.ops.text.insert(text="]")
                
        elif start_selection > end_selection:
            selection = start_selection - end_selection
            bpy.ops.text.move(type='LINE_BEGIN')            
            if "    " in base[:5]:
                bpy.ops.text.move(type='NEXT_WORD')
                new_start = end_selection - bpy.context.space_data.text.select_end_character
                for charactere in range(new_start):   
                    bpy.ops.text.move(type='NEXT_CHARACTER')
                bpy.ops.text.insert(text="[")
                for charactere in range(selection):
                    bpy.ops.text.move(type='NEXT_CHARACTER')
                bpy.ops.text.insert(text="]")

            else:    
                for charactere in range(end_selection):   
                    bpy.ops.text.move(type='NEXT_CHARACTER')
                bpy.ops.text.insert(text="[")
                for charactere in range(selection):
                    bpy.ops.text.move(type='NEXT_CHARACTER')
                bpy.ops.text.insert(text="]")
                
        else:   
            bpy.ops.text.insert(text="[]")
            bpy.ops.text.move(type='PREVIOUS_CHARACTER')
        
        return {'FINISHED'}