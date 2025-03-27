import mysql.connector
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog

# Configuración de la conexión a MySQL
conexion = mysql.connector.connect(
    host="192.168.137.38",
    user="emerson",
    password="shadow.2005.SHADOW",
    database="imager"
)

# Función para añadir un objeto (nombre)
def agregar_objeto():
    nombre_objeto = simpledialog.askstring("Añadir Objeto", "Ingrese el nombre del objeto:")
    if not nombre_objeto:
        return

    try:
        cursor = conexion.cursor()
        sql = "INSERT INTO objetos (nombre) VALUES (%s)"
        cursor.execute(sql, (nombre_objeto,))
        conexion.commit()
        messagebox.showinfo("Éxito", f"Objeto '{nombre_objeto}' añadido correctamente.")
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"No se pudo agregar el objeto: {err}")
    finally:
        cursor.close()

# Función para subir imagen y enlazarla con un objeto existente
def subir_imagen():
    cursor = conexion.cursor()
    cursor.execute("SELECT id, nombre FROM objetos")
    objetos = cursor.fetchall()
    
    if not objetos:
        messagebox.showwarning("Advertencia", "No hay objetos registrados. Agrega uno primero.")
        return

    # Mostrar lista de objetos disponibles
    objeto_elegido = simpledialog.askinteger("Seleccionar Objeto", 
                                             "Ingrese el ID del objeto para asociar la imagen:\n" +
                                             "\n".join([f"{id} - {nombre}" for id, nombre in objetos]))
    
    if not objeto_elegido:
        return
    
    # Seleccionar imagen
    ruta_imagen = filedialog.askopenfilename(title="Seleccionar imagen", filetypes=[("Todos los archivos", "*.*")])
    if not ruta_imagen:
        return

    try:
        with open(ruta_imagen, "rb") as file:
            imagen_binaria = file.read()
        
        # Insertar imagen vinculada al objeto seleccionado
        sql = "INSERT INTO imagenes (id_imager, imagen) VALUES (%s, %s)"
        cursor.execute(sql, (objeto_elegido, imagen_binaria))
        conexion.commit()
        messagebox.showinfo("Éxito", "Imagen subida y enlazada correctamente.")
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"No se pudo subir la imagen: {err}")
    finally:
        cursor.close()

# Crear ventana con Tkinter
ventana = tk.Tk()
ventana.title("Gestión de Objetos e Imágenes")
ventana.geometry("350x200")

btn_objeto = tk.Button(ventana, text="Añadir Objeto", command=agregar_objeto)
btn_objeto.pack(pady=10)

btn_imagen = tk.Button(ventana, text="Subir Imagen y Asociar", command=subir_imagen)
btn_imagen.pack(pady=10)

ventana.mainloop()

# Cerrar conexión
conexion.close()
