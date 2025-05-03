import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

class Actualizar(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack()
        self.place(x=0, y=0, width=1100, height=650)
        self.widgets()

    def widgets(self):
        # Título
        titulo = tk.Label(self, text="Actualizar Producto", font=("Arial", 24, "bold"))
        titulo.pack(pady=20)

        # Tabla de productos
        columnas = ("nombre", "precio", "stock")
        self.tree = ttk.Treeview(self, columns=columnas, show="headings")
        self.tree.heading("nombre", text="Producto")
        self.tree.heading("precio", text="Precio")
        self.tree.heading("stock", text="Stock")
        self.tree.pack(pady=20, expand=True)

        # Cargar productos en la tabla
        self.cargar_productos()

        # Formulario de actualización
        form_frame = tk.Frame(self)
        form_frame.pack(pady=10)

        tk.Label(form_frame, text="Nuevo Nombre:", font=("Arial", 14)).grid(row=0, column=0, padx=10)
        self.nuevo_nombre_entry = tk.Entry(form_frame, font=("Arial", 14))
        self.nuevo_nombre_entry.grid(row=0, column=1, padx=10)

        tk.Label(form_frame, text="Nuevo Precio:", font=("Arial", 14)).grid(row=1, column=0, padx=10)
        self.nuevo_precio_entry = tk.Entry(form_frame, font=("Arial", 14))
        self.nuevo_precio_entry.grid(row=1, column=1, padx=10)

        tk.Label(form_frame, text="Nuevo Stock:", font=("Arial", 14)).grid(row=2, column=0, padx=10)
        self.nuevo_stock_entry = tk.Entry(form_frame, font=("Arial", 14))
        self.nuevo_stock_entry.grid(row=2, column=1, padx=10)

        btn_actualizar = tk.Button(form_frame, text="Actualizar Producto", font=("Arial", 16), command=self.actualizar_producto)
        btn_actualizar.grid(row=3, column=0, columnspan=2, pady=10)

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
            messagebox.showinfo("Info", "No hay productos registrados todavía.")

    def actualizar_producto(self):
        selected = self.tree.focus()
        if not selected:
            messagebox.showerror("Error", "Selecciona un producto primero.")
            return

        nuevo_nombre = self.nuevo_nombre_entry.get().strip()
        nuevo_precio = self.nuevo_precio_entry.get().strip()
        nuevo_stock = self.nuevo_stock_entry.get().strip()

        if not nuevo_nombre and not nuevo_precio and not nuevo_stock:
            messagebox.showerror("Error", "Debes ingresar al menos un nuevo valor.")
            return

        producto_nombre = self.tree.item(selected)["values"][0]

        # Leer productos existentes
        with open("productos.json", "r") as file:
            productos = json.load(file)

        for producto in productos:
            if producto["nombre"] == producto_nombre:
                if nuevo_nombre:
                    producto["nombre"] = nuevo_nombre
                if nuevo_precio.isdigit():
                    producto["precio"] = int(nuevo_precio)
                if nuevo_stock.isdigit():
                    producto["stock"] = int(nuevo_stock)

        # Guardar productos actualizados
        with open("productos.json", "w") as file:
            json.dump(productos, file, indent=4)

        messagebox.showinfo("Éxito", "Producto actualizado correctamente.")

        # Limpiar entradas
        self.nuevo_nombre_entry.delete(0, tk.END)
        self.nuevo_precio_entry.delete(0, tk.END)
        self.nuevo_stock_entry.delete(0, tk.END)

        # Recargar la tabla
        self.cargar_productos()
