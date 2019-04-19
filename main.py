# -*- coding: utf-8 -*-
"""
Created on Sun Mar 10 19:20:12 2019

@author: Đăng Khoa
"""

from screen import *
from config_game import get_prefer_size
import pygame
from os import path
import DSA_battleship

def run_game():
    global FPS,Width,Height,main_panel
    """bắt đầu game"""
    pygame.init()    
    main_panel = pygame.display.set_mode((Width,Height))
    
    link_bg = path.join("images","intro_0.jpg") 
    bg = pygame.image.load(link_bg).convert_alpha() 
    bg = pygame.transform.scale(bg,(Width,Height))
    background = JustDraw(bg,main_panel,0,0)
    
    link_music = path.join("audios","bg_audio.wav")
    
    intro_bg = Intro(main_panel,Width,Height)
    
    link_logo = path.join("images","logo.png")
    logo = pygame.image.load(link_logo).convert_alpha() 
    size = (int(Height/3.5)*4,int(Height/3.5))#để đảm bảo truy cập đc file
    logo = pygame.transform.scale(logo,size)#nhất là trên MAC CỦA NGỌC :)0
    lg = JustDraw(logo,main_panel,int(Width/2 - size[0]/2),0)
    
    pygame.mixer.music.load(link_music)
    pygame.mixer.music.play(-1)#nhạc sẽ chạy liên tục
    
    light = (255,48,48)
    length = int(Width//5)
    height = int(Height//9)  
    pygame.display.update()
    pygame.display.set_caption("Battleship")
    fps_clock = pygame.time.Clock()
    start = Panel(Width//2 - length//2,int(5*Height/6),
                  length,height,light,main_panel)
    button = Text("START",(255,193,193),start)
    intro = True
    run_game = True    
    """intro game loop"""
    while(intro):
        fps_clock.tick(FPS)
        mouse_pos = pygame.mouse.get_pos()
        intro_bg.draw()
        lg.draw()
        button.draw() 
        mouse_on = button.mouse_on(mouse_pos)
        pygame.display.update()
        for event in  pygame.event.get():
            if event.type == pygame.QUIT:
                intro = False
                run_game = False                
                pygame.quit()
                quit()
            elif mouse_on:# làm đổi màu chữ vài các nút bấm
                start.color = (255,64,64)
                button.color = (255,255,255)
            elif not mouse_on:
                start.color = light
                button.color = (255,193,193) 
            if event.type == pygame.MOUSEBUTTONUP and mouse_on == True:
                intro = False
                pygame.mixer.music.stop()
                link_music = path.join("audios","Battleship.ogg")
                pygame.mixer.music.load(link_music)
                pygame.mixer.music.play(-1)
          
    link_bg = path.join("images","ocean7.jpg")
    bg = pygame.image.load(link_bg).convert_alpha()
    bg = pygame.transform.scale(bg,(Width,Height))
    background = JustDraw(bg,main_panel,0,0)
            
    half = Panel(int(2*Width/3),0,int(Width/3),Height,(0,0,0,75),main_panel)
    e1 = Panel(0,0,int(Width/21),int(Width/21),
               (255,250,250),main_panel)#draw undo test
    ima = Image("Undo.png",e1)#draw undo test
    board_1 = Grid(int(Width/16),int(Height/8),
                int(Width/2.2),int(Width/2.2),main_panel) 
    """Bắt đầu import tàu vào game và event cho tàu"""
    subject = Event_Subject()
    list_ship = BuildShip.build_user_ship(Width,Height,main_panel,board_1)
    board = Interactive_Board(board_1)
    subject.add_mouse_hover(board)
    subject.add_mouse_up(board)
    subject.add_draw_list(background)
    subject.add_draw_list(board_1)    
    subject.add_draw_list(half)
    for i in list_ship:
        k = Interactive_Ship(i)
        subject.add_key_r(k)
        subject.add_mouse_up(k)
        subject.add_mouse_down(k)
        subject.add_mouse_hover(k)
        subject.add_draw_list(k)
        board_1.add_boat(i)
        
    clicked = False
    while(run_game):
        fps_clock.tick(FPS)
        subject.draw()
        pygame.display.update()
        mouse_pos = pygame.mouse.get_pos()
        for event in  pygame.event.get():
            keys = pygame.key.get_pressed()
            if event.type == pygame.QUIT:
                run_game = False
                pygame.quit()
                quit()
            """Dành cho event nhấn chuột xuống và thả chuột"""
            if event.type == pygame.MOUSEBUTTONDOWN:
                clicked = True
            if event.type == pygame.MOUSEBUTTONUP:
                subject.notify_mouse_up(mouse_pos)                 
                clicked = False
            """dùng cho cac phím"""
            if keys[pygame.K_r]: 
                subject.notify_key_r(mouse_pos)    
        if(clicked):
            subject.notify_mouse_down(mouse_pos)
        else:
            subject.notify_mouse_hover(mouse_pos)
if __name__ == "__main__":
    """constant"""
    FPS = 60
    Width,Height = get_prefer_size()
    main_panel = None
    """function"""
    run_game()





