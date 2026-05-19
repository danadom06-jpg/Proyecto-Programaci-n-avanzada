# models/user.py
"""Sistema de usuarios con 3 roles: Administrador, Empleado, Cliente"""

from datetime import datetime
from typing import List, Optional


class Usuario:
    """Clase base abstracta para todos los usuarios"""
    
    def __init__(self, nombre: str, email: str, password: str):
        self._id = None
        self._nombre = nombre
        self._email = email
        self._password = password
        self._fecha_registro = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self._activo = True
    
    @property
    def id(self):
        return self._id
    
    @id.setter
    def id(self, valor):
        self._id = valor
    
    @property
    def nombre(self):
        return self._nombre
    
    @property
    def email(self):
        return self._email
    
    @property
    def rol(self):
        return self._rol
    
    @property
    def activo(self):
        return self._activo
    
    def autenticar(self, password: str) -> bool:
        """Verifica la contraseña del usuario"""
        return self._password == password
    
    def cambiar_password(self, nueva_password: str) -> None:
        """Cambia la contraseña del usuario"""
        if len(nueva_password) < 4:
            raise ValueError("La contraseña debe tener al menos 4 caracteres")
        self._password = nueva_password
    
    def desactivar(self):
        """Desactiva el usuario (no se elimina del sistema)"""
        self._activo = False
    
    def to_dict(self) -> dict:
        """Convierte el usuario a diccionario para CSV"""
        return {
            "id": self._id,
            "nombre": self._nombre,
            "email": self._email,
            "password": self._password,
            "rol": self._rol,
            "fecha_registro": self._fecha_registro,
            "activo": self._activo,
            "extra": self._get_extra_fields()
        }
    
    def _get_extra_fields(self) -> str:
        """Método a sobrescribir para campos específicos de cada rol"""
        return ""
    
    def __str__(self):
        return f"{self._nombre} ({self._rol}) - {self._email}"


class Administrador(Usuario):
    """Administrador/Dueño de la tienda - Control total"""
    
    def __init__(self, nombre: str, email: str, password: str, codigo_admin: str = None):
        super().__init__(nombre, email, password)
        self._rol = "administrador"
        self.codigo_admin = codigo_admin or f"ADMIN_{hash(nombre) % 10000}"
    
    def _get_extra_fields(self) -> str:
        return f"codigo_admin:{self.codigo_admin}"
    
    # Permisos
    def puede_editar_inventario(self) -> bool:
        return True
    
    def puede_ver_ganancias(self) -> bool:
        return True
    
    def puede_ver_gastos(self) -> bool:
        return True
    
    def puede_registrar_gastos(self) -> bool:
        return True
    
    def puede_reiniciar_ciclo(self) -> bool:
        return True
    
    def puede_ver_todos_usuarios(self) -> bool:
        return True


class Empleado(Usuario):
    """Empleado - Solo puede ver inventario y hacer ventas"""
    
    def __init__(self, nombre: str, email: str, password: str, numero_empleado: str = None):
        super().__init__(nombre, email, password)
        self._rol = "empleado"
        self.numero_empleado = numero_empleado or f"EMP_{hash(nombre) % 10000}"
        self.ventas_realizadas: List[str] = []  # IDs de ventas
    
    def _get_extra_fields(self) -> str:
        return f"numero_empleado:{self.numero_empleado}"
    
    def registrar_venta(self, id_venta: str):
        """Registra que este empleado realizó una venta"""
        self.ventas_realizadas.append(id_venta)
    
    # Permisos
    def puede_ver_inventario(self) -> bool:
        return True
    
    def puede_registrar_ventas(self) -> bool:
        return True
    
    def puede_ver_precios_compra(self) -> bool:
        return False  # Solo ve precio de venta
    
    def puede_ver_ganancias(self) -> bool:
        return False


class Cliente(Usuario):
    """Cliente registrado - Puede apartar productos"""
    
    def __init__(self, nombre: str, email: str, password: str, telefono: str = ""):
        super().__init__(nombre, email, password)
        self._rol = "cliente"
        self.telefono = telefono
        self.apartados: List[str] = []  # IDs de apartados activos
        self.compras_realizadas: List[str] = []  # IDs de ventas
    
    def _get_extra_fields(self) -> str:
        return f"telefono:{self.telefono}"
    
    def agregar_apartado(self, id_apartado: str):
        self.apartados.append(id_apartado)
    
    def eliminar_apartado(self, id_apartado: str):
        if id_apartado in self.apartados:
            self.apartados.remove(id_apartado)
    
    # Permisos
    def puede_ver_productos(self) -> bool:
        return True
    
    def puede_apartar_productos(self) -> bool:
        return True
    
    def puede_comprar_apartados(self) -> bool:
        return True