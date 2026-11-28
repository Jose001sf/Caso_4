class Vista_Cooperativa:
    def mostrar_menu(self):
        print("COOPERATIVA CUENCA - GUAYAQUIL")
        print("1. Registrar viaje")
        print("2. Mostrar viajes")
        print("3. Vender boletos")
        print("4. Buscar por nombre")
        print("5. Anular boleto")
        print("6. Mostrar boletos")
        print("7. Reporte general")
        print("8. Salir")

    def pedir_opcion(self):
        return input("Opcion: ")

    def pedir_datos_viaje(self):
        codigo = input("Codigo: ")
        hora_salida = input("Hora: ")
        precio = input("Precio: ")
        asientos = input("Asientos: ")
        return codigo, hora_salida, precio, asientos
    
    def mostrar_mensaje(self, texto):
        print(texto)

    def mostrar_error(self, texto):
        print("Error: ", {texto})