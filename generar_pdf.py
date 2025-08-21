from reportlab.lib.pagesizes import letter, landscape #tamaño de hoja y orientación
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle # estilos de texto
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak # elementos del PDF
from datetime import datetime 
from db_config import MiBaseDatos
from tkinter import messagebox
import os 


class GenerarPDF:
    def __init__(self):
        # Inicializar conexión a la base de datos
        self.db = MiBaseDatos()
        self.db.conectar()

    # Método para generar el PDF del reporte completo
    def generar_pdf_reporte_completo(self):

        # CONFIGURACIÓN DEL PDF

        # Nombre del archivo con fecha actual
        fecha_actual = datetime.now().strftime("%Y-%m-%d")
        pdf_file = f"reporte_{fecha_actual}.pdf"

        # Se crea el documento PDF
        doc = SimpleDocTemplate(pdf_file, pagesize=landscape(letter))

        # Estilo por defecto y estilo de celda
        estilo = getSampleStyleSheet()
        estilo_celda = ParagraphStyle(name='celda', fontSize=8, leading=8)

        # Aqu[i se guardan todos los elementos del pdf: tablas, parrafos, etc.
        contenido = []

        # Cursor para ejecutar consultas
        cursor = self.db.conexion.cursor()

        # MANTENIMIENTO
        # Titulo de la sección mantenimiento
        contenido.append(Paragraph("Reporte de Mantenimientos", estilo['Title']))
        contenido.append(Spacer(1, 10))

        # crea las columnas que llevará la tabla mantenimientos
        columnas_mantenimiento = ["# Mant...", "ID Equipo", "Equipo",  "Descripción",  "ID Técnico",  "Técnico",  "Próximo Mantenimiento"]
        datos_mantenimiento = [columnas_mantenimiento]

        # Consulta para obtener los datos necesarios de mantenimientos
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

        # Ciclo para agregar los datos de mantenimiento en la tabla
        for fila in cursor.fetchall():
            datos_mantenimiento.append([
                str(fila[0]),
                str(fila[1]),
                str(fila[2]),
                Paragraph(str(fila[3]), estilo_celda),
                str(fila[4]),
                str(fila[5]),
                str(fila[6]),
            ])

        # Anchos de las columnas de mantenimiento
        columna_ancho_mantenimiento = [50, 50, 80, 150, 50, 80, 100]

        # Crea la tabla de mantenimiento con los datos y estilos 
        tabla_mantenimiento = Table(datos_mantenimiento, colWidths=columna_ancho_mantenimiento, repeatRows=1)

        # Estilo de la tabla de mantenimiento
        tabla_mantenimiento.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#CDEAC0')), ('GRID', (0, 0), (-1, -1), 0.5, colors.black), ('ALIGN', (0, 0), (-1, -1), 'CENTER'), ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'), ('FONTSIZE', (0, 0), (-1, -1), 8)]))
        
        # Finalmente agrega la tabla al contenido[] del pdf
        contenido.append(tabla_mantenimiento)
        contenido.append(PageBreak())

        # FALLAS
        # titulo de la sección fallas
        contenido.append(Paragraph("Reporte de Fallas", estilo['Title']))
        contenido.append(Spacer(1, 10))

        # crea las columnas que llevará la tabla fallas
        columnas_falla = ["ID Falla", "ID Equipo", "Equipo", "Descripción", "Causa", "Solución", "ID Técnico", "Técnico"]
        datos_falla = [columnas_falla]

        # Consulta para obtener los datos necesarios de fallas
        cursor.execute("""
            SELECT 
                f.id_falla,
                e.id_equipo,
                e.nombre,
                f.descripcion,
                f.causa,
                f.solucion,
                t.id_tecnico,
                t.nombre
            FROM falla f, equipo e, tecnico t
            WHERE f.id_equipo = e.id_equipo
            AND f.id_tecnico = t.id_tecnico;
        """)

        # Ciclo para agregar los datos de fallas en la tabla
        for fila in cursor.fetchall():
            datos_falla.append([
                str(fila[0]),
                str(fila[1]),
                str(fila[2]),
                Paragraph(str(fila[3]), estilo_celda),
                Paragraph(str(fila[4]), estilo_celda),
                Paragraph(str(fila[5]), estilo_celda),
                str(fila[6]),
                str(fila[7]),
            ])

        # Anchos de las columnas de fallas
        columna_ancho_falla = [50, 50, 100, 100, 100, 100, 50, 100]
        
        # Crea la tabla de fallas con los datos y estilos
        tabla_falla = Table(datos_falla, colWidths=columna_ancho_falla, repeatRows=1)
        
        # Estilo de la tabla de fallas
        tabla_falla.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#F9D5E5')), ('GRID', (0, 0), (-1, -1), 0.5, colors.black),  ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  ('FONTSIZE', (0, 0), (-1, -1), 8)]))
        
        # Finalmente agrega la tabla al contenido[] del pdf
        contenido.append(tabla_falla)
        contenido.append(PageBreak())

        # EQUIPOS
        # titulo de la sección equipos
        contenido.append(Paragraph("Reporte de Equipos", estilo['Title']))
        contenido.append(Spacer(1, 10))

        # crea las columnas que llevará la tabla equipos
        columnas_equipos = ["ID Equipo", "Nombre", "Modelo", "Tipo",  "Fecha Adquisición", "ID Responsable", "Responsable"]
        datos_equipos = [columnas_equipos]

        # Consulta para obtener los datos necesarios de equipos
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

        # Ciclo para agregar los datos de equipos en la tabla
        for fila in cursor.fetchall():
            datos_equipos.append([
                str(fila[0]),
                str(fila[1]),
                str(fila[2]),
                str(fila[3]),
                str(fila[4]),
                str(fila[5]),
                str(fila[6]),
            ])

        # Anchos de las columnas de equipos
        columna_ancho_equipos = [50, 100, 80, 80, 80, 60, 150]
        
        # Crea la tabla de equipos con los datos y estilos
        tabla_equipos = Table(datos_equipos, colWidths=columna_ancho_equipos, repeatRows=1)
        
        # Estilo de la tabla de equipos
        tabla_equipos.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#D0E4F2')),  ('GRID', (0, 0), (-1, -1), 0.5, colors.black),  ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  ('FONTSIZE', (0, 0), (-1, -1), 8)]))
        contenido.append(tabla_equipos)

        # Genera el PDF con el contenido
        doc.build(contenido)
        messagebox.showinfo("PDF generado", f"El reporte se guardó como: {pdf_file}")

        # Abre el PDF generado
        os.startfile(pdf_file)

