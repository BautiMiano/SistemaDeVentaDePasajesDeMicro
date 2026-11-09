# Sistema de Venta de Pasajes de Micro

Trabajo Práctico Obligatorio de **Programación I – Algoritmos y Estructuras de Datos I** (UADE).
Docente: Lic. Ricardo Thompson.

Programa de consola en Python para gestionar la venta de pasajes de micro a distintos destinos y fechas. Permite administrar destinos, micros y viajes, vender pasajes eligiendo el asiento, buscar y modificar ventas y ver informes de recaudación. Toda la información se guarda en un archivo JSON para recuperarla la próxima vez que se abra el programa.

## Cómo ejecutarlo

Requisitos: Python 3.6 o superior. No usa módulos externos.

```bash
cd SistemaDeVentaDePasajesDeMicro
python main.py
```

El programa busca `datos.json` en la carpeta desde donde se ejecuta, así que hay que correrlo desde la carpeta del proyecto. Si el archivo no existe, arranca vacío y lo crea al guardar el primer dato.

## Archivos

| Archivo | Contenido |
|---|---|
| `main.py` | Programa principal: carga los datos y maneja los menús. |
| `Utils.py` | Estructuras de datos, constantes y todas las funciones del sistema. |
| `datos.json` | Datos guardados: destinos, micros, viajes y ventas. Trae 10 destinos y 10 micros de ejemplo. |

## Funcionalidades

**Ventas**
- Registrar la venta de un pasaje: se elige destino, viaje y asiento, y se ingresan el DNI y el nombre del pasajero. Si el DNI ya tiene compras, se reutiliza el nombre.
- Ver las ventas de un viaje.
- Buscar una venta por viaje y asiento, por DNI o por nombre, y después cancelarla o cambiar el asiento.

**Informes**
- Recaudación por destino.
- Recaudación por mes, en orden cronológico.
- Recaudación total.

**Viajes**
- Consultar disponibilidad: lista los viajes con sus lugares libres y muestra el mapa de asientos del viaje elegido.
- Registrar un viaje: destino, micro y fecha. Al crearlo se generan ventas simuladas al azar para tener datos de prueba.
- Ver los viajes programados.

**Micros y destinos**
- Ver, registrar y dar de baja micros.
- Ver, agregar y eliminar destinos con su distancia en km desde Buenos Aires.
- Al dar de baja un micro o eliminar un destino también se eliminan sus viajes y ventas.

## Reglas del sistema

- Cada micro tiene 40 asientos: 10 filas (1 a 10) por 4 columnas (A, B, C, D). Ejemplo de asiento: `3B`.
- Precio del pasaje = distancia en km × $100.
- Patente con formato `AB123CD`, sin repetir.
- DNI de 7 u 8 números, sin puntos.
- Nombre del pasajero: solo letras, con al menos nombre y apellido.
- Fecha con formato `DD/MM/AAAA`, desde hoy hasta un año hacia adelante.
- Un micro no puede tener dos viajes el mismo día.

## Temas de la materia aplicados

| Tema | Dónde se usa |
|---|---|
| Funciones | Todo el sistema está dividido en funciones dentro de `Utils.py`. |
| Matrices | Los asientos de cada viaje son una matriz de 10 × 4 (`O` libre, `X` ocupado). |
| Cadenas de caracteres | Validación de fechas con `split`, formato de nombres con `title`, f-strings y `rjust`/`ljust` para alinear tablas, precios con puntos de miles armados con rebanadas. |
| Expresiones regulares | Validación de patente, DNI y nombre con `re.search`. |
| Tuplas, conjuntos y diccionarios | Diccionario de destinos y distancias, cada viaje y venta es un diccionario, conjunto de patentes para evitar repetidas, tuplas `(año, mes)` como clave en el informe mensual. |
| Excepciones | `try/except` para datos inválidos (`ValueError`), archivo inexistente (`FileNotFoundError`), errores de disco (`OSError`) y `Ctrl+C` (`KeyboardInterrupt`). |
| Archivos | Lectura y grabación de `datos.json` con el módulo `json`. |
| Recursividad | Búsquedas de viajes y ventas (por ID, asiento, DNI y nombre). Cada búsqueda divide la lista a la mitad, así la profundidad de la recursión es log₂(n) y no da `RecursionError` aunque haya muchas ventas. |

## Formato de `datos.json`

```json
{
  "distancias": {"Mar Del Plata": 400, "Cordoba": 700},
  "micros": [{"patente": "AB122CD"}],
  "patentes": ["AB122CD"],
  "viajes": [
    {"id": 1, "destino": "Cordoba", "patente": "AB122CD",
     "fecha": "13/11/2026", "asientos": [["O", "X", "O", "O"], "..."]}
  ],
  "ventas": [
    {"viaje_id": 1, "destino": "Cordoba", "fecha": "13/11/2026",
     "patente": "AB122CD", "nombre": "Juan Perez", "dni": "30123456",
     "asiento": "1B", "precio": 70000}
  ]
}
```

En el ejemplo, `"..."` reemplaza a las otras 9 filas de la matriz de asientos. El programa guarda el archivo en una sola línea.

## Notas

- Los datos se guardan en `datos.json` cada vez que termina una operación, así que cerrar el programa con `Ctrl+C` no pierde lo que ya se completó.
- Las funciones creadas o modificadas con ayuda de IA están marcadas en el código con `#CREATED BY CLAUDE`, `#MODIFIED BY CLAUDE` y `#CLAUDE`.
