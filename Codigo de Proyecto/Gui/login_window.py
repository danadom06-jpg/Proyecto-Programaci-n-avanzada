# gui/login_window.py
# Ventana de inicio de sesion - diseno limpio para verduleria

import customtkinter as ctk
from tkinter import messagebox
from gui.styles import COLORES, FUENTES
from services.auth_service import AuthService


class VentanaLogin:

    def __init__(self, root, al_iniciar_sesion):
        self.root = root
        self.al_iniciar_sesion = al_iniciar_sesion
        self.auth_service = AuthService()
        # Esta bandera evita que se ejecute iniciar_sesion dos veces
        self.sesion_iniciada = False
        self.configurar_ui()

    def configurar_ui(self):
        self.root.title("Demo Tienda - Iniciar Sesion")
        self.root.geometry("480x580")
        self.root.resizable(False, False)
        self.root.configure(fg_color=COLORES["fondo"])

        # Tarjeta central
        tarjeta = ctk.CTkFrame(
            self.root,
            fg_color=COLORES["superficie"],
            corner_radius=12,
            border_width=1,
            border_color=COLORES["borde"]
        )
        tarjeta.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.88, relheight=0.88)

        # Encabezado con color verde del logo
        encabezado = ctk.CTkFrame(tarjeta, fg_color=COLORES["verde_principal"], corner_radius=10, height=90)
        encabezado.pack(fill="x", padx=2, pady=(2, 0))
        encabezado.pack_propagate(False)

        ctk.CTkLabel(
            encabezado,
            text="Tienda de ropa y accesorios",
            font=FUENTES["pequena"],
            text_color="#FFFFFF"
        ).pack(pady=(16, 0))

        ctk.CTkLabel(
            encabezado,
            text="Demo Tienda",
            font=FUENTES["titulo"],
            text_color="#FFFFFF"
        ).pack()

        # Campos de inicio de sesion
        ctk.CTkLabel(
            tarjeta,
            text="Correo electronico",
            font=FUENTES["pequena"],
            text_color=COLORES["texto_medio"],
            anchor="w"
        ).pack(fill="x", padx=30, pady=(25, 3))

        self.entrada_email = ctk.CTkEntry(
            tarjeta,
            placeholder_text="usuario@ejemplo.com",
            height=40,
            font=FUENTES["cuerpo"],
            border_color=COLORES["borde"],
            fg_color=COLORES["fondo"]
        )
        self.entrada_email.pack(fill="x", padx=30)

        ctk.CTkLabel(
            tarjeta,
            text="Contrasena",
            font=FUENTES["pequena"],
            text_color=COLORES["texto_medio"],
            anchor="w"
        ).pack(fill="x", padx=30, pady=(15, 3))

        self.entrada_password = ctk.CTkEntry(
            tarjeta,
            placeholder_text="••••••••",
            show="*",
            height=40,
            font=FUENTES["cuerpo"],
            border_color=COLORES["borde"],
            fg_color=COLORES["fondo"]
        )
        self.entrada_password.pack(fill="x", padx=30)

        # Boton de entrar
        ctk.CTkButton(
            tarjeta,
            text="Entrar",
            height=42,
            fg_color=COLORES["verde_principal"],
            hover_color=COLORES["verde_hover"],
            font=FUENTES["boton"],
            text_color="#FFFFFF",
            command=self.iniciar_sesion
        ).pack(fill="x", padx=30, pady=(25, 5))

        # Mensaje de error
        self.etiqueta_error = ctk.CTkLabel(
            tarjeta,
            text="",
            font=FUENTES["pequena"],
            text_color=COLORES["peligro"]
        )
        self.etiqueta_error.pack()

        # Separador
        ctk.CTkFrame(tarjeta, height=1, fg_color=COLORES["borde"]).pack(fill="x", padx=30, pady=15)

        # Cuentas de prueba
        ctk.CTkLabel(
            tarjeta,
            text="Cuentas de prueba:",
            font=FUENTES["pequena"],
            text_color=COLORES["texto_claro"]
        ).pack()

        cuentas = [
            ("admin@tienda.com", "admin123", "Administrador"),
            ("empleado@tienda.com", "emp123", "Empleado"),
            ("cliente@mail.com", "cliente123", "Cliente"),
        ]

        for email, pwd, rol in cuentas:
            fila = ctk.CTkFrame(tarjeta, fg_color="transparent")
            fila.pack(pady=2)

            ctk.CTkLabel(
                fila,
                text=f"{rol}:",
                font=FUENTES["pequena"],
                text_color=COLORES["naranja"],
                width=90,
                anchor="e"
            ).pack(side="left", padx=(0, 5))

            ctk.CTkLabel(
                fila,
                text=email,
                font=FUENTES["pequena"],
                text_color=COLORES["texto_medio"]
            ).pack(side="left")

            ctk.CTkButton(
                fila,
                text="Usar",
                width=40,
                height=20,
                fg_color=COLORES["verde_claro"],
                hover_color=COLORES["verde_principal"],
                text_color="#FFFFFF",
                font=("Arial", 9),
                command=lambda e=email, p=pwd: self.autocompletar(e, p)
            ).pack(side="left", padx=5)

        # Bind para entrar con Enter
        # CAMBIO: usamos un metodo separado en vez de lambda directa
        # para poder quitarlo antes de cambiar de ventana
        self.root.bind("<Return>", self._enter_presionado)

    def _enter_presionado(self, evento):
        # Este metodo intermedio evita que el bind se dispare
        # despues de que la ventana fue destruida
        self.iniciar_sesion()

    def autocompletar(self, email, password):
        self.entrada_email.delete(0, "end")
        self.entrada_email.insert(0, email)
        self.entrada_password.delete(0, "end")
        self.entrada_password.insert(0, password)

    def iniciar_sesion(self):
        # CAMBIO: si ya se inicio sesion, no hacer nada
        # Esto evita el error cuando el bind se dispara despues de destruir la ventana
        if self.sesion_iniciada:
            return

        # Leer los campos de texto
        email = self.entrada_email.get().strip()
        password = self.entrada_password.get()

        if not email or not password:
            self.etiqueta_error.configure(text="Ingresa correo y contrasena")
            return

        usuario = self.auth_service.autenticar(email, password)

        if usuario:
            self.etiqueta_error.configure(text="")
            # CAMBIO: marcamos que ya iniciamos sesion y quitamos el bind
            # ANTES de llamar al callback, para que no se pueda ejecutar dos veces
            self.sesion_iniciada = True
            self.root.unbind("<Return>")
            self.al_iniciar_sesion(usuario)
        else:
            self.etiqueta_error.configure(text="Correo o contrasena incorrectos")
