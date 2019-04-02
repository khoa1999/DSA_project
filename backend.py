#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 28 16:03:56 2019

@author: hodangphuongngoc

"""
import DSA_Battleship

"""input toa do chay tu 0"""

class Backend():
    
    
    # goi nhi class
    counter = 0 #dummy variable for front-end without backend
    
    
    @staticmethod
    def start_game():
        """ put sth in here hihi"""
        pass
    
    
    @staticmethod
    def call_place_computer_ship():
        
        """ tra ve dict{chữ cái đầu tên thuyền:value}
       trong value : list có ba giá trị  [x,y,v/h]
       index từ 0 """
       return  { "B" : [0,0,"v"]}
  
    @staticmethod
    def call_set_user_ship(boatname:str,x:int,y:int,direction:str):
    
        return True
    
    
    @staticmethod
    def check_win():
        
        """tra ve win theo format [bool,bool]
        false,true : computer win
        true,false: user win 
        false, false : 
        """
        if(Backend.counter == 20):
            return [False,True]
        else:
            Backend.counter+=1
            return [False,False]
    
    @staticmethod
    def call_hit(x:int,y:int):
        
        """ tra ve cho backend vi tri thuyen bi bắn"""
        pass 
    

    @staticmethod
    def call_undo():
        pass
    
     @staticmethod   
    def call_redo():
        pass
    
    
    
    
        
    
    
        
    
        
        
        
        
        
        
        
    
    