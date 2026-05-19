# gui/cliente_window.py
# Panel del Cliente - puede ver productos y hacer apartados

import customtkinter as ctk
from tkinter import messagebox, ttk
from gui.styles import COLORES, FUENTES
from services.product_service import ProductService
from services.reservation_service import ReservationService


class VentanaCliente:

    def __init__(self, root, usuario):
        self.root = root
        self.usuario = usuario

        self.servicio_productos = ProductService()
        self.servicio_apartados = ReservationService()

        self.configurar_ui()
        self.cargar_productos()

    def configurar_ui(self):
        self.root.title(f"Demo Tienda - Cliente ({self.usuario.nombre})")
        self.root.geometry("1100x620")
        self.root.configure(fg_color=COLORES["fondo"])

        # Encabezado
        encabezado = ctk.CTkFrame(
            self.root, fg_color=COLORES["verde_principal"], height=55
        )
        encabezado.pack(fill="x")
        encabezado.pack_propagate(False)

        ctk.CTkLabel(
            encabezado,
            text=f"Demo Tienda  |  Bienvenido, {self.usuario.nombre}",
            font=FUENTES["encabezado"],
            text_color="#FFFFFF"
        ).pack(side="left", padx=20)

        ctk.CTkButton(
            encabezado,
            text="Mis apartados",
            fg_color=COLORES["naranja"],
            hover_color=COLORES["naranja_hover"],
            font=FUENTES["boton"],
            text_color="#FFFFFF",
            command=self.ver_mis_apartados
        ).pack(side="right", padx=10)

        # Contenido principal
        frame_principal = ctk.CTkFrame(self.root, fg_color="transparent")
        frame_principal.pack(fill="both", expand=True, padx=15, pady=15)

        # Filtro por categoria
        frame_filtro = ctk.CTkFrame(frame_principal, fg_color="transparent")
        frame_filtro.pack(fill="x", pady=(0, 10))

        ctk.CTkLabel(
            frame_filtro,
            text="Filtrar por categoria:",
            font=FUENTES["cuerpo"],
            text_color=COLORES["texto_medio"]
        ).pack(side="left", padx=(0, 8))

        categorias = self.servicio_productos.obtener_categorias()
        categorias.insert(0, "Todos")

        self.combo_categoria = ctk.CTkComboBox(
            frame_filtro,
            values=categorias,
            width=160,
            command=self.filtrar_por_categoria
        )
        self.combo_categoria.set("Todos")
        self.combo_categoria.pack(side="left")

        # Grid de productos (scrollable)
        self.frame_productos = ctk.CTkScrollableFrame(
            frame_principal, fg_color="transparent"
        )
        self.frame_productos.pack(fill="both", expand=True)

    def cargar_productos(self, categoria=None):
        for widget in self.frame_productos.winfo_children():
            widget.destroy()

        productos = self.servicio_productos.listar_productos()
        if categoria and categoria != "Todos":
            productos = [p for p in productos if p.categoria == categoria]

        if not productos:
            ctk.CTkLabel(
                self.frame_productos,
                text="No hay productos disponibles en esta categoria",
                font=FUENTES["cuerpo"],
                text_color=COLORES["texto_claro"]
            ).pack(pady=40)
            return

        # Grid de 3 columnas
        columnas = 3
        for i, producto in enumerate(productos):
            fila = i // columnas
            col = i % columnas
            self._crear_tarjeta_producto(producto, fila, col)
            self.frame_productos.grid_columnconfigure(col, weight=1)

    def _crear_tarjeta_producto(self, producto, fila, col):
        tarjeta = ctk.CTkFrame(
            self.frame_productos,
            fg_color=COLORES["superficie"],
            corner_radius=10,
            border_width=1,
            border_color=COLORES["borde"]
        )
        tarjeta.grid(row=fila, column=col, padx=8, pady=8, sticky="nsew")

        # Barra de color segun categoria
        colores_categoria = {
            "Frutas":    COLORES["naranja"],
            "Verduras":  COLORES["verde_principal"],
            "Tuberculos": COLORES["naranja_claro"],
            "Ropa":      COLORES["info"],
            "Calzado":   COLORES["info"],
            "Accesorios": COLORES["verde_claro"],
        }
        color_cat = colores_categoria.get(producto.categoria, COLORES["verde_claro"])

        ctk.CTkFrame(tarjeta, height=5, fg_color=color_cat, corner_radius=5).pack(fill="x")

        ctk.CTkLabel(
            tarjeta,
            text=producto.nombre,
            font=FUENTES["encabezado"],
            text_color=COLORES["texto_oscuro"]
        ).pack(pady=(12, 2))

        ctk.CTkLabel(
            tarjeta,
            text=producto.categoria,
            font=FUENTES["pequena"],
            text_color=COLORES["texto_claro"]
        ).pack()

        ctk.CTkLabel(
            tarjeta,
            text=f"${producto.precio_venta:.2f}",
            font=("Arial", 16, "bold"),
            text_color=COLORES["verde_principal"]
        ).pack(pady=6)

        # Indicador de stock
        if producto.stock > 10:
            texto_stock = f"Disponible ({producto.stock} uds)"
            color_stock = COLORES["exito"]
        elif producto.stock > 0:
            texto_stock = f"Pocas unidades ({producto.stock})"
            color_stock = COLORES["advertencia"]
        else:
            texto_stock = "Agotado"
            color_stock = COLORES["peligro"]

        ctk.CTkLabel(
            tarjeta,
            text=texto_stock,
            font=FUENTES["pequena"],
            text_color=color_stock
        ).pack()

        if producto.stock > 0:
            ctk.CTkButton(
                tarjeta,
                text="Apartar este producto",
                fg_color=COLORES["verde_principal"],
                hover_color=COLORES["verde_hover"],
                font=FUENTES["boton"],
                text_color="#FFFFFF",
                command=lambda p=producto: self.abrir_dialogo_apartar(p)
            ).pack(pady=10)
        else:
            ctk.CTkLabel(
                tarjeta,
                text="Sin stock",
                font=FUENTES["pequena"],
                text_color=COLORES["peligro"]
            ).pack(pady=10)

    def filtrar_por_categoria(self, seleccion):
        self.cargar_productos(seleccion)

    def abrir_dialogo_apartar(self, producto):
        dialogo = ctk.CTkToplevel(self.root)
        dialogo.title(f"Apartar - {producto.nombre}")
        dialogo.geometry("360x320")
        dialogo.grab_set()
        dialogo.configure(fg_color=COLORES["fondo"])

        ctk.CTkLabel(
            dialogo,
            text=f"Apartar: {producto.nombre}",
            font=FUENTES["encabezado"],
            text_color=COLORES["texto_oscuro"]
        ).pack(pady=(20, 5))

        ctk.CTkLabel(
            dialogo,
            text=f"Precio: ${producto.precio_venta:.2f}  |  Stock: {producto.stock}",
            font=FUENTES["pequena"],
            text_color=COLORES["texto_claro"]
        ).pack()

        ctk.CTkLabel(
            dialogo,
            text="Cantidad:",
            font=FUENTES["cuerpo"],
            text_color=COLORES["texto_medio"]
        ).pack(pady=(20, 4))

        entrada_cantidad = ctk.CTkEntry(
            dialogo, width=160,
            fg_color=COLORES["superficie"],
            border_color=COLORES["borde"]
        )
        entrada_cantidad.pack()

        def confirmar_apartado():
            try:
                cantidad = int(entrada_cantidad.get())
                dias = 2

                if cantidad <= 0 or cantidad > producto.stock:
                    messagebox.showerror(
                        "Error",
                        f"Cantidad no valida. Disponible: {producto.stock}",
                        parent=dialogo
                    )
                    return


                items = [{
                    "producto_id": producto.id_producto,
                    "nombre": producto.nombre,
                    "cantidad": cantidad,
                    "precio_venta": producto.precio_venta
                }]

                apartado = self.servicio_apartados.crear_apartado(
                    cliente_nombre=self.usuario.nombre,
                    cliente_email=self.usuario.email,
                    productos=items,
                    dias_validez=dias
                )

                if apartado:
                    messagebox.showinfo(
                        "Apartado creado",
                        "Tu apartado fue creado.\nVence en 2 dias.",
                        parent=dialogo
                    )
                    dialogo.destroy()
                else:
                    messagebox.showerror(
                        "Error", "No se pudo crear el apartado", parent=dialogo
                    )

            except ValueError:
                messagebox.showerror("Error", "Ingresa valores numericos validos", parent=dialogo)

        ctk.CTkButton(
            dialogo,
            text="Confirmar apartado",
            fg_color=COLORES["verde_principal"],
            hover_color=COLORES["verde_hover"],
            font=FUENTES["boton"],
            text_color="#FFFFFF",
            command=confirmar_apartado
        ).pack(pady=20)

        ctk.CTkButton(
            dialogo,
            text="Cancelar",
            fg_color=COLORES["superficie"],
            hover_color=COLORES["superficie_gris"],
            font=FUENTES["cuerpo"],
            text_color=COLORES["texto_medio"],
            border_width=1,
            border_color=COLORES["borde"],
            command=dialogo.destroy
        ).pack()

    def ver_mis_apartados(self):
        mis_apartados = self.servicio_apartados.listar_apartados_por_cliente(self.usuario.email)

        dialogo = ctk.CTkToplevel(self.root)
        dialogo.title("Mis apartados")
        dialogo.geometry("750x420")
        dialogo.configure(fg_color=COLORES["fondo"])

        ctk.CTkLabel(
            dialogo,
            text="Mis productos apartados",
            font=FUENTES["encabezado"],
            text_color=COLORES["texto_oscuro"]
        ).pack(pady=(15, 8))

        if not mis_apartados:
            ctk.CTkLabel(
                dialogo,
                text="No tienes productos apartados actualmente",
                font=FUENTES["cuerpo"],
                text_color=COLORES["texto_claro"]
            ).pack(pady=40)
        else:
            columnas = ("ID", "Productos", "Total", "Vence", "Estado")
            tabla = ttk.Treeview(dialogo, columns=columnas, show="headings", height=10)

            anchos = [80, 240, 80, 150, 80]
            for col, ancho in zip(columnas, anchos):
                tabla.heading(col, text=col)
                tabla.column(col, width=ancho, anchor="center")

            for a in mis_apartados:
                prods = ", ".join([f"{p['nombre']} x{p['cantidad']}" for p in a.productos])
                dias = a.dias_restantes()
                tabla.insert("", "end", values=(
                    a.id_apartado,
                    prods[:40],
                    f"${a.total_apartado:.2f}",
                    f"{a.fecha_limite}",
                    a.estado
                ))

            tabla.pack(fill="both", expand=True, padx=15, pady=10)

        ctk.CTkButton(
            dialogo,
            text="Cerrar",
            fg_color=COLORES["verde_principal"],
            hover_color=COLORES["verde_hover"],
            font=FUENTES["boton"],
            text_color="#FFFFFF",
            command=dialogo.destroy
        ).pack(pady=10)

    def cerrar_sesion(self):
        self.root.destroy()
        import customtkinter as ctk
        nueva_root = ctk.CTk()
        from gui.login_window import VentanaLogin
        VentanaLogin(nueva_root, self._iniciar_nueva_sesion)
        nueva_root.mainloop()

