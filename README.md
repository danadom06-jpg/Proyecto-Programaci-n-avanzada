# Proyecto-Programación-avanzada
# Sistema para PYMES

Este proyecto consiste en un sistema hecho en Python para ayudar en la administración de pequeñas y medianas empresas (PYMES).

El sistema cuenta con diferentes tipos de usuarios y un dashboard donde se puede visualizar información de manera más organizada mediante gráficas e indicadores.

La aplicación fue desarrollada utilizando Python y CustomTkinter para crear una interfaz más moderna y fácil de usar.

---

# Funciones del sistema

El sistema incluye:

- Inicio de sesión
- Roles de usuario
- Dashboard principal
- Gráficas
- Ventanas diferentes según el usuario
- Interfaz gráfica moderna

Los usuarios que existen dentro del sistema son:

- Administrador
- Empleado
- Cliente

Cada uno tiene diferentes accesos y funciones dentro del programa.

### Roles
- **Administrador** (`administrador`)
  - Dashboard con métricas (ventas e ingresos del día/semana/mes, ganancias, gastos del ciclo)
  - Gestión de **Inventario** (alta de productos)
  - Visualización de **Ventas** (historial + resumen)
  - **Gastos** (registro, resumen por categoría, ciclo de gastos)
  - **Apartados** (vista del estado de apartados activos)
  - Gestión/visualización de **Usuarios**
  - Exportación de reporte a CSV

- **Empleado** (`empleado`)
  - Catálogo/búsqueda de productos
  - Doble clic para agregar productos al **carrito**
  - Cobro y registro de **ventas** (actualiza stock)
  - Generación de **ticket**

- **Cliente** (`cliente`)
  - Visualización de productos (con filtro por categoría)
  - Creación de **apartados** (reservas) indicando cantidad y días de validez
  - Visualización de **“Mis apartados”**

  ## Cuentas de prueba

En la pantalla de **Login** se muestran estas credenciales:

- **Administrador**
  - Email: `admin@tienda.com`
  - Contraseña: `admin123`

- **Empleado**
  - Email: `empleado@tienda.com`
  - Contraseña: `emp123`

- **Cliente**
  - Email: `cliente@mail.com`
  - Contraseña: `cliente123`



# Dashboard

El dashboard permite visualizar información importante de manera más visual y organizada.

Las gráficas ayudan a representar datos de una forma más sencilla para que el usuario pueda entender mejor la información del sistema.

---

# Tecnologías utilizadas

Para el desarrollo del proyecto se utilizaron las siguientes tecnologías:

- Python
- Tkinter
- CustomTkinter
- Programación Orientada a Objetos

---

# Estructura del proyecto

bash
   proyecto
 ┣  gui
 ┃   login_window.py
 ┃   admin_window.py
 ┃   empleado_window.py
 ┃   cliente_window.py
 ┃   styles.py
 ┣  data
 ┃   seed_data.py
 ┣  main.py
 ┗  README.md

 ## Observaciones
 El programa corre como una aplicación de escritorio (GUI). No requiere servidor web.
  La consistencia de la persistencia depende de los CSV presentes en `data/`.

 **Equipo**: FCC
