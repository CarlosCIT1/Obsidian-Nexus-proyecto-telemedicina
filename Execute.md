import sys
from db_connection import get_conn
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from PIL import Image, ImageTk
from medicos import NexusCare
from usuarios import Usuario, hash_password
from citas import Consulta
from citas import ConsultaPaciente

bib = NexusCare()
current_user = None  #

def login_inicial():
    """Ventana gráfica de login estilo registrar usuario."""
    global current_user

    win = tk.Toplevel()
    win.title("Iniciar sesión")
    win.geometry("500x400")
    win.resizable(False, False)

    # ======== Imágenes ========
    img_logo1 = Image.open("C:/Users/maryf/OneDrive/Escritorio/Imagenes Tópicos/Nexus_Care_LOGO_SOLO-removebg-preview.png")
    img_logo1 = img_logo1.resize((80, 80), Image.Resampling.LANCZOS)
    img_logo1_tk = ImageTk.PhotoImage(img_logo1)

    img_logo2 = Image.open("C:/Users/maryf/OneDrive/Escritorio/Imagenes Tópicos/Nexus_Care-removebg-preview.png")
    img_logo2 = img_logo2.resize((230, 80), Image.Resampling.LANCZOS)
    img_logo2_tk = ImageTk.PhotoImage(img_logo2)

    frame_imgs = ttk.Frame(win)
    frame_imgs.pack(pady=15)

    ttk.Label(frame_imgs, image=img_logo1_tk).pack(side="left", padx=10)
    ttk.Label(frame_imgs, image=img_logo2_tk).pack(side="left", padx=10)

    win.img_logo1_tk = img_logo1_tk
    win.img_logo2_tk = img_logo2_tk

    # ======== Formulario Login ========
    frame = ttk.Frame(win, padding=20)
    frame.pack(fill="both", expand=True)

    ttk.Label(frame, text="Usuario:").grid(row=0, column=0, sticky="w", pady=5)
    entry_user = tk.Entry(frame, highlightthickness=2, highlightbackground="#5F9BE0", highlightcolor="green", width=35)
    entry_user.grid(row=0, column=1, pady=5)

    ttk.Label(frame, text="Contraseña:").grid(row=1, column=0, sticky="w", pady=5)
    entry_pwd = tk.Entry(frame, highlightthickness=2, highlightbackground="#5F9BE0", highlightcolor="green", width=35, show="*")
    entry_pwd.grid(row=1, column=1, pady=5)

    resultado = {"user": None}

    # ============ Funciones ============

    def iniciar():
        login = entry_user.get().strip()
        pwd = entry_pwd.get().strip()

        if not login or not pwd:
            messagebox.showwarning("Campos vacíos", "Debes llenar usuario y contraseña.")
            return

        usuario = Usuario.autenticar(login, pwd)
        if usuario:
            resultado["user"] = usuario
            messagebox.showinfo("Bienvenido", f"Hola, {usuario.nombre} ({usuario.role})")
            win.destroy()
        else:
            messagebox.showerror("Error", "Credenciales incorrectas.")

    def registrar():
        win.destroy()
        nuevo = registrar_usuario_publico()
        if nuevo:
            messagebox.showinfo("Bienvenido", f"Usuario creado y conectado: {nuevo.nombre}")
            resultado["user"] = nuevo

    def cancelar():
        root.destroy()

    # Botones
    btn_frame = ttk.Frame(frame)
    btn_frame.grid(row=2, column=0, columnspan=2, pady=20)

    tk.Button(btn_frame, text="Iniciar sesión", relief="raised", bd=4, width=15, bg="#3a7bd5", fg="white",
              command=iniciar).pack(side="left", padx=10)

    tk.Button(btn_frame, text="Registrarse", relief="raised", bd=4, width=15, bg="#4caf50", fg="white",
              command=registrar).pack(side="left", padx=10)

    tk.Button(btn_frame, text="Cancelar", relief="raised", bd=4, width=12, bg="#ef5350", fg="white",
              command=cancelar).pack(side="left", padx=10)

    win.grab_set()
    win.focus_set()
    win.wait_window()

    # Si hubo login:
    if resultado["user"]:
        current_user = resultado["user"]
        lbl_help.config(text=f"Usuario conectado: {current_user.nombre} ({current_user.role})")
        ajustar_menu_por_rol()

    if current_user.role == "Doctor":
        listar_consultas()


def requiere_admin(func):
    """Decorador simple para funciones que requieren rol 'Admin'."""
    def wrapper(*args, **kwargs):
        if current_user is None or (current_user.role or "").lower() != 'admin':
            messagebox.showerror("Permisos", "Acción restringida: se requiere usuario admin.")
            return
        return func(*args, **kwargs)
    return wrapper


# Nueva función: registro público (sin requerir admin)
def registrar_usuario_publico():

    win = tk.Toplevel()
    win.title("Registrar usuario")
    win.geometry("600x500")
    win.resizable(False, False)

    # ======== Cargar imágenes ========
    img_salida3 = Image.open("C:/Users/maryf/OneDrive/Escritorio/Imagenes Tópicos/Nexus_Care_LOGO_SOLO-removebg-preview.png")
    img_salida3 = img_salida3.resize((70, 70), Image.Resampling.LANCZOS)
    img_salida3_tk = ImageTk.PhotoImage(img_salida3)

    img_salida4 = Image.open("C:/Users/maryf/OneDrive/Escritorio/Imagenes Tópicos/Nexus_Care-removebg-preview.png")
    img_salida4 = img_salida4.resize((220, 70), Image.Resampling.LANCZOS)
    img_salida4_tk = ImageTk.PhotoImage(img_salida4)

    # ======== Frame para imágenes ========
    frame_imgs = ttk.Frame(win)
    frame_imgs.pack(pady=20)

    ttk.Label(frame_imgs, image=img_salida3_tk).pack(side="left", padx=10)
    ttk.Label(frame_imgs, image=img_salida4_tk).pack(side="left", padx=10)

    # Guardar referencias para evitar garbage collection
    win.img_salida3_tk = img_salida3_tk
    win.img_salida4_tk = img_salida4_tk

    # ======== Frame del formulario ========
    frame = ttk.Frame(win, padding=20)
    frame.pack(fill="both", expand=True)

    resultado = {"user": None}

    # --- Nombre ---
    ttk.Label(frame, text="Nombre(s) del usuario:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
    entry_nombre = tk.Entry(frame, width=35, highlightthickness=2, highlightbackground="#5F9BE0", highlightcolor="green")
    entry_nombre.grid(row=0, column=1, padx=5, pady=5)

    ttk.Label(frame, text="Apellidos(s) del usuario:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
    entry_apellidos = tk.Entry(frame, width=35, highlightthickness=2, highlightbackground="#5F9BE0", highlightcolor="green")
    entry_apellidos.grid(row=1, column=1, padx=5, pady=5)

    # correo
    ttk.Label(frame, text="Correo:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
    entry_correo = tk.Entry(frame, width=35, highlightthickness=2, highlightbackground="#5F9BE0", highlightcolor="green")
    entry_correo.grid(row=2, column=1, padx=5, pady=5)

    # telefono
    ttk.Label(frame, text="Numero de teléfono:").grid(row=3, column=0, sticky="w", padx=5, pady=5)
    entry_telefono = tk.Entry(frame, width=35, highlightthickness=2, highlightbackground="#5F9BE0", highlightcolor="green")
    entry_telefono.grid(row=3, column=1, padx=5, pady=5)

    # fecha nacimiento
    ttk.Label(frame, text="Fecha de nacimiento (YYYY-MM-DD):").grid(row=4, column=0, sticky="w", padx=5, pady=5)
    entry_fechanac = tk.Entry(frame, width=35, highlightthickness=2, highlightbackground="#5F9BE0", highlightcolor="green")
    entry_fechanac.grid(row=4, column=1, padx=5, pady=5)

    # sexo
    ttk.Label(frame, text="Sexo (M/F/N):").grid(row=5, column=0, sticky="w", padx=5, pady=5)
    cb_sexo = ttk.Combobox(frame, values=["M", "F", "N"], state="readonly", width=32)
    cb_sexo.grid(row=5, column=1, padx=5, pady=5)
    cb_sexo.set("N")

    # --- Rol ---
    ttk.Label(frame, text="Rol (Paciente/Doctor/Admin):").grid(row=6, column=0, sticky="w", padx=5, pady=5)
    cb_role = ttk.Combobox(frame, values=["Paciente", "Doctor", "Admin"], state="readonly", width=32)
    cb_role.grid(row=6, column=1, padx=5, pady=5)
    cb_role.set("Paciente")

    # --- Contraseña ---
    ttk.Label(frame, text="Contraseña (vacío = sin contraseña):").grid(row=7, column=0, sticky="w", padx=5, pady=5)
    entry_pwd = tk.Entry(frame, show="*", width=35, highlightthickness=2, highlightbackground="#5F9BE0", highlightcolor="green")
    entry_pwd.grid(row=7, column=1, padx=5, pady=5)

    # ------------------------
    # Funciones de botones
    # ------------------------
    def guardar():
        nombre = entry_nombre.get().strip()
        if not nombre:
            messagebox.showwarning("Falta nombre", "El nombre es obligatorio.")
            return

        apellidos = entry_apellidos.get().strip()
        if not apellidos:
            messagebox.showwarning("Falta apellidos", "Los apellidos son obligatorios.")
            return

        correo = entry_correo.get().strip()
        if not correo:
            messagebox.showwarning("Falta correo", "El correo es obligatorio.")
            return

        telefono = entry_telefono.get().strip()
        if not telefono:
            messagebox.showwarning("Falta telefono", "El el numero de telefono es obligatorio.")
            return

        fechanac = entry_fechanac.get().strip()
        if not fechanac:
            messagebox.showwarning("Falta fecha", "La fecha de nacimiento es obligatoria (YYYY-MM-DD).")
            return

        sexo = cb_sexo.get().strip().upper()
        if sexo not in ('M', 'F', 'N'):
            messagebox.showwarning("Sexo inválido", "Sexo inválido. Se usará 'N'.")
            sexo = 'N'

        role = cb_role.get().strip()
        if role not in ('Paciente', 'Doctor', 'Admin'):
            messagebox.showwarning("Rol inválido", "Rol inválido. Se usará 'Paciente'.")
            role = 'Paciente'

        pwd = entry_pwd.get()

        u = Usuario.crear(nombre, apellidos, correo, telefono or None, fechanac, sexo, role, pwd)
        resultado["user"] = u

        messagebox.showinfo("OK", f"Usuario registrado: {u.nombre} (id={u.id}, role={u.role})")
        win.destroy()

    def cancelar():
        resultado["user"] = None
        win.destroy()

    # --- Botones ---
    btn_frame = ttk.Frame(frame)
    btn_frame.grid(row=8, column=0, columnspan=2, pady=15)

    tk.Button(
        btn_frame, text="Registrar",
        foreground="white",
        font=("Arial", 8, "bold"),
        relief="raised",
        bd=4,
        activebackground="#5ba8f5",
        background="#3a7bd5",
        command=guardar
    ).pack(side="left", padx=10)

    tk.Button(
        btn_frame, text="Cancelar",
        command=cancelar,
        font=("Arial", 8, "bold"),
        relief="raised",
        bd=4,
        background="#ef5350",
        activebackground="#e57373",
        foreground="white"
    ).pack(side="left", padx=10)

    win.grab_set()
    win.focus_set()
    win.wait_window()

    return resultado["user"]


# --- Registro / modificación / eliminación (admin) ---
@requiere_admin
def registrar_usuario():

    win = tk.Toplevel()
    win.title("Registrar usuario")
    win.geometry("600x500")
    win.resizable(False, False)

    # ======== Cargar imágenes ========
    img_salida3 = Image.open("C:/Users/maryf/OneDrive/Escritorio/Imagenes Tópicos/Nexus_Care_LOGO_SOLO-removebg-preview.png")
    img_salida3 = img_salida3.resize((70, 70), Image.Resampling.LANCZOS)
    img_salida3_tk = ImageTk.PhotoImage(img_salida3)

    img_salida4 = Image.open("C:/Users/maryf/OneDrive/Escritorio/Imagenes Tópicos/Nexus_Care-removebg-preview.png")
    img_salida4 = img_salida4.resize((220, 70), Image.Resampling.LANCZOS)
    img_salida4_tk = ImageTk.PhotoImage(img_salida4)

    # ======== Frame para imágenes ========
    frame_imgs = ttk.Frame(win)
    frame_imgs.pack(pady=20)

    ttk.Label(frame_imgs, image=img_salida3_tk).pack(side="left", padx=10)
    ttk.Label(frame_imgs, image=img_salida4_tk).pack(side="left", padx=10)

    win.img_salida3_tk = img_salida3_tk
    win.img_salida4_tk = img_salida4_tk

    # ======== Frame del formulario ========
    frame = ttk.Frame(win, padding=20)
    frame.pack(fill="both", expand=True)

    resultado = {"user": None}

    # Nombre
    ttk.Label(frame, text="Nombre(s):").grid(row=0, column=0, sticky="w", padx=5, pady=5)
    entry_nombre = tk.Entry(frame, highlightthickness=2, highlightbackground="#5F9BE0", highlightcolor="green", width=35)
    entry_nombre.grid(row=0, column=1, padx=5, pady=5)

    # Apellidos
    ttk.Label(frame, text="Apellidos:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
    entry_apellidos = tk.Entry(frame, highlightthickness=2, highlightbackground="#5F9BE0", highlightcolor="green", width=35)
    entry_apellidos.grid(row=1, column=1, padx=5, pady=5)

    # Correo
    ttk.Label(frame, text="Correo:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
    entry_correo = tk.Entry(frame, highlightthickness=2, highlightbackground="#5F9BE0", highlightcolor="green", width=35)
    entry_correo.grid(row=2, column=1, padx=5, pady=5)

    # Telefono
    ttk.Label(frame, text="Numero de Teléfono:").grid(row=3, column=0, sticky="w", padx=5, pady=5)
    entry_telefono = tk.Entry(frame, highlightthickness=2, highlightbackground="#5F9BE0", highlightcolor="green", width=35)
    entry_telefono.grid(row=3, column=1, padx=5, pady=5)

    # Rol
    ttk.Label(frame, text="Rol:").grid(row=4, column=0, sticky="w", padx=5, pady=5)
    cb_role = ttk.Combobox(frame, values=["Paciente", "Doctor", "Admin"], state="readonly", width=32)
    cb_role.grid(row=4, column=1, padx=5, pady=5)
    cb_role.set("Paciente")

    # Contraseña
    ttk.Label(frame, text="Contraseña:").grid(row=5, column=0, sticky="w", padx=5, pady=5)
    entry_pwd = tk.Entry(frame, highlightthickness=2, highlightbackground="#5F9BE0", highlightcolor="green", show="*", width=35)
    entry_pwd.grid(row=5, column=1, padx=5, pady=5)

    # ========== BOTONES ==========
    def guardar():
        nombre = entry_nombre.get().strip()
        apellidos = entry_apellidos.get().strip()
        correo = entry_correo.get().strip()
        telefono = entry_telefono.get().strip()
        role = cb_role.get().strip()
        pwd = entry_pwd.get()

        if not nombre:
            messagebox.showwarning("Falta nombre", "El nombre es obligatorio.")
            return

        if not correo:
            messagebox.showwarning("Falta correo", "El correo es obligatorio.")
            return
        
        if not telefono:
            messagebox.showwarning("Falta telefono", "El telefono es obligatorio.")
            return
        try:
            u = Usuario.crear(
                nombre,
                apellidos,
                correo,
                telefono,              # teléfono nulo
                "1900-01-01",      # fecha default como en tu versión original
                'N',               # sexo por default
                role,
                pwd,
            )
            resultado["user"] = u
            messagebox.showinfo("OK", f"Usuario registrado: {u.nombre} (id={u.id})")

            win.destroy()
            listar_usuarios()

        except Exception as e:
            messagebox.showerror("Error", f"Error al registrar usuario:\n{e}")

    def cancelar():
        resultado["user"] = None
        win.destroy()

    btn_frame = ttk.Frame(frame)
    btn_frame.grid(row=6, column=0, columnspan=2, pady=20)

    tk.Button(
        btn_frame, text="Registrar",
        foreground="white",
        font=("Arial", 8, "bold"),
        relief="raised",
        bd=4,
        activebackground="#5ba8f5",
        background="#3a7bd5",
        command=guardar
    ).pack(side="left", padx=10)

    tk.Button(
        btn_frame, text="Cancelar",
        command=cancelar,
        font=("Arial", 8, "bold"),
        relief="raised",
        bd=4,
        background="#ef5350",
        activebackground="#e57373",
        foreground="white"
    ).pack(side="left", padx=10)

    win.grab_set()
    win.focus_set()
    win.wait_window()

    return resultado["user"]

@requiere_admin
def modificar_usuario():
    win = tk.Toplevel()
    win.title("Modificar usuario")
    win.geometry("600x550")
    win.resizable(False, False)

    # ======== Cargar imágenes ========
    img_s1 = Image.open("C:/Users/maryf/OneDrive/Escritorio/Imagenes Tópicos/Nexus_Care_LOGO_SOLO-removebg-preview.png")
    img_s1 = img_s1.resize((70, 70), Image.Resampling.LANCZOS)
    img_s1_tk = ImageTk.PhotoImage(img_s1)

    img_s2 = Image.open("C:/Users/maryf/OneDrive/Escritorio/Imagenes Tópicos/Nexus_Care-removebg-preview.png")
    img_s2 = img_s2.resize((220, 70), Image.Resampling.LANCZOS)
    img_s2_tk = ImageTk.PhotoImage(img_s2)

    frame_imgs = ttk.Frame(win)
    frame_imgs.pack(pady=20)

    ttk.Label(frame_imgs, image=img_s1_tk).pack(side="left", padx=10)
    ttk.Label(frame_imgs, image=img_s2_tk).pack(side="left", padx=10)

    win.img1 = img_s1_tk
    win.img2 = img_s2_tk

    # ======== Formulario ========
    frame = ttk.Frame(win, padding=20)
    frame.pack(fill="both", expand=True)

    # Campo para buscar un usuario
    ttk.Label(frame, text="Nombre del usuario a modificar:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
    entry_buscar = tk.Entry(frame, width=35, highlightthickness=2, highlightbackground="#5F9BE0", highlightcolor="green")
    entry_buscar.grid(row=0, column=1, padx=5, pady=5)

    # Campos editables
    labels = ["Nombre", "Apellidos", "Correo", "Telefono", "Rol (Paciente/Doctor/Admin)", "Contraseña (opcional)"]
    entradas = {}

    for i, texto in enumerate(labels, start=1):
        ttk.Label(frame, text=texto + ":").grid(row=i, column=0, sticky="w", padx=5, pady=5)
        ent = tk.Entry(frame, width=35, show="*" if "Contraseña" in texto else "", highlightthickness=2, highlightbackground="#5F9BE0", highlightcolor="green")
        ent.grid(row=i, column=1, padx=5, pady=5)
        entradas[texto] = ent

    # ---------- Buscar usuario ----------
    def buscar_usuario():
        nombre = entry_buscar.get().strip()
        if not nombre:
            messagebox.showwarning("Aviso", "Ingrese un nombre.")
            return

        usr = Usuario.buscar_por_nombre(nombre)
        if usr is None:
            messagebox.showerror("Error", "Usuario no encontrado.")
            return

        win.usr_actual = usr

        entradas["Nombre"].delete(0, tk.END); entradas["Nombre"].insert(0, usr.nombre)
        entradas["Apellidos"].delete(0, tk.END); entradas["Apellidos"].insert(0, usr.apellidos)
        entradas["Correo"].delete(0, tk.END); entradas["Correo"].insert(0, usr.correo)
        entradas["Telefono"].delete(0, tk.END); entradas["Telefono"].insert(0, usr.telefono)
        entradas["Rol (Paciente/Doctor/Admin)"].delete(0, tk.END); entradas["Rol (Paciente/Doctor/Admin)"].insert(0, usr.role)
        entradas["Contraseña (opcional)"].delete(0, tk.END)

        messagebox.showinfo("OK", "Usuario cargado.")

    tk.Button(
        frame, text="Buscar",
        background="#3a7bd5", activebackground="#5ba8f5",
        foreground="white", font=("Arial", 8, "bold"),
        relief="raised", bd=4,
        command=buscar_usuario
    ).grid(row=0, column=2, padx=10)

    # ---------- Guardar cambios ----------
    def guardar_cambios():
        if not hasattr(win, "usr_actual"):
            messagebox.showwarning("Aviso", "Debe buscar un usuario primero.")
            return

        usr = win.usr_actual
        nuevo_nombre = entradas["Nombre"].get().strip()
        nuevo_apellidos = entradas["Apellidos"].get().strip()
        nuevo_correo = entradas["Correo"].get().strip()
        nuevo_telefono = entradas["Teléfono"].get().strip()
        nuevo_role = entradas["Rol (Paciente/Doctor/Admin)"].get().strip()
        nueva_pwd = entradas["Contraseña (opcional)"].get().strip()

        try:
            conn = get_conn()
            cur = conn.cursor()

            if nueva_pwd:
                cur.execute("""
                    UPDATE usuarios 
                    SET us_nombre=%s, us_apellidos=%s, us_correo=%s, us_telefono=%s, us_rol=%s
                    WHERE us_clave=%s
                """, (nuevo_nombre, nuevo_apellidos, nuevo_correo, nuevo_telefono, nuevo_role, hash_password(nueva_pwd), usr.id))
            else:
                cur.execute("""
                    UPDATE usuarios 
                    SET us_nombre=%s, us_apellidos=%s, us_correo=%s, us_rol=%s
                    WHERE us_clave=%s
                """, (nuevo_nombre, nuevo_apellidos, nuevo_correo, nuevo_role, usr.id))

            conn.commit()
            cur.close()
            conn.close()

            messagebox.showinfo("OK", "Usuario modificado correctamente.")
            listar_usuarios()
            win.destroy()

        except Exception as e:
            messagebox.showerror("Error", f"{e}")

    tk.Button(
        frame, text="Guardar",
        background="#3a7bd5", activebackground="#5ba8f5",
        foreground="white", font=("Arial", 8, "bold"),
        relief="raised", bd=4,
        command=guardar_cambios
    ).grid(row=7, column=0, columnspan=2, pady=20)

@requiere_admin
def eliminar_usuario():
    win = tk.Toplevel()
    win.title("Eliminar usuario")
    win.geometry("450x350")
    win.resizable(False, False)

    ttk.Label(win, text="Eliminar usuario", font=("Arial", 12, "bold")).pack(pady=15)

    frame = ttk.Frame(win, padding=20)
    frame.pack()

    # --- Opción 1: eliminar por ID ---
    ttk.Label(frame, text="Eliminar por ID:").grid(row=0, column=0, pady=8, sticky="w")
    entry_id = tk.Entry(frame, width=30)
    entry_id.grid(row=0, column=1)

    def eliminar_id():
        try:
            user_id = int(entry_id.get())
        except:
            messagebox.showerror("Error", "El ID debe ser un número entero.")
            return

        borrados = Usuario.eliminar_por_id(user_id)

        if borrados == 0:
            messagebox.showwarning("Aviso", "No existe un usuario con ese ID.")
        else:
            messagebox.showinfo("Éxito", f"Usuario con ID {user_id} eliminado.")
            listar_usuarios()
            win.destroy()

    tk.Button(frame, text="Eliminar por ID", bg="#ef5350", fg="white",
              command=eliminar_id).grid(row=1, column=1, pady=8, sticky="e")

    # --- Opción 2: eliminar por Apellido ---
    ttk.Label(frame, text="Eliminar por apellido:").grid(row=2, column=0, pady=8, sticky="w")
    entry_apellido = tk.Entry(frame, width=30)
    entry_apellido.grid(row=2, column=1)

    def buscar_apellidos():
        apellido = entry_apellido.get().strip()
        if not apellido:
            messagebox.showwarning("Aviso", "Debe ingresar un apellido.")
            return

        resultados = Usuario.buscar_por_apellido(apellido)

        if not resultados:
            messagebox.showinfo("Sin resultados", "No se encontraron usuarios con ese apellido.")
            return

        # Mostrar lista para elegir
        sel_win = tk.Toplevel()
        sel_win.title("Seleccionar usuario a eliminar")
        sel_win.geometry("400x300")

        ttk.Label(sel_win,
                  text=f"Usuarios con apellido '{apellido}':",
                  font=("Arial", 11, "bold")).pack(pady=10)

        tree = ttk.Treeview(sel_win, columns=("ID", "Nombre", "Correo"), show="headings")
        tree.heading("ID", text="ID")
        tree.heading("Nombre", text="Nombre")
        tree.heading("Correo", text="Correo")
        tree.pack(fill="both", expand=True, padx=10, pady=10)

        for usr in resultados:
            tree.insert("", "end", values=(usr.id, usr.nombre + " " + usr.apellidos, usr.correo))

        def eliminar_seleccion():
            item = tree.selection()
            if not item:
                messagebox.showwarning("Aviso", "Seleccione un usuario.")
                return

            user_id = tree.item(item)["values"][0]

            Usuario.eliminar_por_id(user_id)
            messagebox.showinfo("Eliminado", f"Usuario con ID {user_id} eliminado.")

            sel_win.destroy()
            win.destroy()
            listar_usuarios()

        tk.Button(sel_win, text="Eliminar seleccionado", bg="#ef5350", fg="white", command=eliminar_seleccion).pack(pady=10)
        tk.Button(frame, text="Buscar y eliminar por apellido", bg="#3a7bd5", fg="white", command=buscar_apellidos).grid(row=3, column=1, pady=8, sticky="e")
        tk.Button(win, text="Cerrar", bg="#999", fg="white",command=win.destroy).pack(pady=10)
    

@requiere_admin
def agregar_especialidad():
    win = tk.Toplevel()
    win.title("Agregar especialidad")
    win.geometry("400x250")
    win.resizable(False, False)

    frame = ttk.Frame(win, padding=20)
    frame.pack(fill="both", expand=True)

    ttk.Label(frame, text="Nombre de la especialidad:").grid(row=0, column=0, sticky="w", pady=5)
    entry_nombre = tk.Entry(frame, width=35)
    entry_nombre.grid(row=0, column=1, pady=5)

    def guardar():
        nom = entry_nombre.get().strip()

        if not nom:
            messagebox.showwarning("Falta nombre", "Debes ingresar un nombre para la especialidad.")
            return

        try:
            conn = get_conn()
            c = conn.cursor()
            c.execute("INSERT INTO especialidades (es_nombre) VALUES (%s)", (nom,))
            conn.commit()
            conn.close()

            messagebox.showinfo("OK", "Especialidad agregada correctamente.")
            win.destroy()

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo agregar la especialidad:\n{e}")

    tk.Button(frame, text="Guardar", bg="#3a7bd5", fg="white", command=guardar).grid(row=2, column=0, columnspan=2, pady=15)

@requiere_admin
def modificar_especialidad():
    win = tk.Toplevel()
    win.title("Modificar especialidad")
    win.geometry("450x300")
    win.resizable(False, False)

    frame = ttk.Frame(win, padding=20)
    frame.pack(fill="both", expand=True)

    ttk.Label(frame, text="Buscar especialidad por ID o Nombre:").grid(row=0, column=0, sticky="w")
    entry_buscar = tk.Entry(frame, width=35)
    entry_buscar.grid(row=0, column=1, pady=5)

    # Campos editables
    ttk.Label(frame, text="Nuevo nombre:").grid(row=1, column=0, sticky="w")
    entry_nombre = tk.Entry(frame, width=35)
    entry_nombre.grid(row=1, column=1, pady=5)

    ttk.Label(frame, text="Nueva descripción:").grid(row=2, column=0, sticky="w")
    entry_desc = tk.Entry(frame, width=35)
    entry_desc.grid(row=2, column=1, pady=5)

    def buscar():
        val = entry_buscar.get().strip()
        if not val:
            messagebox.showwarning("Falta dato", "Ingresa un ID o nombre de especialidad.")
            return

        try:
            conn = get_conn()
            c = conn.cursor()

            # Buscar por ID o nombre
            c.execute("""
                SELECT id, nombre, descripcion
                FROM especialidades
                WHERE es_clave = %s OR es_nombre = %s
            """, (val, val))

            esp = c.fetchone()
            conn.close()

            if not esp:
                messagebox.showerror("No encontrado", "No existe esa especialidad.")
                return

            win.esp_id = esp[0]
            entry_nombre.delete(0, tk.END)
            entry_nombre.insert(0, esp[1])

            entry_desc.delete(0, tk.END)
            entry_desc.insert(0, esp[2] or "")

            messagebox.showinfo("OK", "Especialidad cargada.")

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo buscar:\n{e}")

    def guardar():
        if not hasattr(win, "esp_id"):
            messagebox.showwarning("Falta búsqueda", "Primero busca una especialidad.")
            return

        nuevo_nom = entry_nombre.get().strip()
        nuevo_desc = entry_desc.get().strip()

        if not nuevo_nom:
            messagebox.showwarning("Falta nombre", "El nombre no puede quedar vacío.")
            return

        try:
            conn = get_conn()
            c = conn.cursor()
            c.execute("""
                UPDATE especialidades
                SET es_nombre = %s
                WHERE es_clave = %s
            """, (nuevo_nom, nuevo_desc, win.esp_id))
            conn.commit()
            conn.close()

            messagebox.showinfo("OK", "Especialidad modificada.")
            win.destroy()

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo modificar:\n{e}")

    tk.Button(frame, text="Buscar", bg="#4caf50", fg="white", command=buscar).grid(row=3, column=0, columnspan=2, pady=5)
    tk.Button(frame, text="Guardar cambios", bg="#3a7bd5", fg="white", command=guardar).grid(row=4, column=0, columnspan=2, pady=10)

@requiere_admin
def eliminar_especialidad():
    win = tk.Toplevel()
    win.title("Eliminar especialidad")
    win.geometry("400x200")
    win.resizable(False, False)

    frame = ttk.Frame(win, padding=20)
    frame.pack(fill="both", expand=True)

    ttk.Label(frame, text="ID o Nombre de la especialidad a eliminar:").pack()
    entry_val = tk.Entry(frame, width=35)
    entry_val.pack(pady=10)

    def eliminar():
        val = entry_val.get().strip()
        if not val:
            messagebox.showwarning("Falta dato", "Ingresa un ID o un nombre.")
            return

        if not messagebox.askyesno("Confirmar", "¿Seguro que deseas eliminar esta especialidad?"):
            return

        try:
            conn = get_conn()
            c = conn.cursor()
            c.execute("DELETE FROM especialidades WHERE es_clave = %s OR es_nombre = %s", (val, val))
            conn.commit()
            conn.close()

            messagebox.showinfo("OK", "Especialidad eliminada.")
            win.destroy()

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar:\n{e}")

    tk.Button(frame, text="Eliminar", bg="#ef5350", fg="white", command=eliminar).pack(pady=15)

def mostrar_especialidades():
    """Muestra todas las especialidades registradas en una tabla Tk."""
    from tkinter import ttk
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("SELECT es_clave, es_nombre FROM especialidades ORDER BY es_clave")

    filas = cur.fetchall()

    # Ventana
    win = tk.Toplevel()
    win.title("Listado de Especialidades")
    win.geometry("450x300")

    # Tabla
    tabla = ttk.Treeview(win, columns=("ID", "Nombre"), show="headings")
    tabla.heading("ID", text="ID")
    tabla.heading("Nombre", text="Nombre")
    tabla.column("ID", width=60)
    tabla.column("Nombre", width=300)
    tabla.pack(fill="both", expand=True)

    # Insertar datos
    for fila in filas:
        tabla.insert("", "end", values=fila)

    cur.close()
    conn.close()

def registrar_doctor_especialidad():
    win = tk.Toplevel()
    win.title("Asignar Especialidad a Doctor")
    win.geometry("430x260")

    tk.Label(win, text="Seleccione al doctor:", font=("Arial", 10, "bold")).pack(pady=5)

    cb_doctor = ttk.Combobox(win, state="readonly", width=40)
    cb_doctor.pack(pady=5)

    tk.Label(win, text="Seleccione la especialidad:", font=("Arial", 10, "bold")).pack(pady=5)

    cb_esp = ttk.Combobox(win, state="readonly", width=40)
    cb_esp.pack(pady=5)

    # --- CARGAR DOCTORES ---
    try:
        conn = get_conn()
        cur = conn.cursor()

        cur.execute("""
            SELECT us_clave, us_nombre, us_apellidos
            FROM usuarios
            WHERE LOWER(us_rol) = 'doctor'
        """)

        doctores = cur.fetchall()

        lista_doctores = [f"{d[0]} - {d[1]} {d[2]}" for d in doctores] if doctores else []
        cb_doctor["values"] = lista_doctores

        cur.close()
        conn.close()

        if not doctores:
            cb_doctor["values"] = ["(No hay doctores registrados)"]
            cb_doctor.current(0)
            return

    except Exception as e:
        messagebox.showerror("Error", f"No se pudieron cargar doctores:\n{e}")
        win.destroy()
        return

    # --- CARGAR ESPECIALIDADES ---
    try:
        conn = get_conn()
        cur = conn.cursor()

        cur.execute("SELECT es_clave, es_nombre FROM especialidades")
        especialidades = cur.fetchall()

        lista_esps = [f"{e[0]} - {e[1]}" for e in especialidades] if especialidades else []
        cb_esp["values"] = lista_esps

        cur.close()
        conn.close()

        if not especialidades:
            cb_esp["values"] = ["(No hay especialidades registradas)"]
            cb_esp.current(0)
            return

    except Exception as e:
        messagebox.showerror("Error", f"No se pudieron cargar especialidades:\n{e}")
        win.destroy()
        return

    # --- GUARDAR ASIGNACIÓN ---
    def guardar():
        d_sel = cb_doctor.get()
        e_sel = cb_esp.get()

        if not d_sel or not e_sel:
            messagebox.showwarning("Error", "Seleccione doctor y especialidad.")
            return

        try:
            doctor_id = int(d_sel.split(" - ")[0])
            esp_id = int(e_sel.split(" - ")[0])
        except:
            messagebox.showwarning("Error", "Selección inválida.")
            return

        try:
            conn = get_conn()
            cur = conn.cursor()

            # Verificar si ya existe la asignación
            cur.execute("""
                SELECT * FROM doctores_especialidades
                WHERE us_clave = %s AND es_clave = %s
            """, (doctor_id, esp_id))

            if cur.fetchone():
                messagebox.showinfo("Aviso", "Este doctor ya tiene esa especialidad.")
                cur.close()
                conn.close()
                return

            # Insertar relación
            cur.execute("""
                INSERT INTO doctores_especialidades (us_clave, es_clave)
                VALUES (%s, %s)
            """, (doctor_id, esp_id))

            conn.commit()
            cur.close()
            conn.close()

            messagebox.showinfo("OK", "Especialidad asignada correctamente.")
            win.destroy()

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo asignar la especialidad:\n{e}")

    tk.Button(win, text="Asignar especialidad", font=("Arial", 10), command=guardar).pack(pady=15)

def mostrar_doctores_por_especialidad():
    try:
        conn = get_conn()
        cursor = conn.cursor(dictionary=True)

        query = """
        SELECT 
            e.es_clave AS id_especialidad,
            e.es_nombre AS especialidad,
            u.us_clave AS id_doctor,
            u.us_nombre AS nombre_doctor,
            u.us_apellidos AS apellidos_doctor
        FROM especialidades e
        LEFT JOIN doctores_especialidades de ON e.es_clave = de.es_clave
        LEFT JOIN usuarios u ON de.us_clave = u.us_clave
        ORDER BY e.es_nombre ASC, u.us_apellidos ASC;
        """

        cursor.execute(query)
        resultados = cursor.fetchall()

        lb_output.delete(0, tk.END)

        if not resultados:
            lb_output.insert(tk.END, "No hay especialidades registradas.")
            return

        especialidad_actual = None

        for fila in resultados:
            if fila["especialidad"] != especialidad_actual:
                especialidad_actual = fila["especialidad"]
                lb_output.insert(tk.END, "")
                lb_output.insert(tk.END, f"Especialidad: {especialidad_actual}")
                lb_output.insert(tk.END, "----------------------------------------")

            if fila["id_doctor"] is None:
                lb_output.insert(tk.END, "   (Sin doctores asignados)")
            else:
                lb_output.insert(
                    tk.END,
                    f"   • {fila['nombre_doctor']} {fila['apellidos_doctor']} (ID: {fila['id_doctor']})"
                )

    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error al consultar:\n{e}")


# --- Consultas / Consulta (antes 'libros' en tu código) ---

def registrar_consulta():
    """Registrar una nueva consulta/cita con su propia ventana GUI."""
    win = tk.Toplevel()
    win.title("Registrar consulta")
    win.geometry("600x520")
    win.resizable(False, False)

    # ========== Cargar imágenes ==========
    img1 = Image.open("C:/Users/maryf/OneDrive/Escritorio/Imagenes Tópicos/Nexus_Care_LOGO_SOLO-removebg-preview.png")
    img1 = img1.resize((70, 70), Image.Resampling.LANCZOS)
    img1_tk = ImageTk.PhotoImage(img1)

    img2 = Image.open("C:/Users/maryf/OneDrive/Escritorio/Imagenes Tópicos/Nexus_Care-removebg-preview.png")
    img2 = img2.resize((220, 70), Image.Resampling.LANCZOS)
    img2_tk = ImageTk.PhotoImage(img2)

    frame_imgs = ttk.Frame(win)
    frame_imgs.pack(pady=20)

    ttk.Label(frame_imgs, image=img1_tk).pack(side="left", padx=10)
    ttk.Label(frame_imgs, image=img2_tk).pack(side="left", padx=10)

    # evitar que las imágenes se borren
    win.img1 = img1_tk
    win.img2 = img2_tk

    # ========== Formulario ==========
    frame = ttk.Frame(win, padding=20)
    frame.pack(fill="both", expand=True)

    resultado = {"consulta": None}

    # -------- CAMPOS --------
    ttk.Label(frame, text="Diagnóstico:").grid(row=0, column=0, sticky="w", pady=5)
    entry_diagnostico = tk.Entry(frame, width=35)
    entry_diagnostico.grid(row=0, column=1, padx=5, pady=5)

    ttk.Label(frame, text="Motivo de consulta:").grid(row=1, column=0, sticky="w", pady=5)
    entry_motivo = tk.Entry(frame, width=35)
    entry_motivo.grid(row=1, column=1, padx=5, pady=5)

    ttk.Label(frame, text="Hora (HH:MM):").grid(row=2, column=0, sticky="w", pady=5)
    entry_hora = tk.Entry(frame, width=35)
    entry_hora.grid(row=2, column=1, padx=5, pady=5)

    ttk.Label(frame, text="Fecha (YYYY-MM-DD):").grid(row=3, column=0, sticky="w", pady=5)
    entry_fecha = tk.Entry(frame, width=35)
    entry_fecha.grid(row=3, column=1, padx=5, pady=5)

    ttk.Label(frame, text="Tipo de Consulta: ").grid(row=4, column=0, sticky="w", pady=5)
    tipo_consulta = ttk.Combobox(frame, values=["Virtual", "Presencial"], state="readonly", width=32)
    tipo_consulta.grid(row=4, column=1, padx=5, pady=5)
    tipo_consulta.set("Virtual")

    ttk.Label(frame, text="ID Paciente:").grid(row=6, column=0, sticky="w", pady=5)
    entry_paciente = tk.Entry(frame, width=35)
    entry_paciente.grid(row=6, column=1, padx=5, pady=5)

    # ========== Funciones ==========
    def guardar():
        diagnostico = entry_diagnostico.get().strip()
        motivo = entry_motivo.get().strip()
        hora = entry_hora.get().strip()
        fecha = entry_fecha.get().strip()
        paciente = entry_paciente.get().strip()

        # Validaciones simples
        if not diagnostico:
            messagebox.showwarning("Falta diagnóstico", "El diagnóstico es obligatorio.")
            return

        if not motivo:
            messagebox.showwarning("Falta motivo", "El motivo es obligatorio.")
            return

        if not fecha:
            messagebox.showwarning("Falta fecha", "La fecha es obligatoria.")
            return

        if not paciente.isdigit():
            messagebox.showwarning("Paciente inválido", "El ID de paciente debe ser numérico.")
            return

        if current_user is None or current_user.role.lower() != "doctor":
            messagebox.showerror("Error", "Solo los doctores pueden registrar consultas.")
            return

        doctor = current_user.id
        virtual = str(tipo_consulta.get())
        try:
            c = Consulta.crear(
                diagnostico, motivo, hora, fecha,
                virtual, int(paciente), doctor
            )
            resultado["consulta"] = c

            messagebox.showinfo(
                "Consulta registrada",
                f"Consulta creada:\nID={c.id}\nDiagnóstico={c.diagnostico}"
            )
            win.destroy()

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo registrar la consulta:\n{e}")

    def cancelar():
        resultado["consulta"] = None
        win.destroy()

    # ========== Botones ==========
    btn_frame = ttk.Frame(frame)
    btn_frame.grid(row=8, column=0, columnspan=2, pady=20)

    tk.Button(
        btn_frame, text="Registrar",
        foreground="white",
        font=("Arial", 9, "bold"),
        relief="raised",
        bd=4,
        activebackground="#4fb0ff",
        background="#3a7bd5",
        command=guardar
    ).pack(side="left", padx=10)

    tk.Button(
        btn_frame, text="Cancelar",
        font=("Arial", 9, "bold"),
        relief="raised",
        bd=4,
        background="#ef5350",
        activebackground="#e57373",
        foreground="white",
        command=cancelar
    ).pack(side="left", padx=10)

    # Modal
    win.grab_set()
    win.focus_set()
    win.wait_window()

    return resultado["consulta"]

def modificar_consulta():
    win = tk.Toplevel()
    win.title("Modificar consulta")
    win.geometry("550x420")
    win.resizable(False, False)

    # ======== Cargar imágenes ========
    img1 = Image.open("C:/Users/maryf/OneDrive/Escritorio/Imagenes Tópicos/Nexus_Care_LOGO_SOLO-removebg-preview.png")
    img1 = img1.resize((70, 70), Image.Resampling.LANCZOS)
    img1_tk = ImageTk.PhotoImage(img1)

    img2 = Image.open("C:/Users/maryf/OneDrive/Escritorio/Imagenes Tópicos/Nexus_Care-removebg-preview.png")
    img2 = img2.resize((220, 70), Image.Resampling.LANCZOS)
    img2_tk = ImageTk.PhotoImage(img2)

    frame_imgs = ttk.Frame(win)
    frame_imgs.pack(pady=20)

    ttk.Label(frame_imgs, image=img1_tk).pack(side="left", padx=10)
    ttk.Label(frame_imgs, image=img2_tk).pack(side="left", padx=10)

    win.img1_tk = img1_tk
    win.img2_tk = img2_tk

    # ======== Formulario ========
    frame = ttk.Frame(win, padding=20)
    frame.pack(fill="both", expand=True)

    # --- Buscar consulta ---
    ttk.Label(frame, text="ID de la consulta a modificar:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
    entry_id = tk.Entry(frame, width=35, highlightthickness=2, highlightbackground="#5F9BE0")
    entry_id.grid(row=0, column=1, padx=5, pady=5)

    # Campo para fecha
    ttk.Label(frame, text="Nueva fecha (YYYY-MM-DD):").grid(row=1, column=0, sticky="w", padx=5, pady=15)
    entry_fecha = tk.Entry(frame, width=35, highlightthickness=2, highlightbackground="#5F9BE0")
    entry_fecha.grid(row=1, column=1, padx=5, pady=15)

    entry_fecha.config(state="disabled")  # deshabilitado hasta cargar

    # ---------------- BUSCAR CONSULTA ----------------
    def buscar():
        id_val = entry_id.get().strip()
        if not id_val.isdigit():
            messagebox.showwarning("Aviso", "Ingrese un ID numérico válido.")
            return

        consulta = Consulta.buscar_por_id(int(id_val))
        if consulta is None:
            messagebox.showwarning("No encontrado", "Consulta no encontrada.")
            return

        win.consulta_actual = consulta

        entry_fecha.config(state="normal")
        entry_fecha.delete(0, tk.END)
        entry_fecha.insert(0, str(consulta.ci_fecha))

        messagebox.showinfo("OK", "Consulta cargada correctamente.")

    tk.Button(
        frame, text="Buscar",
        background="#3a7bd5", activebackground="#5ba8f5",
        foreground="white", font=("Arial", 8, "bold"),
        relief="raised", bd=4,
        command=buscar
    ).grid(row=0, column=2, padx=10)

    # ---------------- MODIFICAR CONSULTA ----------------
    def guardar():
        if not hasattr(win, "consulta_actual"):
            messagebox.showwarning("Aviso", "Debe buscar una consulta primero.")
            return

        nueva_fecha = entry_fecha.get().strip()
        if not nueva_fecha:
            messagebox.showwarning("Aviso", "Debe ingresar una fecha.")
            return

        try:
            conn = __import__('db_connection').get_conn()
            cur = conn.cursor()

            cur.execute(
                "UPDATE consultas SET co_fecha=%s WHERE co_clave=%s",
                (nueva_fecha, win.consulta_actual.id)
            )

            conn.commit()
            cur.close()
            conn.close()

            messagebox.showinfo("OK", "Consulta modificada correctamente.")
            listar_consultas()
            win.destroy()

        except Exception as e:
            messagebox.showerror("Error", f"Error al modificar consulta:\n{e}")

    tk.Button(
        frame, text="Guardar cambios",
        background="#3a7bd5", activebackground="#5ba8f5",
        foreground="white", font=("Arial", 9, "bold"),
        relief="raised", bd=4,
        command=guardar
    ).grid(row=3, column=0, columnspan=3, pady=20)


def actualizar_lista_consultas(listbox_consultas):
    """Limpia el Listbox de consultas y lo rellena con los datos actualizados de la DB."""
    
    listbox_consultas.delete(0, tk.END)
    
    consultas = bib.listar_consultas()
    
    for consulta in consultas:
        texto = (
            f"ID: {consulta.id} | Fecha: {consulta.fecha} | Hora: {consulta.hora} | "
            f"Paciente: {consulta.nombre_paciente} | Doctor ID: {consulta.doctor} | "
            f"Tipo: {consulta.tipo_consulta} | Estado: {consulta.estado}"
        )
        listbox_consultas.insert(tk.END, texto)


def eliminar_consulta():
    win = tk.Toplevel()
    win.title("Eliminar consulta")
    win.geometry("420x180")
    win.resizable(False, False)

    tk.Label(win, text="Eliminar consulta", font=("Arial", 14, "bold")).pack(pady=10)

    frame = tk.Frame(win)
    frame.pack(pady=10)

    tk.Label(frame, text="ID de la consulta:").grid(row=0, column=0, padx=5, pady=5)
    entry_id = tk.Entry(frame)
    entry_id.grid(row=0, column=1, padx=5, pady=5)

    def eliminar():
        try:
            id_cons = int(entry_id.get().strip())
        except ValueError:
            messagebox.showerror("Error", "El ID debe ser un número entero.")
            return

        if not messagebox.askyesno("Confirmar", f"¿Eliminar la consulta con ID = {id_cons}?"):
            return

        try:
            conn = __import__('db_connection').get_conn()
            cur = conn.cursor()
            cur.execute("DELETE FROM consultas WHERE co_clave = %s", (id_cons,))
            conn.commit()
            cur.close()
            conn.close()

            messagebox.showinfo("OK", f"Consulta con ID {id_cons} eliminada.")
            win.destroy()

            # Refrescar lista en tu GUI principal
            listar_consultas()

        except Exception as e:
            messagebox.showerror("Error", f"Error al eliminar consulta:\n{e}")

    tk.Button(win, text="Eliminar", bg="#c0392b", fg="white",
              font=("Arial", 12), width=12, command=eliminar).pack(pady=5)

    tk.Button(win, text="Cerrar", width=12, command=win.destroy).pack()

    return win

# --- Listados / Agendado (médico y admin) ---

def listar_usuarios():
    try:
        conn = get_conn()
        cur = conn.cursor()

        # Si el usuario conectado es doctor → solo pacientes
        if current_user.role.lower() == "doctor":
            cur.execute("""
                SELECT us_clave, us_nombre, us_apellidos, us_correo, us_telefono, us_rol
                FROM usuarios
                WHERE us_rol = 'Paciente'
            """)
        else:
            # Admin y otros ven todo
            cur.execute("""
                SELECT us_clave, us_nombre, us_apellidos, us_correo, us_telefono, us_rol
                FROM usuarios
            """)

        usuarios = cur.fetchall()
        cur.close()
        conn.close()

        lb_output.delete(0, tk.END)
        lb_output.insert(tk.END, "Usuarios:")

        for u in usuarios:
            uid, nombre, apellidos, correo, telefono, rol = u
            lb_output.insert(tk.END, "")
            lb_output.insert(tk.END, f"[{uid}] {nombre} {apellidos} — {rol} —  {correo} — {telefono}")

    except Exception as e:
        messagebox.showerror("Error", f"Error al listar usuarios:\n{e}")


def listar_consultas():
    try:
        consultas = Consulta.listar_todos()
        lb_output.delete(0, tk.END)
        if not consultas:
            lb_output.insert(tk.END, "No hay consultas registradas.")
            return
        lb_output.insert(tk.END, "Consultas:")
        for c in consultas:
            status = "Disponible" if c.motivo else "No disponible"
            lb_output.insert(tk.END, "")
            lb_output.insert(tk.END, f"  [{c.id}] - ID del paciente: {c.paciente} - Nombre del Paciente: {c.nombre_paciente} - Fecha: {c.fecha} - Estado: ({status}) - Motivo: {c.motivo}")
    except Exception as e:
        messagebox.showerror("Error", f"Error al listar consultas:\n{e}")


def obtener_consultas_usuario():
    nombre = simpledialog.askstring("Consultas agendadas", "Nombre del usuario:")
    if not nombre:
        return
    try:
        usuario = Usuario.buscar_por_nombre(nombre.strip())
        if usuario is None:
            messagebox.showwarning("No encontrado", "Usuario no encontrado.")
            return
        # asumimos que Usuario tiene método obtener_libros_prestados adaptado; si no, mostramos mensaje simple
        try:
            Consulta = usuario.obtener_libros_prestados()
            lb_output.delete(0, tk.END)
            lb_output.insert(tk.END, f"Consultas agendadas a {usuario.nombre}:")
            if not Consulta:
                lb_output.insert(tk.END, "  (No tiene consultas agendadas)")
                return
            for l in Consulta:
                lb_output.insert(tk.END, f"  [{l.id}] {l.ci_especialidad} — {l.ci_fecha}")
        except Exception:
            lb_output.delete(0, tk.END)
            lb_output.insert(tk.END, "Funcionalidad de obtener consultas del usuario no implementada en Usuario.")
    except Exception as e:
        messagebox.showerror("Error", f"Error al obtener consultas del usuario:\n{e}")


def salir():
    root.destroy()
    sys.exit(0)

def ver_consultas_paciente():
    """Muestra las consultas próximas del paciente conectado."""
    if current_user is None or current_user.role.lower() != "paciente":
        messagebox.showerror("Permisos", "Solo los pacientes pueden ver sus consultas.")
        return

    win = tk.Toplevel()
    win.title("Mis consultas")
    win.geometry("600x400")

    ttk.Label(win, text=f"Consultas próximas de: {current_user.nombre}",
              font=("Arial", 12, "bold")).pack(pady=10)

    tree = ttk.Treeview(win, columns=("fecha", "hora", "doctor"), show="headings", height=12)
    tree.pack(fill="both", expand=True, padx=10, pady=10)

    tree.heading("fecha", text="Fecha")
    tree.heading("hora", text="Hora")
    tree.heading("doctor", text="Doctor")

    # Obtener consultas desde la BD
    consultas = ConsultaPaciente.obtener_por_paciente(current_user.id)

    if not consultas:
        messagebox.showinfo("Sin consultas", "No tienes consultas próximas.")
        return

    for c in consultas:
        tree.insert("", "end", values=(c.fecha, c.hora, c.doctor))

@requiere_admin
def grafica_roles_usuarios():
    import matplotlib.pyplot as plt
    from usuarios import Usuario

    # Obtener todos los usuarios desde la BD
    lista = Usuario.listar_todos()

    # Contadores por rol
    roles = {"Paciente": 0, "Doctor": 0, "Admin": 0}

    for u in lista:
        rol = (u.role or "").capitalize()
        if rol in roles:
            roles[rol] += 1

    # Crear gráfica
    plt.figure(figsize=(6, 4))
    plt.bar(roles.keys(), roles.values())
    plt.title("Cantidad de usuarios por rol")
    plt.xlabel("Roles")
    plt.ylabel("Cantidad")
    plt.grid(axis="y", linestyle="--", alpha=0.6)

    plt.show()




def ajustar_menu_por_rol():
    """Habilita/deshabilita opciones del menú según el rol del usuario actual."""
    if current_user is None:
        # deshabilitar todo por seguridad
        acciones_menu.entryconfig("Registrar usuario", state="disabled")
        acciones_menu.entryconfig("Registrar consulta", state="disabled")
        acciones_menu.entryconfig("Mostrar usuarios", state="disabled")
        acciones_menu.entryconfig("Mostrar consultas", state="disabled")
        acciones_menu.entryconfig("Agendar consulta", state="disabled")
        acciones_menu.entryconfig("Cancelar agenda", state="disabled")
        acciones_menu.entryconfig("Consultas (usuario)", state="disabled")
        return

    if (current_user.role or "").lower() == 'admin':
        acciones_menu.entryconfig("Gráfica de usuarios por rol", state="normal")
    else:
        acciones_menu.entryconfig("Gráfica de usuarios por rol", state="disabled")

    if (current_user.role or "").lower() == 'admin':
        # Admin: habilitar todo
        acciones_menu.entryconfig("Registrar usuario", state="normal")
        acciones_menu.entryconfig("Modificar usuario", state="normal")
        acciones_menu.entryconfig("Eliminar usuario", state="normal")
        acciones_menu.entryconfig("Registrar consulta", state="disabled")
        acciones_menu.entryconfig("Modificar consulta", state="disabled")
        acciones_menu.entryconfig("Eliminar consulta", state="disabled")
        acciones_menu.entryconfig("Mostrar usuarios", state="normal")
        acciones_menu.entryconfig("Mostrar consultas", state="normal")
        acciones_menu.entryconfig("Registrar especialidad", state="normal")
        acciones_menu.entryconfig("Modificar especialidad", state="normal")
        acciones_menu.entryconfig("Eliminar especialidad", state="normal")
        acciones_menu.entryconfig("Mostrar especialidades", state="normal")    
    else:
        # doctor o paciente: permisos limitados
        acciones_menu.entryconfig("Registrar usuario", state="disabled")
        acciones_menu.entryconfig("Modificar usuario", state="disabled")
        acciones_menu.entryconfig("Eliminar usuario", state="disabled")
        acciones_menu.entryconfig("Registrar consulta", state="normal")
        acciones_menu.entryconfig("Modificar consulta", state="normal")
        acciones_menu.entryconfig("Eliminar consulta", state="disabled")
        # doctor puede agendar/cancelar y ver usuarios; paciente solo ver y agendar/cancelar sus consultas
        if (current_user.role or "").lower() == 'doctor':
            acciones_menu.entryconfig("Mostrar usuarios", state="normal")
            acciones_menu.entryconfig("Mostrar consultas", state="normal")
            acciones_menu.entryconfig("Eliminar consulta", state="normal")
            acciones_menu.entryconfig("Registrar especialidad", state="disabled")
            acciones_menu.entryconfig("Modificar especialidad", state="disabled")
            acciones_menu.entryconfig("Eliminar especialidad", state="disabled")
            acciones_menu.entryconfig("Mostrar especialidades", state="disabled") 
            acciones_menu.entryconfig("Asignar especialidad a doctor", state="disabled")
            acciones_menu.entryconfig("Mostrar Doctores en Especialidades", state="disabled") 
            acciones_menu.entryconfig("Mis consultas", state="disabled")
        if current_user.role.lower() == "paciente":
            acciones_menu.entryconfig("Mis consultas", state="normal")
            acciones_menu.entryconfig("Registrar consulta", state="disabled")
            acciones_menu.entryconfig("Modificar consulta", state="disabled")
            acciones_menu.entryconfig("Mostrar usuarios", state="disabled")
            acciones_menu.entryconfig("Mostrar consultas", state="disabled")
            acciones_menu.entryconfig("Registrar especialidad", state="disabled")
            acciones_menu.entryconfig("Modificar especialidad", state="disabled")
            acciones_menu.entryconfig("Eliminar especialidad", state="disabled")
            acciones_menu.entryconfig("Mostrar especialidades", state="disabled") 
            acciones_menu.entryconfig("Asignar especialidad a doctor", state="disabled")
            acciones_menu.entryconfig("Mostrar Doctores en Especialidades", state="disabled")
# --- Interfaz principal (ventana) ---
root = tk.Tk()
root.title("Nexus Care - Interfaz gráfica")
root.geometry("800x480")
root.minsize(700, 420)

# Menú principal
menubar = tk.Menu(root)

# Menú "Acciones" con las opciones (adaptado a consultas)
acciones_menu = tk.Menu(menubar, tearoff=0)
acciones_menu.add_command(label="Registrar usuario", command=registrar_usuario)
acciones_menu.add_command(label="Modificar usuario", command=modificar_usuario)
acciones_menu.add_command(label="Eliminar usuario", command=eliminar_usuario)
acciones_menu.add_separator()
acciones_menu.add_command(label="Registrar especialidad", command=agregar_especialidad)
acciones_menu.add_command(label="Modificar especialidad", command=modificar_especialidad)
acciones_menu.add_command(label="Eliminar especialidad", command=eliminar_especialidad)
acciones_menu.add_command(label="Mostrar especialidades", command=mostrar_especialidades)
acciones_menu.add_command(label="Asignar especialidad a doctor", command=registrar_doctor_especialidad)
acciones_menu.add_command(label="Mostrar Doctores en Especialidades", command=mostrar_doctores_por_especialidad)
acciones_menu.add_separator()
acciones_menu.add_command(label="Registrar consulta", command=registrar_consulta)
acciones_menu.add_command(label="Modificar consulta", command=modificar_consulta)
acciones_menu.add_command(label="Eliminar consulta", command=eliminar_consulta)
acciones_menu.add_separator()
acciones_menu.add_command(label="Mostrar usuarios", command=listar_usuarios)
acciones_menu.add_command(label="Mostrar consultas", command=listar_consultas)
acciones_menu.add_separator()
acciones_menu.add_command(label="Mis consultas", command=ver_consultas_paciente)
acciones_menu.add_separator()
acciones_menu.add_command(label="Gráfica de usuarios por rol",command=grafica_roles_usuarios)
menubar.add_cascade(label="Acciones", menu=acciones_menu)

# Menú "Archivo" con Salir
archivo_menu = tk.Menu(menubar, tearoff=0)
archivo_menu.add_command(label="Salir", command=salir)
menubar.add_cascade(label="Archivo", menu=archivo_menu)

root.config(menu=menubar)

# Frame principal para salida / resultados
frame_output = ttk.Frame(root, padding=(12, 12))
frame_output.pack(side=tk.TOP, expand=True, fill=tk.BOTH)

# Imagen al lado del label "Salida" --------
# Cargar imagen
img_salida = Image.open("C:/Users/maryf/OneDrive/Escritorio/Imagenes Tópicos/Nexus_Care_LOGO_SOLO-removebg-preview.png")
img_salida = img_salida.resize((70, 70), Image.Resampling.LANCZOS)
img_salida_tk = ImageTk.PhotoImage(img_salida)

img_salida2 = Image.open("C:/Users/maryf/OneDrive/Escritorio/Imagenes Tópicos/Nexus_Care-removebg-preview.png")
img_salida2 = img_salida2.resize((220, 70), Image.Resampling.LANCZOS)
img_salida2_tk = ImageTk.PhotoImage(img_salida2)

#Frame Contenedor
contenedor = ttk.Frame(frame_output)
contenedor.pack(anchor="center")

# --- Imagen 1 ---
lbl_img1 = ttk.Label(contenedor, image=img_salida_tk)
lbl_img1.pack(side="left", padx=(0, 4))

# --- Imagen 2 ---
lbl_img2 = ttk.Label(contenedor, image=img_salida2_tk)
lbl_img2.pack(side="left", padx=(0, 4))

# MUY IMPORTANTE: guardar referencia para que no se borre
frame_output.img_salida_tk = img_salida_tk
frame_output.img_salida2_tk = img_salida2_tk

# --- Texto "Salida" ---
lbl_output = ttk.Label(
    contenedor,
    font=("Segoe UI", 16, "bold")
)
lbl_output.pack(side="left", padx=4)


# Listbox con scrollbar para mostrar resultados
frame_list = ttk.Frame(frame_output)
frame_list.pack(fill=tk.BOTH, expand=True, pady=(6, 0))

sb = ttk.Scrollbar(frame_list, orient=tk.VERTICAL)
lb_output = tk.Listbox(frame_list, yscrollcommand=sb.set, font=("Consolas", 10))
sb.config(command=lb_output.yview)
sb.pack(side=tk.RIGHT, fill=tk.Y)
lb_output.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Mensaje de ayuda inferior
lbl_help = ttk.Label(frame_output, text="Iniciando...", font=("Segoe UI", 9))
lbl_help.pack(anchor="w", pady=(8, 0))

# Al iniciar, pedir login
root.after(100, login_inicial)

root.mainloop()
