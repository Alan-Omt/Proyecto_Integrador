#variables iniciales, Es una lista de bandas y albunes musicales:
lista = [
  {"nombre": "Muse", "album": "The Resistance", "año": 2009},
  {"nombre": "The Dears", "album": "No Cities Left", "año": 2003},
]
opcion_menu = -1

#Menu Interactivo
while opcion_menu != 3:
  print("----Menu Principal de la Aplicacion----")
  print(
    """
    Opciones:
    1) Agregar un nuevo Albun a la base de datos
    2) Listar Albunes Agregados
    3) Cerrar la Aplicacion
    """
  )
  opcion_menu = int(input("Seleccione una Opcion: "))
  print()
  
  if opcion_menu == 1:
    print("Submenu para agregar album nuevo: ")
    nombre = input("Ingrese el nombre del Artista o Grupo: ")
    disco = input("Ingrese el nombre del album: ")
    año = int(input("Ingrese el año de publicacion: "))
    #se crea el diccionario y se agrega a la lista
    lista.append({"nombre": nombre, "album": disco, "año": año})
    
    print("Albun agregado a la lista, volviendo al menu")
    print()
    #NOTA: faltan validaciones

  elif opcion_menu == 2:
    print("Albunes guardados en la base de datos:")
    print()
    for disco in lista:
      print(f"#Artista: {disco["nombre"]}, Album: {disco["album"]}, Año lanzamiento: {disco["año"]}")
    print()
    print("**Fin de la lista, volviendo al menu principal**")
    print()

  elif opcion_menu == 3:
    print("Opcion 3: Se cerrara la Aplicacion")
  else:
    print("**Opcion invalida, intente nuevamente, mostrando opciones**")

print("Fin del Programa")

#NOTA: me acorde al final que despues habra que trabajar con cantidades, prometo corregirlo para despues.