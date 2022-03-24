#! usr/local/bin/python3
'''
Created on May 17, 2019

@author:toni
'''

import tkinter as tk
from tkinter import ttk  # used for modern, better looks


def main():
    root = tk.Tk()
    label = tk.Label(root, text='Hello World')
    label.pack()
    button = tk.Button(root, text='Button 1')
    button.pack()
    entry = tk.Entry(root)
    entry.pack()
    root.mainloop()


if __name__ == '__main__':
    main()
