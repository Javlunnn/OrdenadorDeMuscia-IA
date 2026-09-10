"""
=============================================================================
CATÁLOGO DEFINITIVO Y MODULAR DE UTILIDADES CON TKINTER Y TTK
=============================================================================
Este archivo contiene ejemplos prácticos, completos y totalmente modulares
de lo que puedes construir con la librería Tkinter en Python.

Cada sección está encapsulada en una clase independiente para que puedas
copiar y pegar cualquier utilidad directamente en tu propio proyecto.

Al ejecutar este archivo, se abre un panel interactivo tipo Dashboard
con navegación lateral para probar en vivo todas las 15 utilidades:

 1. Formularios y Controles Básicos (Entry, Passwords, Combobox, Check, Radio)
 2. Diálogos del Sistema (messagebox, filedialog, colorchooser)
 3. Tabla de Datos Avanzada (ttk.Treeview con columnas, scroll y eventos)
 4. Canvas, Gráficos y Animación en Bucle (after())
 5. Barras de Progreso y Multihilos (Threading para no congelar la GUI)
 6. Menús Emergentes (Clic Derecho), Barra de Menú y Atajos de Teclado
 7. Ventanas Secundarias Libres y Modales (tk.Toplevel con grab_set)
 8. Validación en Tiempo Real en Entradas (validate='key', números, longitud)
 9. Deslizadores (Scale), Spinbox y Transferencia entre Listbox
10. Paneles Divisores Ajustables (ttk.PanedWindow redimensionable)
11. Editor de Texto Enriquecido con Tags, Formato y Buscador
12. Tooltips (Consejos Flotantes al pasar el ratón) y Portapapeles (Clipboard)
13. Diálogos de Entrada Rápida (simpledialog: texto, enteros, decimales)
14. Arrastrar y Soltar Objetos en Lienzo (Drag & Drop en Canvas)
15. Selector de Temas y Estilos Dinámicos (ttk.Style)
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, colorchooser, simpledialog
import threading
import time
import random
import re


# =============================================================================
# 1. FORMULARIOS Y CONTROLES BÁSICOS
# =============================================================================
class UtilidadControlesBasicos(ttk.Frame):
    """Muestra cómo capturar texto, selecciones, opciones booleanas y contraseñas."""
    def __init__(self, parent):
        super().__init__(parent, padding=15)
        
        ttk.Label(self, text="1. Campo de texto estándar (Entry):").pack(anchor="w", pady=(0, 2))
        self.entry_nombre = ttk.Entry(self, width=32)
        self.entry_nombre.insert(0, "Escribe tu nombre...")
        self.entry_nombre.pack(anchor="w", pady=(0, 10))

        ttk.Label(self, text="2. Contraseña con toggle mostrar/ocultar:").pack(anchor="w", pady=(0, 2))
        frame_pass = ttk.Frame(self)
        frame_pass.pack(anchor="w", pady=(0, 10))
        self.entry_pass = ttk.Entry(frame_pass, show="*", width=24)
        self.entry_pass.insert(0, "secreto123")
        self.entry_pass.pack(side="left", padx=(0, 5))
        self.btn_toggle_pass = ttk.Button(frame_pass, text="👁 Ver", width=6, command=self._toggle_password)
        self.btn_toggle_pass.pack(side="left")

        ttk.Label(self, text="3. Menú Desplegable (Combobox):").pack(anchor="w", pady=(0, 2))
        self.combo_opciones = ttk.Combobox(self, values=["Python", "JavaScript", "C++", "Rust", "Go"], state="readonly", width=30)
        self.combo_opciones.current(0)
        self.combo_opciones.pack(anchor="w", pady=(0, 10))

        ttk.Label(self, text="4. Checkboxes y Radiobuttons:").pack(anchor="w", pady=(0, 2))
        self.var_notificaciones = tk.BooleanVar(value=True)
        self.chk_notif = ttk.Checkbutton(self, text="Recibir notificaciones por correo", variable=self.var_notificaciones)
        self.chk_notif.pack(anchor="w", pady=(0, 5))

        self.var_tema = tk.StringVar(value="claro")
        frame_radios = ttk.Frame(self)
        frame_radios.pack(anchor="w", pady=(0, 10))
        ttk.Radiobutton(frame_radios, text="Modo Claro", value="claro", variable=self.var_tema).pack(side="left", padx=5)
        ttk.Radiobutton(frame_radios, text="Modo Oscuro", value="oscuro", variable=self.var_tema).pack(side="left", padx=5)

        btn_leer = ttk.Button(self, text="Obtener Resumen de Valores", command=self._mostrar_resumen)
        btn_leer.pack(anchor="w", pady=(5, 10))

        self.lbl_resultado = ttk.Label(self, text="Presiona el botón para consultar los valores.", foreground="#0d6efd", wraplength=480)
        self.lbl_resultado.pack(anchor="w")

    def _toggle_password(self):
        if self.entry_pass.cget("show") == "":
            self.entry_pass.config(show="*")
            self.btn_toggle_pass.config(text="👁 Ver")
        else:
            self.entry_pass.config(show="")
            self.btn_toggle_pass.config(text="🔒 Ocultar")

    def _mostrar_resumen(self):
        resumen = (
            f"Nombre: {self.entry_nombre.get()} | "
            f"Lenguaje: {self.combo_opciones.get()} | "
            f"Notificaciones: {self.var_notificaciones.get()} | "
            f"Tema: {self.var_tema.get()}"
        )
        self.lbl_resultado.config(text=resumen)


# =============================================================================
# 2. DIÁLOGOS DEL SISTEMA (ALERTAS, ARCHIVOS Y SELECTOR DE COLOR)
# =============================================================================
class UtilidadDialogos(ttk.Frame):
    """Manejo de alertas messagebox, diálogo de archivos y selector de color."""
    def __init__(self, parent):
        super().__init__(parent, padding=15)

        ttk.Label(self, text="Diálogos Nativos del Sistema:", font=("Arial", 10, "bold")).pack(anchor="w", pady=(0, 10))

        frame_msgs = ttk.LabelFrame(self, text="Alertas y Confirmaciones (messagebox)", padding=10)
        frame_msgs.pack(fill="x", pady=5)
        ttk.Button(frame_msgs, text="Info", command=lambda: messagebox.showinfo("Información", "¡Operación completada con éxito!")).pack(side="left", padx=5)
        ttk.Button(frame_msgs, text="Advertencia", command=lambda: messagebox.showwarning("Advertencia", "Espacio en disco bajo.")).pack(side="left", padx=5)
        ttk.Button(frame_msgs, text="Error", command=lambda: messagebox.showerror("Error Crítico", "No se pudo conectar con el servidor.")).pack(side="left", padx=5)
        ttk.Button(frame_msgs, text="Pregunta Sí/No", command=self._preguntar_confirmacion).pack(side="left", padx=5)

        frame_files = ttk.LabelFrame(self, text="Selector de Archivos y Carpetas (filedialog)", padding=10)
        frame_files.pack(fill="x", pady=10)
        ttk.Button(frame_files, text="📂 Abrir Archivo", command=self._abrir_archivo).pack(side="left", padx=5)
        ttk.Button(frame_files, text="💾 Guardar Como...", command=self._guardar_archivo).pack(side="left", padx=5)
        ttk.Button(frame_files, text="📁 Seleccionar Carpeta", command=self._seleccionar_carpeta).pack(side="left", padx=5)

        frame_color = ttk.LabelFrame(self, text="Selector de Color (colorchooser)", padding=10)
        frame_color.pack(fill="x", pady=5)
        ttk.Button(frame_color, text="🎨 Elegir Color", command=self._elegir_color).pack(side="left", padx=5)
        self.lbl_muestra_color = tk.Label(frame_color, text="   Muestra de color   ", bg="#e0e0e0", relief="groove")
        self.lbl_muestra_color.pack(side="left", padx=10)

        self.lbl_info_dialogo = ttk.Label(self, text="El resultado de tus selecciones se verá aquí.", foreground="#555", wraplength=480)
        self.lbl_info_dialogo.pack(anchor="w", pady=10)

    def _preguntar_confirmacion(self):
        respuesta = messagebox.askyesno("Confirmar", "¿Deseas borrar los registros temporales?")
        self.lbl_info_dialogo.config(text=f"Respuesta de confirmación: {'Sí' if respuesta else 'No'}")

    def _abrir_archivo(self):
        ruta = filedialog.askopenfilename(
            title="Selecciona un archivo",
            filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")]
        )
        if ruta:
            self.lbl_info_dialogo.config(text=f"Archivo abierto: {ruta}")

    def _guardar_archivo(self):
        ruta = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Archivo de texto", "*.txt"), ("Todos los archivos", "*.*")]
        )
        if ruta:
            self.lbl_info_dialogo.config(text=f"Guardar en: {ruta}")

    def _seleccionar_carpeta(self):
        carpeta = filedialog.askdirectory(title="Elige una carpeta")
        if carpeta:
            self.lbl_info_dialogo.config(text=f"Carpeta: {carpeta}")

    def _elegir_color(self):
        color = colorchooser.askcolor(title="Selecciona un color")
        if color[1]:
            self.lbl_muestra_color.config(bg=color[1])
            self.lbl_info_dialogo.config(text=f"Color seleccionado: {color[1]} (RGB: {color[0]})")


# =============================================================================
# 3. TABLA DE DATOS AVANZADA (ttk.Treeview)
# =============================================================================
class UtilidadTablaTreeview(ttk.Frame):
    """Muestra datos tabulares con columnas, scrollbar, selección y ordenamiento."""
    def __init__(self, parent):
        super().__init__(parent, padding=15)

        ttk.Label(self, text="Tabla Interactiva (ttk.Treeview):", font=("Arial", 10, "bold")).pack(anchor="w", pady=(0, 5))

        frame_tabla = ttk.Frame(self)
        frame_tabla.pack(fill="both", expand=True)

        columnas = ("id", "nombre", "cargo", "salario")
        self.tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings", height=7)

        self.tabla.heading("id", text="ID")
        self.tabla.heading("nombre", text="Empleado")
        self.tabla.heading("cargo", text="Puesto")
        self.tabla.heading("salario", text="Salario")

        self.tabla.column("id", width=50, anchor="center")
        self.tabla.column("nombre", width=180, anchor="w")
        self.tabla.column("cargo", width=150, anchor="w")
        self.tabla.column("salario", width=100, anchor="e")

        scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=scrollbar.set)
        
        self.tabla.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        empleados = [
            ("101", "Lucía Morales", "Desarrolladora Full Stack", "$3,500"),
            ("102", "Carlos Gómez", "Diseñador UI/UX", "$2,800"),
            ("103", "Elena Vargas", "DevOps Engineer", "$4,100"),
            ("104", "Mateo Ríos", "Analista de Datos", "$3,200"),
            ("105", "Sofía Mendoza", "Project Manager", "$4,500"),
        ]
        for emp in empleados:
            self.tabla.insert("", "end", values=emp)

        self.tabla.bind("<<TreeviewSelect>>", self._al_seleccionar_fila)

        frame_acciones = ttk.Frame(self)
        frame_acciones.pack(fill="x", pady=(10, 0))
        ttk.Button(frame_acciones, text="➕ Agregar Registro", command=self._agregar_fila).pack(side="left", padx=5)
        ttk.Button(frame_acciones, text="🗑 Eliminar Fila", command=self._eliminar_fila).pack(side="left", padx=5)

        self.lbl_seleccion = ttk.Label(self, text="Haz clic en una fila para ver sus detalles.", foreground="#0d6efd")
        self.lbl_seleccion.pack(anchor="w", pady=(5, 0))

    def _al_seleccionar_fila(self, event):
        item_id = self.tabla.focus()
        if item_id:
            valores = self.tabla.item(item_id, "values")
            self.lbl_seleccion.config(text=f"Seleccionado: {valores[1]} - {valores[2]} ({valores[3]})")

    def _agregar_fila(self):
        nuevo_id = str(random.randint(106, 999))
        self.tabla.insert("", "end", values=(nuevo_id, "Nuevo Registro", "Especialista", "$3,000"))

    def _eliminar_fila(self):
        seleccion = self.tabla.selection()
        for item in seleccion:
            self.tabla.delete(item)
            self.lbl_seleccion.config(text="Fila eliminada.")


# =============================================================================
# 4. CANVAS, DIBUJO Y ANIMACIÓN EN BUCLE
# =============================================================================
class UtilidadCanvasAnimacion(ttk.Frame):
    """Manejo de gráficos en 2D, figuras y animaciones continuas con after()."""
    def __init__(self, parent):
        super().__init__(parent, padding=15)

        ttk.Label(self, text="Lienzo Gráfico (Canvas) con Animación en Tiempo Real:", font=("Arial", 10, "bold")).pack(anchor="w", pady=(0, 5))

        self.canvas = tk.Canvas(self, width=480, height=200, bg="#1e1e2e", highlightthickness=1, highlightbackground="#333")
        self.canvas.pack(pady=5)

        # Figuras geométricas fijas
        self.canvas.create_rectangle(20, 20, 120, 70, fill="#3498db", outline="white", width=2)
        self.canvas.create_text(70, 45, text="Rectángulo", fill="white", font=("Arial", 9, "bold"))

        self.canvas.create_oval(150, 20, 210, 80, fill="#e74c3c", outline="white")
        self.canvas.create_text(180, 50, text="Círculo", fill="white", font=("Arial", 8, "bold"))

        self.canvas.create_line(230, 25, 450, 75, fill="#f1c40f", width=3, arrow=tk.LAST)

        # Bola animada
        self.bola = self.canvas.create_oval(20, 110, 60, 150, fill="#2ecc71", outline="white", width=2)
        self.dx = 5
        self.dy = 3
        self.animando = False

        frame_controles = ttk.Frame(self)
        frame_controles.pack(pady=5)
        self.btn_anim = ttk.Button(frame_controles, text="▶ Iniciar Animación", command=self._toggle_animacion)
        self.btn_anim.pack(side="left", padx=5)
        ttk.Button(frame_controles, text="🧹 Reiniciar Posición", command=self._reiniciar_canvas).pack(side="left", padx=5)

    def _toggle_animacion(self):
        self.animando = not self.animando
        if self.animando:
            self.btn_anim.config(text="⏸ Pausar Animación")
            self._animar_paso()
        else:
            self.btn_anim.config(text="▶ Reanudar Animación")

    def _animar_paso(self):
        if not self.animando:
            return
        
        self.canvas.move(self.bola, self.dx, self.dy)
        pos = self.canvas.coords(self.bola)

        if pos[0] <= 0 or pos[2] >= 480:
            self.dx = -self.dx
        if pos[1] <= 90 or pos[3] >= 200:
            self.dy = -self.dy

        self.after(20, self._animar_paso)

    def _reiniciar_canvas(self):
        self.animando = False
        self.btn_anim.config(text="▶ Iniciar Animación")
        self.canvas.coords(self.bola, 20, 110, 60, 150)
        self.dx = 5
        self.dy = 3


# =============================================================================
# 5. BARRAS DE PROGRESO Y MULTIHILOS (THREADING)
# =============================================================================
class UtilidadProgresoThreading(ttk.Frame):
    """Manejo de tareas pesadas en segundo plano para no congelar la GUI."""
    def __init__(self, parent):
        super().__init__(parent, padding=15)

        ttk.Label(self, text="Barra de Progreso y Hilos de Fondo (Threading):", font=("Arial", 10, "bold")).pack(anchor="w", pady=(0, 5))
        ttk.Label(self, text="Permite ejecutar tareas pesadas en segundo plano sin congelar la ventana.", foreground="#666").pack(anchor="w", pady=(0, 10))

        ttk.Label(self, text="Progreso Determinado (0% a 100%):").pack(anchor="w")
        self.progreso_det = ttk.Progressbar(self, orient="horizontal", length=380, mode="determinate")
        self.progreso_det.pack(anchor="w", pady=(2, 10))

        ttk.Label(self, text="Progreso Indeterminado (Cargando indefinido):").pack(anchor="w")
        self.progreso_indet = ttk.Progressbar(self, orient="horizontal", length=380, mode="indeterminate")
        self.progreso_indet.pack(anchor="w", pady=(2, 15))

        frame_btns = ttk.Frame(self)
        frame_btns.pack(anchor="w")
        self.btn_iniciar = ttk.Button(frame_btns, text="🚀 Iniciar Tarea en Hilo", command=self._iniciar_hilo)
        self.btn_iniciar.pack(side="left", padx=(0, 5))
        
        self.lbl_estado = ttk.Label(self, text="Estado: Listo", font=("Arial", 9, "italic"))
        self.lbl_estado.pack(anchor="w", pady=10)

    def _iniciar_hilo(self):
        self.btn_iniciar.config(state="disabled")
        self.lbl_estado.config(text="Estado: Procesando tarea en segundo plano...")
        self.progreso_indet.start(10)

        hilo = threading.Thread(target=self._tarea_pesada, daemon=True)
        hilo.start()

    def _tarea_pesada(self):
        for i in range(1, 101):
            time.sleep(0.025)
            self.progreso_det['value'] = i
        
        self.after(0, self._finalizar_tarea)

    def _finalizar_tarea(self):
        self.progreso_indet.stop()
        self.btn_iniciar.config(state="normal")
        self.lbl_estado.config(text="Estado: ¡Tarea completada con éxito al 100%!")


# =============================================================================
# 6. MENÚS, MENÚ CONTEXTUAL (CLIC DERECHO) Y ATAJOS DE TECLADO
# =============================================================================
class UtilidadMenusYAtajos(ttk.Frame):
    """Menú contextual con clic derecho, eventos del ratón y atajos de teclado."""
    def __init__(self, parent, root):
        super().__init__(parent, padding=15)
        self.root = root

        ttk.Label(self, text="Eventos, Menús Emergentes y Atajos:", font=("Arial", 10, "bold")).pack(anchor="w", pady=(0, 5))

        ttk.Label(self, text="Haz clic derecho dentro del cuadro para ver el menú emergente:").pack(anchor="w", pady=(0, 2))
        self.txt_area = tk.Text(self, width=55, height=6, wrap="word")
        self.txt_area.insert("1.0", "Haz clic derecho aquí para desplegar las opciones de Copiar, Pegar o Limpiar.\n\nTambién puedes presionar [Ctrl + S] en la ventana para activar un atajo.")
        self.txt_area.pack(anchor="w", pady=(0, 10))

        self.menu_contextual = tk.Menu(self, tearoff=0)
        self.menu_contextual.add_command(label="Copiar", command=lambda: self.txt_area.event_generate("<<Copy>>"))
        self.menu_contextual.add_command(label="Pegar", command=lambda: self.txt_area.event_generate("<<Paste>>"))
        self.menu_contextual.add_separator()
        self.menu_contextual.add_command(label="Borrar Todo", command=lambda: self.txt_area.delete("1.0", tk.END))

        self.txt_area.bind("<Button-3>", self._mostrar_menu_contextual)
        self.root.bind("<Control-s>", lambda event: messagebox.showinfo("Atajo Detectado", "¡Presionaste Ctrl + S (Guardar)!"))

        self.lbl_tecla = ttk.Label(self, text="Atajo activo: [Ctrl + S] muestra una alerta.", foreground="#28a745")
        self.lbl_tecla.pack(anchor="w")

    def _mostrar_menu_contextual(self, event):
        self.menu_contextual.tk_popup(event.x_root, event.y_root)


# =============================================================================
# 7. VENTANAS SECUNDARIAS (TOPLEVEL) Y MODALES
# =============================================================================
class UtilidadVentanasSecundarias(ttk.Frame):
    """Creación de ventanas Toplevel emergentes normales o modales."""
    def __init__(self, parent):
        super().__init__(parent, padding=15)

        ttk.Label(self, text="Ventanas Secundarias (Toplevel):", font=("Arial", 10, "bold")).pack(anchor="w", pady=(0, 5))
        ttk.Label(self, text="Crea ventanas independientes o modales (que bloquean la principal).", foreground="#666").pack(anchor="w", pady=(0, 10))

        frame_btns = ttk.Frame(self)
        frame_btns.pack(anchor="w", pady=5)
        ttk.Button(frame_btns, text="🪟 Abrir Ventana Libre", command=self._abrir_ventana_normal).pack(side="left", padx=5)
        ttk.Button(frame_btns, text="🔒 Abrir Ventana Modal", command=self._abrir_ventana_modal).pack(side="left", padx=5)

    def _abrir_ventana_normal(self):
        sub_ventana = tk.Toplevel(self)
        sub_ventana.title("Ventana Independiente")
        sub_ventana.geometry("320x150")
        ttk.Label(sub_ventana, text="Esta es una ventana libre.\nPuedes seguir interactuando con la principal.").pack(pady=20)
        ttk.Button(sub_ventana, text="Cerrar", command=sub_ventana.destroy).pack()

    def _abrir_ventana_modal(self):
        modal = tk.Toplevel(self)
        modal.title("Ventana Modal")
        modal.geometry("340x160")
        modal.transient(self)
        modal.grab_set()  # Bloquea interacción con otras ventanas hasta cerrar

        ttk.Label(modal, text="⚠️ Ventana Modal Activa.\nNo puedes interactuar con la ventana principal\nhasta que cierres esta.", justify="center").pack(pady=15)
        ttk.Button(modal, text="Aceptar y Desbloquear", command=modal.destroy).pack(pady=10)


# =============================================================================
# 8. VALIDACIÓN EN TIEMPO REAL EN ENTRADAS (validate='key')
# =============================================================================
class UtilidadValidacionCampos(ttk.Frame):
    """Validación nativa en caliente: rechazar letras, limitar longitud o chequear emails."""
    def __init__(self, parent):
        super().__init__(parent, padding=15)

        ttk.Label(self, text="Validación de Entradas en Vivo (Entry Validation):", font=("Arial", 10, "bold")).pack(anchor="w", pady=(0, 5))
        ttk.Label(self, text="Usa el comando 'validate' para impedir que el usuario ingrese datos inválidos.", foreground="#666").pack(anchor="w", pady=(0, 10))

        # 1. Solo dígitos (rechaza letras automáticamente)
        ttk.Label(self, text="1. Solo Números Enteros (rechaza letras al teclear):").pack(anchor="w")
        val_digitos = self.register(self._solo_digitos)
        self.entry_numeros = ttk.Entry(self, validate="key", validatecommand=(val_digitos, "%P"), width=30)
        self.entry_numeros.pack(anchor="w", pady=(2, 10))

        # 2. Límite máximo de caracteres (máximo 8 letras)
        ttk.Label(self, text="2. Límite Estricto de Longitud (Máximo 8 caracteres):").pack(anchor="w")
        val_longitud = self.register(self._limite_longitud)
        self.entry_limite = ttk.Entry(self, validate="key", validatecommand=(val_longitud, "%P"), width=30)
        self.entry_limite.pack(anchor="w", pady=(2, 10))

        # 3. Validación de Email con cambio visual en vivo
        ttk.Label(self, text="3. Verificador de Correo Electrónico en Vivo:").pack(anchor="w")
        self.entry_email = ttk.Entry(self, width=30)
        self.entry_email.pack(anchor="w", pady=(2, 5))
        self.entry_email.bind("<KeyRelease>", self._validar_email)

        self.lbl_email_status = ttk.Label(self, text="Ingresa un correo con formato usuario@dominio.com", foreground="#666")
        self.lbl_email_status.pack(anchor="w")

    def _solo_digitos(self, texto_propuesto):
        # Permite vacío para poder borrar o solo dígitos
        return texto_propuesto.isdigit() or texto_propuesto == ""

    def _limite_longitud(self, texto_propuesto):
        return len(texto_propuesto) <= 8

    def _validar_email(self, event):
        valor = self.entry_email.get().strip()
        patron = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if re.match(patron, valor):
            self.lbl_email_status.config(text="✓ Formato de correo válido", foreground="#28a745")
        else:
            self.lbl_email_status.config(text="✗ Formato de correo incompleto o inválido", foreground="#dc3545")


# =============================================================================
# 9. DESLIZADORES (SCALE), SPINBOX Y TRANSFERENCIA DE LISTBOX
# =============================================================================
class UtilidadDeslizadoresListas(ttk.Frame):
    """Controles deslizantes con lectura en vivo y movimiento de elementos entre listas."""
    def __init__(self, parent):
        super().__init__(parent, padding=15)

        ttk.Label(self, text="Sliders (Scale), Spinbox y Listbox Transferible:", font=("Arial", 10, "bold")).pack(anchor="w", pady=(0, 5))

        # Sliders y Spinbox
        frame_controles = ttk.Frame(self)
        frame_controles.pack(fill="x", pady=5)

        # Slider con valor dinámico
        ttk.Label(frame_controles, text="Volumen / Deslizador:").grid(row=0, column=0, sticky="w")
        self.var_slider = tk.DoubleVar(value=50.0)
        self.slider = ttk.Scale(frame_controles, from_=0, to=100, orient="horizontal", variable=self.var_slider, length=200, command=self._actualizar_slider)
        self.slider.grid(row=0, column=1, padx=10)
        self.lbl_slider_val = ttk.Label(frame_controles, text="50.0 %")
        self.lbl_slider_val.grid(row=0, column=2, sticky="w")

        # Spinbox numérico
        ttk.Label(frame_controles, text="Selector Numérico (Spinbox):").grid(row=1, column=0, sticky="w", pady=5)
        self.spin = ttk.Spinbox(frame_controles, from_=1, to=50, width=8)
        self.spin.set(10)
        self.spin.grid(row=1, column=1, sticky="w", padx=10, pady=5)

        # Transferencia entre Listbox
        ttk.Label(self, text="Transferencia interactiva entre listas:", font=("Arial", 9, "bold")).pack(anchor="w", pady=(10, 5))
        frame_listas = ttk.Frame(self)
        frame_listas.pack(fill="both", expand=True)

        # Lista A
        self.lista_a = tk.Listbox(frame_listas, selectmode="extended", height=5, width=20)
        for item in ["Python", "Rust", "TypeScript", "Docker", "PostgreSQL"]:
            self.lista_a.insert(tk.END, item)
        self.lista_a.pack(side="left", padx=5)

        # Botones de transferencia
        frame_transfer_btns = ttk.Frame(frame_listas)
        frame_transfer_btns.pack(side="left", padx=5)
        ttk.Button(frame_transfer_btns, text="→ Mover", width=10, command=self._mover_a_derecha).pack(pady=2)
        ttk.Button(frame_transfer_btns, text="← Regresar", width=10, command=self._mover_a_izquierda).pack(pady=2)

        # Lista B
        self.lista_b = tk.Listbox(frame_listas, selectmode="extended", height=5, width=20)
        for item in ["Linux", "Git"]:
            self.lista_b.insert(tk.END, item)
        self.lista_b.pack(side="left", padx=5)

    def _actualizar_slider(self, val):
        self.lbl_slider_val.config(text=f"{float(val):.1f} %")

    def _mover_a_derecha(self):
        seleccion = list(self.lista_a.curselection())
        for idx in reversed(seleccion):
            item = self.lista_a.get(idx)
            self.lista_b.insert(tk.END, item)
            self.lista_a.delete(idx)

    def _mover_a_izquierda(self):
        seleccion = list(self.lista_b.curselection())
        for idx in reversed(seleccion):
            item = self.lista_b.get(idx)
            self.lista_a.insert(tk.END, item)
            self.lista_b.delete(idx)


# =============================================================================
# 10. PANELES DIVISORES AJUSTABLES (ttk.PanedWindow)
# =============================================================================
class UtilidadPanelesDivisores(ttk.Frame):
    """Paneles con separadores que el usuario puede arrastrar para cambiar su tamaño."""
    def __init__(self, parent):
        super().__init__(parent, padding=15)

        ttk.Label(self, text="Paneles Redimensionables (ttk.PanedWindow):", font=("Arial", 10, "bold")).pack(anchor="w", pady=(0, 5))
        ttk.Label(self, text="Arrastra la barra divisoria gris entre los paneles para cambiar su ancho.", foreground="#666").pack(anchor="w", pady=(0, 10))

        # PanedWindow principal (Horizontal)
        paned_h = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        paned_h.pack(fill="both", expand=True)

        # Panel izquierdo
        frame_izq = ttk.Labelframe(paned_h, text="Panel Izquierdo (Navegación)", padding=10)
        ttk.Label(frame_izq, text="Archivos del Proyecto:").pack(anchor="w")
        listbox_files = tk.Listbox(frame_izq, height=6, width=22)
        listbox_files.insert(tk.END, "📁 src/")
        listbox_files.insert(tk.END, "  📄 main.py")
        listbox_files.insert(tk.END, "  📄 config.json")
        listbox_files.insert(tk.END, "📁 tests/")
        listbox_files.insert(tk.END, "  📄 test_app.py")
        listbox_files.pack(fill="both", expand=True)
        paned_h.add(frame_izq, weight=1)

        # Panel derecho (PanedWindow Vertical interna)
        paned_v = ttk.PanedWindow(paned_h, orient=tk.VERTICAL)
        paned_h.add(paned_v, weight=2)

        # Sub-panel derecho superior
        frame_editor = ttk.Labelframe(paned_v, text="Editor Superior", padding=10)
        txt_editor = tk.Text(frame_editor, height=4, width=30)
        txt_editor.insert("1.0", "# Arrastra la barra horizontal abajo\nprint('¡Hola Mundo!')")
        txt_editor.pack(fill="both", expand=True)
        paned_v.add(frame_editor, weight=2)

        # Sub-panel derecho inferior
        frame_terminal = ttk.Labelframe(paned_v, text="Consola Inferior", padding=10)
        lbl_consola = tk.Label(frame_terminal, text="> salida de consola: éxito (código 0)", bg="#1e1e1e", fg="#00ff00", anchor="w", font=("Consolas", 8))
        lbl_consola.pack(fill="both", expand=True)
        paned_v.add(frame_terminal, weight=1)


# =============================================================================
# 11. EDITOR DE TEXTO ENRIQUECIDO CON FORMATO Y BÚSQUEDA
# =============================================================================
class UtilidadTextoEnriquecido(ttk.Frame):
    """Uso avanzado de tk.Text con tags para negrita, colores y resaltado de palabras."""
    def __init__(self, parent):
        super().__init__(parent, padding=15)

        ttk.Label(self, text="Texto Enriquecido (Tags, Estilos y Búsqueda):", font=("Arial", 10, "bold")).pack(anchor="w", pady=(0, 5))

        # Barra de herramientas superior
        frame_toolbar = ttk.Frame(self)
        frame_toolbar.pack(fill="x", pady=(0, 5))

        ttk.Button(frame_toolbar, text="Negrita", width=8, command=self._aplicar_negrita).pack(side="left", padx=2)
        ttk.Button(frame_toolbar, text="Rojo", width=8, command=self._aplicar_color_rojo).pack(side="left", padx=2)
        ttk.Button(frame_toolbar, text="Resaltar", width=8, command=self._aplicar_resaltado).pack(side="left", padx=2)
        ttk.Button(frame_toolbar, text="Quitar Formato", width=12, command=self._limpiar_formato).pack(side="left", padx=2)

        # Área de texto
        self.text_widget = tk.Text(self, height=7, width=55, wrap="word", font=("Arial", 10))
        self.text_widget.insert("1.0", "Selecciona cualquier fragmento de este texto con el ratón y presiona Negrita o Resaltar.\n\nTambién puedes escribir una palabra en la caja de abajo para buscarla.")
        self.text_widget.pack(fill="both", expand=True, pady=5)

        # Configurar tags de estilo
        self.text_widget.tag_configure("negrita", font=("Arial", 10, "bold"))
        self.text_widget.tag_configure("rojo", foreground="#dc3545")
        self.text_widget.tag_configure("resaltado", background="#ffc107", foreground="#000000")
        self.text_widget.tag_configure("busqueda", background="#0d6efd", foreground="#ffffff")

        # Buscador de palabras
        frame_buscar = ttk.Frame(self)
        frame_buscar.pack(fill="x", pady=5)
        ttk.Label(frame_buscar, text="Buscar palabra:").pack(side="left", padx=(0, 5))
        self.entry_busqueda = ttk.Entry(frame_buscar, width=18)
        self.entry_busqueda.insert(0, "texto")
        self.entry_busqueda.pack(side="left", padx=(0, 5))
        ttk.Button(frame_buscar, text="🔍 Buscar y Resaltar", command=self._buscar_palabra).pack(side="left")

    def _aplicar_negrita(self):
        try:
            self.text_widget.tag_add("negrita", "sel.first", "sel.last")
        except tk.TclError:
            pass

    def _aplicar_color_rojo(self):
        try:
            self.text_widget.tag_add("rojo", "sel.first", "sel.last")
        except tk.TclError:
            pass

    def _aplicar_resaltado(self):
        try:
            self.text_widget.tag_add("resaltado", "sel.first", "sel.last")
        except tk.TclError:
            pass

    def _limpiar_formato(self):
        try:
            for tag in ["negrita", "rojo", "resaltado", "busqueda"]:
                self.text_widget.tag_remove(tag, "sel.first", "sel.last")
        except tk.TclError:
            pass

    def _buscar_palabra(self):
        self.text_widget.tag_remove("busqueda", "1.0", tk.END)
        palabra = self.entry_busqueda.get().strip()
        if not palabra:
            return

        pos = "1.0"
        while True:
            pos = self.text_widget.search(palabra, pos, stopindex=tk.END, nocase=True)
            if not pos:
                break
            fin_pos = f"{pos}+{len(palabra)}c"
            self.text_widget.tag_add("busqueda", pos, fin_pos)
            pos = fin_pos


# =============================================================================
# 12. TOOLTIPS FLOTANTES Y PORTAPAPELES (CLIPBOARD)
# =============================================================================
class Tooltip:
    """Clase auxiliar reutilizable para mostrar carteles informativos flotantes."""
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip_window = None
        self.widget.bind("<Enter>", self.mostrar)
        self.widget.bind("<Leave>", self.ocultar)

    def mostrar(self, event=None):
        if self.tooltip_window or not self.text:
            return
        x = self.widget.winfo_rootx() + 20
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 5
        self.tooltip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        label = tk.Label(tw, text=self.text, justify="left", background="#333333", foreground="#ffffff", relief="solid", borderwidth=1, font=("Arial", 8), padx=6, pady=3)
        label.pack()

    def ocultar(self, event=None):
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None


class UtilidadTooltipsYPortapapeles(ttk.Frame):
    """Muestra cómo crear tooltips explicativos y leer/escribir al portapapeles del SO."""
    def __init__(self, parent):
        super().__init__(parent, padding=15)

        ttk.Label(self, text="Tooltips Flotantes y Portapapeles del Sistema:", font=("Arial", 10, "bold")).pack(anchor="w", pady=(0, 5))
        ttk.Label(self, text="Pasa el ratón sobre los botones para ver los carteles de ayuda.", foreground="#666").pack(anchor="w", pady=(0, 10))

        frame_tooltips = ttk.Frame(self)
        frame_tooltips.pack(fill="x", pady=5)

        btn1 = ttk.Button(frame_tooltips, text="Pasa el ratón aquí")
        btn1.pack(side="left", padx=5)
        Tooltip(btn1, "Este es un tooltip útil que describe la función del botón.")

        btn2 = ttk.Button(frame_tooltips, text="Botón con Ayuda")
        btn2.pack(side="left", padx=5)
        Tooltip(btn2, "Acción sensible: Recuerda guardar los cambios antes.")

        # Portapapeles
        frame_clip = ttk.LabelFrame(self, text="Manejo del Portapapeles (Copiar y Pegar)", padding=10)
        frame_clip.pack(fill="x", pady=15)

        self.entry_clip = ttk.Entry(frame_clip, width=35)
        self.entry_clip.insert(0, "Texto especial para copiar")
        self.entry_clip.pack(anchor="w", pady=(0, 5))

        frame_clip_btns = ttk.Frame(frame_clip)
        frame_clip_btns.pack(anchor="w", pady=5)
        ttk.Button(frame_clip_btns, text="📋 Copiar al Portapapeles", command=self._copiar_portapapeles).pack(side="left", padx=5)
        ttk.Button(frame_clip_btns, text="📥 Leer del Portapapeles", command=self._pegar_portapapeles).pack(side="left", padx=5)

        self.lbl_clip_res = ttk.Label(frame_clip, text="Listo.", foreground="#555")
        self.lbl_clip_res.pack(anchor="w", pady=5)

    def _copiar_portapapeles(self):
        texto = self.entry_clip.get()
        self.clipboard_clear()
        self.clipboard_append(texto)
        self.lbl_clip_res.config(text=f"¡Copiado al portapapeles de Windows!: '{texto}'")

    def _pegar_portapapeles(self):
        try:
            contenido = self.clipboard_get()
            self.lbl_clip_res.config(text=f"Contenido actual del portapapeles: '{contenido}'")
        except tk.TclError:
            self.lbl_clip_res.config(text="El portapapeles está vacío o no contiene texto.")


# =============================================================================
# 13. DIÁLOGOS DE ENTRADA RÁPIDA (simpledialog)
# =============================================================================
class UtilidadDialogosEntrada(ttk.Frame):
    """Petición directa de cadenas, enteros y números decimales con validación incorporada."""
    def __init__(self, parent):
        super().__init__(parent, padding=15)

        ttk.Label(self, text="Diálogos de Entrada Rápida (simpledialog):", font=("Arial", 10, "bold")).pack(anchor="w", pady=(0, 5))
        ttk.Label(self, text="Solicita valores al usuario de forma modal sin diseñar ventanas enteras.", foreground="#666").pack(anchor="w", pady=(0, 10))

        frame_btns = ttk.Frame(self)
        frame_btns.pack(anchor="w", pady=5)

        ttk.Button(frame_btns, text="Pedir Texto", command=self._pedir_texto).pack(side="left", padx=5)
        ttk.Button(frame_btns, text="Pedir Entero (1 a 100)", command=self._pedir_entero).pack(side="left", padx=5)
        ttk.Button(frame_btns, text="Pedir Decimal (Float)", command=self._pedir_decimal).pack(side="left", padx=5)

        self.lbl_resultado_dialogo = ttk.Label(self, text="Ningún valor solicitado aún.", foreground="#0d6efd")
        self.lbl_resultado_dialogo.pack(anchor="w", pady=15)

    def _pedir_texto(self):
        nombre = simpledialog.askstring("Nombre", "¿Cuál es tu nombre de usuario?")
        if nombre is not None:
            self.lbl_resultado_dialogo.config(text=f"Texto ingresado: '{nombre}'")

    def _pedir_entero(self):
        edad = simpledialog.askinteger("Edad", "Ingresa tu edad:", minvalue=1, maxvalue=100)
        if edad is not None:
            self.lbl_resultado_dialogo.config(text=f"Entero validado ingresado: {edad}")

    def _pedir_decimal(self):
        precio = simpledialog.askfloat("Precio", "Ingresa el precio con decimales:", minvalue=0.01, maxvalue=9999.99)
        if precio is not None:
            self.lbl_resultado_dialogo.config(text=f"Número decimal ingresado: ${precio:.2f}")


# =============================================================================
# 14. ARRASTRAR Y SOLTAR ELEMENTOS EN LIENZO (DRAG & DROP EN CANVAS)
# =============================================================================
class UtilidadCanvasDragDrop(ttk.Frame):
    """Permite seleccionar y arrastrar libremente figuras geométricas con el ratón."""
    def __init__(self, parent):
        super().__init__(parent, padding=15)

        ttk.Label(self, text="Arrastrar y Soltar en Lienzo (Drag & Drop en Canvas):", font=("Arial", 10, "bold")).pack(anchor="w", pady=(0, 5))
        ttk.Label(self, text="Haz clic sostenido sobre cualquier figura y arrástrala con el cursor.", foreground="#666").pack(anchor="w", pady=(0, 5))

        self.canvas = tk.Canvas(self, width=480, height=220, bg="#2b2d42", highlightthickness=1, highlightbackground="#444")
        self.canvas.pack(pady=5)

        # Crear figuras arrastrables con la etiqueta 'arrastrable'
        self.canvas.create_oval(30, 30, 100, 100, fill="#ef233c", tags="arrastrable")
        self.canvas.create_rectangle(140, 40, 220, 110, fill="#8d99ae", tags="arrastrable")
        self.canvas.create_oval(250, 60, 330, 140, fill="#ffd166", tags="arrastrable")
        self.canvas.create_rectangle(360, 50, 440, 120, fill="#06d6a0", tags="arrastrable")

        # Variables para tracking del mouse
        self.item_seleccionado = None
        self.inicio_x = 0
        self.inicio_y = 0

        # Vincular eventos
        self.canvas.tag_bind("arrastrable", "<ButtonPress-1>", self._iniciar_arrastre)
        self.canvas.tag_bind("arrastrable", "<B1-Motion>", self._mover_figura)
        self.canvas.tag_bind("arrastrable", "<ButtonRelease-1>", self._soltar_figura)

        self.lbl_info = ttk.Label(self, text="Selecciona una figura para moverla.", foreground="#fff", background="#2b2d42", padding=4)
        self.lbl_info.pack(fill="x")

    def _iniciar_arrastre(self, event):
        self.item_seleccionado = self.canvas.find_withtag("current")[0]
        self.inicio_x = event.x
        self.inicio_y = event.y
        self.canvas.tag_raise(self.item_seleccionado)  # Traer al frente
        self.lbl_info.config(text=f"Moviendo objeto ID: {self.item_seleccionado}")

    def _mover_figura(self, event):
        if self.item_seleccionado:
            dx = event.x - self.inicio_x
            dy = event.y - self.inicio_y
            self.canvas.move(self.item_seleccionado, dx, dy)
            self.inicio_x = event.x
            self.inicio_y = event.y

    def _soltar_figura(self, event):
        self.item_seleccionado = None
        self.lbl_info.config(text="Objeto soltado.")


# =============================================================================
# 15. SELECTOR DE TEMAS Y ESTILOS DINÁMICOS (ttk.Style)
# =============================================================================
class UtilidadTemasYEstilos(ttk.Frame):
    """Cambio de temas globales y personalización con ttk.Style."""
    def __init__(self, parent, style):
        super().__init__(parent, padding=15)
        self.style = style

        ttk.Label(self, text="Temas y Estilos Dinámicos (ttk.Style):", font=("Arial", 10, "bold")).pack(anchor="w", pady=(0, 5))
        ttk.Label(self, text="Cambia el tema de toda la interfaz en tiempo real:", foreground="#666").pack(anchor="w", pady=(0, 10))

        # Selector de tema
        temas_disponibles = list(self.style.theme_names())
        ttk.Label(self, text="Selecciona un tema disponible en tu sistema:").pack(anchor="w")
        self.combo_temas = ttk.Combobox(self, values=temas_disponibles, state="readonly", width=25)
        tema_actual = self.style.theme_use()
        if tema_actual in temas_disponibles:
            self.combo_temas.set(tema_actual)
        self.combo_temas.pack(anchor="w", pady=(2, 10))
        self.combo_temas.bind("<<ComboboxSelected>>", self._cambiar_tema)

        # Muestra de widgets para ver el cambio de tema
        frame_muestra = ttk.LabelFrame(self, text="Demostración del tema activo", padding=15)
        frame_muestra.pack(fill="x", pady=10)

        ttk.Button(frame_muestra, text="Botón de Prueba").pack(side="left", padx=5)
        ttk.Entry(frame_muestra).pack(side="left", padx=5)
        ttk.Checkbutton(frame_muestra, text="Opción").pack(side="left", padx=5)

        self.lbl_tema_info = ttk.Label(self, text=f"Tema activo actualmente: '{tema_actual}'", foreground="#0d6efd")
        self.lbl_tema_info.pack(anchor="w", pady=5)

    def _cambiar_tema(self, event):
        nuevo_tema = self.combo_temas.get()
        self.style.theme_use(nuevo_tema)
        self.lbl_tema_info.config(text=f"Tema activo actualmente: '{nuevo_tema}'")


# =============================================================================
# APLICACIÓN PRINCIPAL TIPO DASHBOARD CON MENÚ LATERAL
# =============================================================================
class AplicacionTkinterDemo:
    def __init__(self, root):
        self.root = root
        self.root.title("Centro de Utilidades y Funciones de Tkinter")
        self.root.geometry("860x600")
        self.root.minsize(780, 520)

        # Aplicar estilo moderno
        self.estilo = ttk.Style()
        if "clam" in self.estilo.theme_names():
            self.estilo.theme_use("clam")

        self._configurar_menu_superior()

        # Layout principal: Izquierda (Menú Lateral) y Derecha (Contenedor de Utilidad)
        contenedor_principal = ttk.Frame(self.root)
        contenedor_principal.pack(fill="both", expand=True)

        # ----------------- PANEL LATERAL -----------------
        panel_lateral = ttk.Frame(contenedor_principal, width=240, padding=10)
        panel_lateral.pack(side="left", fill="y")

        ttk.Label(panel_lateral, text="🛠️ Utilidades Tkinter", font=("Segoe UI", 12, "bold")).pack(anchor="w", pady=(0, 8))
        ttk.Label(panel_lateral, text="Selecciona una opción:", font=("Segoe UI", 8), foreground="#666").pack(anchor="w", pady=(0, 5))

        self.lista_menu = tk.Listbox(
            panel_lateral,
            selectmode="single",
            exportselection=False,
            font=("Segoe UI", 9),
            relief="solid",
            borderwidth=1,
            activestyle="none"
        )
        self.lista_menu.pack(fill="both", expand=True)

        # ----------------- PANEL DE CONTENIDO DERECHO -----------------
        self.panel_contenido = ttk.Frame(contenedor_principal, padding=10)
        self.panel_contenido.pack(side="right", fill="both", expand=True)

        # Registrar todas las utilidades disponibles
        self.utilidades = {
            "1. Formularios y Controles": UtilidadControlesBasicos(self.panel_contenido),
            "2. Diálogos y Archivos": UtilidadDialogos(self.panel_contenido),
            "3. Tablas (ttk.Treeview)": UtilidadTablaTreeview(self.panel_contenido),
            "4. Canvas y Animación": UtilidadCanvasAnimacion(self.panel_contenido),
            "5. Hilos y Progreso": UtilidadProgresoThreading(self.panel_contenido),
            "6. Menús y Clic Derecho": UtilidadMenusYAtajos(self.panel_contenido, self.root),
            "7. Ventanas Popups (Toplevel)": UtilidadVentanasSecundarias(self.panel_contenido),
            "8. Validación de Entradas": UtilidadValidacionCampos(self.panel_contenido),
            "9. Sliders, Spinbox y Listbox": UtilidadDeslizadoresListas(self.panel_contenido),
            "10. Paneles Divisores (Paned)": UtilidadPanelesDivisores(self.panel_contenido),
            "11. Editor Texto Enriquecido": UtilidadTextoEnriquecido(self.panel_contenido),
            "12. Tooltips y Portapapeles": UtilidadTooltipsYPortapapeles(self.panel_contenido),
            "13. Diálogos Entrada Rápida": UtilidadDialogosEntrada(self.panel_contenido),
            "14. Drag & Drop en Canvas": UtilidadCanvasDragDrop(self.panel_contenido),
            "15. Temas y Estilos (ttk.Style)": UtilidadTemasYEstilos(self.panel_contenido, self.estilo),
        }

        # Llenar la lista lateral
        for nombre in self.utilidades.keys():
            self.lista_menu.insert(tk.END, f"  {nombre}")

        self.lista_menu.bind("<<ListboxSelect>>", self._al_cambiar_utilidad)

        # Seleccionar la primera por defecto
        self.lista_menu.selection_set(0)
        self._mostrar_utilidad("1. Formularios y Controles")

    def _al_cambiar_utilidad(self, event):
        seleccion = self.lista_menu.curselection()
        if seleccion:
            nombre = list(self.utilidades.keys())[seleccion[0]]
            self._mostrar_utilidad(nombre)

    def _mostrar_utilidad(self, nombre):
        # Ocultar todas las demás utilidades
        for util in self.utilidades.values():
            util.pack_forget()

        # Mostrar la utilidad activa
        self.utilidades[nombre].pack(fill="both", expand=True)

    def _configurar_menu_superior(self):
        barra_menu = tk.Menu(self.root)
        self.root.config(menu=barra_menu)

        menu_archivo = tk.Menu(barra_menu, tearoff=0)
        menu_archivo.add_command(label="Salir", accelerator="Alt+F4", command=self.root.quit)
        barra_menu.add_cascade(label="Archivo", menu=menu_archivo)

        menu_ayuda = tk.Menu(barra_menu, tearoff=0)
        menu_ayuda.add_command(label="Acerca de...", command=lambda: messagebox.showinfo("Catálogo Tkinter", "Catálogo modular con 15 utilidades prácticas de Tkinter."))
        barra_menu.add_cascade(label="Ayuda", menu=menu_ayuda)


# =============================================================================
# PUNTO DE ENTRADA
# =============================================================================
if __name__ == "__main__":
    ventana_principal = tk.Tk()
    app = AplicacionTkinterDemo(ventana_principal)
    ventana_principal.mainloop()
