#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema Académico de Administración de Tareas
=============================================
Aplicación completa para gestionar tareas académicas con funcionalidades de:
- Agregar, ver, completar y eliminar tareas
- Almacenamiento persistente en JSON
- Alertas de vencimiento
- Estadísticas de productividad

Compatible con Google Colab y entornos locales de Python.
"""

import json
import os
from datetime import datetime, timedelta
from typing import List, Optional


# =============================================================================
# CLASE PRINCIPAL: TAREA
# =============================================================================
class Tarea:
    """
    Representa una tarea académica con sus atributos y métodos asociados.
    """

    def __init__(self, nombre: str, fecha_entrega: str, prioridad: str, estado: str = "pendiente"):
        """
        Constructor de la clase Tarea.

        Args:
            nombre: Nombre/descripción de la tarea
            fecha_entrega: Fecha límite en formato YYYY-MM-DD
            prioridad: Nivel de prioridad ("alta", "media" o "baja")
            estado: Estado de la tarea ("pendiente" o "completada")
        """
        self._nombre = nombre
        self._fecha_entrega = fecha_entrega
        self._prioridad = prioridad.lower()
        self._estado = estado.lower()

    # -------------------------------------------------------------------------
    # GETTERS (Métodos de acceso)
    # -------------------------------------------------------------------------
    def get_nombre(self) -> str:
        """Retorna el nombre de la tarea."""
        return self._nombre

    def get_fecha_entrega(self) -> str:
        """Retorna la fecha de entrega de la tarea."""
        return self._fecha_entrega

    def get_prioridad(self) -> str:
        """Retorna la prioridad de la tarea."""
        return self._prioridad

    def get_estado(self) -> str:
        """Retorna el estado de la tarea."""
        return self._estado

    # -------------------------------------------------------------------------
    # SETTERS (Métodos de modificación)
    # -------------------------------------------------------------------------
    def set_nombre(self, nombre: str) -> None:
        """Modifica el nombre de la tarea."""
        self._nombre = nombre

    def set_fecha_entrega(self, fecha_entrega: str) -> None:
        """Modifica la fecha de entrega de la tarea."""
        self._fecha_entrega = fecha_entrega

    def set_prioridad(self, prioridad: str) -> None:
        """Modifica la prioridad de la tarea."""
        self._prioridad = prioridad.lower()

    def set_estado(self, estado: str) -> None:
        """Modifica el estado de la tarea."""
        self._estado = estado.lower()

    # -------------------------------------------------------------------------
    # MÉTODOS ADICIONALES
    # -------------------------------------------------------------------------
    def __str__(self) -> str:
        """
        Representación en string de la tarea formateada.

        Returns:
            String con los datos de la tarea formateados para mostrar
        """
        # Determinar icono según prioridad
        icono_prioridad = {
            "alta": "🔴",
            "media": "🟡",
            "baja": "🟢"
        }.get(self._prioridad, "⚪")

        # Determinar icono según estado
        icono_estado = "✅" if self._estado == "completada" else "⏳"

        return (f"{icono_prioridad} {self._nombre}\n"
                f"   📅 Fecha de entrega: {self._fecha_entrega}\n"
                f"   🏷️  Prioridad: {self._prioridad.upper()}\n"
                f"   {icono_estado} Estado: {self._estado.upper()}")

    def to_dict(self) -> dict:
        """
        Convierte la tarea a un diccionario para serialización JSON.

        Returns:
            Diccionario con los atributos de la tarea
        """
        return {
            "nombre": self._nombre,
            "fecha_entrega": self._fecha_entrega,
            "prioridad": self._prioridad,
            "estado": self._estado
        }

    @classmethod
    def from_dict(cls, datos: dict) -> "Tarea":
        """
        Crea una instancia de Tarea desde un diccionario.

        Args:
            datos: Diccionario con los datos de la tarea

        Returns:
            Nueva instancia de Tarea
        """
        return cls(
            nombre=datos["nombre"],
            fecha_entrega=datos["fecha_entrega"],
            prioridad=datos["prioridad"],
            estado=datos.get("estado", "pendiente")
        )


# =============================================================================
# CLASE DE GESTIÓN: SISTEMA DE TAREAS
# =============================================================================
class SistemaTareas:
    """
    Sistema principal que gestiona la colección de tareas y su persistencia.
    """

    ARCHIVO_TAREAS = "tareas.json"

    def __init__(self):
        """
        Constructor del sistema. Carga las tareas existentes del archivo JSON.
        """
        self._tareas: List[Tarea] = []
        self.cargar_tareas()

    # -------------------------------------------------------------------------
    # MÉTODOS DE PERSISTENCIA (ALMACENAMIENTO JSON)
    # -------------------------------------------------------------------------
    def cargar_tareas(self) -> None:
        """
        Carga las tareas desde el archivo JSON.
        Si el archivo no existe o está corrupto, inicializa lista vacía.
        """
        try:
            if os.path.exists(self.ARCHIVO_TAREAS):
                with open(self.ARCHIVO_TAREAS, 'r', encoding='utf-8') as archivo:
                    datos = json.load(archivo)
                    self._tareas = [Tarea.from_dict(t) for t in datos]
                print(f"✓ Se cargaron {len(self._tareas)} tarea(s) desde el archivo.")
            else:
                print("✓ No se encontró archivo de tareas. Se creará uno nuevo.")
        except json.JSONDecodeError:
            print("⚠️  Advertencia: El archivo de tareas está corrupto. Se inicia con lista vacía.")
            self._tareas = []
        except Exception as e:
            print(f"⚠️  Error al cargar tareas: {e}")
            self._tareas = []

    def guardar_tareas(self) -> None:
        """
        Guarda todas las tareas en el archivo JSON.
        Se ejecuta automáticamente al salir del programa.
        """
        try:
            with open(self.ARCHIVO_TAREAS, 'w', encoding='utf-8') as archivo:
                json.dump([t.to_dict() for t in self._tareas], archivo, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"❌ Error al guardar tareas: {e}")

    # -------------------------------------------------------------------------
    # VALIDACIONES
    # -------------------------------------------------------------------------
    @staticmethod
    def validar_fecha(fecha: str) -> bool:
        """
        Valida que la fecha tenga el formato correcto YYYY-MM-DD.

        Args:
            fecha: String con la fecha a validar

        Returns:
            True si es válida, False en caso contrario
        """
        try:
            datetime.strptime(fecha, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    @staticmethod
    def validar_prioridad(prioridad: str) -> bool:
        """
        Valida que la prioridad sea una de las opciones permitidas.

        Args:
            prioridad: String con la prioridad a validar

        Returns:
            True si es válida, False en caso contrario
        """
        return prioridad.lower() in ["alta", "media", "baja"]

    def validar_indice_tarea(self, indice: int) -> bool:
        """
        Valida que el índice de tarea exista en la lista.

        Args:
            indice: Número de tarea (1-based)

        Returns:
            True si existe, False en caso contrario
        """
        return 1 <= indice <= len(self._tareas)

    # -------------------------------------------------------------------------
    # FUNCIONALIDADES CRUD
    # -------------------------------------------------------------------------
    def agregar_tarea(self, nombre: str, fecha_entrega: str, prioridad: str) -> None:
        """
        Agrega una nueva tarea al sistema con validaciones.

        Args:
            nombre: Nombre de la tarea
            fecha_entrega: Fecha en formato YYYY-MM-DD
            prioridad: Prioridad (alta, media, baja)

        Raises:
            ValueError: Si alguna validación falla
        """
        # Validar fecha
        if not self.validar_fecha(fecha_entrega):
            raise ValueError("La fecha debe tener el formato YYYY-MM-DD (ejemplo: 2024-12-31)")

        # Validar prioridad
        if not self.validar_prioridad(prioridad):
            raise ValueError('La prioridad debe ser "alta", "media" o "baja"')

        # Crear y agregar la tarea
        nueva_tarea = Tarea(nombre, fecha_entrega, prioridad)
        self._tareas.append(nueva_tarea)
        print(f"\n✅ Tarea agregada exitosamente: '{nombre}'")

    def ver_todas_tareas(self) -> None:
        """
        Muestra todas las tareas numeradas con sus datos completos.
        """
        if not self._tareas:
            print("\n📭 No hay tareas registradas.")
            return

        print("\n" + "=" * 50)
        print("📋 LISTA DE TAREAS")
        print("=" * 50)

        for i, tarea in enumerate(self._tareas, 1):
            print(f"\n[{i}]")
            print(tarea)
            print("-" * 40)

    def marcar_completada(self, numero_tarea: int) -> None:
        """
        Marca una tarea como completada.

        Args:
            numero_tarea: Número de la tarea (1-based)

        Raises:
            ValueError: Si el número de tarea no existe
        """
        if not self.validar_indice_tarea(numero_tarea):
            raise ValueError(f"La tarea #{numero_tarea} no existe. Hay {len(self._tareas)} tarea(s).")

        tarea = self._tareas[numero_tarea - 1]

        if tarea.get_estado() == "completada":
            print(f"\n⚠️  La tarea '{tarea.get_nombre()}' ya está completada.")
        else:
            tarea.set_estado("completada")
            print(f"\n✅ Tarea '{tarea.get_nombre()}' marcada como completada.")

    def eliminar_tarea(self, numero_tarea: int) -> None:
        """
        Elimina una tarea del sistema.

        Args:
            numero_tarea: Número de la tarea a eliminar (1-based)

        Raises:
            ValueError: Si el número de tarea no existe
        """
        if not self.validar_indice_tarea(numero_tarea):
            raise ValueError(f"La tarea #{numero_tarea} no existe. Hay {len(self._tareas)} tarea(s).")

        tarea_eliminada = self._tareas.pop(numero_tarea - 1)
        print(f"\n🗑️  Tarea '{tarea_eliminada.get_nombre()}' eliminada exitosamente.")

    # -------------------------------------------------------------------------
    # FUNCIONALIDADES DE CONSULTA Y ESTADÍSTICAS
    # -------------------------------------------------------------------------
    def ver_tareas_ordenadas(self) -> None:
        """
        Muestra las tareas ordenadas por fecha de entrega
        (de más próxima a más lejana).
        """
        if not self._tareas:
            print("\n📭 No hay tareas registradas.")
            return

        # Ordenar tareas por fecha de entrega
        tareas_ordenadas = sorted(self._tareas, key=lambda t: t.get_fecha_entrega())

        print("\n" + "=" * 50)
        print("📅 TAREAS ORDENADAS POR FECHA DE ENTREGA")
        print("=" * 50)

        for i, tarea in enumerate(tareas_ordenadas, 1):
            dias_restantes = self._calcular_dias_restantes(tarea.get_fecha_entrega())
            indicador_fecha = self._indicador_dias(dias_restantes, tarea.get_estado())

            print(f"\n[{i}] {indicador_fecha}")
            print(tarea)
            print(f"   ⏰ Días restantes: {dias_restantes}")
            print("-" * 40)

    def mostrar_alertas(self) -> None:
        """
        Muestra alertas de tareas próximas a vencer (en 3 días o menos)
        y tareas vencidas pendientes.
        """
        if not self._tareas:
            return  # No hay tareas, no mostrar nada

        hoy = datetime.now().date()
        tareas_alerta = []

        for tarea in self._tareas:
            if tarea.get_estado() == "pendiente":
                fecha_entrega = datetime.strptime(tarea.get_fecha_entrega(), "%Y-%m-%d").date()
                dias_restantes = (fecha_entrega - hoy).days

                if dias_restantes <= 3:  # Vence en 3 días o ya venció
                    tareas_alerta.append((tarea, dias_restantes))

        if tareas_alerta:
            print("\n" + "🚨" * 25)
            print("⚠️  ALERTAS DE TAREAS URGENTES")
            print("🚨" * 25)

            for tarea, dias in tareas_alerta:
                if dias < 0:
                    mensaje = f"🔴 VENCIDA hace {abs(dias)} día(s)"
                elif dias == 0:
                    mensaje = "🔴 VENCE HOY"
                elif dias == 1:
                    mensaje = "🟠 Vence mañana"
                else:
                    mensaje = f"🟡 Vence en {dias} días"

                print(f"\n   • {tarea.get_nombre()}")
                print(f"     {mensaje} (Fecha límite: {tarea.get_fecha_entrega()})")

            print("\n" + "🚨" * 25)

    def verificar_alertas_inicio(self) -> None:
        """
        Verifica y muestra alertas al iniciar el programa.
        Muestra conteo de tareas urgentes y vencidas.
        """
        if not self._tareas:
            return

        hoy = datetime.now().date()
        vencidas = 0
        proximas = 0

        for tarea in self._tareas:
            if tarea.get_estado() == "pendiente":
                fecha_entrega = datetime.strptime(tarea.get_fecha_entrega(), "%Y-%m-%d").date()
                dias_restantes = (fecha_entrega - hoy).days

                if dias_restantes < 0:
                    vencidas += 1
                elif dias_restantes <= 3:
                    proximas += 1

        if vencidas > 0 or proximas > 0:
            print("\n" + "⚠️" * 20)
            print("   🔔 NOTIFICACIONES AL INICIAR:")

            if vencidas > 0:
                print(f"   🔴 Tienes {vencidas} tarea(s) VENCIDA(S) pendiente(s)!")

            if proximas > 0:
                print(f"   🟡 Tienes {proximas} tarea(s) que vencen en los próximos 3 días.")

            print("⚠️" * 20)
            print("\nUsa la opción 6 del menú para ver los detalles.")

    def ver_estadisticas(self) -> None:
        """
        Muestra estadísticas del sistema: totales, completadas, pendientes
        y porcentaje de productividad.
        """
        total = len(self._tareas)

        if total == 0:
            print("\n📊 No hay tareas registradas para generar estadísticas.")
            return

        completadas = sum(1 for t in self._tareas if t.get_estado() == "completada")
        pendientes = total - completadas

        # Calcular porcentaje de productividad
        productividad = (completadas / total) * 100

        # Determinar emoji de productividad
        if productividad >= 80:
            emoji_prod = "🌟"
        elif productividad >= 50:
            emoji_prod = "👍"
        elif productividad >= 25:
            emoji_prod = "📈"
        else:
            emoji_prod = "💪"

        # Contar por prioridad
        prioridad_alta = sum(1 for t in self._tareas if t.get_prioridad() == "alta")
        prioridad_media = sum(1 for t in self._tareas if t.get_prioridad() == "media")
        prioridad_baja = sum(1 for t in self._tareas if t.get_prioridad() == "baja")

        print("\n" + "=" * 50)
        print("📊 ESTADÍSTICAS DEL SISTEMA")
        print("=" * 50)
        print(f"\n   📁 Total de tareas:     {total}")
        print(f"   ✅ Completadas:         {completadas}")
        print(f"   ⏳ Pendientes:          {pendientes}")
        print(f"\n   {emoji_prod} Productividad:       {productividad:.1f}%")
        print(f"\n   🔴 Prioridad Alta:      {prioridad_alta}")
        print(f"   🟡 Prioridad Media:     {prioridad_media}")
        print(f"   🟢 Prioridad Baja:      {prioridad_baja}")
        print("=" * 50)

    # -------------------------------------------------------------------------
    # MÉTODOS AUXILIARES
    # -------------------------------------------------------------------------
    def _calcular_dias_restantes(self, fecha_str: str) -> int:
        """
        Calcula los días restantes hasta una fecha.

        Args:
            fecha_str: Fecha en formato YYYY-MM-DD

        Returns:
            Número de días (negativo si ya pasó)
        """
        hoy = datetime.now().date()
        fecha = datetime.strptime(fecha_str, "%Y-%m-%d").date()
        return (fecha - hoy).days

    def _indicador_dias(self, dias: int, estado: str) -> str:
        """
        Genera un indicador visual según los días restantes.

        Args:
            dias: Días restantes (puede ser negativo)
            estado: Estado de la tarea

        Returns:
            String con indicador visual
        """
        if estado == "completada":
            return "✅"
        elif dias < 0:
            return "🔴 VENCIDA"
        elif dias == 0:
            return "🔴 HOY"
        elif dias <= 3:
            return "🟡 URGENTE"
        elif dias <= 7:
            return "🟠 PRÓXIMA"
        else:
            return "🟢 A TIEMPO"


# =============================================================================
# INTERFAZ DE USUARIO (MENÚ PRINCIPAL)
# =============================================================================
def mostrar_menu() -> None:
    """
    Muestra el menú principal del sistema.
    """
    print("\n" + "=" * 50)
    print("📚 SISTEMA ACADÉMICO DE ADMINISTRACIÓN DE TAREAS")
    print("=" * 50)
    print("\n   [1] ➕ Agregar nueva tarea")
    print("   [2] 📋 Ver todas las tareas")
    print("   [3] ✔️  Marcar tarea como completada")
    print("   [4] 🗑️  Eliminar tarea")
    print("   [5] 📅 Ver tareas ordenadas por fecha")
    print("   [6] 🚨 Mostrar alertas de vencimiento")
    print("   [7] 📊 Ver estadísticas")
    print("   [8] 🚪 Salir")
    print("\n" + "=" * 50)


def solicitar_opcion() -> int:
    """
    Solicita y valida la opción del menú.

    Returns:
        Número entero de la opción seleccionada
    """
    while True:
        try:
            opcion = input("\n👉 Seleccione una opción (1-8): ").strip()
            opcion_int = int(opcion)

            if 1 <= opcion_int <= 8:
                return opcion_int
            else:
                print("❌ Error: La opción debe estar entre 1 y 8.")

        except ValueError:
            print("❌ Error: Debe ingresar un número entero válido.")


def solicitar_datos_tarea(sistema: SistemaTareas) -> tuple:
    """
    Solicita los datos para una nueva tarea.

    Args:
        sistema: Instancia del sistema de tareas

    Returns:
        Tupla con (nombre, fecha, prioridad)
    """
    print("\n" + "-" * 40)
    print("➕ AGREGAR NUEVA TAREA")
    print("-" * 40)

    # Solicitar nombre
    nombre = input("\n📝 Nombre de la tarea: ").strip()
    while not nombre:
        print("❌ El nombre no puede estar vacío.")
        nombre = input("📝 Nombre de la tarea: ").strip()

    # Solicitar fecha
    fecha = input("📅 Fecha de entrega (YYYY-MM-DD): ").strip()

    # Solicitar prioridad
    print("\n🏷️  Prioridades disponibles:")
    print("   🔴 alta")
    print("   🟡 media")
    print("   🟢 baja")
    prioridad = input("\nSeleccione prioridad: ").strip()

    return nombre, fecha, prioridad


def solicitar_numero_tarea(operacion: str) -> int:
    """
    Solicita el número de una tarea.

    Args:
        operacion: Descripción de la operación (para mostrar al usuario)

    Returns:
        Número de tarea seleccionado
    """
    while True:
        try:
            numero = input(f"\n👉 Número de tarea a {operacion}: ").strip()
            return int(numero)
        except ValueError:
            print("❌ Error: Debe ingresar un número entero válido.")


def ejecutar_opcion(sistema: SistemaTareas, opcion: int) -> bool:
    """
    Ejecuta la acción correspondiente a la opción seleccionada.

    Args:
        sistema: Instancia del sistema de tareas
        opcion: Número de opción seleccionada

    Returns:
        False si debe salir del programa, True en caso contrario
    """
    try:
        if opcion == 1:  # Agregar tarea
            nombre, fecha, prioridad = solicitar_datos_tarea(sistema)
            sistema.agregar_tarea(nombre, fecha, prioridad)

        elif opcion == 2:  # Ver todas
            sistema.ver_todas_tareas()

        elif opcion == 3:  # Marcar completada
            if not sistema._tareas:
                print("\n📭 No hay tareas para marcar.")
                return True

            sistema.ver_todas_tareas()
            numero = solicitar_numero_tarea("completar")
            sistema.marcar_completada(numero)

        elif opcion == 4:  # Eliminar
            if not sistema._tareas:
                print("\n📭 No hay tareas para eliminar.")
                return True

            sistema.ver_todas_tareas()
            numero = solicitar_numero_tarea("eliminar")

            # Confirmar eliminación
            if 1 <= numero <= len(sistema._tareas):
                tarea = sistema._tareas[numero - 1]
                confirmar = input(f"\n⚠️  ¿Seguro que desea eliminar '{tarea.get_nombre()}'? (s/n): ").strip().lower()
                if confirmar == 's':
                    sistema.eliminar_tarea(numero)
                else:
                    print("\n✖️  Operación cancelada.")
            else:
                sistema.eliminar_tarea(numero)  # Esto lanzará el error de validación

        elif opcion == 5:  # Ver ordenadas
            sistema.ver_tareas_ordenadas()

        elif opcion == 6:  # Mostrar alertas
            sistema.mostrar_alertas()

        elif opcion == 7:  # Estadísticas
            sistema.ver_estadisticas()

        elif opcion == 8:  # Salir
            print("\n💾 Guardando tareas...")
            sistema.guardar_tareas()
            print("✅ ¡Hasta luego!")
            return False

    except ValueError as e:
        print(f"\n❌ Error de validación: {e}")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")

    return True


# =============================================================================
# FUNCIÓN PRINCIPAL
# =============================================================================
def main():
    """
    Función principal que inicia el sistema.
    """
    # Limpiar pantalla (compatible con Google Colab y terminal)
    try:
        from IPython import get_ipython
        if get_ipython() is not None:
            from IPython.display import clear_output
            clear_output(wait=True)
        else:
            os.system('cls' if os.name == 'nt' else 'clear')
    except:
        pass

    print("\n" + "🎓" * 25)
    print("   BIENVENIDO AL SISTEMA ACADÉMICO")
    print("   DE ADMINISTRACIÓN DE TAREAS")
    print("🎓" * 25)

    # Crear instancia del sistema (carga automáticamente las tareas)
    sistema = SistemaTareas()

    # Mostrar alertas al iniciar
    sistema.verificar_alertas_inicio()

    # Bucle principal del menú
    continuar = True
    while continuar:
        mostrar_menu()
        opcion = solicitar_opcion()
        continuar = ejecutar_opcion(sistema, opcion)


# =============================================================================
# PUNTO DE ENTRADA
# =============================================================================
if __name__ == "__main__":
    main()
