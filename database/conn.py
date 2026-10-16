import mysql.connector
from dependencies.conn_dep import cursor_types

def gen_cursor(cursor_type):
    cfg = cursor_types[cursor_type]
    conn = mysql.connector.connect(**cfg)
    return conn, conn.cursor()

def kill_cursor(conn, cursor):
    cursor.close()
    conn.close()

