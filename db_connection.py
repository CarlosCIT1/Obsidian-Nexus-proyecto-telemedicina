import mysql.connector
from mysql.connector import pooling, Error
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", 3306)),
    "database": os.getenv("DB_NAME", "dbnexuscare"),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", ""),
    "charset": "utf8mb4",
    "autocommit": False
}

POOL_NAME = os.getenv("POOL_NAME", "nexuscare_pool")
POOL_SIZE = int(os.getenv("POOL_SIZE", 5))

try:
    pool = pooling.MySQLConnectionPool(
        pool_name=POOL_NAME,
        pool_size=POOL_SIZE,
        **DB_CONFIG
    )
    print("Pool de conexiones creado correctamente.")
except Error as e:
    print(f"Error al crear el pool: {e}")
    pool = None


def get_conn():
    if pool is None:
        raise Exception("El pool de conexiones no está disponible.")
    
    conn = pool.get_connection()
    
    # Debug: Mostrar estado tras PRESTAR una conexión
    mostrar_estado_pool("PRESTADA")
    return conn

def release_conn(conn):
    if conn and conn.is_connected():
        conn.close()  # Devuelve la conexión al pool
        
        # Debug: Mostrar estado tras DEVOLVER una conexión
        mostrar_estado_pool("DEVUELTA")

def mostrar_estado_pool(accion):
    """
    Calcula y muestra cuántas conexiones hay libres y ocupadas.
    """
    # El tamaño total del pool
    total = pool.pool_size
    # Conexiones disponibles en la cola interna
    disponibles = pool._pool_queue.qsize()
    # Conexiones ocupadas (Total - Disponibles)
    ocupadas = total - disponibles
    
    print(f"\n--- ESTADO DEL POOL ({accion}) ---")
    print(f"Total configurado: {total}")
    print(f"Disponibles:       {disponibles}")
    print(f"Ocupadas:          {ocupadas}")
    print("================================")
