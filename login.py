import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
from db_config import MiBaseDatos

class SistemaLogin:
    def __init__(self):
        # Ventana principal
        self.root = tk.Tk()
        self.root.title("TecnoMant - Sistema de Mantenimiento")
        self.root.state('zoomed') 
        self.root.resizable(True, True)
        
        # Colores del tema
        self.colores = {
        'primario': "#CDCBC9",      
        'secundario': "#F0EFED",    
        'acento': "#929393",       
        'acento_hover': "#C7C7C7",               
        'texto': "#272727",         
        'texto_secundario': '#272727', 
        'fondo': '#CDCBC9',         
        'fondo_claro': '#F0EFED'
        }

        # Conexión a la base de datos
        self.db = MiBaseDatos()
        self.db.conectar()

        # Configuración del tema y creación de la interfaz de login
        self.configurar_tema()
        self.crear_interfaz_login()

    # método para configurar el tema visual
    def configurar_tema(self):
        # configurar colores de fondo
        self.root.configure(bg=self.colores['fondo'])
        
        # Configurar estilo ttk
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Configura el estilo del tema
        self.style.configure('Login.TFrame', 
                           background=self.colores['secundario'],
                           borderwidth=0,
                           relief='flat')
        
        # estilo de la card de login
        self.style.configure('Card.TFrame',
                           background=self.colores['secundario'],
                           borderwidth=2,
                           relief='raised')
        
        # estilo de titulos
        self.style.configure('Title.TLabel',
                           background=self.colores['secundario'],
                           foreground=self.colores['texto'],
                           font=('Segoe UI', 32, 'bold'))
        
        # estilo de subtitulos
        self.style.configure('Subtitle.TLabel',
                           background=self.colores['secundario'],
                           foreground=self.colores['texto_secundario'],
                           font=('Segoe UI', 12))
        
        # estilo de labels de los campos
        self.style.configure('Field.TLabel',
                           background=self.colores['secundario'],
                           foreground=self.colores['texto'],
                           font=('Segoe UI', 12, 'bold'))
        
        # estilo de los campos
        self.style.configure('Login.TEntry',
                           fieldbackground=self.colores['fondo_claro'],
                           borderwidth=2,
                           relief='flat',
                           insertcolor=self.colores['texto'],
                           foreground=self.colores['texto'],
                           font=('Segoe UI', 11))
        
        # estilo de los botones
        self.style.configure('Primary.TButton',
                           background=self.colores['acento'],
                           foreground=self.colores['texto'],
                           borderwidth=0,
                           relief='flat',
                           font=('Segoe UI', 12, 'bold'))
        
        # Estilo de hover y presionado de los botones
        self.style.map('Primary.TButton', background=[('active', self.colores['acento_hover']), ('pressed', self.colores['acento']),])
        
        # estilo de botones secundarios
        self.style.configure('Secondary.TButton',
                           background=self.colores['fondo_claro'],
                           foreground=self.colores['texto'],
                           borderwidth=1,
                           relief='flat',
                           font=('Segoe UI', 11))
        
        # Estilo de hover y presionado de los botones secundarios
        self.style.map('Secondary.TButton',
                      background=[('active', self.colores['secundario']),
                                ('pressed', self.colores['fondo_claro'])])

    # método para crear la interfaz de login
    def crear_interfaz_login(self):

        # Contenedor principal
        contenedor_principal = tk.Frame(self.root, bg=self.colores['fondo'])
        contenedor_principal.pack(fill=tk.BOTH, expand=True)
        
        # Frame izquierdo, logo y descripción
        left_frame = tk.Frame(contenedor_principal, bg=self.colores['primario'], width=500)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=20, pady=20)
        left_frame.pack_propagate(False)
        
        # Contenido del frame izquierdo
        brand_container = tk.Frame(left_frame, bg=self.colores['primario'])
        brand_container.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        # Logo
        logo_label = tk.Label(brand_container, text="⚙️", font=('Segoe UI', 80), bg=self.colores['primario'], fg=self.colores['acento']) 
        logo_label.pack(pady=20)
        
        # Título del sistema
        tk.Label(brand_container, text="TECNOMANT", font=('Segoe UI', 18, 'bold'), bg=self.colores['primario'], fg=self.colores['texto']).pack(pady=5)
        
        # Descripción
        tk.Label(brand_container, text="Control total de tus equipos y mantenimientos", font=('Segoe UI', 12), bg=self.colores['primario'], fg=self.colores['texto_secundario']).pack(pady=20)
        
        # Frame derecho donde va el formulario de login
        right_frame = tk.Frame(contenedor_principal, bg=self.colores['fondo'])
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Card de login
        login_card = ttk.Frame(right_frame, style='Card.TFrame', padding=60)
        login_card.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        # Título del login
        ttk.Label(login_card, text="Iniciar Sesión", style='Title.TLabel').pack(pady=(0, 10))
        
        # Subtítulo
        ttk.Label(login_card, text="Ingresa tus credenciales para acceder al sistema", style='Subtitle.TLabel').pack(pady=(0, 30))
        
        # Campo Usuario
        ttk.Label(login_card, text="USUARIO", style='Field.TLabel').pack(anchor='w', pady=(0, 5))
        self.usuario_entry = ttk.Entry(login_card, width=35, style='Login.TEntry', font=('Segoe UI', 12))
        self.usuario_entry.pack(pady=(0, 20), ipady=8)
        
        # Campo Contraseña
        ttk.Label(login_card, text="CONTRASEÑA", style='Field.TLabel').pack(anchor='w', pady=(0, 5))
        self.password_entry = ttk.Entry(login_card, width=35, show="●", style='Login.TEntry', font=('Segoe UI', 12))
        self.password_entry.pack(pady=(0, 30), ipady=8)
        
        # contenedor de botones
        botones_frame = ttk.Frame(login_card, style='Login.TFrame')
        botones_frame.pack(fill=tk.X, pady=10)
        
        #botones
        login_btn = ttk.Button(botones_frame, text="INICIAR SESIÓN", style='Primary.TButton', command=self.iniciar_sesion)
        login_btn.pack(fill=tk.X, pady=(0, 15), ipady=12)
        registrar_btn = ttk.Button(botones_frame, text="REGISTRAR NUEVO USUARIO", style='Secondary.TButton', command=self.abrir_registro)
        registrar_btn.pack(fill=tk.X, ipady=10)
        
        # Enter para iniciar sesión
        self.root.bind('<Return>', lambda event: self.iniciar_sesion())
        
        # Focus inicial en el campo usuario
        self.usuario_entry.focus()

    # método para iniciar sesión al dar click en el botón o enter
    def iniciar_sesion(self):
        # Obtiene los valores de los campos
        usuario = self.usuario_entry.get()
        password = self.password_entry.get()

        # valida que no estén vacíos
        if not usuario or not password:
            messagebox.showinfo("Error de Validación", "Debes llenar todos los campos.")
            return

        # Intenta iniciar sesión verificando en la base de datos
        try:
            cursor = self.db.conexion.cursor()
            # Verificar si el usuario se encuentra en responsable
            cursor.execute("SELECT * FROM responsable WHERE nombre_usuario=? AND Contrasena=?", (usuario, password))
            if cursor.fetchone():
                messagebox.showinfo("Acceso Concedido", "Bienvenido Responsable.")
                self.root.destroy()
                subprocess.Popen(["python", "main.py"])
                return

            # si no encontró en responsable, verifica en técnico
            cursor.execute("SELECT * FROM tecnico WHERE nombre_usuario=? AND Contrasena=?", (usuario, password))
            if cursor.fetchone():
                messagebox.showinfo("Acceso Concedido", "Bienvenido Técnico.")
                self.root.destroy()
                subprocess.Popen(["python", "main.py"])
                return

            # Si no encontró en ninguno
            messagebox.showerror("Acceso Denegado", "Usuario o contraseña incorrectos.")
            print(usuario, password)

        except Exception as e:
            messagebox.showerror("Error de Conexión", f"No se pudo iniciar sesión: {str(e)}")

    # método para abrir la ventana de registro 
    def abrir_registro(self):
        RegistroUsuario(self.db, self.colores, self.style)

    # método para ejecutar la aplicación
    def ejecutar(self):
        self.root.mainloop()


class RegistroUsuario:
    def __init__(self, db, colores, style):
        self.db = db
        self.colores = colores
        self.style = style

        # Nueva ventana completa
        self.registro_win = tk.Toplevel()
        self.registro_win.title("TecnoMant - Sistema de Mantenimiento")
        self.registro_win.state('zoomed')
        self.registro_win.resizable(False, False)
        self.registro_win.configure(bg=self.colores['fondo'])
        
        # Crear la interfaz de registro
        self.crear_interfaz_registro()

    # método para crear la interfaz de registro
    def crear_interfaz_registro(self):
        # Frame principal
        frame_principal = tk.Frame(self.registro_win, bg=self.colores['fondo'])
        frame_principal.pack(fill=tk.BOTH, expand=True)
        
        # Header
        header_frame = tk.Frame(frame_principal, bg=self.colores['primario'], height=100)
        header_frame.pack(fill=tk.X, padx=20, pady=(20, 0))
        header_frame.pack_propagate(False)
        
        # contenido del encabezado
        contenedor_encabezado = tk.Frame(header_frame, bg=self.colores['primario'])
        contenedor_encabezado.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        # Título y descripción
        tk.Label(contenedor_encabezado, text="👤 REGISTRO DE USUARIO", font=('Segoe UI', 24, 'bold'), bg=self.colores['primario'], fg=self.colores['texto']).pack()
        tk.Label(contenedor_encabezado, text="Crear nueva cuenta de acceso al sistema", font=('Segoe UI', 12), bg=self.colores['primario'], fg=self.colores['texto_secundario']).pack()
        
        # Card de registro
        registro_card = ttk.Frame(frame_principal, style='Card.TFrame', padding=60)
        registro_card.pack(expand=True, pady=40)
        
        # Grid para organizar campos en dos columnas
        campos_frame = ttk.Frame(registro_card, style='Login.TFrame')
        campos_frame.pack(fill=tk.BOTH, expand=True)
        
        # Columna izquierda
        columna_izquierda = ttk.Frame(campos_frame, style='Login.TFrame')
        columna_izquierda.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 30))
        
        # Campo ID
        ttk.Label(columna_izquierda, text="ID", style='Field.TLabel').pack(anchor='w', pady=(0, 5))
        self.id_entry = ttk.Entry(columna_izquierda, width=30, style='Login.TEntry', font=('Segoe UI', 12))
        self.id_entry.pack(pady=(0, 20), ipady=8, fill=tk.X)

        # Campo Nombre
        ttk.Label(columna_izquierda, text="NOMBRE COMPLETO", style='Field.TLabel').pack(anchor='w', pady=(0, 5))
        self.nombre_entry = ttk.Entry(columna_izquierda, width=30, style='Login.TEntry', font=('Segoe UI', 12))
        self.nombre_entry.pack(pady=(0, 20), ipady=8, fill=tk.X)
        
        # Campo Usuario
        ttk.Label(columna_izquierda, text="NOMBRE DE USUARIO", style='Field.TLabel').pack(anchor='w', pady=(0, 5))
        self.usuario_entry = ttk.Entry(columna_izquierda, width=30, style='Login.TEntry',font=('Segoe UI', 12))
        self.usuario_entry.pack(pady=(0, 20), ipady=8, fill=tk.X)
        
        # Columna derecha
        columna_derecha = ttk.Frame(campos_frame, style='Login.TFrame')
        columna_derecha.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(30, 0))
        
        # Campo Contraseña
        ttk.Label(columna_derecha, text="CONTRASEÑA", style='Field.TLabel').pack(anchor='w', pady=(0, 5))
        self.password_entry = ttk.Entry(columna_derecha, width=30, style='Login.TEntry', font=('Segoe UI', 12))
        self.password_entry.pack(pady=(0, 20), ipady=8, fill=tk.X)
        
        # Campo Puesto
        ttk.Label(columna_derecha, text="PUESTO", style='Field.TLabel').pack(anchor='w', pady=(0, 5))
        self.puesto_entry = ttk.Entry(columna_derecha, width=30, style='Login.TEntry', font=('Segoe UI', 12))
        self.puesto_entry.pack(pady=(0, 20), ipady=8, fill=tk.X)

        # Campo Especialidad (solo para técnicos)
        ttk.Label(columna_derecha, text="ESPECIALIDAD (técnico)", style='Field.TLabel').pack(anchor='w', pady=(0, 5))
        self.especialidad_entry = ttk.Entry(columna_derecha, width=30, style='Login.TEntry', font=('Segoe UI', 12))
        self.especialidad_entry.pack(pady=(0, 20), ipady=8, fill=tk.X)
        
        # frames para los botones
        button_frame = ttk.Frame(registro_card, style='Login.TFrame')
        button_frame.pack(fill=tk.X, pady=30)
        
        # contenedor de botones
        btn_container = ttk.Frame(button_frame, style='Login.TFrame')
        btn_container.pack()
        
        # botones
        registrar_btn = ttk.Button(btn_container, text="✓ REGISTRAR", style='Primary.TButton', command=self.registrar_usuario)
        registrar_btn.pack(side=tk.LEFT, padx=(0, 15), ipady=12, ipadx=20)
        cancelar_btn = ttk.Button(btn_container, text="✕ CANCELAR", style='Secondary.TButton', command=self.registro_win.destroy)
        cancelar_btn.pack(side=tk.LEFT, ipady=12, ipadx=20)
        
        # Focus inicial en el campo nombre
        self.id_entry.focus()

    # método para registrar el usuario en la base de datos
    def registrar_usuario(self):
        # Obtiene los valores de los campos
        id = self.id_entry.get()
        nombre = self.nombre_entry.get()
        usuario = self.usuario_entry.get()
        password = self.password_entry.get()
        puesto = self.puesto_entry.get()
        especialidad = self.especialidad_entry.get()

        # valida que no estén vacíos
        if not id or not nombre or not usuario or not password or not puesto:
            messagebox.showerror("Error de Validación", "Todos los campos son obligatorios.")
            return

        # Intenta registrar el usuario en la base de datos
        try:
            cursor = self.db.conexion.cursor()

            # Verificar si ya existe en responsable
            cursor.execute("SELECT * FROM responsable WHERE nombre_usuario=?", (usuario,))
            if cursor.fetchone():
                messagebox.showerror("Usuario Duplicado", "El usuario ya existe en el sistema.")
                return

            # si no encontró en responsable, verifica en técnico
            cursor.execute("SELECT * FROM tecnico WHERE nombre_usuario=?", (usuario,))
            if cursor.fetchone():
                messagebox.showerror("Usuario Duplicado", "El usuario ya existe en el sistema.")
                return

            # Insertar en la tabla correspondiente, si puesto es técnico va a técnico, si no a responsable
            if puesto.lower() == "tecnico":
                cursor.execute("INSERT INTO tecnico (id_tecnico, nombre, nombre_usuario, Contrasena, especialidad) VALUES (?, ?, ?, ?, ?)",
                            (id, nombre, usuario, password, especialidad))
            else:
                cursor.execute("INSERT INTO responsable (id_responsable, nombre, nombre_usuario, Contrasena, puesto) VALUES (?, ?, ?, ?, ?)", 
                            (id, nombre, usuario, password, puesto))
            self.db.conexion.commit()
            messagebox.showinfo("Registro Exitoso", f"Usuario '{usuario}' registrado correctamente.")
            self.limpiar_campos()

        except Exception as e:
            messagebox.showerror("Error de Base de Datos", f"No se pudo registrar el usuario: {str(e)}")

    # método para limpiar los campos después de un registro exitoso
    def limpiar_campos(self):
        self.nombre_entry.delete(0, tk.END)
        self.usuario_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        self.puesto_entry.delete(0, tk.END)
        self.especialidad_entry.delete(0, tk.END)
        self.nombre_entry.focus()

if __name__ == "__main__":
    app = SistemaLogin()
    app.ejecutar()
    