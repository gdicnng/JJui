# -*- coding: utf_8_sig-*-
import tkinter as tk
from tkinter import ttk

# self.new_ui_
# self.new_var_
# self.new_func_

class Text_with_scrollbar(ttk.Frame):
    def __init__(
                self,
                parent,
                *args,
                wrap=tk.NONE,
                horizontal=False,
                sizegrip=False,
                state="disabled",
                **kwargs
            ):
        super().__init__(parent,*args,**kwargs)
        
        self.new_var_wrap  = wrap
        self.new_var_state = state
        self.new_var_flag_horizontal = horizontal
        self.new_var_flag_sizegrip   = sizegrip
            # if horizontal 滚动条
                # if sizegrip
                    # ttk.sizegrip 添加到右下角
        
        
        self.new_func_ui()
        
    def new_func_ui(self,):
        parent=self
        
        parent.rowconfigure(0, weight=1)
        parent.columnconfigure(0, weight=1)
        parent.columnconfigure(1, weight=0)
        
        self.new_ui_text = tk.Text(
                    parent,
                    undo=False,
                    borderwidth = 0,
                    highlightthickness = 0,
                    takefocus=False,
                    state=self.new_var_state,
                    wrap=self.new_var_wrap,
                    )
        self.new_ui_scrollbar_v = ttk.Scrollbar( parent, orient=tk.VERTICAL, command=self.new_ui_text.yview)
        
        self.new_ui_text.configure(yscrollcommand=self.new_ui_scrollbar_v.set)
        
        self.new_ui_text.grid(row=0,column=0,sticky=tk.N+tk.S+tk.E+tk.W,)
        self.new_ui_scrollbar_v.grid(row=0,column=1,sticky=tk.N+tk.S,)
        
        if self.new_var_flag_horizontal:
            
            parent.rowconfigure(1, weight=0)
            
            self.new_ui_scrollbar_h = ttk.Scrollbar( parent, orient=tk.HORIZONTAL , command=self.new_ui_text.xview)
            
            self.new_ui_text.configure(xscrollcommand=self.new_ui_scrollbar_h.set)
            
            self.new_ui_scrollbar_h.grid(row=1,column=0,sticky=tk.W+tk.E,)
            
            if self.new_var_flag_sizegrip :
                self.new_ui_sizegrip = ttk.Sizegrip(parent)
                self.new_ui_sizegrip.grid(row=1,column=1,sticky=tk.E,)
    
    def new_func_insert_string(self,a_string=''):
        self.new_ui_text.configure(state="normal")
        
        self.new_ui_text.insert(tk.END,a_string)
        
        self.new_ui_text.configure(state="disabled")

    def new_func_insert_window(self,text_index,window):
        self.new_ui_text.configure(state="normal")
        
        self.new_ui_text.window_create(text_index,window=window)
        
        self.new_ui_text.configure(state="disabled")

if __name__ == "__main__" :
    
    root=tk.Tk()
    root.geometry('800x600')
    root.rowconfigure(0,weight=1)
    root.columnconfigure(0,weight=1)
    

    
    #a=Text_with_scrollbar(root)
    a=Text_with_scrollbar(root,horizontal=True,sizegrip=False)
    a.grid(row=0,column=0,sticky=tk.W+tk.N+tk.E+tk.S,)
    
    text = a.new_ui_text
    for x in range(1000):
        a.new_func_insert_string(str(x) + " : "+"test\n") 
    
    root.mainloop()



