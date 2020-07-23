import time
import Busca

def setup():
    global busca
    size(800, 600)
    busca = Busca.Busca()
    
   
def draw():
        background(255)
        if (key == 'l'):
            busca.largura()
        elif (key == 'd'):
            busca.profundidade()
        elif (key == 'u'):
            busca.uniforme()
        elif (key == 'g'):
            busca.gulosa()
        elif (key == 'b'):
            busca.brilho()
        else:
            print("Rodando...")
        
                     
        busca.rota()
        busca.display()
        time.sleep(0.1)
        
        # Pontuacao
        stroke(255);
        strokeWeight(2);
        fill(0, 100, 255);
        textSize(20);
        text('Comidas: ' + str(busca.pontos), 25, 25);    
       
       
