import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

class Agregar(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack()
        self.place(x=0, y=0, width=1100, height=650)
        self.widgets()

    def widgets(self):
        # Título
        titulo = tk.Label(self, text="Agregar Nuevo Producto", font=("Arial", 24, "bold"))
        titulo.pack(pady=20)

        # Formulario de entrada
        form_frame = tk.Frame(self)
        form_frame.pack(pady=20)

        tk.Label(form_frame, text="Nombre del producto:", font=("Arial", 14)).grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.nombre_entry = tk.Entry(form_frame, font=("Arial", 14))
        self.nombre_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(form_frame, text="Precio:", font=("Arial", 14)).grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.precio_entry = tk.Entry(form_frame, font=("Arial", 14))
        self.precio_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(form_frame, text="Stock inicial:", font=("Arial", 14)).grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.stock_entry = tk.Entry(form_frame, font=("Arial", 14))
        self.stock_entry.grid(row=2, column=1, padx=10, pady=5)

#botoncitos
        agregar_btn = tk.Button(self, text="Agregar Producto", font=("Arial", 16), command=self.agregar_producto)
        agregar_btn.pack(pady=20)

#tabli de productos 
        self.tree = ttk.Treeview(self, columns=("nombre", "precio", "stock"), show="headings")
        self.tree.heading("nombre", text="Producto")
        self.tree.heading("precio", text="Precio")
        self.tree.heading("stock", text="Stock")
        self.tree.pack(pady=10, expand=True)

        self.cargar_productos()

    def cargar_productos(self):
        self.tree.delete(*self.tree.get_children())
        if os.path.exists("productos.json"):
            with open("productos.json", "r") as file:
                try:
                    productos = json.load(file)
                    for producto in productos:
                        self.tree.insert("", "end", values=(producto["nombre"], producto["precio"], producto["stock"]))
                except json.JSONDecodeError:
                    messagebox.showerror("Error", "Error al leer productos.json")
        else:
            # Si no existe, crear un archivo vacío
            with open("productos.json", "w") as file:
                json.dump([], file)

    def agregar_producto(self):
        nombre = self.nombre_entry.get()
        precio = self.precio_entry.get()
        stock = self.stock_entry.get()

        # Validaciones
        if not nombre or not precio or not stock:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return
        if not precio.isdigit() or not stock.isdigit():
            messagebox.showerror("Error", "Precio y Stock deben ser números.")
            return

        nuevo_producto = {
            "nombre": nombre,
            "precio": int(precio),
            "stock": int(stock)
        }

        # Guardar en el JSON
        productos = []
        if os.path.exists("productos.json"):
            with open("productos.json", "r") as file:
                try:
                    productos = json.load(file)
                except json.JSONDecodeError:
                    productos = []

        productos.append(nuevo_producto)

        with open("productos.json", "w") as file:
            json.dump(productos, file, indent=4)

        messagebox.showinfo("Éxito", f"Producto '{nombre}' agregado correctamente.")

        # Limpiar entradas
        self.nombre_entry.delete(0, tk.END)
        self.precio_entry.delete(0, tk.END)
        self.stock_entry.delete(0, tk.END)

        # Refrescar tabla
        self.cargar_productos()
