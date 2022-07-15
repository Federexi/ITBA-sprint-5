#importo el json 
import json

with open("tps.json", "r") as f:
    data = json.load(f)

print(data)

#clases Cuenta, Direccion y Cliente
class Cuenta:
    def __Init__(self, limite_extraccion_diario, limite_transferencia_recibida, monto, costo_transferencias, saldo_descubierto_disponible):
        self.__limite_extraccion_diario = limite_extraccion_diario #encapsulo todos los atributos con doble guión bajo
        self.__limite_transferencia_recibida = limite_transferencia_recibida
        self.__monto = monto
        self.__costo_transferencias = costo_transferencias
        self.__saldo_descubierto_disponible = saldo_descubierto_disponible

    #Métodos get con el decorador property para acceder a los atributos encapsulados
    @property
    def limite_extraccion(self):
        return self.__limite_extraccion_diario

    @property
    def limite_transferencia(self):
        return self.__limite_transferencia_recibida

    @property
    def monto(self):
        return self.__monto

    @property
    def costo_transferencias(self):
        return self.__costo_transferencias

    @property
    def saldo_disponible(self):
        return self.__saldo_descubierto_disponible

class Direccion: 
    def __init__(self, calle, numero_direccion, ciudad, provincia, pais):
        self.__calle = calle 
        self.__numero_direccion = numero_direccion
        self.__ciudad = ciudad 
        self.__provincia = provincia
        self.__pais = pais

    @property
    def calle(self):
        return self.__calle

    @property
    def numero_direccion(self):
        return self.__numero_direccion

    @property
    def ciudad(self):
        return self.__ciudad

    @property
    def provincia(self):
        return self.__provincia

    @property
    def pais(self):
        return self.__pais

class Cliente:
    def __init__(self, nombre, apellido, numero, dni, tipo, calle, numero_direccion, ciudad, provincia, pais, transacciones=[]):
        self.__nombre = nombre
        self.__apellido = apellido 
        self.__numero = numero
        self.__dni = dni
        self.__tipo = tipo
        self.__transacciones = transacciones
        self.__direccion = Direccion(calle, numero_direccion, ciudad, provincia, pais) 
        self.__cuenta = Cuenta()

    @property
    def nombre(self):
        return self.__nombre

    @property
    def apellido(self):
        return self.__apellido

    @property
    def numero(self):
        return self.__numero

    @property
    def dni(self):
        return self.__dni

    @property
    def tipo(self):
        return self.__tipo

    @property
    def transacciones(self):
        return self.__transacciones

    @property
    def direccion(self):
        return self.__direccion

    @property
    def cuenta(self):
        return self.__cuenta

#Las clases Classic, Gold y Black heredan de la clase Cliente
class Classic(Cliente):
    def __init__(self, nombre, apellido, numero, dni, tipo, calle, numero_direccion, ciudad, provincia, pais, transacciones=[]): #no se porque toma como código muerto a transacciones=[] en esta línea, si funcionan los métodos que haga Agustín, entonces borrar transacciones=[] en esta línea
        super().__init__(nombre, apellido, numero, dni, tipo, calle, numero_direccion, ciudad, provincia, pais, transacciones=[])

class Gold(Cliente):
    def __init__(self, nombre, apellido, numero, dni, tipo, calle, numero_direccion, ciudad, provincia, pais, transacciones=[]): #lo mismo que dije en Classic sobre transacciones=[]
        super().__init__(nombre, apellido, numero, dni, tipo, calle, numero_direccion, ciudad, provincia, pais, transacciones=[])

class Black(Cliente):
    def __init__(self, nombre, apellido, numero, dni, tipo, calle, numero_direccion, ciudad, provincia, pais, transacciones=[]): #lo mismo que dije en Classic sobre transacciones=[]
        super().__init__(nombre, apellido, numero, dni, tipo, calle, numero_direccion, ciudad, provincia, pais, transacciones=[])

#Creación de la clase Razon, asociada con la clase Cliente
class Razon:
    def __init__(self, razon):
        self.__razon = razon

    @property 
    def razon(self):
        return self.__razon

#Las siguientes clases heredan de la clase Razon
class Razon_alta_chequera(Razon):
    def __init__(self, razon):
        super().__init__(razon)

class Razon_alta_tarjeta_credito(Razon):
    def __init__(self, razon):
        super().__init__(razon)

class Razon_compra_dolar(Razon):
    def __init__(self, razon):
        super().__init__(razon)

class Razon_retiro_efectivo_cajero_automatico(Razon):
    def __init__(self, razon):
        super().__init__(razon)

class Razon_transferencia_enviada(Razon):
    def __init__(self, razon):
        super().__init__(razon)

class Razon_transferencia_recibida(Razon):
    def __init__(self, razon):
        super().__init__(razon)