
class Quadro:

    def __init__(self, x, y, indice):
        self.x = x
        self.y = y
        self.estado = 0
        self.pai = None
        self.indice = indice
        self.vizinhos = []
        self.vizinhos_costs = {}

    def __repr__(self):
        return "({},{}) : {}".format(self.x, self.y, [(q.x, q.y) for q in self.vizinhos])
