import tkinter as tk
from tkinter import ttk, messagebox
#Importamos clases que tenemos en otros archivos
from db_config import MiBaseDatos
from generar_pdf import GenerarPDF
from mantenimiento import Mantenimiento
from falla import Falla
from equipos import Equipos


class SistemaMantenimiento:
    def __init__(self):
        # Inicialización de la ventana principal
        self.root = tk.Tk()
        self.root.title("TecnoMant - Sistema de Mantenimiento")
        self.root.resizable(True, True)
        self.root.state('zoomed')

        # Ejecuta la función al cerrar la ventana
        self.root.protocol("WM_DELETE_WINDOW", self.al_cerrar_ventana)

        # Conexión a la base de datos
        self.db = MiBaseDatos()
        self.db.conectar()

        #Confugiración del estilo de la interfaz
        self.style = ttk.Style()
        self.style.theme_use('clam')

        #ejecuta la interfaz
        self.crear_interfaz()

    # Método para abrir ventanas de mantenimiento, equipos y fallas
    def ventanaMantenimiento(self):
        self.root.withdraw()
        Mantenimiento(self.root,  self.consultar_mantenimientos)

    def ventanaEquipo(self):
        self.root.withdraw()
        Equipos(self.root)

    def ventanaFalla(self):
        self.root.withdraw()
        Falla(self.root, self.consultar_mantenimientos)

    # Método para generar el PDF del reporte completo
    def generar_pdf(self):
        pdf = GenerarPDF()
        pdf.generar_pdf_reporte_completo()

    # Método para crear la interfaz principal
    def crear_interfaz(self):
        # Configuración del frame principal
        frame_principal = ttk.Frame(self.root)
        frame_principal.pack(fill="both", expand=True, padx=10, pady=10)

        # Frame de menu
        frame_menu = ttk.LabelFrame(frame_principal, text="Menú", padding=10)
        frame_menu.pack(fill="x", pady=(0, 10))

        # Botones del menú
        ttk.Button(frame_menu, text="Equipos", command=self.ventanaEquipo, width=20).pack(side="left", padx=(0, 10))
        ttk.Button(frame_menu, text="Mantenimientos", command=self.ventanaMantenimiento, width=20).pack(side="left", padx=(0, 10))
        ttk.Button(frame_menu, text="Fallas", command=self.ventanaFalla, width=20).pack(side="left", padx=(0, 10))
        ttk.Button(frame_menu, text="Imprimir reporte", command=self.generar_pdf, width=25).pack(side="right", padx=(0, 10))

        # Frame de mantenimientos registrados treeview
        frame_mantenimiento = ttk.LabelFrame(frame_principal, text="Próximos Mantenimientos", padding=10)
        frame_mantenimiento.pack(fill="both", expand=True, pady=(0, 10))

        # Panel de contenido para el treeview de mantenimientos
        mantenimiento_contenido = ttk.Frame(frame_mantenimiento)
        mantenimiento_contenido.pack(fill="both", expand=True)

        #Definición de las columnas del treeview de mantenimientos
        columnas_mantenimiento = ("ID Mantenimiento", "ID Equipo","Equipo", "Descripción", "ID Técnico", "Técnico", "Próximo Mantenimiento")
        self.tree_mantenimiento = ttk.Treeview(mantenimiento_contenido, columns=columnas_mantenimiento, show="headings", height=6)
        
        # Define los anchos de cada columna de mantenimiento
        anchos = {
            "ID Mantenimiento": 100,
            "ID Equipo": 100,
            "Equipo": 140,
            "Descripción": 300,
            "ID Técnico": 100,
            "Técnico": 140,
            "Próximo Mantenimiento": 160
            }
        
        # Ciclo for para configurar las columnas del treeview, añade encabezado y el ancho correspondiente
        for columna in columnas_mantenimiento:
            self.tree_mantenimiento.heading(columna, text=columna)
            self.tree_mantenimiento.column(columna, width=anchos[columna], anchor="center")

        # Scrollbar vertical para el treeview de mantenimientos
        scrollbar_mantenimiento = ttk.Scrollbar(mantenimiento_contenido, orient="vertical", command=self.tree_mantenimiento.yview)
        self.tree_mantenimiento.configure(yscrollcommand=scrollbar_mantenimiento.set)

        # Ordenamos el treview y el scrollbar dentro del frame contenedor
        self.tree_mantenimiento.pack(side="left", fill="both", expand=True)
        scrollbar_mantenimiento.pack(side="left", fill="y")

        # Frame de fallas registradas treeview
        frame_fallas = ttk.LabelFrame(frame_principal, text="Fallas", padding=10)
        frame_fallas.pack(fill="both", expand=True, pady=(10, 0))

        # Panel de contenido para el treeview de fallas
        fallas_contenido = ttk.Frame(frame_fallas)
        fallas_contenido.pack(fill="both", expand=True)
        
        # Definición de las columnas del treeview de fallas
        columnas_fallas = ("# Falla", "ID Equipo", "Equipo", "Fecha de la falla","Descripción", "Causa", "Solución", "ID Técnico", "Técnico")
        self.tree_fallas = ttk.Treeview(fallas_contenido, columns=columnas_fallas, show="headings", height=8)

        # Define los anchos de cada columna del treeview de fallas
        anchos_falla = {
            "# Falla": 80,
            "ID Equipo": 80,
            "Equipo": 130,
            "Fecha de la falla": 130,
            "Descripción": 240,
            "Causa": 220,
            "Solución": 220,
            "ID Técnico": 80,
            "Técnico": 130
        }

        # Ciclo for para configurar las columnas del treeview, añade encabezado y el ancho correspondiente
        for columna in columnas_fallas:
            self.tree_fallas.heading(columna, text=columna)
            self.tree_fallas.column(columna, width=anchos_falla[columna], anchor="center")

        # Scrollbar vertical para el treeview de mantenimientos
        scrollbar_fallas_vertical = ttk.Scrollbar(fallas_contenido, orient="vertical", command=self.tree_fallas.yview)

        # Scrollbar horizontal para el treeview de fallas 
        scrollbar_fallas_horizontal = ttk.Scrollbar(fallas_contenido, orient="horizontal", command=self.tree_fallas.xview)

        # Configura los scrollbars del treeview de fallas
        self.tree_fallas.configure(yscrollcommand=scrollbar_fallas_vertical.set, xscrollcommand=scrollbar_fallas_horizontal.set)

        # Ordenamos el treeview y los scrollbars dentro del frame contenedor
        #usamos grid para organizar los widgets en forma de tabla
        self.tree_fallas.grid(row=0, column=0, sticky="nsew")
        scrollbar_fallas_vertical.grid(row=0, column=1, sticky="ns")
        scrollbar_fallas_horizontal.grid(row=1, column=0, sticky="ew")
        fallas_contenido.grid_rowconfigure(0, weight=1)
        fallas_contenido.grid_columnconfigure(0, weight=1)

        # Ejecuta las consultas para llenar los treeviews
        self.consultar_mantenimientos()
        self.consultar_fallas()

    # Método para consultar los mantenimientos
    def consultar_mantenimientos(self):
        # Ejecuta la consulta SQL para obtener los mantenimientos
        cursor = self.db.conexion.cursor()
        cursor.execute("""
            SELECT 
                m.id_mantenimiento,
                e.id_equipo,
                e.nombre,
                m.descripcion,
                t.id_tecnico,
                t.nombre,
                m.proximo_mantenimiento
            FROM mantenimiento m
            JOIN equipo e ON m.id_equipo = e.id_equipo
            JOIN tecnico t ON m.id_tecnico = t.id_tecnico
            ORDER BY m.proximo_mantenimiento ASC;
        """)

        #limpia el treeview antes de insertar nuevos datos
        for item in self.tree_mantenimiento.get_children():
            self.tree_mantenimiento.delete(item)
        
        # Inserta los datos obtenidos en el treeview de mantenimientos
        for curso in cursor.fetchall():
            self.tree_mantenimiento.insert("", "end", values=curso)
        self.db.conexion.commit()

    # Método para consultar las fallas
    def consultar_fallas(self):
        # Ejecuta la consulta SQL para obtener las fallas
        cursor = self.db.conexion.cursor()
        cursor.execute("""
            SELECT 
                f.id_falla,
                e.id_equipo,
                e.nombre,
                f.fecha,
                f.descripcion,
                f.causa,
                f.solucion,
                t.id_tecnico,
                t.nombre
            FROM falla f, equipo e, tecnico t
            WHERE f.id_equipo = e.id_equipo
            AND f.id_tecnico = t.id_tecnico;
        """)

        # Limpia el treeview antes de insertar nuevos datos
        for item in self.tree_fallas.get_children():
            self.tree_fallas.delete(item)
        
        # Inserta los datos obtenidos en el treeview de fallas
        for curso in cursor.fetchall():
            self.tree_fallas.insert("", "end", values=curso)
        self.db.conexion.commit()

    # Método para ejecutar la aplicación
    def ejecutar(self):
        self.root.mainloop()

    #Metodo para confirmar la salida de la aplicación
    def al_cerrar_ventana(self):
        respuesta = messagebox.askyesno("Confirmar salida", "¿Estás seguro de que quieres salir?")
        if respuesta:
            self.root.destroy()
            self.db.cerrar()
 
if __name__ == "__main__":
    app = SistemaMantenimiento()
    app.ejecutar()