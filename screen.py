# -*- coding: utf-8 -*-
"""
Created on Sun Mar 10 18:53:44 2019
3
@author: Đăng Khoa
"""
import pygame
from abc import ABC,abstractmethod
from os import path
from numpy.random import randint
"""Interface to draw"""
class Draw():
    @abstractmethod
    def draw():
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
        self.tick = self.tick%200
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
    def __init__(self,x:int,y:int,length:int,height:int,frame:pygame.display):
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
    def __init__(self,x,y,length,height,color:tuple,frame:pygame.display):
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
    def draw(self):
        font = pygame.font.Font(None,1000)
        text = font.render(self.text,True,self.color)
        self.parent.draw()
        text = pygame.transform.scale(text,(int(0.8*self.w),int(0.8*self.h)))
        self.frame.blit(text,(int(self.x + 0.1*self.w),
                              int(self.y + 0.1*self.h)))  
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
    def __init__(self,link,x,y,frame,health):
        self.link = link
        self.ima = pygame.image.load(link).convert_alpha()
        w,h = self.image.get_size()
        self._placed = False
        self._x = x
        self._y = y
        self.sink = False
        self._health = health
        self._health_left = health
        self.base_ship = self
        self._num_rotate = 0
        super().__init__(x,y,w,h,frame) 
    def draw(self):
        self.frame.blit(self.image,(self.x,self.y))
    def fixed(self):
        self._placed = True        
    def rotate(self):
        if(not self._placed):
            self._num_rotate += 1
            self.image = pygame.transform.rotate(self.image,90)
    def undo(self):
        self._placed = False
        return self
    def hitandupdate(self,section:int):
        return BuildShip.update_ship(self,section)
    def get_health(self):
        return self._health_left
    @property
    def x(self):
        return self._x
    @x.setter
    def x(self,num):
        if(not self._placed):
            self._x = num
    @property
    def y(self):
        return self._y
    @y.setter
    def y(self,num):
        if(not self._placed):
            self._y= num    
    @property
    def image(self):
        return self.ima
    @image.setter
    def image(self,image:pygame.Surface):
        self.ima = image
        self.w = self.ima.get_width()
        self.h = self.ima.get_height()
    def set_fire_location(self,location):
        pass
    def resize(self,y:int):
        if(self.x > self.y):
            self.image = pygame.transform.scale(self.image,
                                                (y*self.get_health(),y))
        else:
            prev = self._placed
            self._placed = False
            self.rotate()
            self.image = pygame.transform.scale(self.image,
                                                (y*self.get_health(),y))
            self._placed = prev
    def is_fixed(self):
        return self._placed
"""Base class for computer ship"""    
class Computer_ship(Ship):
    def __init__(self,link,x,y,frame,health):
        super().__init__(link,x,y,frame,health)
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
        return cls(ship.link,ship.x,ship.y,ship.frame,ship._health)
    def list_ship(cls,array:list):
        return_list = []
        for i in array:
            return_list.append(Computer_ship.make_computer(i))
        return return_list
"""Decorator for ship"""        
class Ship_on_fire(Ship):
    def __init__(self,ship:Ship,section:int):
        self.parent = ship 
        self.offset_1 = 0
        self.offset_2 = 0
        self.fire_size = (35,45)
        super().__init__(ship.link,ship.x,ship.y,ship.frame,ship._health) 
        self.base_ship = ship.base_ship
        self._health_left = (ship.get_health() - 1)
        self._placed = True
        self.image = pygame.image.load(path.join("images","fire.png"))
    def draw(self):
        self.parent.draw()
        self.image = pygame.transform.scale(self.image,self.fire_size)
        self.frame.blit(self.image,(self.x,self.y))
    def undo(self):
        return self.parent
"""Decorator for ship"""    
class Sink(Ship):
    def __init__(self,ship:Ship):
        self.parent = ship
        super().__init__(ship.link,ship.x,ship.y,ship.frame,ship._health)
        self.image = ship.base_ship.image
        canvas = pygame.Surface((self.image.get_width(),
                                 self.image.get_height()))
        canvas.fill((224,255,255))
        canvas.blit(self.image,(0,0))
        canvas.set_alpha(200)
        self.image = canvas
        self._health_left = 0
        self._placed = True
    def undo(self):
        return self.parent
class BuildShip():
    @staticmethod
    def update_ship(ship:Ship,location:int):
        health = (ship.get_health() - 1)
        if(health == 0):
            if(isinstance(ship.base_ship,Computer_ship)):
                ship.base_ship = ship.base_ship.convert()
            return Sink(ship)
        else:
            return Ship_on_fire(ship,location)
    @staticmethod
    def build_user_ship(Width,Height,main_panel,board):
        link = path.join("images","patrol.png")
        patrol = Ship(link,int(5*Width//7),int(Height//10),main_panel,2)
        patrol.rotate()
        patrol.resize(int(0.92*board.w/10))  
        link = path.join("images","destroyer.png")
        destroyer = Ship(link,int(5*Width//7),int(2.5*Height//10),main_panel,3)
        destroyer.rotate()
        destroyer.resize(int(0.92*board.w/10))  
        link = path.join("images","battleship.png")
        battle_ship = Ship(link,int(5*Width//7),int(4*Height//10),main_panel,5)
        battle_ship.rotate()
        battle_ship.resize(int(0.92*board.w/10))      
        link = path.join("images","carrier.png")
        air_carrier = Ship(link,int(5*Width//7),int(5.5*Height//10),main_panel,4)
        air_carrier.rotate()
        air_carrier.resize(int(0.92*board.w/10))
        link = path.join("images","submarine.png")
        sub = Ship(link,int(5*Width//7),int(7*Height//10),main_panel,3)
        sub.rotate()
        sub.resize(int(0.92*board.w/10))
        return [patrol,destroyer,battle_ship,air_carrier,sub]        
"""The base class for grid"""
class Grid(Icon):
    def __init__(self,x,y,width,height,main_panel):
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
             self.frame.blit(self._one_square,
                             (int(self.x + (self.w/11)*self._mouse_square[0]),
                              int(self.y + (self.h/11)*self._mouse_square[1])))
    def add_boat(self,ship):
        self.list_ship.append(ship)
    @abstractmethod
    def square(self,coor:tuple):
        pass
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
                                           self.grid.x)/(self.grid.w/11)),
                                  int((mouse_pos[1] - 
                                       self.grid.y)/(self.grid.w/11)))
        if(self.grid._mouse_square[0] == 11 or 
           self.grid._mouse_square[1] == 11 or not 
           self.grid.mouse_on(mouse_pos)):
            self.grid._mouse_square = (-1,-1)
                           
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
    """chuyển cảnh"""
    def clear_scene(self):
        self._mouse_up.clear()
        self._mouse_hover.clear()
        self._mouse_down.clear()
        self._key_r.clear()
        self._draw_list.clear()