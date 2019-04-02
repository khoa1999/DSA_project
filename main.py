﻿# -*- coding: utf-8 -*-
"""
Created on Sun Mar 10 19:20:12 2019

@author: Đăng Khoa
"""

from screen import *
import pygame
from pygame.locals import *
from os import path,chdir

def run_game():
    global FPS,Width,Height,main_panel
    """bắt đầu game"""

    pygame.init()    
    main_panel = pygame.display.set_mode((Width,Height)) 
    link_bg = path.join("images","8983.jpg") #để đảm bảo truy cập đc file
    bg = pygame.image.load(link_bg).convert_alpha() #nhất là trên MAC CỦA NGỌC :)0
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
    pygame.display.update()
    pygame.display.set_caption("Battleship")
    fps_clock = pygame.time.Clock()
    start = Panel(Width//2 - length//2,int(2*Height/3),
                  length,height,light,main_panel)
    button = Text("START",(255,193,193),start)
    intro = True
    run_game = True    
    """intro game loop"""
    while(intro):
        fps_clock.tick(FPS)
        mouse_pos = pygame.mouse.get_pos()
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
                button.draw()
            elif not mouse_on:
                start.color = light
                button.color = (255,193,193)
                button.draw()  
            if event.type == pygame.MOUSEBUTTONUP and mouse_on == True:
                intro = False
                pygame.mixer.music.stop()
                link_music = path.join("audios","Battleship.ogg")
                pygame.mixer.music.load(link_music)
                pygame.mixer.music.play(-1)                
    half = pygame.Surface((Width//2,Height),pygame.SRCALPHA)
    half.fill((0,0,0,75))
    drag = False
    e1 = Panel(0,0,int(Width/21),int(Width/21),
               (255,250,250),main_panel)#draw undo test
    ima = Image("Undo.png",e1)#draw undo test
    board_1 = User_Board(int(Width/16),int(Height/6),
                int(Width/2.5),int(Width/2.5),main_panel)
    """Bắt đầu import tàu vào game và event cho tàu"""
    observer = Event_Observer()
    list_ship = BuildShip.build_user_ship(Width,Height,main_panel,board_1)
    for i in list_ship:
        k = Interactive_Ship(i)
        observer._key_r.append(k)
        observer._mouse_up.append(k)
        observer._mouse_down.append(k)
        observer._draw_list.append(i)
    patrol = list_ship[0]
    destroyer = list_ship[1]
    battle_ship = list_ship[2]
    air_carrier = list_ship[3]
    sub = list_ship[4]
    clicked = False
    while(run_game):
        fps_clock.tick(FPS)
        main_panel.blit(bg,(0,0))
        main_panel.blit(half,(Width//2,0))
        board_1.draw()
        ima.draw()#draw undo test
        observer.draw()
        pygame.display.update()
        mouse_pos = pygame.mouse.get_pos()
        mouse_on = battle_ship.mouse_on(mouse_pos)
        board_1.mouse_on(mouse_pos)
        for event in  pygame.event.get():
            keys = pygame.key.get_pressed()
            if event.type == pygame.QUIT:
                run_game = False
                pygame.quit()
            """Dành cho việc drag và drop"""
            if event.type == pygame.MOUSEBUTTONDOWN:
                clicked = True
            if event.type == pygame.MOUSEBUTTONUP:
                clicked = False
            """dùng cho cac phím"""
            if keys[pygame.K_r]: 
                observer.notify_key_r(mouse_pos)
            if(keys[pygame.K_f]):
                battle_ship.fixed()
            if(keys[pygame.K_d]):
                battle_ship = Sink(battle_ship)
            if(keys[pygame.K_s]):
                battle_ship = Ship_on_fire(battle_ship,1)     
        if(clicked):
            observer.notify_mouse_down(mouse_pos)
        else:
            observer.notify_mouse_up(mouse_pos)            
    
if __name__ == "__main__":
    """constant"""
    FPS = 60
    Width,Height = prefer_size()
    main_panel = None
    """function"""
    run_game()





