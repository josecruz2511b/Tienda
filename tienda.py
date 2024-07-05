import pyodbc



try:
    conexion = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                              'Server=Josedelacruz25;'
                              'Database=Tienda1;'
                              'Trusted_Connection=yes;')
    print("Conexion Correcta")

except Exception as e:
     # Atrapar error
    print("Ocurrio un error al conectar a SQL Server: ", e)
