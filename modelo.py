from datetime import datetime

class Viaje:
    def __init__(self, codigo, hora_salida, precio, asientos):
        self.codigo = codigo
        self.hora_salida = hora_salida
        self.precio = float(precio)
        self.asientos = int(asientos)

    def __str__(self):
        return f"{self.codigo} | Salida: {self.hora_salida} | ${self.precio:.2f} | Asientos disp.: {self.asientos}"


class Boleto:
    def __init__(self,numero,codigo_viaje,cantidad,total,fecha,estado,):
        self.numero = int(numero)
        self.codigo_viaje = codigo_viaje
        self.cantidad = int(cantidad)
        self.total = float(total)
        self.fecha = fecha 
        self.estado = "Activo"

    def __str__(self):
        return (f"Boleto #{self.numero} | Viaje: {self.codigo_viaje} | " f"Cant.: {self.cantidad} | Total: ${self.total:.2f} | " f"Fecha: {self.fecha} | Estado: {self.estado}")


class Cooperativa:
    def __init__(self, archivo_viajes: str = "viajes.txt", archivo_boletos: str = "boletos.txt"):
        self.archivo_viajes = archivo_viajes
        self.archivo_boletos = archivo_boletos
        self.viajes: list[Viaje] = []
        self.boletos: list[Boleto] = []
        self.cargar()

    def registrar(self, codigo: str, hora_salida: str, precio: float, asientos: int):
        if self.buscar_por_codigo(codigo) is not None:
            raise ValueError(f"Ya existe un viaje registrado con el código '{codigo.strip().upper()}'.")
        nuevo_viaje = Viaje(codigo, hora_salida, precio, asientos)
        self.viajes.append(nuevo_viaje)
        self.guardar()
        return nuevo_viaje