from db_connection import get_conn

class Especialidad:
    def __init__(self, id_especialidad, nom_especialidad):
        self.id_especialidad = id_especialidad
        self.nom_especialidad = nom_especialidad

    @classmethod
    def crear(cls, nom_especialidad):
        conn = get_conn()
        try:
            cur = conn.cursor()

            cur.execute("""
                INSERT INTO especialidades (nom_especialidad)
                VALUES (%s)
            """, (nom_especialidad,))

            conn.commit()
            eid = cur.lastrowid  # id de la nueva especialidad

            return cls(eid, nom_especialidad)

        finally:
            cur.close()
            conn.close()
