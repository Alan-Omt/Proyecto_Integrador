import sqlite3
from colorama import init, Fore, Style
#Funciones de la Base de Datos--------------------------------------------------------------------------------------------

#funcion de comprobar y crear la tabla:
def comprobar_tabla():
  cursor_sqlite.execute(
    """CREATE TABLE IF NOT EXISTS Albunes_musica (
      Id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
      Nombre TEXT NOT NULL,
      Album TEXT NOT NULL,
      Año INTEGER,
      Stock INTEGER NOT NULL
      ) 
    """)

#funcion para precargar datos en caso que haya que reiniciar la DB
def cargar_prueba():
  cursor_sqlite.execute(
    """INSERT INTO Albunes_musica (Nombre, Album, Año, Stock) VALUES 
      ("Muse", "The Resistance", 2009, 3),
      ("Muse", "Will of the People", 2022, 10),
      ("Muse", "Drones", 2015, 2),
      ("The Beatles", "Abbey Road", 1969, 8),
      ("The Beatles", "Magical Mystery Tour", 1967, 1),
      ("Rage against the Machine", "Evil Empire", 1996, 6),
      ("Rage against the Machine", "The Battle of Los Angeles", 1999, 7)
    """
  )

#funcion para cargar registros
def cargar_album(album: tuple):
  cursor_sqlite.execute(
    """INSERT INTO Albunes_musica (Nombre, Album, Año, Stock) VALUES(?,?,?,?)""",(album[0],album[1],album[2],album[3])
  )
  conexion_sqlite.commit()

#funcion para contar la cantidad de registros
def contar_registros():
  cursor_sqlite.execute(
    """SELECT Id FROM Albunes_musica """
  )
  cantidad = cursor_sqlite.fetchall()
  return (len(cantidad))

#funcion para buscar registro individual
def buscar_registro(id):
  cursor_sqlite.execute("SELECT * FROM Albunes_musica WHERE Id = ?",(id,))
  registro = cursor_sqlite.fetchone()
  return registro

#Funciones del menu------------------------------------------------------------------------------------------------------------

#Verificar que el campo input no este vacio
def verificar_input():
  entrada = input()

  while entrada.strip() == "":
    print(Fore.RED + "¡¡Este campo NO puede quedar vacio!!")
    entrada = input("Intente nuevamente: ")
  
  return entrada

#Verificar que lo ingresado sea un numero, en caso no ser obligatorio se puede agragar como parametro False
def verificar_numero(obligatorio = True):
  entrada = input()
  if obligatorio == False and entrada.strip() == "":
    return ""
  
  while True:
    entrada.strip()
    if entrada == "":
      print(Fore.RED + "La entrada es OBLIGATORIA ")

    elif not entrada.isnumeric():
      print("La entrada tiene que ser un numero ")

    elif entrada.isnumeric():
      entrada = int(entrada)
      if entrada <= 0:
        print(Fore.RED + "La entrada tiene que ser MAYOR al cero ")
      elif entrada > 0:
        return int(entrada)
    entrada = input("Ingresar nuevamente: ")


#Agregar un albun nuevo a la bd
def agregar_albun():
  print("Submenu para agregar album nuevo: ")
  print("Ingrese el nombre del Artista o Grupo (obligatorio): ",end="")
  nombre = verificar_input().capitalize()
  print("Ingrese el nombre del album (obligatorio): ",end="")
  album = verificar_input().capitalize()
  print("Ingrese el año de publicacion (si no se sabe puede omitirse): ",end="")
  año = verificar_numero(False)
  print("Ingresar la cantidad de stock inicial (Mayor a cero): ",end="")
  stock = verificar_numero()
  registro = (nombre, album, año, stock)
  print("Registro creado: ")
  print(Style.BRIGHT + Fore.YELLOW + f"Banda: {nombre}, Album: {album}, año de estreno: {año}, cantidad inicial: {stock}")
  cargar_album(registro)
  print(Fore.GREEN + "Album agregado a la Base de Datos, volviendo al menu")
  print()

#Listar albunes en la bd
def listar_albunes():
  print("Albunes guardados en la base de datos:")
  print()
  cursor_sqlite.execute("SELECT * FROM Albunes_musica")
  registros = cursor_sqlite.fetchall()
  for registro in registros:
    print(Style.BRIGHT + Fore.YELLOW + f"Id: {registro[0]}, Artista: {registro[1]}, Album: {registro[2]}, Año Lanzamiento: {registro[3]}, Cantidad: {registro[4]}")
  print()
  print(Fore.GREEN + "Fin de los registros, volviendo al menu\n")

#Buscar un registro individual y editarlo
def editar_registro():
  #primera parte:Buscar registro
  print(f"Ingrese el Id del registro al editar, Pista: hay {contar_registros()} en la Base de Datos")
  print("Ingresar el Id del album: ", end="")
  id_registro = verificar_numero()
  registro = buscar_registro(id_registro)
  if registro == None:
    print(Fore.RED + "Registro no encontrado, volviendo al menu pricipal")
    return
  else:
    print("Registro Encontrado:")
    print(Style.BRIGHT + Fore.YELLOW + f"Id: {registro[0]}, Nombre: {registro[1]}, Album: {registro[2]}, Año: {registro[3]}, Stock: {registro[4]}")
    print("""Ingrese que Editar:
          1)Artista
          2)Album
          3)Año Lanzamiento
          4)Cantidad""")
    print("Ingresar una opcion: ", end="")

    opciones = ("Id", "Nombre", "Album", "Año", "Stock") #tupla auxiliar para editar registros

    #Segunda Parte: Buscar nuevo registro
    opcion = verificar_numero()
    while opcion > 4:
      print("Opcion No valida, ingrese nuevamente: ",end="" )
      opcion = verificar_numero()
    print(f"Ingrese el nuevo {opciones[opcion]}:     ---(Valor anterior: {registro[opcion]})--- ",end="")
    nuevo_valor = input()
    cursor_sqlite.execute(f"""
      UPDATE Albunes_musica
      SET {opciones[opcion]} = ?
      WHERE Id = ?
    """,(nuevo_valor,registro[0]))
    conexion_sqlite.commit()
    registro = buscar_registro(id_registro)
    print("Registro Actualizado:")
    print(Style.BRIGHT + Fore.YELLOW + f"Id: {registro[0]}, Nombre: {registro[1]}, Album: {registro[2]}, Año: {registro[3]}, Stock: {registro[4]}")
    print(Fore.GREEN + "Fin de la edicion, Volviendo al menu\n")

#Eliminar registro 
def eliminar_registro():
  #primera parte:Buscar registro
  print(f"Ingrese el Id del registro para eliminar, Pista: hay {contar_registros()} en la Base de Datos")
  print("Ingresar el Id del album: ", end="")
  id_registro = verificar_numero()
  registro = buscar_registro(id_registro)
  if registro == None:
    print(Fore.RED + "Registro no encontrado, volviendo al menu pricipal")
    return
  else:
    print("Registro Encontrado:")
    print(Style.BRIGHT + Fore.YELLOW + f"Id: {registro[0]}, Nombre: {registro[1]}, Album: {registro[2]}, Año: {registro[3]}, Stock: {registro[4]}")
  
  cursor_sqlite.execute("DELETE FROM Albunes_musica WHERE Id = ?",(registro[0],))
  conexion_sqlite.commit()
  print(Fore.GREEN + "Registro Eliminado, Volviendo al menu\n")

#Buscar por palabras que contengan
def buscar_parecido():
  print("Submenu para buscar por parecido")
  print("ingrese referencias o palabras que estan contenidas: ", end="")  
  referencia = verificar_input()

  referencia = f"%{referencia}%" #Para poder usar query parametrizada sin error hay que colocar los % por fuera

  cursor_sqlite.execute(f"SELECT * FROM Albunes_musica WHERE Nombre LIKE ? OR Album LIKE ?",(referencia, referencia))

  resultado = cursor_sqlite.fetchall()
  if len(resultado) == 0:
    print(Fore.RED + f"NO hay registros con la referencia indicada (referencia:{referencia})")
  else:
    print("REGISTROS ENCONTRADOS:")
    for registro in resultado:
      print(Style.BRIGHT + Fore.YELLOW + f"Id: {registro[0]}, Artista: {registro[1]}, Album: {registro[2]}, Año Lanzamiento: {registro[3]}, Cantidad: {registro[4]}")
  print( Fore.GREEN + "Volviendo al menu Principal\n")

#Listar por stock minimo
def listar_stock():
  print("Submenu para buscar por Stock:")
  print("Ingrese cantidad de la cual se comparara el stock: ",end="")
  cantidad = verificar_numero()
  cursor_sqlite.execute("SELECT * FROM Albunes_musica WHERE Stock <= ?",(cantidad,))

  resultado = cursor_sqlite.fetchall()
  if len(resultado) == 0:
    print(Fore.RED + f"NO hay registros con stock debajo del indicado (stock indicado:{cantidad})")
  else:
    print("REGISTROS ENCONTRADOS:")
    for registro in resultado:
      print(Style.BRIGHT + Fore.YELLOW + f"Id: {registro[0]}, Artista: {registro[1]}, Album: {registro[2]}, Año Lanzamiento: {registro[3]}, Cantidad: {registro[4]}")
  print(Fore.GREEN + "Volviendo al menu Principal\n")

#Menu Interactivo

init(autoreset=True)
opcion_menu = -1

conexion_sqlite = sqlite3.connect("BaseDatosPFI.db")
cursor_sqlite = conexion_sqlite.cursor()
comprobar_tabla()
conexion_sqlite.commit()

while opcion_menu != 7:
  print(Style.BRIGHT + Fore.BLUE + "----Menu Principal de la Aplicacion----")
  print(Style.BRIGHT + Fore.BLUE +
    """
    Opciones:
    1) Agregar un nuevo Album a la base de datos
    2) Listar Albunes Agregados
    3) Editar un album y/o actualizar su precio o stock
    4) Eliminar un albun de la Base de Datos
    5) Buscar por Categoria o id
    6) Mostar Alertas de stock
    7) Cerrar la Aplicacion
    """
  )
  print(Fore.RED +"    8)Precargar Datos de Prueba (Hacer solo en caso de que la BD este vacia y deba crearse de cero)\n")
  opcion_menu = int(input("Seleccione una Opcion: "))
  print()
  
  if opcion_menu == 1:
    agregar_albun()

  elif opcion_menu == 2:
    listar_albunes()

  elif opcion_menu == 3:
    editar_registro()

  elif opcion_menu == 4:
    eliminar_registro()

  elif opcion_menu == 5:
    buscar_parecido()

  elif opcion_menu == 6:
    listar_stock()

  elif opcion_menu == 7:
    print(Fore.GREEN + "Opcion 7: Se cerrara la Aplicacion")
    break

  elif opcion_menu == 8:
    print("Se cargaran registros para probar los comandos")
    print(Fore.RED +"NOTA: Volver a pulsar esta opcion repetira los datos!!")
    cargar_prueba()
    conexion_sqlite.commit()
    print()

  else:
    print(Fore.RED +"**Opcion invalida, intente nuevamente, mostrando opciones**\n")

conexion_sqlite.close()
print(Fore.GREEN + "Fin del Programa")
