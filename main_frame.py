# -*- coding: utf-8 -*-
"""
Created on Sun Mar 10 19:20:12 2019

@author: Đăng Khoa
"""

from screen_info import prefer_size
import pygame
from pygame.locals import *
from os import path

def run_game():
    global FPS,Width,Height,main_panel
    """bắt đầu game"""
    pygame.init()    
    main_panel = pygame.display.set_mode((Width,Height)) 
    link_bg = path.join("images","background.jpg") #để đảm bảo truy cập đc file
    bg = pygame.image.load(link_bg).convert_alpha() #nhất là trên Mac của Ngọc
    link_music = path.join("audios","bg_audio.wav")
    link_logo = path.join("images","logo.png")
    logo = pygame.image.load(link_logo).convert_alpha() 
    size = (int(Height/2.5)*4,int(Height/2.5))
    logo = pygame.transform.scale(logo,size)
    pygame.mixer.music.load(link_music)
    pygame.mixer.music.play(-1)#nhạc sẽ chạy liên tục
    main_panel.blit(bg,(0,0))
    main_panel.blit(logo,(int(Width/2 - size[0]/2),int(Height/9)))
    light = (255,48,48)
    length = int(Width//4.5)
    height = int(Height//7)
    coordinate = (Width//2 - length//2,int(2*Height/3),length,height)    
    pygame.display.update()
    pygame.display.set_caption("Battleship")
    fps_clock = pygame.time.Clock()
    start = Button(light,coordinate,main_panel,"START")
    intro = True
    run_game = True    
    """intro game loop"""
    while(intro):
        fps_clock.tick(FPS)
        mouse_pos = pygame.mouse.get_pos()
        start.draw()#vẽ cái nút
        mouse_on = start.mouse_on(mouse_pos,(255,64,64))
        pygame.display.update()
        for event in  pygame.event.get():
            if event.type == pygame.QUIT:
                intro = False
                run_game = False                
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONUP and mouse_on == True:
                intro = False
                pygame.mixer.music.stop()
                link_music = path.join("audios","Battleship.ogg")
                pygame.mixer.music.load(link_music)
                pygame.mixer.music.play(-1)
                
    obj = Button((0,0,255),(0,0,100,200),main_panel)
    drag = False    
    while(run_game):
        main_panel.blit(bg,(0,0)) 
        fps_clock.tick(FPS)        
        obj.draw()
        pygame.display.update()
        mouse_pos = pygame.mouse.get_pos()   
        mouse_on = obj.mouse_on(mouse_pos,obj.color)
        for event in  pygame.event.get():
            if event.type == pygame.QUIT:
                run_game = False
                pygame.quit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    length = obj.width
                    height = obj.height
                    obj.width = height
                    obj.height = length
            if event.type == pygame.MOUSEBUTTONDOWN and mouse_on:
                drag = True
            if event.type == pygame.MOUSEBUTTONUP and drag == True:
                drag = False
        if(drag):
            obj.x = (mouse_pos[0] - obj.width/2)
            obj.y = (mouse_pos[1] - obj.height/2)
    
class Button():
    def __init__(self,color:tuple,coordinate:tuple,frame,text = ""):
        self.text = text
        self.color = color
        self.coordinate = coordinate
        self.frame = frame
    def draw(self):
        pygame.draw.rect(self.frame,self.color,self.coordinate)  
        self.render_string((255,193,193))        
    def render_string(self,color):
        font = pygame.font.Font(None,1000)
        text = font.render(self.text,True,color)
        text = pygame.transform.scale(text,(int(0.8*self.coordinate[2]),
                                     int(self.coordinate[3]*0.8)))
        self.frame.blit(text,(int(self.coordinate[0] + 0.1*self.coordinate[2]),
                        int(self.coordinate[1] + 0.1*self.coordinate[3])))
    def mouse_on(self,mouse_pos:tuple,new_color:tuple,str_color = None):
        """cho bk chuột cho trên nút không và  làm nó đổi màu"""
        if(self.coordinate[0] + self.coordinate[2]
        >=mouse_pos[0]>=self.coordinate[0] and self.coordinate[1] + self.coordinate[3]
        >=mouse_pos[1]>=self.coordinate[1] ):
            pygame.draw.rect(self.frame,new_color,self.coordinate)
            self.render_string((255,255,255))
            return True
        return False
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
if __name__ == "__main__":
    """constant"""
    FPS = 30
    Width,Height = prefer_size()
    main_panel = None
    """function"""
    run_game()





