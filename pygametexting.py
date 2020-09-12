class pyg_text():
    
    def __init__(self,Size,Color,TXTFont,Win=None,Color_over=(0,100,200),Color_press=(0,100,100)):
        
        self.Win = Win
        self.Size = Size
        self.Color = Color
        self.TXTFont = TXTFont
        self.Color_over = Color_over
        self.Color_press = Color_press
        if Win!=None:
        	self.Win = Win

    def count_full_lines(text):
    
        lines = 1
    
        for i in text:
            if i =="\n":
                lines += 1
            
        return lines

    def count_text_lines(text):
    
        lines = 0
        parcial_lines = 0
        got_char = False
        
        early_lines = 0
        
        for i in text:
            if i=="\n":
                early_lines += 1
                
            elif i==" " and i=="\t":
                pass
            else:
                break
        
        for i,j in zip(text,range(len(text))):
            
            if j+1 == len(text):
                if got_char or (i!=" " and i!="\t" and i!="\n"):
                    lines += 1
                    lines += parcial_lines
            else:
                if i == "\n":
                    if got_char:
                        lines += 1
                        lines += parcial_lines
                        parcial_lines = 0
                    else:
                        parcial_lines += 1
                    got_char = False
                elif i!=" " and i!="\t":
                    got_char = True
                    
        lines = lines-early_lines
                
        return lines

    def usable_text(text):
        
        total = 0
        spaces = 0
        chars = 0
        
        for i,j in zip(text,range(len(text))):
            
            if j+1 == len(text):
                if (i!=" " and i!="\t" and i!="\n"):
                    chars += spaces
                    chars += 1
                total += chars
                spaces = 0
                chars = 0
                    
            else:
                if i == "\n":
                    total += chars
                    spaces = 0
                    chars = 0
                elif i == " ":
                    spaces += 1
                else:
                    chars += spaces
                    chars += 1
                    spaces = 0
                
        return total

    def count_big_line(text):

        big_number = 0
        spaces = 0
        chars = 0
        text_line = ""
        big_line = ""


        for i,j in zip(text,range(len(text))):

            if j+1 == len(text):
                if (i!=" " and i!="\t" and i!="\n"):
                    chars += spaces
                    chars += 1
                    for s in range(spaces):
                        text_line = text_line + " "
                    text_line = text_line + i

                if chars>big_number:
                    big_number = chars
                    big_line = text_line
                spaces = 0
                chars = 0
                text_line = ""

            else:
                if i == "\n":
                    if chars>big_number:
                        big_number = chars
                        big_line = text_line
                    spaces = 0
                    chars = 0
                    text_line = ""
                elif i == " ":
                    spaces += 1
                else:
                    chars += spaces
                    chars += 1
                    for s in range(spaces):
                        text_line = text_line + " "
                    text_line = text_line + i
                    spaces = 0

        return [big_number,big_line]

    def screen_text_centerpos(self,text, x_pos, y_pos, size=None, color=None, txtfont=None, win=None):
        import pygame
        import sys
        
        if win==None:
            win=self.Win
        if size==None:
            size=self.Size
        if color==None:
            color=self.Color
        if txtfont==None:
            txtfont=self.TXTFont
        
        text_font = pygame.font.SysFont(txtfont, size) 
        rendered_text = text_font.render(str(text), True, color)
        textRect = rendered_text.get_rect()
        textRect.center = (x_pos, y_pos)
        win.blit(rendered_text, textRect)

    def screen_multtext_centerpos(self,text, x_pos, y_pos, y_dist, var_x=True, 
    	size=None, color=None, txtfont=None, win=None):
        import pygame
        import sys

        # var_x has the default as True, that means it selects the beginning of the text
        # based on the usable text divided by the number of text lines
        # the middle of that average length will be located in the set x_pos
        # If this value is False, it selects the middle location as the beginning of the text lines
        
        if win==None:
            win=self.Win
        if size==None:
            size=self.Size
        if color==None:
            color=self.Color
        if txtfont==None:
            txtfont=self.TXTFont
        
        o_font = pygame.font.SysFont(txtfont, size) 
        o_rendered_text = o_font.render('o', True, (0,0,0))
        o_textRect = o_rendered_text.get_rect()
        o_textlist=list(o_textRect[2:4])
        o_total_x=int(o_textlist[0])
        o_total_y=int(o_textlist[1])

        y_sub = int(o_total_y/2)

        if var_x:

            magic_number = pyg_text.usable_text(text)/pyg_text.count_text_lines(text)

            x = x_pos - int(magic_number*o_total_x/2)

        else:
            x = x_pos

        n_lines = pyg_text.count_full_lines(text)

        start_point = 0
        lines = 0
        y = int(y_pos - ((n_lines-1)*y_dist/2))

        for char,index in zip(text,range(len(text))):
            if index+1 == len(text):
                if char == "\n":
                    self.screen_text_initpos(text[start_point+1:index],x,y-y_sub,size=size,color=color,txtfont=txtfont,win=win)
                else:
                    self.screen_text_initpos(text[start_point+1:index+1],x,y-y_sub,size=size,color=color,txtfont=txtfont,win=win)

            elif char == "\n":
                if lines == 0:
                    self.screen_text_initpos(text[start_point:index],x,y-y_sub,size=size,color=color,txtfont=txtfont,win=win)
                else:
                    self.screen_text_initpos(text[start_point+1:index],x,y-y_sub,size=size,color=color,txtfont=txtfont,win=win)
                start_point = index
                y += y_dist
                lines += 1
        
    def screen_text_initpos(self,text, x_pos, y_pos, size=None, color=None, txtfont=None, win=None):
        import pygame
        import sys
        
        if win==None:
            win=self.Win
        if size==None:
            size=self.Size
        if color==None:
            color=self.Color
        if txtfont==None:
            txtfont=self.TXTFont
        
        text_font = pygame.font.SysFont(txtfont, size)
        rendered_text = text_font.render(str(text), True, color)
        textRect = rendered_text.get_rect()
        textRect.x = x_pos
        textRect.y = y_pos
        win.blit(rendered_text, textRect)

    def screen_multtext_initpos(self,text, x_pos, y_pos, y_dist, size=None, color=None, txtfont=None, win=None):
        import pygame
        import sys
        
        if win==None:
            win=self.Win
        if size==None:
            size=self.Size
        if color==None:
            color=self.Color
        if txtfont==None:
            txtfont=self.TXTFont

        start_point = 0
        lines = 0
        y = y_pos

        for char,index in zip(text,range(len(text))):
            if index+1 == len(text):
                if char == "\n":
                    self.screen_text_initpos(text[start_point+1:index],x_pos,y,size=size,color=color,txtfont=txtfont,win=win)
                else:
                    self.screen_text_initpos(text[start_point+1:index+1],x_pos,y,size=size,color=color,txtfont=txtfont,win=win)

            elif char == "\n":
                if lines == 0:
                    self.screen_text_initpos(text[start_point:index],x_pos,y,size=size,color=color,txtfont=txtfont,win=win)
                else:
                    self.screen_text_initpos(text[start_point+1:index],x_pos,y,size=size,color=color,txtfont=txtfont,win=win)
                start_point = index
                y += y_dist
                lines += 1
        
    def screen_text_limitpos(self,text, x_pos, y_pos, size=None, color=None, txtfont=None, win=None):
        import pygame
        import sys
        
        if win==None:
            win=self.Win        
        if size==None:
            size=self.Size
        if color==None:
            color=self.Color
        if txtfont==None:
            txtfont=self.TXTFont
        
        text_font = pygame.font.SysFont(txtfont, size) 
        rendered_text = text_font.render(str(text), True, color)
        textRect = rendered_text.get_rect()
        textlist=list(textRect[2:4])
        x_init= x_pos - textlist[0]
        y_init= y_pos - textlist[1]
        textRect.x = x_init
        textRect.y = y_init
        win.blit(rendered_text, textRect)

    def screen_multtext_limitpos(self,text, x_pos, y_pos, y_dist, size=None, color=None, txtfont=None, win=None):
        import pygame
        import sys
        
        if win==None:
            win=self.Win
        if size==None:
            size=self.Size
        if color==None:
            color=self.Color
        if txtfont==None:
            txtfont=self.TXTFont

        magic_number = pyg_text.count_big_line(text)

        mn_font = pygame.font.SysFont(txtfont, size) 
        mn_rendered_text = mn_font.render(magic_number[1], True, (0,0,0))
        mn_textRect = mn_rendered_text.get_rect()
        mn_textlist=list(mn_textRect[2:4])
        mn_total_x=int(mn_textlist[0])
        mn_total_y=int(mn_textlist[1])

        y_sub = int(mn_total_y)

        x = int(x_pos-mn_total_x)

        n_lines = pyg_text.count_full_lines(text)

        start_point = 0
        lines = 0
        y = int(y_pos - (n_lines-1)*y_dist)

        for char,index in zip(text,range(len(text))):
            if index+1 == len(text):
                if char == "\n":
                    self.screen_text_initpos(text[start_point+1:index],x,y-y_sub,size=size,color=color,txtfont=txtfont,win=win)
                else:
                    self.screen_text_initpos(text[start_point+1:index+1],x,y-y_sub,size=size,color=color,txtfont=txtfont,win=win)

            elif char == "\n":
                if lines == 0:
                    self.screen_text_initpos(text[start_point:index],x,y-y_sub,size=size,color=color,txtfont=txtfont,win=win)
                else:
                    self.screen_text_initpos(text[start_point+1:index],x,y-y_sub,size=size,color=color,txtfont=txtfont,win=win)
                start_point = index
                y += y_dist
                lines += 1

    def screen_button_centerpos(self,text, x_pos, y_pos, over_effect=False, size=None, color=None, 
        color_over=None, color_press=None, txtfont=None, win=None):

        import pygame
        import sys

        if win==None:
            win=self.Win
        if size==None:
            size=self.Size
        if color==None:
            color=self.Color
        if color_over==None:
            color_over=self.Color_over
        if color_press==None:
            color_press=self.Color_press
        if txtfont==None:
            txtfont=self.TXTFont
        
        text_font = pygame.font.SysFont(txtfont, size) 
        rendered_text = text_font.render(str(text), True, (0,0,0))
        textRect = rendered_text.get_rect()
        textlist=list(textRect[2:4])
        x_center = x_pos
        y_center = y_pos
        total_x=int(textlist[0])
        total_y=int(textlist[1])
        x_init=int(x_center-total_x/2)
        y_init=int(y_center-total_y/2)
        x_limit=int(x_center+total_x/2)
        y_limit=int(y_center+total_y/2)

        n_actions = 0

        self.screen_text_centerpos(text,x_center,y_center, size=size, color = color, txtfont=txtfont, win=win)
        if x_init<pygame.mouse.get_pos()[0]<x_limit and y_init<pygame.mouse.get_pos()[1]<y_limit:
            n_actions = 1
            self.screen_text_centerpos(text,x_center,y_center, size=size, color = color_over, txtfont=txtfont, win=win)
            if pygame.mouse.get_pressed()[0]:
                n_actions = 2
                self.screen_text_centerpos(text,x_center,y_center, size=size, color = color_press, txtfont=txtfont, win=win)
                pygame.display.update((x_init,y_init),(total_x,total_y))

        if over_effect:
            return n_actions
        elif n_actions == 2:
            return True



    def screen_button_initpos(self,text, x_pos, y_pos, over_effect=False, size=None, color=None, 
        color_over=None, color_press=None, txtfont=None, win=None):

        import pygame
        import sys

        if win==None:
            win=self.Win
        if size==None:
            size=self.Size
        if color==None:
            color=self.Color
        if color_over==None:
            color_over=self.Color_over
        if color_press==None:
            color_press=self.Color_press
        if txtfont==None:
            txtfont=self.TXTFont
        
        text_font = pygame.font.SysFont(txtfont, size) 
        rendered_text = text_font.render(str(text), True, (0,0,0))
        textRect = rendered_text.get_rect()
        textlist=list(textRect[2:4])
        x_init = x_pos
        y_init = y_pos
        total_x=int(textlist[0])
        total_y=int(textlist[1])
        x_center=int(x_init+total_x/2)
        y_center=int(y_init+total_y/2)
        x_limit=int(x_init+total_x)
        y_limit=int(y_init+total_y)

        n_actions = 0

        self.screen_text_initpos(text,x_init,y_init, size=size, color = color, txtfont=txtfont, win=win)
        if x_init<pygame.mouse.get_pos()[0]<x_limit and y_init<pygame.mouse.get_pos()[1]<y_limit:
            n_actions = 1
            self.screen_text_initpos(text,x_init,y_init, size=size, color = color_over, txtfont=txtfont, win=win)
            if pygame.mouse.get_pressed()[0]:
                n_actions = 2
                self.screen_text_initpos(text,x_init,y_init, size=size, color = color_press, txtfont=txtfont, win=win)
                pygame.display.update((x_init,y_init),(total_x,total_y))

        if over_effect:
            return n_actions
        elif n_actions == 2:
            return True


    def screen_button_limitpos(self,text, x_pos, y_pos, over_effect=False, size=None, color=None, 
        color_over=None, color_press=None, txtfont=None, win=None):

        import pygame
        import sys

        if win==None:
            win=self.Win
        if size==None:
            size=self.Size
        if color==None:
            color=self.Color
        if color_over==None:
            color_over=self.Color_over
        if color_press==None:
            color_press=self.Color_press
        if txtfont==None:
            txtfont=self.TXTFont
        
        text_font = pygame.font.SysFont(txtfont, size) 
        rendered_text = text_font.render(str(text), True, (0,0,0))
        textRect = rendered_text.get_rect()
        textlist=list(textRect[2:4])
        x_limit = x_pos
        y_limit = y_pos
        total_x=int(textlist[0])
        total_y=int(textlist[1])
        x_init=int(x_limit-total_x)
        y_init=int(y_limit-total_y)
        x_center=int(x_limit-total_x/2)
        y_center=int(y_limit-total_y/2)

        n_actions = 0

        self.screen_text_limitpos(text,x_limit,y_limit, size=size, color = color, txtfont=txtfont, win=win)
        if x_init<pygame.mouse.get_pos()[0]<x_limit and y_init<pygame.mouse.get_pos()[1]<y_limit:
            n_actions = 1
            self.screen_text_limitpos(text,x_limit,y_limit, size=size, color = color_over, txtfont=txtfont, win=win)
            if pygame.mouse.get_pressed()[0]:
                n_actions = 2
                self.screen_text_limitpos(text,x_limit,y_limit, size=size, color = color_press, txtfont=txtfont, win=win)
                pygame.display.update((x_init,y_init),(total_x,total_y))

        if over_effect:
            return n_actions
        elif n_actions == 2:
            return True

class pyg_tesxt():
    
    def __init__(self,Size,TXTFont):
        
        self.Size = Size
        self.TXTFont = TXTFont
        
    #Use print(xxx.method()) to print with the correct formatting
    
    def test_on_screen_center_text(self,text, x_center=0, y_center=0, size=None, txtfont=None):
        import pygame
        import sys    
        
        if size==None:
            size=self.Size
        if font==None:
            txtfont=self.Font

        pygame.init()
        font = pygame.font.SysFont(txtfont, size) 
        rendered_text = font.render(str(text), True, (0,0,0))
        textRect = rendered_text.get_rect()
        textlist=list(textRect[2:4])
        x_to_y=textlist[0]/textlist[1]
        final_report="Total Rect width: {}, x init: {}, x limit: {}\n".format(int(textlist[0]), int(x_center-textlist[0]/2), int(x_center+textlist[0]/2))
        final_report+="Total Rect height: {}, y init: {}, y limit: {}\n".format(int(textlist[1]), int(y_center-textlist[1]/2), int(y_center+textlist[1]/2))
        final_report+="x/y: {}".format(x_to_y)
        pygame.quit()
        
        return final_report
    
    def test_on_screen_init_text(self,text, x_init=0, y_init=0, size=None, txtfont=None):
        import pygame
        import sys    
        
        if size==None:
            size=self.Size
        if font==None:
            txtfont=self.TXTFont
        
        pygame.init()
        font = pygame.font.SysFont(txtfont, size) 
        rendered_text = font.render(str(text), True, (0,0,0))
        textRect = rendered_text.get_rect()
        textlist=list(textRect[2:4])
        x_to_y=textlist[0]/textlist[1]
        final_report="Total Rect width: {}, x center: {}, x limit: {}\n".format(int(textlist[0]), int(x_init+textlist[0]/2), int(x_init+textlist[0]))
        final_report+="Total Rect height: {}, y center: {}, y limit: {}\n".format(int(textlist[1]), int(y_init+textlist[1]/2), int(y_init+textlist[1]))
        final_report+="x/y: {}".format(x_to_y)
        pygame.quit()
        
        return final_report
    
    def test_on_screen_limit_text(self,text, x_limit=0, y_limit=0, size=None, font=None):
        import pygame
        import sys    
        
        if size==None:
            size=self.Size
        if font==None:
            txtfont=self.TXTFont
        
        pygame.init()
        font = pygame.font.SysFont(txtfont, size) 
        rendered_text = font.render(str(text), True, (0,0,0))
        textRect = rendered_text.get_rect()
        textlist=list(textRect[2:4])
        x_to_y=textlist[0]/textlist[1]
        final_report="Total Rect width: {}, x init: {}, x center: {}\n".format(int(textlist[0]), int(x_limit-textlist[0]), int(x_limit-textlist[0]/2))
        final_report+="Total Rect height: {}, y init: {}, y center: {}\n".format(int(textlist[1]), int(y_limit-textlist[1]), int(y_limit-textlist[1]/2))
        final_report+="x/y: {}".format(x_to_y)
        pygame.quit()
        
        return final_report
    
        
    def test_size_for_screen_x(self,text, x, txtfont=None):
        import pygame
        import sys          
        
        if font==None:
            txtfont=self.TXTFont
        
        pygame.init()
        font = pygame.font.SysFont(txtfont, 10) 
        rendered_text = font.render(str(text), True, (0,0,0))
        textRect = rendered_text.get_rect()
        textlist=list(textRect[2:4])
        x_to_y=textlist[0]/textlist[1]
        size_needed=int(x/x_to_y)
        pygame.quit()
        
        return size_needed
        
    # Examples    

    # from pygametexting import pyg_tesxt
    
    # tt=pyg_tesxt(20,"comicsansms")
        
    # print(tt.test_on_screen_center_text("ALOHA")):
    
    # Total Rect width: 70, x init: -35, x limit: 35
    # Total Rect height: 29, y init: -14, y limit: 14
    # x/y: 2.413793103448276
    
    # print(tt.test_on_screen_init_text("ALOHA")):
    
    # Total Rect width: 70, x center: 35, x limit: 70
    # Total Rect height: 29, y center: 14, y limit: 29
    # x/y: 2.413793103448276
    
    # print(tt.test_on_screen_limit_text("ALOHA")):
    
    # Total Rect width: 70, x init: -70, x center: -35
    # Total Rect height: 29, y init: -29, y center: -14
    # x/y: 2.413793103448276
    
    # print(test_size_for_screen_x("ALOHA",20)) --> 8


class pyg_button():
    
    #obj1 is the object name for the properties Size and Font
    #obj2 is the string version (used with "" or '') of obj1
    
    def __init__(self,obj1,obj2):
        
        self.Size = obj1.Size
        self.TXTFont = obj1.TXTFont
        self.Obj = obj2
        
    # Use print(xxx.method()) to print with the correct formatting
    # color1 is the color for the button selection
    # color2 is the color for the button press
        
    def center_button(self,text, x_center, y_center, color1, color2, size=None,txtfont=None,obj=None):    

        import pygame
        import sys

        if size==None:
            size=self.Size
        if txtfont==None:
            txtfont=self.TXTFont
        if obj==None:
            obj=self.Obj
        
            
        pygame.init()
        font = pygame.font.SysFont(txtfont, size) 
        rendered_text = font.render(str(text), True, (0,0,0))
        textRect = rendered_text.get_rect()
        textlist=list(textRect[2:4])
        total_x=int(textlist[0])
        total_y=int(textlist[1])
        x_init=int(x_center-total_x/2)
        y_init=int(y_center-total_y/2)
        x_limit=int(x_center+total_x/2)
        y_limit=int(y_center+total_y/2)
        ifs = '''{11}.screen_text_centerpos(\'{0}\',{3},{4})
if {1}<pygame.mouse.get_pos()[0]<{5} and {2}<pygame.mouse.get_pos()[1]<{6}:
    {11}.screen_text_centerpos(\'{0}\',{3},{4},color = {9})
    if mouse[0]:
        {11}.screen_text_centerpos(\'{0}\',{3},{4},color = {10})
        pygame.display.update(({1},{2}),({7},{8}))'''.format(text,x_init,y_init,x_center,y_center,
                                                             x_limit,y_limit,total_x,total_y,color1,
                                                             color2,obj)
        pygame.quit()
        
        return ifs
    
    def init_button(self,text, x_init, y_init, color1, color2, size=None,txtfont=None,obj=None):  

        import pygame
        import sys

        if size==None:
            size=self.Size
        if txtfont==None:
            txtfont=self.TXTFont
        if obj==None:
            obj=self.Obj
        
            
        pygame.init()
        font = pygame.font.SysFont(txtfont, size) 
        rendered_text = font.render(str(text), True, (0,0,0))
        textRect = rendered_text.get_rect()
        textlist=list(textRect[2:4])
        total_x=int(textlist[0])
        total_y=int(textlist[1])
        x_center=int(x_init+total_x/2)
        y_center=int(y_init+total_y/2)
        x_limit=int(x_init+total_x)
        y_limit=int(y_init+total_y)
        ifs = '''{11}.screen_text_initpos(\'{0}\',{1},{2})
if {1}<pygame.mouse.get_pos()[0]<{5} and {2}<pygame.mouse.get_pos()[1]<{6}:
    {11}.screen_text_initpos(\'{0}\',{1},{2},color = {9})
    if mouse[0]:
        {11}.screen_text_initpos(\'{0}\',{1},{2},color = {10})
        pygame.display.update(({1},{2}),({7},{8}))'''.format(text,x_init,y_init,x_center,y_center,
                                                             x_limit,y_limit,total_x,total_y,color1,
                                                             color2,obj)
        pygame.quit()
        
        return ifs
    
    def limit_button(self,text, x_limit, y_limit, color1, color2, size=None,txtfont=None,obj=None):  

        import pygame
        import sys

        if size==None:
            size=self.Size
        if txtfont==None:
            txtfont=self.TXTFont
        if obj==None:
            obj=self.Obj
        
            
        pygame.init()
        font = pygame.font.SysFont(txtfont, size) 
        rendered_text = font.render(str(text), True, (0,0,0))
        textRect = rendered_text.get_rect()
        textlist=list(textRect[2:4])
        total_x=int(textlist[0])
        total_y=int(textlist[1])
        x_init=int(x_limit-total_x)
        y_init=int(y_limit-total_y)
        x_center=int(x_limit-total_x/2)
        y_center=int(y_limit-total_y/2)
        ifs = '''{11}.screen_text_limitpos(\'{0}\',{5},{6})
if {1}<pygame.mouse.get_pos()[0]<{5} and {2}<pygame.mouse.get_pos()[1]<{6}:
    {11}.screen_text_limitpos(\'{0}\',{5},{6},color = {9})
    if mouse[0]:
        {11}.screen_text_limitpos(\'{0}\',{5},{6},color = {10})
        pygame.display.update(({1},{2}),({7},{8}))'''.format(text,x_init,y_init,x_center,y_center,
                                                             x_limit,y_limit,total_x,total_y,color1,
                                                             color2,obj)
        pygame.quit()
        
        return ifs
    
    # Examples:

    # from pygametexting import pyg_text, pyg_button
    
    # pgt=pyg_text(20,(255,255,255),"comicsansms")
    # pygb=pyg_button(pgt,"pgt")
    # print(pygb.center_button("Huehue",50,50,(0,100,200),(0,100,100)))
    
    # Results:
    
    # pgt.screen_text_centerpos('Huehue',50,50)
    # if 15<pygame.mouse.get_pos()[0]<84 and 35<pygame.mouse.get_pos()[1]<64:
    #     pgt.screen_text_centerpos('Huehue',50,50,color = (0, 100, 200))
    #     if mouse[0]:
    #         pgt.screen_text_centerpos('Huehue',50,50,color = (0, 100, 100))
    #         pygame.display.update((15,35),(69,29))

