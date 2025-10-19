import psycopg2


def get_connection(password):
    # Implement your function to establish a PostgreSQL connection here

    conn = psycopg2.connect(
        host="",
        port="",
        database="", 
        user="", 
        password=password
    )
    return conn