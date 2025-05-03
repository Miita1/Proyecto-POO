import json
import os
from tkinter import *
import tkinter as tk
from tkinter import ttk, messagebox
from container import Container
from PIL import Image, ImageTk

class Login(tk.Frame):
    db_name = "database.db"

    def __init__(self, padre, controlador):
        super().__init__(padre)
        self.pack()
        self.place(x=0, y=0, width=1100, height=650)
        self.controlador = controlador
        
        #para q no sea visible
        self.menu_visible = False

        self.pedido_actual = []  #almacena ítems

        #frames menu para mostrarlo
        self.menu_frame = None
        self.pedido_frame = None
        self.imagen_frame = None
        
        #visuales
        self.widgets()


    def validacion(self, user, pas):
        return len(user) > 0 and len(pas) > 0
    
    def eliminar_item(self):
        seleccionado = self.tree.selection()
        if seleccionado:
            for item_id in seleccionado:
                self.tree.delete(item_id)
                index = self.tree.index(item_id)
                del self.pedido_actual[index]

    
    def login(self):
        user = self.username.get()
        pas = self.password.get()

        if self.validacion(user, pas):
            try:
                if os.path.exists("usuarios.json"):
                    with open("usuarios.json", "r") as archivo:
                        usuarios = json.load(archivo)

                    encontrado = any(u["username"] == user and u["password"] == pas for u in usuarios)

                    if encontrado:
                        self.control1()
                    else:
                        self.username.delete(0, 'end')
                        self.password.delete(0, 'end')
                        messagebox.showerror(title="Error", message="Usuario y/o contraseña incorrecta")
                
                else:
                    messagebox.showerror(title="Error", message="Archivo de usuarios no encontrado")
            except Exception as e:
                messagebox.showerror(title="Error", message=f"Ocurrió un error: {e}")
        else:
            messagebox.showerror(title="Error", message="Llene todas las casillas")

    def seleccionar_producto(self, nombre, tipo):
        if tipo == "bebida":
            self.bebida_var.set(nombre)
        elif tipo == "postre":
            self.postre_var.set(nombre)


    def control1(self):
        usuario = self.username.get()
        contrasena = self.password.get()

        if not usuario or not contrasena:
            messagebox.showerror("Error", "Por favor, ingresa usuario y contraseña.")
            return

        try:
            with open("usuarios.json", "r") as archivo:
                usuarios = json.load(archivo)
        except FileNotFoundError:
            messagebox.showerror("Error", "No se encontró el archivo de usuarios.")
            return

        for user in usuarios:
            if user["username"] == usuario and user["password"] == contrasena:
                messagebox.showinfo("Acceso permitido", "Bienvenido al panel de administración.")

                self.controlador.show_frame(Container)
            # Aquí abres el panel de administrador
                return

        messagebox.showerror("Error", "Usuario o contraseña incorrectos.")

    def widgets(self):
        fondo = tk.Frame(self, bg= "blue")
        fondo.pack()
        fondo.place(x=0, y=0, width=1100, height=650)

        self.bg_image = Image.open("imagenes/cafeteria.jpg")
        self.bg_image = self.bg_image.resize((1100, 650))
        self.bg_image = ImageTk.PhotoImage(self.bg_image)
        self.bg_label = ttk.Label(fondo, image=self.bg_image)
        self.bg_label.place(x=0, y=0, width=1100, height=650)

        frame1 = tk.Frame(self, bg="white", highlightbackground="black",highlightthickness=1)
        frame1.place(x=350, y=20, width=400, height=600)

        self.logo_image = Image.open("imagenes/logo.jpg") 
        self.logo_image = self.logo_image.resize((300, 300))  
        self.logo_image = ImageTk.PhotoImage(self.logo_image)
        
        logo_label = tk.Label(frame1, image=self.logo_image, bg="white")
        logo_label.place(x=70, y=7)

        user = ttk.Label(frame1, text="Nombre de usuario", font="arial 16 bold", background="white")
        user.place(x=100, y=250)
        self.username = ttk.Entry(frame1, font="arial 16 bold")
        self.username.place(x=80, y=290, width=240, height=40)

        pas = ttk.Label(frame1, text="Contraseña", font="arial 16 bold", background="white")
        pas.place(x=100, y=340)
        self.password = ttk.Entry(frame1, show="*", font="arial 16 bold")
        self.password.place(x=80, y=380, width=240, height=40)

        btn_menu = tk.Button(frame1, text="Menú", font="arial 16 bold", command=self.toggle_menu)
        btn_menu.place(x=80, y=490, width=240, height=40)

        btn1 = tk.Button(frame1, text="iniciar sesion", font="arial 16 bold", command=self.control1)
        btn1.place(x=80, y= 440, width=240, height=40)


        
        #inicia pero no se coloca
        self.menu_frame = tk.Frame(self, bg="white")
        self.pedido_frame = tk.Frame(self, bg="white")
        self.imagen_frame = tk.Frame(self, bg="white")

        #se oculta hasta el boton
        self.menu_frame.place_forget()
        self.pedido_frame.place_forget()
        self.imagen_frame.place_forget()




    def toggle_menu(self):
        if not self.menu_visible:
            self.menu_frame.place(x=20, y=20, width=280, height=600)
            self.imagen_frame.place(x=710, y=20, width=387, height=600)
            self.pedido_frame.place(x=0, y=20, width=370, height=600)
        else:
        # Ocultar los frames
            self.menu_frame.place_forget()
            self.imagen_frame.place_forget()
            self.pedido_frame.place_forget()
        self.menu_visible = not self.menu_visible



                # === Menú Interactivo ===
        menu_frame = tk.Frame(self, bg="white")
        menu_frame.place(x=20, y=20, width=280, height=600)

        ttk.Label(menu_frame, text="Menú", font="arial 20 bold", background="white").pack(pady=10)

        # Producto 1: Bebida
        ttk.Label(menu_frame, text="Bebida:", background="white", font="arial 12").pack(anchor="w", padx=10)
        self.bebida_var = tk.StringVar()
        bebida_combo = ttk.Combobox(menu_frame, textvariable=self.bebida_var, values=["Capuchino", "Latte", "Té"], state="readonly")
        bebida_combo.pack(padx=10, pady=5)

        ttk.Label(menu_frame, text="Cantidad:", background="white", font="arial 12").pack(anchor="w", padx=10)
        self.bebida_cantidad = tk.Spinbox(menu_frame, from_=0, to=10, width=5)
        self.bebida_cantidad.pack(padx=10)

        # Producto 2: Postre
        ttk.Label(menu_frame, text="Postre:", background="white", font="arial 12").pack(anchor="w", padx=10, pady=(15,0))
        self.postre_var = tk.StringVar()
        postre_combo = ttk.Combobox(menu_frame, textvariable=self.postre_var, values=["Cheesecake", "Brownie", "Croissant"], state="readonly")
        postre_combo.pack(padx=10, pady=5)

        ttk.Label(menu_frame, text="Cantidad:", background="white", font="arial 12").pack(anchor="w", padx=10)
        self.postre_cantidad = tk.Spinbox(menu_frame, from_=0, to=10, width=5)
        self.postre_cantidad.pack(padx=10)

        # Personalización
        ttk.Label(menu_frame, text="Personalización:", background="white", font="arial 12 bold").pack(pady=10)

        self.extra_leche = tk.BooleanVar()
        ttk.Checkbutton(menu_frame, text="Extra leche", variable=self.extra_leche).pack(anchor="w", padx=10)

        self.sin_azucar = tk.BooleanVar()
        ttk.Checkbutton(menu_frame, text="Sin azúcar", variable=self.sin_azucar).pack(anchor="w", padx=10)

        self.tamaño_var = tk.StringVar(value="Mediano")
        ttk.Label(menu_frame, text="Tamaño:", background="white").pack(anchor="w", padx=10, pady=(10, 0))
        ttk.Combobox(menu_frame, textvariable=self.tamaño_var, values=["Chico", "Mediano", "Grande"], state="readonly").pack(padx=10)



        # Confirmar Pedido
        tk.Button(menu_frame, text="Confirmar Pedido", command=self.confirmar_pedido).pack(pady=20)

        btn_regresar = tk.Button(self.menu_frame, text="Regresar al inicio", font="Arial 16 bold", command=lambda:self.controlador.show_frame(Login))
        btn_regresar.pack(pady=10)


        catalogo_canvas = tk.Canvas(self.imagen_frame, background="white", width=300, height=580)
        catalogo_scroll = tk.Scrollbar(self.imagen_frame, orient="vertical", command=catalogo_canvas.yview)
        self.catalogo_frame = tk.Frame(catalogo_canvas, bg="white")

        self.catalogo_frame.bind(
            "<Configure>",
            lambda e: catalogo_canvas.configure(scrollregion=catalogo_canvas.bbox("all"))
        )

        catalogo_canvas.create_window((0, 0), window=self.catalogo_frame, anchor="nw")
        catalogo_canvas.configure(yscrollcommand=catalogo_scroll.set)

        catalogo_canvas.pack(side="left", fill="both", expand=True)
        catalogo_scroll.pack(side="right", fill="y")

        # Productos organizados por tipo
        productos = {
            "Capuchino": "bebida",
            "Latte": "bebida",
            "Té": "bebida",
            "Chai": "bebida",
            "Espresso": "bebida",
            "Limonada mineral": "bebida",
            "Limonada rosa": "bebida",
            "Malteada de chocolate": "bebida",
            "Malteada de fresa": "bebida",
            "Matcha": "bebida",
            "Smoothie": "bebida",
            "Taro": "bebida",
            "Cheesecake": "postre",
            "Chocoflan": "postre",
            "Copa de helado": "postre",
            "Crepa": "postre",
            "Flan": "postre",
            "Gelatina": "postre",
            "Pastel de zanahoria": "postre",
            "Tiramisú": "postre",
            "Waffles": "postre",
            "Brownie": "postre",
            "Pay de limón": "postre",
            "Croissant": "postre"
        }

        for tipo in ["bebida", "postre"]:
            ttk.Label(self.catalogo_frame, text=tipo.capitalize(), font="arial 14 bold", background="white").pack(pady=(10, 0))
            fila = tk.Frame(self.catalogo_frame, bg="white")
            fila.pack(pady=5)

            columna = 0
            fila_actual = fila
            for nombre, categoria in productos.items():
                if categoria == tipo:
                    if columna >= 3:
                         fila_actual = tk.Frame(self.catalogo_frame, bg="white")
                         fila_actual.pack(pady=5)
                         columna = 0
                    try:
                        img = Image.open(f"imagenes/{nombre.lower()}.jpg").resize((100, 80))
                        img = ImageTk.PhotoImage(img)
                        btn = tk.Button(fila_actual, image=img, text=nombre, compound="top", bd=1,
                                        command=lambda n=nombre, t=tipo: self.seleccionar_producto(n, t))
                        btn.image = img
                        btn.grid(row=0, column=columna, padx=5, pady=5)
                        columna += 1
                    except:
                        ttk.Label(fila_actual, text=nombre).grid(row=0, column=columna, padx=5, pady=5)
                        columna += 1

                # === Vista del pedido actual ===
        self.pedido_frame = tk.Frame(self, bg="white")
        self.pedido_frame.place(x=340, y=20, width=370, height=600)

        #nombre del cliente 
        ttk.Label(self.pedido_frame, text="Nombre del Cliente:", background="white", font="arial 12 bold").pack(pady=(10, 0))
        self.nombre_cliente = tk.Entry(self.pedido_frame, font="arial 12")
        self.nombre_cliente.pack(pady=5)


        ttk.Label(self.pedido_frame, text="Pedido Actual", font="arial 16 bold", background="white").pack(pady=10)

        columnas = ("producto", "cantidad", "personalizacion")
        self.tree = ttk.Treeview(self.pedido_frame, columns=columnas, show="headings")
        self.tree.heading("producto", text="Producto")
        self.tree.heading("cantidad", text="Cantidad")
        self.tree.heading("personalizacion", text="Personalización")
        self.tree.pack(pady=10, expand=True)

        tk.Button(self.pedido_frame, text="Eliminar Seleccionado", command=self.eliminar_item).pack(pady=10)
        tk.Button(self.pedido_frame, text="Finalizar Pedido", command=self.finalizar_pedido).pack(pady=10)

#finaliza el pedido 
    def finalizar_pedido(self):
        nombre = self.nombre_cliente.get()

        if not nombre:
            messagebox.showerror("Error", "Por favor, ingresa el nombre del cliente.")
            return

        if not self.pedido_actual:
            messagebox.showerror("Error", "No hay productos en el pedido.")
            return

        resumen = f"Pedido de {nombre}:\n\n"

        for item in self.pedido_actual:
            resumen += f"{item['cantidad']}x {item['producto']} - {item['personalizacion']}\n"

        messagebox.showinfo("Pedido Realizado", resumen)

        #guarda en archivo 
        nuevo_pedido = {
            "cliente": nombre,
            "pedido": self.pedido_actual
        }

        pedidos = []
        if os.path.exists("pedidos.json"):
            with open("pedidos.json", "r") as archivo:
                try:
                    pedidos = json.load(archivo)
                except json.JSONDecodeError:
                    pedidos = []

        pedidos.append(nuevo_pedido)

        with open("pedidos.json", "w") as archivo:
            json.dump(pedidos, archivo, indent=4)

        #limpia opciones
        self.tree.delete(*self.tree.get_children())
        self.pedido_actual.clear()
        self.nombre_cliente.delete(0, 'end')




    def confirmar_pedido(self):
        bebida = self.bebida_var.get()
        postre = self.postre_var.get()

        try:
            bebida_cant = int(self.bebida_cantidad.get())
            postre_cant = int(self.postre_cantidad.get())
        except ValueError:
            messagebox.showerror("Error", "La cantidad debe ser un número válido")
            return

        try:
            with open("productos.json", "r") as file:
                productos = json.load(file)
        except FileNotFoundError:
            messagebox.showerror("Error", "No se encontró el inventario de productos.")
            return
        
        error = False

    # Verificar disponibilidad de bebida
        if bebida:
            bebida_encontrada = False
            for prod in productos:
                if prod["nombre"].lower() == bebida.lower():
                    bebida_encontrada = True
                    if bebida_cant > prod["stock"]:
                        messagebox.showerror("Error", f"No hay suficiente stock de {bebida}. Stock disponible: {prod['stock']}")
                        error = True
                    else:
                        prod["stock"] -= bebida_cant
            if not bebida_encontrada:
                messagebox.showerror("Error", f"Producto '{bebida}' no encontrado en inventario")
                return


    # Verificar disponibilidad de postre
        if postre:
            postre_encontrado = False
            for prod in productos:
                if prod["nombre"].lower() == postre.lower():
                    postre_encontrado = True
                    if postre_cant > prod["stock"]:
                        messagebox.showerror("Error", f"No hay suficiente stock de {postre}. Stock disponible: {prod['stock']}")
                        error = True
                    else:
                        prod["stock"] -= postre_cant
                    
            if not postre_encontrado:
                messagebox.showerror("Error", f"Producto '{postre}' no encontrado en inventario.")
                return
            
        if error:
            return
        
        with open("productos.json", "w") as file:
            json.dump(productos, file, indent=4)

        personalizacion = []
        if self.extra_leche.get():
            personalizacion.append("Extra leche")
        if self.sin_azucar.get():
            personalizacion.append("Sin azúcar")
        personalizacion.append(f"Tamaño: {self.tamaño_var.get()}")

        if bebida and int(bebida_cant) > 0:
            item = {"producto": bebida, "cantidad": bebida_cant, "personalizacion": ", ".join(personalizacion)}
            self.pedido_actual.append(item)
            self.tree.insert("", "end", values=(bebida, bebida_cant, item["personalizacion"]))

        if postre and int(postre_cant) > 0:
            item = {"producto": postre, "cantidad": postre_cant, "personalizacion": ""}
            self.pedido_actual.append(item)
            self.tree.insert("", "end", values=(postre, postre_cant, ""))
    
        messagebox.showinfo("Éxito", "Producto(s) agregado(s) al pedido.")

    



    