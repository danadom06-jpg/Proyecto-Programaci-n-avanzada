# gui/admin_window.py
# Panel del Administrador - acceso completo al sistema

import customtkinter as ctk
from tkinter import messagebox, ttk
from datetime import datetime, timedelta
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from collections import defaultdict
from gui.styles import COLORES, FUENTES
from services.product_service import ProductService
from services.sale_service import SaleService
from services.expense_service import ExpenseService
from services.reservation_service import ReservationService
from analytics.calculadora_ganancia import CalculadoraGanancia
from models.product import Producto
from models.expense import Gasto



def convertir_a_date(fecha):
    """Convierte v.fecha a un objeto date sin importar si es texto o datetime."""
    if isinstance(fecha, str):
        # Intenta varios formatos comunes
        for formato in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%Y-%m-%d"):
            try:
                return datetime.strptime(fecha, formato).date()
            except ValueError:
                continue
        return None  # si no reconoce el formato, devuelve None
    elif hasattr(fecha, "date"):
        return fecha.date()
    return None


class VentanaAdmin:

    def __init__(self, root, usuario):
        self.root = root
        self.usuario = usuario

        # Inicializar servicios
        self.servicio_productos = ProductService()
        self.servicio_ventas = SaleService(self.servicio_productos)
        self.servicio_gastos = ExpenseService()
        self.servicio_apartados = ReservationService()
        self.calculadora = CalculadoraGanancia(
            self.servicio_ventas, self.servicio_gastos, self.servicio_productos
        )

        self.configurar_ui()
        self.mostrar_dashboard()

    def configurar_ui(self):
        self.root.title(f"Demo Tienda - Administrador ({self.usuario.nombre})")
        self.root.geometry("1250x750")
        self.root.configure(fg_color=COLORES["fondo"])

        # Frame principal
        frame_principal = ctk.CTkFrame(self.root, fg_color="transparent")
        frame_principal.pack(fill="both", expand=True)

        # Panel lateral izquierdo
        self.configurar_sidebar(frame_principal)

        # Area de contenido derecha
        self.frame_contenido = ctk.CTkFrame(frame_principal, fg_color=COLORES["fondo"])
        self.frame_contenido.pack(side="right", fill="both", expand=True)

        self.configurar_encabezado()

        # Frame dinamico donde cambia el contenido
        self.frame_dinamico = ctk.CTkScrollableFrame(
            self.frame_contenido,
            fg_color="transparent"
        )
        self.frame_dinamico.pack(fill="both", expand=True, padx=15, pady=10)

    def configurar_sidebar(self, padre):
        sidebar = ctk.CTkFrame(
            padre,
            width=210,
            fg_color=COLORES["verde_principal"],
            corner_radius=0
        )
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        # Nombre del negocio
        ctk.CTkLabel(
            sidebar,
            text="Demo Tienda",
            font=FUENTES["subtitulo"],
            text_color="#FFFFFF"
        ).pack(pady=(25, 2))

        ctk.CTkLabel(
            sidebar,
            text="Panel Administrador",
            font=FUENTES["pequena"],
            text_color="#C8DDB8"
        ).pack(pady=(0, 20))

        ctk.CTkFrame(sidebar, height=1, fg_color="#5A9A50").pack(fill="x", padx=15, pady=5)

        opciones_menu = [
            ("Dashboard",       self.mostrar_dashboard),
            ("Inventario",      self.mostrar_inventario),
            ("Ventas",          self.mostrar_ventas),
            ("Gastos",          self.mostrar_gastos),
            ("Ciclo de Gastos", self.mostrar_ciclo_gastos),
            ("Apartados",       self.mostrar_apartados),
            ("Usuarios",        self.mostrar_usuarios),
        ]

        for texto, comando in opciones_menu:
            btn = ctk.CTkButton(
                sidebar,
                text=texto,
                fg_color="transparent",
                hover_color=COLORES["verde_hover"],
                anchor="w",
                font=FUENTES["cuerpo"],
                text_color="#FFFFFF",
                height=40,
                command=comando
            )
            btn.pack(fill="x", padx=8, pady=2)


    def configurar_encabezado(self):
        encabezado = ctk.CTkFrame(
            self.frame_contenido,
            fg_color=COLORES["superficie"],
            height=55,
            border_width=1,
            border_color=COLORES["borde"]
        )
        encabezado.pack(fill="x")
        encabezado.pack_propagate(False)

        ctk.CTkLabel(
            encabezado,
            text=f"Bienvenido, {self.usuario.nombre}",
            font=FUENTES["encabezado"],
            text_color=COLORES["texto_oscuro"]
        ).pack(side="left", padx=20)

        fecha = datetime.now().strftime("%d/%m/%Y")
        ctk.CTkLabel(
            encabezado,
            text=fecha,
            font=FUENTES["pequena"],
            text_color=COLORES["texto_claro"]
        ).pack(side="right", padx=20)

    def limpiar_frame_dinamico(self):
        for widget in self.frame_dinamico.winfo_children():
            widget.destroy()

    # -------------------------------------------------------------------------
    # DASHBOARD
    # -------------------------------------------------------------------------
    def mostrar_dashboard(self):
        self.limpiar_frame_dinamico()

        # Tarjetas con ventas del dia, semana y mes
        ventas_hoy = self.servicio_ventas.obtener_ventas_hoy()
        ventas_semana = self.servicio_ventas.obtener_ventas_semana()
        ventas_mes = self.servicio_ventas.obtener_ventas_mes()

        ingresos_hoy = sum(v.total for v in ventas_hoy)
        ingresos_semana = sum(v.total for v in ventas_semana)
        ingresos_mes = sum(v.total for v in ventas_mes)

        ganancia_hoy = sum(v.ganancia_neta for v in ventas_hoy)
        ganancia_semana = sum(v.ganancia_neta for v in ventas_semana)
        ganancia_mes = sum(v.ganancia_neta for v in ventas_mes)

        gastos_total = self.servicio_gastos.total_gastos()

        # --- Fila 1: Ventas ---
        ctk.CTkLabel(
            self.frame_dinamico,
            text="Ventas",
            font=FUENTES["subtitulo"],
            text_color=COLORES["texto_oscuro"]
        ).pack(anchor="w", pady=(10, 5))

        fila_ventas = ctk.CTkFrame(self.frame_dinamico, fg_color="transparent")
        fila_ventas.pack(fill="x", pady=(0, 10))

        tarjetas_ventas = [
            ("Ventas hoy",    f"${ingresos_hoy:.2f}",    f"{len(ventas_hoy)} transacciones"),
            ("Esta semana",   f"${ingresos_semana:.2f}", f"{len(ventas_semana)} transacciones"),
            ("Este mes",      f"${ingresos_mes:.2f}",    f"{len(ventas_mes)} transacciones"),
        ]

        for i, (titulo, valor, detalle) in enumerate(tarjetas_ventas):
            self._crear_tarjeta(fila_ventas, titulo, valor, detalle, COLORES["verde_principal"], i)
            fila_ventas.grid_columnconfigure(i, weight=1)

        # --- Fila 2: Ganancias ---
        ctk.CTkLabel(
            self.frame_dinamico,
            text="Ganancias",
            font=FUENTES["subtitulo"],
            text_color=COLORES["texto_oscuro"]
        ).pack(anchor="w", pady=(5, 5))

        fila_ganancias = ctk.CTkFrame(self.frame_dinamico, fg_color="transparent")
        fila_ganancias.pack(fill="x", pady=(0, 10))

        tarjetas_ganancias = [
            ("Ganancia hoy",    f"${ganancia_hoy:.2f}",    "Bruta del dia"),
            ("Ganancia semana", f"${ganancia_semana:.2f}", "Bruta de la semana"),
            ("Gastos del ciclo", f"${gastos_total:.2f}",   "Renta, luz, agua..."),
        ]

        for i, (titulo, valor, detalle) in enumerate(tarjetas_ganancias):
            color = COLORES["naranja"] if i < 2 else COLORES["peligro"]
            self._crear_tarjeta(fila_ganancias, titulo, valor, detalle, color, i)
            fila_ganancias.grid_columnconfigure(i, weight=1)

        # --- Top productos ---
        ctk.CTkLabel(
            self.frame_dinamico,
            text="Productos mas vendidos",
            font=FUENTES["subtitulo"],
            text_color=COLORES["texto_oscuro"]
        ).pack(anchor="w", pady=(5, 5))

        frame_top = ctk.CTkFrame(
            self.frame_dinamico,
            fg_color=COLORES["superficie"],
            corner_radius=8,
            border_width=1,
            border_color=COLORES["borde"]
        )
        frame_top.pack(fill="x", pady=(0, 10))

        top_productos = self.servicio_ventas.obtener_top_productos(5)

        if not top_productos:
            ctk.CTkLabel(
                frame_top,
                text="Aun no hay ventas registradas",
                font=FUENTES["cuerpo"],
                text_color=COLORES["texto_claro"]
            ).pack(pady=20)
        else:
            for i, prod in enumerate(top_productos, 1):
                fila = ctk.CTkFrame(frame_top, fg_color="transparent")
                fila.pack(fill="x", padx=15, pady=4)

                ctk.CTkLabel(
                    fila,
                    text=f"{i}.",
                    font=FUENTES["cuerpo_bold"],
                    text_color=COLORES["naranja"],
                    width=25
                ).pack(side="left")

                ctk.CTkLabel(
                    fila,
                    text=prod["nombre"],
                    font=FUENTES["cuerpo"],
                    text_color=COLORES["texto_oscuro"]
                ).pack(side="left", padx=5)

                ctk.CTkLabel(
                    fila,
                    text=f"{prod['cantidad']} unidades",
                    font=FUENTES["pequena"],
                    text_color=COLORES["texto_claro"]
                ).pack(side="right")

        # --- Seccion de Graficas ---
        ctk.CTkLabel(
            self.frame_dinamico,
            text="Analisis Visual",
            font=FUENTES["subtitulo"],
            text_color=COLORES["texto_oscuro"]
        ).pack(anchor="w", pady=(10, 5))

        frame_graficas = ctk.CTkFrame(self.frame_dinamico, fg_color="transparent")
        frame_graficas.pack(fill="x", pady=(0, 10))
        frame_graficas.grid_columnconfigure(0, weight=3)
        frame_graficas.grid_columnconfigure(1, weight=2)

        # --- Grafica 1: Ingresos vs Gastos (ultimos 7 dias) ---
        frame_lineas = ctk.CTkFrame(
            frame_graficas,
            fg_color=COLORES["superficie"],
            corner_radius=8,
            border_width=1,
            border_color=COLORES["borde"]
        )
        frame_lineas.grid(row=0, column=0, padx=(0, 6), pady=4, sticky="nsew")

        ctk.CTkLabel(
            frame_lineas,
            text="Ingresos vs Gastos (ultimos 7 dias)",
            font=FUENTES["encabezado"],
            text_color=COLORES["texto_oscuro"]
        ).pack(anchor="w", padx=15, pady=(12, 5))

        self._crear_grafica_ingresos_gastos(frame_lineas)

        # --- Grafica 2: Productos mas vendidos (barras) ---
        frame_barras = ctk.CTkFrame(
            frame_graficas,
            fg_color=COLORES["superficie"],
            corner_radius=8,
            border_width=1,
            border_color=COLORES["borde"]
        )
        frame_barras.grid(row=0, column=1, padx=(6, 0), pady=4, sticky="nsew")

        ctk.CTkLabel(
            frame_barras,
            text="Top Productos Vendidos",
            font=FUENTES["encabezado"],
            text_color=COLORES["texto_oscuro"]
        ).pack(anchor="w", padx=15, pady=(12, 5))

        self._crear_grafica_top_productos(frame_barras)

        # --- Fila 2 de graficas ---
        frame_graficas2 = ctk.CTkFrame(self.frame_dinamico, fg_color="transparent")
        frame_graficas2.pack(fill="x", pady=(0, 10))
        frame_graficas2.grid_columnconfigure(0, weight=1)
        frame_graficas2.grid_columnconfigure(1, weight=1)

        # --- Grafica 3: Ventas por hora del dia ---
        frame_horas = ctk.CTkFrame(
            frame_graficas2,
            fg_color=COLORES["superficie"],
            corner_radius=8,
            border_width=1,
            border_color=COLORES["borde"]
        )
        frame_horas.grid(row=0, column=0, padx=(0, 6), pady=4, sticky="nsew")

        ctk.CTkLabel(
            frame_horas,
            text="Ventas por Hora del Dia (hoy)",
            font=FUENTES["encabezado"],
            text_color=COLORES["texto_oscuro"]
        ).pack(anchor="w", padx=15, pady=(12, 5))

        self._crear_grafica_ventas_por_hora(frame_horas, ventas_hoy)

        # --- Grafica 4: Distribucion de ganancias (dona) ---
        frame_dona = ctk.CTkFrame(
            frame_graficas2,
            fg_color=COLORES["superficie"],
            corner_radius=8,
            border_width=1,
            border_color=COLORES["borde"]
        )
        frame_dona.grid(row=0, column=1, padx=(6, 0), pady=4, sticky="nsew")

        ctk.CTkLabel(
            frame_dona,
            text="Distribucion: Ganancias vs Costos",
            font=FUENTES["encabezado"],
            text_color=COLORES["texto_oscuro"]
        ).pack(anchor="w", padx=15, pady=(12, 5))

        self._crear_grafica_dona_ganancias(frame_dona, ingresos_mes, ganancia_mes, gastos_total)

        # Boton exportar
        ctk.CTkButton(
            self.frame_dinamico,
            text="Exportar reporte a CSV",
            fg_color=COLORES["info"],
            hover_color="#1E5080",
            font=FUENTES["boton"],
            text_color="#FFFFFF",
            command=self.exportar_reporte
        ).pack(pady=10)

    # -------------------------------------------------------------------------
    # METODOS DE GRAFICAS
    # -------------------------------------------------------------------------
    def _estilo_figura(self):
        """Retorna colores base para las graficas segun el tema."""
        bg = COLORES.get("superficie", "#FFFFFF")
        fg = COLORES.get("texto_oscuro", "#1A1A1A")
        return bg, fg

    def _crear_grafica_ingresos_gastos(self, padre):
        """Grafica de lineas: ingresos diarios vs gastos fijos (ultimos 7 dias)."""
        try:
            self._crear_grafica_ingresos_gastos_interno(padre)
        except Exception as error:
            ctk.CTkLabel(padre, text=f"Error al cargar grafica: {error}",
                         font=FUENTES["pequena"], text_color=COLORES["peligro"]).pack(pady=10)

    def _crear_grafica_ingresos_gastos_interno(self, padre):
        bg, fg = self._estilo_figura()

        # Construir datos de los ultimos 7 dias
        hoy = datetime.now().date()
        dias = [hoy - timedelta(days=i) for i in range(6, -1, -1)]
        etiquetas = [d.strftime("%d/%m") for d in dias]

        ingresos_por_dia = []
        for dia in dias:
            ventas_dia = []
            for v in self.servicio_ventas.obtener_ventas_mes():
                if not hasattr(v, "fecha"):
                    continue
                # v.fecha puede ser texto o datetime, convertir_a_date lo maneja
                fecha_venta = convertir_a_date(v.fecha)
                if fecha_venta == dia:
                    ventas_dia.append(v)
            ingresos_por_dia.append(sum(v.total for v in ventas_dia))

        # gastos_total no existe aqui, se obtiene directo del servicio
        _gastos_ciclo = self.servicio_gastos.total_gastos()
        gastos_por_dia = [(_gastos_ciclo / 30) if _gastos_ciclo > 0 else 0] * 7

        fig, ax = plt.subplots(figsize=(5.5, 2.8))
        fig.patch.set_facecolor(bg)
        ax.set_facecolor(bg)

        verde = COLORES.get("verde_principal", "#4A7C59")
        naranja = COLORES.get("naranja", "#D4742A")

        ax.plot(etiquetas, ingresos_por_dia, color=verde, linewidth=2,
                marker="o", markersize=4, label="Ingresos")
        ax.fill_between(range(len(etiquetas)), ingresos_por_dia,
                        alpha=0.15, color=verde)
        ax.plot(etiquetas, gastos_por_dia, color=naranja, linewidth=1.5,
                linestyle="--", label="Gasto diario")

        ax.set_xticks(range(len(etiquetas)))
        ax.set_xticklabels(etiquetas, fontsize=7, color=fg)
        ax.tick_params(axis="y", labelsize=7, colors=fg)
        ax.spines[["top", "right"]].set_visible(False)
        ax.spines[["left", "bottom"]].set_color(COLORES.get("borde", "#CCCCCC"))
        ax.legend(fontsize=7, facecolor=bg, labelcolor=fg, framealpha=0.6)
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"${x:,.0f}"))
        fig.tight_layout(pad=1.0)

        canvas = FigureCanvasTkAgg(fig, master=padre)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=(0, 10))
        plt.close(fig)

    def _crear_grafica_top_productos(self, padre):
        """Grafica de barras horizontales con top 5 productos."""
        try:
            self._crear_grafica_top_productos_interno(padre)
        except Exception as error:
            ctk.CTkLabel(padre, text=f"Error al cargar grafica: {error}",
                         font=FUENTES["pequena"], text_color=COLORES["peligro"]).pack(pady=10)

    def _crear_grafica_top_productos_interno(self, padre):
        bg, fg = self._estilo_figura()
        top = self.servicio_ventas.obtener_top_productos(5)

        fig, ax = plt.subplots(figsize=(4.2, 2.8))
        fig.patch.set_facecolor(bg)
        ax.set_facecolor(bg)

        if not top:
            ax.text(0.5, 0.5, "Sin ventas aun", ha="center", va="center",
                    transform=ax.transAxes, color=fg, fontsize=9)
        else:
            nombres = [p["nombre"][:18] for p in reversed(top)]
            cantidades = [p["cantidad"] for p in reversed(top)]
            colores_barras = [
                COLORES.get("verde_principal", "#4A7C59"),
                COLORES.get("verde_hover", "#5A9A50"),
                COLORES.get("naranja", "#D4742A"),
                "#8FB87A",
                "#C9A96A",
            ][:len(nombres)]

            bars = ax.barh(nombres, cantidades, color=colores_barras[::-1],
                           height=0.5, edgecolor="none")
            for bar, val in zip(bars, cantidades):
                ax.text(bar.get_width() + 0.3, bar.get_y() + bar.get_height() / 2,
                        str(val), va="center", fontsize=7, color=fg)

        ax.tick_params(labelsize=7, colors=fg)
        ax.spines[["top", "right", "left"]].set_visible(False)
        ax.spines["bottom"].set_color(COLORES.get("borde", "#CCCCCC"))
        ax.set_xlabel("Unidades vendidas", fontsize=7, color=fg)
        fig.tight_layout(pad=1.0)

        canvas = FigureCanvasTkAgg(fig, master=padre)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=(0, 10))
        plt.close(fig)

    def _crear_grafica_ventas_por_hora(self, padre, ventas_hoy):
        """Grafica de barras: distribucion de ventas segun la hora del dia."""
        try:
            self._crear_grafica_ventas_por_hora_interno(padre, ventas_hoy)
        except Exception as error:
            ctk.CTkLabel(padre, text=f"Error al cargar grafica: {error}",
                         font=FUENTES["pequena"], text_color=COLORES["peligro"]).pack(pady=10)

    def _crear_grafica_ventas_por_hora_interno(self, padre, ventas_hoy):
        bg, fg = self._estilo_figura()

        horas = defaultdict(float)
        for v in ventas_hoy:
            if not hasattr(v, "fecha"):
                continue
            # v.fecha puede ser texto o datetime
            if isinstance(v.fecha, str):
                try:
                    fecha_obj = datetime.strptime(v.fecha[:16], "%Y-%m-%d %H:%M")
                    hora = fecha_obj.hour
                except ValueError:
                    continue
            elif hasattr(v.fecha, "hour"):
                hora = v.fecha.hour
            else:
                continue
            horas[hora] += v.total

        fig, ax = plt.subplots(figsize=(4.5, 2.8))
        fig.patch.set_facecolor(bg)
        ax.set_facecolor(bg)

        if horas:
            xs = sorted(horas.keys())
            ys = [horas[h] for h in xs]
            ax.bar(xs, ys, color=COLORES.get("verde_principal", "#4A7C59"),
                   width=0.6, edgecolor="none", alpha=0.85)
            ax.set_xlabel("Hora del dia", fontsize=7, color=fg)
            ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"${x:,.0f}"))
        else:
            ax.text(0.5, 0.5, "Sin ventas hoy", ha="center", va="center",
                    transform=ax.transAxes, color=fg, fontsize=9)

        ax.tick_params(labelsize=7, colors=fg)
        ax.spines[["top", "right"]].set_visible(False)
        ax.spines[["left", "bottom"]].set_color(COLORES.get("borde", "#CCCCCC"))
        fig.tight_layout(pad=1.0)

        canvas = FigureCanvasTkAgg(fig, master=padre)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=(0, 10))
        plt.close(fig)

    def _crear_grafica_dona_ganancias(self, padre, ingresos_mes, ganancia_mes, gastos_total):
        """Grafica de dona: desglose de ingresos en costo, gasto fijo y ganancia neta."""
        try:
            self._crear_grafica_dona_ganancias_interno(padre, ingresos_mes, ganancia_mes, gastos_total)
        except Exception as error:
            ctk.CTkLabel(padre, text=f"Error al cargar grafica: {error}",
                         font=FUENTES["pequena"], text_color=COLORES["peligro"]).pack(pady=10)

    def _crear_grafica_dona_ganancias_interno(self, padre, ingresos_mes, ganancia_mes, gastos_total):
        bg, fg = self._estilo_figura()

        costo_productos = max(ingresos_mes - ganancia_mes, 0)
        ganancia_neta = max(ganancia_mes - gastos_total, 0)
        gastos_fijos = min(gastos_total, ganancia_mes)

        valores = [costo_productos, gastos_fijos, ganancia_neta]
        etiquetas = ["Costo productos", "Gastos fijos", "Ganancia neta"]
        colores_dona = [
            COLORES.get("naranja", "#D4742A"),
            COLORES.get("peligro", "#C0392B"),
            COLORES.get("verde_principal", "#4A7C59"),
        ]

        # Quitar segmentos en cero
        datos = [(v, l, c) for v, l, c in zip(valores, etiquetas, colores_dona) if v > 0]
        if not datos:
            datos = [(1, "Sin datos", "#AAAAAA")]

        valores_f, etiquetas_f, colores_f = zip(*datos)

        fig, ax = plt.subplots(figsize=(3.8, 2.8))
        fig.patch.set_facecolor(bg)
        ax.set_facecolor(bg)

        wedges, texts, autotexts = ax.pie(
            valores_f,
            labels=etiquetas_f,
            colors=colores_f,
            autopct="%1.0f%%",
            pctdistance=0.75,
            startangle=90,
            wedgeprops={"width": 0.55, "edgecolor": bg, "linewidth": 2}
        )
        for t in texts:
            t.set_fontsize(7)
            t.set_color(fg)
        for at in autotexts:
            at.set_fontsize(6)
            at.set_color("#FFFFFF")

        ax.set_aspect("equal")
        fig.tight_layout(pad=0.5)

        canvas = FigureCanvasTkAgg(fig, master=padre)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=(0, 10))
        plt.close(fig)

    def _crear_tarjeta(self, padre, titulo, valor, detalle, color, columna):
        tarjeta = ctk.CTkFrame(
            padre,
            fg_color=COLORES["superficie"],
            corner_radius=8,
            border_width=1,
            border_color=COLORES["borde"]
        )
        tarjeta.grid(row=0, column=columna, padx=6, pady=4, sticky="nsew")

        ctk.CTkFrame(tarjeta, height=4, fg_color=color, corner_radius=4).pack(fill="x")

        ctk.CTkLabel(
            tarjeta,
            text=titulo,
            font=FUENTES["pequena"],
            text_color=COLORES["texto_claro"]
        ).pack(pady=(10, 2))

        ctk.CTkLabel(
            tarjeta,
            text=valor,
            font=("Arial", 20, "bold"),
            text_color=color
        ).pack()

        ctk.CTkLabel(
            tarjeta,
            text=detalle,
            font=FUENTES["pequena"],
            text_color=COLORES["texto_claro"]
        ).pack(pady=(2, 12))

    # -------------------------------------------------------------------------
    # INVENTARIO
    # -------------------------------------------------------------------------
    def mostrar_inventario(self):
        self.limpiar_frame_dinamico()

        # Formulario para agregar producto
        frame_form = ctk.CTkFrame(
            self.frame_dinamico,
            fg_color=COLORES["superficie"],
            corner_radius=8,
            border_width=1,
            border_color=COLORES["borde"]
        )
        frame_form.pack(fill="x", pady=(0, 10))

        ctk.CTkLabel(
            frame_form,
            text="Agregar producto",
            font=FUENTES["encabezado"],
            text_color=COLORES["texto_oscuro"]
        ).pack(anchor="w", padx=15, pady=(12, 8))

        frame_campos = ctk.CTkFrame(frame_form, fg_color="transparent")
        frame_campos.pack(padx=15, pady=(0, 10))

        entradas = {}
        campos = [
            ("ID Producto",    "id_producto",    0, 0),
            ("Nombre",         "nombre",         0, 2),
            ("Categoria",      "categoria",      1, 0),
            ("Precio compra",  "precio_compra",  1, 2),
            ("Precio venta",   "precio_venta",   2, 0),
            ("Stock inicial",  "stock",          2, 2),
        ]

        for etiqueta, clave, fila, col in campos:
            ctk.CTkLabel(
                frame_campos, text=etiqueta, font=FUENTES["pequena"],
                text_color=COLORES["texto_medio"]
            ).grid(row=fila, column=col, padx=(10, 3), pady=5, sticky="w")

            entrada = ctk.CTkEntry(
                frame_campos, width=180,
                fg_color=COLORES["fondo"],
                border_color=COLORES["borde"]
            )
            entrada.grid(row=fila, column=col + 1, padx=(0, 10), pady=5)
            entradas[clave] = entrada

        def guardar_producto():
            try:
                producto = Producto(
                    id_producto=entradas["id_producto"].get().strip(),
                    nombre=entradas["nombre"].get().strip(),
                    categoria=entradas["categoria"].get().strip(),
                    precio_compra=float(entradas["precio_compra"].get()),
                    precio_venta=float(entradas["precio_venta"].get()),
                    stock=int(entradas["stock"].get())
                )
                if not producto.id_producto or not producto.nombre:
                    messagebox.showwarning("Atencion", "ID y nombre son obligatorios")
                    return

                if self.servicio_productos.agregar_producto(producto):
                    messagebox.showinfo("Listo", "Producto agregado correctamente")
                    self.mostrar_inventario()
                else:
                    messagebox.showerror("Error", "Ya existe un producto con ese ID")
            except ValueError as e:
                messagebox.showerror("Error", f"Revisa los datos: {e}")

        ctk.CTkButton(
            frame_form,
            text="Guardar producto",
            fg_color=COLORES["verde_principal"],
            hover_color=COLORES["verde_hover"],
            font=FUENTES["boton"],
            text_color="#FFFFFF",
            command=guardar_producto
        ).pack(pady=(0, 12))

        # Tabla de inventario
        frame_tabla = ctk.CTkFrame(
            self.frame_dinamico,
            fg_color=COLORES["superficie"],
            corner_radius=8,
            border_width=1,
            border_color=COLORES["borde"]
        )
        frame_tabla.pack(fill="both", expand=True)

        ctk.CTkLabel(
            frame_tabla,
            text="Inventario actual",
            font=FUENTES["encabezado"],
            text_color=COLORES["texto_oscuro"]
        ).pack(anchor="w", padx=15, pady=(12, 5))

        # Estilo para Treeview
        estilo = ttk.Style()
        estilo.configure(
            "Custom.Treeview",
            background=COLORES["superficie"],
            foreground=COLORES["texto_oscuro"],
            fieldbackground=COLORES["superficie"],
            rowheight=26,
            font=("Arial", 10)
        )
        estilo.configure(
            "Custom.Treeview.Heading",
            background=COLORES["verde_fondo"],
            foreground=COLORES["verde_principal"],
            font=("Arial", 10, "bold")
        )

        columnas = ("ID", "Nombre", "Categoria", "Compra", "Venta", "Stock", "Ganancia/u")
        tabla = ttk.Treeview(
            frame_tabla, columns=columnas, show="headings",
            height=12, style="Custom.Treeview"
        )

        anchos = [80, 180, 110, 90, 90, 70, 90]
        for col, ancho in zip(columnas, anchos):
            tabla.heading(col, text=col)
            tabla.column(col, width=ancho, anchor="center")

        productos = self.servicio_productos.listar_productos()
        for p in productos:
            tabla.insert("", "end", values=(
                p.id_producto, p.nombre, p.categoria,
                f"${p.precio_compra:.2f}", f"${p.precio_venta:.2f}",
                p.stock, f"${p.ganancia_por_unidad:.2f}"
            ))

        scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=tabla.yview)
        tabla.configure(yscrollcommand=scrollbar.set)

        tabla.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        scrollbar.pack(side="right", fill="y", pady=10)

    # -------------------------------------------------------------------------
    # VENTAS
    # -------------------------------------------------------------------------
    def mostrar_ventas(self):
        self.limpiar_frame_dinamico()

        ventas = self.servicio_ventas.listar_ventas()
        resumen = self.servicio_ventas.obtener_resumen_ventas()

        # Resumen en tarjetas
        frame_resumen = ctk.CTkFrame(
            self.frame_dinamico,
            fg_color=COLORES["superficie"],
            corner_radius=8,
            border_width=1,
            border_color=COLORES["borde"]
        )
        frame_resumen.pack(fill="x", pady=(0, 10))

        ctk.CTkLabel(
            frame_resumen,
            text="Resumen general de ventas",
            font=FUENTES["encabezado"],
            text_color=COLORES["texto_oscuro"]
        ).pack(anchor="w", padx=15, pady=(12, 8))

        fila_stats = ctk.CTkFrame(frame_resumen, fg_color="transparent")
        fila_stats.pack(fill="x", padx=15, pady=(0, 12))

        estadisticas = [
            ("Total de ventas",   str(resumen["total_ventas"])),
            ("Ingresos totales",  f"${resumen['total_ingresos']:.2f}"),
            ("Ganancia total",    f"${resumen['total_ganancia']:.2f}"),
            ("Ticket promedio",   f"${resumen['ticket_promedio']:.2f}"),
        ]

        for i, (etiqueta, valor) in enumerate(estadisticas):
            frame_stat = ctk.CTkFrame(fila_stats, fg_color=COLORES["verde_fondo"], corner_radius=6)
            frame_stat.grid(row=0, column=i, padx=5, sticky="nsew")
            fila_stats.grid_columnconfigure(i, weight=1)

            ctk.CTkLabel(frame_stat, text=etiqueta, font=FUENTES["pequena"],
                         text_color=COLORES["texto_medio"]).pack(pady=(8, 2))
            ctk.CTkLabel(frame_stat, text=valor, font=FUENTES["cuerpo_bold"],
                         text_color=COLORES["verde_principal"]).pack(pady=(0, 8))

        # Tabla de ventas
        frame_tabla = ctk.CTkFrame(
            self.frame_dinamico,
            fg_color=COLORES["superficie"],
            corner_radius=8,
            border_width=1,
            border_color=COLORES["borde"]
        )
        frame_tabla.pack(fill="both", expand=True)

        ctk.CTkLabel(
            frame_tabla,
            text="Historial de ventas",
            font=FUENTES["encabezado"],
            text_color=COLORES["texto_oscuro"]
        ).pack(anchor="w", padx=15, pady=(12, 5))

        columnas = ("ID", "Vendedor", "Total", "Ganancia", "Metodo", "Fecha")
        tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings", height=14)

        anchos = [80, 160, 90, 90, 120, 140]
        for col, ancho in zip(columnas, anchos):
            tabla.heading(col, text=col)
            tabla.column(col, width=ancho, anchor="center")

        for v in ventas:
            tabla.insert("", "end", values=(
                v.id_venta, v.vendedor_nombre,
                f"${v.total:.2f}", f"${v.ganancia_neta:.2f}",
                v.metodo_pago, v.fecha[:16]
            ))

        scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=tabla.yview)
        tabla.configure(yscrollcommand=scrollbar.set)
        tabla.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        scrollbar.pack(side="right", fill="y", pady=10)

    # -------------------------------------------------------------------------
    # GASTOS
    # -------------------------------------------------------------------------
    def mostrar_gastos(self):
        self.limpiar_frame_dinamico()

        # Formulario
        frame_form = ctk.CTkFrame(
            self.frame_dinamico,
            fg_color=COLORES["superficie"],
            corner_radius=8,
            border_width=1,
            border_color=COLORES["borde"]
        )
        frame_form.pack(fill="x", pady=(0, 10))

        ctk.CTkLabel(
            frame_form,
            text="Registrar gasto",
            font=FUENTES["encabezado"],
            text_color=COLORES["texto_oscuro"]
        ).pack(anchor="w", padx=15, pady=(12, 8))

        frame_campos = ctk.CTkFrame(frame_form, fg_color="transparent")
        frame_campos.pack(padx=15, pady=(0, 10))

        entrada_concepto = ctk.CTkEntry(
            frame_campos, placeholder_text="Concepto (ej: Renta local)",
            width=240, fg_color=COLORES["fondo"], border_color=COLORES["borde"]
        )
        entrada_concepto.grid(row=0, column=0, padx=8, pady=5)

        entrada_monto = ctk.CTkEntry(
            frame_campos, placeholder_text="Monto $",
            width=120, fg_color=COLORES["fondo"], border_color=COLORES["borde"]
        )
        entrada_monto.grid(row=0, column=1, padx=8, pady=5)

        combo_categoria = ctk.CTkComboBox(
            frame_campos,
            values=Gasto.CATEGORIAS,
            width=150
        )
        combo_categoria.set(Gasto.CATEGORIAS[0])
        combo_categoria.grid(row=0, column=2, padx=8, pady=5)

        entrada_descripcion = ctk.CTkEntry(
            frame_campos, placeholder_text="Descripcion adicional (opcional)",
            width=350, fg_color=COLORES["fondo"], border_color=COLORES["borde"]
        )
        entrada_descripcion.grid(row=1, column=0, columnspan=3, padx=8, pady=5)

        def guardar_gasto():
            concepto = entrada_concepto.get().strip()
            if not concepto:
                messagebox.showwarning("Atencion", "El concepto es obligatorio")
                return
            try:
                monto = float(entrada_monto.get())
                if monto <= 0:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Error", "Ingresa un monto valido mayor a 0")
                return

            gasto = Gasto(
                id_gasto=None,
                concepto=concepto,
                monto=monto,
                categoria=combo_categoria.get(),
                descripcion=entrada_descripcion.get()
            )
            if self.servicio_gastos.registrar_gasto(gasto):
                messagebox.showinfo("Listo", "Gasto registrado correctamente")
                self.mostrar_gastos()
            else:
                messagebox.showerror("Error", "No se pudo registrar el gasto")

        ctk.CTkButton(
            frame_form,
            text="Registrar gasto",
            fg_color=COLORES["naranja"],
            hover_color=COLORES["naranja_hover"],
            font=FUENTES["boton"],
            text_color="#FFFFFF",
            command=guardar_gasto
        ).pack(pady=(0, 12))

        # Resumen por categoria
        gastos = self.servicio_gastos.listar_gastos_actuales()
        total = self.servicio_gastos.total_gastos()
        por_categoria = self.servicio_gastos.resumen_por_categoria()

        frame_resumen = ctk.CTkFrame(
            self.frame_dinamico,
            fg_color=COLORES["superficie"],
            corner_radius=8,
            border_width=1,
            border_color=COLORES["borde"]
        )
        frame_resumen.pack(fill="x", pady=(0, 10))

        ctk.CTkLabel(
            frame_resumen,
            text=f"Total gastos del ciclo actual: ${total:.2f}",
            font=FUENTES["encabezado"],
            text_color=COLORES["peligro"]
        ).pack(anchor="w", padx=15, pady=(12, 5))

        fila_cats = ctk.CTkFrame(frame_resumen, fg_color="transparent")
        fila_cats.pack(fill="x", padx=15, pady=(0, 10))

        for cat, monto in por_categoria.items():
            ctk.CTkLabel(
                fila_cats,
                text=f"{cat}: ${monto:.2f}",
                font=FUENTES["pequena"],
                text_color=COLORES["texto_medio"]
            ).pack(side="left", padx=10)

        # Tabla de gastos
        frame_tabla = ctk.CTkFrame(
            self.frame_dinamico,
            fg_color=COLORES["superficie"],
            corner_radius=8,
            border_width=1,
            border_color=COLORES["borde"]
        )
        frame_tabla.pack(fill="both", expand=True)

        ctk.CTkLabel(
            frame_tabla,
            text="Gastos del ciclo actual",
            font=FUENTES["encabezado"],
            text_color=COLORES["texto_oscuro"]
        ).pack(anchor="w", padx=15, pady=(12, 5))

        columnas = ("ID", "Concepto", "Monto", "Categoria", "Fecha")
        tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings", height=10)

        anchos = [70, 220, 90, 110, 140]
        for col, ancho in zip(columnas, anchos):
            tabla.heading(col, text=col)
            tabla.column(col, width=ancho, anchor="center")

        for g in gastos:
            tabla.insert("", "end", values=(
                g.id_gasto, g.concepto,
                f"${g.monto:.2f}", g.categoria, g.fecha[:16]
            ))

        tabla.pack(fill="both", expand=True, padx=10, pady=10)

    # -------------------------------------------------------------------------
    # CICLO DE GASTOS
    # -------------------------------------------------------------------------
    def mostrar_ciclo_gastos(self):
        self.limpiar_frame_dinamico()

        ciclo = self.servicio_gastos.ciclo

        frame_info = ctk.CTkFrame(
            self.frame_dinamico,
            fg_color=COLORES["superficie"],
            corner_radius=8,
            border_width=1,
            border_color=COLORES["borde"]
        )
        frame_info.pack(fill="x", pady=(0, 10))

        ctk.CTkLabel(
            frame_info,
            text="Ciclo de gastos",
            font=FUENTES["encabezado"],
            text_color=COLORES["texto_oscuro"]
        ).pack(anchor="w", padx=15, pady=(12, 5))

        datos_ciclo = [
            ("Numero de ciclo:",   str(ciclo.ciclo_actual)),
            ("Inicio del ciclo:",  ciclo.fecha_inicio_ciclo[:16]),
            ("Gastos acumulados:", f"${self.servicio_gastos.total_gastos():.2f}"),
        ]

        for etiqueta, valor in datos_ciclo:
            fila = ctk.CTkFrame(frame_info, fg_color="transparent")
            fila.pack(fill="x", padx=20, pady=3)
            ctk.CTkLabel(fila, text=etiqueta, font=FUENTES["cuerpo_bold"],
                         text_color=COLORES["texto_medio"]).pack(side="left")
            ctk.CTkLabel(fila, text=valor, font=FUENTES["cuerpo"],
                         text_color=COLORES["verde_principal"]).pack(side="left", padx=10)

        def reiniciar_ciclo():
            respuesta = messagebox.askyesno(
                "Confirmar",
                "¿Reiniciar el ciclo de gastos?\n\nLos gastos actuales se guardaran en el historial."
            )
            if respuesta:
                self.servicio_gastos.reiniciar_ciclo()
                messagebox.showinfo("Listo", "Ciclo reiniciado correctamente")
                self.mostrar_ciclo_gastos()

        ctk.CTkButton(
            frame_info,
            text="Reiniciar ciclo",
            fg_color=COLORES["peligro"],
            hover_color=COLORES["peligro_hover"],
            font=FUENTES["boton"],
            text_color="#FFFFFF",
            command=reiniciar_ciclo
        ).pack(pady=12)

        # Historial de ciclos
        historial = self.servicio_gastos.obtener_historial()
        if historial:
            frame_hist = ctk.CTkFrame(
                self.frame_dinamico,
                fg_color=COLORES["superficie"],
                corner_radius=8,
                border_width=1,
                border_color=COLORES["borde"]
            )
            frame_hist.pack(fill="both", expand=True)

            ctk.CTkLabel(
                frame_hist,
                text="Historial de ciclos anteriores",
                font=FUENTES["encabezado"],
                text_color=COLORES["texto_oscuro"]
            ).pack(anchor="w", padx=15, pady=(12, 5))

            columnas = ("Ciclo", "Inicio", "Cierre", "Total Gastos")
            tabla = ttk.Treeview(frame_hist, columns=columnas, show="headings", height=8)

            for col in columnas:
                tabla.heading(col, text=col)
                tabla.column(col, width=180, anchor="center")

            for ciclo_hist in historial:
                tabla.insert("", "end", values=(
                    ciclo_hist["ciclo_numero"],
                    ciclo_hist["fecha_inicio"][:16],
                    ciclo_hist["fecha_cierre"][:16],
                    f"${ciclo_hist['total_gastos']:.2f}"
                ))

            tabla.pack(fill="both", expand=True, padx=10, pady=10)
        else:
            ctk.CTkLabel(
                self.frame_dinamico,
                text="No hay ciclos anteriores todavia",
                font=FUENTES["cuerpo"],
                text_color=COLORES["texto_claro"]
            ).pack(pady=20)

    # -------------------------------------------------------------------------
    # APARTADOS
    # -------------------------------------------------------------------------
    def mostrar_apartados(self):
        self.limpiar_frame_dinamico()

        resumen = self.servicio_apartados.obtener_resumen()

        frame_resumen = ctk.CTkFrame(
            self.frame_dinamico,
            fg_color=COLORES["superficie"],
            corner_radius=8,
            border_width=1,
            border_color=COLORES["borde"]
        )
        frame_resumen.pack(fill="x", pady=(0, 10))

        ctk.CTkLabel(
            frame_resumen,
            text="Resumen de apartados",
            font=FUENTES["encabezado"],
            text_color=COLORES["texto_oscuro"]
        ).pack(anchor="w", padx=15, pady=(12, 5))

        fila = ctk.CTkFrame(frame_resumen, fg_color="transparent")
        fila.pack(fill="x", padx=15, pady=(0, 12))

        datos = [
            ("Total",       str(resumen["total_apartados"])),
            ("Activos",     str(resumen["apartados_activos"])),
            ("Completados", str(resumen["apartados_completados"])),
            ("Valor",       f"${resumen['valor_apartados_activos']:.2f}"),
        ]

        for i, (etiqueta, valor) in enumerate(datos):
            frame_stat = ctk.CTkFrame(fila, fg_color=COLORES["verde_fondo"], corner_radius=6)
            frame_stat.grid(row=0, column=i, padx=5, sticky="nsew")
            fila.grid_columnconfigure(i, weight=1)

            ctk.CTkLabel(frame_stat, text=etiqueta, font=FUENTES["pequena"],
                         text_color=COLORES["texto_medio"]).pack(pady=(8, 2))
            ctk.CTkLabel(frame_stat, text=valor, font=FUENTES["cuerpo_bold"],
                         text_color=COLORES["verde_principal"]).pack(pady=(0, 8))

        # Tabla de apartados
        frame_tabla = ctk.CTkFrame(
            self.frame_dinamico,
            fg_color=COLORES["superficie"],
            corner_radius=8,
            border_width=1,
            border_color=COLORES["borde"]
        )
        frame_tabla.pack(fill="both", expand=True)

        ctk.CTkLabel(
            frame_tabla,
            text="Apartados activos",
            font=FUENTES["encabezado"],
            text_color=COLORES["texto_oscuro"]
        ).pack(anchor="w", padx=15, pady=(12, 5))

        columnas = ("ID", "Cliente", "Productos", "Total", "Vence", "Estado")
        tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings", height=10)

        anchos = [80, 140, 180, 80, 130, 80]
        for col, ancho in zip(columnas, anchos):
            tabla.heading(col, text=col)
            tabla.column(col, width=ancho, anchor="center")

        apartados = self.servicio_apartados.listar_apartados_activos()
        for a in apartados:
            productos_str = ", ".join([p["nombre"] for p in a.productos])
            dias = a.dias_restantes()
            tabla.insert("", "end", values=(
                a.id_apartado, a.cliente_nombre,
                productos_str[:35],
                f"${a.total_apartado:.2f}",
                f"{a.fecha_limite}",
                a.estado
            ))

        tabla.pack(fill="both", expand=True, padx=10, pady=10)

    # -------------------------------------------------------------------------
    # USUARIOS
    # -------------------------------------------------------------------------
    def mostrar_usuarios(self):
        self.limpiar_frame_dinamico()

        from services.auth_service import AuthService
        auth = AuthService()
        usuarios = auth.listar_usuarios()

        frame_tabla = ctk.CTkFrame(
            self.frame_dinamico,
            fg_color=COLORES["superficie"],
            corner_radius=8,
            border_width=1,
            border_color=COLORES["borde"]
        )
        frame_tabla.pack(fill="both", expand=True)

        ctk.CTkLabel(
            frame_tabla,
            text="Usuarios del sistema",
            font=FUENTES["encabezado"],
            text_color=COLORES["texto_oscuro"]
        ).pack(anchor="w", padx=15, pady=(12, 5))

        columnas = ("ID", "Nombre", "Email", "Rol")
        tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings", height=15)

        anchos = [60, 200, 220, 120]
        for col, ancho in zip(columnas, anchos):
            tabla.heading(col, text=col)
            tabla.column(col, width=ancho, anchor="center")

        for u in usuarios:
            tabla.insert("", "end", values=(u.id, u.nombre, u.email, u.rol))

        tabla.pack(fill="both", expand=True, padx=10, pady=10)

    # -------------------------------------------------------------------------
    # EXPORTAR / SESION
    # -------------------------------------------------------------------------
    def exportar_reporte(self):
        from tkinter import filedialog
        archivo = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV", "*.csv")],
            title="Guardar reporte"
        )
        if archivo:
            if self.calculadora.exportar_reporte_csv(archivo):
                messagebox.showinfo("Listo", f"Reporte exportado correctamente")
            else:
                messagebox.showerror("Error", "No se pudo exportar el reporte")

    def cerrar_sesion(self):
        self.root.destroy()
        import customtkinter as ctk
        nueva_root = ctk.CTk()
        from gui.login_window import VentanaLogin
        VentanaLogin(nueva_root, self._iniciar_nueva_sesion)
        nueva_root.mainloop()

"""   def _iniciar_nueva_sesion(self, usuario):
       #self.root.destroy()
        import customtkinter as ctk
        root = ctk.CTk()
        if usuario.rol == "administrador":
            VentanaAdmin(root, usuario)
        elif usuario.rol == "empleado":
            from gui.empleado_window import VentanaEmpleado
            VentanaEmpleado(root, usuario)
        else:
            from gui.cliente_window import VentanaCliente
            VentanaCliente(root, usuario)
        root.mainloop()
"""