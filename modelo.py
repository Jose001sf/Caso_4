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
    def __init__(self, numero, codigo_viaje, cantidad, total, fecha, estado="Activo"):
        self.numero = int(numero)
        self.codigo_viaje = codigo_viaje
        self.cantidad = int(cantidad)
        self.total = float(total)
        self.fecha = fecha
        self.estado = estado

    def __str__(self):
        return (
            f"Boleto #{self.numero} | Viaje: {self.codigo_viaje} | "
            f"Cant.: {self.cantidad} | Total: ${self.total:.2f} | "
            f"Fecha: {self.fecha} | Estado: {self.estado}"
        )


class Cooperativa:
    def __init__(self, archivo_viajes="viajes.txt", archivo_boletos="boletos.txt"):
        self.archivo_viajes = archivo_viajes
        self.archivo_boletos = archivo_boletos
        self.viajes = []
        self.boletos = []
        self.cargar()

    def buscar_por_codigo(self, codigo):
        for v in self.viajes:
            if v.codigo.lower() == codigo.lower():
                return v
        return None

    def buscar(self, texto):
        resultados = []
        for v in self.viajes:
            if texto.lower() in v.codigo.lower() or texto.lower() in v.hora_salida.lower():
                resultados.append(v)
        return resultados

    def registrar(self, codigo, hora_salida, precio, asientos):
        if self.buscar_por_codigo(codigo) is not None:
            raise ValueError(f"Ya existe un viaje registrado con el código '{codigo}'.")
        if float(precio) <= 0 or int(asientos) < 0:
            raise ValueError("El precio debe ser mayor a 0 y los asientos no pueden ser negativos.")

        nuevo_viaje = Viaje(codigo, hora_salida, precio, asientos)
        self.viajes.append(nuevo_viaje)
        self.guardar()
        return nuevo_viaje

    def vender(self, codigo_viaje, cantidad):
        viaje = self.buscar_por_codigo(codigo_viaje)
        if viaje is None:
            raise ValueError("No existe un viaje con ese código.")
        if int(cantidad) <= 0:
            raise ValueError("La cantidad debe ser mayor a 0.")
        if viaje.asientos < int(cantidad):
            raise ValueError(f"No hay suficientes asientos. Disponibles: {viaje.asientos}.")

        viaje.asientos -= int(cantidad)
        numero = len(self.boletos) + 1
        total = viaje.precio * int(cantidad)
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M")

        boleto = Boleto(numero, viaje.codigo, cantidad, total, fecha, "Activo")
        self.boletos.append(boleto)
        self.guardar()
        return boleto

    def anular(self, numero_boleto):
        for b in self.boletos:
            if b.numero == int(numero_boleto):
                if b.estado == "Anulado":
                    raise ValueError("Ese boleto ya está anulado.")
                b.estado = "Anulado"
                viaje = self.buscar_por_codigo(b.codigo_viaje)
                if viaje is not None:
                    viaje.asientos += b.cantidad
                self.guardar()
                return b
        raise ValueError("No se encontró ese número de boleto.")

    def reporte(self):
        activos = 0
        anulados = 0
        pasajes = 0
        recaudado = 0.0

        for b in self.boletos:
            if b.estado == "Activo":
                activos += 1
                pasajes += b.cantidad
                recaudado += b.total
            else:
                anulados += 1

        return {
            "total_viajes": len(self.viajes),
            "boletos_activos": activos,
            "boletos_anulados": anulados,
            "pasajes_vendidos": pasajes,
            "recaudacion_total": recaudado,
        }

    def guardar(self):
        with open(self.archivo_viajes, "w", encoding="utf-8") as f:
            for v in self.viajes:
                f.write(f"{v.codigo}|{v.hora_salida}|{v.precio}|{v.asientos}\n")

        with open(self.archivo_boletos, "w", encoding="utf-8") as f:
            for b in self.boletos:
                f.write(f"{b.numero}|{b.codigo_viaje}|{b.cantidad}|{b.total}|{b.fecha}|{b.estado}\n")

    def cargar(self):
        self.viajes = []
        self.boletos = []

        try:
            with open(self.archivo_viajes, "r", encoding="utf-8") as f:
                for linea in f:
                    if linea.strip():
                        datos = linea.strip().split("|")
                        self.viajes.append(Viaje(datos[0], datos[1], datos[2], datos[3]))
        except FileNotFoundError:
            pass

        try:
            with open(self.archivo_boletos, "r", encoding="utf-8") as f:
                for linea in f:
                    if linea.strip():
                        datos = linea.strip().split("|")
                        self.boletos.append(Boleto(datos[0], datos[1], datos[2], datos[3], datos[4], datos[5]))
        except FileNotFoundError:
            pass