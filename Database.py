#Database Connection Settings
import psycopg2

def connection():
    try:
        con = psycopg2.connect(
            host="localhost",
            database="ecommerce",
            user="postgres",
            password="12345", #your databse password that you have used during installation
            port="5432" #default port for other servers POSTGRE(5432), MYSQL(3306), SQLSERVER(1433), ORACLE(1521)
        )
        print("Connection successful")
        return con

    except Exception as e:
        print("Connection failed")
        print("Error:", e)
        return None

conn = connection()

