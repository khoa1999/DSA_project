# -*- coding: utf-8 -*-
"""
Created on Sun Mar 10 19:20:12 2019

@author: Đăng Khoa
"""
from os import path
import time
import pygame
from screen import *
from config_game import get_prefer_size
import DSA_battleship

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
        Hu.size = get_prefer_size()
        Hu.width = Hu.size[0]
        Hu.height = Hu.size[1]
        pygame.init()        
        Hu.main_panel = pygame.display.set_mode(Hu.size)
        pygame.display.set_caption("Battleship")
        
        Hu.subject = Intro_State()
        place_ship = Place_Ship()
        count_down = Count_Down_State()
        Hu.subject.set_next(place_ship)
        place_ship.set_next(count_down)
        
        Hu.subject.enter_state()
        
        Hu.fps_clock = pygame.time.Clock()
            
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
        
class Intro_State(Abstract_State):
    def __init__(self):
        super().__init__("intro")
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

class Place_Ship(Abstract_State):
    def __init__(self):
        super().__init__('place')
    def _build_data(self):
        link_bg = path.join("images","ocean7.jpg")
        bg = pygame.image.load(link_bg).convert_alpha()
        bg = pygame.transform.scale(bg,Hu.size)
        background = JustDraw(bg,Hu.main_panel,0,0)
        half = Panel(int(2*Hu.width/3),0,int(Hu.width/3),
                         Hu.height,(0,0,0,75),Hu.main_panel)
        board_1 = Grid(int(Hu.width/16),int(Hu.height/20),
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
        button = Button.create_image_button(int(7*Hu.width/8),int(6*Hu.height/7),
                                            Hu.width//21,Hu.width//21,
                                            (255,255,255),"Undo.png",
                                            Hu.main_panel)
        button.set_listener(Undo_Listener())
        button_1 = Button.create_image_button(int(6*Hu.width/8),
                                            int(6*Hu.height/7),
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
    def enter_state(self):
        super().enter_state()
        Hu.states.pop("intro")#t ko cần dến nó nửa
        
class Count_Down_State(Abstract_State):
    def __init__(self):
        super().__init__("Count Down State")
        self.count_down = Count_Down(Hu.width,Hu.height,Hu.main_panel)
    def _build_data(self):
        prev = Hu.states.pop('place')
        self._draw_list = prev._draw_list
        self.add_draw_list(Panel(0,0,Hu.width,Hu.height,
                                     (0,0,0,200),Hu.main_panel))
        self.add_draw_list(self.count_down)     
        b = Button.create_image_button(0,0,Hu.width//21,Hu.width//21,
                                       (255,255,255),"pause.png",Hu.main_panel)
        b.set_listener(Pause_Listener(b))
        self.add_draw_list(b)
        self.add_mouse_up(b)
        self.count_down.start()
    def draw(self):
        if(self.count_down.time_left < 0.1):
            Hu.to_change_state = True#nếu sắp hết thời gian chuyển state tiếp theo
        super().draw()
        
"""t dùng listener 1 lần thôi nên cho thẳng giá trị vô luôn nếu như vậy thì 
java có thể sử dụng anouysmous class bên python lambda expression(anouysmous 
function) lý do t chọn class bên python vì nó dễ hiểu cho bà hơn"""
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
    """zip như java iterator nhưng khi bà iter 1 list hay dict 
    thì ko cần zip, zip có thể qua 2 hoặc nhiều list cùng 1 lúc 
    kết hợp với unpack tuple cho rút ngấn code và tối ưu hơn(nếu ko tính
    dòng comment này)"""    
    def mouse_up_listener(self):
        for i,v in zip(Hu.users,Hu.ship_location):
            i.ship.x,i.ship.y = v
        for i in Hu.users:
            for j in range(5 - i.ship._num_rotate%4):
                i.ship.rotate()        
                
class Start_Battle_Listener(Listener):
    def mouse_up_listener(self):
        Hu.grid_player.grid.snap()
        if(Hu.grid_player.grid.ready()):
            Hu.to_change_state = True
        else:
            Hu.info_board.set_text("Invalid placement. Try again")
"""có thứ quan trọng class này nhắc t để chỉ"""
class Pause_Listener(Listener):
    def __init__(self,button:Button):
        self.button = button
        self.num_click = 0
        self.decorator = Image("play.png",self.button.icon.parent)
    def mouse_up_listener(self):
        temp = self.decorator#swap the icon 
        self.decorator = self.button.icon
        self.button.icon = temp
        Hu.states["Count Down State"].count_down.paused = not Hu.states["Count Down State"].count_down.paused
            
if __name__ == "__main__":
    """function"""
    Hu.run_game()
    





