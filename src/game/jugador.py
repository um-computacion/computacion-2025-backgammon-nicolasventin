class Jugador:
    def __init__(self, nombre, ficha):
        self.nombre = nombre
        self.ficha = ficha

    def obtener_info(self):
        return f"{self.nombre} ({self.ficha})"