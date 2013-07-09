import Image #esto para trabajar con imagenes                       
import sys
import math
from time import *
import random

sobelX = ([-1,0,1],[-2,0,2],[-1,0,1])
sobelY = ([1,2,1],[0,0,0],[-1,-2,-1])
#-------------------------------------------------------
def eg(img,ancho,alto):
    pixels = img.load()
    for i in range(ancho):
        for j in range(alto):
            (r,g,b) = img.getpixel((i,j))
            prom = int((r+g+b)/3)
            pixels [i,j] = (prom,prom,prom)

    return img
#-------------------------------------------------------
def conv(img,ancho,alto):
    pixels =img.load()
    pix = []
    matrizX =([-1,0,1],[-2,0,2],[-1,0,1])
    matrizY =([1,2,1],[0,0,0],[-1,-2,-1])
    
    for i in range(ancho):
        for j in range(alto):
            sumx = 0
            sumy = 0
            a=3
            for x in range(a):
                for y in range(a):
                    try:
                        sumx +=(pixels[x+i,y+j][0]*matrizX[x][y])
                        sumy += (pixels[x+i,y+j][0]*matrizY[x][y])
                    except:
                        pass        
            grad = math.sqrt(pow(sumx,2)+pow(sumy,2))
            grad = int(grad)
            pixels[i,j] = (grad,grad,grad)
            pix.append(pixels[i,j])
    #im = img.save('conv.jpg')
    return img
#----------------------------------------------------
def binarizacion(foto,ancho,alto):
    p = int(raw_input('valor para binarizar:'))
    print p
    pixel = foto.load()
    for i in range(ancho):
        for j in range(alto):
            (r,g,b) = foto.getpixel((i,j))
            promedio = ((r+g+b)/3)
            #r = (promedio * p)
            if promedio > p:
                pixel[i,j] = (255,255,255)
            else:
                pixel[i,j] = (0,0,0)
    return foto
#----------------------------------------------------
def bfs(img,ancho,alto):
    cola = []
    cola2 = []
    pixeles = img.load()
    for i in range (ancho):
        for j in range(alto):
            (r,g,b) = img.getpixel((i,j))
            if ((r,g,b,)==(255,255,255)):
                cola.append((i,j))
            else:
                cola2.append((i,j))
    return cola,cola2
#--------------------------------------------------------
def dil(foto,ancho,alto,cola):
    pixeles = foto.load()
    x=0
    while x<len(cola):
        (i,j) = cola[x]
        (r,g,b) = foto.getpixel((i,j))
        try: #derechos
            if(pixeles[i+1,j]): 
                pixeles[i+1,j] = (255,255,255)
        except:
            pass
        try: #izquierdos
            if(pixeles[i-1,j]):
                   pixeles[i-1,j] =(255,255,255)
        except:
            pass
        try:#arriba
            if(pixeles[i,j+1]):
                pixeles[i,j+1]=(255,255,255)
        except:
            pass
        try: #abajo
            if(pixeles[i,j-1]):
                pixeles[i,j-1] = (255,255,255)
        except:
            pass
        try: #esq derecha arriba
            if(pixeles[i+1,j+1]):
                pixeles[i+1,j+1]=(255,255,255)
        except:
            pass
        try: #esq izq arriba
            if(pixeles[i-1,j+1]):
                pixeles[i-1,j+1] = (255,255,255)
        except:
            pass
        try:#esq derecha abajo
            if(pixeles[i+1,j-1]):
                pixeles[i+1,j-1] = (255,255,255)
        except:
            pass
        try: #esq izq abajo
            if(pixeles[i-1,j-1]):
                pixeles[i-1,j-1] = (255,255,255)
        except:
            pass
        x+=1
    return foto
#--------------------------------------------------------
def eros(foto,ancho,alto,cola):
    pixeles = foto.load()
    x=0
    while x<len(cola):
        (i,j) = cola[x]
        (r,g,b) = foto.getpixel((i,j))
        try: #derechos                      
            if(pixeles[i+1,j]):
                pixeles[i+1,j] = (0,0,0)
        except:
            pass
        try: #izquierdos       
            if(pixeles[i-1,j]):
                   pixeles[i-1,j] =(0,0,0)
        except:
            pass
        try:#arriba                                                                                                    
            if(pixeles[i,j+1]):
                pixeles[i,j+1]=(0,0,0)
        except:
            pass
        try: #abajo                                                                  
            if(pixeles[i,j-1]):
                pixeles[i,j-1] = (0,0,0)
        except:
            pass
        try: #esq derecha arriba                                                                        
            if(pixeles[i+1,j+1]):
                pixeles[i+1,j+1]=(0,0,0)
        except:
            pass
        try: #esq izq arriba                  
            if(pixeles[i-1,j+1]):
                pixeles[i-1,j+1] = (0,0,0)
        except:
            pass
        try:#esq derecha abajo          
            if(pixeles[i+1,j-1]):
                pixeles[i+1,j-1] = (0,0,0)
        except:
            pass
        try: #esq izq abajo      
            if(pixeles[i-1,j-1]):
                pixeles[i-1,j-1] = (0,0,0)
        except:
            pass
        x+=1
    return foto
#--------------------------------------------------------    
def main():
    img = str(raw_input('Nombre de la imagen:'))
    foto = Image.open(img)
    ancho,alto = foto.size
    
    escg =eg (foto,ancho,alto)
    escg.save('eg.jpg')
    
    binarizar = binarizacion(escg,ancho,alto)
    binarizar.save('binarizada.jpg')

    convol = conv(binarizar,ancho,alto)
    convol.save('conv.jpg')

    cola,cola2 = bfs(convol,ancho,alto)

    dilatado = dil(foto,ancho,alto,cola)
    dilatado.save('aumento.jpg')

    erosionado = eros(foto,ancho,alto,cola2)
    erosionado.save('menos_borde.jpg')

main()
