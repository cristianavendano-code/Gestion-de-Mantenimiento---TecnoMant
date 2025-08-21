import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from db_config import MiBaseDatos
from tkcalendar import DateEntry

class Mantenimiento:
    def __init__(self, master, callback_actualizar):
        # self.master es la ventana principal de la aplicación
        self.master = master
        # Callback_actualizar es el metodo de la clase SistemaMantenimiento que actualiza el treeview de mantenimientos
        self.callback_actualizar = callback_actualizar

        # Crea una nueva ventana para el mantenimiento.
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
        
    # Método para crear la interfaz de mantenimientos
    def crear_interfaz(self):
        # Frame principal
        frame_principal = ttk.Frame(self.root)
        frame_principal.pack(fill="both", expand=True)

        # Frame de mantenimiento
        frame_mantenimiento = ttk.LabelFrame(frame_principal, text="Mantenimiento", padding=10)
        frame_mantenimiento.pack(side="right", fill="both", expand=True, padx=(5, 0))
        
        # Frame horizontal para organizar los campos y botones
        frame_horizontal = ttk.Frame(frame_mantenimiento)
        frame_horizontal.pack(fill="both", pady=10)

        # CAMPOS DE MANTENIMIENTO

        # Frame para los campos de mantenimiento
        mantenimiento_campos_frame = ttk.Frame(frame_horizontal)
        mantenimiento_campos_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        
        # Numero de mantenimiento
        ttk.Label(mantenimiento_campos_frame, text="Número de mantenimiento:").grid(row=0, column=0, sticky="w", pady=2)
        self.entry_numero_mantenimiento = ttk.Entry(mantenimiento_campos_frame, width=20)
        self.entry_numero_mantenimiento.grid(row=0, column=1, sticky="ew", padx=(5, 0), pady=2)

        # Id del equipo con combobox
        self.equipos = self.obtener_equipos()
        self.lista_id_equipo = [f"{id} - {nombre}" for id, nombre in self.equipos]

        # Combobox para seleccionar el ID del equipo
        ttk.Label(mantenimiento_campos_frame, text="ID del equipo:").grid(row=1, column=0, sticky="w", pady=2)
        self.entry_id_equipo = ttk.Combobox(mantenimiento_campos_frame, values=self.lista_id_equipo, state="readonly", width=40)
        self.entry_id_equipo.grid(row=1, column=1, sticky="ew", padx=(5, 0), pady=2)
        self.entry_id_equipo.bind("<<ComboboxSelected>>", self.seleccionar_equipo)

        # Nombre del equipo
        ttk.Label(mantenimiento_campos_frame, text="Nombre del equipo:").grid(row=2, column=0, sticky="w", pady=2)
        self.nombre_entry = ttk.Entry(mantenimiento_campos_frame, state="readonly", width=65)
        self.nombre_entry.grid(row=2, column=1, sticky="ew", padx=(5, 0), pady=2)

        # Descripcion
        ttk.Label(mantenimiento_campos_frame, text="Descripción:").grid(row=3, column=0, sticky="w", pady=2)
        self.entry_descripcion = ttk.Entry(mantenimiento_campos_frame, width=20)
        self.entry_descripcion.grid(row=3, column=1, sticky="ew", padx=(5, 0), pady=2)

        # ID tecnico
        ttk.Label(mantenimiento_campos_frame, text="ID técnico:").grid(row=4, column=0, sticky="w", pady=2)
        self.entry_id_tecnico = ttk.Entry(mantenimiento_campos_frame, width=20)
        self.entry_id_tecnico.grid(row=4, column=1, sticky="ew", padx=(5, 0), pady=2)

        # Proximo mantenimiento en formato fecha
        ttk.Label(mantenimiento_campos_frame, text="Próximo mantenimiento:").grid(row=6, column=0, sticky="w", pady=2)
        self.entry_proximo_mantenimiento = DateEntry(mantenimiento_campos_frame, width=18, borderwidth=2, date_pattern='yyyy-mm-dd')
        self.entry_proximo_mantenimiento.set_date(datetime.now())
        self.entry_proximo_mantenimiento.grid(row=6, column=1, sticky="ew", padx=(5, 0), pady=2)

        # Organiza los campos del mantenimiento
        mantenimiento_campos_frame.columnconfigure(1, weight=1)
        
        # Frame para los botones
        frame_botones = ttk.Frame(frame_horizontal)
        frame_botones.grid(row=0, column=1, sticky="n")

        # Botones para agregar, editar, limpiar y eliminar mantenimientos
        ttk.Button(frame_botones, text="Agregar", width=20, command=self.agregar_mantenimiento).pack(pady=5)
        ttk.Button(frame_botones, text="Editar", width=20, command=self.modificar_mantenimiento).pack(pady=5)
        ttk.Button(frame_botones, text="Limpiar", width=20, command=self.limpiar_campos).pack(pady=5)
        ttk.Button(frame_botones, text="Eliminar", width=20, command=self.eliminar_mantenimiento).pack(pady=5)

        # Organiza el frame de botones
        frame_horizontal.columnconfigure(0, weight=1)

        # Frame para el treeview de mantenimientos
        ttk.Label(frame_mantenimiento, text="Mantenimientos registrados", font=("Arial", 10)).pack(pady=(10, 0))

        # Definición de las columnas del treeview de mantenimientos
        columnas_mantenimiento = ("ID Mantenimiento", "ID Equipo", "Equipo", "Descripción", "ID Técnico", "Técnico", "Próximo Mantenimiento")
        self.tree_mantenimiento = ttk.Treeview(frame_mantenimiento, columns=columnas_mantenimiento, show="headings", height=6)

        #  Define los anchos de cada columna del treeview
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
        scrollbar_mantenimiento = ttk.Scrollbar(frame_mantenimiento, orient="vertical", command=self.tree_mantenimiento.yview)
        self.tree_mantenimiento.configure(yscrollcommand=scrollbar_mantenimiento.set)

        # Obtiene la selección del treeview de mantenimientos y ejecuta el metodo obtener_seleccion
        self.tree_mantenimiento.bind("<<TreeviewSelect>>", self.obtener_seleccion)

        # Ordenamos el treview y el scrollbar dentro del frame contenedor
        self.tree_mantenimiento.pack(side="left", fill="both", expand=True)
        scrollbar_mantenimiento.pack(side="left", fill="y")

        # Ejecuta la consulta para llenar el treeview de mantenimientos
        self.consultar_mantenimiento()

    # Método para agregar un mantenimiento
    def agregar_mantenimiento(self):
        # Obtiene los valores de los campos
        numero = self.entry_numero_mantenimiento.get()
        id_equipo_completo = self.entry_id_equipo.get()
        descripcion = self.entry_descripcion.get()
        id_tecnico = self.entry_id_tecnico.get()
        proximo_mantenimiento = self.entry_proximo_mantenimiento.get()

        # Verifica que todos los campos estén completos
        if not (numero and id_equipo_completo and descripcion and id_tecnico and proximo_mantenimiento):
            messagebox.showwarning("Campos Vacíos", "Por favor, complete todos los campos.")
            return
        
        # Extrae solo el ID del equipo del campo combinado
        id_equipo = id_equipo_completo.split(" - ")[0]

        try:
            # Inserta el mantenimiento en la base de datos
            cursor = self.db.conexion.cursor()
            cursor.execute("INSERT INTO mantenimiento (id_mantenimiento, id_equipo, descripcion, id_tecnico, proximo_mantenimiento) VALUES (?, ?, ?, ?, ?)",
                        (numero, id_equipo, descripcion, id_tecnico, proximo_mantenimiento))
            self.db.conexion.commit()
            messagebox.showinfo("Éxito", "Se ha agregado el mantenimiento.")
            self.limpiar_campos()
            self.consultar_mantenimiento()
        except Exception as e:
            messagebox.showerror("Error", f"Error al agregar mantenimiento: {e}")

    # Método para consultar los mantenimeintos
    def consultar_mantenimiento(self):
        # Verifica si hay conexión a la base de datos
        if not self.db.conexion:
            messagebox.showerror("Error de Conexión", "No hay conexión a la base de datos.")
            return
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

        # Limpia el treeview antes de insertar nuevos datos
        for item in self.tree_mantenimiento.get_children():
            self.tree_mantenimiento.delete(item)
        
        # Inserta los datos obtenidos en el treeview de mantenimientos
        for equipo in cursor.fetchall():
            self.tree_mantenimiento.insert("", "end", values=equipo)
        self.db.conexion.commit()

    # Método para modificar un mantenimimiento
    def modificar_mantenimiento(self):
        # Extrae los valores de los campos
        numero = self.entry_numero_mantenimiento.get()
        id_equipo_completo = self.entry_id_equipo.get()
        descripcion = self.entry_descripcion.get()
        id_tecnico = self.entry_id_tecnico.get()
        proximo_mantenimiento = self.entry_proximo_mantenimiento.get()

        # Verifica que todos los campos estén completos
        if not (numero and id_equipo_completo and descripcion and id_tecnico and proximo_mantenimiento):
            messagebox.showwarning("Campos Vacíos", "Por favor, complete todos los campos.")
            return
        
        # Extrae solo el ID del equipo del campo combinado
        id_equipo = id_equipo_completo.split(" - ")[0] if " - " in id_equipo_completo else id_equipo_completo

        try:
            # Actualiza el mantenimiento en la base de datos
            cursor = self.db.conexion.cursor()
            cursor.execute("UPDATE mantenimiento SET id_equipo=?, descripcion=?, id_tecnico=?, proximo_mantenimiento=? WHERE id_mantenimiento=?",
                        (id_equipo, descripcion, id_tecnico, proximo_mantenimiento, numero))
            self.db.conexion.commit() 
            messagebox.showinfo("Éxito", "Se ha actualizado el mantenimiento.")
            self.limpiar_campos()
            self.consultar_mantenimiento()
            return True
        
        except Exception as e:
            messagebox.showerror("Error", f"Error al modificar mantenimiento: {e}")
            return False
        
    # Método para eliminar un mantenimiento
    def eliminar_mantenimiento(self):
        # Obtiene el id de mantenimineto en el campo de id_mantenimiento
        id_mantenimiento = self.entry_numero_mantenimiento.get()

        # Verifica que el campo de id_mantenimiento no esté vacío
        if not id_mantenimiento:
            messagebox.showwarning("Campo Vacío", "Por favor, ingrese el número del mantenimiento a eliminar.")
            return
        try:
            # Confirma la eliminación del mantenimiento
            respuesta = messagebox.askyesno("Confirmar Eliminación", f"¿Estás seguro de eliminar el proximo mantenimiento con ID: {id_mantenimiento}?")
            if not respuesta:
                return
            else:
                # Elimina el mantenimiento de la base de datos
                cursor = self.db.conexion.cursor()
                sql = "DELETE FROM mantenimiento WHERE id_mantenimiento=?"
                cursor.execute(sql, (id_mantenimiento,))
                self.db.conexion.commit()
                messagebox.showinfo("Éxito", "Mantenimiento eliminado correctamente.")
                self.limpiar_campos()
                self.consultar_mantenimiento()
                return True
        except Exception as e:
            messagebox.showerror("Error al Eliminar", str(e))
            return False

    # Método para obtener la selección del treeview de mantenimientos y los pone en los campos correspondientes
    def obtener_seleccion(self, event):

        # Obtiene el item seleccionado en el treeview de mantenimientos
        selected_item = self.tree_mantenimiento.selection()

        # Si hay un item seleccionado, extrae sus valores y los pone en los campos correspondientes
        if selected_item:
            item = self.tree_mantenimiento.item(selected_item[0], 'values')
            self.entry_numero_mantenimiento.delete(0, tk.END)
            self.entry_numero_mantenimiento.insert(0, item[0])
            self.entry_id_equipo.set(item[1])
            self.nombre_entry.config(state="normal")
            self.nombre_entry.delete(0, tk.END)
            self.nombre_entry.insert(0, item[2])
            self.nombre_entry.config(state="readonly")
            self.entry_descripcion.delete(0, tk.END)
            self.entry_descripcion.insert(0, item[3])
            self.entry_id_tecnico.delete(0, tk.END)
            self.entry_id_tecnico.insert(0, item[4])
            self.entry_proximo_mantenimiento.delete(0, tk.END)
            self.entry_proximo_mantenimiento.insert(0, item[6])

    # Método para obtener los equipos de la base de datos
    def obtener_equipos(self):
        try:
            # Ejecuta la consulta SQL para obtener los equipos
            cursor = self.db.conexion.cursor()
            cursor.execute("SELECT id_equipo, nombre FROM equipo")
            return cursor.fetchall()
        except Exception as e:
            messagebox.showerror("Error", f"Error al obtener equipos: {e}")
            return []
    
    # Método para seleccionar un equipo del combobox y mostrar su nombre en el campo correspondiente
    def seleccionar_equipo(self, event=None):

        # Obtiene el valor seleccionado en el combobox
        seleccion = self.entry_id_equipo.get()

        # Si hay una selección y contiene " - ", extrae el ID y el nombre del equipo
        if seleccion and " - " in seleccion:
            id_equipo, nombre_equipo = seleccion.split(" - ", 1)

            # Mostrar solo el id en el combobox
            self.entry_id_equipo.set(id_equipo)

            # Mostrar solo el nombre en el campo nombre
            self.nombre_entry.config(state="normal")
            self.nombre_entry.delete(0, tk.END)
            self.nombre_entry.insert(0, nombre_equipo)
            self.nombre_entry.config(state="readonly")

        
    # Método para limpiar los campos del formulario
    def limpiar_campos(self):
        self.entry_numero_mantenimiento.delete(0, tk.END)
        self.entry_id_equipo.set('')
        self.nombre_entry.config(state="normal")
        self.nombre_entry.delete(0, tk.END)
        self.nombre_entry.config(state="readonly")
        self.entry_descripcion.delete(0, tk.END)
        self.entry_id_tecnico.delete(0, tk.END)
        self.entry_proximo_mantenimiento.set_date(datetime.now())

    # Método para ejecutar la aplicación
    def ejecutar(self):
        self.root.mainloop()

    # Método para confirmar la salida de la aplicación
    def al_cerrar_ventana(self):
        self.root.destroy()
        self.master.deiconify()
        self.master.state('zoomed')
        self.callback_actualizar()

if __name__ == "__main__":
    app = Mantenimiento()
    app.ejecutar()