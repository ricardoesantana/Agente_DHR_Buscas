import random
import time
from Quadro import Quadro

import sys
from ctypes import c_int64


def increment(number):
    number.value += 1
    return number.value

NV = 0
VISITADO = 1
OBSTACULO = 2
COMIDA = 3
AGENTE = 4
ROTA = 5

COR = {
    NV: (255, 255, 255), 
    VISITADO: (0,255,255), 
    OBSTACULO: (148,148,148), 
    COMIDA: (220,20,60), 
    AGENTE: (139,0,139), 
    ROTA: (255,215,0)} 


class Busca:

    def __init__(self, linhas=18, colunas=24, obstaculo=35):
        self.linhas = linhas
        self.colunas = colunas
        self.obstaculo = obstaculo
        self.comida= None
        self.veiculo= None
        self.PComidaX = None
        self.PComidaY = None
        self.grid = self.criar()
        self.add(OBSTACULO, self.obstaculo)
        self.add(COMIDA)
        self.add(AGENTE)

        self.fila = [self.agente]
        self.pilha = [self.agente] 
        self.prox = [self.agente]
        
        self.pontos = 0       
       

    def criar(self):
        index = c_int64(0)
        grid = [[Quadro(linha,coluna,increment(index)) for coluna in range(self.colunas)] for linha in range(self.linhas)]
        print("Grid", grid)
        for linha in range(self.linhas):
            for coluna in range(self.colunas):
                if(coluna < self.colunas - 1): # vai pra direita
                    grid[linha][coluna].vizinhos.append(grid[linha][coluna + 1])
                    grid[linha][coluna].vizinhos_costs[grid[linha][coluna + 1].indice] = random.randint(1,4)
                if(coluna > 0): # vai para esquerda
                    grid[linha][coluna].vizinhos.append(grid[linha][coluna - 1])
                    grid[linha][coluna].vizinhos_costs[grid[linha][coluna - 1].indice] = random.randint(1,4)
                if(linha < self.linhas - 1): # desce
                    grid[linha][coluna].vizinhos.append(grid[linha + 1][coluna])
                    grid[linha][coluna].vizinhos_costs[grid[linha + 1][coluna].indice] = random.randint(1,4)
                if(linha > 0): # sobe
                    grid[linha][coluna].vizinhos.append(grid[linha - 1][coluna])
                    grid[linha][coluna].vizinhos_costs[grid[linha - 1][coluna].indice] = random.randint(1,4)
                if(linha < self.linhas - 1 and coluna < self.colunas - 1): # diagonal esquerda descendo
                    grid[linha][coluna].vizinhos.append(grid[linha + 1][coluna + 1])
                    grid[linha][coluna].vizinhos_costs[grid[linha + 1][coluna + 1].indice] = random.randint(1,4)
                if(linha > 0 and coluna > 0): # diagonal esqueda subindo
                    grid[linha][coluna].vizinhos.append(grid[linha - 1][coluna - 1])
                    grid[linha][coluna].vizinhos_costs[grid[linha - 1][coluna - 1].indice] = random.randint(1,4)
                if(linha > 0 and coluna < self.colunas - 1): # diagonal direita subindo
                    grid[linha][coluna].vizinhos.append(grid[linha - 1][coluna + 1])
                    grid[linha][coluna].vizinhos_costs[grid[linha - 1][coluna + 1].indice] = random.randint(1,4)
                if(linha < self.linhas - 1 and coluna > 0): # diagonal direita descendo
                    grid[linha][coluna].vizinhos.append(grid[linha + 1][coluna - 1])
                    grid[linha][coluna].vizinhos_costs[grid[linha + 1][coluna - 1].indice] = random.randint(1,4)
        return grid

    def add(self, estado, amount=1):
        added = 0
        while(added < amount):
            x = random.randint(0, len(self.grid) - 1)
            y = random.randint(0, len(self.grid[0]) - 1)
            q = self.grid[x][y]           
            is_NV = q.estado == NV
            if(is_NV):
                q.estado = estado
                if(estado == OBSTACULO):
                    for vizinho in self.grid[x][y].vizinhos:
                        vizinho.vizinhos.remove(q)
                        #print("Vizinhos:", self.grid[x][y].vizinhos)
                    q.vizinhos = []
                if(estado == AGENTE):
                    self.agente= q
                   
                added = added + 1

    def largura(self):
        if(self.fila):
            current = self.fila.pop(0)
            for q in current.vizinhos:
                if(q.estado == COMIDA):
                    self.comida= current
                    self.fila = []
                    self.pontos += 1
                    break
                if(q.estado == NV):
                    self.fila.append(q)
                    q.estado = VISITADO
                    q.pai = current

    def profundidade(self):
        if(self.pilha):
            current = self.pilha.pop()
            for q in current.vizinhos:
                if(q.estado == COMIDA):
                    self.comida= current
                    self.pilha = []
                    self.pontos += 1
                    break
                if(q.estado == NV):
                    self.pilha.append(q)
                    q.estado = VISITADO
                    q.pai = current
                    
    def uniforme(self):
        if(self.prox):
            miniI = self.minDistancia(self.prox)
            current = self.prox.pop(miniI)
       
            for q in current.vizinhos:
                if(q.estado == COMIDA):
                    self.comida = current
                    self.prox = []
                    self.pontos += 1
                    break
                if(q.estado == NV):
                    self.prox.append(q)
                    q.estado = VISITADO
                    q.pai = current
     
    def gulosa(self):
        if(self.fila):
            current = self.fila.pop()
            miniI = self.minCusto(current.vizinhos, current)
            
            if(current.vizinhos[miniI].estado == COMIDA):
                self.comida = current
                self.fila = []
                
            if(current.vizinhos[miniI].estado == NV):
                self.fila.append(current.vizinhos[miniI])
                current.vizinhos[miniI].estado = VISITADO
                current.vizinhos[miniI].pai = current
                
    def brilho(self):
        if(self.prox):
            miniI = self.minDH(self.prox)
            current = self.prox.pop(miniI)
       
            for q in current.vizinhos:
                if(q.estado == COMIDA):
                    self.estado = current
                    self.prox = []
                    break
                if(q.estado == NV):
                    self.prox.append(q)
                    node.estado = VISITADO
                    node.pai = current
                    
    def minCusto(self, vizinhos, pai):
        minValor = sys.maxint
        miniI = 0 
        for id, n in enumerate(vizinhos):
            if(n.estado == NV or n.estado == COMIDA):
                h = dist(n.x, n.y, self.PComidaX, self.PComidaY)
                if(h < minValor):
                    minValor = h
                    miniI = id
        return(miniI)

    def minDistancia(self, quadros):
        minValor = sys.maxint
        miniI = 0 
        for id, n in enumerate(quadros):
            if(self.relativeCost(n) < minValor):
                minValor = self.relativeCost(n)
                miniI = id 
        return(miniI)

    def minDH(self, quadros):
        minValor = sys.maxint
        miniI = 0 
        cost = 0
        for id, n in enumerate(quadros):
            cost = self.relativeCost(n) + dist(self.PComidaX, self.PComidaY, n.x, n.y)
            if(cost < minValue):
                minValor = cost
                miniI = id 
        return(miniI)

    def relativeCost(self, current):
       tempCurrent = current 
       cost = 0
       while(tempCurrent.indice != self.agente.indice):
           if(tempCurrent.pai != None):
               cost += tempCurrent.pai.vizinhos_costs[tempCurrent.indice] 
               tempCurrent = tempCurrent.pai
       return(cost)

    def rota(self):
        if(self.comida):
            if(self.comida.estado != AGENTE):
                self.comida.estado = ROTA
                self.comida= self.comida.pai
            else:
                self.bora()

    def bora(self):
        for linha in range(self.linhas):
            for coluna in range(self.colunas):
                if(self.grid[linha][coluna].estado == COMIDA):
                    self.grid[linha][coluna].estado = AGENTE
                    self.agente = self.grid[linha][coluna]
                elif(self.grid[linha][coluna].estado in [VISITADO, AGENTE, ROTA]):
                    self.grid[linha][coluna].estado = NV

        self.comida = None
        self.fila = [self.agente]
        self.pilha = [self.agente]
        self.prox = [self.agente]
        self.add(COMIDA)

    def display(self):
        for x in range(10):
            with pushMatrix():
                #stroke (148,148,148)
                strokeWeight(5)
                beginShape()
                posicaox = 30
                posicaoy= 30
                for linha in range(self.linhas):
                    for coluna in range(self.colunas):
                        value = self.grid[linha][coluna].estado                    
                        r, g, b = COR[value]
                        if value == NV:
                            stroke (148,148,148)
                        else:
                            stroke (r-30, g-30, b-30)
                        fill(r, g, b)
                        rect(posicaox, posicaoy, 30, 30)
                        posicaox += 30
                    posicaox = 30
                    posicaoy += 30
                endShape(CLOSE)
