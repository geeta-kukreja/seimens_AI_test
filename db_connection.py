from psycopg import Connection
from config import DB_URI
from langgraph.store.postgres import PostgresStore
from langgraph.checkpoint.postgres import PostgresSaver


def get_conn():
    connection_kwargs = {
        "autocommit": True,
        "prepare_threshold": 0,
    }
    conn = Connection.connect(DB_URI, **connection_kwargs)
    return conn


def create_user_table():
    conn = get_conn()
    cur = conn.cursor()
    # Create a table for users.
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            session_id TEXT UNIQUE NOT NULL
        )
    """)
    conn.commit()
def set_up_db():

    # conn = Connection.connect(DB_URI, **connection_kwargs)
    conn = get_conn()
    memory_store = PostgresStore(conn)

    memory_store.setup()

    checkpointer = PostgresSaver(conn)
    checkpointer.setup()

    # Create user db to store session_ids
    create_user_table()

    return checkpointer, memory_store


checkpointer, memory_store = set_up_db()
