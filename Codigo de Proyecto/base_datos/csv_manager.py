# data/csv_manager.py
"""Manejo de persistencia con archivos CSV - Operaciones seguras"""

import csv
import os
import json
from typing import List, Dict, Any, Optional


class CSVManager:
    """Gestor de operaciones CSV con manejo de errores"""
    
    @staticmethod
    def guardar(archivo: str, datos: List[Dict], campos: List[str]) -> bool:
        """
        Guarda datos en un archivo CSV.
        Retorna True si fue exitoso.
        """
        try:
            # Asegurar que el directorio existe
            directorio = os.path.dirname(archivo)
            if directorio and not os.path.exists(directorio):
                os.makedirs(directorio)
            
            es_nuevo = not os.path.exists(archivo)
            
            with open(archivo, mode='a', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=campos)
                if es_nuevo:
                    writer.writeheader()
                writer.writerows(datos)
            return True
        except Exception as e:
            print(f"Error guardando en {archivo}: {e}")
            return False
    
    @staticmethod
    def cargar(archivo: str) -> List[Dict]:
        """
        Carga datos desde un archivo CSV.
        Retorna lista vacía si no existe o hay error.
        """
        if not os.path.exists(archivo):
            return []
        
        try:
            with open(archivo, mode='r', newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                return list(reader)
        except Exception as e:
            print(f"Error cargando {archivo}: {e}")
            return []
    
    @staticmethod
    def sobrescribir(archivo: str, datos: List[Dict], campos: List[str]) -> bool:
        """
        Sobrescribe completamente un archivo CSV.
        Retorna True si fue exitoso.
        """
        try:
            directorio = os.path.dirname(archivo)
            if directorio and not os.path.exists(directorio):
                os.makedirs(directorio)
            
            with open(archivo, mode='w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=campos)
                writer.writeheader()
                writer.writerows(datos)
            return True
        except Exception as e:
            print(f"Error sobrescribiendo {archivo}: {e}")
            return False
    
    @staticmethod
    def buscar(archivo: str, **criterios) -> List[Dict]:
        """Busca registros que cumplan los criterios"""
        datos = CSVManager.cargar(archivo)
        resultados = []
        
        for registro in datos:
            coincide = True
            for clave, valor in criterios.items():
                if str(registro.get(clave, "")) != str(valor):
                    coincide = False
                    break
            if coincide:
                resultados.append(registro)
        
        return resultados
    
    @staticmethod
    def actualizar(archivo: str, id_campo: str, id_valor: str, nuevos_datos: Dict) -> bool:
        """Actualiza un registro por su ID"""
        datos = CSVManager.cargar(archivo)
        encontrado = False
        
        for i, registro in enumerate(datos):
            if registro.get(id_campo) == id_valor:
                datos[i].update(nuevos_datos)
                encontrado = True
                break
        
        if encontrado:
            campos = list(datos[0].keys()) if datos else list(nuevos_datos.keys())
            return CSVManager.sobrescribir(archivo, datos, campos)
        return False
    
    @staticmethod
    def eliminar(archivo: str, id_campo: str, id_valor: str) -> bool:
        """Elimina un registro por su ID"""
        datos = CSVManager.cargar(archivo)
        nuevos_datos = [d for d in datos if d.get(id_campo) != id_valor]
        
        if len(nuevos_datos) != len(datos):
            campos = list(nuevos_datos[0].keys()) if nuevos_datos else []
            return CSVManager.sobrescribir(archivo, nuevos_datos, campos)
        return False
    
