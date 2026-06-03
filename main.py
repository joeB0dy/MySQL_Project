import mysql.connector


def get_connection(host: str, user: str, password: str, database: str):
    return mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database,
    )


def run_query(connection, query: str):
    cursor = connection.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    return results


if __name__ == "__main__":
    print("MySQL Goals — Capstone Project")
    print("Connect to your database and start building!")
