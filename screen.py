# -*- coding: utf-8 -*-
"""
Created on Sun Mar 10 18:53:44 2019
3
@author: Đăng Khoa
"""
import time
from abc import ABC,abstractmethod
from os import path
from numpy.random import randint
from copy import deepcopy
import pygame
from backend import Backend

"""Interface to draw"""
class Draw():
    @abstractmethod
    def draw(self):
        pass
"""Class to draw a pygame surface"""
class JustDraw(Draw):
    def __init__(self,surface:pygame.Surface,display:pygame.display,x:int,y:int):
        self.surface = surface
        self.frame = display
        self.x = x
        self.y = y
    def draw(self):
        self.frame.blit(self.surface,(self.x,self.y))
"""Intro back ground"""
class Intro(Draw):
    def __init__(self,frame:pygame.display,width:int,height:int):
        self.tick = 0
        self.frame = frame
        self.curr = randint(4)
        self.current_ima = None
        self.size = (width,height)
    def draw(self):
        self.tick = self.tick%170
        if(self.tick == 0):
            self.curr += 1
            self.curr = self.curr%5
            link = path.join("images","intro_{:d}.jpg".format(self.curr))
            self.current_ima = pygame.image.load(link)
            self.current_ima = pygame.transform.scale(
                self.current_ima.convert_alpha(),self.size)
        self.frame.blit(self.current_ima,(0,0))
        self.tick += 1
"""Base class of object in the game """
class Icon(Draw):
    def __init__(self,x:int,y:int,length:int,height:int,
                 frame:pygame.display):
        self.x = x
        self.y = y
        self.w = length
        self.h = height
        self.frame = frame
    def mouse_on(self,mouse_pos:tuple):
        """cho bk chuột cho trên nút không"""
        if(self.x + self.w
        >=mouse_pos[0]>=self.x and self.y + self.h
        >=mouse_pos[1]>=self.y ):
            return True
        return False
"""Topping lên Icon"""
class Decorator(Icon):
    def __init__(self,icon:Icon):
        self.parent = icon
        super().__init__(icon.x,icon.y,icon.w,icon.h,icon.frame)
    def mouse_on(self,mouse_pos):
        return self.parent.mouse_on(mouse_pos)       
"""Inherted từ class Icon để base hình chữ nhật"""    
class Panel(Icon):
    def __init__(self,x,y,length,height,color:tuple,
                 frame:pygame.display):
        self.color = color
        self.surface = pygame.Surface((length,height),pygame.SRCALPHA)
        super().__init__(x,y,length,height,frame)
    def draw(self):
        self.surface.fill(self.color)
        self.frame.blit(self.surface,(self.x,self.y))  
"""Topping text on panel"""        
class Text(Decorator):
    def __init__(self,text:str,color:tuple,panel:Icon):
        super().__init__(panel)
        self.color = color
        self.text = text
        self.font =  pygame.font.Font(None,50)
    def draw(self):
        text = self.font.render(self.text,True,self.color)
        self.parent.draw()
        text = pygame.transform.scale(text,(int(0.8*self.w),int(0.8*self.h)))
        self.frame.blit(text,(int(self.x + 0.1*self.w),
                              int(self.y + 0.1*self.h))) 
    def set_font(self,font:str):
        self.font = pygame.font.Font(font,1000)
"""Topping image on panel"""
class Image(Decorator):
    def __init__(self,link:str,panel:Icon):
        super().__init__(panel)
        self.image = pygame.image.load(path.join("images",link))
        self.image = pygame.transform.scale(self.image,(panel.w,panel.h))
    def draw(self):
        self.parent.draw()
        self.frame.blit(self.image,(self.x,self.y))
"""Ship base class"""      
class Ship(Icon):
    _placed = False
    def __init__(self,link,x,y,health,frame:pygame.display):
        self.link = link
        self.ima = pygame.image.load(path.join("images",link)).convert_alpha()
        w,h = self.image.get_size()
        self._x = x
        self._y = y
        self.sink = False
        self._health = health
        self._health_left = health
        self.base_ship = self
        self._num_rotate = 0
        super().__init__(x,y,w,h,frame) 
        self.position_ship_on_grid = {}
    def set_spot_grid(self,x:int,y:int,ori:str):
        self.coor = (x,y)
        self.ori = ori
    def find_place(self,x,y):
        if(self.base_ship.ori == 'h' and self.base_ship.coor[0] == x and 
           -1<(self.base_ship.coor[1] - y) < (self.base_ship._health - 1)):
            return self.base_ship.coor[1] - y
        elif(self.base_ship.ori == 'v' and self.base_ship.coor[1] == y and 
           -1<(self.base_ship.coor[0] - x) < (self.base_ship._health - 1)):
            return self.base_ship.coor[0] - x
        else:
            return -1
    def draw(self):
        self.frame.blit(self.image,(self.x,self.y))
    def fixed(self):
        Ship._placed = True        
    def rotate(self):
        if(not Ship._placed):
            self._num_rotate += 1
            self.image = pygame.transform.rotate(self.image,90)
    def undo(self):
        Ship._placed = False
        return self
    def hit_and_update(self,section:int):
        return BuildShip.update_ship(self,section)
    def get_health(self):
        return self._health_left
    @property
    def x(self):
        return self._x
    @x.setter
    def x(self,num):
        if(not Ship._placed):
            self._x = num
    @property
    def y(self):
        return self._y
    @y.setter
    def y(self,num):
        if(not Ship._placed):
            self._y= num    
    @property
    def image(self):
        return self.ima
    @image.setter
    def image(self,image:pygame.Surface):
        self.ima = image
        self.w = self.ima.get_width()
        self.h = self.ima.get_height()
    def resize(self,y:int):
        if(self.w > self.h):
            self.image = pygame.transform.scale(self.image,
                                                (y*self.get_health(),y))
        else:
            prev = Ship._placed
            Ship._placed = False
            self.rotate()
            self.image = pygame.transform.scale(self.image,
                                                (y*self.get_health(),y))
            Ship._placed = prev
    def is_fixed(self):
        return Ship._placed
"""Base class for computer ship"""    
class Computer_ship(Ship):
    def __init__(self,link,x,y,health:int,frame:pygame.display):
        super().__init__(link,x,y,health,frame)
        self.image = pygame.Surface((self.image.get_width(),
                                     self.image.get_height()),
                                    pygame.SRCALPHA)
    def convert(self):
        ship = Ship(self.link,self.x,self.y,self.frame,self._health)
        i = 0
        while(self._num_rotate > i):
            ship.rotate()
        return ship
    @classmethod
    def make_computer(cls,ship:Ship):
        return cls(ship.link,ship.x,ship.y,ship._health,ship.frame)
    @staticmethod
    def list_ship(array:list):
        return_list = []
        for i in array:
            return_list.append(Computer_ship.make_computer(i.icon))
        return return_list
"""Decorator for ship"""        
class Ship_on_fire(Ship):
    def __init__(self,ship:Ship,section:int):
        self.section = section
        self.parent = ship 
        if(ship.w > ship.h):
            self.fire_size = (ship.h,ship.h)
        else:
            self.fire_size = (ship.w,ship.w)
        super().__init__(ship.link,ship.x,ship.y,ship._health,ship.frame)
        self.base_ship = ship.base_ship
        self._health_left = (ship.get_health() - 1)
        self.fixed()
        self.image = pygame.image.load(path.join("images","fire.png"))
        self.w = ship.w
        self.h = ship.h
    def draw(self):
        self.parent.draw()
        self.image = pygame.transform.scale(self.image,self.fire_size)
        self.w = self.parent.w
        self.h = self.parent.h
        if(self.w > self.h):
            self.frame.blit(self.image,(self.x + self.h*self.section,self.y))
        else:
            self.frame.blit(self.image,(self.x + self.h*self.section,self.y))
    def undo(self):
        return self.parent
"""Decorator for ship"""    
class Sunk(Ship):
    def __init__(self,ship:Ship):
        self.parent = ship
        super().__init__(ship.link,ship.x,ship.y,ship._health,ship.frame)
        self.image = ship.base_ship.image
        canvas = pygame.Surface((self.image.get_width(),
                                 self.image.get_height()))
        canvas.fill((224,255,255))
        canvas.blit(self.image,(0,0))
        canvas.set_alpha(125)
        self.image = canvas
        self._health_left = 0
        self._placed = True
        self.fixed()
    def undo(self):
        return self.parent
"""The base class for grid"""
class Grid(Icon):
    def __init__(self,x:int,y:int,width:int,height:int,main_panel:pygame.display):
        self.link = path.join ("images","final-0.png")
        self.grid = pygame.image.load(self.link).convert_alpha()
        super().__init__(x,y,width,height,main_panel)
        self.grid = pygame.transform.scale(self.grid,(int(self.w),int(self.h)))
        self.list_ship = []
        self._mouse_square = (-1,-1)
        self._one_square = pygame.Surface((int(self.w/10),int(self.h/10)),
                                          pygame.SRCALPHA)
        self._one_square.fill((255,255,255,200))
    def draw(self):
        self.frame.blit(self.grid,(self.x,self.y))
        if(self._mouse_square != (-1,-1)):
        	self.frame.blit(self._one_square,(int(self.x + (self.w/10)*self._mouse_square[0]),
                              int(self.y + (self.h/10)*self._mouse_square[1])))
    def add_boat(self,ship):
        self.list_ship.append(ship)
    def snap(self):
        for i in self.list_ship:
            i.x = int((i.x - self.x)/(self.w//10))*(self.w//10) + self.x
            i.y = int((i.y - self.y)/(self.h//10))*(self.h//10) + self.y
    def ready(self):
        location_ship_on_grid = {}
        for i in self.list_ship:
            x = int((i.x - self.x)/(self.w//10))
            y = int((i.y - self.y)/(self.h//10))
            if(-1< x < 10 and -1 < y < 10):
                self.snap()
            else:
                return False
            if(i.w > i.h):
                location_ship_on_grid[str.split(i.link,".")[0]]= (y,x,'h')
                i.set_spot_grid(x,y,'h')
            else:
                location_ship_on_grid[str.split(i.link,".")[0]] = (y,x,'v') 
                i.set_spot_grid(x,y,'v')
        if(Backend.set_user_ship(location_ship_on_grid)):
            i.fixed()
            #Backend.set_computer_ship()
            return True
        Backend.start_game()
        return False
    
    def set_hit(self,x:int,y:int):
        pass
class BuildShip():
    @staticmethod
    def update_ship(ship:Ship,location:int):
        health = (ship.get_health() - 1)
        if(health == 0):
            if(isinstance(ship.base_ship,Computer_ship)):
                ship.base_ship = ship.base_ship.convert()
            return Sunk(ship)
        else:
            return Ship_on_fire(ship,location)
    @staticmethod
    def build_user_ship(Width,Height,board:Grid,
                        main_panel:pygame.display):
        magic_num = 1
    
        patrol = Ship("Patrol Boat.png",int(5*Width//7),int(Height//10),2,main_panel)
        patrol.rotate()
        patrol.resize(int(magic_num*board.w/10))
        
        destroyer = Ship("Destroyer.png",
                         int(5*Width//7),int(2.75*Height//10),3,main_panel)
        destroyer.rotate()
        destroyer.resize(int(magic_num*board.w/10))
        
        battle_ship = Ship("Battleship.png",
                           int(5*Width//7),int(4.5*Height//10),5,main_panel)
        battle_ship.rotate()
        battle_ship.resize(int(magic_num*board.w/10))
        
        air_carrier = Ship("Aircraft Carrier.png",
                           int(5*Width//7),int(6*Height//10),4,main_panel)
        air_carrier.rotate()
        air_carrier.resize(int(magic_num*board.w/10))
        
        sub = Ship("Submarine.png",
                   int(5*Width//7),int(7.75*Height//10),3,main_panel)
        sub.rotate()
        sub.resize(int(magic_num*board.w/10))
        
        return [patrol,destroyer,battle_ship,air_carrier,sub]        
"""Event handling"""
class Event(Draw):
    def __init__(self,icon:Icon):
        self.icon = icon
        self.click = False
        self.key = False
    @abstractmethod
    def mouse_hover(self,mouse_pos):
        pass
    @abstractmethod
    def mouse_down(self,mouse_pos):
        pass
    @abstractmethod
    def mouse_up(self,mouse_pos):
        pass
    @abstractmethod
    def key_r(self,mouse_pos):
        pass
    
class Interactive_Ship(Event):
    to_move = None
    def __init__(self,ship:Ship):
        self.hover = False
        panel = Panel(0,0,int(ship.h*3),int(ship.h/1.6),
                      (255,255,255),ship.frame)
        self.text_field = Text("",(0,0,0),panel)
        super().__init__(ship)
        self.ship = self.icon
    def mouse_down(self,mouse_pos):
        if(((self.ship.mouse_on(mouse_pos) and not self.click) 
        or self.click) and (Interactive_Ship.to_move == None 
                     or Interactive_Ship.to_move == self)):
            self.ship.x = (mouse_pos[0] - self.ship.w/2)
            self.ship.y = (mouse_pos[1] - self.ship.h/2)
            self.click = True
            Interactive_Ship.to_move = self
        self.hover = False
    def mouse_up(self,mouse_pos):
        if(self.ship.mouse_on(mouse_pos)):
            self.click = False
        self.hover = False
        Interactive_Ship.to_move = None
    def mouse_hover(self,mouse_pos):
        if(self.ship.mouse_on(mouse_pos)):
            self.hover = True
        else:
            self.hover = False
    def key_r(self,mouse_pos):
        if(self.ship.mouse_on(mouse_pos)):
            self.ship.rotate()
    def draw(self):
        self.ship.draw()
        if(self.hover):
            self.text_field.parent.x = self.ship.x + self.ship.w//2
            self.text_field.parent.y = self.ship.y + self.ship.h//2
            self.text_field.x = self.ship.x + self.ship.w//2
            self.text_field.y = self.ship.y + self.ship.h//2            
            if(not self.ship.is_fixed()):
                self.text_field.text = "Press R to rotate"
            else:
                self.text_field.text = "Health left {:d}".format(self.ship.get_health())
            self.text_field.draw()
            
class Interactive_Board(Event):
    def __init__(self,grid:Grid):
        super().__init__(grid)
        self.grid = grid
        self.first = False
    def mouse_hover(self,mouse_pos):
        if(self.grid.mouse_on(mouse_pos)):
            self.grid._mouse_square =  (int((mouse_pos[0] - 
                                           self.grid.x)/(self.grid.w/10)),
                                  int((mouse_pos[1] - 
                                       self.grid.y)/(self.grid.w/10)))
        if(self.grid._mouse_square[0] == 10 or 
           self.grid._mouse_square[1] == 10 or not 
           self.grid.mouse_on(mouse_pos)):
            self.grid._mouse_square = (-1,-1)
    def draw(self):
        self.grid.draw()

class Player_Board(Draw):
    def __init__(self,board:Grid):
        self.board = board
        self.fire =  pygame.image.load(path.join("images","fire.png"))
    def draw(self):
        self.board.draw()
        for i in self.board.list_ship:
            i.draw()
        for i,v in Backend.computer_hits.items():
            if(v):
                self.board.frame.blit(pygame.transform.scale(self.fire,(self.board.h//10,
                                                                        self.board.h//10)),
                                      (self.board.x + i[1]*self.board.h//10,
                                             self.board.y + i[0]*self.board.h//10))
    def set_board(self,board:Grid):
        self.board = board
    
class Computer_Board(Event):
    def __init__(self,grid:Grid):
        super().__init__(grid)
        self.target = pygame.image.load(path.join("images",'1b.png'))
        self.target = pygame.transform.scale(self.target,
                                             (self.icon.h//10,self.icon.w//10))
        self.find_spot = True
        self.spot = (self.icon.x,self.icon.y)
        self.fire = False
        self.fire_location = None
        self.shell_land = None
    def receive_ship(self,ships:list,location:dict):
        pass
    def mouse_hover(self,mouse_pos:tuple):
        if(self.icon.mouse_on(mouse_pos)):
            self.find_spot = True
            self.spot = mouse_pos
        else:
            self.find_spot = False
    def mouse_up(self,mouse_pos:tuple):
        if(self.icon.mouse_on(mouse_pos)):
            self.fire = True
            x = 10*(self.spot[0]-self.icon.x)//self.icon.h
            y = 10*(self.spot[1]-self.icon.y)//self.icon.w
            if(x == 10):
                x = 9
            if(y == 10):
                y = 9
            self.fire_location = (x,y)
            self.shell_land = ()
    def draw(self):
        if(self.find_spot):
            self.icon.frame.blit(self.target,(self.spot[0] - self.icon.h//20,
                                              self.spot[1] - self.icon.h//20))

class Listener():
    @abstractmethod
    def mouse_up_listener(self):
        pass
    @abstractmethod
    def mouse_down_listener(self):
        pass
    @abstractmethod
    def mouse_hover_listener(self):
        pass
    @abstractmethod
    def not_mouse_on_listener(self):
        pass#có lý do cho thằng này tồn tại
    @abstractmethod
    def key_r_listner(self):
        pass
    def draw(self):
        pass
     
class Button(Event):
    def __init__(self,base:Decorator): #lý do m cần overwrite constructor
        super().__init__(base) #làm vì Decorator là subclass của Icon
    def set_listener(self,listener:Listener):
        self.listener = listener
    def mouse_hover(self,mouse_pos:tuple):
        try:
            if(self.icon.mouse_on(mouse_pos)):
                self.listener.mouse_hover_listener()
            else:
                self.listener.not_mouse_on_listener()
        except Exception as e:
            print(str(e))
    def mouse_down(self,mouse_pos:tuple):
        if(self.icon.mouse_on(mouse_pos)):
            try:
                self.listener.mouse_down_listener()
            except Exception as e:
                print(str(e))        
    def mouse_up(self,mouse_pos:tuple):
        if(self.icon.mouse_on(mouse_pos)):
            try:
                self.listener.mouse_up_listener()
            except Exception as e:
                print(str(e))         
    def draw(self):
        self.icon.draw()
        self.listener.draw()
    @classmethod
    def create_text_button(cls,x:int,y:int,length:int,height:int,text:str,
                         color_bg:tuple,color_txt:tuple,frame:pygame.display):
        p = Panel(x,y,length,height,color_bg,frame)
        text = Text(text,color_txt,p)
        return cls(text)
    @classmethod
    def create_image_button(cls,x:int,y:int,length:int,height:int,color:tuple,
                            link:str,frame:pygame.display):
        p = Panel(x,y,length,height,color,frame)
        i = Image(link,p)
        return cls(i)

class Info(Draw):
    def __init__(self,x:int,y:int,w:int,h:int,frame:pygame.display):
        self.base_panel = Panel(x,y,w,h,(0,0,0),frame)
        self.text = ["",""]
        self.font = pygame.font.Font(None,50)
        self.frame = frame
        self.color = (0,205,0)
    def draw(self):
        self.base_panel.draw()
        for i,v in zip(self.text,(0,1)):
            text = self.font.render(i,True,self.color)
            ratio = (self.base_panel.h/text.get_height())
            text = pygame.transform.scale(text,(int(ratio*0.7*text.get_width())//2,
                                            int(0.7*ratio*text.get_height())//2))
            self.frame.blit(text,(self.base_panel.w//2 + self.base_panel.x - 
                              text.get_width()//2
                ,int(self.base_panel.y + (v/2 + 0.15)*self.base_panel.h)))
        
    def set_text(self,text:str):
        self.text.append(text)
        self.text.pop(0)
"""Count Down class"""
class Count_Down(Draw):
    def __init__(self,width:int,height:int,frame:pygame.display):
        self.duration = 4
        self.paused = False
        self.time_left = 4
        self.curr_index = 3 #dùng để tối ưu chương trình
        self.pic = pygame.image.load(path.join("images","3.png"))
        self.pic = pygame.transform.scale(self.pic,(int(0.4*height),
                                                    int(0.4*height)))
        self.size = (width,height)
        self.frame = frame
    def start(self):
        self.start_time = time.time()
    def draw(self):
        curr = time.time()               
        if(self.paused):
            self.start_time = curr#có thê cải thiện hơn
        self.time_left = self.duration-(curr-self.start_time)
        
        if(int(self.time_left) != self.curr_index and 0 < self.time_left < 4):
            self.curr_index = int(self.time_left)
            self.pic = pygame.image.load(path.join("images",
                                        "{:d}.png".format(self.curr_index)))
            self.pic = pygame.transform.scale(self.pic,
                                (int(0.4*self.size[1]),int(0.4*self.size[1])))
        self.frame.blit(self.pic,(int(self.size[0])*(1/2 - 0.1),
                                  int(self.size[1])*(1/2 - 0.2)))
        
class Winner(Draw):
    def __init__(self,width:int,height:int,frame:pygame.display):
        self.pic = pygame.image.load(path.join("images","win.jpg"))
        self.pic = pygame.transform.scale(self.pic,(width,height))
        self.frame = frame
        self.ratio = 3.72
        self.score = 0
        other = pygame.image.load(path.join("images","won.png"))
        self.pic.blit(
                pygame.transform.scale(other,(int(3.72*width//9),width//9)),
                (width//12,width//25))
    def draw(self):
        self.frame.blit(self.pic,(0,0))
    def set_score(self,num:int):
        self.score = num
        
class Loser(Draw):
    def __init__(self,width:int,height:int,frame:pygame.display):
        self.pic = pygame.image.load(path.join("images","lost.jpg"))
        self.pic = pygame.transform.scale(self.pic,(width,height))
        self.frame = frame
        self.ratio = 4
        self.score = 0
        other = pygame.image.load(path.join("images","lost.png"))
        self.pic.blit(
                pygame.transform.scale(other,(int(4*width//9),width//9)),
                (width//12,width//25))
    def draw(self):
        self.frame.blit(self.pic,(0,0))        
        
class Shell(Icon):
    def __init__(self,width:int,height:int,frame:pygame.display):
        self.proto = pygame.image.load(path.join("images","bullet1.png"))
        self.shell = pygame.transform.scale(self.proto,
                                            (int(8*height//(21*3)),
                                             height//21))
        super().__init__(0,0,int(8*height//(21*3)),height//21,frame)
        self.angle = 0
    def draw(self):      
        self.frame.blit(self.shell,(self.x,self.y))
    def rotate(self,angle:int):
        self.shell = pygame.transform.rotate(self.shell,angle)
        self.angle = angle
    def reset(self):
        self.shell = pygame.transform.scale(self.proto,(self.w,self.h))

class Missile(Icon):
    def __init__(self,width:int,height:int,frame:pygame.display):
        self.proto = pygame.image.load(path.join("images","Missile04N.png"))
        self.shell = pygame.transform.scale(self.proto,
                                            (int(8*height//(21*3)),
                                             height//7))
        super().__init__(0,0,int(8*height//(21*3)),height//7,frame)
        self.angle = 0
    def draw(self):      
        self.frame.blit(self.shell,(self.x,self.y))
    def rotate(self,angle:int):
        self.shell = pygame.transform.rotate(self.shell,angle)
        self.angle = angle
    def reset(self):
        self.shell = pygame.transform.scale(self.proto,(self.w,self.h))
        
class Effect_Board(Draw):
    def __init__(self,grid:Grid):
        self.grid = grid
        self.location = []
        self.splash = pygame.image.load(path.join("images","water-splash.png"))
        self.fire = pygame.image.load(path.join("images","fire.png"))
        self.cross = pygame.image.load(path.join("images","cancel.png"))
        self.image_ship = []
    def set_grid(self,grid:Grid):
        self.grid = grid
    def set_location(self,loc:tuple):
        self.location.append(loc)
    def reset(self):
        self.location.clear()
    def draw(self):
        a = Backend.check()
        if(a != None):
            self.image_ship.append(Ship(a[0] + ".png",
                                        self.grid.x + a[1][1]*self.grid.h//10,
                                        self.grid.y + a[1][0]*self.grid.h//10,
                                        self.grid.frame))
            if(a[1][2] == 'h'):
                self.image_ship[len(self.image_ship) - 1].rotate()
        for i in self.image_ship:
            i.draw()
        for i,v in Backend.player_hits.items():
            if(v):
                self.grid.frame.blit(pygame.transform.scale(self.fire,
                (self.grid.h//10,self.grid.h//10)),
                (self.grid.x + i[1]*self.grid.h//10,
                 self.grid.y + i[0]*self.grid.h//10))  
            else:
                self.grid.frame.blit(pygame.transform.scale(self.cross,
                (self.grid.h//10,self.grid.h//10)),
                (self.grid.x + i[1]*self.grid.h//10,
                 self.grid.y + i[0]*self.grid.h//10))  
        for i in self.location:
            if(i[0] < 0 or i[0] > 9 or i[1] < 0 or i[1] > 9):
                continue
            else:
                if(not Backend.user_hit_at(i[1],i[0])):
                    self.grid.frame.blit(pygame.transform.scale(self.splash,
                    (self.grid.h//10,self.grid.h//10)),
                    (self.grid.x + i[0]*self.grid.h//10,
                     self.grid.y + i[1]*self.grid.h//10))
                else:
                    self.grid.frame.blit(pygame.transform.scale(self.fire,
                    (self.grid.h//10,self.grid.h//10)),
                    (self.grid.x + i[0]*self.grid.h//10,
                     self.grid.y + i[1]*self.grid.h//10))                    

class Score_Board(Icon):
    def __init__(self,x:int,y:int,width:int,height:int,frame:pygame.display):
        super().__init__(x,y,width,height,frame)
        self.panel = pygame.Surface((self.w,self.h),pygame.SRCALPHA)
        self.panel.fill((0,0,0,150))
    def draw(self):
        font = pygame.font.Font(None,50)
        text = font.render("Human",True,(255,255,255))        
        text = pygame.transform.scale(text,(int(0.25*self.w),int(0.2*self.h)))
        a = Backend.get_score()
        self.frame.blit(self.panel,(self.x,self.y))        
        self.frame.blit(text,(int(self.x + 0.1*self.w),
                              int(self.y + 0.1*self.h)))
        text = font.render(str(a[1]),True,(255,255,255))     
        if(a[1] > 10):
            text = pygame.transform.scale(text,(int(0.15*self.w),
                                                int(0.2*self.h)))
        else:
            text = pygame.transform.scale(text,(int(0.05*self.w),
                                            int(0.2*self.h)))
        self.frame.blit(text,(int(self.x + 0.13*self.w),
                        int(self.y + 0.5*self.h)))
        text = font.render(str(a[0]),True,(255,255,255)) 
        if(a[0] > 10):
            text = pygame.transform.scale(text,(int(0.13*self.w),
                                                int(0.2*self.h)))
        else:
            text = pygame.transform.scale(text,(int(0.05*self.w),
                                            int(0.2*self.h))) 
        self.frame.blit(text,(int(self.x + 0.7*self.w),
                        int(self.y + 0.5*self.h)))            
        text = font.render("AI",True,(255,255,255))        
        text = pygame.transform.scale(text,(int(0.1*self.w),int(0.2*self.h)))        
        self.frame.blit(text,(int(self.x + 0.68*self.w),
                              int(self.y + 0.1*self.h))) 
   
class Event_Subject():
    def __init__(self):
        self._mouse_hover = []
        self._mouse_down = []
        self._mouse_up = []
        self._key_r = []
        self._draw_list = []
    """Add subscribers"""        
    def add_mouse_up(self,event:Event):
        self._mouse_up.append(event)
    def add_mouse_down(self,event:Event):
        self._mouse_down.append(event)
    def add_mouse_hover(self,event:Event):
        self._mouse_hover.append(event)
    def add_key_r(self,event:Event):
        self._key_r.append(event)
    def add_draw_list(self,draw:Draw):
        self._draw_list.append(draw)
    """Notify subscribers"""
    def notify_mouse_down(self,mouse_pos):
        for i in self._mouse_down:
            i.mouse_down(mouse_pos)
    def notify_mouse_up(self,mouse_pos):
        for i in self._mouse_up:
            i.mouse_up(mouse_pos)
    def notify_mouse_hover(self,mouse_pos):
        for i in self._mouse_hover:
            i.mouse_hover(mouse_pos)
    def notify_key_r(self,mouse_pos):
        for i in self._key_r:
            i.key_r(mouse_pos)
    def draw(self):
        for i in self._draw_list:
            i.draw()
    def clear_all(self):
        self._mouse_hover = []
        self._mouse_down = []
        self._mouse_up = []
        self._key_r = []
        self._draw_list = []