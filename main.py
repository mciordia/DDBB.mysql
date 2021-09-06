# hacer un programa que calcule las propinas de un mozo en un dia de trabajo
# se ingresaran los datos de la persona apellido y nombre, lugar de trabajo, edad, dni alojarlo en diccionarios y pasarlo a base de datos
# se ingresa el dia, se ingresa el sueldo fijo, se le sumara cada propina que recibe, como resultado saldra todo lo recaudado  de propina,
# al final de mes se sumara el sueldo y la propina
# agregar restaurants o bares registrados en la app, chequear si esta registrado en la app
# las propinas ingresan con qr

import datetime
import mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode

host_local = "localhost"
usuario = "root"
password_de_msql = ""  # mysql2021
print("Conectamos con MySQL")
connection = mysql.connector.connect(host=host_local, user=usuario, passwd=password_de_msql)
print(f"mysql.connector.connect(host= {host_local} ,user= {usuario} , passwd= {password_de_msql} )")
cursor = connection.cursor()
nombre_ddbb = "propinas"
nombre_tabla = "Registro"


def creacion_BBDD():
    connection = mysql.connector.connect(host=host_local, user=usuario, passwd=password_de_msql)
    cursor = connection.cursor()
    cursor.execute(f"DROP DATABASE IF EXISTS {nombre_ddbb}")
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {nombre_ddbb}")
    cursor.execute(f"USE {nombre_ddbb}")
    cursor = connection.cursor()


def crear_tabla_columnas():
    connection = mysql.connector.connect(host=host_local, user=usuario, passwd=password_de_msql)
    cursor = connection.cursor()
    cursor.execute(f"USE {nombre_ddbb}")
    columna1 = "Dni"
    columna2 = "nombre"
    columna3 = "edad"
    columna4 = "sexo"
    columna5 = "restaurante"
    columna6 = "recaudado"
    string = (
        f"CREATE TABLE {nombre_tabla} ({columna1} INT PRIMARY KEY  , {columna2} VARCHAR(55), {columna3} INT, {columna4} VARCHAR (55), {columna5} VARCHAR (55), {columna6} FLOAT); ")
    cursor.execute(string)
    cursor = connection.cursor()
    cursor.close
    connection.close


def insertar_datos():
    connection = mysql.connector.connect(host=host_local, user=usuario, passwd=password_de_msql)
    cursor = connection.cursor()
    cursor.execute(f"USE {nombre_ddbb}")
    columna1 = "Dni"
    columna2 = "nombre"
    columna3 = "edad"
    columna4 = "sexo"
    columna5 = "restaurante"
    columna6 = "recaudado"

    print("Ingrese los datos de registro")

    DNI = int(input("Ingrese su numero de dni: \n"))
    nombre = input("Ingrese su nombre y apellido: \n ").capitalize()
    edad = int(input("Ingrese su edad: \n"))
    sexo = input("Ingrese su sexo : \n ").upper()
    restaurante = input("Ingrese su lugar de trabajo: \n ").capitalize()
    recaudado = 0

    query = f"""INSERT INTO  {nombre_tabla}  ({columna1}, {columna2}, {columna3},{columna4},{columna5}, {columna6}) VALUES(%s,%s,%s,%s,%s,%s)"""
    cursor.execute(query, (DNI, nombre, edad, sexo, restaurante, recaudado))
    connection.commit()

    ###la recaudacion lo pasamos despues cuando calculemos la propina

    Total_Propina = 0

    while True:
        usuario2 = input("Recibira propina?:(S/N) \n")
        if usuario2.upper() == "S":
            propina = float(input("Ingrese el monto de su propina: \n"))
            Total_Propina += propina
            print(f"Vas generando un total de ${Total_Propina}")
            Salida = input("Termino tu dia laboral?: \n")
            # cuando termino mi dia laboral quiero enviar a la bbdd lo recaudado, tengo q volver a llamar a toda la funcion o como puedo hacer

            if Salida.upper() == "S":
                cursor = connection.cursor()
                query = f"""UPDATE {nombre_tabla} SET recaudado = {Total_Propina} WHERE Dni = {DNI} """
                # ~ query = f"""INSERT INTO  {nombre_tabla}  ({columna6}) """
                cursor.execute(query, (Total_Propina))
                connection.commit()
                print(f"Felicidades has recaudado un total de {Total_Propina} el {fecha.strftime('%c')}")

        else:
            break


def Agregar_Propina():
    # traer lo recaudado de la bbdd y sumar con lo nuevo y pisarlo
    connection = mysql.connector.connect(host=host_local, user=usuario, passwd=password_de_msql)
    cursor = connection.cursor()
    cursor.execute(f"USE {nombre_ddbb}")
    dni = int(input("Cual es su dni:  "))
    propina2 = int(input("Ingrese su nueva propina:  "))
    query1 = f"""SELECT recaudado FROM {nombre_tabla} WHERE Dni={dni}"""
    cursor.execute(query1)
    resultado = list(cursor.fetchone())

    print(resultado[0])

    final = resultado[0] + propina2

    print(final)
    query2 = f"""UPDATE {nombre_tabla} SET recaudado = {final} WHERE Dni = {dni} """
    cursor.execute(query2)
    connection.commit()


# convertir resultado en float o string y sumarle lo q le agregamos

def Crear_sueldo():
    # agregar columna de sueldos y montos
    connection = mysql.connector.connect(host=host_local, user=usuario, passwd=password_de_msql)
    cursor = connection.cursor()
    cursor.execute(f"USE {nombre_ddbb}")

    addColumn = f"""ALTER TABLE {nombre_tabla} ADD COLUMN Sueldo INT"""
    cursor.execute(addColumn)


def Agregar_Sueldo():
    connection = mysql.connector.connect(host=host_local, user=usuario, passwd=password_de_msql)
    cursor = connection.cursor()
    cursor.execute(f"USE {nombre_ddbb}")
    try:
        dni = int(input("Cual es su dni:  "))
        sueldo = int(input("Ingrese su nueva propina:  "))
        query2 = f"""UPDATE {nombre_tabla} SET Sueldo = {sueldo} WHERE Dni = {dni} """
        cursor.execute(query2)
        connection.commit()
    except:
        print("Creo base")
    Crear_sueldo()
    query3 = f"""UPDATE {nombre_tabla} SET Sueldo = {sueldo} WHERE Dni = {dni} """
    cursor.execute(query3)
    connection.commit()


fecha = datetime.datetime.now()
print(fecha.strftime("%c"))

Empleado = input("Es usted mozo o empleado de resto o bar : \n ")
if Empleado.upper() == "S":

    registro = input("Desea registrarse (S/N):\n ")
    if registro.upper() == "S":
        print("Registramos sus datos")

        creacion_BBDD()
        crear_tabla_columnas()

        opciones = input("A-Propinas B-AGREGAR PROPINA C-AGREGAR SUELDO D-VER TOTAL DE PROPINA RECAUDADO :")
        if opciones.upper() == "A":
            insertar_datos()

        elif opciones.upper() == "B":
            Agregar_Propina()

        if opciones.upper() == "C":
            Agregar_Sueldo()
    # ~ if opciones.upper() == "D":

# FUNCION AGREGAR SUELDO: CREAR FUNCION Q INGRESE EL SUELDO Y CREE Y SE GUARDE EN OTRA COLUMNA
# FUNCION D: SUMAR TODA LA PROPINA RECAUDADA EN EL MES.

