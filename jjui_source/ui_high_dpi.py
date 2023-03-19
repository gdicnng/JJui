# -*- coding: utf_8_sig-*-
import sys
import ctypes
# import re

def high_dpi_0(root):
    print("high dpi not set")

def high_dpi_1(root):
    # Windows Vista, 7, 8 and Server 2012
    ctypes.windll.user32.SetProcessDPIAware() 
    print(r"ctypes.windll.user32.SetProcessDPIAware()")

def high_dpi_2(root):
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
    print(r"ctypes.windll.shcore.SetProcessDpiAwareness(1)")

def high_dpi_3(root):
    ctypes.windll.shcore.SetProcessDpiAwareness(2)
    print(r"ctypes.windll.shcore.SetProcessDpiAwareness(2)")

#   https://zhuanlan.zhihu.com/p/162164360
def high_dpi_4(root):
    #   https://zhuanlan.zhihu.com/p/162164360
    # ctypes.windll.shcore.SetProcessDpiAwareness(2)
    # 仅可在win8.1版本及以上使用，并且微软建议使用SetThreadDpiAwarenessContext
    
    #try:  # >= win 8.1
    #    ctypes.windll.shcore.SetProcessDpiAwareness(2)
    #except:  # win 8.0 or less
    #    ctypes.windll.user32.SetProcessDPIAware()
    ctypes.windll.shcore.SetProcessDpiAwareness(2)
    ScaleFactor = ctypes.windll.shcore.GetScaleFactorForDevice(0)
    root.tk.call('tk', 'scaling', ScaleFactor/75)
    
    print(r"ctypes.windll.shcore.SetProcessDpiAwareness(2)")
    print(r"tk scaling")

# 另外
#   hdpitkinter
#   https://pypi.org/project/hdpitkinter
#   MIT License


def main(root,number):
    if not sys.platform.startswith('win32'):
        return
    
    high_dpi = high_dpi_0
    
    if   number == 1 : high_dpi = high_dpi_1
    elif number == 2 : high_dpi = high_dpi_2
    elif number == 3 : high_dpi = high_dpi_3
    elif number == 4 : high_dpi = high_dpi_4
    
    print()
    print("high dpi")
    print(number)
    
    try:
        high_dpi(root)
        #print(number)
    except:
            pass

# https://learn.microsoft.com/zh-cn/windows/win32/hidpi/high-dpi-desktop-application-development-on-windows?redirectedfrom=MSDN
# ？？？？？？？？？？？？？？