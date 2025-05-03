from tkinter import *
import tkinter as tk
from agregar import Agregar
from actualizar import Actualizar
import sys
import os

class Container(tk.Frame):
    def __init__(self, padre, controlador):
        super().__init__(padre)
        self.controlador = controlador
        self.pack()
        self.place(x=0, y=0,width=1100, height=650)
        self.widgets()
        self.frames = {}
        self.buttons = []
        for i in (Agregar, Actualizar):
            frame = i(self)
            self.frames[i] = frame
            frame.pack()
            frame.config(bg= "gray", highlightbackground= "gray", highlightthickness=1)
            frame.place(x=0, y=40, width= 1100, height= 610)
        self.show_frames(Agregar)


    def show_frames(self, container):
        frame = self.frames[container]
        frame.tkraise()

    def agregar(self):
        self.show_frames(Agregar)

    def actualizar(self):
        self.show_frames(Actualizar)

    def widgets(self):
        frame2 = tk.Frame(self)
        frame2.place(x=0, y=0, width=1100, height=40)


        self.btn_agregar = Button(frame2, fg="black", text="Agregar producto", font="sans 16 bold", command=self.agregar)
        self.btn_agregar.place(x=0, y=0, width=550, height=40)

        self.btn_actualizar = Button(frame2, fg="black", text="Actualizar stock", font="sans 16 bold", command=self.actualizar)
        self.btn_actualizar.place(x=550, y=0, width=550, height=40)


        self.buttons= [self.btn_actualizar, self.btn_agregar]
        
