# TPO_Grupo3

Trabajo Práctico Obligatorio de **Programación I – Algoritmos y Estructuras de Datos I** (UADE).
Docente: Lic. Ricardo Thompson.

Es un programa de consola en Python para manejar la venta de pasajes de micro entre distintas terminales. Se pueden cargar terminales, micros y viajes, vender pasajes eligiendo el asiento, buscar ventas para cancelarlas o cambiar el asiento, y ver informes de recaudación. Todo se guarda en `datos.json`, así que al volver a abrir el programa los datos siguen ahí.

## Cómo correrlo

Solo hace falta Python 3, sin librerías externas. Desde la carpeta del proyecto:

```bash
python main.py
```

## Archivos

- `main.py`: carga los datos y maneja los menús.
- `Utils.py`: todas las funciones del sistema.
- `datos.json`: terminales, micros, viajes y ventas guardados.

## Qué se puede hacer

- **Ventas**: vender un pasaje, ver las ventas de un viaje y buscar una venta (por asiento, DNI o nombre) para cancelarla o cambiar el asiento.
- **Informes**: recaudación por destino, por mes y total.
- **Viajes**: ver los lugares libres de cada viaje, registrar viajes nuevos y listarlos. Cuando se crea un viaje se llenan algunos asientos al azar para tener datos de prueba.
- **Micros y terminales**: dar de alta, ver y dar de baja. Si se borra un micro o una terminal, también se borran sus viajes y ventas.

Cada micro tiene 40 asientos (10 filas, columnas A a D) y el pasaje cuesta $100 por km.

## Temas de la materia que usamos

Funciones, matrices (los asientos), cadenas, expresiones regulares (patente, DNI y nombre), diccionarios, conjuntos y tuplas, excepciones, archivos JSON y recursividad (las búsquedas de viajes y ventas).
