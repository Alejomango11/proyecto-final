# 📚 Sistema Académico de Administración de Tareas

Aplicación completa en Python para gestionar tareas académicas con funcionalidades de CRUD, alertas de vencimiento y estadísticas de productividad.

## ✨ Características

- ✅ **CRUD Completo**: Agregar, ver, completar y eliminar tareas
- 💾 **Persistencia**: Almacenamiento automático en archivo JSON
- 🔔 **Alertas Inteligentes**: Notificaciones de tareas próximas a vencer
- 📊 **Estadísticas**: Métricas de productividad y conteo por prioridad
- 🔒 **Validaciones**: Manejo robusto de errores con try/except
- 🎨 **Interfaz Amigable**: Menú en consola con emojis e indicadores visuales

## 🚀 Cómo usar en Google Colab

### Método 1: Copiar y pegar

1. Abre [Google Colab](https://colab.research.google.com/)
2. Crea un nuevo notebook
3. Copia el contenido del archivo `sistema_academico_tareas.py`
4. Pégalo en una celda de código
5. Ejecuta la celda

### Método 2: Subir archivo

1. Descarga el archivo `sistema_academico_tareas.py`
2. En Colab, haz clic en el ícono 📁 (Archivos) en el panel lateral
3. Sube el archivo arrastrándolo o con el botón "Subir"
4. Ejecuta: `exec(open('sistema_academico_tareas.py').read())`

## 📋 Menú de Opciones

| Opción | Descripción |
|--------|-------------|
| 1 | ➕ Agregar nueva tarea |
| 2 | 📋 Ver todas las tareas |
| 3 | ✔️ Marcar tarea como completada |
| 4 | 🗑️ Eliminar tarea |
| 5 | 📅 Ver tareas ordenadas por fecha |
| 6 | 🚨 Mostrar alertas de vencimiento |
| 7 | 📊 Ver estadísticas |
| 8 | 🚪 Salir y guardar |

## 📝 Formato de Datos

- **Fecha de entrega**: `YYYY-MM-DD` (ejemplo: `2024-12-31`)
- **Prioridades**: `alta`, `media` o `baja`
- **Estados**: `pendiente` o `completada`

## 🔔 Alertas Automáticas

Al iniciar, el sistema muestra:
- 🔴 Tareas vencidas pendientes
- 🟡 Tareas que vencen en los próximos 3 días

## 📊 Estadísticas

- Total de tareas
- Completadas y pendientes
- Porcentaje de productividad
- Distribución por prioridad

## 🛠️ Estructura del Código

```
Clase Tarea
├── Constructor y atributos (nombre, fecha, prioridad, estado)
├── Getters y Setters
├── Método __str__ para formateo
└── Métodos de serialización (to_dict, from_dict)

Clase SistemaTareas
├── Persistencia (cargar/guardar JSON)
├── Validaciones (fecha, prioridad, índices)
├── Operaciones CRUD
├── Consultas y estadísticas
└── Alertas de vencimiento

Funciones de Interfaz
├── mostrar_menu()
├── solicitar_opcion()
├── solicitar_datos_tarea()
├── solicitar_numero_tarea()
└── ejecutar_opcion()

Función main()
└── Bucle principal del programa
```

## 🗄️ Almacenamiento

Las tareas se guardan automáticamente en el archivo `tareas.json` en el mismo directorio del script.

## 📄 Ejemplo de tareas.json

```json
[
  {
    "nombre": "Entregar proyecto de Python",
    "fecha_entrega": "2024-06-15",
    "prioridad": "alta",
    "estado": "pendiente"
  },
  {
    "nombre": "Estudiar para examen",
    "fecha_entrega": "2024-06-10",
    "prioridad": "media",
    "estado": "completada"
  }
]
```

## ⚠️ Validaciones Implementadas

- ✅ Formato de fecha `YYYY-MM-DD`
- ✅ Prioridad válida (`alta`, `media`, `baja`)
- ✅ Número de tarea existente
- ✅ Opción de menú numérica válida
- ✅ Todos los errores muestran mensajes claros sin cerrar el programa

## 👨‍💻 Autor

Proyecto académico desarrollado como práctica de programación en Python.

---

**Nota**: Este sistema está diseñado para funcionar tanto en Google Colab como en cualquier entorno Python local con Python 3.6 o superior.
