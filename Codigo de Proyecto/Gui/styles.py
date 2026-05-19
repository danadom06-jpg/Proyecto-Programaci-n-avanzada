# gui/styles.py
# Colores basados en el logo de Frutas y Verduras Don Marcelino

import customtkinter as ctk

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("green")

# Paleta de colores inspirada en el logo:
# Verde olivo del circulo exterior, naranja de las frutas, crema de fondo
COLORES = {
    # Verdes (del circulo y vegetales del logo)
    "verde_principal":  "#4A7C3F",   # verde olivo oscuro
    "verde_hover":      "#3A6230",
    "verde_claro":      "#7AAD5F",   # verde mas claro para acentos
    "verde_fondo":      "#EEF4E8",   # fondo verdoso muy suave

    # Naranjas / ambar (de las frutas y el sol del logo)
    "naranja":          "#D47A1E",   # naranja tierra / ambar
    "naranja_hover":    "#B86818",
    "naranja_claro":    "#F5C06A",   # naranja claro para detalles

    # Fondo y superficies (crema del logo)
    "fondo":            "#F7F4EE",   # crema / beige muy suave
    "superficie":       "#FFFFFF",   # blanco para tarjetas
    "superficie_gris":  "#F0EDE6",   # gris cremoso para alternados

    # Texto
    "texto_oscuro":     "#2C2416",   # cafe muy oscuro (mas natural que negro puro)
    "texto_medio":      "#6B5E4A",   # cafe medio para subtitulos
    "texto_claro":      "#9E8E76",   # cafe claro para texto secundario

    # Estados
    "exito":            "#3D7A35",   # verde para confirmaciones
    "exito_hover":      "#2D5E27",
    "peligro":          "#B03A2E",   # rojo tierra
    "peligro_hover":    "#8C2D23",
    "advertencia":      "#C17F24",   # ambar para advertencias
    "info":             "#2E6EA6",   # azul moderado para info

    # Bordes
    "borde":            "#D4C9B5",   # borde calido
    "borde_oscuro":     "#A89880",
}

# Fuentes - mas simples y legibles
FUENTES = {
    "titulo":       ("Arial", 22, "bold"),
    "subtitulo":    ("Arial", 16, "bold"),
    "encabezado":   ("Arial", 13, "bold"),
    "cuerpo":       ("Arial", 12),
    "cuerpo_bold":  ("Arial", 12, "bold"),
    "pequena":      ("Arial", 10),
    "boton":        ("Arial", 12, "bold"),
}


def configurar_tema():
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("green")
