# -*- coding: utf-8 -*-
"""
Created on Sun Mar 10 18:53:44 2019

@author: Đăng Khoa
"""

import tkinter as tk
""" tìm độ phân giải của màn hình """
def get_screen_info():
    root = tk.Tk()
    Screen_Width = root.winfo_screenwidth()
    Screen_Height = root.winfo_screenheight()
    return (Screen_Width,Screen_Height)
"""setup độ phân giải tối ưu cho từng máy"""
def prefer_size():
    Screen_Width,Screen_Height = get_screen_info()
    aspect_ratio = Screen_Width/Screen_Height
    if(aspect_ratio >= 1.778):
        Prefer_Height = int(Screen_Height*0.8)
        Prefer_Width = int(Prefer_Height/9)*16      
    else:
        Prefer_Width = int(Screen_Width*0.8)
        Prefer_Height = int(Prefer_Width/16)*9
    return (Prefer_Width,Prefer_Height)

        