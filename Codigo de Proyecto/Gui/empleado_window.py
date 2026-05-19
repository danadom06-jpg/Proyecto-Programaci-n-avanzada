# gui/empleado_window.py
# Panel del Empleado - puede ver inventario y registrar ventas

import customtkinter as ctk
from tkinter import messagebox, ttk
from gui.styles import COLORES, FUENTES
from services.product_service import ProductService
from services.sale_service import SaleService
from models.sale import Venta


class VentanaEmpleado:

    def __init__(self, root, usuario):
        self.root = root
        self.usuario = usuario

        self.servicio_productos = ProductService()
        self.servicio_ventas = SaleService(self.servicio_productos)

        self.carrito = []

        self.configurar_ui()
        self.cargar_inventario()

    def configurar_ui(self):
        self.root.title(f"Demo Tienda - Empleado ({self.usuario.nombre})")
        self.root.geometry("1200x680")
        self.root.configure(fg_color=COLORES["fondo"])

        # Encabezado
        encabezado = ctk.CTkFrame(
            self.root, fg_color=COLORES["verde_principal"], height=55
        )
        encabezado.pack(fill="x")
        encabezado.pack_propagate(False)

        ctk.CTkLabel(
            encabezado,
            text=f"Demo Tienda  |  Empleado: {self.usuario.nombre}",
            font=FUENTES["encabezado"],
            text_color="#FFFFFF"
        ).pack(side="left", padx=20)


        # Frame principal dividido en dos columnas
        frame_principal = ctk.CTkFrame(self.root, fg_color="transparent")
        frame_principal.pack(fill="both", expand=True, padx=10, pady=10)

        # Panel izquierdo - catalogo
        frame_catalogo = ctk.CTkFrame(
            frame_principal,
            fg_color=COLORES["superficie"],
            corner_radius=8,
            border_width=1,
            border_color=COLORES["borde"]
        )
        frame_catalogo.pack(side="left", fill="both", expand=True, padx=(0, 5))

        ctk.CTkLabel(
            frame_catalogo,
            text="Catalogo de productos",
            font=FUENTES["encabezado"],
            text_color=COLORES["texto_oscuro"]
        ).pack(anchor="w", padx=15, pady=(12, 5))

        # Barra de busqueda
        frame_busqueda = ctk.CTkFrame(frame_catalogo, fg_color="transparent")
        frame_busqueda.pack(fill="x", padx=10, pady=5)

        self.entrada_busqueda = ctk.CTkEntry(
            frame_busqueda,
            placeholder_text="Buscar por nombre...",
            width=220,
            fg_color=COLORES["fondo"],
            border_color=COLORES["borde"]
        )
        self.entrada_busqueda.pack(side="left", padx=5)

        ctk.CTkButton(
            frame_busqueda, text="Buscar", width=80,
            fg_color=COLORES["verde_principal"], hover_color=COLORES["verde_hover"],
            font=FUENTES["boton"], text_color="#FFFFFF",
            command=self.buscar_producto
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            frame_busqueda, text="Ver todos", width=90,
            fg_color=COLORES["naranja"], hover_color=COLORES["naranja_hover"],
            font=FUENTES["boton"], text_color="#FFFFFF",
            command=self.cargar_inventario
        ).pack(side="left", padx=5)

        # Tabla de productos
        # CORRECCION: se bindea el doble clic correctamente aqui
        columnas = ("ID", "Nombre", "Categoria", "Precio", "Stock")
        self.tabla_productos = ttk.Treeview(
            frame_catalogo, columns=columnas, show="headings", height=18
        )

        anchos = [80, 200, 120, 90, 70]
        for col, ancho in zip(columnas, anchos):
            self.tabla_productos.heading(col, text=col)
            self.tabla_productos.column(col, width=ancho, anchor="center")

        self.tabla_productos.pack(fill="both", expand=True, padx=10, pady=10)

        # Instruccion para el usuario
        ctk.CTkLabel(
            frame_catalogo,
            text="Doble clic en un producto para agregarlo al carrito",
            font=FUENTES["pequena"],
            text_color=COLORES["texto_claro"]
        ).pack(pady=(0, 8))

        # CORRECCION: el binding estaba definido pero nunca se conectaba
        self.tabla_productos.bind("<Double-1>", self.agregar_al_carrito)

        # Panel derecho - carrito
        frame_carrito = ctk.CTkFrame(
            frame_principal,
            width=320,
            fg_color=COLORES["superficie"],
            corner_radius=8,
            border_width=1,
            border_color=COLORES["borde"]
        )
        frame_carrito.pack(side="right", fill="y", padx=(5, 0))
        frame_carrito.pack_propagate(False)

        ctk.CTkLabel(
            frame_carrito,
            text="Carrito de venta",
            font=FUENTES["encabezado"],
            text_color=COLORES["texto_oscuro"]
        ).pack(anchor="w", padx=15, pady=(12, 5))

        # Lista del carrito (scrollable)
        self.frame_lista_carrito = ctk.CTkScrollableFrame(
            frame_carrito,
            fg_color=COLORES["fondo"],
            height=300
        )
        self.frame_lista_carrito.pack(fill="both", expand=True, padx=10, pady=5)

        # Total
        self.etiqueta_total = ctk.CTkLabel(
            frame_carrito,
            text="Total: $0.00",
            font=("Arial", 18, "bold"),
            text_color=COLORES["verde_principal"]
        )
        self.etiqueta_total.pack(pady=8)

        # Metodo de pago
        ctk.CTkLabel(
            frame_carrito,
            text="Metodo de pago:",
            font=FUENTES["pequena"],
            text_color=COLORES["texto_medio"]
        ).pack()

        self.combo_pago = ctk.CTkComboBox(
            frame_carrito,
            values=Venta.METODOS_PAGO,
            width=220
        )
        self.combo_pago.set("Efectivo")
        self.combo_pago.pack(pady=5)

        # Botones del carrito
        frame_botones = ctk.CTkFrame(frame_carrito, fg_color="transparent")
        frame_botones.pack(pady=10)

        ctk.CTkButton(
            frame_botones,
            text="Cobrar",
            fg_color=COLORES["verde_principal"],
            hover_color=COLORES["verde_hover"],
            font=FUENTES["boton"],
            text_color="#FFFFFF",
            width=130,
            command=self.realizar_venta
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            frame_botones,
            text="Limpiar",
            fg_color=COLORES["peligro"],
            hover_color=COLORES["peligro_hover"],
            font=FUENTES["boton"],
            text_color="#FFFFFF",
            width=130,
            command=self.limpiar_carrito
        ).pack(side="left", padx=5)

    def cargar_inventario(self):
        for item in self.tabla_productos.get_children():
            self.tabla_productos.delete(item)

        productos = self.servicio_productos.listar_productos()
        for p in productos:
            self.tabla_productos.insert("", "end", values=(
                p.id_producto, p.nombre, p.categoria,
                f"${p.precio_venta:.2f}", p.stock
            ))

    def buscar_producto(self):
        termino = self.entrada_busqueda.get().strip().lower()
        if not termino:
            self.cargar_inventario()
            return

        for item in self.tabla_productos.get_children():
            self.tabla_productos.delete(item)

        productos = self.servicio_productos.listar_productos()
        for p in productos:
            if termino in p.nombre.lower():
                self.tabla_productos.insert("", "end", values=(
                    p.id_producto, p.nombre, p.categoria,
                    f"${p.precio_venta:.2f}", p.stock
                ))

    def agregar_al_carrito(self, event=None):
        seleccion = self.tabla_productos.selection()
        if not seleccion:
            return

        item = self.tabla_productos.item(seleccion[0])
        valores = item["values"]

        # Ventana para ingresar cantidad
        dialogo = ctk.CTkToplevel(self.root)
        dialogo.title("Cantidad")
        dialogo.geometry("300x210")
        dialogo.grab_set()
        dialogo.configure(fg_color=COLORES["fondo"])

        ctk.CTkLabel(
            dialogo,
            text=valores[1],
            font=FUENTES["encabezado"],
            text_color=COLORES["texto_oscuro"]
        ).pack(pady=(20, 5))

        ctk.CTkLabel(
            dialogo,
            text=f"Precio: {valores[3]}   |   Stock disponible: {valores[4]}",
            font=FUENTES["pequena"],
            text_color=COLORES["texto_claro"]
        ).pack()

        ctk.CTkLabel(
            dialogo,
            text="Cantidad a vender:",
            font=FUENTES["pequena"],
            text_color=COLORES["texto_medio"]
        ).pack(pady=(15, 3))

        entrada_cantidad = ctk.CTkEntry(
            dialogo, width=150,
            fg_color=COLORES["superficie"],
            border_color=COLORES["borde"]
        )
        entrada_cantidad.pack()
        entrada_cantidad.focus()

        def confirmar():
            try:
                cantidad = int(entrada_cantidad.get())
                if cantidad <= 0:
                    raise ValueError("La cantidad debe ser positiva")
                stock_disponible = int(valores[4])
                if cantidad > stock_disponible:
                    messagebox.showerror(
                        "Error", f"Solo hay {stock_disponible} unidades disponibles",
                        parent=dialogo
                    )
                    return

                precio = float(valores[3].replace("$", ""))

                # Verificar si ya esta en el carrito para sumar
                for item_carrito in self.carrito:
                    if item_carrito["id_producto"] == valores[0]:
                        item_carrito["cantidad"] += cantidad
                        dialogo.destroy()
                        self.actualizar_carrito()
                        return

                self.carrito.append({
                    "id_producto": valores[0],
                    "nombre": valores[1],
                    "cantidad": cantidad,
                    "precio_venta": precio,
                    "costo_compra": 0  # El empleado no ve el costo
                })
                dialogo.destroy()
                self.actualizar_carrito()

            except ValueError as e:
                messagebox.showerror("Error", "Ingresa una cantidad valida", parent=dialogo)

        ctk.CTkButton(
            dialogo,
            text="Agregar",
            fg_color=COLORES["verde_principal"],
            hover_color=COLORES["verde_hover"],
            font=FUENTES["boton"],
            text_color="#FFFFFF",
            command=confirmar
        ).pack(pady=15)

        dialogo.bind("<Return>", lambda e: confirmar())

    def actualizar_carrito(self):
        for widget in self.frame_lista_carrito.winfo_children():
            widget.destroy()

        total = 0
        for item in self.carrito:
            subtotal = item["cantidad"] * item["precio_venta"]
            total += subtotal

            frame_item = ctk.CTkFrame(
                self.frame_lista_carrito,
                fg_color=COLORES["superficie"],
                corner_radius=6
            )
            frame_item.pack(fill="x", pady=3)

            ctk.CTkLabel(
                frame_item,
                text=f"{item['nombre']}",
                font=FUENTES["pequena"],
                text_color=COLORES["texto_oscuro"],
                anchor="w"
            ).pack(side="left", padx=8, pady=6)

            ctk.CTkLabel(
                frame_item,
                text=f"x{item['cantidad']}  ${subtotal:.2f}",
                font=FUENTES["pequena"],
                text_color=COLORES["verde_principal"]
            ).pack(side="right", padx=5)

            ctk.CTkButton(
                frame_item,
                text="X",
                width=28, height=22,
                fg_color=COLORES["peligro"],
                hover_color=COLORES["peligro_hover"],
                text_color="#FFFFFF",
                font=("Arial", 9, "bold"),
                command=lambda i=item: self.quitar_del_carrito(i)
            ).pack(side="right", padx=3)

        self.etiqueta_total.configure(text=f"Total: ${total:.2f}")

    def quitar_del_carrito(self, item_a_quitar):
        self.carrito = [i for i in self.carrito if i != item_a_quitar]
        self.actualizar_carrito()

    def limpiar_carrito(self):
        self.carrito = []
        self.actualizar_carrito()

    def realizar_venta(self):
        if not self.carrito:
            messagebox.showwarning("Atencion", "El carrito esta vacio")
            return

        total = sum(item["cantidad"] * item["precio_venta"] for item in self.carrito)
        metodo = self.combo_pago.get()

        if not messagebox.askyesno("Confirmar venta", f"Total a cobrar: ${total:.2f}\nMetodo: {metodo}\n\n¿Confirmar?"):
            return

        # Calcular ID de venta
        id_venta = f"V_{len(self.servicio_ventas.ventas_cache) + 1}"

        venta = Venta(
            id_venta=id_venta,
            vendedor_nombre=self.usuario.nombre,
            items=self.carrito.copy(),
            total=total,
            metodo_pago=metodo
        )

        # Actualizar stock de cada producto
        todo_bien = True
        for item in self.carrito:
            ok = self.servicio_productos.actualizar_stock(
                item["id_producto"], item["cantidad"], es_venta=True
            )
            if not ok:
                todo_bien = False
                break

        if todo_bien:
            self.servicio_ventas.registrar_venta(venta)
            self.mostrar_ticket(venta)
            self.limpiar_carrito()
            self.cargar_inventario()
        else:
            messagebox.showerror("Error", "No se pudo actualizar el inventario. Revisa el stock.")

    def mostrar_ticket(self, venta):
        dialogo = ctk.CTkToplevel(self.root)
        dialogo.title("Ticket de venta")
        dialogo.geometry("450x500")
        dialogo.configure(fg_color=COLORES["fondo"])

        # FRAME PRINCIPAL
        frame = ctk.CTkFrame(
            dialogo,
            fg_color=COLORES["superficie"],
            corner_radius=15
        )
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        # HEADER
        ctk.CTkLabel(
            frame,
            text="Demo Tienda",
            font=("Arial", 24, "bold")
        ).pack(pady=(20, 5))
        ctk.CTkLabel(
            frame,
            text="Ticket de venta",
            font=("Arial", 14)
        ).pack(pady=(0, 15))

        # SEPARADOR
        ctk.CTkFrame(frame, height=1, fg_color="gray70").pack(fill="x", padx=20, pady=(0, 12))

        # INFO
        ctk.CTkLabel(frame, text=f"Folio: {venta.id_venta}").pack(anchor="w", padx=20)
        ctk.CTkLabel(frame, text=f"Fecha: {venta.fecha}").pack(anchor="w", padx=20)
        ctk.CTkLabel(frame, text=f"Vendedor: {venta.vendedor_nombre}").pack(anchor="w", padx=20, pady=(0, 15))

        # SEPARADOR
        ctk.CTkFrame(frame, height=1, fg_color="gray70").pack(fill="x", padx=20, pady=(0, 10))

        # PRODUCTOS
        for item in venta.items:
            subtotal = item["cantidad"] * item["precio_venta"]
            texto = f"{item['cantidad']}x  {item['nombre']}    ${subtotal:.2f}"
            ctk.CTkLabel(frame, text=texto).pack(anchor="w", padx=20, pady=2)

        # SEPARADOR
        ctk.CTkFrame(frame, height=1, fg_color="gray70").pack(fill="x", padx=20, pady=(10, 0))

        # TOTAL
        ctk.CTkLabel(
            frame,
            text=f"TOTAL: ${venta._total:.2f}",
            font=("Arial", 20, "bold")
        ).pack(pady=20)

        # BOTÓN
        ctk.CTkButton(
            frame,
            text="Cerrar",
            fg_color=COLORES["verde_principal"],
            hover_color=COLORES["verde_hover"],
            font=FUENTES["boton"],
            text_color="#FFFFFF",
            command=dialogo.destroy
        ).pack(pady=(0, 20))

    def cerrar_sesion(self):
        self.root.destroy()
        import customtkinter as ctk
        nueva_root = ctk.CTk()
        from gui.login_window import VentanaLogin
        VentanaLogin(nueva_root, self._iniciar_nueva_sesion)
        nueva_root.mainloop()
