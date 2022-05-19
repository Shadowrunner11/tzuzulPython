import sqlite3
from sqlite3.dbapi2 import Error


class Conexion:
    # Aprentemente si se cierra pero puedo volve ra ejecutar conexion por algun motivo

    def __init__(self):
        self.__result = []

    def start(self, query):
        # try:
        with sqlite3.connect(".//model//posDB") as conexion:
            self.__result = conexion.execute(query).fetchall()
            conexion.commit()
        conexion.close()
        # es necesario?
        del conexion
        return self
        # except:
        # print("ups")

    @property
    def resultado(self):
        return self.__result

    def __del__(self):
        print("Conexion destruida")


def create(tabla: str, first, *arg):
    values = f"'{first}'" if type(first) == str else f"{first}"
    for i in arg:
        if type(i) == str:
            values += f", '{i}'"
        else:
            values += f", {i}"

    query = f"INSERT INTO {tabla} VALUES ({values})"
    Conexion().start(query)


def createUser(name: str, password: str) -> str:
    try:
        create("usuario", name, password)
        return "Creando usuario"
    except:
        return "Usuario ya existe"


def updateUser(name: str, newPass: str):
    query = f"UPDATE usuario SET password='{newPass}' WHERE nombre='{name}';"
    Conexion().start(query)


def updateCant(id: int, cant: int, mode: str = "+"):
    query = f"UPDATE productos SET stock=stock{mode} {cant} WHERE id={id}"

    Conexion().start(query)


def creatProduct(pname: str, precio: float, stock: int, des: str):
    if stock < 1:
        raise Exception
    query = f"INSERT INTO productos (pname, precio,stock, descripcion) VALUES ('{pname}',{precio}, {stock}, '{des}')"
    Conexion().start(query)


def delete():
    pass


def read(tabla, column="", value="", control="all"):
    if control == "all":
        query = f"SELECT * FROM {tabla}"
    elif control == "alike":
        query = f"SELECT * FROM {tabla} WHERE {column} LIKE '%{value}%'"
    elif control == "exact":
        query = f"SELECT * FROM {tabla} WHERE {column}={value}"

    return Conexion().start(query).resultado


def readProductos():
    return read("productos")


def searchProducto(value):
    return read("productos", "pname", value, "alike")


def searchProductoByID(id):
    return read("productos", "id", id, "exact")


def searchUser(name: str, level=0) -> 1 or 0:
    query = f"SELECT EXISTS (SELECT 1 FROM admin WHERE nombre='{name}')"
    if not level:
        query = f"SELECT EXISTS (SELECT 1 FROM usuario WHERE nombre='{name}')"

    return Conexion().start(query).resultado[0][0]

def searchUserPass(name: str, password: str, level=False):
    query = f"SELECT EXISTS (SELECT 1 FROM admin WHERE nombre='{name}' AND password='{password}')"

    if not level:
        query = f"SELECT EXISTS (SELECT 1 FROM usuario WHERE nombre='{name}' AND password='{password}')"

    return Conexion().start(query).resultado[0][0]


def validar(name: str, password: str, level=False) -> str:
    if searchUser(name, level):
        return (
            "Ingresando"
            if searchUserPass(name, password, level)
            else "Contraseña incorrecta"
        )
    return "No existe este usuario"
