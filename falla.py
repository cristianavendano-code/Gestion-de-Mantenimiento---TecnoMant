import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from db_config import MiBaseDatos
from tkcalendar import DateEntry

class Falla:
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

    # Método para crear la interfaz de fallas
    def crear_interfaz(self):
        # Frame principal
        frame_principal = ttk.Frame(self.root)
        frame_principal.pack(fill="both", expand=True)

        # Frame de falla
        frame_falla = ttk.LabelFrame(frame_principal, text="Falla", padding=10)
        frame_falla.pack(side="right", fill="both", expand=True, padx=(5, 0))
        
       
        # Frame horizontal para organizar los campos y botones
        frame_horizontal = ttk.Frame(frame_falla)
        frame_horizontal.pack(fill="both", pady=10)

        # CAMPOS DE EQUIPO

        # Frame para los campos de mantenimiento
        falla_campos_frame = ttk.Frame(frame_horizontal)
        falla_campos_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        
        # Numero de falla
        ttk.Label(falla_campos_frame, text="Número de falla:").grid(row=0, column=0, sticky="w", pady=2)
        self.entry_numero_falla = ttk.Entry(falla_campos_frame, width=20)
        self.entry_numero_falla.grid(row=0, column=1, sticky="ew", padx=(5, 0), pady=2)

        # Id del equipo con combobox
        self.equipos = self.obtener_equipos()
        self.lista_id_equipo = [f"{id} - {nombre}" for id, nombre in self.equipos]

        # Combobox para seleccionar el ID del equipo
        ttk.Label(falla_campos_frame, text="ID del equipo:").grid(row=1, column=0, sticky="w", pady=2)
        self.entry_id_equipo = ttk.Combobox(falla_campos_frame, values=self.lista_id_equipo, state="readonly", width=40)
        self.entry_id_equipo.grid(row=1, column=1, sticky="ew", padx=(5, 0), pady=2)
        self.entry_id_equipo.bind("<<ComboboxSelected>>", self.seleccionar_equipo)

        # Nombre del equipo
        ttk.Label(falla_campos_frame, text="Nombre del equipo:").grid(row=2, column=0, sticky="w", pady=2)
        self.nombre_entry = ttk.Entry(falla_campos_frame, state="readonly", width=65)
        self.nombre_entry.grid(row=2, column=1, sticky="ew", padx=(5, 0), pady=2)

        # fecha del fallo
        ttk.Label(falla_campos_frame, text="Fecha de la falla:").grid(row=3, column=0, sticky="w", pady=2)
        self.entry_fecha_falla = DateEntry(
            falla_campos_frame,
            width=18,
            borderwidth=2,
            date_pattern='yyyy-mm-dd',
        )
        self.entry_fecha_falla.set_date(datetime.now())
        self.entry_fecha_falla.grid(row=3, column=1, sticky="ew", padx=(5, 0), pady=2)

        # Descripción
        ttk.Label(falla_campos_frame, text="Descripción:").grid(row=4, column=0, sticky="w", pady=2)
        self.entry_descripcion = ttk.Entry(falla_campos_frame, width=20)
        self.entry_descripcion.grid(row=4, column=1, sticky="ew", padx=(5, 0), pady=2)

        # Causa
        ttk.Label(falla_campos_frame, text="Causa:").grid(row=5, column=0, sticky="w", pady=2)
        self.entry_causa = ttk.Entry(falla_campos_frame, width=20)
        self.entry_causa.grid(row=5, column=1, sticky="ew", padx=(5, 0), pady=2)

        # Solución
        ttk.Label(falla_campos_frame, text="Solución:").grid(row=6, column=0, sticky="w", pady=2)
        self.entry_solucion = ttk.Entry(falla_campos_frame, width=20)
        self.entry_solucion.grid(row=6, column=1, sticky="ew", padx=(5, 0), pady=2)

        # Id tecnico
        ttk.Label(falla_campos_frame, text="ID técnico:").grid(row=7, column=0, sticky="w", pady=2)
        self.entry_id_tecnico = ttk.Entry(falla_campos_frame, width=20)
        self.entry_id_tecnico.grid(row=7, column=1, sticky="ew", padx=(5, 0), pady=2)

        # Organiza los campos de falla
        falla_campos_frame.columnconfigure(1, weight=1)
        
        # Frame para los botones
        frame_botones = ttk.Frame(frame_horizontal)
        frame_botones.grid(row=0, column=1, sticky="n")  # "n" para alinear arriba

        #Botones para agregar, editar, limpiar y eliminar falla
        ttk.Button(frame_botones, text="Agregar", width=20, command=self.agregar_falla).pack(pady=5)
        ttk.Button(frame_botones, text="Editar", width=20, command=self.modificar_falla).pack(pady=5)
        ttk.Button(frame_botones, text="Limpiar", width=20, command=self.limpiar_campos).pack(pady=5)
        ttk.Button(frame_botones, text="Eliminar", width=20, command=self.eliminar_falla).pack(pady=5)

         # Organza el frame de botones
        frame_horizontal.columnconfigure(0, weight=1)

        # Frame para espacio entre los campos y el treeview
        ttk.Label(frame_falla, text="Fallas registradas", font=("Arial", 10)).pack(pady=(10, 0))

        # frame para el treeview de fallas
        frame_tabla = ttk.Frame(frame_falla)
        frame_tabla.pack(fill="both", expand=True)

        # Definición de las columnas del treeview de fallas
        columnas_falla = ("# Falla", "ID Equipo", "Equipo", "Fecha de la falla","Descripción", "Causa", "Solución", "ID Técnico", "Técnico")
        self.tree_falla = ttk.Treeview(frame_tabla, columns=columnas_falla, show="headings", height=6)

        #  Define los anchos de cada columna del treeview
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
        for columna in columnas_falla:
            self.tree_falla.heading(columna, text=columna)
            self.tree_falla.column(columna, width=anchos_falla[columna], anchor="center")

        # Scrollbar vertical y horizontal para el treeview de fallas
        scrollbar_vertical = ttk.Scrollbar(frame_tabla, orient="vertical", command=self.tree_falla.yview)
        scrollbar_horizontal = ttk.Scrollbar(frame_tabla, orient="horizontal", command=self.tree_falla.xview)
        self.tree_falla.configure(yscrollcommand=scrollbar_vertical.set, xscrollcommand=scrollbar_horizontal.set)

        # Obtiene la selección del treeview de falla y ejecuta el metodo obtener_seleccion
        self.tree_falla.bind("<<TreeviewSelect>>", self.obtener_seleccion)

        # Ordenamos el treeview y los scrollbars dentro del frame contenedor
        # usamos grid para organizar los widgets en forma de tabla
        self.tree_falla.grid(row=0, column=0, sticky="nsew")
        scrollbar_vertical.grid(row=0, column=1, sticky="ns")
        scrollbar_horizontal.grid(row=1, column=0, sticky="ew")
        frame_tabla.grid_rowconfigure(0, weight=1)
        frame_tabla.grid_columnconfigure(0, weight=1)

        # Llama al método para consultar las fallas y llenar el treeview
        self.consultar_falla()

    # Método para agregar una falla
    def agregar_falla(self):
        # Obtiene los valores de los campos
        numero = self.entry_numero_falla.get()
        id_equipo = self.entry_id_equipo.get()
        fecha = self.entry_fecha_falla.get()
        descripcion = self.entry_descripcion.get()
        causa = self.entry_causa.get()
        solucion = self.entry_solucion.get()
        id_tecnico = self.entry_id_tecnico.get()

        # Verifica que todos los campos estén completos
        if not (numero and id_equipo and fecha and descripcion and causa and solucion and id_tecnico):
            messagebox.showwarning("Campos Vacíos", "Por favor, complete todos los campos.")
            return
        
        # Extrae solo el ID del equipo del campo combinado
        id_equipo = id_equipo.split(" - ")[0]

        try:
          # Inserta la falla en la base de datos
            cursor = self.db.conexion.cursor()
            cursor.execute("INSERT INTO falla (id_falla, id_equipo, fecha,  descripcion, causa, solucion, id_tecnico) VALUES (?, ?, ?, ?, ?, ?, ?)",
                        (numero, id_equipo, fecha, descripcion, causa, solucion, id_tecnico))
            self.db.conexion.commit()
            messagebox.showinfo("Éxito", "Se ha agregado el equipo con falla.")
            self.limpiar_campos()
            self.consultar_falla()
        except Exception as e:
            messagebox.showerror("Error", f"Error al agregar falla: {e}")

    # Método para consultar las fallas
    def consultar_falla(self):
        # verfica si hay conexión a la base de datos
        if not self.db.conexion:
            messagebox.showerror("Error de Conexión", "No hay conexión a la base de datos.")
            return
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
        for item in self.tree_falla.get_children():
            self.tree_falla.delete(item)

        # Inserta los datos obtenidos en el treeview de fallas
        for equipo in cursor.fetchall():
            self.tree_falla.insert("", "end", values=equipo)

    # Método para mdificar una falla
    def modificar_falla(self):
        # Extrae los valores de los campos
        numero = self.entry_numero_falla.get()
        id_equipo = self.entry_id_equipo.get()
        fecha = self.entry_fecha_falla.get()
        descripcion = self.entry_descripcion.get()
        causa = self.entry_causa.get()
        solucion = self.entry_solucion.get()
        id_tecnico = self.entry_id_tecnico.get()

        # Verifica que todos los campos estén completos
        if not (numero and id_equipo and fecha and descripcion and causa and solucion and id_tecnico):
            messagebox.showwarning("Campos Vacíos", "Por favor, complete todos los campos.")
            return
        
        # Extrae solo el ID del equipo del campo combinado
        id_equipo = id_equipo.split(" - ")[0] if " - " in id_equipo else id_equipo
        try:
            # Actualiza la falla en la base de datos
            cursor = self.db.conexion.cursor()
            cursor.execute("UPDATE falla SET id_equipo=?, fecha=?, descripcion=?, causa=?, solucion=?, id_tecnico=? WHERE id_falla=?",
                        (id_equipo, fecha, descripcion, causa, solucion, id_tecnico, numero))
            self.db.conexion.commit() 
            messagebox.showinfo("Éxito", "Se ha actualizado la falla.")
            self.limpiar_campos()
            self.consultar_falla()
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Error al modificar falla: {e}")
            return False
        
    # Método para eliminar una falla
    def eliminar_falla(self):
        # Obtiene el id de falla en el campo de id_falla
        id_falla = self.entry_numero_falla.get()

        # Verifica que el campo de id_falla no esté vacío
        if not id_falla:
            messagebox.showwarning("Campo Vacío", "Por favor, ingrese el número de la falla a eliminar.")
            return
        try:
            # Confirma la eliminación de la falla
            respuesta = messagebox.askyesno("Confirmar Eliminación", f"¿Estás seguro de eliminar la falla con ID: {id_falla}?")
            if not respuesta:
                return
            else:
                # Elimina la falla de la base de datos
                cursor = self.db.conexion.cursor()
                sql = "DELETE FROM falla WHERE id_falla=?"
                cursor.execute(sql, (id_falla,))
                self.db.conexion.commit()
                messagebox.showinfo("Éxito", "Falla eliminado correctamente.")
                self.limpiar_campos()
                self.consultar_falla()
                return True
        except Exception as e:
            messagebox.showerror("Error al Eliminar", str(e))
            return False

    # Método para obtener la selección del treeview de fallas y los pone en los campos correspondientes
    def obtener_seleccion(self, event):

        # Obtiene el item seleccionado en el treeview de fallas
        selected_item = self.tree_falla.selection()

        # Si hay un item seleccionado, extrae sus valores y los pone en los campos correspondientes
        if selected_item:
            item = self.tree_falla.item(selected_item[0], 'values')
            self.entry_numero_falla.delete(0, tk.END)
            self.entry_numero_falla.insert(0, item[0])
            self.entry_id_equipo.set(item[1])
            self.nombre_entry.config(state="normal")
            self.nombre_entry.delete(0, tk.END)
            self.nombre_entry.insert(0, item[2])
            self.nombre_entry.config(state="readonly")
            self.entry_fecha_falla.delete(0, tk.END)
            self.entry_fecha_falla.insert(0, item[3])
            self.entry_descripcion.delete(0, tk.END)
            self.entry_descripcion.insert(0, item[4])
            self.entry_causa.delete(0, tk.END)
            self.entry_causa.insert(0, item[5])
            self.entry_solucion.delete(0, tk.END)
            self.entry_solucion.insert(0, item[6])
            self.entry_id_tecnico.delete(0, tk.END)
            self.entry_id_tecnico.insert(0, item[7])

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
        self.entry_numero_falla.delete(0, tk.END)
        self.entry_id_equipo.set('')
        self.nombre_entry.config(state="normal")
        self.nombre_entry.delete(0, tk.END)
        self.nombre_entry.config(state="readonly")
        self.entry_fecha_falla.set_date(datetime.now())
        self.entry_descripcion.delete(0, tk.END)
        self.entry_causa.delete(0, tk.END)
        self.entry_solucion.delete(0, tk.END)
        self.entry_id_tecnico.delete(0, tk.END)

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
    app = Falla()
    app.ejecutar()