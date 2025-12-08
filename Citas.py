from db_connection import get_conn

class Citas:
    def __init__(self, ci_clave, ci_especialidad, ci_fecha, ci_motivo=True):
        self.id = ci_clave
        self.ci_especialidad = ci_especialidad
        self.ci_fecha = ci_fecha
        self.ci_motivo = ci_motivo

    def agendar(self, usuario_id):
        conn = get_conn()
        try:
            cur = conn.cursor()
            # Verificar disponibilidad actual
            cur.execute("SELECT ci_motivo FROM citas WHERE id = %s FOR UPDATE", (self.id,))
            row = cur.fetchone()
            if not row:
                return False
            ci_motivo = bool(row[0])
            if not ci_motivo:
                return False

            # Actualizar libro y crear préstamo
            cur.execute("UPDATE citas SET ci_motivo = 0 WHERE id = %s", (self.id,))
            cur.execute(
                "INSERT INTO prestamos (usuario_id, libro_id) VALUES (%s, %s)",
                (usuario_id, self.id)
            )
            conn.commit()
            self.ci_motivo = False
            return True
        except Exception as e:
            conn.rollback()
            raise
        finally:
            cur.close()
            conn.close()

    def devolver(self, usuario_id):
        conn = get_conn()
        try:
            cur = conn.cursor()
            # Buscar préstamo no devuelto para este usuario y libro
            cur.execute("""
                SELECT id FROM prestamos
                WHERE usuario_id = %s AND libro_id = %s AND devuelto = 0
                ORDER BY fecha_prestamo DESC LIMIT 1
            """, (usuario_id, self.id))
            row = cur.fetchone()
            if not row:
                return False
            prestamo_id = row[0]
            cur.execute("UPDATE prestamos SET devuelto = 1, fecha_devolucion = NOW() WHERE id = %s", (prestamo_id,))
            cur.execute("UPDATE citas SET ci_motivo = 1 WHERE id = %s", (self.id,))
            conn.commit()
            self.ci_motivo = True
            return True
        except Exception as e:
            conn.rollback()
            raise
        finally:
            cur.close()
            conn.close()

    # Métodos de clase para CRUD
    @classmethod
    def crear(cls, ci_especialidad, ci_fecha):
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute("INSERT INTO citas (ci_especialidad, ci_fecha) VALUES (%s, %s)", (ci_especialidad, ci_fecha))
            conn.commit()
            lid = cur.lastrowid
            return cls(lid, ci_especialidad, ci_fecha, True)
        finally:
            cur.close()
            conn.close()

    @classmethod
    def listar_todos(cls):
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute("SELECT id, ci_especialidad, ci_fecha, ci_motivo FROM citas ORDER BY ci_especialidad")
            rows = cur.fetchall()
            return [cls(r[0], r[1], r[2], r[3]) for r in rows]
        finally:
            cur.close()
            conn.close()

    @classmethod
    def buscar_por_ci_especialidad(cls, ci_especialidad):
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute("SELECT id, ci_especialidad, ci_fecha, ci_motivo FROM citas WHERE ci_especialidad = %s", (ci_especialidad,))
            r = cur.fetchone()
            return cls(r[0], r[1], r[2], r[3]) if r else None
        finally:
            cur.close()
            conn.close()

    @classmethod
    def Eliminar_libro(cls, ci_especialidad):
        conn = get_conn()
        try :
            cur = conn.cursor()
            cur.execute("DELETE FROM citas WHERE ci_especialidad = %s", (ci_especialidad,))
            conn.commit()
        finally:
            cur.close()
            conn.close()

    @classmethod
    def buscar_por_id(cls, ci_clave):
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute("SELECT id, ci_especialidad, ci_fecha, ci_motivo FROM citas WHERE id = %s", (ci_clave,))
            r = cur.fetchone()
            return cls(r[0], r[1], r[2], r[3]) if r else None
        finally:
            cur.close()
            conn.close()

    def __str__(self):
        status = "Motivo" if self.ci_motivo else "-------"
        return f"{self.ci_especialidad} - {self.ci_fecha} ({status})"
