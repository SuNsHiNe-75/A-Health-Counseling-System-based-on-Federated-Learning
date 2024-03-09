from tkinter import *
from tkinter import ttk

gui=Tk()
gui.title('Serlizing Data')
gui.geometry('600x100')

def StartProgress():
    # start progress
    progress_var.start(10)

def StopProgress():
    # stop progress
    progress_var.stop()
# create an object of progress bar
progress_var=ttk.Progressbar(gui,orient=HORIZONTAL, style="red.Horizontal.TProgressbar",length=400,mode='indeterminate')
progress_var.pack(pady=30)
StartProgress()
gui.mainloop()