import pyodbc

try:
    conexion = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                              'Server=LAPTOP-2GT147OG;'
                              'Database=TiendaCRUD;'
                              'Trusted_Connection=yes;')
    print("Conexion Correcta")

except Exception as e:
     # Atrapar error
    print("Ocurrio un error al conectar a SQL Server: ", e)
