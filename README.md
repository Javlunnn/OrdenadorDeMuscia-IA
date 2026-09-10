🎵 Organizador y Reproductor de Música
Aplicación de escritorio en Python que permite arrastrar y soltar archivos de música para organizarlos automáticamente en carpetas por Artista/Álbum, y reproducirlos desde una interfaz gráfica mostrando su información (título, artista, álbum, género y duración).
---
Características
Arrastrar y soltar (drag & drop): suelta archivos o carpetas completas sobre la ventana.
Organización automática: copia cada canción a `Musica_Organizada/Artista/Álbum/` según sus metadatos.
Lectura de metadatos: título, artista, álbum, género y duración, usando `mutagen`.
Reproductor integrado: reproducir, pausar/reanudar y detener, con barra de progreso.
Formatos soportados: `.mp3`, `.wav`, `.flac`, `.ogg`, `.m4a`, `.wma`.
---
Requisitos
Python 3.12 (recomendado). Versiones muy recientes como 3.14 pueden no tener instaladores precompilados de `pygame` todavía.
Librerías:
`tkinterdnd2` — soporte de arrastrar y soltar en Tkinter.
`mutagen` — lectura de metadatos de audio.
`pygame` — reproducción de audio.
---
Instalación
Se recomienda usar un entorno virtual para evitar conflictos con otras instalaciones de Python.
```bash
# Crear entorno virtual (usando Python 3.12)
py -3.12 -m venv venv

# Activar el entorno virtual
# En Windows:
venv\Scripts\activate
# En macOS/Linux:
source venv/bin/activate

# Instalar dependencias
pip install tkinterdnd2 mutagen pygame
```
En macOS puede ser necesario instalar `tkinter` por separado:
```bash
brew install python-tk
```
---
Uso
Con el entorno virtual activado, ejecuta:
```bash
python organizador_musica.py
```
Se abrirá una ventana con un recuadro que dice "Soltar archivos de música aquí".
Arrastra uno o varios archivos de audio (o una carpeta completa) sobre ese recuadro.
Las canciones organizadas aparecerán en la tabla con su información.
Selecciona una canción y usa los botones ▶ Reproducir, ⏸ Pausar/Reanudar o ⏹ Detener. También puedes hacer doble clic sobre una fila para reproducirla directamente.
Los archivos organizados se guardan (copiados, no movidos) dentro de la carpeta `Musica_Organizada`, en la misma ubicación donde ejecutes el script, siguiendo la estructura:
```
Musica_Organizada/
└── Nombre del Artista/
    └── Nombre del Álbum/
        └── Título de la canción.mp3
```
Si una canción no tiene metadatos, se clasifica en carpetas llamadas `Desconocido` y usa el nombre del archivo como título.
---
Solución de problemas
El arrastrar y soltar no funciona / no entra ningún archivo
No ejecutes la terminal como Administrador: Windows bloquea el arrastre desde el Explorador (que corre sin privilegios) hacia una app en modo administrador.
Verifica que `tkinterdnd2` esté instalado en el entorno activo: `pip show tkinterdnd2`.
Prueba arrastrar un archivo desde una carpeta local normal (no desde un ZIP ni desde archivos "solo en la nube" de OneDrive).
Error al instalar `pygame` (falla compilando desde código fuente)
Suele pasar en versiones muy nuevas de Python que aún no tienen instalador precompilado. Usa Python 3.12 en un entorno virtual, como se indica en la sección de instalación.
No se reproduce el audio
Confirma que el archivo no esté dañado y que el formato esté entre los soportados.
Revisa que ninguna otra aplicación tenga bloqueado el dispositivo de audio.
---
Notas
Los archivos originales no se eliminan: el script los copia a la nueva carpeta organizada.
Si ya existe un archivo con el mismo nombre en el destino, se guarda con un sufijo numérico para no sobrescribirlo, por ejemplo `Canción (1).mp3`.
