# models/product.py
"""Producto con precio de compra y precio de venta para cálculo de ganancias"""

from typing import Optional


class Producto:
    """Representa un producto en el inventario"""
    
    def __init__(self, id_producto: str, nombre: str, categoria: str,
                 precio_compra: float, precio_venta: float, stock: int,
                 codigo_barras: str = "", descripcion: str = ""):
        self.id_producto = id_producto
        self.nombre = nombre
        self.categoria = categoria
        self._precio_compra = float(precio_compra)
        self._precio_venta = float(precio_venta)
        self._stock = int(stock)
        self.codigo_barras = codigo_barras
        self.descripcion = descripcion
        self._activo = True
    
    # Propiedades con validación
    @property
    def precio_compra(self) -> float:
        return self._precio_compra
    
    @precio_compra.setter
    def precio_compra(self, valor: float):
        if valor < 0:
            raise ValueError("El precio de compra no puede ser negativo")
        if valor > self._precio_venta:
            raise ValueError("El precio de compra no puede ser mayor al precio de venta")
        self._precio_compra = valor
    
    @property
    def precio_venta(self) -> float:
        return self._precio_venta
    
    @precio_venta.setter
    def precio_venta(self, valor: float):
        if valor < 0:
            raise ValueError("El precio de venta no puede ser negativo")
        if valor < self._precio_compra:
            raise ValueError("El precio de venta no puede ser menor al precio de compra")
        self._precio_venta = valor
    
    @property
    def stock(self) -> int:
        return self._stock
    
    @property
    def ganancia_por_unidad(self) -> float:
        """Ganancia bruta por producto vendido"""
        return self._precio_venta - self._precio_compra
    
    @property
    def margen_ganancia(self) -> float:
        """Porcentaje de ganancia sobre precio de venta"""
        if self._precio_venta == 0:
            return 0
        return (self.ganancia_por_unidad / self._precio_venta) * 100
    
    @property
    def valor_inventario_costo(self) -> float:
        """Valor total del inventario al costo de compra"""
        return self._precio_compra * self._stock
    
    @property
    def valor_inventario_venta(self) -> float:
        """Valor potencial del inventario al precio de venta"""
        return self._precio_venta * self._stock
    
    @property
    def activo(self) -> bool:
        return self._activo
    
    def reducir_stock(self, cantidad: int) -> bool:
        """Reduce el stock, retorna True si fue exitoso"""
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser positiva")
        if cantidad > self._stock:
            return False
        self._stock -= cantidad
        return True
    
    def aumentar_stock(self, cantidad: int):
        """Aumenta el stock (reabastecimiento)"""
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser positiva")
        self._stock += cantidad
    
    def desactivar(self):
        """Desactiva el producto (no se elimina del sistema)"""
        self._activo = False
    
    def to_dict(self) -> dict:
        """Convierte a diccionario para CSV"""
        return {
            "id_producto": self.id_producto,
            "nombre": self.nombre,
            "categoria": self.categoria,
            "precio_compra": self._precio_compra,
            "precio_venta": self._precio_venta,
            "stock": self._stock,
            "codigo_barras": self.codigo_barras,
            "descripcion": self.descripcion,
            "activo": self._activo
        }
    
    def __str__(self):
        return f"{self.nombre} | Compra: ${self._precio_compra:.2f} | Venta: ${self._precio_venta:.2f} | Ganancia: ${self.ganancia_por_unidad:.2f} ({self.margen_ganancia:.1f}%) | Stock: {self._stock}"
    