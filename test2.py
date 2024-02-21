import pygame
import sys
from pygame.locals import QUIT
import numpy as np
import os 
from subprocess import run
from exec import exec_with_return 
import sys
import random
from dataclasses import dataclass
import sqlite3



class Text():

    def __init__(self):
        self.font = pygame.font.SysFont("Courier", 20)
        self.text = self.font.render(("hello"), True, (155, 155, 155))

    def render(self, display, text, locx, locy, font_size, colour):
        self.font = pygame.font.SysFont("Courier", font_size)
        self.text = self.font.render((str(text)), True, colour)
        display.blit(self.text, (locx, locy))

    def renderall(self,display, font_size, colour,list, user_row):
        y=10
        row_num=1
        for row in list:
            #box to indicate where the user is (which line the user is on)
            if row_num==(user_row+1):
                self.render(display,str(row_num),0,y ,font_size,colour) 
                self.render(display, str(row)+"□", 40, y , font_size, colour)
            else:
                self.render(display,str(row_num),0,y ,font_size,colour) 
                self.render(display, row, 40, y , font_size, colour)
            y+=40
            row_num+=1

@dataclass
class Question():
    function_name : str
    comments : str
    pre_written_code: list
    end_written_code : list
    conditions : list 
    answer : str    


class Terminal():
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.display = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.screen_width, self.screen_height =self.display.get_size()
        self.background_colour=((63,63,63))
        self.display.fill(self.background_colour)
        pygame.display.set_caption('hackbox')
        self.text=Text()
        question_parts=self.get_random_from_table()
        self.question=Question(question_parts[0],question_parts[1],question_parts[2],question_parts[3],question_parts[4],question_parts[5])
        self.user_text=[self.question_2_array()]
        self.start_limit=2+len(self.str_2_list(self.question.pre_written_code))
        self.end_limit=1+len(self.str_2_list(self.question.end_written_code))
        self.user_row=self.start_limit
        self.user_text=[self.question_2_array()]
        self.user_text=self.user_text[0]

    def convert_2_string(self, question: Question):
        written_code=self.user_text[2:-1]
        code_str = f"def {question.function_name}():"+"\n"
        code_str += "    " + (f"""#{question.comments}""" or "") +"\n"
        for line in written_code:
            code_str+=f"""{line}\n"""
        code_str += f"""{question.function_name}()"""
        return code_str
    
    def check_code(self):
        code_output=self.return_execute_output()
        output_answer_check=False
        if str(code_output)==str(self.question.answer):
            output_answer_check=True
        only_user_code=self.user_text[self.start_limit:-self.end_limit]
        condition_check=True
        for condition in self.str_2_list(self.question.conditions):
            if str(condition.strip("'")) not in str(only_user_code) :
                condition_check=False
        return (output_answer_check,condition_check)

    def check_process(self):  
        a=self.check_code()
        font_size=20
        self.text.render(self.display,f"output: {self.return_execute_output()}",30,self.screen_height/3*2,font_size,((200,155,50)))
        self.text.renderall(self.display,20,(255,255,255),self.user_text,self.user_row)
        pygame.display.update()
        pygame.time.delay(800)
        if a[0]==True:
            colour=(0,250,0)
            text="correct"   
        else:
            colour=(250,0,0)
            text="incorrect"
        self.text.render(self.display,f"answer check: {text}",30,self.screen_height/3*2+font_size,font_size,colour)
        self.text.renderall(self.display,20,(255,255,255),self.user_text,self.user_row)
        pygame.display.update()
        pygame.time.delay(800)
        if a[1]==True:
            colour=(0,250,0)
            text="check passed"
        else:
            colour=(250,0,0)
            text="check failed"
        self.text.render(self.display,f"condition check: {text}",30,self.screen_height/3*2+font_size*2,font_size,colour)
        pygame.display.update()
        pygame.time.delay(800)
        if a[0]==True and a[1]==True:
            return True
    def return_execute_output(self):   
        code_str=self.convert_2_string(self.question)
        try:
            code_output=exec_with_return(code_str)
            return code_output
        except Exception as error_code:
            return error_code
       
        

    def question_2_array(self):
        question_array=[]
        question_array+=[f"""def {self.question.function_name}():"""]
        question_array+=[f"""    #{self.question.comments}"""]
        pre_written_code = self.str_2_list(self.question.pre_written_code)
        for question_line in pre_written_code:
            question_array+=[f"""    {question_line}"""]
        question_array+=["    "]
        end_written_code = self.str_2_list(self.question.end_written_code)
        for question_line in end_written_code:
            question_array+=[f"""    {question_line}"""]
        question_array+=[f"""{self.question.function_name}()"""]
        return question_array
        
    def str_2_list(self, str):
        list = str.strip("""]['""").split(', ')
        return list

    def get_random_from_table(self):
        connection_obj = sqlite3.connect('QUESTION.db')
        cursor_obj = connection_obj.cursor()
        cursor_obj.execute("""
        SELECT MAX(id) FROM question;
        """)
        range=cursor_obj.fetchall()
        random_num=random.randint(1,range[0][0])
        cursor_obj.execute(f"""
        SELECT * FROM question
        WHERE id={random_num}
        """)
        a=cursor_obj.fetchall()
        question=a[0][1],a[0][2],a[0][3],a[0][4],a[0][5],a[0][6]
        return question

    def clear(self):
        self.user_text=[self.question_2_array()]
        self.start_limit=2+len(self.str_2_list(self.question.pre_written_code))
        self.end_limit=1+len(self.str_2_list(self.question.end_written_code))
        self.user_row=self.start_limit
        self.user_text=[self.question_2_array()]
        self.user_text=self.user_text[0]
    
    def check_inputs(self):
             for event in pygame.event.get():
                self.display.fill((self.background_colour))
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                        button_press=event.key
                        if (button_press==pygame.K_DOWN or button_press==pygame.K_RETURN) and self.user_row+1==len(self.user_text) and self.user_row<18:
                            self.user_text+=["    "]  
                        if button_press==pygame.K_UP and self.user_row>self.start_limit:
                            self.user_row-=1
                        elif button_press==pygame.K_DOWN and self.user_row<18 and self.user_row<len(self.user_text)-3:
                            self.user_row+=1
                        elif button_press==pygame.K_RETURN and self.user_row<18:
                            self.user_row+=1
                            self.user_text.insert(self.user_row,"    ")
                        elif button_press==pygame.K_BACKSPACE:
                            if not len(self.user_text[self.user_row])<=4:
                                self.user_text[self.user_row]=self.user_text[self.user_row][:len(self.user_text[self.user_row])-1]
                        elif button_press==pygame.K_TAB:
                            self.user_text[self.user_row]+="    "
                            #run the code
                        elif button_press==pygame.K_ESCAPE:
                            if self.check_process()==True:
                                return False
                            #clear the code
                        elif button_press==pygame.K_HASH:
                            self.clear()
                        if (button_press!=pygame.K_RETURN) and (button_press!=pygame.K_BACKSPACE) and (button_press!=pygame.K_TAB) and( button_press!=pygame.K_ESCAPE) and button_press!=pygame.K_HASH:
                            button_press=event.unicode 
                            self.user_text[self.user_row]+=button_press
    def run(self, display):
        while True:
            if self.check_inputs()==False:
                break
            self.text.renderall(display,20,(255,255,255),self.user_text,self.user_row)
            pygame.display.update()
            self.clock.tick(60)