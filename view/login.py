from ast import Str
from tkinter import *
from tkinter.font import Font
from tkinter import ttk
from typing import ItemsView


class Login(Frame):
    cont = 0

    def __init__(self, parent=None, lite=True):
        super(Login, self).__init__(parent)
        self.parentIn = parent
        self.lite=lite
        self.__iniciar(self.parentIn, "Iniciando", lite)

    def __iniciar(self, parent: Tk, debuggerMessage: str, lite=True) -> None:
        """
        Introducimos los widgets a la ventana principal
        """
        print(debuggerMessage)

        self.gap = 8
        self.bg = "#101010"
        self.fg1 = "#003566"
        self.fg2 = "#fff"
        self.fontFam1 = Font(family="Tahoma", size=17, weight="bold")
        self.fontFam2 = Font(family="Arial", size=15)

        if lite == True:
            parent.title("Login")
            self.toggleTheme = Button(parent, command=self.cambiarColor)
            self.toggleTheme.grid(
                column=0, row=0, sticky="W", padx=self.gap, pady=self.gap
            )

        if lite != True:
            self.gap = 2
            self.bg = "#e1e1e1"
            self.fg1 = "#000"
            self.fg2 = "#000"
            self.fontFam1 = Font(family="Arial", size=10)
            self.fontFam2 = Font(family="Arial", size=10)

        parent.configure(bg=self.bg)

        mode = IntVar()

        self.__lfUser = LabelFrame(
            parent, text="Inicio", font=self.fontFam2, fg=self.fg2, bg=self.bg
        )
        if lite == False:
            self.__lfUser["text"] = "Admin"
        self.__lfUser.grid(column=0, row=1, columnspan=2, padx=self.gap, pady=self.gap)

        self.labelUser = Label(
            self.__lfUser, text="Usuario", font=self.fontFam1, fg=self.fg2, bg=self.bg
        )
        self.labelUser.grid(column=0, row=0, padx=self.gap, pady=self.gap)
        self.user2 = StringVar()
        self.txtUser = Entry(
            self.__lfUser,
            text="Ingrese su usuario",
            font=self.fontFam1,
            textvariable=self.user2,
        )
        self.txtUser.grid(column=1, row=0, padx=self.gap, pady=self.gap)

        self.labelContra = Label(
            self.__lfUser,
            text="Contraseña",
            font=self.fontFam1,
            fg=self.fg2,
            bg=self.bg,
        )
        self.labelContra.grid(column=0, row=1, padx=self.gap, pady=self.gap)
        self.passw = StringVar(None)
        self.txtPass = Entry(
            self.__lfUser, show="*", font=self.fontFam1, textvariable=self.passw
        )
        self.txtPass.grid(column=1, row=1, padx=self.gap, pady=self.gap)

        self.labelVerif = Label(
            self.__lfUser, text="", font=self.fontFam1, fg="#bb3e03", bg=self.bg
        )
        self.labelVerif.grid(
            column=0, row=2, columnspan=2, padx=self.gap, pady=self.gap
        )

        self.__btnIngresar = Button(
            parent, text="Ingresar", font=self.fontFam1, fg="white", bg=self.fg1
        )

        self.__btnIngresar.grid(
            column=0, row=2, padx=self.gap, pady=self.gap, sticky="WE"
        )

        self.btnBloquear = Button(
            parent,
            text="Bloquear",
            font=self.fontFam1,
            bg=self.bg,
            fg=self.fg2,
            state=DISABLED,
        )
        if lite == False:
            self.__btnIngresar.configure(text="Permiso", bg=self.bg, fg=self.fg2)
            self.__btnIngresar.grid_configure(columnspan=2)
            self.btnBloquear.grid(
                column=0, row=3, columnspan=2, padx=self.gap, pady=self.gap, sticky="WE"
            )

        self.__btnRegistrar = Button(
            parent,
            text="Nuevo",
            font=self.fontFam1,
            fg="white",
            bg=self.fg1,
            command=self.accionBtnRegistro,
        )

        if lite == True:
            self.__btnRegistrar.grid(
                column=1, row=2, padx=self.gap, pady=self.gap, sticky="WE"
            )

        self.__btnRegisNew = Button(
            parent,
            text="Registrar",
            font=self.fontFam1,
            fg="white",
            bg=self.fg1,
        )
        self.__btnRegresar = Button(
            parent,
            text="Regresar",
            font=self.fontFam1,
            fg="white",
            bg=self.fg1,
            command=self.regresar,
        )
        self.lista = [
            self.parentIn,
            self.labelVerif,
            self.labelUser,
            self.__lfUser,
            self.labelContra,
        ]
        self.listabtn = [
            self.__btnRegisNew,
            self.__btnRegistrar,
            self.__btnIngresar,
            self.__btnRegresar,
        ]
        self.listalabel = [
            self.labelContra,
            self.labelUser,
            self.labelUser,
            self.__lfUser,
        ]
    
    @property
    def user(self) -> dict:
        """
        Getter de los datos del usuario
        """
        return {"Name": self.user2.get(), "Pass": self.passw.get()}

    @property
    def newUser(self) -> dict:
        return {
            "Name": self.txtUser.get(),
            "Pass": self.txtPass.get(),
            "NPass": self.__txtPass2.get(),
        }

    @property
    def level(self)->1 or 0:
        return not self.lite

    def accionBtnBloq(self, accion):
        self.btnBloquear["command"] = accion

    def message(self, text: str) -> None:
        self.labelVerif["text"] = text

    def accionBtnIngreso(self, accion) -> None:
        self.__btnIngresar["command"] = accion

    def accionBtnRegNew(self, accion) -> None:
        self.__btnRegisNew["command"] = accion

    def accionBtnRegistro(self) -> None:
        self.labelVerif["text"] = ""
        self.__btnIngresar.grid_remove()
        self.__btnRegistrar.grid_remove()
        self.__btnRegisNew.grid(column=0, row=2, sticky="WE", padx=self.gap)
        self.__btnRegresar.grid(column=1, row=2, sticky="WE", padx=self.gap)
        self.__lfUser["text"] = "Registro"
        new_bg = "#f3f3f3" if self.cont % 2 else self.bg
        new_fg = "#12aaff" if self.cont % 2 else self.fg2
        self.labelContra2 = Label(
            self.__lfUser, text="Confirmar", font=self.fontFam1, fg=new_fg, bg=new_bg
        )
        self.labelContra2.grid(column=0, row=2, padx=self.gap, pady=self.gap)
        self.lista.append(self.labelContra2)
        self.listalabel.append(self.labelContra2)

        self.__txtPass2 = Entry(self.__lfUser, show="*", font=self.fontFam1)
        self.__txtPass2.grid(column=1, row=2, padx=self.gap, pady=self.gap)

        self.labelVerif.grid(column=0, row=3)

    def cambiarColor(self) -> None:
        self.labelVerif["text"] = ""
        self.cont += 1
        new_bg = "#f3f3f3" if self.cont % 2 else self.bg
        new_fg = "#12aaff" if self.cont % 2 else self.fg2
        self.toogle(self.lista, new_bg)
        self.toogleFont(self.listalabel, new_fg)
        self.toogleFont(self.listabtn, new_fg)

    @staticmethod
    def toogle(lista: list, back: str) -> None:
        for e in lista:
            e.configure(bg=back)

    @staticmethod
    def toogleFont(lista: list, back: str) -> None:
        for e in lista:
            e.configure(fg=back)

    def regresar(self):
        self.labelVerif["text"] = ""
        self.labelContra2.grid_remove()
        self.__txtPass2.grid_remove()
        self.__btnRegisNew.grid_remove()
        self.__btnRegresar.grid_remove()
        self.__btnIngresar.grid()
        self.__btnRegistrar.grid()


class PointSale(Frame):
    def __init__(self, parent=None):
        super(PointSale, self).__init__(parent)
        self.parentIn = parent
        self.__iniciar(self.parentIn, "Iniciando")

    def __iniciar(self, parent: Tk, debuggerMessage: str) -> None:
        """
        Introducimos los widgets a la ventana principal
        """
        print(debuggerMessage)
        self.gap = 3
        self.bg = "#101010"
        self.fg1 = "#003566"
        self.fg2 = "#fff"
        self.fontFam1 = Font(family="Tahoma", size=17, weight="bold")
        self.fontFam2 = Font(family="Arial", size=15)

        # parent.configure(bg=self.bg)
        parent.title("Teletubies SAC")

        self.frVender = Frame(parent)
        self.frVender.pack(side="left", fill=BOTH)

        self.lblCajero = Label(self.frVender)
        self.lblCajero.pack(pady=self.gap)

        self.lblFrBuscar = LabelFrame(self.frVender, text="Buscar")
        self.lblFrBuscar.pack(pady=self.gap)

        self.lblFiltro = Label(self.lblFrBuscar, text="Filtrar")
        self.lblFiltro.grid(column=0, row=0, sticky="w", pady=self.gap)

        self.filtro = IntVar(None, 1)
        self.radioNombre = Radiobutton(
            self.lblFrBuscar, text="Nombre", variable=self.filtro, value=1
        )
        self.radioNombre.grid(column=0, row=1, sticky="w", pady=self.gap)

        self.radioId = Radiobutton(
            self.lblFrBuscar, text="Codigo", variable=self.filtro, value=2
        )
        self.radioId.grid(column=1, row=1, pady=self.gap)

        # self.lblProduct = Label(self.lblFrBuscar, text="Producto")
        # self.lblProduct.grid(column=0, row=0)
        self.textProduct = StringVar()
        # self.textProduct.trace("w", lambda x, y, z:print(textProduct.get()) )

        self.txtProduct = Entry(self.lblFrBuscar, textvariable=self.textProduct)
        self.txtProduct.grid(column=0, row=2, columnspan=2, sticky="we", pady=self.gap)
        
        self.frAdd = LabelFrame(self.frVender, text="cantidad")
        self.frAdd.pack(expand=1, pady=self.gap)

        self.cantidad = IntVar(None, 1)

        self.txtAdd = Entry(self.frAdd, textvariable=self.cantidad)
        self.txtAdd.grid(column=0, row=0, pady=self.gap)

        self.btnAdd = Button(self.frAdd, text="Add")        
        self.btnAdd.grid(column=1, row=0, pady=self.gap)

        self.treeBoleta = ttk.Treeview(self.frVender, columns=["0", "1", "2"], displaycolumns=["0","1"])

        self.treeBoleta.column("#0", width=180)
        self.treeBoleta.column("#1", width=60)
        self.treeBoleta.column("#2", width=60)
        self.treeBoleta.pack(fill=Y)

        self.btnBorrar=Button(self.frVender, text="Borrar")
        self.btnBorrar.pack(expand=1)

        self.total = StringVar()
        self.lbltotal = Label(self.frVender, textvariable=self.total, text="Total")
        self.lbltotal.pack(anchor=E, padx=self.gap)

        self.frClient = Cliente(self.frVender)
        self.frClient.pack(pady=self.gap)

        self.frOpciones = Frame(self.frVender)
        self.frOpciones.pack(expand=1, pady=self.gap)

        self.btnAceptar = Button(self.frOpciones, text="VENTA")
        self.btnAceptar.grid(column=0, row=0, sticky=W + E)

        self.btnCancel = Button(self.frOpciones, text="CANCELAR")
        self.btnCancel.grid(column=1, row=0, sticky=W + E)

        self.btnAlm = Button(self.frOpciones, text="ALMACEN", state="disabled")
        self.btnAlm.grid(column=0, row=1, sticky=W + E)

        self.btnDevol = Button(self.frOpciones, text="DEVOLUCION", state="disabled")
        self.btnDevol.grid(column=1, row=1, sticky=W + E)

        self.frAdmin = Frame(self.frVender)
        self.frAdmin.pack()

        self.login = Login(self.frAdmin, False)
        self.login.grid(column=0, row=0, columnspan=2)

        self.treeCatalogo = ttk.Treeview(parent, columns=["0", "1", "2", "3"])
        self.treeCatalogo.pack(expand=1, fill=BOTH)

        self.frNuevo = Frame(parent)
        self.frNuevo.pack(side="bottom")

        self.nombreProd = StringVar()
        self.lblNombreProd = Label(self.frNuevo, text="Nombre")
        self.txtNombreProd = Entry(
            self.frNuevo, state="disabled", textvariable=self.nombreProd
        )

        self.precioProd = DoubleVar()
        self.lblPrecioProd = Label(self.frNuevo, text="Precio")
        self.txtPrecioProd = Entry(
            self.frNuevo, state="disabled", textvariable=self.precioProd
        )

        self.cantidadProd = IntVar()
        self.lblCantidadProd = Label(self.frNuevo, text="Cantidad")
        self.txtCantidadProd = Entry(
            self.frNuevo, state="disabled", textvariable=self.cantidadProd
        )

        self.desProd = StringVar()
        self.lblDesProd = Label(self.frNuevo, text="Descripcion")
        self.txtDesProd = Entry(
            self.frNuevo, state="disabled", textvariable=self.desProd
        )

        listaNuevo = [
            self.lblNombreProd,
            self.lblPrecioProd,
            self.lblCantidadProd,
            self.lblDesProd,
        ]

        listaNuevo2 = [
            self.txtNombreProd,
            self.txtPrecioProd,
            self.txtCantidadProd,
            self.txtDesProd,
        ]

        for i in range(len(listaNuevo)):

            listaNuevo[i].grid(column=i, row=0, padx=self.gap, pady=self.gap)

            listaNuevo2[i].grid(column=i, row=1, padx=self.gap, pady=(0, self.gap))

        self.btnNuevo = Button(self.frNuevo, text="Add", state="disabled")
        self.btnNuevo.grid(column=4, row=0, rowspan=2)

    def actualizar(self, datos: list, tabla: ttk.Treeview) -> None:
        cant = len(datos)
        for i in range(cant):
            item = tabla.insert("", i, text=datos[i][0])
            for j in range(len(datos[0]) - 1):
                tabla.set(item, f"{j}", f"{datos[i][j+1]}")

    def borrar(self, tabla):
        tabla.delete(*tabla.get_children())

    def getTablaSeleccion(self, tabla: ttk.Treeview):
        return tabla.selection()

    def addCommandAdd(self, function):
        self.btnAdd["command"] = function

    def addCommandCancel(self, function):
        self.btnCancel["command"] = function

    def addCommandNuevo(self, function):
        self.btnNuevo["command"] = function

    def addCommandVenta(self, function):
        self.btnAceptar["command"] = function

    def addCommandAlm(self, function):
        self.btnAlm["command"] = function
    
    def addCommandBorrar(self, function):
        self.btnBorrar["command"] = function


class Cliente(Frame):
    def __init__(self, parent=None):
        super(Cliente, self).__init__(parent)
        self.lblFrClient = LabelFrame(self, text="Cliente")
        self.lblFrClient.pack()

        self.lblNombreCliente = Label(self.lblFrClient, text="Nombre")
        self.lblNombreCliente.grid(column=0, row=0)

        self.NombreCliente = StringVar()

        self.txtNombreCliente = Entry(self.lblFrClient, textvariable=self.NombreCliente)
        self.txtNombreCliente.grid(column=1, row=0)

        self.lblDniCliente = Label(self.lblFrClient, text="DNI")
        self.lblDniCliente.grid(column=0, row=1)

        self.dniCliente = IntVar()
        self.txtDniCliente = Entry(self.lblFrClient, textvariable=self.dniCliente)
        self.txtDniCliente.grid(column=1, row=1)
