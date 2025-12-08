from db_connection import get_conn

class Consulta:
    def __init__(self, co_clave, diagnostico, motivo, estado, hora, fecha, virtual, presencial, paciente, doctor):
        self.id = co_clave
        self.diagnostico = diagnostico
        self.motivo = motivo
        self.estado = estado
        self.hora = hora
        self.fecha = fecha
        self.virtual = virtual
        self.presencial = presencial
        self.paciente = paciente
        self.doctor = doctor

    @classmethod
    def crear(cls, diagnostico, motivo, hora, fecha, virtual, presencial, paciente, doctor):
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO consultas (
                    co_diagnostico, co_motivo, co_hora, co_fecha,
                    co_virtual, co_presencial, paciente_clave, doctor_clave
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (diagnostico, motivo, hora, fecha, virtual, presencial, paciente, doctor))

            conn.commit()
            cid = cur.lastrowid
            return cls(cid, diagnostico, motivo, "Pendiente", hora, fecha, virtual, presencial, paciente, doctor)
        
        finally:
            cur.close()
            conn.close()

    @classmethod
    def listar_todos(cls):
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute("""
                SELECT 
                    co_clave, co_diagnostico, co_motivo, co_estado,
                    co_hora, co_fecha, co_virtual, co_presencial,
                    paciente_clave, doctor_clave
                FROM consultas
            """)

            filas = cur.fetchall()
            consultas = []

            for fila in filas:
                co_clave, diagnostico, motivo, estado, hora, fecha, virtual, presencial, paciente, doctor = fila
                consulta = cls(
                    co_clave, diagnostico, motivo, estado,
                    hora, fecha, virtual, presencial, paciente, doctor
                )
                consultas.append(consulta)

            return consultas

        finally:
            cur.close()
            conn.close()

class ConsultaPaciente:
    def __init__(self, fecha, hora, doctor):
        self.fecha = fecha
        self.hora = hora
        self.doctor = doctor


    @staticmethod
    def obtener_por_paciente(id_paciente):
        conn = get_conn()
        cur = conn.cursor()

        cur.execute("""
            SELECT co_fecha, co_hora, us_nombre
            FROM consultas c
            JOIN usuarios u ON us_clave = doctor_clave
            WHERE paciente_clave = %s
            ORDER BY co_fecha, co_hora
        """, (id_paciente,))

        rows = cur.fetchall()
        conn.close()

        resultado = []
        for fecha, hora, doctor in rows:
            obj = ConsultaPaciente(fecha, hora, doctor)
            resultado.append(obj)

        return resultado
