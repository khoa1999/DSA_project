# -*- coding: utf-8 -*-
"""
Created on Sun Mar 10 19:20:12 2019

@author: Đăng Khoa
"""
import sys
from os import path
import pygame
import numpy as np
from abc import ABC,abstractmethod
from screen import *
from config_game import get_prefer_size
from backend import Backend


class Hu():
    subject = None
    bg = None
    main_panel = None
    enemies = []
    users = []
    states = {}
    fps_clock = None
    size = None
    grid_player = None
    grid_sys = None
    to_change_state = False
    width = 0
    height = 0
    fps = 60
    ship_location = []
    info_board = None
    weapons = []
    score_board = None
    effect_board = None
    @staticmethod
    def run_game():
        Hu.load()
        run_game = True
        clicked = False
        while(run_game):
            Hu.fps_clock.tick(Hu.fps)
            Hu.subject.draw()
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
                    Hu.subject.notify_mouse_up(mouse_pos)                 
                    clicked = False
                """dùng cho cac phím"""
                if keys[pygame.K_r]: 
                    Hu.subject.notify_key_r(mouse_pos)    
            if(clicked):
                Hu.subject.notify_mouse_down(mouse_pos)
            else:
                Hu.subject.notify_mouse_hover(mouse_pos)
            if(Hu.to_change_state):
                Hu.to_change_state = False
                Hu.subject = Hu.subject.change_state()
                Hu.subject.enter_state()
    @staticmethod
    def load():
        Backend.start_game()
        Hu.size = get_prefer_size()
        Hu.width = Hu.size[0]
        Hu.height = Hu.size[1]
        pygame.init()        
        Hu.main_panel = pygame.display.set_mode(Hu.size)
        pygame.display.set_caption("Battleship")
        
        Hu.subject = Intro_State()
        place_ship = Place_Ship_State()
        count_down = Count_Down_State()
        player_state = Player_State()
        weapon_state = Weapon_State()
        computer_state = Computer_State()
        winner_state = Winner_State()
        loser_state = Loser_State()
        
        Hu.subject.set_next(place_ship)#nhở đổi lại
        place_ship.set_next(count_down)
        count_down.set_next(player_state)
        player_state.set_next(weapon_state)
        weapon_state.set_next(computer_state)
        computer_state.set_next(player_state)
        winner_state.set_next(Hu.subject)
        loser_state.set_next(Hu.subject)
        
        Hu.subject.enter_state()
        
        Hu.fps_clock = pygame.time.Clock()
        
        Hu.weapons.append(Shell(Hu.width,Hu.height,Hu.main_panel))
        Hu.weapons.append(Missile(Hu.width,Hu.height,Hu.main_panel))
        Hu.score_board = Score_Board(0,0,2*Hu.width//5,
                                     Hu.height//3,Hu.main_panel)
        Hu.grid_sys = Grid(int(Hu.width/2),int(Hu.height/20),
        int(Hu.width/2.2),int(Hu.width/2.2),Hu.main_panel)
        Hu.effect_board = Effect_Board(Hu.grid_sys)
        
class Abstract_State(Event_Subject):
    def __init__(self,key:str):
        self.key = key
        Hu.states[self.key] = self
        self.has_data = False
        self._next = None
        super().__init__()
    def enter_state(self):
        if(not self.has_data):
            self._build_data()
            self.has_data = True
    @abstractmethod
    def _build_data(self):
        pass
    def set_next(self,state):
        self._next = state
    def change_state(self):
        if(self._next != None):
            return self._next
        else:
            return self
    def _special_condition(self):
        return False
    def draw(self):
        if(self._special_condition()):
            Hu.to_change_state = True
        super().draw()
        
class Intro_State(Abstract_State):
    def __init__(self):
        super().__init__("Intro")
    def _build_data(self):
        intro_bg = Intro(Hu.main_panel,Hu.width,Hu.height)
        link_logo = path.join("images","logo.png")
        logo = pygame.image.load(link_logo).convert_alpha()
        size = (int(Hu.height/3.5)*4,int(Hu.height/3.5))#để đảm bảo truy cập đc file
        logo = pygame.transform.scale(logo,size)#nhất là trên MAC CỦA NGỌC :)0
        lg = JustDraw(logo,Hu.main_panel,int(Hu.width/2 - size[0]/2),0)
        
        length = int(Hu.width//5)
        height = int(Hu.height//9) 
        start = Button.create_text_button(Hu.width//2 - length//2,
                    int(5*Hu.height/6),length,height,'START',(255,48,48),
                    (255,193,193),Hu.main_panel)
        start.set_listener(Start_Listener(start))
        self._mouse_hover.append(start)
        self._mouse_up.append(start)
        self._draw_list = [intro_bg,lg,start]

class Place_Ship_State(Abstract_State):
    def __init__(self):
        super().__init__("Place")
    def _build_data(self):
        link_bg = path.join("images","ocean7.jpg")
        bg = pygame.image.load(link_bg).convert_alpha()
        bg = pygame.transform.scale(bg,Hu.size)
        background = JustDraw(bg,Hu.main_panel,0,0)
        Hu.bg = background
        half = Panel(int(2*Hu.width/3),0,int(Hu.width/3),
                         Hu.height,(0,0,0,75),Hu.main_panel)
        board_1 = Grid(int(Hu.width/10),int(Hu.height/20),
                int(Hu.width/2.2),int(Hu.width/2.2),Hu.main_panel)
        """Bắt đầu import tàu vào game và event cho tàu"""
        list_ship = BuildShip.build_user_ship(Hu.width,Hu.height,
                                              board_1,Hu.main_panel)
        board = Interactive_Board(board_1)
        self.add_mouse_hover(board)
        self.add_mouse_up(board)
        self.add_draw_list(background)
        self.add_draw_list(board)    
        self.add_draw_list(half)
        Hu.grid_player = board
        button = Button.create_image_button(int(2.15*Hu.width/3),int(6.25*Hu.height/7),
                                            Hu.width//21,Hu.width//21,
                                            (255,255,255),"Undo.png",
                                            Hu.main_panel)
        button.set_listener(Undo_Listener())
        button_1 = Button.create_image_button(int(2.75*Hu.width/3),
                                            int(6.25*Hu.height/7),
                                            Hu.width//21,Hu.width//21,
                                            (255,255,255),"tick.png",
                                            Hu.main_panel)
        button_1.set_listener(Start_Battle_Listener())        
        self.add_draw_list(button)
        self.add_draw_list(button_1)
        self.add_mouse_up(button)
        self.add_mouse_up(button_1)
        Hu.info_board = Info(Hu.width//9,int(14*Hu.height/16),
                                int(0.8*Hu.width//2.2),Hu.width//15,Hu.main_panel)
        Hu.info_board.set_text("Welcome to Battleship")
        Hu.info_board.set_text("Drag the ships to the grid")
        self.add_draw_list(Hu.info_board)
        for i in list_ship:
            k = Interactive_Ship(i)
            self.add_key_r(k)
            self.add_mouse_up(k)
            self.add_mouse_down(k)
            self.add_mouse_hover(k)
            self.add_draw_list(k)
            board_1.add_boat(i)
            Hu.users.append(k)
            Hu.ship_location.append((i.x,i.y))
        Hu.states["Intro"].clear_all()
        
class Count_Down_State(Abstract_State):
    def __init__(self):
        super().__init__("Count Down")
    def _build_data(self):
        self.count_down = Count_Down(Hu.width,Hu.height,Hu.main_panel)
        prev = Hu.states["Place"]
        self._draw_list = prev._draw_list
        self.add_draw_list(Panel(0,0,Hu.width,Hu.height,
                                     (0,0,0,200),Hu.main_panel))
        self.add_draw_list(self.count_down)     
        #b = Button.create_image_button(0,0,Hu.width//21,Hu.width//21,
        #                               (255,255,255),"pause.png",Hu.main_panel)
        #b.set_listener(Pause_Listener(b))
        #self.add_draw_list(b)
        #self.add_mouse_up(b)
        self.count_down.start()
        Hu.states["Place"].clear_all()
    def _special_condition(self):
        if(self.count_down.time_left < 0.1):
            return True
        return False

class Player_State(Abstract_State):
    def __init__(self):
        super().__init__("Player")
    def _build_data(self):
        self.turn_left = 3
        self.board = Computer_Board(Hu.grid_sys)        
        self.add_draw_list(Hu.bg)
        Hu.info_board.set_text("Start Game")
        Hu.info_board.set_text("You have 3 missiles")
        self.add_draw_list(Hu.info_board)
        Hu.enemies = Computer_ship.list_ship(Hu.users)
        a = self.board
        self.add_draw_list(Hu.grid_sys)
        self.add_draw_list(Hu.effect_board)
        self.add_draw_list(a)
        self.add_mouse_hover(a)
        self.add_mouse_up(a)
        Hu.states['Count Down'].clear_all()
        b = Button.create_image_button(Hu.width//3,Hu.height//2,Hu.width//21,Hu.width//21,
                                       (255,255,255),'a_0.png',Hu.main_panel)
        b.set_listener(Weapon_Listener(b,0,"Destroy 1 square"))
        self.add_draw_list(b)
        self.add_mouse_up(b)
        self.add_mouse_hover(b) 
        b_2 = Button.create_image_button(Hu.width//12,Hu.height//2,Hu.width//21,Hu.width//21,
                                       (255,255,255),'a_1.png',Hu.main_panel)
        b_2.set_listener(Weapon_Listener(b_2,1,"Destroy 5 squares"))
        b_2.listener.other_listener(b.listener)
        b.listener.other_listener(b_2.listener)
        self.add_draw_list(b_2)
        self.add_mouse_up(b_2)
        self.add_mouse_hover(b_2)
        Weapon_Listener.set_default_choice(b.listener)
        self.add_draw_list(Hu.score_board)
        
    def _special_condition(self):
        if(self.board.fire):
            Hu.states["Weapon"].set_location_fire(self.board.fire_location)
            pygame.mixer.init()
            pygame.mixer.music.load(path.join("audios","ARTILLERY+1.wav"))
            pygame.mixer.music.play(1)
            self.board.fire = False
            if(Hu.states["Weapon"].get_weapon_choice() == 1 and self.turn_left >0):
                self.turn_left -= 1
            elif(Hu.states["Weapon"].get_weapon_choice() == 1 and self.turn_left <= 0):
                Hu.info_board.set_text("You are out of missile")
                Hu.states["Weapon"].set_weapon_choice(0)
            return True
        return False
        
class Weapon_State(Abstract_State):
    def __init__(self):
        super().__init__('Weapon')
        self.effect = Effect_Board(None)
    def get_weapon_choice(self):
        return self.choice
    def set_weapon_choice(self,choice:int):
        self.choice = choice
    def set_location_fire(self,location:tuple):
        self.location = location
        self.actual_location = (Hu.grid_sys.x + location[0]*Hu.grid_sys.w//10,
                                Hu.grid_sys.y + location[1]*Hu.grid_sys.h//10)
    def _build_data(self):
        self.effect.set_grid(Hu.grid_sys)
        Hu.info_board.set_text("Your Turn")
        self._draw_list = []
        self.tick = 0
        self._draw_list.extend(Hu.states["Player"]._draw_list)
        Hu.states["Player"].board.find_spot = False
        self.add_draw_list(Hu.weapons[self.choice])
        self.add_draw_list(self.effect)
    def skip(self):
        self.tick = 200
    def _special_condition(self):
        self.has_data = False
        self.tick += 1
        if(self.tick == 70):
            if(self.choice == 0):
                self.effect.set_location(self.location)
            else:
                 self.effect.set_location(self.location)
                 self.effect.set_location((self.location[0] - 1,self.location[1]))
                 self.effect.set_location((self.location[0] + 1,self.location[1]))
                 self.effect.set_location((self.location[0],self.location[1] + 1))
                 self.effect.set_location((self.location[0],self.location[1] - 1))                 
            return False
        elif(self.tick < 50 and self.choice == 0):
            a = Hu.weapons[self.choice]
            a.x += self.actual_location[0]//49
            a.y = (self.actual_location[1]/(self.actual_location[0])**2)*(a.x)**2
            a.reset()
            a.rotate(-90*np.arctan(2*(self.actual_location[1]/(self.actual_location[0])**2)*a.x)/(np.pi/2))
            return False
        elif(self.tick > 120):
            self.tick = 0
            a = Hu.weapons[self.choice]
            a.reset()
            a.x = 0
            a.y = 0
            self.effect.reset()
            if(Backend.check_win()[0]):
                self._next = Hu.states["Winner"]
            else:
                Hu.info_board.set_text("AI turn")
                y,x = Backend.computer_hit_at()
                Hu.states["Computer"].set_location_fire([x,y])
                self._next = Hu.states["Computer"]
            return True
        elif(self.tick == 1 and self.choice == 1):
            a = Hu.weapons[self.choice]
            a.rotate(
                    -90*np.arctan(self.actual_location[1]/
                                 self.actual_location[0])/np.pi)
        elif(self.tick < 50 and self.choice == 1):
            a = Hu.weapons[self.choice]
            a.x += self.actual_location[0]//49
            a.y += self.actual_location[1]//49
        
class Computer_State(Abstract_State):
    def __init__(self):
        super().__init__("Computer")
        self.player_board = Player_Board(None)
        self.tick = 0
    def _build_data(self):
        self.player_board.set_board(Hu.grid_player.grid)
        self.add_draw_list(Hu.bg)
        self.add_draw_list(Hu.info_board)
        self.add_draw_list(self.player_board)
        self.add_draw_list(Hu.weapons[0])
    def set_location_fire(self,location:list):
        self.location = location
        self.actual_location = (Hu.grid_player.grid.x + location[0]*Hu.grid_player.grid.w//10,
                                Hu.grid_player.grid.y + location[1]*Hu.grid_player.grid.h//10)
        Hu.grid_player.grid.set_hit(self.location[0],self.location[1])
    def _special_condition(self):
        self.tick += 1
        a = Hu.weapons[0]
        if(Backend.check_win()[1]):
            self._next = Hu.states["Loser"]
        else:
            self._next = Hu.states["Player"]
        if(self.tick < 40):
            a.x += self.actual_location[0]//40
            a.y = (self.actual_location[1]/(self.actual_location[0])**2)*(a.x)**2
            a.reset()
            a.rotate(-90*np.arctan(2*(self.actual_location[1]/(self.actual_location[0])**2)*a.x)/(np.pi/2))
            return False
        elif(self.tick > 90):
            a.reset()
            a.x = 0
            a.y = 0
            self.tick = 0
            return True            
    
class Winner_State(Abstract_State):
    def __init__(self):
        super().__init__("Winner")
    def _build_data(self):
        winner = Winner(Hu.width,Hu.height,Hu.main_panel)
        self.add_draw_list(winner)
        b = Button.create_image_button(Hu.width//5,Hu.height//3,
                                       Hu.width//7,Hu.width//int(7*3.5),
                                       (0,0,0,0),'restart.png',Hu.main_panel)
        b.set_listener(Reset_Listener())
        self.add_draw_list(b)
        self.add_mouse_up(b)        
        
class Loser_State(Abstract_State):
    def __init__(self):
        super().__init__("Loser")
    def _build_data(self):
        loser = Loser(Hu.width,Hu.height,Hu.main_panel)
        self.add_draw_list(loser)
        b = Button.create_image_button(Hu.width//5,Hu.height//3,
                                       Hu.width//7,Hu.width//int(7*3.5),
                                       (0,0,0,0),'restart.png',Hu.main_panel)
        b.set_listener(Reset_Listener())
        self.add_draw_list(b)
        self.add_mouse_up(b)         
    
class Start_Listener(Listener):
    def __init__(self,button:Button):
        self.button = button
        self.colors = [(255,255,255),(255,64,64),(255,193,193),(255,48,48)]
    def mouse_up_listener(self):
        Hu.to_change_state = True
    def mouse_hover_listener(self):
        self.button.icon.color = self.colors[0]
        self.button.icon.parent.color = self.colors[1]
    def not_mouse_on_listener(self):
        self.button.icon.color = self.colors[2]
        self.button.icon.parent.color = self.colors[3]
        
class Undo_Listener(Listener):   
    def mouse_up_listener(self):
        for i,v in zip(Hu.users,Hu.ship_location):
            i.ship.x,i.ship.y = v
        for i in Hu.users:
            for j in range(5 - i.ship._num_rotate%4):
                i.ship.rotate()        
                
class Start_Battle_Listener(Listener):
    def mouse_up_listener(self):
        #Hu.grid_player.grid.snap()
        if(Hu.grid_player.grid.ready()):
            Hu.to_change_state = True
            Backend.set_computer_ship()
        else:
            Hu.info_board.set_text("Invalid placement. Try again")

class Pause_Listener(Listener):
    def __init__(self,button:Button):
        self.button = button
        self.num_click = 0
        self.decorator = Image("play.png",self.button.icon.parent)
    def mouse_up_listener(self):
        temp = self.decorator#swap the icon 
        self.decorator = self.button.icon
        self.button.icon = temp
        Hu.states["Count Down"].count_down.paused = not Hu.states["Count Down State"].count_down.paused

class Weapon_Listener(Listener):
    def __init__(self,button:Button,choice:int,string:str):
        self.button = button
        self.icon_2 = Image("b_{}.png".format(choice),
                            Panel(button.icon.x,button.icon.y,
                                  button.icon.w,button.icon.h,(255,215,0),
                                  button.icon.frame))
        self.is_mouse_on = False
        self.text_field = Text(string,(0,0,0),Panel(button.icon.x + button.icon.w//2,
                              button.icon.y + button.icon.h//2,button.icon.w*4,
                              button.icon.h/1.5,(255,255,255),button.icon.frame))
        self.clicked = False
        self.choice = choice
        self.other = None
    def mouse_up_listener(self):
        if(not self.clicked):
            Hu.states['Weapon'].set_weapon_choice(self.choice)
        self.swap()
        self.other.swap()
    def mouse_hover_listener(self):
        self.is_mouse_on = True
    def not_mouse_on_listener(self):
        self.is_mouse_on = False
    def draw(self):
        if(self.is_mouse_on):
            self.text_field.draw()
    def swap(self):
        temp = self.icon_2
        self.icon_2 = self.button.icon
        self.button.icon = temp 
    def other_listener(self,listener:Listener):
        self.other = listener
    @staticmethod
    def set_default_choice(listener:Listener):
        listener.swap()
        Hu.states['Weapon'].set_weapon_choice(listener.choice)
        
class Reset_Listener(Listener):
    def mouse_up_listener(self):
        Backend.end_game()
        Backend.start_game()
        for v in Hu.states.values():
            v.has_data = False
        Hu.to_change_state = True
        Ship._placed = False
        
        
class Skip_Listener(Listener):
    def mouse_up_listener(self):
        Hu.states["Weapon"].skip()

if __name__ == "__main__":
    if(getattr(sys,"Frozen",False)):
        CurrentPath = sys._MEIPASS
    else:
        CurrentPath = path.dirname(__file__)
    imageFolderPath = path.join(CurrentPath,'images')
    Hu.run_game()






