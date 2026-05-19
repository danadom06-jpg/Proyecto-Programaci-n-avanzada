# data/seed_data.py
# Crea datos iniciales para la base de datos de Don Marcelino

import os
from data.csv_manager import CSVManager


def crear_datos_iniciales() -> bool:
    """Crea datos iniciales si no existen. Retorna True si se crearon."""

    datos_creados = False

    # Usuarios iniciales
    usuarios_path = "data/users.csv"
    if not os.path.exists(usuarios_path) or os.path.getsize(usuarios_path) == 0:
        usuarios = [
            {
                "id": "1", "nombre": "Don Marcelino", "email": "admin@tienda.com",
                "password": "admin123", "rol": "administrador",
                "fecha_registro": "2025-01-01 00:00:00", "activo": "True",
                "extra": "codigo_admin:ADMIN001"
            },
            {
                "id": "2", "nombre": "Juan Perez", "email": "empleado@tienda.com",
                "password": "emp123", "rol": "empleado",
                "fecha_registro": "2025-01-01 00:00:00", "activo": "True",
                "extra": "numero_empleado:EMP001"
            },
            {
                "id": "3", "nombre": "Maria Lopez", "email": "cliente@mail.com",
                "password": "cliente123", "rol": "cliente",
                "fecha_registro": "2025-01-01 00:00:00", "activo": "True",
                "extra": "telefono:555-1234"
            }
        ]
        CSVManager.sobrescribir(
            usuarios_path, usuarios,
            ["id", "nombre", "email", "password", "rol", "fecha_registro", "activo", "extra"]
        )
        datos_creados = True

    # Productos de verduleria / fruteria
    productos_path = "data/products.csv"
    if not os.path.exists(productos_path) or os.path.getsize(productos_path) == 0:
        productos = [
            {
                "id_producto": "P001", "nombre": "Tomate", "categoria": "Verduras",
                "precio_compra": 8.00, "precio_venta": 15.00, "stock": 100,
                "codigo_barras": "750001", "descripcion": "Tomate rojo por kilo", "activo": "True"
            },
            {
                "id_producto": "P002", "nombre": "Papa", "categoria": "Tuberculos",
                "precio_compra": 5.00, "precio_venta": 10.00, "stock": 150,
                "codigo_barras": "750002", "descripcion": "Papa blanca por kilo", "activo": "True"
            },
            {
                "id_producto": "P003", "nombre": "Cebolla", "categoria": "Verduras",
                "precio_compra": 6.00, "precio_venta": 12.00, "stock": 80,
                "codigo_barras": "750003", "descripcion": "Cebolla blanca por kilo", "activo": "True"
            },
            {
                "id_producto": "P004", "nombre": "Zanahoria", "categoria": "Verduras",
                "precio_compra": 5.00, "precio_venta": 10.00, "stock": 90,
                "codigo_barras": "750004", "descripcion": "Zanahoria por kilo", "activo": "True"
            },
            {
                "id_producto": "P005", "nombre": "Manzana", "categoria": "Frutas",
                "precio_compra": 18.00, "precio_venta": 30.00, "stock": 60,
                "codigo_barras": "750005", "descripcion": "Manzana roja por kilo", "activo": "True"
            },
            {
                "id_producto": "P006", "nombre": "Naranja", "categoria": "Frutas",
                "precio_compra": 10.00, "precio_venta": 18.00, "stock": 70,
                "codigo_barras": "750006", "descripcion": "Naranja por kilo", "activo": "True"
            },
            {
                "id_producto": "P007", "nombre": "Platano", "categoria": "Frutas",
                "precio_compra": 8.00, "precio_venta": 14.00, "stock": 80,
                "codigo_barras": "750007", "descripcion": "Platano tabasco por kilo", "activo": "True"
            },
            {
                "id_producto": "P008", "nombre": "Lechuga", "categoria": "Verduras",
                "precio_compra": 6.00, "precio_venta": 12.00, "stock": 40,
                "codigo_barras": "750008", "descripcion": "Lechuga orejona", "activo": "True"
            },
        ]
        CSVManager.sobrescribir(
            productos_path, productos,
            ["id_producto", "nombre", "categoria", "precio_compra", "precio_venta",
             "stock", "codigo_barras", "descripcion", "activo"]
        )
        datos_creados = True

    # Archivos vacios si no existen
    archivos_vacios = [
        ("data/sales.csv", ["id_venta", "vendedor_nombre", "total", "ganancia_neta",
                            "metodo_pago", "fecha", "items"]),
        ("data/expenses.csv", ["id_gasto", "concepto", "monto", "categoria",
                               "descripcion", "fecha", "ciclo_id", "pagado"]),
        ("data/reservations.csv", ["id_apartado", "cliente_nombre", "cliente_email",
                                   "productos", "total", "fecha_apartado", "fecha_limite",
                                   "dias_validez", "estado"]),
    ]

    for archivo, campos in archivos_vacios:
        if not os.path.exists(archivo):
            CSVManager.sobrescribir(archivo, [], campos)
            datos_creados = True

    return datos_creados
