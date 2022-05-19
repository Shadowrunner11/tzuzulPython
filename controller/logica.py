import re
from bussines import *
from passlib.context import CryptContext
from tkinter import Tk
from view import login

pwd_context = CryptContext(
    schemes=["pbkdf2_sha256"],
    default="pbkdf2_sha256",
    pbkdf2_sha256__default_rounds=30000,
)


class Controller:
    def __init__(self, lite=True):
        
        print("Inicio")

    def start(self):
        self.RootLogin = Tk()
        self.__AppLogin = login.Login(parent=self.RootLogin)
        self.__AppLogin.accionBtnIngreso(self.__wrapper)
        self.__AppLogin.accionBtnRegNew(self.___wrapper2)
        self.__AppLogin.mainloop()
        self.__AppLogin.destroy()

    def conect(self, login:login.Login):
        self.__AppLogin=login
        self.__AppLogin.accionBtnIngreso(self.__wrapper)
        

    def __wrapper(self) -> None:
        mensaje = (
            self.validarBas()
            if self.validarLen(self.correctInfo(self.__AppLogin.user))
            else "Campos vacios"
        )
        self.__AppLogin.passw.set("")
        self.__AppLogin.message(mensaje)
        if mensaje == "Ingresando":
            self.RootLogin.destroy()
            Controller2(self.__AppLogin.user2.get())

    def ___wrapper2(self) -> None:
        dictio = self.correctInfo(self.__AppLogin.newUser)
        mensaje = "Campos incompletos"
        if self.validarLen(dictio):
            mensaje = (
                createUser(dictio["Name"], dictio["Pass"])
                if self.validarNew()
                else "No coinciden las contraseñas"
            )
        self.__AppLogin.passw.set("")
        self.__AppLogin.message(mensaje)

    def validarBas(self) -> str:
        dictio = self.correctInfo(self.__AppLogin.user)
        return validar(dictio["Name"], dictio["Pass"], self.__AppLogin.level)

    def validarNew(self) -> bool:
        dictio = self.correctInfo(self.__AppLogin.newUser)
        return dictio["Pass"] == dictio["NPass"]

    @staticmethod
    def valQuery(regex: str, query:str)->bool:
        flag = re.compile(regex)
        return bool(flag.fullmatch(query))

    
    def correctInfo(self, karg:dict)->dict:
        """
        Solo consideramos letras, numeros y ._- para evitar inyecciones
        """                
        dictio = {}
        for key, value in karg.items():
            dictio[key]=value if self.valQuery('[a-zA-Z0-9._-]+', value) else ""

        return dictio
            



    @staticmethod
    def validarLen(karg: dict) -> bool:
        flag = True
        for value in karg.values():
            flag = len(value) > 0

        return flag

    @staticmethod
    def encryptarPass(password: str) -> str:
        return pwd_context.encrypt(password)


class Controller2:
    def __init__(self, cajero_name: str):
        self.listaId = []
        self.datos = {}
        self.datos2=[]
        self.RootLogin = Tk()
        self.__AppLogin = login.PointSale(parent=self.RootLogin)
        self.__Admin = self.__AppLogin.login
        Controller().conect(self.__Admin)
        self.__AppLogin.lblCajero["text"]=f"Cajero: {cajero_name}"
        self.__tabla = self.__AppLogin.treeCatalogo
        self.__boleta = self.__AppLogin.treeBoleta
        self.__AppLogin.actualizar(readProductos(), self.__tabla)
        text = self.__AppLogin.textProduct
        text.trace("w", lambda x, y, z: self.search(text.get() if Controller().valQuery('[a-zA-Z ]+',text.get()) else ""))
        self.__AppLogin.addCommandAdd(self.add)
        self.__AppLogin.addCommandCancel(self.cancel)
        self.__AppLogin.addCommandNuevo(self.addProdAlmacen)
        self.__AppLogin.addCommandVenta(self.wrapperLogis)
        self.__AppLogin.addCommandAlm(self.wrapperLogis2)
        self.__AppLogin.addCommandBorrar(self.borrar)
        self.__Admin.accionBtnIngreso(self.permiso)
        self.__Admin.accionBtnBloq(self.bloquear)
        self.__AppLogin.mainloop()
        self.__AppLogin.destroy()

    def wrapperLogis(self):
        self.logistica("-")
        self.recibo() 
        self.cancel()

    def wrapperLogis2(self):
        self.logistica("+")
           
        self.cancel()

    def recibo(self):
        string=""
        for item in self.datos:
            for dato in self.datos[item]:
                string+=f" {dato}"
            string+="\n"    
        with open(".//venta.txt","w+") as recibo:
            recibo.write(
    f"""
    Teletubies SAC
    RUC 1111111111

    Nombre :{self.__AppLogin.frClient.NombreCliente.get()}
    DNI : {self.__AppLogin.frClient.dniCliente.get()}

{string}
    {self.__AppLogin.total.get()}
    
    {self.__AppLogin.lblCajero["text"]}
    Que tenga buen dia
    """
)
            
    def borrar(self):
        print(self.__boleta.selection())
        for index in self.__boleta.selection():
            del self.datos[self.__boleta.item(index)["values"][2]]
        self.__boleta.delete(self.__boleta.selection())
        total=sum([float(self.__boleta.item(index)["values"][1]) for index in self.__boleta.get_children()])
        self.__AppLogin.total.set(f"Total: {total}" )
        print(self.datos)

    def search(self, value):

        self.__AppLogin.borrar(self.__tabla)
        self.__AppLogin.actualizar(searchProducto(value), self.__tabla)

    def add(self):

        cant = self.__AppLogin.cantidad.get()
       
        if cant < 0:
            raise Exception
        for index in self.__AppLogin.getTablaSeleccion(self.__tabla):
            self.datos[self.__tabla.item(index)["text"]]=[
                    self.__tabla.item(index)["values"][0],
                    cant,
                    cant * float(self.__tabla.item(index)["values"][1]),
                    self.__tabla.item(index)["text"]

            ]
        self.datos2=[self.datos[value] for value in self.datos]    

        self.__AppLogin.borrar(self.__boleta)  
        self.__AppLogin.actualizar(self.datos2, self.__boleta)  
        total=sum([float(self.__boleta.item(index)["values"][1]) for index in self.__boleta.get_children()])       
        
        self.__AppLogin.total.set(f"Total: {total}" )
        self.__AppLogin.cantidad.set(1)

    def cancel(self):
        self.__AppLogin.borrar(self.__boleta)
        self.listaId = []
        self.datos2 = []
        self.datos={}

    def logistica(self, mode: str = "+"):
        for item in self.datos:
            print (item)
            print (self.datos[item])
            updateCant(self.datos[item][3], self.datos[item][1], mode)
        self.search("")

    def permiso(self):
        del self.__Admin
        self.__Admin=self.__AppLogin.login
        self.__Admin.message("")
        
        mensaje = (
            self.validarBas()
            if Controller().validarLen(self.__Admin.user)
            else "Campos vacios"
        )
        
        self.__Admin.message(mensaje)
        if self.__Admin.labelVerif["text"] == "Ingresando":
            modif = [
                self.__AppLogin.btnAlm,
                self.__AppLogin.btnDevol,
                self.__AppLogin.btnAlm,
                self.__AppLogin.txtCantidadProd,
                self.__AppLogin.txtNombreProd,
                self.__AppLogin.txtDesProd,
                self.__AppLogin.txtPrecioProd,
                self.__Admin.btnBloquear,
                self.__AppLogin.btnNuevo,
            ]

            for item in modif:
                item.configure(state="normal")

            self.__Admin.user2.set("")
        self.__Admin.passw.set("")
        
        

    def bloquear(self):
        modif = [
            self.__AppLogin.btnAlm,
            self.__AppLogin.btnDevol,
            self.__AppLogin.btnAlm,
            self.__AppLogin.txtCantidadProd,
            self.__AppLogin.txtNombreProd,
            self.__AppLogin.txtDesProd,
            self.__AppLogin.txtPrecioProd,
            self.__Admin.btnBloquear,
            self.__AppLogin.btnNuevo,
        ]

        for item in modif:
            item.configure(state="disabled")
        self.__Admin.labelVerif["text"] = ""

    def validarBas(self):
        dictio = self.__Admin.user
        return validar(dictio["Name"], dictio["Pass"], 1)

    def addProdAlmacen(self):
        try:
            cantidad = self.__AppLogin.cantidadProd.get()
            des = self.__AppLogin.desProd.get()
            precio = self.__AppLogin.precioProd.get()
            nombre = self.__AppLogin.nombreProd.get()

            creatProduct(nombre, precio, cantidad, des)
            self.__AppLogin.cantidadProd.set(0)
           
            self.__AppLogin.desProd.set("")
            self.__AppLogin.precioProd.set(0)
            self.__AppLogin.nombreProd.set("")

        except:
            print("No se registro prodcuto")
        self.search("")

if __name__=="__main__":
    controler = Controller().start()
