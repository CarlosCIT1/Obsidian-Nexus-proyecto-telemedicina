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

# Crear pool
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
    return conn


def release_conn(conn):
    """
    Devuelve la conexión al pool cerrándola correctamente.
    """
    try:
        if conn and conn.is_connected():
            conn.close()
    except Exception as e:
        print(f"Error al liberar conexión: {e}")
