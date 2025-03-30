import tkinter as tk
from tkinter import ttk, messagebox
from click import command
from pymongo import MongoClient, ReturnDocument
from PIL import Image, ImageTk
from datetime import datetime, timezone

# Conexión a la base de datos
client = MongoClient("mongodb://localhost:27017/")
base = client["Hotel"]
clienteHotel = client["Cliente"]
empleadoHotel = client["Empleado"]

# Función para contador
def contador(nombre_id):
    counter = base.Counters.find_one_and_update(
        {"id": nombre_id},
        {"$inc": {"seq": 1}},
        upsert=True,
        return_document=ReturnDocument
    )
    return counter["seq"]

# Función para abrir la ventana de gestión de clientes
def ventana_clientes():
    ventana_cli = tk.Toplevel()
    ventana_cli.title("Gestión de Clientes")
    ventana_cli.geometry("800x600")

    # Tabla para mostrar los clientes
    tabla_clientes = ttk.Treeview(ventana_cli, columns=2)
    tabla_clientes.grid(row=0, column=0, columnspan=2, pady=10)
    tabla_clientes.heading("#0", text="ID Cliente")
    tabla_clientes.heading("#1", text="Nombre cliente")
    # Función para mostrar clientes
    def mostrar_clientes():
        try:
            clientes = tabla_clientes.get_children()
            for cliente_temporal in clientes:
                tabla_clientes.delete(cliente_temporal)
            for cliente in clienteHotel.Cliente.find():
                tabla_clientes.insert('', 0, text=cliente["id_cliente"], values=cliente["nombre_cliente"])
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar los cliente: {e}")

    # Función para crear un cliente
    def crear_cliente():
        if len(id_cliente.get()) != 0 and len(nombre_cliente.get()) != 0:
            try:
                cliente = {
                    "id_cliente": int(id_cliente.get()),
                    "Nombre": nombre_cliente.get()
                }
                clienteHotel.Cliente.insert_one(cliente)
                id_cliente.delete(0, tk.END)
                nombre_cliente.delete(0, tk.END)
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
            clienteHotel.Cliente.delete_one({"id_cliente": int(id_cli)})
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

            if len(nuevo_nombre) == 0:
                messagebox.showerror("Error", "El nombre no puede estar vacío.")
                return

            clienteHotel.Cliente.update_one(
                {"id_cliente": int(id_cli)},
                {"$set": {"nombre_cliente": nuevo_nombre}}
            )
            nombre_cliente.delete(0, tk.END)
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

    tk.Button(ventana_cli, text="Crear", command=crear_cliente, bg="light green", fg="black").grid(row=3, column=0, pady=10)
    tk.Button(ventana_cli, text="Modificar", command=modificar_cliente, bg="light yellow", fg="black").grid(row=3, column=1, pady=10)
    tk.Button(ventana_cli, text="Eliminar", command=eliminar_cliente, bg="red", fg="black").grid(row=3, column=2, pady=10)

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

    tk.Button(ventana_dep, text="Crear", command=crear_departamento, bg="light green", fg="black").grid(row=3, column=0, pady=10)
    tk.Button(ventana_dep, text="Modificar", command=modificar_departamento, bg="light yellow", fg="black").grid(row=3, column=1, pady=10)
    tk.Button(ventana_dep, text="Eliminar", command=eliminar_departamento, bg="red", fg="black").grid(row=3, column=2, pady=10)

    # Cargar los departamentos inicialmente
    mostrar_departamentos()

# Función para abrir la ventana de gestión de empleados
def ventana_empleados():
    ventana_emple = tk.Toplevel()
    ventana_emple.title("Gestión de Empleados")
    ventana_emple.geometry("800x600")

    # Tabla para mostrar los empleados
    tabla_empleados = ttk.Treeview(ventana_emple, columns=2)
    tabla_empleados.grid(row=0, column=0, columnspan=2, pady=10)
    tabla_empleados.heading("#0", text="ID Empleado")
    tabla_empleados.heading("#1", text="Nombre empleado")
    # Función para mostrar empleados
    def mostrar_empleados():
        try:
            empleados = tabla_empleados.get_children()
            for empleado_temporal in empleados:
                tabla_empleados.delete(empleado_temporal)
            for empleado in empleadoHotel.Empleado.find():
                tabla_empleados.insert('', 0, text=empleado["id_empleado"], values=empleado["nombre_empleado"])
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar los empleados: {e}")

    # Función para crear un empleado
    def crear_empleado():
        if len(id_empleado.get()) != 0 and len(nombre_empleado.get()) != 0:
            try:
                empleado = {
                    "id_empleado": int(id_empleado.get()),
                    "nombre_empleado": nombre_empleado.get()
                }
                empleadoHotel.Empleado.insert_one(empleado)
                id_empleado.delete(0, tk.END)
                nombre_empleado.delete(0, tk.END)
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
            empleadoHotel.Empleado.delete_one({"id_empleado": int(id_emple)})
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

            if len(nuevo_nombre) == 0:
                messagebox.showerror("Error", "El nombre no puede estar vacío.")
                return

            empleadoHotel.Empleado.update_one(
                {"id_empleado": int(id_cli)},
                {"$set": {"nombre_empleado": nuevo_nombre}}
            )
            nombre_empleado.delete(0, tk.END)
            mostrar_empleados()
        except IndexError:
            messagebox.showwarning("Advertencia", "Selecciona un empleado para modificar")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo modificar el empleado: {e}")

   # Campos de entrada y botones para empleado
    tk.Label(ventana_emple, text="ID Empleado").grid(row=1, column=0)
    id_empleado = tk.Entry(ventana_emple)
    id_empleado.grid(row=1, column=1)

    tk.Label(ventana_emple, text="Nombre empleado").grid(row=2, column=0)
    nombre_empleado = tk.Entry(ventana_emple)
    nombre_empleado.grid(row=2, column=1)

    tk.Button(ventana_emple, text="Crear", command=crear_empleado, bg="light green", fg="black").grid(row=3, column=0, pady=10)
    tk.Button(ventana_emple, text="Modificar", command=modificar_empleado, bg="light yellow", fg="black").grid(row=3, column=1, pady=10)
    tk.Button(ventana_emple, text="Eliminar", command=eliminar_empleado, bg="red", fg="black").grid(row=3, column=2, pady=10)

    # Cargar los empleados inicialmente
    mostrar_empleados()

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

        tk.Button(ventana_ser, text="Crear", command=crear_servicio, bg="light green", fg="black").grid(row=3,
                                                                                                            column=0,
                                                                                                            pady=10)
        tk.Button(ventana_ser, text="Modificar", command=modificar_servicio, bg="light yellow", fg="black").grid(
            row=3, column=1, pady=10)
        tk.Button(ventana_ser, text="Eliminar", command=eliminar_servicio, bg="red", fg="black").grid(row=3,
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

            tk.Button(ventana_fac, text="Crear", command=crear_factura, bg="light green", fg="black").grid(row=5, column=1)

        # Cargar las facturas inicialmente
        mostrar_facturas()





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
menu.add_command(label='Gewstionar Eventos')#Keyla
menu.add_command(label='Gestionar Habitaciones')#Adriela
menu.add_command(label='Gestionar Sedes de Hotel')#Adriela
menu.add_command(label='Gestionar Mantenimientos')#Rachel
menu.add_command(label='Gestionar Registros')#Rachel
menu.add_command(label='Gestionar Reservaciones')#Keyla
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
