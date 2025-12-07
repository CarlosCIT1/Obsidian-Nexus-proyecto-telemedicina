# Versionamiento-POO
Se suben las versiones que se han tenido en base al código del proyecto integrador
import sys
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from PIL import Image, ImageTk
from nexus_care import NexusCare
from usuarios import Usuario, hash_password  # si necesitas el hash
from citas import Citas

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
    entry_user = tk.Entry(frame, width=35)
    entry_user.grid(row=0, column=1, pady=5)

    ttk.Label(frame, text="Contraseña:").grid(row=1, column=0, sticky="w", pady=5)
    entry_pwd = tk.Entry(frame, width=35, show="*")
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
        global current_user
        current_user = resultado["user"]
        lbl_help.config(text=f"Usuario conectado: {current_user.nombre} ({current_user.role})")
        ajustar_menu_por_rol()
        listar_libros()



def requiere_admin(func):
    """Decorador simple para funciones que requieren rol 'Admin'."""
    def wrapper(*args, **kwargs):
        if current_user is None or current_user.role != 'Admin':
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
    ttk.Label(frame, text="Fecha de nacimiento:").grid(row=4, column=0, sticky="w", padx=5, pady=5)
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
            return

        apellidos = entry_apellidos.get().strip()
        if not apellidos:
            return
        
        correo = entry_correo.get().strip()
        if not correo:
            return
        
        telefono = entry_telefono.get().strip()
        if not telefono:
            return
        
        fechanac = entry_fechanac.get().strip()
        if not fechanac:
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

        u = Usuario.crear(nombre, apellidos, correo, telefono, fechanac, sexo, role, pwd)
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
    nombre = simpledialog.askstring("Registrar usuario", "Nombre del usuario:")
    if not nombre:
        return
    role = simpledialog.askstring("Registrar usuario", "Rol (admin/médico):", initialvalue="médico")
    pwd = simpledialog.askstring("Registrar usuario", "Contraseña:", show='*')
    try:
        u = bib.registrar_usuario(nombre.strip()) if role is None and pwd is None else None
        # Si se pasó role/ pwd usamos Usuario.crear directamente
        if u is None:
            u = Usuario.crear(nombre.strip(), role.strip() if role else 'médico', pwd)
        messagebox.showinfo("OK", f"Usuario registrado: {u.nombre} (id={u.id})")
        listar_usuarios()
    except Exception as e:
        messagebox.showerror("Error", f"Error al registrar usuario:\n{e}")

@requiere_admin
def modificar_usuario():
    nombre = simpledialog.askstring("Modificar usuario", "Nombre del usuario a modificar:")
    if not nombre:
        return
    usr = bib.buscar_usuario(nombre.strip())
    if usr is None:
        messagebox.showwarning("No encontrado", "Usuario no encontrado.")
        return
    nuevo_nombre = simpledialog.askstring("Modificar usuario", "Nuevo nombre:", initialvalue=usr.nombre)
    nuevo_role = simpledialog.askstring("Modificar usuario", "Nuevo rol (admin/médico):", initialvalue=usr.role)
    nueva_pwd = simpledialog.askstring("Modificar usuario", "Nueva contraseña (vacío = sin cambio):", show='*')
    try:
        conn = __import__('db_connection').get_conn()
        cur = conn.cursor()
        if nueva_pwd:
            from usuarios import hash_password
            cur.execute("UPDATE usuarios SET us_nombre=%s, us_role=%s, us_password=%s WHERE us_clave=%s",
                        (nuevo_nombre.strip(), nuevo_role.strip(), hash_password(nueva_pwd), usr.id))
        else:
            cur.execute("UPDATE usuarios SET us_nombre=%s, us_role=%s WHERE us_clave=%s",
                        (nuevo_nombre.strip(), nuevo_role.strip(), usr.id))
        conn.commit()
        cur.close()
        conn.close()
        messagebox.showinfo("OK", "Usuario modificado.")
        listar_usuarios()
    except Exception as e:
        messagebox.showerror("Error", f"Error al modificar usuario:\n{e}")

@requiere_admin
def eliminar_usuario():
    nombre = simpledialog.askstring("Eliminar usuario", "Nombre del usuario a eliminar:")
    if not nombre:
        return
    usr = bib.buscar_usuario(nombre.strip())
    if usr is None:
        messagebox.showwarning("No encontrado", "Usuario no encontrado.")
        return
    if messagebox.askyesno("Confirmar", f"¿Eliminar al usuario '{usr.nombre}' (id={usr.id})?"):
        try:
            conn = __import__('db_conection').get_conn()
            cur = conn.cursor()
            cur.execute("DELETE FROM usuarios WHERE id = %s", (usr.id,))
            conn.commit()
            cur.close()
            conn.close()
            messagebox.showinfo("OK", "Usuario eliminado.")
            listar_usuarios()
        except Exception as e:
            messagebox.showerror("Error", f"Error al eliminar usuario:\n{e}")

@requiere_admin
def registrar_libro():
    titulo = simpledialog.askstring("Registrar libro", "Título del libro:")
    if not titulo:
        return
    autor = simpledialog.askstring("Registrar libro", "Autor del libro:")
    if not autor:
        return
    try:
        l = bib.registrar_libro(titulo.strip(), autor.strip())
        messagebox.showinfo("OK", f"Libro registrado: {l.titulo} (id={l.id})")
        listar_libros()
    except Exception as e:
        messagebox.showerror("Error", f"Error al registrar libro:\n{e}")

@requiere_admin
def modificar_libro():
    titulo = simpledialog.askstring("Modificar libro", "Título del libro a modificar:")
    if not titulo:
        return
    lib = bib.buscar_libro(titulo.strip())
    if lib is None:
        messagebox.showwarning("No encontrado", "Libro no encontrado.")
        return
    nuevo_titulo = simpledialog.askstring("Modificar libro", "Nuevo título:", initialvalue=lib.titulo)
    nuevo_autor = simpledialog.askstring("Modificar libro", "Nuevo autor:", initialvalue=lib.autor)
    try:
        conn = __import__('db_connection').get_conn()
        cur = conn.cursor()
        cur.execute("UPDATE libros SET titulo=%s, autor=%s WHERE id=%s", (nuevo_titulo.strip(), nuevo_autor.strip(), lib.id))
        conn.commit()
        cur.close()
        conn.close()
        messagebox.showinfo("OK", "Libro modificado.")
        listar_libros()
    except Exception as e:
        messagebox.showerror("Error", f"Error al modificar libro:\n{e}")

@requiere_admin
def eliminar_libro():
    titulo = simpledialog.askstring("Eliminar libro", "Título del libro a eliminar:")
    if not titulo:
        return
    lib = bib.buscar_libro(titulo.strip())
    if lib is None:
        messagebox.showwarning("No encontrado", "Libro no encontrado.")
        return
    if messagebox.askyesno("Confirmar", f"¿Eliminar el libro '{lib.titulo}' (id={lib.id})?"):
        try:
            conn = __import__('db_connection').get_conn()
            cur = conn.cursor()
            cur.execute("DELETE FROM libros WHERE id = %s", (lib.id,))
            conn.commit()
            cur.close()
            conn.close()
            messagebox.showinfo("OK", "Libro eliminado.")
            listar_libros()
        except Exception as e:
            messagebox.showerror("Error", f"Error al eliminar libro:\n{e}")

# --- Listados / Prestamos (médico y admin) ---

def listar_usuarios():
    try:
        usuarios = bib.listar_usuarios()
        lb_output.delete(0, tk.END)
        if not usuarios:
            lb_output.insert(tk.END, "No hay usuarios registrados.")
            return
        lb_output.insert(tk.END, "Usuarios:")
        for u in usuarios:
            lb_output.insert(tk.END, f"  [{u.id}] {u.nombre} — {u.role}")
    except Exception as e:
        messagebox.showerror("Error", f"Error al listar usuarios:\n{e}")

def listar_libros():
    try:
        libros = bib.listar_libros()
        lb_output.delete(0, tk.END)
        if not libros:
            lb_output.insert(tk.END, "No hay libros registrados.")
            return
        lb_output.insert(tk.END, "Libros:")
        for l in libros:
            status = "Disponible" if l.disponible else "Prestado"
            lb_output.insert(tk.END, f"  [{l.id}] {l.titulo} — {l.autor} ({status})")
    except Exception as e:
        messagebox.showerror("Error", f"Error al listar libros:\n{e}")

def prestar_libro():
    if current_user is None:
        messagebox.showerror("Permisos", "Debe iniciar sesión.")
        return
    nombre = simpledialog.askstring("Prestar libro", "Nombre del usuario que toma el libro:")
    if not nombre:
        return
    titulo = simpledialog.askstring("Prestar libro", "Título del libro:")
    if not titulo:
        return
    try:
        msg = bib.prestar_libro(titulo.strip(), nombre.strip())
        messagebox.showinfo("Resultado", msg)
        listar_libros()
    except Exception as e:
        messagebox.showerror("Error", f"Error al prestar libro:\n{e}")

def devolver_libro():
    if current_user is None:
        messagebox.showerror("Permisos", "Debe iniciar sesión.")
        return
    nombre = simpledialog.askstring("Devolver libro", "Nombre del usuario que devuelve el libro:")
    if not nombre:
        return
    titulo = simpledialog.askstring("Devolver libro", "Título del libro:")
    if not titulo:
        return
    try:
        msg = bib.devolver_libro(titulo.strip(), nombre.strip())
        messagebox.showinfo("Resultado", msg)
        listar_libros()
    except Exception as e:
        messagebox.showerror("Error", f"Error al devolver libro:\n{e}")

def obtener_libros_prestados():
    nombre = simpledialog.askstring("Libros prestados", "Nombre del usuario:")
    if not nombre:
        return
    try:
        usuario = bib.buscar_usuario(nombre.strip())
        if usuario is None:
            messagebox.showwarning("No encontrado", "Usuario no encontrado.")
            return
        libros = usuario.obtener_libros_prestados()
        lb_output.delete(0, tk.END)
        lb_output.insert(tk.END, f"Libros prestados a {usuario.nombre}:")
        if not libros:
            lb_output.insert(tk.END, "  (No tiene libros prestados)")
            return
        for l in libros:
            lb_output.insert(tk.END, f"  [{l.id}] {l.titulo} — {l.autor}")
    except Exception as e:
        messagebox.showerror("Error", f"Error al obtener libros prestados:\n{e}")

def salir():
    root.destroy()
    sys.exit(0)

def ajustar_menu_por_rol():
    """Habilita/deshabilita opciones del menú según el rol del usuario actual."""
    if current_user is None:
        # deshabilitar todo por seguridad
        acciones_menu.entryconfig("Registrar usuario", state="disabled")
        acciones_menu.entryconfig("Registrar libro", state="disabled")
        # ... deshabilitar o habilitar entradas manualmente
        return

    if current_user.role.lower() == 'admin':
        # Admin: habilitar todo
        acciones_menu.entryconfig("Registrar usuario", state="normal")
        acciones_menu.entryconfig("Modificar usuario", state="normal")
        acciones_menu.entryconfig("Eliminar usuario", state="normal")
        acciones_menu.entryconfig("Registrar libro", state="normal")
        acciones_menu.entryconfig("Modificar libro", state="normal")
        acciones_menu.entryconfig("Eliminar libro", state="normal")
        acciones_menu.entryconfig("Prestar libro", state="normal")
        acciones_menu.entryconfig("Devolver libro", state="normal")
        acciones_menu.entryconfig("Mostrar usuarios", state="normal")
        acciones_menu.entryconfig("Mostrar libros", state="normal")
        acciones_menu.entryconfig("Obtener libros prestados (usuario)", state="normal")
    else:
        # médico o Paciente: permisos limitados
        acciones_menu.entryconfig("Registrar usuario", state="disabled")
        acciones_menu.entryconfig("Modificar usuario", state="disabled")
        acciones_menu.entryconfig("Eliminar usuario", state="disabled")
        acciones_menu.entryconfig("Registrar libro", state="disabled")
        acciones_menu.entryconfig("Modificar libro", state="disabled")
        acciones_menu.entryconfig("Eliminar libro", state="disabled")
        # médico puede prestar/devolver; Paciente solo listar y ver sus prestamos
        if current_user.role == 'médico':
            acciones_menu.entryconfig("Prestar libro", state="normal")
            acciones_menu.entryconfig("Devolver libro", state="normal")
            acciones_menu.entryconfig("Mostrar usuarios", state="normal")
            acciones_menu.entryconfig("Mostrar libros", state="normal")
            acciones_menu.entryconfig("Obtener libros prestados (usuario)", state="normal")
        else:  # Paciente
            acciones_menu.entryconfig("Prestar libro", state="disabled")
            acciones_menu.entryconfig("Devolver libro", state="disabled")
            acciones_menu.entryconfig("Mostrar usuarios", state="disabled")
            acciones_menu.entryconfig("Mostrar libros", state="normal")
            acciones_menu.entryconfig("Obtener libros prestados (usuario)", state="normal")
root = tk.Tk()
root.title("Biblioteca - Interfaz gráfica")
root.geometry("800x480")
root.minsize(700, 420)

# Menú principal
menubar = tk.Menu(root)

# Menú "Acciones" con las opciones
acciones_menu = tk.Menu(menubar, tearoff=0)
acciones_menu.add_command(label="Registrar usuario", command=registrar_usuario)
acciones_menu.add_command(label="Modificar usuario", command=modificar_usuario)
acciones_menu.add_command(label="Eliminar usuario", command=eliminar_usuario)
acciones_menu.add_separator()
acciones_menu.add_command(label="Registrar libro", command=registrar_libro)
acciones_menu.add_command(label="Modificar libro", command=modificar_libro)
acciones_menu.add_command(label="Eliminar libro", command=eliminar_libro)
acciones_menu.add_separator()
acciones_menu.add_command(label="Mostrar usuarios", command=listar_usuarios)
acciones_menu.add_command(label="Mostrar libros", command=listar_libros)
acciones_menu.add_separator()
acciones_menu.add_command(label="Prestar libro", command=prestar_libro)
acciones_menu.add_command(label="Devolver libro", command=devolver_libro)
acciones_menu.add_separator()
acciones_menu.add_command(label="Obtener libros prestados (usuario)", command=obtener_libros_prestados)
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
