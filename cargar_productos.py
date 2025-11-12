import os
import django
import random
from decimal import Decimal

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "financiero.settings")
django.setup()

from appfinanciero.models import Product

# Borra si quieres limpiar los previos
# Product.objects.all().delete()

nombres = [
    "Tornillo", "Tuerca", "Clavo", "Cemento", "Arena", "Grava", "Bloque", "Pintura",
    "Brocha", "Martillo", "Serrucho", "Cinta Métrica", "Taladro", "Cable Eléctrico",
    "Tubos PVC", "Conector", "Llave Inglesa", "Manguera", "Lija", "Pegamento",
    "Aceite", "Grasa", "Pala", "Pico", "Escoba", "Detergente", "Trapo", "Guantes",
    "Casco", "Lámpara", "Linterna", "Extensión", "Candado", "Sierra Circular",
    "Compresor", "Aspiradora", "Soldadora", "Disco Corte", "Broca", "Clavadora",
    "Tiza", "Nivel", "Cinta Aislante", "Pintura Anticorrosiva", "Esmalte", "Diluyente",
    "Mazo", "Cincel", "Taladro Inalámbrico", "Escalera", "Madera Pino", "Ladrillo",
    "Cuerda", "Cinta Doble Cara", "Tornillo Autoperforante", "Ancla", "Tuerca Mariposa",
    "Resanador", "Silicón", "Sellador", "Termofusor", "Nivel Láser", "Escuadra",
    "Metro Plegable", "Rodillo", "Cúter", "Trincheta", "Brocha Angular", "Pintura Blanca",
    "Pintura Roja", "Pintura Azul", "Pintura Verde", "Pintura Amarilla", "Arena Fina",
    "Arena Gruesa", "Cemento Gris", "Cemento Blanco", "Varilla", "Alambre", "Malla",
    "Concreto Premezclado", "Bloque Hueco", "Bloque Macizo", "Puerta Madera",
    "Puerta Metálica", "Ventana Aluminio", "Bisagra", "Cerradura", "Tubo Cobre",
    "Tubo Galvanizado", "Codo PVC", "Té PVC", "Reducción PVC", "Empaque", "Tapa PVC",
    "Grifo", "Válvula", "Llave de Paso"
]

unidades = ["unidad", "kg", "m", "litro", "pieza", "rollo", "paquete", "caja"]

productos_creados = []

for i, nombre in enumerate(nombres, start=1):
    p = Product.objects.create(
        nombre=f"{nombre} #{i}",
        descripcion=f"Producto de prueba {nombre.lower()} número {i}.",
        unidad=random.choice(unidades),
        precio_unitario=Decimal(random.uniform(1, 200)).quantize(Decimal('0.01')),
    )
    productos_creados.append(p)

print(f"✅ Se crearon {len(productos_creados)} productos de prueba.")
