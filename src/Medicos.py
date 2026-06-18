# medicos.py
from citas import Consulta
from usuarios import Usuario
from especialidades import Especialidad

class NexusCare:
    def __init__(self):
        pass

    # -------------------------------------------------------
    #   REGISTROS
    # -------------------------------------------------------
    def registrar_usuario(self, nombre, apellidos, correo, telefono, fechanac, sexo, rol, contrasena):
        return Usuario.crear(nombre, apellidos, correo, telefono, fechanac, sexo, rol, contrasena)

    def registrar_consulta(self, diagnostico, motivo, estado, hora, fecha, virtual, presencial,
                           paciente_clave, doctor_clave):
        return Consulta.crear(
            diagnostico, motivo, estado, hora, fecha, virtual, presencial,
            paciente_clave, doctor_clave
        )

    def registrar_especialidad(self, nombre):
        return Especialidad.crear(nombre)

    # -------------------------------------------------------
    #   BÚSQUEDAS
    # -------------------------------------------------------
    def buscar_usuario(self, correo):
        return Usuario.buscar_por_correo(correo)

    def buscar_consulta(self, consulta_id):
        return Consulta.buscar_por_id(consulta_id)

    def buscar_especialidad(self, nombre):
        return Especialidad.buscar_por_nombre(nombre)

    # -------------------------------------------------------
    #   LISTADOS
    # -------------------------------------------------------
    def listar_usuarios(self):
        return Usuario.listar_todos()

    def listar_consultas(self):
        return Consulta.listar_todos()

    def listar_especialidades(self):
        return Especialidad.listar_todas()

    # -------------------------------------------------------
    #   BORRADO
    # -------------------------------------------------------
    def eliminar_consulta(self, consulta_id):
        return Consulta.eliminar(consulta_id)

    def eliminar_usuario(self, usuario_id):
        return Usuario.eliminar(usuario_id)

    def eliminar_especialidad(self, especialidad_id):
        return Especialidad.eliminar(especialidad_id)

    # -------------------------------------------------------
    #   ASIGNACIÓN DOCTOR–ESPECIALIDAD
    # -------------------------------------------------------
    def asignar_especialidad_a_doctor(self, doctor_id, especialidad_id):
        return Especialidad.asignar_a_doctor(doctor_id, especialidad_id)

    def listar_asignaciones_doctores(self):
        return Especialidad.listar_asignaciones()
