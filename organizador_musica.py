"""
Organizador y Reproductor de Música
=====================================
- Arrastra archivos de música (mp3, wav, flac, ogg, m4a) a la ventana.
- El programa los organiza automáticamente en carpetas por Artista/Álbum
  dentro de la carpeta "Musica_Organizada".
- Muestra la información de cada canción (título, artista, álbum,
  duración, género) y permite reproducirlas.

Dependencias necesarias (instalar con pip):
    pip install tkinterdnd2 mutagen pygame

Ejecutar con:
    python organizador_musica.py
"""

import os
import shutil
import threading
import time
import tkinter as tk
from tkinter import ttk, messagebox

try:
    from tkinterdnd2 import DND_FILES, TkinterDnD
except ImportError:
    raise SystemExit(
        "Falta la librería 'tkinterdnd2'. Instálala con:\n"
        "    pip install tkinterdnd2"
    )

try:
    from mutagen import File as MutagenFile
except ImportError:
    raise SystemExit(
        "Falta la librería 'mutagen'. Instálala con:\n"
        "    pip install mutagen"
    )

try:
    import pygame
except ImportError:
    raise SystemExit(
        "Falta la librería 'pygame'. Instálala con:\n"
        "    pip install pygame"
    )


# ----------------------------------------------------------------------
# Configuración
# ----------------------------------------------------------------------
CARPETA_DESTINO = os.path.join(os.getcwd(), "Musica_Organizada")
EXTENSIONES_VALIDAS = {".mp3", ".wav", ".flac", ".ogg", ".m4a", ".wma"}

os.makedirs(CARPETA_DESTINO, exist_ok=True)


# ----------------------------------------------------------------------
# Utilidades de metadatos
# ----------------------------------------------------------------------
def limpiar_nombre(texto):
    """Elimina caracteres inválidos para nombres de carpetas/archivos."""
    if not texto:
        return "Desconocido"
    invalidos = '<>:"/\\|?*'
    for c in invalidos:
        texto = texto.replace(c, "")
    return texto.strip() or "Desconocido"


def formatear_duracion(segundos):
    if not segundos:
        return "0:00"
    m, s = divmod(int(segundos), 60)
    return f"{m}:{s:02d}"


def obtener_info(ruta_archivo):
    """Lee los metadatos de un archivo de audio con mutagen."""
    info = {
        "titulo": os.path.splitext(os.path.basename(ruta_archivo))[0],
        "artista": "Desconocido",
        "album": "Desconocido",
        "genero": "Desconocido",
        "duracion": 0,
        "duracion_txt": "0:00",
    }
    try:
        audio = MutagenFile(ruta_archivo, easy=True)
        if audio is not None:
            if audio.tags:
                info["titulo"] = audio.tags.get("title", [info["titulo"]])[0]
                info["artista"] = audio.tags.get("artist", ["Desconocido"])[0]
                info["album"] = audio.tags.get("album", ["Desconocido"])[0]
                info["genero"] = audio.tags.get("genre", ["Desconocido"])[0]
            if audio.info and hasattr(audio.info, "length"):
                info["duracion"] = audio.info.length
                info["duracion_txt"] = formatear_duracion(audio.info.length)
    except Exception as e:
        print(f"No se pudieron leer metadatos de {ruta_archivo}: {e}")
    return info


# ----------------------------------------------------------------------
# Aplicación principal
# ----------------------------------------------------------------------
class OrganizadorMusica:
    def __init__(self, root):
        self.root = root
        self.root.title("🎵 Organizador y Reproductor de Música")
        self.root.geometry("780x520")
        self.root.configure(bg="#1e1e2e")

        pygame.mixer.init()

        self.canciones = {}  # iid del treeview -> dict con info + ruta
        self.reproduciendo_iid = None
        self.pausado = False

        self._construir_interfaz()
        self._actualizar_progreso()

    # ------------------------------------------------------------------
    # Construcción de la interfaz
    # ------------------------------------------------------------------
    def _construir_interfaz(self):
        estilo = ttk.Style()
        estilo.theme_use("clam")
        estilo.configure(
            "Treeview",
            background="#2a2a3d",
            fieldbackground="#2a2a3d",
            foreground="white",
            rowheight=26,
        )
        estilo.configure("Treeview.Heading", font=("Segoe UI", 9, "bold"))

        titulo = tk.Label(
            self.root,
            text="Arrastra tus canciones aquí para organizarlas",
            font=("Segoe UI", 13, "bold"),
            bg="#1e1e2e",
            fg="white",
        )
        titulo.pack(pady=(12, 4))

        self.zona_drop = tk.Label(
            self.root,
            text="⬇  Soltar archivos de música aquí  ⬇",
            font=("Segoe UI", 11),
            bg="#313244",
            fg="#cdd6f4",
            relief="ridge",
            bd=2,
            height=3,
        )
        self.zona_drop.pack(fill="x", padx=15, pady=5)
        self.zona_drop.drop_target_register(DND_FILES)
        self.zona_drop.dnd_bind("<<Drop>>", self._on_drop)

        # Tabla de canciones
        columnas = ("titulo", "artista", "album", "genero", "duracion")
        self.tabla = ttk.Treeview(
            self.root, columns=columnas, show="headings", selectmode="browse"
        )
        encabezados = {
            "titulo": "Título",
            "artista": "Artista",
            "album": "Álbum",
            "genero": "Género",
            "duracion": "Duración",
        }
        anchos = {"titulo": 220, "artista": 150, "album": 150, "genero": 100, "duracion": 80}
        for col in columnas:
            self.tabla.heading(col, text=encabezados[col])
            self.tabla.column(col, width=anchos[col], anchor="w")
        self.tabla.pack(fill="both", expand=True, padx=15, pady=10)
        self.tabla.bind("<Double-1>", lambda e: self._reproducir_seleccion())

        # Controles de reproducción
        marco_controles = tk.Frame(self.root, bg="#1e1e2e")
        marco_controles.pack(fill="x", padx=15, pady=(0, 10))

        self.lbl_actual = tk.Label(
            marco_controles,
            text="Ninguna canción seleccionada",
            font=("Segoe UI", 10, "italic"),
            bg="#1e1e2e",
            fg="#a6adc8",
        )
        self.lbl_actual.pack(side="top", anchor="w")

        self.barra_progreso = ttk.Progressbar(
            marco_controles, orient="horizontal", mode="determinate"
        )
        self.barra_progreso.pack(fill="x", pady=5)

        botones = tk.Frame(marco_controles, bg="#1e1e2e")
        botones.pack(pady=5)

        tk.Button(
            botones, text="▶ Reproducir", command=self._reproducir_seleccion,
            bg="#89b4fa", fg="black", relief="flat", padx=10, pady=4
        ).grid(row=0, column=0, padx=4)

        tk.Button(
            botones, text="⏸ Pausar / Reanudar", command=self._pausar_reanudar,
            bg="#f9e2af", fg="black", relief="flat", padx=10, pady=4
        ).grid(row=0, column=1, padx=4)

        tk.Button(
            botones, text="⏹ Detener", command=self._detener,
            bg="#f38ba8", fg="black", relief="flat", padx=10, pady=4
        ).grid(row=0, column=2, padx=4)

        tk.Label(
            self.root,
            text=f"Carpeta de destino: {CARPETA_DESTINO}",
            font=("Segoe UI", 8),
            bg="#1e1e2e",
            fg="#6c7086",
        ).pack(side="bottom", pady=4)

    # ------------------------------------------------------------------
    # Manejo de arrastrar y soltar
    # ------------------------------------------------------------------
    def _on_drop(self, event):
        rutas = self.root.tk.splitlist(event.data)
        organizadas = 0
        for ruta in rutas:
            if os.path.isdir(ruta):
                for raiz, _, archivos in os.walk(ruta):
                    for nombre in archivos:
                        if self._procesar_archivo(os.path.join(raiz, nombre)):
                            organizadas += 1
            else:
                if self._procesar_archivo(ruta):
                    organizadas += 1

        if organizadas:
            self.zona_drop.config(text=f"✔ {organizadas} canción(es) organizada(s)")
            self.root.after(2500, lambda: self.zona_drop.config(
                text="⬇  Soltar archivos de música aquí  ⬇"))
        else:
            messagebox.showwarning(
                "Sin archivos válidos",
                "No se encontró ningún archivo de audio compatible."
            )

    def _procesar_archivo(self, ruta_origen):
        ext = os.path.splitext(ruta_origen)[1].lower()
        if ext not in EXTENSIONES_VALIDAS:
            return False

        info = obtener_info(ruta_origen)
        carpeta_artista = limpiar_nombre(info["artista"])
        carpeta_album = limpiar_nombre(info["album"])
        carpeta_final = os.path.join(CARPETA_DESTINO, carpeta_artista, carpeta_album)
        os.makedirs(carpeta_final, exist_ok=True)

        nombre_archivo = limpiar_nombre(info["titulo"]) + ext
        ruta_destino = os.path.join(carpeta_final, nombre_archivo)

        # Evitar sobrescribir si ya existe un archivo con ese nombre
        contador = 1
        base_destino = ruta_destino
        while os.path.exists(ruta_destino):
            ruta_destino = base_destino.replace(ext, f" ({contador}){ext}")
            contador += 1

        try:
            if os.path.abspath(ruta_origen) != os.path.abspath(ruta_destino):
                shutil.copy2(ruta_origen, ruta_destino)
        except Exception as e:
            print(f"Error al copiar {ruta_origen}: {e}")
            return False

        iid = self.tabla.insert(
            "", "end",
            values=(info["titulo"], info["artista"], info["album"],
                    info["genero"], info["duracion_txt"])
        )
        self.canciones[iid] = {"ruta": ruta_destino, "info": info}
        return True

    # ------------------------------------------------------------------
    # Reproducción
    # ------------------------------------------------------------------
    def _reproducir_seleccion(self):
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showinfo("Sin selección", "Selecciona una canción de la lista primero.")
            return
        iid = seleccion[0]
        datos = self.canciones[iid]

        try:
            pygame.mixer.music.load(datos["ruta"])
            pygame.mixer.music.play()
            self.reproduciendo_iid = iid
            self.pausado = False
            info = datos["info"]
            self.lbl_actual.config(
                text=f"▶ Reproduciendo: {info['titulo']} — {info['artista']} "
                     f"({info['album']}) [{info['duracion_txt']}]"
            )
            self.barra_progreso["maximum"] = info["duracion"] or 1
            self._inicio_reproduccion = time.time()
        except Exception as e:
            messagebox.showerror("Error al reproducir", str(e))

    def _pausar_reanudar(self):
        if self.reproduciendo_iid is None:
            return
        if self.pausado:
            pygame.mixer.music.unpause()
            self.pausado = False
        else:
            pygame.mixer.music.pause()
            self.pausado = True

    def _detener(self):
        pygame.mixer.music.stop()
        self.reproduciendo_iid = None
        self.pausado = False
        self.lbl_actual.config(text="Ninguna canción seleccionada")
        self.barra_progreso["value"] = 0

    def _actualizar_progreso(self):
        if self.reproduciendo_iid is not None and not self.pausado:
            transcurrido = time.time() - self._inicio_reproduccion
            self.barra_progreso["value"] = min(transcurrido, self.barra_progreso["maximum"])
            if not pygame.mixer.music.get_busy() and transcurrido > 0.5:
                # La canción terminó
                self.reproduciendo_iid = None
                self.barra_progreso["value"] = 0
                self.lbl_actual.config(text="Ninguna canción seleccionada")
        self.root.after(500, self._actualizar_progreso)


# ----------------------------------------------------------------------
# Punto de entrada
# ----------------------------------------------------------------------
if __name__ == "__main__":
    root = TkinterDnD.Tk()
    app = OrganizadorMusica(root)
    root.mainloop()
