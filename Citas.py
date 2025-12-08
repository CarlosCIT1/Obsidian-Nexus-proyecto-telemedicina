from db_connection import get_conn

class Consulta:
    def __init__(self, co_clave, diagnostico, motivo, estado, hora, fecha, tipo_consulta, paciente, doctor, nombre_paciente):
        self.id = co_clave
        self.diagnostico = diagnostico
        self.motivo = motivo
        self.estado = estado
        self.hora = hora
        self.fecha = fecha
        self.tipo_consulta = tipo_consulta
        self.paciente = paciente
        self.doctor = doctor
        self.nombre_paciente = nombre_paciente


    @classmethod
    def crear(cls, diagnostico, motivo, hora, fecha, tipo_consulta, paciente, doctor):
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO consultas (
                    co_diagnostico, co_motivo, co_hora, co_fecha,
                    co_tipo_consulta, paciente_clave, doctor_clave 
                ) VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (diagnostico, motivo, hora, fecha, tipo_consulta, paciente, doctor))

            conn.commit()
            cid = cur.lastrowid
            
            # ⬅️ CORRECCIÓN 1: Se añade 'None' para el argumento 'nombre_paciente' que faltaba.
            return cls(cid, diagnostico, motivo, "Pendiente", hora, fecha, tipo_consulta, paciente, doctor, None)
        
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
                    c.co_clave, c.co_diagnostico, c.co_motivo, c.co_estado,
                    c.co_hora, c.co_fecha, c.co_tipo_consulta,
                    c.paciente_clave, c.doctor_clave,
                    u.us_nombre
                FROM consultas c
                JOIN usuarios u ON u.us_clave = c.paciente_clave;
            """)

            filas = cur.fetchall()
            consultas = []

            for fila in filas:
                co_clave, diagnostico, motivo, estado, hora, fecha, tipo_consulta, paciente, doctor, nombre_paciente = fila
                consulta = cls(
                    co_clave, diagnostico, motivo, estado,
                    hora, fecha, tipo_consulta, paciente, doctor, nombre_paciente
                )
                consultas.append(consulta)

            return consultas

        finally:
            cur.close()
            conn.close()
    
    @staticmethod
    def listar_por_paciente(id_paciente):
        conn = get_conn()
        cur = conn.cursor(dictionary=True)

        cur.execute("""
            SELECT 
                co_clave, 
                co_diagnostico AS diagnostico, 
                co_motivo AS motivo, 
                co_estado AS estado,
                co_hora AS hora, 
                co_fecha AS fecha, 
                co_tipo_consulta AS tipo_consulta, 
                paciente_clave AS paciente,      
                doctor_clave AS doctor,          
                NULL AS nombre_paciente  
            FROM consultas
            WHERE paciente_clave = %s 
            ORDER BY co_fecha DESC
        """, (id_paciente,))

        rows = cur.fetchall()
        conn.close()

        return [Consulta(**row) for row in rows]

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
            SELECT co_fecha, co_hora, u.us_nombre
            FROM consultas c
            -- ⬅️ CORRECCIÓN 4: Se especifica el alias 'u.' para evitar ambigüedad en el JOIN
            JOIN usuarios u ON u.us_clave = c.doctor_clave 
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
