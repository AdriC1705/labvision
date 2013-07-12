from time import *
import sys
from Tkinter import *
import Tkinter
from PIL import Image, ImageTk
import random
import math
from math import pi
import ImageDraw

def ventana(foto,ancho,alto,titulo):# creacion de  ventana de grises                           
    x=0#Cordenadas de posicion de la ventana                                                           
    y=0
    ventana= Tkinter.Tk()#Creacion de ventana                                           
    ventana.title(titulo)#Titulo de ventana                      
    ventana.geometry("%dx%d+%d+%d" % (ancho,alto,x,y))#Tamano y posicio                 
    tkimage=ImageTk.PhotoImage(foto)#Se convierte la imagen en un objeto tk                            
    Tkinter.Label(ventana,image=tkimage).pack()#Colocar imagen en venta                  
    ventana.mainloop()

def convolucion(foto,ancho,alto):
    t_in=time()
    gx=[]
    gy=[]
    magnitud=[]
    Gx=([-1,0,1],[-2,0,2],[-1,0,1])#Formulas Convolucion
    Gy=([1,2,1],[0,0,0],[-1,-2,-1])
    pixeles=foto.load()
    for i in range(alto):
        gx.append([])
        gy.append([])
        for j in range(ancho):
            sumx=0
            sumy=0
            for x in range(len(Gx[0])):
                for y in range(len(Gy[0])):
                    try:
                        sumx +=(pixeles[j+y,i+x][0]*Gx[x][y])
                        sumy +=(pixeles[j+y,i+x][0]*Gy[x][y])
                    except:
                        pass
                    Gradiente_Horizontal=pow(sumx,2)#Formulas para obtener el gradiente
                    Gradiente_Vertical=pow(sumy,2)
                    Magnitud=int(math.sqrt(Gradiente_Horizontal+Gradiente_Vertical))
                    gx[i].append(sumx)
                    gy[i].append(sumy)
                    pixeles[j,i]=(Magnitud,Magnitud,Magnitud)
    t_fi=time()
    tot=t_fi-t_in
    print "Tiempo bordes:"+str(tot)+"segundos"
    return foto,gx,gy

def filtro(foto,ancho,alto):#Funcion para realiza el filtrado
    t_in=time()
    pixeles=foto.load() #Cargar imagen                                                        
    for i in range(ancho):#Se recogrre la imagen
        for j in range(alto):
            con=0#Contador
            promedio=0
            (r,g,b)=foto.getpixel((i,j))
            try:
                if(pixeles[i+1,j]):#Vecinos derecho
                    promedio+=pixeles[i+1,j][0]
                    con+=1
            except:
                pass
            try:
                if(pixeles[i-1,j]):#Vecino izq
                    promedio+=pixeles[i-1,j][0]
                    con+=1
            except:
                pass
            try:
                if(pixeles[i,j+1]):#Vecino arriba
                    promedio+=pixeles[i,j+1][0]
                    con+=1
            except:
                pass
            try:
                if(pixeles[i,j-1]):#Vecino abajo
                    promedio+=pixeles[i,j-1][0]
                    con+=1
            except:
                pass
            Total=promedio/con#Promedio entre vecinos disponibles
            pixeles[i,j]=(Total,Total,Total)
    t_fi=time()
    tot=t_fi-t_in
    print "Tiempo de filtro:"+str(tot)+"segundos"
    return foto

def binarizacion(foto,ancho,alto):
    x=194
    print "Valor maximo binarizacion:"+str(x)
    pixeles=foto.load()
    for i in range(ancho):
        for j in range(alto):
            (r,g,b)=foto.getpixel((i,j))
            promedio=int((r+g+b)/3)
            if promedio > x:
                pixeles[i,j]=(255,255,255)
            else:
                pixeles[i,j]=(0,0,0)
    return foto

def formas(foto,ancho,alto):
    centro=[]
    contador=[]
    colores=[]
    figuras=[]
    pixeles=foto.load()#Cargar imagen
    for i in range(ancho):#Recorrer imagen
        for j in range (alto):
            if pixeles[i,j]==(0,0,0):#Si el pixel actual es negro
                col1=random.randint(0,255)
                col2=random.randint(0,255)#Se genera un color random
                col3=random.randint(0,255)
                r,g,b=(col1,col2,col3)
                cont,color,centro1,centro2,cordenadas,actual=bfs(foto,(i,j),(r,g,b),ancho,alto)#Se llama al bfs
                contador.append(cont)#Se agrega a la cadena contador el numero de pixeles sumados en el recorrido anterior
                colores.append(color)#Se agrega el color que se uso en el recorrido pasado
                try:
                    centros=((sum(centro1)/float(len(centro1)),sum(centro2)/float(len(centro2))))#Formula para obtener los centros
                    centro.append(centros)
                    figura= circulos(actual,centros,cont,color)
                    for i in range(ancho):
                        for j in range(alto):
                            if pixeles[i,j]==figura:
                                pixeles[i,j]=(0,0,255)
                except:
                    pass
    #print contador
    #print colores
    maximo=contador.index(max(contador))#Se obtiene el valor mas alto de la cadena contador
    #print maximo
    gris=colores[maximo]#Se obtiene el color usado en el valor mas alto del contador
    #print gris
    #rint centro1
    #rint centro2
    for i in range(ancho):#Recorrer imagen para repintar el area mas grande por gris
        for j in range(alto):
            if pixeles[i,j]==gris:
                       pixeles[i,j]=(81,81,81)
    #rint centro
    draw=ImageDraw.Draw(foto)#Pintamos un circulo en cada uno de los centros que se almacenaron en la lista centro
    for i,recor in enumerate(centro):
        draw.ellipse((recor[0]-2,recor[1]-2,recor[0]+2,recor[1]+2),fill=(0,0,0))
        #etiqueta = Label(text=i)#Se coloca la etiqueta de la figura
        #etiqueta.place(x = recor[0]+16,y = recor[1])
    return foto
    
                
def bfs(foto,actual,color,ancho,alto):
    pixeles=foto.load()
    con=0
    cola=[]#Se crea la cola
    cordenadas=[]
    centro_i=[]
    centro_j=[]
    puntos=[]
    cola.append(actual)#Se agrega el valor actual a la cola
    act=actual
    partida=pixeles[actual]#punto de partida
    #print actual
    while len(cola)>0:#Mientras existan valores en la cola hacer...
        (x,y)=cola.pop(0)#Removemos el valor de la cola
        actual=pixeles[x,y]#actual toma el valor de la cola
        if actual==partida or actual ==color:#Si el pixel actual es igual al punto de partida o color 
            
            try:
                if (pixeles[x-1,y]):#Revisar vecino izq
                    if (pixeles[x-1,y]==partida):#Si rgb de vecino izq es igual a punto de partida
                        pixeles[x-1,y]=color#Pintar pixel de color
                        cola.append((x-1,y))#Y agregar a cola
                        con+=1
                        centro_i.append((x-1))#Agregar a lista para obtener los centros
                        centro_j.append((y))
                        cordenadas.append((x-1,y))
            except:
                pass

            try:
                if (pixeles[x+1,y]):#Revisar vecino der                                                
                    if (pixeles[x+1,y]==partida):#Lo mismo vecino der
                        pixeles[x+1,y]=color
                        cola.append((x+1,y))
                        con+=1
                        centro_i.append((x+1))
                        centro_j.append((y))
                        cordenadas.append((x+1,y))
            except:
                pass
            try:
                if (pixeles[x,y-1]):#Revisar vecino abajo                                              
                    if (pixeles[x,y-1]==partida):#Lo mismo vecino abajo
                        pixeles[x,y-1]=color
                        cola.append((x,y-1))
                        con+=1
                        centro_i.append((x))
                        centro_j.append((y-1))
                        cordenadas.append((x,y-1))
                                    
            except:
                pass

            try:
                if (pixeles[x,y+1]):#Revisar vecino arriba                                              
                    if (pixeles[x,y+1]==partida):#Lo mismo vecino arriba
                        pixeles[x,y+1]=color
                        cola.append((x,y+1))
                        con+=1
                        centro_i.append((x))
                        centro_j.append((y+1))
                        cordenadas.append((x,y+1))
            except:
                pass

    return con,color,centro_i,centro_j,cordenadas,act

def turn(p1,p2,p3):
    izq=cmp(0,(p2[0]-p1[0])*(p3[1]-p1[1])-(p3[0]-p1[0])*(p2[1]-p1[1]))
    if izq == -1: return 'LEFT'
    elif izq == 0: return 'NONE'
    elif izq == 1: return 'RIGHT'

def jarvis_algorithm(cordenadas):
    hull= [min(cordenadas)]#Obtenemos el punto mas a la izq de la lista
    print hull
    i=0
    while(cordenadas):
        puntofinal=cordenadas[0]#definimos el punto de inicio como final de recorrido
        for j in range(len(cordenadas)-1):
            if puntofinal==hull[i] or turn(cordenadas[j], hull[i], puntofinal)== 'LEFT':
                puntofinal = cordenadas[j]
        i+=1
        hull.append(puntofinal)
        if puntofinal==hull[0]:
            break
    return hull

def convex_hull(foto,ancho,alto):
    pixeles=foto.load()
    puntos=[]
    for i in range(ancho):
        for j in range(alto):
            if pixeles[i,j]==(255,255,255):
                con,color,centro1,centro2,cordenadas=bfs(foto,(i,j),(0,0,255),ancho,alto)     
                puntos.append(jarvis_algorithm(cordenadas))#Guardamos los puntos del contorno
    for x in puntos: #Pintamos los puntos del contorno
        for y in x:
            pixeles[y]=(255,255,0)#de color amarillo
            print "prueba"
    return foto

def umbral(foto,ancho,alto):#Funcion para generar la imagen umbral
    minimo=random.randint(1,100)#valores para usar en el umbral               
    maximo=random.randint(101,200)
    print "Valor minimo: "+str(minimo)
    print "Valor maximo: "+str(maximo)
    pixeles=foto.load()#cargar la imagen
    for i in range(ancho):#Se recorre los pixeles de la imagen
        for a in range(alto):
            (r,g,b)=foto.getpixel((i,a))
            promedio=int((r+g+b)/3)#Obtenemos el promedio de cada pixel
            if promedio <minimo: #Se hace la comparacion con los valores 
                promedio=0
            if promedio >=maximo:
                promedio=255
            pixeles[i,a]=(promedio,promedio,promedio)#Se sustituye el valor de rgb segun sea
    return foto

def escala(foto,ancho,alto):#Creacion de imagen con escala de grises
    pixeles=foto.load()#Proceso igual que el del umbral pero sin las comparaciones
    for i in range(ancho):
        for a in range(alto):
            (r,g,b)=foto.getpixel((i,a))
            promedio=int((r+g+b)/3)
            pixeles[i,a]=(promedio,promedio,promedio)
    return foto

def circulos(actual,centro,cont,color):
    print "------------------------------"
    x1,y1=actual
    x2,y2=centro
    print "punto de inicio:"+str(actual)
    print "Centro:"+str(centro)
    area=cont
    print "Area de figura en revision:"+str(area)
    radio=math.sqrt((x2-x1)**2+(y2-y1)**2)
    print "Radio de posible circulo:"+str(radio)
    comprobar_area=(pi*(radio**2))
    print "Area de posible circulo:"+str(comprobar_area)
    if(comprobar_area-500)<area<(comprobar_area+500):
        print "La figura es un circulo"
        return color
    else:
        print "Esta figura no es un circulo"

def main():
    img= str(raw_input('Nombre de imagen: '))#Pedir imagen                                                                                                  
    foto=Image.open(img)#Abrir la imagen   
    ancho,alto=foto.size
    escalada=escala(foto,ancho,alto)
    escalada.save('escalada.jpg')
    titulo="Escala de grises"
   # ventana(escalada,ancho,alto,titulo)
    foto=Image.open(img)
    umbrales=umbral(foto,ancho,alto)
    umbrales.save('umbral.jpg')
    titulo="Umbrales"
    #ventana(umbrales,ancho,alto,titulo)
    foto=Image.open('escalada.jpg')
    filtrada=filtro(escalada,ancho,alto)
    filtrada.save('filtro.jpg')
    titulo="Filtro"
    #ventana(filtrada,ancho,alto,titulo)
    bordes,gx,gy=convolucion(filtrada,ancho,alto)
    bordes.save('Convolucion.jpg')
    titulo="Convolucion_Bordes"
    bordes=Image.open('Convolucion.jpg')
    binaria=binarizacion(bordes,ancho,alto)
    binaria.save('Binarizacion.jpg')
    titulo="Binarizacion"
    #ventana(binaria,ancho,alto,titulo)
    form=formas(binaria,ancho,alto)
    form.save('FormasyAreas.jpg')
    titulo="FormasyAreas"
    #ventana(form,ancho,alto,titulo)
    #binaria=Image.open('Binarizacion.jpg')
    #conv=convex_hull(binaria,ancho,alto)
    #conv.save('Convex.jpg')
main()

