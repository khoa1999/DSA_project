# -*- coding: utf-8 -*-
"""
Created on Sun Mar 10 19:20:12 2019

@author: Đăng Khoa
"""

from screen import prefer_size,Button
import pygame
from pygame.locals import *
from os import path

def run_game():
    global FPS,Width,Height,main_panel
    """bắt đầu game"""
    pygame.init()    
    main_panel = pygame.display.set_mode((Width,Height)) 
    link_bg = path.join("images","background.jpg") #để đảm bảo truy cập đc file
    bg = pygame.image.load(link_bg).convert_alpha() #nhất là trên MAC CỦA NGỌC :)
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
        mouse_on = start.mouse_on(mouse_pos)
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
            elif mouse_on:# làm đổi màu chữ vài các nút bấm
                start.bg = (255,64,64)
                start.str_col = (255,255,255)
                start.draw()
            elif not mouse_on:
                start.bg = light
                start.str_col = (255,193,193)
                start.draw()               
    obj = Button((0,0,255),(0,0,100,200),main_panel)
    drag = False    
    while(run_game):
        fps_clock.tick(FPS)        
        main_panel.blit(bg,(0,0))         
        obj.draw()
        pygame.display.update()
        mouse_pos = pygame.mouse.get_pos()   
        mouse_on = obj.mouse_on(mouse_pos)
        for event in  pygame.event.get():
            keys = pygame.key.get_pressed()
            if event.type == pygame.QUIT:
                run_game = False
                pygame.quit()
            """Dành cho việc drag và drop"""
            if event.type == pygame.MOUSEBUTTONDOWN and mouse_on:
                drag = True
            if event.type == pygame.MOUSEBUTTONUP and drag == True:
                drag = False
            """dùng cho cac phím"""
            if keys[pygame.K_r]: 
                length = obj.width
                height = obj.height
                obj.width = height
                obj.height = length                
        if(drag):
            obj.x = (mouse_pos[0] - obj.width/2)
            obj.y = (mouse_pos[1] - obj.height/2)
    
if __name__ == "__main__":
    """constant"""
    FPS = 30
    Width,Height = prefer_size()
    main_panel = None
    """function"""
    run_game()





