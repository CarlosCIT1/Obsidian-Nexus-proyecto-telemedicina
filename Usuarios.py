# usuario.py
from db_connection import get_conn
from citas import Citas
import hashlib

def hash_password(password: str) -> str:
        if password is None:
            return None
        return hashlib.sha256(password.encode("utf-8")).hexdigest()

class Usuario:
    def __init__(self, id_, nombre, apellidos, correo, telefono, fechanac, sexo, role, contrasena):
        self.id = id_
        self.nombre = nombre
        self.apellidos = apellidos
        self.correo = correo
        self.telefono = telefono
        self.fechanac = fechanac
        self.sexo = sexo
        self.role = role
        self.contrasena = contrasena

    @classmethod
    def crear(cls, nombre, apellidos, correo, telefono, fechanac, sexo, role, password=None):
        conn = get_conn()
        try:
            cur = conn.cursor()
            pwd_hash = hash_password(password) if password else None

            cur.execute("""
                INSERT INTO usuarios (
                    us_nombre, us_apellidos, us_correo, us_telefono, 
                    us_fechanac, us_sexo, us_rol, us_contrasena
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (nombre, apellidos, correo, telefono, fechanac, sexo, role, pwd_hash))

            conn.commit()
            uid = cur.lastrowid

            return cls(uid, nombre, apellidos, correo, telefono, fechanac, sexo, role, pwd_hash)

        finally:
            cur.close()
            conn.close()


    @classmethod
    def listar_todos(cls):
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute("SELECT us_clave, us_nombre, us_apellidos, us_correo, us_telefono, us_fechanac, us_sexo, us_rol, us_contrasena FROM usuarios ORDER BY us_nombre")
            rows = cur.fetchall()
            return [cls(r[0], r[1], r[2], r[3], r[4], r[5], r[6], r[7], r[8]) for r in rows]
        finally:
            cur.close()
            conn.close()

    @classmethod
    def buscar_por_nombre(cls, nombre):
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute("SELECT us_clave, us_nombre FROM usuarios WHERE us_nombre = %s", (nombre,))
            r = cur.fetchone()
            return cls(r[0], r[1]) if r else None
        finally:
            cur.close()
            conn.close()

    @classmethod
    def buscar_por_id(cls, id_):
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute("SELECT us_clave, us_nombre FROM usuarios WHERE us_clave = %s", (id_,))
            r = cur.fetchone()
            return cls(r[0], r[1]) if r else None
        finally:
            cur.close()
            conn.close()

    def obtener_libros_prestados(self):
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute("""
                SELECT l.id, l.titulo, l.autor, l.disponible
                FROM libros l
                JOIN prestamos p ON p.libro_id = l.id
                WHERE p.usuario_id = %s AND p.devuelto = 0
            """, (self.id,))
            rows = cur.fetchall()
            return [Citas(r[0], r[1], r[2], r[3]) for r in rows]
        finally:
            cur.close()
            conn.close()

    @classmethod
    def autenticar(cls, nombre, password):
        conn = get_conn()
        try:
            cur = conn.cursor()

            # Traer TODOS los campos para construir correctamente al Usuario
            cur.execute("""
                SELECT 
                    us_clave, us_nombre, us_apellidos, us_correo, us_telefono,
                    us_fechanac, us_sexo, us_rol, us_contrasena
                FROM usuarios
                WHERE us_nombre = %s
            """, (nombre,))

            r = cur.fetchone()

            if not r:
                return None  # Usuario no encontrado

            (user_id, nombre, apellidos, correo, telefono,
            fechanac, sexo, role, stored_hash) = r

            # Verificar contraseña hasheada
            if stored_hash == hash_password(password):
                return cls(user_id, nombre, apellidos, correo, telefono,
                        fechanac, sexo, role, stored_hash)
            else:
                return None

        finally:
            cur.close()
            conn.close()



    
    def __str__(self):
        return f"{self.nombre}"
