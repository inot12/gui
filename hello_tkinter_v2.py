#! usr/local/bin/python3
'''
Created on May 21, 2019

@author:toni
'''

import tkinter as tk
import tkinter.messagebox as msgbox


class Window(tk.Tk):

    def __init__(self):
        # We created Window as a subclass of tk.Tk, so super().init() ensures
        # we inherit all the tk.Tk class attributes.
        super().__init__()
        self.title("Hello Tkinter")

        self.label_text = tk.StringVar()
        self.label_text.set("Choose One")
        self.label = tk.Label(self, text=self.label_text.get())
        self.label.pack(fill=tk.BOTH, expand=1, padx=100, pady=30)

        # hello button command definition and positioning.
        hello_button = tk.Button(self, text="Say Hello",
                                 command=self.say_hello)
        hello_button.pack(side=tk.LEFT, padx=(20, 0), pady=(0, 20))

        goodbye_button = tk.Button(self, text="Say Goodbye",
                                   command=self.say_goodbye)
        goodbye_button.pack(side=tk.RIGHT, padx=(0, 20), pady=(0, 20))

    def say_hello(self):
        # Initialize a new window that says hello world.
        msgbox.showinfo("Hello", "Hello World!")

    def say_goodbye(self):
        close = msgbox.askyesno("Close Window?",
                                "Would you like to close this window?")
        if close:
            # self.destroy() immediately closes the window.
            self.after(500, self.destroy)  # 0.5 s delay before closing.

# =============================================================================
# Useful methods that should be used with
# msgbox.method('box_title', 'box_message')
# askquestion
# askyesno
# askokcancel
# askretrycancel
# =============================================================================


def main():
    window = Window()
    window.mainloop()


if __name__ == '__main__':
    main()
