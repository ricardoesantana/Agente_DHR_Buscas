import Busca

def setup():
    global search
    size(800, 600)
    search = Busca.Busca()
    
def draw():
        background(255)
        if (key == 'l'):
            search.largura()
        elif (key == 'd'):
            search.profundidade()
        elif (key == 'u'):
            search.uniforme()
        elif (key == 'g'):
            search.gulosa()
        elif (key == 'b'):
            search.brilho()     
                     
        search.rota()
        search.display()
        
        # Pontuacao
        stroke(255);
        strokeWeight(2);
        fill(0, 100, 255);
        textSize(20);
        text('Comidas: ' + str(search.pontos), 25, 25);    
       
