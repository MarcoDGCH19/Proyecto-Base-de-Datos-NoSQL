import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from click import command
from pymongo import MongoClient, ReturnDocument
from PIL import Image, ImageTk
from datetime import datetime, timezone

# Conexión a la base de datos
client = MongoClient("mongodb://localhost:27017/")
base = client["Hotel"]

# Función para contador
def contador(nombre_id):
    counter = base.Counters.find_one_and_update(
        {"id": nombre_id},
        {"$inc": {"seq": 1}},
        upsert=True,
        return_document=ReturnDocument.AFTER
    )
    return counter["seq"]

# Función para abrir la ventana de gestión de clientes
def ventana_clientes():
    ventana_cli = tk.Toplevel()
    ventana_cli.title("Gestión de Clientes")
    ventana_cli.geometry("1000x600")

    # Tabla para mostrar los clientes
    tabla_clientes = ttk.Treeview(ventana_cli, columns=("ID cliente", "Nombre cliente", "Correo cliente","Telefono cliente", "Direccion cliente"))
    tabla_clientes.grid(row=0, column=0, columnspan=5, pady=10)
    tabla_clientes.heading("#0", text="ID cliente")
    tabla_clientes.heading("#1", text="Nombre cliente")
    tabla_clientes.heading("#2", text="Correo cliente")
    tabla_clientes.heading("#3", text="Telefono cliente")
    tabla_clientes.heading("#4", text="Direccion cliente")
    # Función para mostrar clientes
    def mostrar_clientes():
        try:
            clientes = tabla_clientes.get_children()
            for cliente_temporal in clientes:
                tabla_clientes.delete(cliente_temporal)
            for cliente in base.Clientes.find():
                tabla_clientes.insert('', 0, text=cliente["id_cliente"], values=(cliente["nombre"]
                                      , cliente["correo"], cliente["telefono"]
                                      , cliente["Direccion"]))
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar los cliente: {e}")

    # Función para crear un cliente
    def crear_cliente():
        if len(id_cliente.get()) != 0 and len(nombre_cliente.get()) != 0 and len(telefono_cliente.get()) != 0 and len(correo_cliente.get()) != 0 and len(direccion_cliente.get()) != 0:
            try:
                cliente = {
                    "id_cliente": int(id_cliente.get()),
                    "nombre": nombre_cliente.get(),
                    "correo": correo_cliente.get(),
                    "telefono": telefono_cliente.get(),
                    "Direccion": direccion_cliente.get()
                }
                base.Clientes.insert_one(cliente)
                id_cliente.delete(0, tk.END)
                nombre_cliente.delete(0, tk.END)
                correo_cliente.delete(0, tk.END)
                telefono_cliente.delete(0, tk.END)
                direccion_cliente.delete(0, tk.END)
                mostrar_clientes()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo crear el cliente: {e}")
        else:
            messagebox.showerror("Error", "Los campos no pueden estar vacíos.")

    # Función para eliminar un cliente
    def eliminar_cliente():
        try:
            selected_item = tabla_clientes.selection()[0]
            id_cli = tabla_clientes.item(selected_item, "text")
            base.Clientes.delete_one({"id_cliente": int(id_cli)})
            mostrar_clientes()
        except IndexError:
            messagebox.showwarning("Advertencia", "Seleccione un cliente para eliminar.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar el cliente: {e}")

    # Función para modificar un cliente
    def modificar_cliente():
        try:
            selected_item = tabla_clientes.selection()[0]
            id_cli = tabla_clientes.item(selected_item, "text")
            nuevo_nombre = nombre_cliente.get()
            nuevo_correo = correo_cliente.get()
            nuevo_telefono = telefono_cliente.get()
            nueva_direccion = direccion_cliente.get()

            if len(nuevo_nombre) == 0:
                messagebox.showerror("Error", "El nombre no puede estar vacío.")
                return
            if len(nuevo_telefono) == 0:
                messagebox.showerror("Error", "El teléfono no puede estar vacío.")
                return
            if len(nuevo_correo) == 0:
                messagebox.showerror("Error", "El correo no puede estar vacío.")
                return
            if len(nueva_direccion) == 0:
                messagebox.showerror("Error", "La dirección no puede estar vacía.")
                return

            base.Clientes.update_one(
                {"id_cliente": int(id_cli)},
                {"$set": {"nombre": nuevo_nombre,
                          "correo": nuevo_correo,
                          "telefono": nuevo_telefono,
                          "Direccion": nueva_direccion}}
            )
            nombre_cliente.delete(0, tk.END)
            correo_cliente.delete(0, tk.END)
            telefono_cliente.delete(0, tk.END)
            direccion_cliente.delete(0, tk.END)
            mostrar_clientes()
        except IndexError:
            messagebox.showwarning("Advertencia", "Selecciona un cliente para modificar")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo modificar el cliente: {e}")
   # Campos de entrada y botones para cliente
    tk.Label(ventana_cli, text="ID Cliente").grid(row=1, column=0)
    id_cliente = tk.Entry(ventana_cli)
    id_cliente.grid(row=1, column=1)

    tk.Label(ventana_cli, text="Nombre cliente").grid(row=2, column=0)
    nombre_cliente = tk.Entry(ventana_cli)
    nombre_cliente.grid(row=2, column=1)

    tk.Label(ventana_cli, text="Correo cliente").grid(row=3, column=0)
    correo_cliente = tk.Entry(ventana_cli)
    correo_cliente.grid(row=3, column=1)

    tk.Label(ventana_cli, text="Teléfono cliente").grid(row=4, column=0)
    telefono_cliente = tk.Entry(ventana_cli)
    telefono_cliente.grid(row=4, column=1)

    tk.Label(ventana_cli, text="Direccion cliente").grid(row=5, column=0)
    direccion_cliente = tk.Entry(ventana_cli)
    direccion_cliente.grid(row=5, column=1)

    tk.Button(ventana_cli, text="Agregar", command=crear_cliente, bg="#4CAF50", fg="white").grid(row=6, column=0, pady=10)
    tk.Button(ventana_cli, text="Modificar", command=modificar_cliente, bg="#4CAF50", fg="white").grid(row=6, column=1, pady=10)
    tk.Button(ventana_cli, text="Eliminar", command=eliminar_cliente, bg="#ca0000", fg="white").grid(row=6, column=2, pady=10)

    # Cargar los clientes inicialmente
    mostrar_clientes()

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

    # Campos de entrada y botones para departamento
    tk.Label(ventana_dep, text="ID Departamento").grid(row=1, column=0)
    id_departamento = tk.Entry(ventana_dep)
    id_departamento.grid(row=1, column=1)

    tk.Label(ventana_dep, text="Descripción").grid(row=2, column=0)
    descripcion = tk.Entry(ventana_dep)
    descripcion.grid(row=2, column=1)

    tk.Button(ventana_dep, text="Agregar", command=crear_departamento, bg="#4CAF50", fg="white").grid(row=3, column=0, pady=10)
    tk.Button(ventana_dep, text="Modificar", command=modificar_departamento, bg="#4CAF50", fg="white").grid(row=3, column=1, pady=10)
    tk.Button(ventana_dep, text="Eliminar", command=eliminar_departamento, bg="#ca0000", fg="white").grid(row=3, column=2, pady=10)

    # Cargar los departamentos inicialmente
    mostrar_departamentos()

# Función para abrir la ventana de gestión de empleados
def ventana_empleados():
    ventana_emple = tk.Toplevel()
    ventana_emple.title("Gestión de Empleados")
    ventana_emple.geometry("1400x1000")

    # Tabla para mostrar los empleados
    tabla_empleados = ttk.Treeview(ventana_emple, columns=("ID empleado","Nombre empleado","Salario empleado","Teléfono empleado","Correo empleado","Departamento","Horario"))
    tabla_empleados.grid(row=0, column=0, columnspan=7, pady=10)
    tabla_empleados.heading("#0", text="ID empleado")
    tabla_empleados.heading("#1", text="Nombre empleado")
    tabla_empleados.heading("#2", text="Salario empleado")
    tabla_empleados.heading("#3", text="Teléfono empleado")
    tabla_empleados.heading("#4", text="Correo empleado")
    tabla_empleados.heading("#5", text="Departamento")
    tabla_empleados.heading("#6", text="Horario")
    # Función para mostrar empleados
    def mostrar_empleados():
        try:
            empleados = tabla_empleados.get_children()
            for empleado_temporal in empleados:
                tabla_empleados.delete(empleado_temporal)
            for empleado in base.Empleados.find():
                tabla_empleados.insert('', 0, text=empleado["id_empleado"], values=(empleado["nombre"]
                                       , empleado["salario"], empleado["telefono"]
                                       , empleado["correo"], empleado["id_departamento"]
                                       , empleado["id_horario"]))
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar los empleados: {e}")

    # Función para crear un empleado
    def crear_empleado():
        if len(id_empleado.get()) != 0 and len(nombre_empleado.get()) != 0 and len(salario_empleado.get()) != 0 and len(telefono_empleado.get()) != 0 and len(correo_empleado.get()) != 0:
            try:
                departamento_seleccionado = combo_departamento.get()
                horario_seleccionado = combo_horario.get()
                empleado = {
                    "id_empleado": int(id_empleado.get()),
                    "nombre": nombre_empleado.get(),
                    "salario": salario_empleado.get(),
                    "telefono": telefono_empleado.get(),
                    "correo": correo_empleado.get(),
                    "id_departamento": int(departamento_seleccionado.split(" - ")[0]),
                    "id_horario": int(horario_seleccionado.split(" - ")[0])
                }
                base.Empleados.insert_one(empleado)
                id_empleado.delete(0, tk.END)
                nombre_empleado.delete(0, tk.END)
                salario_empleado.delete(0, tk.END)
                telefono_empleado.delete(0, tk.END)
                correo_empleado.delete(0, tk.END)
                combo_departamento.set("")
                combo_horario.set("")
                mostrar_empleados()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo crear el empleado: {e}")
        else:
            messagebox.showerror("Error", "Los campos no pueden estar vacíos.")

    # Función para eliminar un empleado
    def eliminar_empleado():
        try:
            selected_item = tabla_empleados.selection()[0]
            id_emple = tabla_empleados.item(selected_item, "text")
            base.Empleados.delete_one({"id_empleado": int(id_emple)})
            mostrar_empleados()
        except IndexError:
            messagebox.showwarning("Advertencia", "Seleccione un empleado para eliminar.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar el empleado: {e}")

    # Función para modificar un empleado
    def modificar_empleado():
        try:
            selected_item = tabla_empleados.selection()[0]
            id_emple = tabla_empleados.item(selected_item, "text")
            nuevo_nombre = nombre_empleado.get()
            nuevo_salario = salario_empleado.get()
            nuevo_telefono = telefono_empleado.get()
            nuevo_correo = correo_empleado.get()
            departamento_nuevo = combo_departamento.get()
            horario_nuevo = combo_horario.get()

            if len(nuevo_nombre) == 0:
                messagebox.showerror("Error", "El nombre no puede estar vacío.")
                return
            
            if len(nuevo_salario) == 0:
                messagebox.showerror("Error", "El salario no puede estar vacío.")
                return
            
            if len(nuevo_telefono) == 0:
                messagebox.showerror("Error", "El telefono no puede estar vacío.")
                return
            
            if len(nuevo_correo) == 0:
                messagebox.showerror("Error", "El correo no puede estar vacío.")
                return

            if not departamento_nuevo:
                messagebox.showerror("Error", "El departamento no puede estar vacío.")
                return

            if not horario_nuevo:
                messagebox.showerror("Error", "El horario no puede estar vacío.")
                return
            
            base.Empleados.update_one(
                {"id_empleado": int(id_emple)},
                {"$set": {"nombre": nuevo_nombre,
                          "salario": nuevo_salario,
                          "telefono": nuevo_telefono,
                          "correo": nuevo_correo,
                          "id_departamento": int(departamento_nuevo.split(" - ")[0]),
                          "id_horario": int(horario_nuevo.split(" - ")[0])}}
            )
            nombre_empleado.delete(0, tk.END)
            nombre_empleado.delete(0, tk.END)
            salario_empleado.delete(0, tk.END)
            telefono_empleado.delete(0, tk.END)
            correo_empleado.delete(0, tk.END)
            combo_departamento.set("")
            combo_horario.set("")
            mostrar_empleados()
        except IndexError:
            messagebox.showwarning("Advertencia", "Selecciona un empleado para modificar")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo modificar el empleado: {e}")

   # Campos de entrada y botones para empleado
    tk.Label(ventana_emple, text="ID empleado").grid(row=1, column=0)
    id_empleado = tk.Entry(ventana_emple)
    id_empleado.grid(row=1, column=1)

    tk.Label(ventana_emple, text="Nombre empleado").grid(row=2, column=0)
    nombre_empleado = tk.Entry(ventana_emple)
    nombre_empleado.grid(row=2, column=1)

    tk.Label(ventana_emple, text="Salario empleado").grid(row=3, column=0)
    salario_empleado = tk.Entry(ventana_emple)
    salario_empleado.grid(row=3, column=1)

    tk.Label(ventana_emple, text="Telefono empleado").grid(row=4, column=0)
    telefono_empleado = tk.Entry(ventana_emple)
    telefono_empleado.grid(row=4, column=1)
    
    tk.Label(ventana_emple, text="Correo empleado").grid(row=5, column=0)
    correo_empleado = tk.Entry(ventana_emple)
    correo_empleado.grid(row=5, column=1)
    
    # Obtener departamentos
    departamentos = [{"id_departamento": departamento["id_departamento"], "Descripcion": departamento["Descripcion"]} for departamento in
                 base.Departamentos.find({}, {"_id": 0, "id_departamento": 1, "Descripcion": 1})]
    departamentos_combo = [f'{departamento["id_departamento"]} - {departamento["Descripcion"]}' for departamento in departamentos]

    tk.Label(ventana_emple, text="ID departamento:").grid(row=6, column=0)
    combo_departamento = ttk.Combobox(ventana_emple, values=departamentos_combo, state="readonly")
    combo_departamento.grid(row=6, column=1)
    
    # Obtener horarios
    horarios = [{"id_horario": horario["id_horario"], "Turno": horario["Turno"]} for horario in
                 base.Horarios.find({}, {"_id": 0, "id_horario": 1, "Turno": 1})]
    horarios_combo = [f'{horario["id_horario"]} - {horario["Turno"]}' for horario in horarios]

    tk.Label(ventana_emple, text="ID horario:").grid(row=7, column=0)
    combo_horario = ttk.Combobox(ventana_emple, values=horarios_combo, state="readonly")
    combo_horario.grid(row=7, column=1)

    tk.Button(ventana_emple, text="Agregar", command=crear_empleado, bg="#4CAF50", fg="white").grid(row=8, column=0, pady=10)
    tk.Button(ventana_emple, text="Modificar", command=modificar_empleado, bg="#4CAF50", fg="white").grid(row=8, column=1, pady=10)
    tk.Button(ventana_emple, text="Eliminar", command=eliminar_empleado, bg="#ca0000", fg="white").grid(row=8, column=2, pady=10)

    # Cargar los empleados inicialmente
    mostrar_empleados()

# Función para abrir la ventana de gestión de habitaciones
def ventana_habitaciones():
    ventana_dep = tk.Toplevel()
    ventana_dep.title("Gestión de Habitaciones")
    ventana_dep.geometry("1100x450")

    # Tabla para mostrar habitaciones
    tabla_habitaciones = ttk.Treeview(ventana_dep, columns=("IdHabitacion", "Habitacion", "Descripción", "Precio", "Estado","id_Hotel"), show="headings")
    tabla_habitaciones.grid(row=0, column=0, columnspan=6, pady=10)
    tabla_habitaciones.heading("#0", text="IdHabitacion")
    tabla_habitaciones.heading("#1", text="Habitacion")
    tabla_habitaciones.heading("#2", text="Descripción")
    tabla_habitaciones.heading("#3", text="Precio")
    tabla_habitaciones.heading("#4", text="Estado")
    tabla_habitaciones.heading("#5", text="id_Hotel")
    tabla_habitaciones.heading("#6", text="id_habitacion")

    # Función para mostrar habitaciones
    def mostrar_habitaciones():
        try:
            registros = tabla_habitaciones.get_children()
            for registro in registros:
                tabla_habitaciones.delete(registro)
            for documento in base.Habitaciones.find():
                tabla_habitaciones.insert('', 0, text=documento["id_habitacion"],
                                          values=(
                                              documento["numero"],
                                              documento["Descripcion"],
                                              documento["precio"],
                                              documento["estado"],
                                              documento["id_hotel"],
                                              documento["id_habitacion"]
                                          ))
        except Exception as e:
            messagebox.showerror("Error", f"No se pueden cargar las habitaciones: {e}")

    # Función para crear habitacion
    def crear_habitacion():

        if len(id_habitacion.get()) != 0 and len(numero.get()) != 0 and len(descripcion.get()) != 0 and len(precio.get()) != 0 and len(estado.get()) != 0 and combo_hotel.get() != "":
            try:
                hotel_seleccionado = combo_hotel.get()
                id_hotel = hotel_seleccionado.split(" - ")[0]
                documento = {
                    "id_habitacion": int(id_habitacion.get()),
                    "numero": int(numero.get()),
                    "Descripcion": descripcion.get(),
                    "precio": int(precio.get()),
                    "estado": (estado.get()),
                    "id_hotel": int(id_hotel)
                }
                print(documento)

                base.Habitaciones.insert_one(documento)
                id_habitacion.delete(0, tk.END)
                numero.delete(0, tk.END)
                descripcion.delete(0, tk.END)
                precio.delete(0, tk.END)
                estado.delete(0, tk.END)

                mostrar_habitaciones()

            except Exception as e:
                messagebox.showerror("Error", f"No se pudo crear la habitacion: {e}")
        else:
            messagebox.showerror("Error", "Los campos no pueden estar vacíos")

    # Función para eliminar habitacion
    def eliminar_habitacion():
        try:
            selected_item = tabla_habitaciones.selection()[0]
            id_dep = tabla_habitaciones.item(selected_item, "text")
            base.Habitaciones.delete_one({"id_habitacion": int(id_dep)})
            mostrar_habitaciones()
        except IndexError:
            messagebox.showwarning("Advertencia", "Selecciona una habitacion para eliminar")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar la habitacion: {e}")

            # Función para modificar habitacion
    def modificar_habitacion():
        try:
            selected_item = tabla_habitaciones.selection()[0]
            id_dep = tabla_habitaciones.item(selected_item, "text")

            nuevo_numero = numero.get()
            nueva_descripcion = descripcion.get()
            nuevo_precio = precio.get()
            nuevo_estado = estado.get()


            if not nuevo_numero or not nueva_descripcion or not nuevo_precio or not nuevo_estado:
                messagebox.showerror("Error", "La descripción no puede estar vacía")
                return

            base.Habitaciones.update_one(
                {"id_habitacion": int(id_dep)},
                {"$set": {
                    "numero": int(nuevo_numero),
                    "Descripcion": nueva_descripcion,
                    "precio": int(nuevo_precio),
                    "estado": nuevo_estado
                }}
            )
            numero.delete(0, tk.END)
            descripcion.delete(0, tk.END)
            precio.delete(0, tk.END)
            estado.delete(0, tk.END)

            mostrar_habitaciones()

        except IndexError:
            messagebox.showwarning("Advertencia", "Selecciona una habitacion para modificar")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo modificar la habitacion: {e}")

    # Campos de entrada y botones para departamento
    tk.Label(ventana_dep, text="id_habitacion").grid(row=1, column=0)
    id_habitacion = tk.Entry(ventana_dep)
    id_habitacion.grid(row=1, column=1)

    tk.Label(ventana_dep, text="Numero de Habitacion").grid(row=2, column=0)
    numero = tk.Entry(ventana_dep)
    numero.grid(row=2, column=1)

    tk.Label(ventana_dep, text="Descripción").grid(row=3, column=0)
    descripcion = tk.Entry(ventana_dep)
    descripcion.grid(row=3, column=1)

    tk.Label(ventana_dep, text="Precio").grid(row=4, column=0)
    precio = tk.Entry(ventana_dep)
    precio.grid(row=4, column=1)

    tk.Label(ventana_dep, text="Estado").grid(row=5, column=0)
    estado = tk.Entry(ventana_dep)
    estado.grid(row=5, column=1)

    # Obtener los id_hotel+ nombre  hoteles
    hoteles = [{"id_hotel": hoteles["id_hotel"], "descripcion": hoteles["descripcion"]} for hoteles in
                    base.Hoteles.find({}, {"_id": 0, "id_hotel": 1, "descripcion": 1})]

    # Formatear los valores para mostrar en el Combobox
    hoteles_combo = [f'{hoteles["id_hotel"]} - {hoteles["descripcion"]}' for hoteles in hoteles]

    # Crear el Combobox
    tk.Label(ventana_dep, text="Id Hotel").grid(row=4, column=2)
    combo_hotel = ttk.Combobox(ventana_dep, values=hoteles_combo, state="readonly")
    combo_hotel.grid(row=4, column=3)

    # Función para obtener el id_cliente seleccionado
    def seleccionar_hotel(event):
        seleccionado = combo_hotel.get()
        print(f"Seleccionado: {seleccionado}")
        id_hotel = seleccionado.split(" - ")[0]

    combo_hotel.bind("<<ComboboxSelected>>", seleccionar_hotel)

    tk.Button(ventana_dep, text="Agregar", command=crear_habitacion, bg="#4CAF50", fg="white").grid(row=6,
                                                                                                              column=0,
                                                                                                              pady=10)
    tk.Button(ventana_dep, text="Modificar", command=modificar_habitacion, bg="#4CAF50", fg="white").grid(
        row=6, column=1, pady=10)

    tk.Button(ventana_dep, text="Eliminar", command=eliminar_habitacion, bg="#ca0000", fg="white").grid(row=6,
                                                                                                            column=2,
                                                                                                            pady=10)

    # Cargar las habitaciones inicialmente
    mostrar_habitaciones()

# Función para abrir la ventana de gestión de sedes
def ventana_hoteles():
    ventana_dep = tk.Toplevel()
    ventana_dep.title("Gestión de Sedes")
    ventana_dep.geometry("1000x600")

    frame = tk.Frame(ventana_dep, padx=20, pady=20)
    frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

    # Tabla para mostrar sedes disponibles
    tabla_hoteles = ttk.Treeview(ventana_dep,
                                 columns=("IdHotel", "Descripción", "Ubicación", "Servicios"),
                                 show="headings")
    tabla_hoteles.grid(row=0, column=0, columnspan=2, pady=10)

    tabla_hoteles.heading("IdHotel", text="IdHotel")
    tabla_hoteles.heading("Descripción", text="Descripción")
    tabla_hoteles.heading("Ubicación", text="Ubicación")
    tabla_hoteles.heading("Servicios", text="Servicios")

    tk.Label(frame, text="Id Hotel:").grid(row=1, column=0, sticky="w", pady=5)
    id_hotel = tk.Entry(frame, width=30)
    id_hotel.grid(row=1, column=1, columnspan=2, pady=5)

    tk.Label(frame, text="Descripción:").grid(row=2, column=0, sticky="w", pady=5)
    descripcion = tk.Entry(frame, width=30)
    descripcion.grid(row=2, column=1, columnspan=2, pady=5)

    tk.Label(frame, text="Ubicación:").grid(row=3, column=0, sticky="w", pady=5)
    ubicación = tk.Entry(frame, width=30)
    ubicación.grid(row=3, column=1, columnspan=2, pady=5)

    # Lista de servicios
    servicios = [{"id_servicio": s["id_servicio"], "Descripcion": s["Descripcion"]} for s in base.Servicios.find({}, {"_id": 0})]
    servicios_combo = [f'{s["id_servicio"]} - {s["Descripcion"]}' for s in servicios]

    tk.Label(frame, text="Servicios:").grid(row=4, column=0, sticky="w", pady=5)
    combo_servicios = ttk.Combobox(frame, values=servicios_combo, state="readonly", width=28)
    combo_servicios.grid(row=4, column=1, columnspan=2, pady=5)

    # Función para mostrar sedes
    def mostrar_hoteles():
        registros = tabla_hoteles.get_children()
        for r in registros:
            tabla_hoteles.delete(r)

        for doc in base.Hoteles.find():
            servicios = ", ".join(map(str, doc.get("servicios", [])))
            tabla_hoteles.insert('', 'end',
                                 values=(
                                     doc.get("id_hotel", ""),
                                     doc.get("descripcion", ""),
                                     doc.get("ubicación", ""),
                                     servicios
                                 )
                                 )
    # Función para crear sede
    def crear_hotel():
        if id_hotel.get() and descripcion.get() and ubicación.get() and combo_servicios.get():
            try:
                servicio = combo_servicios.get().split(" - ")[0]
                documento = {
                    "id_hotel": int(id_hotel.get()),
                    "descripcion": descripcion.get(),
                    "ubicación": ubicación.get(),
                    "servicios": [int(servicio)]
                }

                base.Hoteles.insert_one(documento)

                id_hotel.delete(0, tk.END)
                descripcion.delete(0, tk.END)
                ubicación.delete(0, tk.END)
                combo_servicios.set("")

                mostrar_hoteles()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo crear el hotel: {e}")
        else:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")

    tk.Button(frame, text="Agregar", command=crear_hotel,
              bg="#4CAF50", fg="white", font=("Arial", 12, "bold"), padx=10, pady=5).grid(
        row=6, column=0, columnspan=3, pady=10, sticky="ew")

    # Función para eliminar sede
    def eliminar_hotel():
        if id_hotel.get():
            try:
                resultado = base.Hoteles.delete_one({"id_hotel": int(id_hotel.get())})

                if resultado.deleted_count > 0:
                    messagebox.showinfo("Éxito", "Hotel eliminado correctamente.")
                    mostrar_hoteles()
                else:
                    messagebox.showwarning("No encontrado", "No se encontró un hotel con ese ID.")

                # Limpiar campos
                id_hotel.delete(0, tk.END)
                descripcion.delete(0, tk.END)
                ubicación.delete(0, tk.END)
                combo_servicios.set("")

            except Exception as e:
                messagebox.showerror("Error", f"No se pudo eliminar el hotel: {e}")
        else:
            messagebox.showerror("Error", "Debes ingresar un ID de hotel para eliminar.")

    tk.Button(frame, text="Eliminar", command=eliminar_hotel,
              bg="#ca0000", fg="white", font=("Arial", 12, "bold"), padx=10, pady=5).grid(
        row=8, column=0, columnspan=3, pady=5, sticky="ew")

    # Función para modificar sede
    def modificar_hotel():
        if id_hotel.get() and descripcion.get() and ubicación.get() and combo_servicios.get():
            try:
                servicio = combo_servicios.get().split(" - ")[0]
                nuevo_documento = {
                    "descripcion": descripcion.get(),
                    "ubicación": ubicación.get(),
                    "servicios": [int(servicio)]
                }

                resultado = base.Hoteles.update_one(
                    {"id_hotel": int(id_hotel.get())},
                    {"$set": nuevo_documento}
                )

                if resultado.modified_count > 0:
                    messagebox.showinfo("Éxito", "Hotel modificado correctamente.")
                    mostrar_hoteles()
                else:
                    messagebox.showwarning("Sin cambios", "No se encontró el hotel o los datos no cambiaron.")

                # Limpiar campos
                id_hotel.delete(0, tk.END)
                descripcion.delete(0, tk.END)
                ubicación.delete(0, tk.END)
                combo_servicios.set("")

            except Exception as e:
                messagebox.showerror("Error", f"No se pudo modificar el hotel: {e}")
        else:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")

    tk.Button(frame, text="Modificar", command=modificar_hotel,
              bg="#4CAF50", fg="white", font=("Arial", 12, "bold"), padx=10, pady=5).grid(
        row=7, column=0, columnspan=3, pady=5, sticky="ew")

    # Cargar las sedes inicialmente
    mostrar_hoteles()

# Función para abrir la ventana de gestión de servicios
def ventana_servicios():
        ventana_ser = tk.Toplevel()
        ventana_ser.title("Gestión de Servicios")
        ventana_ser.geometry("800x600")

        # Tabla para mostrar los servicios
        tabla_ser = ttk.Treeview(ventana_ser, columns=2)
        tabla_ser.grid(row=0, column=0, columnspan=2, pady=10)
        tabla_ser.heading("#0", text="ID Servicio")
        tabla_ser.heading("#1", text="Descripción")

        # Función para mostrar servicios
        def mostrar_servicios():
            try:
                registros = tabla_ser.get_children()
                for registro in registros:
                    tabla_ser.delete(registro)
                for documento in base.Servicios.find():
                    tabla_ser.insert('', 0, text=documento["id_servicio"],
                                               values=documento["Descripcion"])
            except Exception as e:
                messagebox.showerror("Error", f"No se pudieron cargar los servicios: {e}")

        # Función para crear un servicios
        def crear_servicio():
            if len(id_servicio.get()) != 0 and len(descripcion.get()) != 0:
                try:
                    documento = {
                        "id_servicio": int(id_servicio.get()),
                        "Descripcion": descripcion.get()
                    }
                    base.Servicios.insert_one(documento)
                    id_servicio.delete(0, tk.END)
                    descripcion.delete(0, tk.END)
                    mostrar_servicios()
                except Exception as e:
                    messagebox.showerror("Error", f"No se pudo crear el servicio: {e}")
            else:
                messagebox.showerror("Error", "Los campos no pueden estar vacíos")

        # Función para eliminar un servicio
        def eliminar_servicio():
            try:
                selected_item = tabla_ser.selection()[0]
                id_ser = tabla_ser.item(selected_item, "text")
                base.Servicios.delete_one({"id_servicio": int(id_ser)})
                mostrar_servicios()
            except IndexError:
                messagebox.showwarning("Advertencia", "Selecciona un servicio para eliminar")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo eliminar el servicio: {e}")

        # Función para modificar un departamento
        def modificar_servicio():
            try:
                selected_item = tabla_ser.selection()[0]
                id_ser = tabla_ser.item(selected_item, "text")
                nueva_descripcion = descripcion.get()

                if len(nueva_descripcion) == 0:
                    messagebox.showerror("Error", "La descripción no puede estar vacía")
                    return

                base.Servicios.update_one(
                    {"id_servicio": int(id_ser)},
                    {"$set": {"Descripcion": nueva_descripcion}}
                )
                descripcion.delete(0, tk.END)
                mostrar_servicios()
            except IndexError:
                messagebox.showwarning("Advertencia", "Selecciona un servicio para modificar")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo modificar el servicio: {e}")

        # Campos de entrada y botones para servicios
        tk.Label(ventana_ser, text="ID Servicio").grid(row=1, column=0)
        id_servicio = tk.Entry(ventana_ser)
        id_servicio.grid(row=1, column=1)

        tk.Label(ventana_ser, text="Descripción").grid(row=2, column=0)
        descripcion = tk.Entry(ventana_ser)
        descripcion.grid(row=2, column=1)

        tk.Button(ventana_ser, text="Agregar", command=crear_servicio, bg="#4CAF50", fg="white").grid(row=3,
                                                                                                            column=0,
                                                                                                            pady=10)
        tk.Button(ventana_ser, text="Modificar", command=modificar_servicio, bg="#4CAF50", fg="white").grid(
            row=3, column=1, pady=10)
        tk.Button(ventana_ser, text="Eliminar", command=eliminar_servicio, bg="#ca0000", fg="white").grid(row=3,
                                                                                                          column=2,
                                                                                                          pady=10)

        # Cargar los departamentos inicialmente
        mostrar_servicios()

# Función para abrir la ventana de gestión de facturas
def ventana_facturas():
        ventana_fac = tk.Toplevel()
        ventana_fac.title("Gestión de facturas")
        ventana_fac.geometry("1600x800")

        # Tabla para mostrar las facturas
        tabla_fac = ttk.Treeview(ventana_fac, columns=("Metodo", "id_cliente", "id_habitacion", "total", "fecha"))
        tabla_fac.grid(row=0, column=0, columnspan=6, pady=10)

        tabla_fac.heading("#0", text="ID Factura")
        tabla_fac.heading("Metodo", text="Metodo")
        tabla_fac.heading("id_cliente", text="id_cliente")
        tabla_fac.heading("id_habitacion", text="id_habitacion")
        tabla_fac.heading("total", text="total")
        tabla_fac.heading("fecha", text="fecha")

        # Función para mostrar facturas
        def mostrar_facturas():
            try:
                registros = tabla_fac.get_children()
                for registro in registros:
                    tabla_fac.delete(registro)
                for documento in base.Facturas.find():
                    tabla_fac.insert('', 0, text=documento["id_factura"],values=(documento["metodo"], documento["id_cliente"], documento["id_habitacion"], documento["total"], documento["fecha"]))
            except Exception as e:
                messagebox.showerror("Error", f"No se pudieron cargar las facturas: {e}")

        # Función para crear una factura
            def crear_factura():
                if len(id_factura.get()) != 0 and metodo.get() in ["Tarjeta","Efectivo"] and combo_clientes.get() != "":
                    try:
                       
                        cliente_seleccionado = combo_clientes.get()
                        habitacion_seleccionado = combo_habitaciones.get()
                        precio_seleccionado = combo_habitaciones.get()
                        id_cliente = cliente_seleccionado.split(" - ")[0]  
                        id_habitacion= habitacion_seleccionado.split(" - ")[0]
                        precio =  precio_seleccionado.split(" - ")[2]
                        fecha_actual = datetime.now()

                        # Crear el diccionario para insertar en la base de datos
                        documento = {
                            "id_factura": int(id_factura.get()),
                            "metodo": metodo.get(),
                            "id_cliente": int(id_cliente),
                            "id_habitacion": int(id_habitacion),
                            "total": int(precio),
                            "fecha": fecha_actual
                        }
                        # Insertar en la colección Facturas
                        base.Facturas.insert_one(documento)

                        # Limpiar los campos
                        id_factura.delete(0, tk.END)
                        metodo.set("Seleccionar")
                        combo_clientes.set("")
                        combo_habitaciones.set("")

                        # Mostrar las facturas actualizadas
                        mostrar_facturas()
                    except Exception as e:
                        messagebox.showerror("Error", f"No se pudo crear la factura: {e}")
                else:
                    messagebox.showerror("Error",
                                         "Los campos no pueden estar vacíos o no se ha seleccionado un cliente/método/habitacion válido")

            # Campos de entrada y botones para facturas
            tk.Label(ventana_fac, text="ID Factura").grid(row=1, column=0)
            id_factura = tk.Entry(ventana_fac)
            id_factura.grid(row=1, column=1)

            tk.Label(ventana_fac, text="Método de pago").grid(row=2, column=0)
            metodo = ttk.Combobox(ventana_fac, values=["Tarjeta", "Efectivo"])
            metodo.grid(row=2, column=1)
            metodo.set("Seleccionar")

            # Obtener los id_cliente y nombre de la colección Clientes
            clientes = [{"id_cliente": cliente["id_cliente"], "nombre": cliente["nombre"]} for cliente in
                        base.Clientes.find({}, {"_id": 0, "id_cliente": 1, "nombre": 1})]

            # Formatear los valores para mostrar en el Combobox
            clientes_combo = [f'{cliente["id_cliente"]} - {cliente["nombre"]}' for cliente in clientes]

            # Crear el Combobox
            tk.Label(ventana_fac, text="id Cliente").grid(row=3, column=0)
            combo_clientes = ttk.Combobox(ventana_fac, values=clientes_combo, state="readonly")
            combo_clientes.grid(row=3, column=1)

            # Función para obtener el id_cliente seleccionado
            def seleccionar_cliente(event):
                seleccionado = combo_clientes.get()
                id_cliente = seleccionado.split(" - ")[0]


            combo_clientes.bind("<<ComboboxSelected>>", seleccionar_cliente)

            # Obtener los id_habitacion y descripcion de la colección habitacion
            habitaciones = [{"id_habitacion": habitacion["id_habitacion"], "Descripcion": habitacion["Descripcion"],"precio":habitacion["precio"]} for habitacion in
                        base.Habitaciones.find({}, {"_id": 0, "id_habitacion": 1, "Descripcion": 1,"precio":1})]

            # Formatear los valores para mostrar en el Combobox
            habitaciones_combo = [f'{habitacion["id_habitacion"]} - {habitacion["Descripcion"]} - {habitacion["precio"]}' for habitacion in habitaciones]

            # Crear el Combobox
            tk.Label(ventana_fac, text="ID Habitacion / Precio").grid(row=4, column=0)
            combo_habitaciones = ttk.Combobox(ventana_fac, values=habitaciones_combo, state="readonly")
            combo_habitaciones.grid(row=4, column=1)

            # Función para obtener el id_cliente seleccionado
            def seleccionar_habitacion(event):
                seleccionado = combo_habitaciones.get()

                id_habitacion = seleccionado.split(" - ")[0]
                precio = seleccionado.split(" - ")[2]
                print(precio)




            combo_habitaciones.bind("<<ComboboxSelected>>", seleccionar_habitacion)

            tk.Button(ventana_fac, text="Agregar", command=crear_factura, bg="#4CAF50", fg="white").grid(row=5, column=1)

        # Cargar las facturas inicialmente
        mostrar_facturas()


# Función para abrir la ventana de gestión de mantenimientos

def ventana_mantenimientos():
    ventana_mant = tk.Toplevel()
    ventana_mant.title("Gestión de Mantenimientos")
    ventana_mant.geometry("900x600") 

    # Contenedor principal con padding
    frame = tk.Frame(ventana_mant, padx=20, pady=20)
    frame.pack(expand=True)

    # Tabla de Mantenimientos con estilo
    estilo = ttk.Style()
    estilo.configure("Treeview", rowheight=25, font=("Arial", 10))
    estilo.configure("Treeview.Heading", font=("Arial", 11, "bold"), background="lightblue")

    tabla_mant = ttk.Treeview(frame, columns=("Descripcion", "id_empleado", "id_habitacion", "fecha"), show="headings")
    tabla_mant.grid(row=0, column=0, columnspan=3, pady=10, sticky="ew")

    # Encabezados
    tabla_mant.heading("Descripcion", text="Descripción")
    tabla_mant.heading("id_empleado", text="ID Empleado")
    tabla_mant.heading("id_habitacion", text="ID Habitación")
    tabla_mant.heading("fecha", text="Fecha")

    for col in ("Descripcion", "id_empleado", "id_habitacion", "fecha"):
        tabla_mant.column(col, width=150, anchor="center")

    # Función que muestra los mantenimientos
    def mostrar_mantenimientos():
        try:
            registros = tabla_mant.get_children()
            for registro in registros:
                tabla_mant.delete(registro)
                
            empleados_dict = {str(empleado["id_empleado"]): empleado["nombre"] for empleado in base.Empleados.find({}, {"_id": 0, "id_empleado": 1, "nombre": 1})}

            for documento in base.Mantenimientos.find():
                id_empleado = str(documento["id_empleado"])
                nombre_empleado = empleados_dict.get(id_empleado, "NA") 

                tabla_mant.insert("", "end", text=documento["id_mantenimiento"], values=(
                    documento["Descripcion"], 
                    f"{id_empleado} - {nombre_empleado}",  
                    documento["id_habitacion"], 
                    documento["fecha"]
                ))
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar los mantenimientos: {e}")

    # Campos de entrada Id Mantenimiento/Descripcion
    tk.Label(frame, text="ID Mantenimiento:").grid(row=1, column=0, sticky="w", pady=5)
    id_mantenimiento = tk.Entry(frame, width=30)
    id_mantenimiento.grid(row=1, column=1, columnspan=2, pady=5)

    tk.Label(frame, text="Descripción:").grid(row=2, column=0, sticky="w", pady=5)
    Descripcion = ttk.Combobox(frame, values=[
        "Reparacion de electrodomesticos", "Reparacion de sistemas", "Fugas","Reparación de conexion", "Revision de cerraduras", "Revision de moviliario" ], state="readonly", width=28)
    Descripcion.grid(row=2, column=1, columnspan=2, pady=5)
    Descripcion.set("Seleccionar")

    # Obtener empleados
    empleados = [{"id_empleado": empleado["id_empleado"], "nombre": empleado["nombre"]} for empleado in
                 base.Empleados.find({}, {"_id": 0, "id_empleado": 1, "nombre": 1})]
    empleados_combo = [f'{empleado["id_empleado"]} - {empleado["nombre"]}' for empleado in empleados]

    tk.Label(frame, text="ID Empleado:").grid(row=3, column=0, sticky="w", pady=5)
    combo_empleados = ttk.Combobox(frame, values=empleados_combo, state="readonly", width=28)
    combo_empleados.grid(row=3, column=1, columnspan=2, pady=5)

    # Obtener habitaciones
    habitaciones = [{"id_habitacion": habitacion["id_habitacion"], "Descripcion": habitacion["Descripcion"]} for habitacion in
                    base.Habitaciones.find({}, {"_id": 0, "id_habitacion": 1, "Descripcion": 1})]
    habitaciones_combo = [f'{habitacion["id_habitacion"]} - {habitacion["Descripcion"]}' for habitacion in habitaciones]

    tk.Label(frame, text="ID Habitación:").grid(row=4, column=0, sticky="w", pady=5)
    combo_habitaciones = ttk.Combobox(frame, values=habitaciones_combo, state="readonly", width=28)
    combo_habitaciones.grid(row=4, column=1, columnspan=2, pady=5)

    # Función para crear mantenimiento
    def crear_mantenimiento():
        if id_mantenimiento.get() and Descripcion.get() != "Seleccionar" and combo_empleados.get() and combo_habitaciones.get():
            try:
                empleado_seleccionado = combo_empleados.get()
                habitacion_seleccionada = combo_habitaciones.get()

                if " - " in empleado_seleccionado and " - " in habitacion_seleccionada:
                    id_empleado = empleado_seleccionado.split(" - ")[0]
                    id_habitacion = habitacion_seleccionada.split(" - ")[0]
                else:
                    messagebox.showerror("Error", "Selección inválida.")
                    return

                fecha_actual = datetime.now()

                documento = {
                    "id_mantenimiento": int(id_mantenimiento.get()),
                    "Descripcion": Descripcion.get(),
                    "id_empleado": int(id_empleado),
                    "id_habitacion": int(id_habitacion),
                    "fecha": fecha_actual
                }

                base.Mantenimientos.insert_one(documento)

                id_mantenimiento.delete(0, tk.END)
                Descripcion.set("Seleccionar")
                combo_empleados.set("")
                combo_habitaciones.set("")

                mostrar_mantenimientos()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo crear el mantenimiento: {e}")
        else:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")

     # Función para eliminar un mantenimiento
    def eliminar_mantenimiento():
        try:
            selected_item = tabla_mant.selection()[0]  
            id_mantenimiento = tabla_mant.item(selected_item, "text") 

            if not id_mantenimiento:
                messagebox.showwarning("Advertencia", "No se pudo obtener el ID del mantenimiento.")
                return

            base.Mantenimientos.delete_one({"id_mantenimiento": int(id_mantenimiento)})
            mostrar_mantenimientos()
        except IndexError:
            messagebox.showwarning("Advertencia", "Selecciona un mantenimiento para eliminar.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar el mantenimiento: {e}")

                
    # Botón de Crear/Eliminar con estilo
    boton_crear = tk.Button(frame, text="Agregar", command=crear_mantenimiento,
        bg="#4CAF50", fg="white", font=("Arial", 12, "bold"), padx=10, pady=5)
    boton_crear.grid(row=5, column=0, columnspan=3, pady=10, sticky="ew")
    
    boton_eliminar = tk.Button(frame, text="Eliminar", command=eliminar_mantenimiento,
        bg="#ca0000", fg="white", font=("Arial", 12, "bold"), padx=10, pady=5)
    boton_eliminar.grid(row=6, column=0, columnspan=3, pady=10, sticky="ew")
    
    
    mostrar_mantenimientos()


# Función para abrir la ventana de gestión de registros

def ventana_registros():
    ventana_reg = tk.Toplevel()
    ventana_reg.title("Gestión de Registros")
    ventana_reg.geometry("900x600")

    # Contenedor principal con padding
    frame = tk.Frame(ventana_reg, padx=20, pady=20)
    frame.pack(expand=True)

    # Tabla de Registros con estilo
    estilo = ttk.Style()
    estilo.configure("Treeview", rowheight=25, font=("Arial", 10))
    estilo.configure("Treeview.Heading", font=("Arial", 11, "bold"), background="lightblue")

    tabla_reg = ttk.Treeview(frame, columns=("accion", "id_cliente", "fecha"))
    tabla_reg.grid(row=0, column=0, columnspan=3, pady=10, sticky="ew")

    tabla_reg.heading("#0", text="ID Registro")
    tabla_reg.heading("accion", text="Registro Cliente")
    tabla_reg.heading("id_cliente", text="ID Cliente")
    tabla_reg.heading("fecha", text="Fecha")

    for col in ("accion", "id_cliente", "fecha"):
        tabla_reg.column(col, width=150, anchor="center")

    # Función que muestra los registros
    def mostrar_registros():
        try:
            registros = tabla_reg.get_children()
            for registro in registros:
                tabla_reg.delete(registro)
                
            clientes_dict = {str(cliente["id_cliente"]): cliente["nombre"] for cliente in base.Clientes.find({}, {"_id": 0, "id_cliente": 1, "nombre": 1})}

            for documento in base.Registros.find():
                id_cliente = str(documento["id_cliente"])
                nombre_cliente = clientes_dict.get(id_cliente, "NA") 

                tabla_reg.insert("", 0, text=documento["id_registro"], values=(
                    documento["accion"], 
                    f"{id_cliente} - {nombre_cliente}",  
                    documento["fecha"]
                ))
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar los registros: {e}")

    # Campos de entrada Id Registro/accion
    
    tk.Label(frame, text="ID Registro:").grid(row=1, column=0, sticky="w", pady=5)
    id_registro = tk.Entry(frame, width=30)
    id_registro.grid(row=1, column=1, columnspan=2, pady=5)

    tk.Label(frame, text="Registro de Cliente:").grid(row=2, column=0, sticky="w", pady=5)
    accion = ttk.Combobox(frame, values=["Entrada", "Salida" ], state="readonly", width=28)
    accion.grid(row=2, column=1, columnspan=2, pady=5)
    accion.set("Seleccionar")

    # Obtener clientes
    clientes = [{"id_cliente": cliente["id_cliente"], "nombre": cliente["nombre"]} for cliente in
                 base.Clientes.find({}, {"_id": 0, "id_cliente": 1, "nombre": 1})]
    clientes_combo = [f'{cliente["id_cliente"]} - {cliente["nombre"]}' for cliente in clientes]

    tk.Label(frame, text="ID Cliente:").grid(row=3, column=0, sticky="w", pady=5)
    combo_clientes = ttk.Combobox(frame, values=clientes_combo, state="readonly", width=28)
    combo_clientes.grid(row=3, column=1, columnspan=2, pady=5)

    # Función para crear registro
    def crear_registro():
        if id_registro.get() and accion.get() != "Seleccionar" and combo_clientes.get():
            try:
                cliente_seleccionado = combo_clientes.get()

                if " - " in cliente_seleccionado:
                    id_cliente = cliente_seleccionado.split(" - ")[0]
                else:
                    messagebox.showerror("Error", "Selección inválida.")
                    return

                fecha_actual = datetime.now()

                documento = {
                    "id_registro": int(id_registro.get()),
                    "accion": accion.get(),
                    "id_cliente": int(id_cliente),
                    "fecha": fecha_actual
                }

                base.Registros.insert_one(documento)

                id_registro.delete(0, tk.END)
                accion.set("Seleccionar")
                combo_clientes.set("")

                mostrar_registros()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo crear el registro: {e}")
        else:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")

     # Función para eliminar un registro
    def eliminar_registro():
        try:
            selected_item = tabla_reg.selection()[0]  
            id_registro = tabla_reg.item(selected_item, "text") 

            if not id_registro:
                messagebox.showwarning("Advertencia", "No se pudo obtener el ID del registro.")
                return

            base.Registros.delete_one({"id_registro": int(id_registro)})
            mostrar_registros()
        except IndexError:
            messagebox.showwarning("Advertencia", "Selecciona un registro para eliminar.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar el registro: {e}")

                
    # Botón de Crear/Eliminar con estilo
    boton_crear = tk.Button(frame, text="Agregar", command=crear_registro,
        bg="#4CAF50", fg="white", font=("Arial", 12, "bold"), padx=10, pady=5)
    boton_crear.grid(row=5, column=0, columnspan=3, pady=10, sticky="ew")
    
    boton_eliminar = tk.Button(frame, text="Eliminar", command=eliminar_registro,
        bg="#ca0000", fg="white", font=("Arial", 12, "bold"), padx=10, pady=5)
    boton_eliminar.grid(row=6, column=0, columnspan=3, pady=10, sticky="ew")
    

    mostrar_registros()

# Funcion para la ventana y gestionar eventos
def gestionar_eventos():
    ventana_eventos = tk.Toplevel()
    ventana_eventos.title("Gestión de Eventos")
    ventana_eventos.geometry("850x450")

    # Tabla para eventos
    tabla_eventos = ttk.Treeview(ventana_eventos, columns=("nombre", "fecha", "lugar", "descripcion"), show="headings")
    tabla_eventos.heading("nombre", text="Nombre")
    tabla_eventos.heading("fecha", text="Fecha")
    tabla_eventos.heading("lugar", text="Lugar")
    tabla_eventos.heading("descripcion", text="Descripción")
    tabla_eventos.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

    def actualizar_tabla():
        tabla_eventos.delete(*tabla_eventos.get_children())
        for evento in base.Eventos.find({}, {"_id": 0}):
            tabla_eventos.insert("", tk.END, values=(evento["nombre"], evento["fecha"], evento["lugar"], evento["descripcion"]))

    def agregar_evento():
        popup = tk.Toplevel()
        popup.title("Nuevo Evento")
        popup.geometry("350x300")
        popup.grab_set()

        tk.Label(popup, text="Nombre del evento:").pack()
        entry_nombre = tk.Entry(popup)
        entry_nombre.pack()

        tk.Label(popup, text="Fecha del evento (dd/mm/yyyy):").pack()
        entry_fecha = tk.Entry(popup)
        entry_fecha.pack()

        tk.Label(popup, text="Lugar del evento:").pack()
        entry_lugar = tk.Entry(popup)
        entry_lugar.pack()

        tk.Label(popup, text="Descripción del evento:").pack()
        entry_descripcion = tk.Entry(popup)
        entry_descripcion.pack()

        def guardar_evento():
            try:
                nombre = entry_nombre.get()
                fecha = entry_fecha.get()
                lugar = entry_lugar.get()
                descripcion = entry_descripcion.get()

                if not all([nombre, fecha, lugar, descripcion]):
                    raise ValueError("Todos los campos son requeridos.")

                # Validar formato de fecha
                fecha_dt = datetime.strptime(fecha, "%d/%m/%Y")

                # Comprobar si ya hay un evento con esa fecha
                if base.Eventos.find_one({"fecha": fecha}):
                    messagebox.showerror("Error", f"Ya existe un evento registrado para el día {fecha}. Por favor, seleccione otra fecha.")
                    return

                # Insertar evento
                base.Eventos.insert_one({
                    "nombre": nombre,
                    "fecha": fecha,
                    "lugar": lugar,
                    "descripcion": descripcion
                })

                actualizar_tabla()
                popup.destroy()
            except ValueError as e:
                messagebox.showerror("Error", str(e))


        tk.Button(popup, text="Guardar", command=guardar_evento, bg="#9b59b6").pack(pady=10)

    def eliminar_evento():
        seleccionado = tabla_eventos.selection()
        if seleccionado:
            valores = tabla_eventos.item(seleccionado[0], "values")
            nombre, fecha, lugar, descripcion = valores
            base.Eventos.delete_one({
                "nombre": nombre,
                "fecha": fecha,
                "lugar": lugar,
                "descripcion": descripcion
            })
            actualizar_tabla()
        else:
            messagebox.showwarning("Advertencia", "Seleccione un evento para eliminar.")

    # Botones
    frame_botones = tk.Frame(ventana_eventos)
    frame_botones.grid(row=2, column=0, pady=10)

    boton_crear = tk.Button(frame_botones, text="Agregar", command=agregar_evento,
                            bg="#4CAF50", fg="white", font=("Arial", 12, "bold"), padx=10, pady=5)
    boton_crear.grid(row=0, column=0, padx=5)

    boton_eliminar = tk.Button(frame_botones, text="Eliminar", command=eliminar_evento,
                               bg="#ca0000", fg="white", font=("Arial", 12, "bold"), padx=10, pady=5)
    boton_eliminar.grid(row=0, column=1, padx=5)

    actualizar_tabla()


# Función para abrir la ventana de gestión de reservaciones
def gestionar_reservaciones():
    ventana = tk.Toplevel()
    ventana.title("Gestión de Reservaciones")
    ventana.geometry("950x450")

    tabla = ttk.Treeview(ventana, columns=("cliente", "entrada", "salida", "cantidad", "habitacion"), show="headings")
    tabla.heading("cliente", text="Cliente")
    tabla.heading("entrada", text="Fecha Entrada")
    tabla.heading("salida", text="Fecha Salida")
    tabla.heading("cantidad", text="Cantidad Clientes")
    tabla.heading("habitacion", text="ID Habitación")
    tabla.pack(fill=tk.BOTH, expand=True, pady=10)

    def actualizar_tabla():
        tabla.delete(*tabla.get_children())
        for r in base.Reservaciones.find({}, {"_id": 0}):
            habitacion_id = r.get("id_habitacion", "N/A")
            tabla.insert("", tk.END, values=(r["cliente"], r["entrada"], r["salida"], r["cantidad"], habitacion_id))

    def agregar_reserva():
        popup = tk.Toplevel()
        popup.title("Nueva Reservación")
        popup.geometry("350x400")
        popup.grab_set()

        tk.Label(popup, text="Nombre del cliente:").pack()
        entry_nombre = tk.Entry(popup)
        entry_nombre.pack()

        tk.Label(popup, text="Fecha de entrada (dd/mm/yyyy):").pack()
        entry_entrada = tk.Entry(popup)
        entry_entrada.pack()

        tk.Label(popup, text="Fecha de salida (dd/mm/yyyy):").pack()
        entry_salida = tk.Entry(popup)
        entry_salida.pack()

        tk.Label(popup, text="Cantidad de clientes:").pack()
        entry_cantidad = tk.Entry(popup)
        entry_cantidad.pack()

        habitaciones = list(base.Habitaciones.find({"estado": "Disponible"}, {"_id": 0}))
        opciones_hab = [f'{h["id_habitacion"]} - {h["Descripcion"]}' for h in habitaciones]

        tk.Label(popup, text="Seleccione una habitación disponible:").pack()
        combo_habitacion = ttk.Combobox(popup, values=opciones_hab, state="readonly")
        combo_habitacion.pack()

        def guardar_reserva():
            try:
                nombre = entry_nombre.get()
                entrada = datetime.strptime(entry_entrada.get(), "%d/%m/%Y")
                salida = datetime.strptime(entry_salida.get(), "%d/%m/%Y")
                cantidad = int(entry_cantidad.get())
                habitacion_str = combo_habitacion.get()

                if salida < entrada:
                    messagebox.showerror("Error", "La fecha de salida no puede ser anterior a la de entrada.")
                    return

                if not habitacion_str:
                    messagebox.showerror("Error", "Debe seleccionar una habitación disponible.")
                    return

                id_habitacion = int(habitacion_str.split(" - ")[0])

                id_reservacion = contador("reservacion")

                base.Reservaciones.insert_one({
                    "id_reservacion": id_reservacion,
                    "cliente": nombre,
                    "entrada": entrada.strftime("%d/%m/%Y"),
                    "salida": salida.strftime("%d/%m/%Y"),
                    "cantidad": cantidad,
                    "id_habitacion": id_habitacion
                })

                base.Habitaciones.update_one(
                    {"id_habitacion": id_habitacion},
                    {"$set": {"estado": "Ocupada"}}
                )

                messagebox.showinfo("Reservación registrada", f"Reservación exitosa.\nNúmero de reservación: {id_reservacion}")
                actualizar_tabla()
                popup.destroy()
                ventana.lift()
            except ValueError as e:
                messagebox.showerror("Error", f"Datos inválidos: {e}")

        tk.Button(popup, text="Guardar", command=guardar_reserva, bg="lightblue").pack(pady=10)

    def eliminar_reserva():
        seleccionado = tabla.selection()
        if seleccionado:
            valores = tabla.item(seleccionado[0], "values")
            cliente, entrada, salida, cantidad, habitacion_id = valores

            base.Reservaciones.delete_one({
                "cliente": cliente,
                "entrada": entrada,
                "salida": salida,
                "cantidad": int(cantidad),
                "id_habitacion": int(habitacion_id)
            })

            base.Habitaciones.update_one(
                {"id_habitacion": int(habitacion_id)},
                {"$set": {"estado": "Disponible"}}
            )

            actualizar_tabla()
            messagebox.showinfo("Eliminado", f"La reservación fue eliminada y la habitación {habitacion_id} está disponible.")
            ventana.lift()
            ventana.attributes('-topmost', True)
            ventana.after(100, lambda: ventana.attributes('-topmost', False))
        else:
            messagebox.showwarning("Advertencia", "Seleccione una reservación para eliminar.")

    # Botones principales
    frame_botones = tk.Frame(ventana)
    frame_botones.pack(pady=5)
    tk.Button(frame_botones, text="Agregar Reservación", command=agregar_reserva).pack(side=tk.LEFT, padx=10)
    tk.Button(frame_botones, text="Eliminar Reservación", command=eliminar_reserva, bg="red").pack(side=tk.LEFT, padx=10)
    
    actualizar_tabla()

# Ventana principal
ventana = tk.Tk()
ventana.title('Menú principal de la Hotelera')
ventana.geometry('800x600')

barra_menu = tk.Menu(ventana)
ventana.config(menu=barra_menu)

menu = tk.Menu(barra_menu, tearoff=False)

menu.add_command(label='Gestionar Clientes', command=ventana_clientes)#Shernna
menu.add_command(label='Gestionar Departamentos', command=ventana_departamentos) #Marco
menu.add_command(label='Gestionar Empleados', command=ventana_empleados)#Shernna #
menu.add_command(label='Gestionar Eventos', command=gestionar_eventos) #Keyla
menu.add_command(label='Gestionar Habitaciones', command=ventana_habitaciones)#Adriela
menu.add_command(label='Gestionar Sedes de Hotel', command=ventana_hoteles)#Adriela
menu.add_command(label='Gestionar Mantenimientos', command = ventana_mantenimientos)#Rachel
menu.add_command(label='Gestionar Registros', command = ventana_registros)#Rachel
menu.add_command(label='Gestionar Reservaciones', command=gestionar_reservaciones)  #Keyla
menu.add_command(label='Gestionar Servicios', command=ventana_servicios)#Marco
menu.add_command(label='Cancelar Factura', command = ventana_facturas)#Marco
menu.add_separator()
menu.add_command(label='Salir', command=ventana.destroy)

barra_menu.add_cascade(label="Menú", menu=menu)

# Cargar imagen
try:
    imagen_original = Image.open('img/hotelera.jpg')
    imagen_redimensionada = imagen_original.resize((800, 600))
    imagen = ImageTk.PhotoImage(imagen_redimensionada)


    canvas = tk.Canvas(ventana, width=800, height=600)
    canvas.pack()


    canvas.create_image(0, 0, anchor="nw", image=imagen)


    canvas.create_text(400, 300, text="Bienvenido al sistema de gestión hotelera", font=("Times New Roman", 24, "bold"),
                       fill="white")
except tk.TclError:
    messagebox.showerror("Error", "No se pudo cargar la imagen")

ventana.mainloop()

