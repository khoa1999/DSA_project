# -*- coding: utf-8 -*-
"""
Created on Sun Mar 10 18:53:44 2019

@author: Đăng Khoa
"""

import tkinter as tk
import pygame
""" tìm độ phân giải của màn hình """
def get_screen_info():
    root = tk.Tk()
    Screen_Width = root.winfo_screenwidth()
    Screen_Height = root.winfo_screenheight()
    return (Screen_Width,Screen_Height)
"""setup độ phân giải tối ưu cho từng máy"""
def prefer_size():
    Screen_Width,Screen_Height = get_screen_info()
    aspect_ratio = Screen_Width/Screen_Height
    if(aspect_ratio >= 1.778):
        Prefer_Height = int(Screen_Height*0.8)
        Prefer_Width = int(Prefer_Height/9)*16      
    else:
        Prefer_Width = int(Screen_Width*0.8)
        Prefer_Height = int(Prefer_Width/16)*9
    return (Prefer_Width,Prefer_Height)

class Button():
    def __init__(self,color:tuple,coordinate:tuple,frame,text = "",
                 str_color = (255,255,255)):
        self.text = text
        self.color = color
        self.coordinate = coordinate
        self.frame = frame
        self.str_color = str_color
    def draw(self):
        pygame.draw.rect(self.frame,self.color,self.coordinate)  
        self.render_string()
    def render_string(self):
        font = pygame.font.Font(None,1000)
        text = font.render(self.text,True,self.str_color)
        text = pygame.transform.scale(text,(int(0.8*self.coordinate[2]),
                                     int(self.coordinate[3]*0.8)))
        self.frame.blit(text,(int(self.coordinate[0] + 0.1*self.coordinate[2]),
                        int(self.coordinate[1] + 0.1*self.coordinate[3])))
    def mouse_on(self,mouse_pos:tuple):
        """cho bk chuột cho trên nút không"""
        if(self.x + self.width
        >=mouse_pos[0]>=self.x and self.y + self.height
        >=mouse_pos[1]>=self.y ):
            return True
        return False
    
    """getter and setter"""
    
    @property
    def width(self):
        return self.coordinate[2]
    @width.setter
    def width(self,num):
        self.coordinate = (self.coordinate[0],self.coordinate[1],
                           int(num),self.coordinate[3])
    @property
    def height(self):
        return self.coordinate[3]
    @height.setter
    def height(self,num):
        self.coordinate = (self.coordinate[0],self.coordinate[1],
                           self.coordinate[2],num)   
    @property
    def x(self):
        return self.coordinate[0]
    @x.setter
    def x(self,num):
        self.coordinate = (num,self.coordinate[1],
                           self.coordinate[2],self.coordinate[3])
    @property
    def y(self):
        return self.coordinate[1]
    @y.setter
    def y(self,num):
        self.coordinate = (self.coordinate[0],num,
                           self.coordinate[2],self.coordinate[3])  
    @property
    def bg(self):
        return self.color
    @bg.setter
    def bg(self,color:tuple):
        self.color = color
    @property
    def str_col(self):
        return self.str_color
    @str_col.setter
    def str_col(self,color:tuple):
        self.str_color = color

        