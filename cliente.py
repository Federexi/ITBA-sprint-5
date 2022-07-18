
import sys
import json
from jsonschema import ValidationError, validate
from jinja2 import Environment, PackageLoader, select_autoescape

argumentos = sys.argv #guardo en variable los datos pasados por terminal

if not len(argumentos) == 2: #chequeo cantidad correcta de argumentos
    print('La cantidad de argumentos es incorrecta')
    exit(1)

archivo = argumentos[1] #declaro el nombre del archivo como el segundo argumento pasado por terminal    

schema = { #declaro el schema que debera tener el JSON
    "type" : "object",
    "properties" : {
        "numero": {"type": "number"},
        "nombre": {"type": "string"},
        "apellido": {"type": "string"},
        "DNI": {"type": "string"},
        "tipo": {"enum": ["BLACK","CLASSIC","GOLD"]},
        "direccion": {
            "type": "object",
            "properties": {
                "calle": {"type": "string"},
                "numero": {"type": "string"},
                "ciudad": {"type": "string"},
                "provincia": {"type": "string"},
                "pais": {"type": "string"},
            }
        },
        "transacciones": {
            "type": "array",
            "items": {
                "type" : "object",
                "properties" : {
                    "estado": {"enum": ["ACEPTADA","RECHAZADA"]},
                    "tipo": {"enum": ["RETIRO_EFECTIVO_CAJERO_AUTOMATICO","ALTA_TARJETA_CREDITO","ALTA_CHEQUERA","COMPRAR_DOLAR","COMPRA_DOLAR","TRANSFERENCIA_ENVIADA","TRANSFERENCIA_RECIBIDA"]},
                    "cuentaNumero": {"type": "number"},
                    "cupoDiarioRestante": {"type": "number"},
                    "monto": {"type": "number"},
                    "fecha": {"type": "string"},
                    "numero": {"type": "number"},
                    "saldoEnCuenta": {"type": "number"},
                    "totalTarjetasDeCreditoActualmente": {"type": "number"},
                    "totalChequerasActualmente": {"type": "number"}
                }
            }
        }
    }
}

try: #chequeo excistencia y lectura correcta del archivo
    with open(archivo, "r") as f:
        data = json.load(f)
        try: #chequeo formateo del JSON
            validate(instance=data, schema=schema)
        except:
            print('El archivo se encuentra mal formado')
            exit(1)

except IOError:
    print('El archivo ingresado es inexistente')
    exit(1)

except json.JSONDecodeError:
    print('El archivo ingresado no tiene contenido')
    exit(1)


#clases Cuenta, Direccion y Cliente
class Cuenta:
    def __init__(self, limite_extraccion_diario, limite_transferencia_recibida, monto, costo_transferencias, saldo_descubierto_disponible):
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
    
    #setters para modificar los valores encapsulados
    @limite_extraccion.setter
    def limite_extraccion(self,nuevoValor):
        self.__limite_extraccion_diario = nuevoValor
    
    @limite_transferencia.setter
    def limite_transferencia(self,nuevoValor):
        self.__limite_transferencia_recibida = nuevoValor

    @monto.setter
    def monto(self,nuevoValor):
        self.__monto = nuevoValor

    @saldo_disponible.setter
    def saldo_disponible(self,nuevoValor):
        self.__saldo_descubierto_disponible = nuevoValor

    @costo_transferencias.setter
    def costo_transferencias(self,nuevoValor):
        self.__costo_transferencias = nuevoValor

class Direccion: #clase direccion dependiente de Cliente ya que se genera en su interior
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
    def __init__(self, nombre, apellido, numero, dni, tipo, calle, numero_direccion, ciudad, provincia, pais, objCuenta, transacciones=[]):
        self.__nombre = nombre
        self.__apellido = apellido 
        self.__numero = numero
        self.__dni = dni
        self.__tipo = tipo
        self.__transacciones = transacciones
        self.__direccion = Direccion(calle, numero_direccion, ciudad, provincia, pais) 
        self.__cuenta = objCuenta
    
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
    def __init__(self, nombre, apellido, numero, dni, tipo, calle, numero_direccion, ciudad, provincia, pais, objCuenta, transacciones=[], cantChequeras=0, cantTarj=0): 
        super().__init__(nombre, apellido, numero, dni, tipo, calle, numero_direccion, ciudad, provincia, pais, objCuenta, transacciones)
        self.__limiteChequeras = 0 #asigno variables arbitrariamente segun lo estipulado en los parametros de la consigna
        self.__cantChequeras = cantChequeras
        self.__limiteTarj = 0
        self.__cantTarj = cantTarj
        self.__accesoDolar = 'NO'
    
    @property
    def limiteChequeras(self):
        return self.__limiteChequeras
    @property
    def cantChequeras(self):
        return self.__cantChequeras
    @property
    def limiteTarj(self):
        return self.__limiteTarj
    @property
    def cantTarj(self):
        return self.__cantTarj
    @property
    def accesoDolar(self):
        return self.__accesoDolar
    @cantChequeras.setter
    def cantChequeras(self,nuevoValor):
        self.__cantChequeras = nuevoValor
    @cantTarj.setter
    def cantTarj(self,nuevoValor):
        self.__cantTarj = nuevoValor

    #funciones dependientes de la clase Classic que utilizan los nuevos parametros asignados, inexistentes en Cliente
    def puede_comprar_dolar(self):
        if self.__accesoDolar == 'NO':
            return False
        else:
            return True

    def puede_crear_chequera(self):
        if self.__cantChequeras < self.__limiteChequeras:
            return True
        else:
            return False        
    
    def puede_crear_tarjeta_credito(self):
        if self.__cantTarj < self.__limiteTarj:
            return True
        else:
            return False
    
    #funciones Filtro a las cuales se accede unicamente si se cumple la igualdad en el tipo de operacion de la transaccion correspondiente
    def filtro_compra_dolar(self,iterador,index):       
        if self.puede_comprar_dolar():
            if iterador['monto'] > iterador['saldoEnCuenta']:
                globals()[f"razon{index}"] = Razon_compra_dolar('Fondos insuficientes')
                return globals()[f"razon{index}"].razon
            else:
                globals()[f"razon{index}"] = Razon_compra_dolar('Razon desconocida')
                return globals()[f"razon{index}"].razon
        else:
            globals()[f"razon{index}"] = Razon_compra_dolar(f'Los clientes {self.tipo} no pueden comprar dolares')
            return globals()[f"razon{index}"].razon


    def filtro_alta_tarj(self,index):
        if self.puede_crear_tarjeta_credito():
            globals()[f"razon{index}"] = Razon_alta_tarjeta_credito('Razon desconocida')
            return globals()[f"razon{index}"].razon
        else:
            globals()[f"razon{index}"] = Razon_alta_tarjeta_credito('Alcanzo el limite de tarjetas de credito')
            return globals()[f"razon{index}"].razon

    def filtro_alta_chequera(self,index):  
        if self.tipo == 'CLASSIC':
            globals()[f"razon{index}"] = Razon_alta_chequera(f'Los clientes {self.tipo} no pueden solicitar chequeras')
            return globals()[f"razon{index}"].razon
        else:
            if self.puede_crear_chequera():
                globals()[f"razon{index}"] = Razon_alta_chequera('Razon desconocida')
                return globals()[f"razon{index}"].razon
            else:
                globals()[f"razon{index}"] = Razon_alta_chequera('Alcanzo el limite de chequeras')
                return globals()[f"razon{index}"].razon

    def filtro_retiro_efectivo_cajero(self,iterador,index): 
        if self.tipo == 'CLASSIC':
            if iterador['monto'] > iterador['saldoEnCuenta']:
                globals()[f"razon{index}"] = Razon_retiro_efectivo_cajero_automatico('Saldo en cuenta insuficiente')
                return globals()[f"razon{index}"].razon
            elif iterador['monto'] > iterador['cupoDiarioRestante']:
                globals()[f"razon{index}"] = Razon_retiro_efectivo_cajero_automatico('La operacion excede el limite de cupo diario restante')
                return globals()[f"razon{index}"].razon
            else:
                globals()[f"razon{index}"] = Razon_retiro_efectivo_cajero_automatico('Razon desconocida')
                return globals()[f"razon{index}"].razon
        else:
            if iterador['monto'] > iterador['saldoEnCuenta'] + self.cuenta.saldo_disponible:
                globals()[f"razon{index}"] = Razon_retiro_efectivo_cajero_automatico('Saldo en cuenta insuficiente')
                return globals()[f"razon{index}"].razon
            elif iterador['monto'] > iterador['cupoDiarioRestante']:
                globals()[f"razon{index}"] = Razon_retiro_efectivo_cajero_automatico('La operacion excede el limite de cupo diario restante')
                return globals()[f"razon{index}"].razon
            else:
                globals()[f"razon{index}"] = Razon_retiro_efectivo_cajero_automatico('Razon desconocida')
                return globals()[f"razon{index}"].razon

    def filtro_transf_enviada(self,iterador,index):       
        if iterador['monto'] + iterador['monto']*self.cuenta.costo_transferencias > iterador['saldoEnCuenta'] + self.cuenta.saldo_disponible:
            globals()[f"razon{index}"] = Razon_transferencia_enviada('Saldo en cuenta insuficiente')
            return globals()[f"razon{index}"].razon
        else:
            globals()[f"razon{index}"] = Razon_transferencia_enviada('Razon desconocida')
            return globals()[f"razon{index}"].razon


    def filtro_transf_recibida(self,iterador,index):        
        if iterador['monto'] > self.cuenta.limite_transferencia:
            globals()[f"razon{index}"] = Razon_transferencia_recibida('Excede el monto limite a recibir')
            return globals()[f"razon{index}"].razon
        else:
            globals()[f"razon{index}"] = Razon_transferencia_recibida('Razon desconocida')
            return globals()[f"razon{index}"].razon

    def filtro(self,t,i): #funcion filtro principal que determina si la transaccion se acepto o rechazo y busca las igualdades correspondientes para ejecurar la funcion deseada
        if t['estado'] == 'ACEPTADA':
            globals()[f"razon{i}"] = Razon_nula('')
            return globals()[f"razon{i}"].razon 
        elif t['estado'] == 'RECHAZADA':
            if t['tipo'] == 'COMPRA_DOLAR':
                self.filtro_compra_dolar(t,i)
            elif t['tipo'] == 'ALTA_TARJETA_CREDITO':
                self.filtro_alta_tarj(i)
            elif t['tipo'] == 'ALTA_CHEQUERA':    
                self.filtro_alta_chequera(i)
            elif t['tipo'] == 'RETIRO_EFECTIVO_CAJERO_AUTOMATICO':    
                self.filtro_retiro_efectivo_cajero(t,i)
            elif t['tipo'] == 'TRANSFERENCIA_ENVIADA':    
                self.filtro_transf_enviada(t,i)
            elif t['tipo'] == 'TRANSFERENCIA_RECIBIDA':    
                self.filtro_transf_recibida(t,i)

    def retorno(self): #funcion retorno, encargada de crear una lista que recolecta toda la informacion del cliente y sus transacciones y luego la retorna para utilizarla al exportar el HTML
        lista_transacciones = []
        usuario = [{'nombre_completo':f'{self.nombre} {self.apellido}'},{'numero':self.numero},{'DNI':self.dni},{'direccion':f'{self.direccion.calle} {self.direccion.numero_direccion}, {self.direccion.ciudad}, {self.direccion.provincia}, {self.direccion.pais}'}]
        lista_transacciones.append(usuario)
        for i, transaccion in enumerate(self.transacciones):
            globals()[f"transaccion{i}"] = [{'fecha':transaccion['fecha']},{'tipo':transaccion['tipo']},{'estado':transaccion['estado']},{'monto':transaccion['monto']}]
            self.filtro(transaccion,i)
            globals()[f"transaccion{i}"].append({'razon':globals()[f"razon{i}"].razon})
            lista_transacciones.append(globals()[f"transaccion{i}"])
        return lista_transacciones

class Gold(Cliente):
    def __init__(self, nombre, apellido, numero, dni, tipo, calle, numero_direccion, ciudad, provincia, pais, objCuenta, transacciones=[], cantChequeras=0, cantTarj=0): 
        super().__init__(nombre, apellido, numero, dni, tipo, calle, numero_direccion, ciudad, provincia, pais, objCuenta, transacciones)
        self.__limiteChequeras = 1
        self.__cantChequeras = cantChequeras
        self.__limiteTarj = 1
        self.__cantTarj = cantTarj
        self.__accesoDolar = 'SI'
    
    @property
    def limiteChequeras(self):
        return self.__limiteChequeras
    @property
    def cantChequeras(self):
        return self.__cantChequeras
    @property
    def limiteTarj(self):
        return self.__limiteTarj
    @property
    def cantTarj(self):
        return self.__cantTarj
    @property
    def accesoDolar(self):
        return self.__accesoDolar
    @cantChequeras.setter
    def cantChequeras(self,nuevoValor):
        self.__cantChequeras = nuevoValor
    @cantTarj.setter
    def cantTarj(self,nuevoValor):
        self.__cantTarj = nuevoValor   

    #funciones dependientes de la clase Classic que utilizan los nuevos parametros asignados, inexistentes en Cliente
    def puede_comprar_dolar(self):
        if self.__accesoDolar == 'NO':
            return False
        else:
            return True

    def puede_crear_chequera(self):
        if self.__cantChequeras < self.__limiteChequeras:
            return True
        else:
            return False        
    
    def puede_crear_tarjeta_credito(self):
        if self.__cantTarj < self.__limiteTarj:
            return True
        else:
            return False
    
    #funciones Filtro a las cuales se accede unicamente si se cumple la igualdad en el tipo de operacion de la transaccion correspondiente
    def filtro_compra_dolar(self,iterador,index):       
        if self.puede_comprar_dolar():
            if iterador['monto'] > iterador['saldoEnCuenta']:
                globals()[f"razon{index}"] = Razon_compra_dolar('Fondos insuficientes')
                return globals()[f"razon{index}"].razon
            else:
                globals()[f"razon{index}"] = Razon_compra_dolar('Razon desconocida')
                return globals()[f"razon{index}"].razon
        else:
            globals()[f"razon{index}"] = Razon_compra_dolar(f'Los clientes {self.tipo} no pueden comprar dolares')
            return globals()[f"razon{index}"].razon


    def filtro_alta_tarj(self,index):
        if self.puede_crear_tarjeta_credito():
            globals()[f"razon{index}"] = Razon_alta_tarjeta_credito('Razon desconocida')
            return globals()[f"razon{index}"].razon
        else:
            globals()[f"razon{index}"] = Razon_alta_tarjeta_credito('Alcanzo el limite de tarjetas de credito')
            return globals()[f"razon{index}"].razon

    def filtro_alta_chequera(self,index):  
        if self.tipo == 'CLASSIC':
            globals()[f"razon{index}"] = Razon_alta_chequera(f'Los clientes {self.tipo} no pueden solicitar chequeras')
            return globals()[f"razon{index}"].razon
        else:
            if self.puede_crear_chequera():
                globals()[f"razon{index}"] = Razon_alta_chequera('Razon desconocida')
                return globals()[f"razon{index}"].razon
            else:
                globals()[f"razon{index}"] = Razon_alta_chequera('Alcanzo el limite de chequeras')
                return globals()[f"razon{index}"].razon

    def filtro_retiro_efectivo_cajero(self,iterador,index): 
        if self.tipo == 'CLASSIC':
            if iterador['monto'] > iterador['saldoEnCuenta']:
                globals()[f"razon{index}"] = Razon_retiro_efectivo_cajero_automatico('Saldo en cuenta insuficiente')
                return globals()[f"razon{index}"].razon
            elif iterador['monto'] > iterador['cupoDiarioRestante']:
                globals()[f"razon{index}"] = Razon_retiro_efectivo_cajero_automatico('La operacion excede el limite de cupo diario restante')
                return globals()[f"razon{index}"].razon
            else:
                globals()[f"razon{index}"] = Razon_retiro_efectivo_cajero_automatico('Razon desconocida')
                return globals()[f"razon{index}"].razon
        else:
            if iterador['monto'] > iterador['saldoEnCuenta'] + self.cuenta.saldo_disponible:
                globals()[f"razon{index}"] = Razon_retiro_efectivo_cajero_automatico('Saldo en cuenta insuficiente')
                return globals()[f"razon{index}"].razon
            elif iterador['monto'] > iterador['cupoDiarioRestante']:
                globals()[f"razon{index}"] = Razon_retiro_efectivo_cajero_automatico('La operacion excede el limite de cupo diario restante')
                return globals()[f"razon{index}"].razon
            else:
                globals()[f"razon{index}"] = Razon_retiro_efectivo_cajero_automatico('Razon desconocida')
                return globals()[f"razon{index}"].razon

    def filtro_transf_enviada(self,iterador,index):       
        if iterador['monto'] + iterador['monto']*self.cuenta.costo_transferencias > iterador['saldoEnCuenta'] + self.cuenta.saldo_disponible:
            globals()[f"razon{index}"] = Razon_transferencia_enviada('Saldo en cuenta insuficiente')
            return globals()[f"razon{index}"].razon
        else:
            globals()[f"razon{index}"] = Razon_transferencia_enviada('Razon desconocida')
            return globals()[f"razon{index}"].razon


    def filtro_transf_recibida(self,iterador,index):        
        if iterador['monto'] > self.cuenta.limite_transferencia:
            globals()[f"razon{index}"] = Razon_transferencia_recibida('Excede el monto limite a recibir')
            return globals()[f"razon{index}"].razon
        else:
            globals()[f"razon{index}"] = Razon_transferencia_recibida('Razon desconocida')
            return globals()[f"razon{index}"].razon

    def filtro(self,t,i): #funcion filtro principal que determina si la transaccion se acepto o rechazo y busca las igualdades correspondientes para ejecurar la funcion deseada
        if t['estado'] == 'ACEPTADA':
            globals()[f"razon{i}"] = Razon_nula('')
            return globals()[f"razon{i}"].razon 
        elif t['estado'] == 'RECHAZADA':
            if t['tipo'] == 'COMPRA_DOLAR':
                self.filtro_compra_dolar(t,i)
            elif t['tipo'] == 'ALTA_TARJETA_CREDITO':
                self.filtro_alta_tarj(i)
            elif t['tipo'] == 'ALTA_CHEQUERA':    
                self.filtro_alta_chequera(i)
            elif t['tipo'] == 'RETIRO_EFECTIVO_CAJERO_AUTOMATICO':    
                self.filtro_retiro_efectivo_cajero(t,i)
            elif t['tipo'] == 'TRANSFERENCIA_ENVIADA':    
                self.filtro_transf_enviada(t,i)
            elif t['tipo'] == 'TRANSFERENCIA_RECIBIDA':    
                self.filtro_transf_recibida(t,i)

    def retorno(self): #funcion retorno, encargada de crear una lista que recolecta toda la informacion del cliente y sus transacciones y luego la retorna para utilizarla al exportar el HTML
        lista_transacciones = []
        usuario = [{'nombre_completo':f'{self.nombre} {self.apellido}'},{'numero':self.numero},{'DNI':self.dni},{'direccion':f'{self.direccion.calle} {self.direccion.numero_direccion}, {self.direccion.ciudad}, {self.direccion.provincia}, {self.direccion.pais}'}]
        lista_transacciones.append(usuario)
        for i, transaccion in enumerate(self.transacciones):
            globals()[f"transaccion{i}"] = [{'fecha':transaccion['fecha']},{'tipo':transaccion['tipo']},{'estado':transaccion['estado']},{'monto':transaccion['monto']}]
            self.filtro(transaccion,i)
            globals()[f"transaccion{i}"].append({'razon':globals()[f"razon{i}"].razon})
            lista_transacciones.append(globals()[f"transaccion{i}"])
        return lista_transacciones

class Black(Cliente):
    def __init__(self, nombre, apellido, numero, dni, tipo, calle, numero_direccion, ciudad, provincia, pais, objCuenta, transacciones=[], cantChequeras=0, cantTarj=0): 
        super().__init__(nombre, apellido, numero, dni, tipo, calle, numero_direccion, ciudad, provincia, pais, objCuenta, transacciones)
        self.__limiteChequeras = 2
        self.__cantChequeras = cantChequeras
        self.__limiteTarj = 5
        self.__cantTarj = cantTarj
        self.__accesoDolar = 'SI'
    
    @property
    def limiteChequeras(self):
        return self.__limiteChequeras
    @property
    def cantChequeras(self):
        return self.__cantChequeras
    @property
    def limiteTarj(self):
        return self.__limiteTarj
    @property
    def cantTarj(self):
        return self.__cantTarj
    @property
    def accesoDolar(self):
        return self.__accesoDolar

    #funciones dependientes de la clase Classic que utilizan los nuevos parametros asignados, inexistentes en Cliente
    def puede_comprar_dolar(self):
        if self.__accesoDolar == 'NO':
            return False
        else:
            return True

    def puede_crear_chequera(self):
        if self.__cantChequeras < self.__limiteChequeras:
            return True
        else:
            return False        
    
    def puede_crear_tarjeta_credito(self):
        if self.__cantTarj < self.__limiteTarj:
            return True
        else:
            return False
    
    #funciones Filtro a las cuales se accede unicamente si se cumple la igualdad en el tipo de operacion de la transaccion correspondiente
    def filtro_compra_dolar(self,iterador,index):       
        if self.puede_comprar_dolar():
            if iterador['monto'] > iterador['saldoEnCuenta']:
                globals()[f"razon{index}"] = Razon_compra_dolar('Fondos insuficientes')
                return globals()[f"razon{index}"].razon
            else:
                globals()[f"razon{index}"] = Razon_compra_dolar('Razon desconocida')
                return globals()[f"razon{index}"].razon
        else:
            globals()[f"razon{index}"] = Razon_compra_dolar(f'Los clientes {self.tipo} no pueden comprar dolares')
            return globals()[f"razon{index}"].razon


    def filtro_alta_tarj(self,index):
        if self.puede_crear_tarjeta_credito():
            globals()[f"razon{index}"] = Razon_alta_tarjeta_credito('Razon desconocida')
            return globals()[f"razon{index}"].razon
        else:
            globals()[f"razon{index}"] = Razon_alta_tarjeta_credito('Alcanzo el limite de tarjetas de credito')
            return globals()[f"razon{index}"].razon

    def filtro_alta_chequera(self,index):  
        if self.tipo == 'CLASSIC':
            globals()[f"razon{index}"] = Razon_alta_chequera(f'Los clientes {self.tipo} no pueden solicitar chequeras')
            return globals()[f"razon{index}"].razon
        else:
            if self.puede_crear_chequera():
                globals()[f"razon{index}"] = Razon_alta_chequera('Razon desconocida')
                return globals()[f"razon{index}"].razon
            else:
                globals()[f"razon{index}"] = Razon_alta_chequera('Alcanzo el limite de chequeras')
                return globals()[f"razon{index}"].razon

    def filtro_retiro_efectivo_cajero(self,iterador,index): 
        if self.tipo == 'CLASSIC':
            if iterador['monto'] > iterador['saldoEnCuenta']:
                globals()[f"razon{index}"] = Razon_retiro_efectivo_cajero_automatico('Saldo en cuenta insuficiente')
                return globals()[f"razon{index}"].razon
            elif iterador['monto'] > iterador['cupoDiarioRestante']:
                globals()[f"razon{index}"] = Razon_retiro_efectivo_cajero_automatico('La operacion excede el limite de cupo diario restante')
                return globals()[f"razon{index}"].razon
            else:
                globals()[f"razon{index}"] = Razon_retiro_efectivo_cajero_automatico('Razon desconocida')
                return globals()[f"razon{index}"].razon
        else:
            if iterador['monto'] > iterador['saldoEnCuenta'] + self.cuenta.saldo_disponible:
                globals()[f"razon{index}"] = Razon_retiro_efectivo_cajero_automatico('Saldo en cuenta insuficiente')
                return globals()[f"razon{index}"].razon
            elif iterador['monto'] > iterador['cupoDiarioRestante']:
                globals()[f"razon{index}"] = Razon_retiro_efectivo_cajero_automatico('La operacion excede el limite de cupo diario restante')
                return globals()[f"razon{index}"].razon
            else:
                globals()[f"razon{index}"] = Razon_retiro_efectivo_cajero_automatico('Razon desconocida')
                return globals()[f"razon{index}"].razon

    def filtro_transf_enviada(self,iterador,index):       
        if iterador['monto'] + iterador['monto']*self.cuenta.costo_transferencias > iterador['saldoEnCuenta'] + self.cuenta.saldo_disponible:
            globals()[f"razon{index}"] = Razon_transferencia_enviada('Saldo en cuenta insuficiente')
            return globals()[f"razon{index}"].razon
        else:
            globals()[f"razon{index}"] = Razon_transferencia_enviada('Razon desconocida')
            return globals()[f"razon{index}"].razon


    def filtro_transf_recibida(self,iterador,index):        
        if iterador['monto'] > self.cuenta.limite_transferencia:
            globals()[f"razon{index}"] = Razon_transferencia_recibida('Excede el monto limite a recibir')
            return globals()[f"razon{index}"].razon
        else:
            globals()[f"razon{index}"] = Razon_transferencia_recibida('Razon desconocida')
            return globals()[f"razon{index}"].razon

    def filtro(self,t,i): #funcion filtro principal que determina si la transaccion se acepto o rechazo y busca las igualdades correspondientes para ejecurar la funcion deseada
        if t['estado'] == 'ACEPTADA':
            globals()[f"razon{i}"] = Razon_nula('')
            return globals()[f"razon{i}"].razon 
        elif t['estado'] == 'RECHAZADA':
            if t['tipo'] == 'COMPRA_DOLAR':
                self.filtro_compra_dolar(t,i)
            elif t['tipo'] == 'ALTA_TARJETA_CREDITO':
                self.filtro_alta_tarj(i)
            elif t['tipo'] == 'ALTA_CHEQUERA':    
                self.filtro_alta_chequera(i)
            elif t['tipo'] == 'RETIRO_EFECTIVO_CAJERO_AUTOMATICO':    
                self.filtro_retiro_efectivo_cajero(t,i)
            elif t['tipo'] == 'TRANSFERENCIA_ENVIADA':    
                self.filtro_transf_enviada(t,i)
            elif t['tipo'] == 'TRANSFERENCIA_RECIBIDA':    
                self.filtro_transf_recibida(t,i)

    def retorno(self): #funcion retorno, encargada de crear una lista que recolecta toda la informacion del cliente y sus transacciones y luego la retorna para utilizarla al exportar el HTML
        lista_transacciones = []
        usuario = [{'nombre_completo':f'{self.nombre} {self.apellido}'},{'numero':self.numero},{'DNI':self.dni},{'direccion':f'{self.direccion.calle} {self.direccion.numero_direccion}, {self.direccion.ciudad}, {self.direccion.provincia}, {self.direccion.pais}'}]
        lista_transacciones.append(usuario)
        for i, transaccion in enumerate(self.transacciones):
            globals()[f"transaccion{i}"] = [{'fecha':transaccion['fecha']},{'tipo':transaccion['tipo']},{'estado':transaccion['estado']},{'monto':transaccion['monto']}]
            self.filtro(transaccion,i)
            globals()[f"transaccion{i}"].append({'razon':globals()[f"razon{i}"].razon})
            lista_transacciones.append(globals()[f"transaccion{i}"])
        return lista_transacciones

            
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

class Razon_nula(Razon):
    def __init__(self, razon):
        super().__init__(razon)       


#Ejecucion:
#creo objeto cuenta y cliente 
cuenta1 = Cuenta(0,0,0,0,0)
cl = Cliente(data['nombre'],data['apellido'],data['numero'],data['dni'],data['tipo'],data['direccion']['calle'],data['direccion']['numero'],data['direccion']['ciudad'],data['direccion']['provincia'],data['direccion']['pais'],cuenta1,data['transacciones'])
#creo clases que heredan de cliente segun el tipo de cliente
if cl.tipo == 'BLACK':
    if not cl.transacciones == []: #permito el funcionamiento de un JSON con usuario sin transacciones filtrando la asignacion de variables
        cliente = Black(cl.nombre,cl.apellido,cl.numero,cl.dni,cl.tipo,cl.direccion.calle,cl.direccion.numero_direccion,cl.direccion.ciudad,cl.direccion.provincia,cl.direccion.pais,cl.cuenta,cl.transacciones,data['transacciones'][0]['totalChequerasActualmente'],data['transacciones'][0]['totalTarjetasDeCreditoActualmente'])
    else:
        cliente = Black(cl.nombre,cl.apellido,cl.numero,cl.dni,cl.tipo,cl.direccion.calle,cl.direccion.numero_direccion,cl.direccion.ciudad,cl.direccion.provincia,cl.direccion.pais,cl.cuenta)
    # asigno por setters las variables correspondientes a cada categoria segun los limites y condiciones estipulados
    cliente.cuenta.limite_extraccion = 100000 
    cliente.cuenta.limite_transferencia = float('inf')
    if not cliente.transacciones == []:
        cliente.cuenta.monto = data['transacciones'][0]['monto']
    cliente.cuenta.saldo_disponible = 10000
    cliente.cuenta.costo_transferencias = 0
elif cl.tipo == 'GOLD':
    if not cl.transacciones == []:
        cliente = Gold(cl.nombre,cl.apellido,cl.numero,cl.dni,cl.tipo,cl.direccion.calle,cl.direccion.numero_direccion,cl.direccion.ciudad,cl.direccion.provincia,cl.direccion.pais,cl.cuenta,cl.transacciones,data['transacciones'][0]['totalChequerasActualmente'],data['transacciones'][0]['totalTarjetasDeCreditoActualmente'])
    else:
        cliente = Gold(cl.nombre,cl.apellido,cl.numero,cl.dni,cl.tipo,cl.direccion.calle,cl.direccion.numero_direccion,cl.direccion.ciudad,cl.direccion.provincia,cl.direccion.pais,cl.cuenta)
    cliente.cuenta.limite_extraccion = 20000
    cliente.cuenta.limite_transferencia = 500000
    if not cliente.transacciones == []:
        cliente.cuenta.monto = data['transacciones'][0]['monto']
    cliente.cuenta.saldo_disponible = 10000
    cliente.cuenta.costo_transferencias = 0.005
elif cl.tipo == 'CLASSIC':
    if not cl.transacciones == []:
        cliente = Classic(cl.nombre,cl.apellido,cl.numero,cl.dni,cl.tipo,cl.direccion.calle,cl.direccion.numero_direccion,cl.direccion.ciudad,cl.direccion.provincia,cl.direccion.pais,cl.cuenta,cl.transacciones,data['transacciones'][0]['totalChequerasActualmente'],data['transacciones'][0]['totalTarjetasDeCreditoActualmente'])
    else:
        cliente = Classic(cl.nombre,cl.apellido,cl.numero,cl.dni,cl.tipo,cl.direccion.calle,cl.direccion.numero_direccion,cl.direccion.ciudad,cl.direccion.provincia,cl.direccion.pais,cl.cuenta)
    cliente.cuenta.limite_extraccion = 10000
    cliente.cuenta.limite_transferencia = 150000
    if not cliente.transacciones == []:
        cliente.cuenta.monto = data['transacciones'][0]['monto']
    cliente.cuenta.saldo_disponible = 0
    cliente.cuenta.costo_transferencias = 0.01

info = cliente.retorno() # retorna una lista diagramada a base de diccionarios que contiene como primer elemento los datos del cliente que se necesitan exportar y a partir del segundo elemento cada uno es una transaccion con la info a exportar 
info_transacciones = info.copy()
if not info_transacciones == []:
    info_transacciones.pop(0) #creo lista de transacciones a recorrer en HTML

#ejemplos para llamar a los valores:
# cliente.retorno()[0] -->  [{'nombre_completo': 'Nicolas Gaston'}, {'numero': 100001}, {'DNI': '29494777'}, {'direccion': 'Rivadavia 7900, Capital Federal, Buenos Aires, Argentina'}]
# cliente.retorno()[0][0] -->  {'nombre_completo': 'Nicolas Gaston'}
# cliente.retorno()[0][0]['nombre_completo'] -->  Nicolas Gaston

#Creacion de HTML

env = Environment(
    loader=PackageLoader("paquete"),
    autoescape=select_autoescape()
)
template = env.get_template("template.html")
filename = "rps.html"
with open (filename,"w") as file:
    file.write(template.render(info = info, info_transacciones = info_transacciones))

nombre = info[0][0]['nombre_completo']
print(f'El informe {filename} del cliente {nombre} se ha creado exitosamente') #emito mensaje de confirmacion
