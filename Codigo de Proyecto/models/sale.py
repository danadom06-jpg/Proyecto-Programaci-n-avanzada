# models/sale.py
"""Venta realizada por empleado o cliente - SIN PRINTS"""

from datetime import datetime
from typing import List, Dict
import customtkinter as ctk
from gui.styles import COLORES


class Venta:
    """Representa una venta de productos"""
    
    METODOS_PAGO = ["Efectivo", "Tarjeta Débito", "Tarjeta Crédito", "Transferencia", "Vale"]
    
    def __init__(self, id_venta: str, vendedor_nombre: str, 
                 items: List[Dict], total: float, metodo_pago: str):
        self.id_venta = id_venta
        self.vendedor_nombre = vendedor_nombre
        self.items = items
        self._total = float(total)
        self.metodo_pago = metodo_pago if metodo_pago in self.METODOS_PAGO else "Efectivo"
        self.fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    @property
    def total(self) -> float:
        return self._total
    
    @property
    def costo_total_compra(self) -> float:
        return sum(item["cantidad"] * item.get("costo_compra", 0) for item in self.items)
    
    @property
    def ganancia_neta(self) -> float:
        return self._total - self.costo_total_compra
    
    @property
    def margen_ganancia(self) -> float:
        if self._total == 0:
            return 0
        return (self.ganancia_neta / self._total) * 100
    
    @property
    def total_productos(self) -> int:
        return sum(item["cantidad"] for item in self.items)
    
    def mostrar_ticket(self):
        ventana = ctk.CTkToplevel(self.root)
        ventana.title("Ticket")
        ventana.geometry("400x520")
        ventana.configure(fg_color=COLORES["fondo"])

        frame = ctk.CTkFrame(ventana, fg_color=COLORES["superficie"], corner_radius=15)
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        # HEADER
        ctk.CTkLabel(frame, text="Demo Tienda", font=("Arial", 24, "bold")).pack(pady=(20, 4))
        ctk.CTkLabel(frame, text="Ticket de venta", font=("Arial", 13)).pack(pady=(0, 14))

        # SEPARADOR
        ctk.CTkFrame(frame, height=1, fg_color="gray70").pack(fill="x", padx=20, pady=(0, 12))

        # INFO
        def fila(etiqueta, valor):
            f = ctk.CTkFrame(frame, fg_color="transparent")
            f.pack(fill="x", padx=24, pady=2)
            ctk.CTkLabel(f, text=etiqueta, font=("Arial", 12), anchor="w").pack(side="left")
            ctk.CTkLabel(f, text=valor,    font=("Arial", 12), anchor="e").pack(side="right")

        fila("Folio:",    str(self.id_venta))
        fila("Fecha:",    self.fecha)
        fila("Vendedor:", self.vendedor_nombre)

        # SEPARADOR
        ctk.CTkFrame(frame, height=1, fg_color="gray70").pack(fill="x", padx=20, pady=12)

        # PRODUCTOS
        for item in self.items:
            subtotal = item["cantidad"] * item["precio_venta"]
            fila(f"{item['cantidad']}x  {item['nombre']}", f"${subtotal:.2f}")

        # SEPARADOR
        ctk.CTkFrame(frame, height=1, fg_color="gray70").pack(fill="x", padx=20, pady=12)

        # TOTAL
        fila("TOTAL:", f"${self._total:.2f}")

        # BOTÓN
        ctk.CTkButton(frame, text="Cerrar", command=ventana.destroy).pack(pady=20)

    def to_dict(self) -> dict:
        return {
            "id_venta": self.id_venta,
            "vendedor_nombre": self.vendedor_nombre,
            "total": self._total,
            "ganancia_neta": self.ganancia_neta,
            "metodo_pago": self.metodo_pago,
            "fecha": self.fecha,
            "items": str(self.items)
        }
    
    def __str__(self):
        return f"Venta {self.id_venta} | ${self._total:.2f} | Ganancia: ${self.ganancia_neta:.2f} | {self.fecha}"
    
    