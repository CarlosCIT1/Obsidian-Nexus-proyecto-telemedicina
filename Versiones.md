import sys
from db_connection import get_conn
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from PIL import Image, ImageTk
from medicos import NexusCare
from usuarios import Usuario, hash_password
from citas import Consulta

bib = NexusCare()
current_user = None  # objeto Usuario autenticado

# --------------------------
# Funciones de la aplicación
# --------------------------


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

    ttk.Label(frame, text="Usuario / correo:").grid(row=0, column=0, sticky="w", pady=5)
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
        win.destroy()

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
        # telefono puede ser opcional en la BD (es NULLABLE) — lo dejamos aceptar vacío
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

    # Rol
    ttk.Label(frame, text="Rol:").grid(row=3, column=0, sticky="w", padx=5, pady=5)
    cb_role = ttk.Combobox(frame, values=["Paciente", "Doctor", "Admin"], state="readonly", width=32)
    cb_role.grid(row=3, column=1, padx=5, pady=5)
    cb_role.set("Paciente")

    # Contraseña
    ttk.Label(frame, text="Contraseña:").grid(row=4, column=0, sticky="w", padx=5, pady=5)
    entry_pwd = tk.Entry(frame, highlightthickness=2, highlightbackground="#5F9BE0", highlightcolor="green", show="*", width=35)
    entry_pwd.grid(row=4, column=1, padx=5, pady=5)

    # ========== BOTONES ==========
    def guardar():
        nombre = entry_nombre.get().strip()
        apellidos = entry_apellidos.get().strip()
        correo = entry_correo.get().strip()
        role = cb_role.get().strip()
        pwd = entry_pwd.get()

        if not nombre:
            messagebox.showwarning("Falta nombre", "El nombre es obligatorio.")
            return

        if not correo:
            messagebox.showwarning("Falta correo", "El correo es obligatorio.")
            return

        try:
            u = Usuario.crear(
                nombre,
                apellidos,
                correo,
                None,              # teléfono nulo
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
    btn_frame.grid(row=5, column=0, columnspan=2, pady=20)

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
    labels = ["Nombre", "Apellidos", "Correo", "Rol (Paciente/Doctor/Admin)", "Contraseña (opcional)"]
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
        entradas["Rol (Paciente/Doctor/Admin)"].delete(0, tk.END); entradas["Rol (Paciente/Doctor/Admin)"].insert(0, usr.role)
        entradas["Contraseña (opcional)"].delete(0, tk.END)

        messagebox.showinfo("OK", "Usuario cargado.")

    tk.Button(
        frame, text="Buscar",
        background="#3a7bd5", activebackground="#5ba8f5",
        foreground="white", font=("Arial", 8, "bold"),
        relief="raised", bd=4,
        command=buscar_usuario
    ).grid(row=1, column=2, padx=10)

    # ---------- Guardar cambios ----------
    def guardar_cambios():
        if not hasattr(win, "usr_actual"):
            messagebox.showwarning("Aviso", "Debe buscar un usuario primero.")
            return

        usr = win.usr_actual
        nuevo_nombre = entradas["Nombre"].get().strip()
        nuevo_apellidos = entradas["Apellidos"].get().strip()
        nuevo_correo = entradas["Correo"].get().strip()
        nuevo_role = entradas["Rol (Paciente/Doctor/Admin)"].get().strip()
        nueva_pwd = entradas["Contraseña (opcional)"].get().strip()

        try:
            conn = get_conn()
            cur = conn.cursor()

            if nueva_pwd:
                cur.execute("""
                    UPDATE usuarios 
                    SET us_nombre=%s, us_apellidos=%s, us_correo=%s, us_rol=%s, us_contrasena=%s
                    WHERE us_clave=%s
                """, (nuevo_nombre, nuevo_apellidos, nuevo_correo, nuevo_role, hash_password(nueva_pwd), usr.id))
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
        win.geometry("500x300")
        win.resizable(False, False)

        # ======== Cargar imágenes ========
        img_s1 = Image.open("C:/Users/maryf/OneDrive/Escritorio/Imagenes Tópicos/Nexus_Care_LOGO_SOLO-removebg-preview.png")
        img_s1 = img_s1.resize((70, 70), Image.Resampling.LANCZOS)
        img_s1_tk = ImageTk.PhotoImage(img_s1)

        frame_imgs = ttk.Frame(win)
        frame_imgs.pack(pady=20)

        ttk.Label(frame_imgs, image=img_s1_tk).pack()
        win.img1 = img_s1_tk

        frame = ttk.Frame(win, padding=20)
        frame.pack()

        ttk.Label(frame, text="Nombre del usuario a eliminar:").grid(row=0, column=0, padx=5, pady=5)
        entry_nombre = tk.Entry(frame, width=35, highlightthickness=2, highlightbackground="#5F9BE0")
        entry_nombre.grid(row=0, column=1, padx=5, pady=5)

        def eliminar():
            nombre = entry_nombre.get().strip()
            if not nombre:
                messagebox.showwarning("Aviso", "Ingrese un nombre.")
                return

            usr = Usuario.buscar_por_nombre(nombre)
            if usr is None:
                messagebox.showerror("Error", "Usuario no encontrado.")
                return

            if not messagebox.askyesno("Confirmar", f"¿Eliminar a '{usr.nombre}' (id={usr.id})?"):
                return

            try:
                conn = get_conn()
                cur = conn.cursor()

                cur.execute("DELETE FROM usuarios WHERE us_clave=%s", (usr.id,))
                conn.commit()
                cur.close()
                conn.close()

                messagebox.showinfo("OK", "Usuario eliminado correctamente.")
                listar_usuarios()
                win.destroy()

            except Exception as e:
                messagebox.showerror("Error", f"{e}")

        tk.Button(
            frame, text="Eliminar",
            background="#ef5350", activebackground="#e57373",
            foreground="white", font=("Arial", 8, "bold"),
            relief="raised", bd=4,
            command=eliminar
        ).grid(row=1, column=0, columnspan=2, pady=20)


# --- Consultas / Consulta (antes 'libros' en tu código) ---

@requiere_admin
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

    ttk.Label(frame, text="¿Es virtual? (0/1):").grid(row=4, column=0, sticky="w", pady=5)
    cb_virtual = ttk.Combobox(frame, values=["0", "1"], state="readonly", width=32)
    cb_virtual.grid(row=4, column=1, padx=5, pady=5)
    cb_virtual.set("0")

    ttk.Label(frame, text="¿Es presencial? (0/1):").grid(row=5, column=0, sticky="w", pady=5)
    cb_presencial = ttk.Combobox(frame, values=["0", "1"], state="readonly", width=32)
    cb_presencial.grid(row=5, column=1, padx=5, pady=5)
    cb_presencial.set("1")

    ttk.Label(frame, text="ID Paciente:").grid(row=6, column=0, sticky="w", pady=5)
    entry_paciente = tk.Entry(frame, width=35)
    entry_paciente.grid(row=6, column=1, padx=5, pady=5)

    ttk.Label(frame, text="ID Doctor:").grid(row=7, column=0, sticky="w", pady=5)
    entry_doctor = tk.Entry(frame, width=35)
    entry_doctor.grid(row=7, column=1, padx=5, pady=5)

    # ========== Funciones ==========
    def guardar():
        diagnostico = entry_diagnostico.get().strip()
        motivo = entry_motivo.get().strip()
        hora = entry_hora.get().strip()
        fecha = entry_fecha.get().strip()
        paciente = entry_paciente.get().strip()
        doctor = entry_doctor.get().strip()

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

        if not doctor.isdigit():
            messagebox.showwarning("Doctor inválido", "El ID de doctor debe ser numérico.")
            return

        virtual = int(cb_virtual.get())
        presencial = int(cb_presencial.get())

        try:
            c = Consulta.crear(
                diagnostico, motivo, hora, fecha,
                virtual, presencial, int(paciente), int(doctor)
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

@requiere_admin
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

@requiere_admin
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
        usuarios = Usuario.listar_todos()
        lb_output.delete(0, tk.END)
        if not usuarios:
            lb_output.insert(tk.END, "No hay usuarios registrados.")
            return
        lb_output.insert(tk.END, "Usuarios:")
        for u in usuarios:
            lb_output.insert(tk.END, f"  [{u.id}] {u.nombre} {u.apellidos} — {u.role}")
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
            status = "Disponible" if c.ci_motivo else "No disponible"
            lb_output.insert(tk.END, f"  [{c.id}] {c.ci_especialidad} — {c.ci_fecha} ({status})")
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
        # Admin: habilitar todo
        acciones_menu.entryconfig("Registrar usuario", state="normal")
        acciones_menu.entryconfig("Modificar usuario", state="normal")
        acciones_menu.entryconfig("Eliminar usuario", state="normal")
        acciones_menu.entryconfig("Registrar consulta", state="normal")
        acciones_menu.entryconfig("Modificar consulta", state="normal")
        acciones_menu.entryconfig("Eliminar consulta", state="normal")
        acciones_menu.entryconfig("Mostrar usuarios", state="normal")
        acciones_menu.entryconfig("Mostrar consultas", state="normal")
        acciones_menu.entryconfig("Consultas (usuario)", state="normal")
    else:
        # doctor o paciente: permisos limitados
        acciones_menu.entryconfig("Registrar usuario", state="disabled")
        acciones_menu.entryconfig("Modificar usuario", state="disabled")
        acciones_menu.entryconfig("Eliminar usuario", state="disabled")
        acciones_menu.entryconfig("Registrar consulta", state="disabled")
        acciones_menu.entryconfig("Modificar consulta", state="disabled")
        acciones_menu.entryconfig("Eliminar consulta", state="disabled")
        # doctor puede agendar/cancelar y ver usuarios; paciente solo ver y agendar/cancelar sus consultas
        if (current_user.role or "").lower() == 'doctor':
            acciones_menu.entryconfig("Agendar consulta", state="normal")
            acciones_menu.entryconfig("Cancelar agenda", state="normal")
            acciones_menu.entryconfig("Mostrar usuarios", state="normal")
            acciones_menu.entryconfig("Mostrar consultas", state="normal")
            acciones_menu.entryconfig("Consultas (usuario)", state="normal")
        else:  # Paciente u otros
            acciones_menu.entryconfig("Agendar consulta", state="normal")
            acciones_menu.entryconfig("Cancelar agenda", state="normal")
            acciones_menu.entryconfig("Mostrar usuarios", state="disabled")
            acciones_menu.entryconfig("Mostrar consultas", state="normal")
            acciones_menu.entryconfig("Consultas (usuario)", state="normal")


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
acciones_menu.add_command(label="Registrar consulta", command=registrar_consulta)
acciones_menu.add_command(label="Modificar consulta", command=modificar_consulta)
acciones_menu.add_command(label="Eliminar consulta", command=eliminar_consulta)
acciones_menu.add_separator()
acciones_menu.add_command(label="Mostrar usuarios", command=listar_usuarios)
acciones_menu.add_command(label="Mostrar consultas", command=listar_consultas)
acciones_menu.add_separator()
acciones_menu.add_command(label="Consultas (usuario)", command=obtener_consultas_usuario)
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
