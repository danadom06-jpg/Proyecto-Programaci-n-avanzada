# models/reservation.py
"""Clientes pueden apartar productos"""

from datetime import datetime, timedelta
from typing import List, Dict, Optional


class Apartado:
    """Productos apartados por un cliente"""
    
    ESTADOS = ["activo", "completado", "cancelado", "vencido"]
    
    def __init__(self, id_apartado: str, cliente_nombre: str, cliente_email: str,
                 productos: List[Dict], dias_validez: int = 2):
        """
        productos: lista de dict con {"producto_id":, "nombre":, "cantidad":, "precio_venta":}
        dias_validez: días que dura el apartado (default 3)
        """
        self.id_apartado = id_apartado
        self.cliente_nombre = cliente_nombre
        self.cliente_email = cliente_email
        self.productos = productos
        self.fecha_apartado = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.dias_validez = dias_validez
        self.fecha_limite = (datetime.now() + timedelta(days=dias_validez)).strftime("%Y-%m-%d")
        self._estado = "activo"
    
    @property
    def estado(self) -> str:
        # Verificar si está vencido automáticamente
        if self._estado == "activo" and self.esta_vencido():
            self._estado = "vencido"
        return self._estado
    
    @estado.setter
    def estado(self, valor: str):
        if valor not in self.ESTADOS:
            raise ValueError(f"Estado inválido. Use: {self.ESTADOS}")
        self._estado = valor
    
    @property
    def total_apartado(self) -> float:
        """Valor total de los productos apartados"""
        return sum(p["cantidad"] * p["precio_venta"] for p in self.productos)
    
    def esta_vencido(self) -> bool:
        """Verifica si el apartado ya expiró"""
        hoy = datetime.now().strftime("%Y-%m-%d")
        return hoy > self.fecha_limite
    
    def dias_restantes(self) -> int:
        """Días que quedan antes de que venza"""
        hoy = datetime.now()
        limite = datetime.strptime(self.fecha_limite, "%Y-%m-%d")
        dias = (limite - hoy).days
        return max(0, dias)
    
    def cancelar(self):
        """Cancela el apartado"""
        if self.estado == "activo":
            self._estado = "cancelado"
    
    def completar(self):
        """Marca el apartado como completado (ya se compró)"""
        if self.estado == "activo":
            self._estado = "completado"
    
    def to_dict(self) -> dict:
        return {
            "id_apartado": self.id_apartado,
            "cliente_nombre": self.cliente_nombre,
            "cliente_email": self.cliente_email,
            "productos": str(self.productos),
            "total": self.total_apartado,
            "fecha_apartado": self.fecha_apartado,
            "fecha_limite": self.fecha_limite,
            "dias_validez": self.dias_validez,
            "estado": self._estado
        }
    
    def __str__(self):
        return f"Apartado {self.id_apartado} - {self.cliente_nombre} - ${self.total_apartado:.2f} - {self.estado}"
    
