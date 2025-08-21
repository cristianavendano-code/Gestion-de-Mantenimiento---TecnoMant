import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from db_config import MiBaseDatos
from tkcalendar import DateEntry

class Equipos:
    def __init__(self, master):
        # Inicialización de la ventana principal
        self.master = master
        # Crea una nueva ventana para Equipos
        self.root = tk.Toplevel(master)
        self.root.title("TecnoMant - Sistema de Mantenimiento")
        self.root.state('zoomed')
        self.root.resizable(True, True)

        # Ejecuta la función al cerrar la ventana
        self.root.protocol("WM_DELETE_WINDOW", self.al_cerrar_ventana)

        # Conexión a la base de datos
        self.db = MiBaseDatos()
        self.db.conectar()

        # Configuración del estilo de la interfaz
        self.style = ttk.Style()
        self.style.theme_use('clam')

        # Ejecuta la interfaz
        self.crear_interfaz()

    # Método para crear la interfaz de equipos
    def crear_interfaz(self):
        # Frame principal
        frame_principal = ttk.Frame(self.root)
        frame_principal.pack(fill="both", expand=True)

        # Frame de equipos
        frame_equipos = ttk.LabelFrame(frame_principal, text="Equipos (Máquinas)", padding=10)
        frame_equipos.pack(side="right", fill="both", expand=True, padx=(5, 0))
        
        # Frame horizontal para organizar los campos y botones
        frame_horizontal = ttk.Frame(frame_equipos)
        frame_horizontal.pack(fill="both", pady=10)

        # CAMPOS DE EQUIPO

        # Frame para los campos de equipo
        equipos_campos_frame = ttk.Frame(frame_horizontal)
        equipos_campos_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        # ID Equipo
        ttk.Label(equipos_campos_frame, text="ID del Equipo:").grid(row=0, column=0, sticky="w", pady=2)
        self.entry_id_equipo = ttk.Entry(equipos_campos_frame, width=20)
        self.entry_id_equipo.grid(row=0, column=1, sticky="ew", padx=(5, 0), pady=2)

        # Nombre
        ttk.Label(equipos_campos_frame, text="Nombre:").grid(row=1, column=0, sticky="w", pady=2)
        self.entry_nombre = ttk.Entry(equipos_campos_frame, width=20)
        self.entry_nombre.grid(row=1, column=1, sticky="ew", padx=(5, 0), pady=2)

        # Modelo
        ttk.Label(equipos_campos_frame, text="Modelo:").grid(row=2, column=0, sticky="w", pady=2)
        self.entry_modelo = ttk.Entry(equipos_campos_frame, width=20)
        self.entry_modelo.grid(row=2, column=1, sticky="ew", padx=(5, 0), pady=2)

        # Tipo
        ttk.Label(equipos_campos_frame, text="Tipo:").grid(row=3, column=0, sticky="w", pady=2)
        self.entry_tipo = ttk.Entry(equipos_campos_frame, width=20)
        self.entry_tipo.grid(row=3, column=1, sticky="ew", padx=(5, 0), pady=2)

        # Fecha de Adquisición
        ttk.Label(equipos_campos_frame, text="Fecha de Adquisición:").grid(row=4, column=0, sticky="w", pady=2)
        self.entry_fecha_adquisicion = DateEntry(equipos_campos_frame, width=18, borderwidth=2, date_pattern='yyyy-mm-dd')
        self.entry_fecha_adquisicion.set_date(datetime.now())
        self.entry_fecha_adquisicion.grid(row=4, column=1, sticky="ew", padx=(5, 0), pady=2)

        # ID Responsable
        ttk.Label(equipos_campos_frame, text="ID Responsable:").grid(row=5, column=0, sticky="w", pady=2)
        self.entry_id_reponsable = ttk.Entry(equipos_campos_frame, width=20)
        self.entry_id_reponsable.grid(row=5, column=1, sticky="ew", padx=(5, 0), pady=2)

        # Organiza los campos de equipos
        equipos_campos_frame.columnconfigure(1, weight=1)

        # Frame para los botones
        frame_botones = ttk.Frame(frame_horizontal)
        frame_botones.grid(row=0, column=1, sticky="n")  # "n" para alinear arriba

        # Botones para agregar, editar, limpiar y eliminar equipos
        ttk.Button(frame_botones, text="Agregar", width=20, command=self.agregar_equipo).pack(pady=5)
        ttk.Button(frame_botones, text="Editar", width=20, command=self.modificar_equipo).pack(pady=5)
        ttk.Button(frame_botones, text="Limpiar", width=20, command=self.limpiar_campos).pack(pady=5)
        ttk.Button(frame_botones, text="Eliminar", width=20, command=self.eliminar_equipo).pack(pady=5)

        # Organiza el frame de botones
        frame_horizontal.columnconfigure(0, weight=1)

        #crear espacio entre campos y treeview y abajo mostrar texto equipos
        ttk.Label(frame_equipos, text="Equipos registrados", font=("Arial", 10)).pack(pady=(10, 0))

        # Definición de las columnas del treeview de equipos
        columnas_equipos = ("ID Equipo", "Nombre", "Modelo", "Tipo", "Fecha Adquisición", "ID Responsable", "Responsable")
        self.tree_equipos = ttk.Treeview(frame_equipos, columns=columnas_equipos, show="headings", height=6)

        # Ciclo for para configurar las columnas del treeview y añade encabezado 
        for columna in columnas_equipos:
            self.tree_equipos.heading(columna, text=columna)
            self.tree_equipos.column(columna, width=120, anchor="center")

        # Scrollbar vertical para el treeview de equipos
        scrollbar_equipos = ttk.Scrollbar(frame_equipos, orient="vertical", command=self.tree_equipos.yview)
        self.tree_equipos.configure(yscrollcommand=scrollbar_equipos.set)

        # Obtiene la selección del treeview de equipos y ejecuta el metodo obtener_seleccion
        self.tree_equipos.bind("<<TreeviewSelect>>", self.obtener_seleccion)

        # Ordenamos el treview y el scrollbar dentro del frame contenedor
        self.tree_equipos.pack(side="left", fill="both", expand=True)
        scrollbar_equipos.pack(side="left", fill="y")

        # Ejecuta la consulta para llenar el treeview de equipos
        self.consultar_equipos()

    # Método para agregar un equipo
    def agregar_equipo(self):
        # Obtiene los valores de los campos
        id_equipo = self.entry_id_equipo.get()
        nombre = self.entry_nombre.get()
        modelo = self.entry_modelo.get()
        tipo = self.entry_tipo.get()
        fecha_adquisicion = self.entry_fecha_adquisicion.get()
        id_responsable = self.entry_id_reponsable.get()

        # Verifica que todos los campos estén llenos
        if not (id_equipo and nombre and modelo and tipo and fecha_adquisicion and id_responsable):
            messagebox.showwarning("Campos Vacíos", "Por favor, complete todos los campos.")
            return
        
        try:
            # Inserta el nuevo equipo en la base de datos
            cursor = self.db.conexion.cursor()
            cursor.execute("INSERT INTO equipo (id_equipo, nombre, modelo, tipo, fecha_adquisicion, id_responsable) VALUES (?, ?, ?, ?, ?, ?)",
                           (id_equipo, nombre, modelo, tipo, fecha_adquisicion, id_responsable))
            self.db.conexion.commit()
            messagebox.showinfo("Éxito", "Equipo agregado correctamente.")
            self.consultar_equipos()
            self.limpiar_campos()
            self.consultar_equipos()
        except Exception as e:
            messagebox.showerror("Error", f"Error al agregar equipo: {e}")

   # Método para consultar los equipos
    def consultar_equipos(self):
        # Verifica si hay conexión a la base de datos
        if not self.db.conexion:
            messagebox.showerror("Error de Conexión", "No hay conexión a la base de datos.")
            return
        # Ejecuta la consulta SQL para obtener los equipos
        cursor = self.db.conexion.cursor()
        cursor.execute("""
            SELECT 
                e.id_equipo,
                e.nombre,
                e.modelo,
                e.tipo,
                e.fecha_adquisicion,
                e.id_responsable,
                r.nombre AS nombre_responsable
            FROM equipo e, responsable r
            WHERE e.id_responsable = r.id_responsable;
        """)
        
        # Limpia el treeview antes de insertar nuevos datos
        for item in self.tree_equipos.get_children():
            self.tree_equipos.delete(item)

        # Inserta los datos obtenidos en el treeview de mantenimientos
        for equipo in cursor.fetchall():
            self.tree_equipos.insert("", "end", values=equipo)

    # Método para modificar un equipo
    def modificar_equipo(self):
        # Extrae los valores de los campos
        id_equipo = self.entry_id_equipo.get()
        nombre = self.entry_nombre.get()
        modelo = self.entry_modelo.get()
        tipo = self.entry_tipo.get()
        fecha_adquisicion = self.entry_fecha_adquisicion.get()
        id_responsable = self.entry_id_reponsable.get()

        # Verifica que todos los campos estén completos
        if not (id_equipo and nombre and modelo and tipo and fecha_adquisicion and id_responsable):
            messagebox.showwarning("Campos Vacíos", "Por favor, complete todos los campos.")
            return
        
        try:
            # Actualiza el equipo en la base de datos
            cursor = self.db.conexion.cursor()
            sql = "UPDATE equipo SET nombre=?, modelo=?, tipo=?, fecha_adquisicion=?, id_responsable=? WHERE id_equipo=?"
            cursor.execute(sql, (nombre, modelo, tipo, fecha_adquisicion, id_responsable, id_equipo))
            self.db.conexion.commit()
            messagebox.showinfo("Éxito", "Equipo actualizado correctamente.")
            self.limpiar_campos()
            self.consultar_equipos()
            return True
        except Exception as e:
            messagebox.showerror("Error al Actualizar", str(e))
            return False

    # Método para eliminar un equipo
    def eliminar_equipo(self):
        # Obtiene el id del equipo en el campo de id_equipo
        id_equipo = self.entry_id_equipo.get()
        nombre = self.entry_nombre.get()

        # Verifica que el campo de id_equipo no esté vacío
        if not id_equipo:
            messagebox.showwarning("Campo Vacío", "Por favor, ingrese el ID del equipo a eliminar.")
            return
        try:
            # Confirma la eliminación del equipo
            respuesta = messagebox.askyesno("Confirmar Eliminación", f"¿Estás seguro de eliminar el equipo {nombre} con ID {id_equipo}?")
            if not respuesta:
                return
            else:
                # Elimina el equipo de la base de datos
                cursor = self.db.conexion.cursor()
                sql = "DELETE FROM equipo WHERE id_equipo=?"
                cursor.execute(sql, (id_equipo,))
                self.db.conexion.commit()
                messagebox.showinfo("Éxito", "Equipo eliminado correctamente.")
                self.limpiar_campos()
                self.consultar_equipos()
                return True
        except Exception as e:
            messagebox.showerror("Error al Eliminar", str(e))
            return False
        
    # Método para obtener la selección del treeview de equipos y los pone en los campos correspondientes
    def obtener_seleccion(self, event):

        # Obtiene el item seleccionado en el treeview de equipos
        selected_item = self.tree_equipos.selection()
        if selected_item:
            item = self.tree_equipos.item(selected_item[0], 'values')
            self.entry_id_equipo.delete(0, tk.END)
            self.entry_id_equipo.insert(0, item[0])
            self.entry_nombre.delete(0, tk.END)
            self.entry_nombre.insert(0, item[1])
            self.entry_modelo.delete(0, tk.END)
            self.entry_modelo.insert(0, item[2])
            self.entry_tipo.delete(0, tk.END)
            self.entry_tipo.insert(0, item[3])
            self.entry_fecha_adquisicion.delete(0, tk.END)
            self.entry_fecha_adquisicion.insert(0, item[4])
            self.entry_id_reponsable.delete(0, tk.END)
            self.entry_id_reponsable.insert(0, item[5])

    # Método para limpiar los campos del formulario
    def limpiar_campos(self):
        self.entry_id_equipo.delete(0, tk.END)
        self.entry_nombre.delete(0, tk.END)     
        self.entry_modelo.delete(0, tk.END)
        self.entry_tipo.delete(0, tk.END)
        self.entry_fecha_adquisicion.delete(0, tk.END)
        self.entry_id_reponsable.delete(0, tk.END)

    # Método para ejecutar la aplicación
    def ejecutar(self):
        self.root.mainloop()

    # Método para confirmar la salida de la aplicación
    def al_cerrar_ventana(self):
        self.root.destroy()
        self.master.deiconify()
        self.master.state('zoomed')

if __name__ == "__main__":
    app = Equipos()
    app.ejecutar()