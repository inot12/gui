#! usr/local/bin/python3
'''
Created on May 20, 2019

@author:toni
'''

import tkinter as tk


class Window(tk.Tk):
    """Create a subclass of the tk.Tk class."""

    def __init__(self):
        super().__init__()
        self.title("Hello Tkinter")

        label = tk.Label(self, text="Hello World!")
        label.pack(fill=tk.BOTH, expand=1, padx=100, pady=50)

        self.label = tk.Label(self, text="Choose One")
        self.label.pack(fill=tk.BOTH, expand=1, padx=100, pady=30)

        hello_button = tk.Button(self, text="Say Hello",
                                 command=self.say_hello)
        hello_button.pack(side=tk.LEFT, padx=(20, 0), pady=(0, 20))

        goodbye_button = tk.Button(self, text="Say Goodbye",
                                   command=self.say_goodbye)
        goodbye_button.pack(side=tk.RIGHT, padx=(0, 20), pady=(0, 20))

    def say_hello(self):
        # .configure() changes the attributes of widgets.
        self.label.configure(text="Hello World!")

    def say_goodbye(self):
        self.label.configure(text="Goodbye! \n (Closing in 2 seconds)")
        # .after() method calls a piece of code after time in milliseconds.
        self.after(2000, self.destroy)


def main():
    window = Window()
    window.mainloop()


if __name__ == '__main__':
    main()
