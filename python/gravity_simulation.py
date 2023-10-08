
#importando livrarias e declarando variaveis iniciais
import time
import random
import matplotlib.pyplot as lib

inicio = time.time()
t = 0 #tempo
d = 0 #distancia
d2 = 0 #distanccia_y
f = 0 #força
m = 1 #massa
g = 9.8 #gravidade
v = 0 #velocidade
vi = -50 #velocidade_inicial 
vi2 = 10
a = 0 #altura
q = a #queda
loop = True

#preparando coleta de dados:
width = []
data_height = []

#definindo as funçoes da simulaçao

def resistencia(v,drag):
    return v*drag

def velocidade(vi, gravidade, tempo):
    velocidade = vi + gravidade*tempo
    return velocidade

def distancia(vi,tempo, gravidade):
        return (tempo *vi+(tempo**2 *gravidade)/2)
    
def distancia2(v2, tempo):
    return  v2*tempo
    

def queda(altura, distancia):
    return altura - distancia

def força(massa, velocidade,gravidade):
    return massa*gravidade* velocidade

def status():
    return {
    "distancia": round(d,2),
    "tempo simulado: ": round(t,2),
    "altura: ": round(q,2),
    "distancia_horizontal:":round(d2,2),
    "velocidade": round(v,2),
    "força de impacto:":round(f,2)
    
    }
    
print("calculando simulação")

#preparando o loop principal
while loop == True:
    #coleta de dados:
    data_height.append(round(q,2))
    width.append(round(d2,2))
    
    #calculando simulação
    
    drag_x = 1*(random.randint(1,5))
    drag_y = 0.1*(random.randint(1,5))


    v = velocidade(vi,g,t)
    d = distancia(vi,t,g)
    q = queda(a,d)
    f = força(m,v,g)
    
    
    d2 = distancia2(vi2,t)
    
    print(status())
    time.sleep(0)
    t += 0.01
    fim = time.time()
    #visualização de dados
    lib.style.use("dark_background")
    lib.plot(width,data_height, label = "data_height")
    lib.xlabel("distancia em metros")
    lib.ylabel("altura em metros")
    lib.title("lançamento vertical")
    
    
    
    if q < 0:
        print("fim da simulaçao")
        print("tempo real: ", round(fim - inicio,2))
        print(status())
        loop = False
        lib.show()
        lib.pause(0.1)
    