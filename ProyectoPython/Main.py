import tkinter as tk
from tkinter import ttk, messagebox
from pymongo import MongoClient, ReturnDocument
from PIL import Image, ImageTk

# Conexión a la base de datos
client = MongoClient("mongodb://localhost:27017/")
base = client["Hotel"]

# Función para contador
def contador(nombre_id):
    counter = base.Counters.find_one_and_update(
        {"id": nombre_id},
        {"$inc": {"seq": 1}},
        upsert=True,
        return_document=ReturnDocument
    )
    return counter["seq"]

# Función para abrir la ventana de gestión de departamentos
def ventana_departamentos():
    ventana_dep = tk.Toplevel()
    ventana_dep.title("Gestión de Departamentos")
    ventana_dep.geometry("800x600")

    # Tabla para mostrar los departamentos
    tabla_departamentos = ttk.Treeview(ventana_dep, columns=2)
    tabla_departamentos.grid(row=0, column=0, columnspan=2, pady=10)
    tabla_departamentos.heading("#0", text="ID Departamento")
    tabla_departamentos.heading("#1", text="Descripción")

    # Función para mostrar departamentos
    def mostrar_departamentos():
        try:
            registros = tabla_departamentos.get_children()
            for registro in registros:
                tabla_departamentos.delete(registro)
            for documento in base.Departamentos.find():
                tabla_departamentos.insert('', 0, text=documento["id_departamento"], values=documento["Descripcion"])
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar los departamentos: {e}")

    # Función para crear un departamento
    def crear_departamento():
        if len(id_departamento.get()) != 0 and len(descripcion.get()) != 0:
            try:
                documento = {
                    "id_departamento": int(id_departamento.get()),
                    "Descripcion": descripcion.get()
                }
                base.Departamentos.insert_one(documento)
                id_departamento.delete(0, tk.END)
                descripcion.delete(0, tk.END)
                mostrar_departamentos()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo crear el departamento: {e}")
        else:
            messagebox.showerror("Error", "Los campos no pueden estar vacíos")

    # Función para eliminar un departamento
    def eliminar_departamento():
        try:
            selected_item = tabla_departamentos.selection()[0]
            id_dep = tabla_departamentos.item(selected_item, "text")
            base.Departamentos.delete_one({"id_departamento": int(id_dep)})
            mostrar_departamentos()
        except IndexError:
            messagebox.showwarning("Advertencia", "Selecciona un departamento para eliminar")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar el departamento: {e}")

    # Función para modificar un departamento
    def modificar_departamento():
        try:
            selected_item = tabla_departamentos.selection()[0]
            id_dep = tabla_departamentos.item(selected_item, "text")
            nueva_descripcion = descripcion.get()

            if len(nueva_descripcion) == 0:
                messagebox.showerror("Error", "La descripción no puede estar vacía")
                return

            base.Departamentos.update_one(
                {"id_departamento": int(id_dep)},
                {"$set": {"Descripcion": nueva_descripcion}}
            )
            descripcion.delete(0, tk.END)
            mostrar_departamentos()
        except IndexError:
            messagebox.showwarning("Advertencia", "Selecciona un departamento para modificar")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo modificar el departamento: {e}")

    # Campos de entrada y botones
    tk.Label(ventana_dep, text="ID Departamento").grid(row=1, column=0)
    id_departamento = tk.Entry(ventana_dep)
    id_departamento.grid(row=1, column=1)

    tk.Label(ventana_dep, text="Descripción").grid(row=2, column=0)
    descripcion = tk.Entry(ventana_dep)
    descripcion.grid(row=2, column=1)

    tk.Button(ventana_dep, text="Crear", command=crear_departamento, bg="light green", fg="black").grid(row=3, column=0, pady=10)
    tk.Button(ventana_dep, text="Modificar", command=modificar_departamento, bg="light yellow", fg="black").grid(row=3, column=1, pady=10)
    tk.Button(ventana_dep, text="Eliminar", command=eliminar_departamento, bg="red", fg="black").grid(row=3, column=2, pady=10)

    # Cargar los departamentos inicialmente
    mostrar_departamentos()

# Ventana principal
ventana = tk.Tk()
ventana.title('Menú principal de la Hotelera')
ventana.geometry('800x600')

barra_menu = tk.Menu(ventana)
ventana.config(menu=barra_menu)

menu = tk.Menu(barra_menu, tearoff=False)

menu.add_command(label='Gestionar Clientes')#Shernna
menu.add_command(label='Gestionar Departamentos', command=ventana_departamentos) #Marco
menu.add_command(label='Gestionar Empleados')#Shernna #
menu.add_command(label='Gewstionar Eventos')#Keyla
menu.add_command(label='Gestionar Habitaciones')#Adriela
menu.add_command(label='Gestionar Sedes de Hotel')#Adriela
menu.add_command(label='Gestionar Mantenimientos')#Rachel
menu.add_command(label='Gestionar Registros')#Rachel
menu.add_command(label='Gestionar Reservaciones')#Keyla
menu.add_command(label='Gestionar Servicios')#Marco
menu.add_command(label='Cancelar Factura')#Marco
menu.add_separator()
menu.add_command(label='Salir', command=ventana.destroy)

barra_menu.add_cascade(label="Menú", menu=menu)

# Cargar imagen
try:
    imagen_original = Image.open('img/hotelera.jpg')
    imagen_redimensionada = imagen_original.resize((800, 600))  # Ajustar el tamaño de la imagen
    imagen = ImageTk.PhotoImage(imagen_redimensionada)

    # Crear un canvas para colocar la imagen y el texto
    canvas = tk.Canvas(ventana, width=800, height=600)
    canvas.pack()

    # Colocar la imagen en el canvas
    canvas.create_image(0, 0, anchor="nw", image=imagen)

    # Agregar el texto en el centro del canvas
    canvas.create_text(400, 300, text="Bienvenido al sistema de gestión hotelera", font=("Times New Roman", 24, "bold"),
                       fill="white")
except tk.TclError:
    messagebox.showerror("Error", "No se pudo cargar la imagen")

ventana.mainloop()
