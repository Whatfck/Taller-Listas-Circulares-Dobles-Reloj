class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.siguiente = None
        self.anterior = None

class ListaCircularDoble:
    def __init__(self, valores):
        if not valores:
            raise ValueError("La lista debe tener al menos un valor")
        self.valores = valores
        self.longitud = len(valores)
        self.indice_actual = 0
        self._construir_lista()

    def _construir_lista(self):
        self.cabeza = Nodo(self.valores[0])
        nodo_actual = self.cabeza
        for i in range(1, self.longitud):
            nuevo_nodo = Nodo(self.valores[i])
            nuevo_nodo.anterior = nodo_actual
            nodo_actual.siguiente = nuevo_nodo
            nodo_actual = nuevo_nodo
        # Hacer circular
        nodo_actual.siguiente = self.cabeza
        self.cabeza.anterior = nodo_actual

    def obtener_actual(self):
        return self.valores[self.indice_actual]

    def avanzar(self):
        self.indice_actual = (self.indice_actual + 1) % self.longitud

    def retroceder(self):
        self.indice_actual = (self.indice_actual - 1) % self.longitud

    def establecer_valor(self, valor):
        if valor not in self.valores:
            raise ValueError(f"Valor {valor} no está en la lista de valores permitidos")
        self.indice_actual = self.valores.index(valor)

    def __str__(self):
        return f"Valor actual: {self.obtener_actual()}"