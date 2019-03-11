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
    """bắt đầu game"""
    pygame.init()    
    main_panel = pygame.display.set_mode((Width,Height)) 
    link_bg = path.join("images","background.jpg") #để đảm bảo truy cập đc file
    bg = pygame.image.load(link_bg).convert_alpha() #nhất là trên Mac của Ngọc
    link_music = path.join("audios","bg_audio.wav")
    pygame.mixer.music.load(link_music)
    pygame.mixer.music.play(-1)#nhạc sẽ chạy liên tục
    main_panel.blit(bg,(0,0))
    pygame.display.update()
    pygame.display.set_caption("Battleship")
    fps_clock = pygame.time.Clock()
    run_game = True
    """maingame loop"""
    while(run_game):
        fps_clock.tick(FPS)
        for event in  pygame.event.get():
            if event.type == QUIT:          
                run_game =  False
    pygame.quit()
if __name__ == "__main__":
    """constant"""
    FPS = 30
    Width,Height = prefer_size()
    """function"""
    run_game()





