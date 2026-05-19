# models/expense.py
"""Gastos operativos y ciclo de reinicio"""

from datetime import datetime
from typing import List, Dict, Optional


class Gasto:
    """Gasto operativo de la tienda"""
    
    CATEGORIAS = ["Renta", "Luz", "Agua", "Internet", "Sueldos", "Publicidad", "Mantenimiento", "Otros"]
    
    def __init__(self, id_gasto: str, concepto: str, monto: float, 
                 categoria: str, descripcion: str = "", fecha: str = None):
        self.id_gasto = id_gasto
        self.concepto = concepto
        self._monto = float(monto)
        self.categoria = categoria if categoria in self.CATEGORIAS else "Otros"
        self.descripcion = descripcion
        self.fecha = fecha or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.ciclo_id: Optional[int] = None
        self._pagado = True  # Por defecto, al registrar se considera pagado
    
    @property
    def monto(self) -> float:
        return self._monto
    
    @monto.setter
    def monto(self, valor: float):
        if valor < 0:
            raise ValueError("El monto no puede ser negativo")
        self._monto = valor
    
    def to_dict(self) -> dict:
        return {
            "id_gasto": self.id_gasto,
            "concepto": self.concepto,
            "monto": self._monto,
            "categoria": self.categoria,
            "descripcion": self.descripcion,
            "fecha": self.fecha,
            "ciclo_id": self.ciclo_id,
            "pagado": self._pagado
        }
    
    def __str__(self):
        return f"{self.concepto}: ${self._monto:.2f} ({self.categoria}) - {self.fecha[:10]}"


class CicloGastos:
    """
    Maneja ciclos de gastos (ej: mensuales, semanales)
    El administrador decide cuándo reiniciar el ciclo
    """
    
    def __init__(self):
        self.gastos_actuales: List[Gasto] = []
        self.gastos_historicos: List[Dict] = []
        self.ciclo_actual: int = 1
        self.fecha_inicio_ciclo: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.fondo_inicial_ciclo: float = 0.0
    
    def agregar_gasto(self, gasto: Gasto) -> None:
        """Agrega un gasto al ciclo actual"""
        gasto.ciclo_id = self.ciclo_actual
        self.gastos_actuales.append(gasto)
    
    def eliminar_gasto(self, id_gasto: str) -> bool:
        """Elimina un gasto del ciclo actual"""
        for i, g in enumerate(self.gastos_actuales):
            if g.id_gasto == id_gasto:
                del self.gastos_actuales[i]
                return True
        return False
    
    def total_gastos_ciclo(self) -> float:
        """Suma total de gastos en el ciclo actual"""
        return sum(g.monto for g in self.gastos_actuales)
    
    def total_por_categoria(self) -> Dict[str, float]:
        """Agrupa gastos por categoría"""
        resultado = {}
        for gasto in self.gastos_actuales:
            resultado[gasto.categoria] = resultado.get(gasto.categoria, 0) + gasto.monto
        return resultado
    
    def reiniciar_ciclo(self, fondo_inicial: float = 0.0) -> bool:
        """
        Reinicia el ciclo de gastos (el admin decide cuándo)
        Retorna True si el ciclo anterior tenía gastos
        """
        if self.gastos_actuales:
            # Guardar ciclo en histórico
            self.gastos_historicos.append({
                "ciclo_numero": self.ciclo_actual,
                "fecha_inicio": self.fecha_inicio_ciclo,
                "fecha_cierre": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "total_gastos": self.total_gastos_ciclo(),
                "gastos": [g.to_dict() for g in self.gastos_actuales],
                "desglose_categorias": self.total_por_categoria()
            })
            
            # Iniciar nuevo ciclo
            self.ciclo_actual += 1
            self.gastos_actuales = []
            self.fecha_inicio_ciclo = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.fondo_inicial_ciclo = fondo_inicial
            return True
        
        # Si no había gastos, igual avanzamos ciclo pero sin guardar histórico vacío
        self.ciclo_actual += 1
        self.fecha_inicio_ciclo = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.fondo_inicial_ciclo = fondo_inicial
        return False
    
    def obtener_historial(self) -> List[Dict]:
        """Retorna el historial de ciclos completados"""
        return self.gastos_historicos
    
    def obtener_resumen_historial(self) -> Dict:
        """Resumen estadístico del historial de gastos"""
        if not self.gastos_historicos:
            return {"total_ciclos": 0, "promedio_por_ciclo": 0, "mayor_gasto_ciclo": 0}
        
        totales = [c["total_gastos"] for c in self.gastos_historicos]
        return {
            "total_ciclos": len(self.gastos_historicos),
            "promedio_por_ciclo": sum(totales) / len(totales),
            "mayor_gasto_ciclo": max(totales),
            "menor_gasto_ciclo": min(totales)
        }
    
    def to_dict(self) -> dict:
        """Exporta el estado actual del ciclo"""
        return {
            "ciclo_actual": self.ciclo_actual,
            "fecha_inicio_ciclo": self.fecha_inicio_ciclo,
            "fondo_inicial": self.fondo_inicial_ciclo,
            "total_gastos_actual": self.total_gastos_ciclo(),
            "gastos_actuales": [g.to_dict() for g in self.gastos_actuales],
            "historial": self.gastos_historicos
        }
    
