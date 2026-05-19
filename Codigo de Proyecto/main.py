
# Punto de entrada de la aplicacion 

import customtkinter as ctk
from gui.styles import configurar_tema
from gui.login_window import VentanaLogin
from gui.admin_window import VentanaAdmin
from gui.empleado_window import VentanaEmpleado
from gui.cliente_window import VentanaCliente
from data.seed_data import crear_datos_iniciales


def limpiar_pantalla(ventana):
    """Elimina todos los widgets de la ventana actual."""
    for widget in ventana.winfo_children():
        widget.destroy()

def regresar_al_login(ventana):
    """Limpia la pantalla por completo antes de volver a montar el Login."""
    # 1. Forzamos la limpieza total de la ventana principal
    limpiar_pantalla(ventana)
    
    ventana.title("Iniciar Sesión - Don Marcelino")
    
    # 2. Volvemos a crear el Login asegurándonos de pasarle 'ventana' como master
    VentanaLogin(ventana, lambda usr: al_iniciar_sesion(ventana, usr))



def al_iniciar_sesion(root, usuario):
    """Maneja el cambio de pantalla una vez que el usuario se autentica exitosamente."""
    # ¡AQUÍ ESTÁ EL CAMBIO CLAVE!
    # En lugar de root.destroy() y crear otra ventana, limpiamos la que ya existe.
    limpiar_pantalla(root)

    # Cambiamos dinámicamente el título según el rol
    if usuario.rol == "administrador":
        root.title("Panel de Administración - Demo Tienda")
        VentanaAdmin(root, usuario)
    elif usuario.rol == "empleado":
        root.title("Panel de Empleado - Demo Tienda")
        VentanaEmpleado(root, usuario)
    else:
        root.title("Catálogo de Cliente - Demo Tienda")
        VentanaCliente(root, usuario)
    
# Inyectamos el botón de cerrar sesión al final de la ventana seleccionada

def iniciar_aplicacion():
    crear_datos_iniciales()
    configurar_tema()

    # Se crea LA ÚNICA ventana de todo el ciclo de vida del programa
    root = ctk.CTk()
    root.geometry("800x600") # Puedes definir un tamaño estándar inicial aquí
    root.title("Iniciar Sesión - Demo Tienda")

   
    VentanaLogin(root, lambda usr: al_iniciar_sesion(root, usr))
    
    # El ÚNICO mainloop de toda la aplicación
    root.mainloop()


if __name__ == "__main__":
    iniciar_aplicacion()
