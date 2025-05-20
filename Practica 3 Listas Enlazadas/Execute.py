from Logic import DoubleLinkedList
from Logic import Cancion
import time
import random
import os

class Lista_Reproduccion:
    def __init__(self):
        self.lista: DoubleLinkedList = DoubleLinkedList()
        self.reproduciendo: Cancion = None
        self.shuffle_mode = False
        self.shuffled_list = []
        self.paused = False
        self.segundos_transcurridos = 0

    def insertar_cancion(self):
        try:
            titulo = input("🎵 Ingrese el título de la canción que desea agregar: ")
            autor = input("👤 Ingrese el autor de la canción: ")
            duracion = int(input("⏱️ Ingrese la duración de la canción (10-15 seg): "))
            if not (10 <= duracion <= 15):
                print("⚠️ Duración fuera del rango permitido.")
                return
        except ValueError:
            print("❌ Duración inválida. Intente nuevamente.")
            return
        if self.lista.search(titulo):
            print("⚠️ La canción ya existe en la lista.")
        else:
            self.lista.append(titulo, autor, duracion)
            print("✅ Canción agregada a la lista de reproducción")

    def eliminar_cancion(self):
        titulo = input("🗑️ Ingrese el título de la canción que desea eliminar: ")
        if self.lista.search(titulo):
            if self.reproduciendo and self.reproduciendo.titulo == titulo:
                self.reproduciendo = self.siguiente_cancion(self.reproduciendo)
            self.lista.delete(titulo)
            print("✅ Canción eliminada con éxito")
        else:
            print("❌ La canción no existe en la lista")

    def siguiente_cancion(self, cancion: Cancion):
        siguiente = cancion.next
        return siguiente if siguiente else self.lista.head

    def anterior_cancion(self, cancion: Cancion):
        anterior = cancion.prev
        return anterior if anterior else self.lista.tail

    def mostrar_cancion_actual(self):
        if self.reproduciendo:
            print(f"🎶 Reproduciendo: {self.reproduciendo.titulo} - {self.reproduciendo.autor} ({self.reproduciendo.duracion}s)")
        else:
            print("🔇 No hay canción en reproducción")

    def mostrar_playlist(self):
        print("\n📜 Lista de Reproducción:")
        nodo = self.lista.head
        while nodo:
            actual = "🎧 " if self.reproduciendo and self.reproduciendo.titulo == nodo.titulo else "   "
            print(f"{actual}{nodo.titulo} - {nodo.autor} ({nodo.duracion}s)")
            nodo = nodo.next

    def activar_shuffle(self):
        self.shuffle_mode = True
        self.shuffled_list = self.lista.to_list()
        random.shuffle(self.shuffled_list)
        self.reproduciendo = self.shuffled_list.pop(0) if self.shuffled_list else None
        print("🔀 Modo aleatorio activado")

    def adelantar_durante_reproduccion(self):
        try:
            porcentaje = int(input("⏸️ Reproducción pausada. Ingrese el % a adelantar: "))
        except ValueError:
            print("❌ Porcentaje inválido")
            return False

        if not self.reproduciendo:
            print("❌ No hay canción en reproducción")
            return False

        restante = self.reproduciendo.duracion - self.segundos_transcurridos
        adelanto = int((porcentaje / 100) * self.reproduciendo.duracion)

        print(f"⏩ Adelantando {adelanto}s...")
        if adelanto >= restante:
            print("⏭️ Adelanto mayor a lo restante, pasando a la siguiente canción...")
            return True
        else:
            self.segundos_transcurridos += adelanto
            return False

    def simular_reproduccion(self):
        if not self.reproduciendo:
            self.reproduciendo = self.lista.head if not self.shuffle_mode else (self.shuffled_list.pop(0) if self.shuffled_list else None)

        if not self.reproduciendo:
            print("❌ No hay canciones para reproducir.")
            return

        while self.reproduciendo:
            self.segundos_transcurridos = 0
            print(f"\n🎵 Reproduciendo: {self.reproduciendo.titulo} - {self.reproduciendo.autor}")
            while self.segundos_transcurridos < self.reproduciendo.duracion:
                barra = "█" * self.segundos_transcurridos + "-" * (self.reproduciendo.duracion - self.segundos_transcurridos)
                print(f"[{barra}] {self.segundos_transcurridos}/{self.reproduciendo.duracion}s", end='\r')
                time.sleep(1)
                self.segundos_transcurridos += 1

                if self.check_adelantar():
                    break

            print()  # salto de línea
            if self.shuffle_mode:
                self.reproduciendo = self.shuffled_list.pop(0) if self.shuffled_list else None
            else:
                siguiente = self.siguiente_cancion(self.reproduciendo)
                self.reproduciendo = siguiente if siguiente != self.lista.head else None

        print("\n📭 Fin de la lista de reproducción. Volviendo al menú...")

    def check_adelantar(self):
        print("\n⏯️ Pulse 'a' para adelantar la canción o Enter para continuar...")
        opcion = input()
        if opcion.lower() == 'a':
            return self.adelantar_durante_reproduccion()
        return False

    def generar_subplaylist(self, titulos):
        sublista = Lista_Reproduccion()
        for titulo in titulos:
            cancion = self.lista.get_node(titulo)
            if cancion:
                sublista.lista.append(cancion.titulo, cancion.autor, cancion.duracion)
        print("🆕 Subplaylist creada.")
        usar = input("\u00bfDesea usar la subplaylist? (s/n): ").lower()
        if usar == 's':
            sublista.menu()

    def menu(self):
        opciones = {
            '1': self.insertar_cancion,
            '2': lambda: self.eliminar_cancion(),
            '3': lambda: self.set_reproduccion(self.siguiente_cancion(self.reproduciendo)),
            '4': lambda: self.set_reproduccion(self.anterior_cancion(self.reproduciendo)),
            '5': self.mostrar_cancion_actual,
            '6': self.mostrar_playlist,
            '7': self.activar_shuffle,
            '8': lambda: print("⛔ Esta opción ahora está disponible durante la reproducción. Use 'a' para adelantar."),
            '9': self.simular_reproduccion,
            '10': lambda: self.generar_subplaylist(input("Ingrese títulos separados por coma: ").split(',')),
        }
        while True:
            print("""
🎼 Menú Principal
------------------------
1. ➕ Agregar canción
2. 🗑️ Eliminar canción
3. ⏭️ Siguiente canción
4. ⏮️ Canción anterior
5. 🎧 Mostrar canción en reproducción
6. 📃 Mostrar playlist
7. 🔀 Activar modo aleatorio
8. ⏩ Adelantar canción (durante reproducción)
9. ▶️ Reproducir playlist
10. 🧩 Generar subplaylist
0. ❌ Salir
""")
            op = input("Seleccione una opción: ")
            if op == '0':
                break
            accion = opciones.get(op)
            if accion:
                accion()
            else:
                print("⚠️ Opción inválida")

    def set_reproduccion(self, cancion):
        self.reproduciendo = cancion
        self.mostrar_cancion_actual()


x = Lista_Reproduccion()

x.menu()
