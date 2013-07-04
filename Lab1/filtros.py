import Image
import sys
import pygame
from math import *
import random
import math

def invertir(foto,ancho,alto):
    pixel = foto.load()
    for i in range(ancho):
        for j in range(alto):
            (r,g,b) = foto.getpixel((i,j))
            if (r>0 and g>0 and b>0):
                r = 255- r
                g = 255-g
                b = 255 - b
            pixel[i,j] = (r,g,b)
    return foto    
# -------------------
def toono(foto,ancho,alto):
    pixel = foto.load()
    #pixeles = []
    for i in range(ancho):
        for j in range(alto):
            (r,g,b) = foto.getpixel((i,j))
            #if (r>100 and g>100 and b>100):
            r =(r,g,b)[0]
            g = 0
            b = 0
            pixel [i,j] = (r,g,b)
    return foto
#----------------------
def contraste(foto,ancho,alto):
    z = str(raw_input('Nivel de contraste:'))
    pixel = foto.load()
    for i in range (ancho):
        for j in range(alto):
            (r,g,b) = foto.getpixel((i,j))
            prom = int((r+g+b)/3)
            pixel[i,j] = (prom,prom,prom)
            if prom>128:
                pixel[i,j]=(255,255,255)
            else:
                pixel[i,j]=(0,0,0)
    return foto
            
#------------------------
def lumi(foto,ancho,alto):
    mini= random.randint(1,50)
    maxi =random.randint(101,200)
    print "Valor minimo de luminosidad:"+str (mini)
    print "Valor maximo de luminosidad:"+str (maxi)
    pixel = foto.load()
    for i in range(ancho):
        for j in range(alto):
            (r,g,b) = foto.getpixel((i,j))
            promedio = int((r+g+b)/3)
            if promedio <= mini:
                promedio = 0
            if promedio >= maxi:
                promedio = 255
            pixel[i,j] = (promedio,promedio,promedio)
    return foto

#-----------------------
def main():

    img = str(raw_input('Nombre de imagen:'))
    foto = Image.open(img)
    ancho,alto = foto.size
    
    invert = invertir(foto,ancho,alto)
    invert.save('invertir.jpg')

    tono = toono(foto,ancho,alto)
    tono.save('ton.jpg')
    
    foto2=Image.open(img)

    cont = contraste(foto2,ancho,alto)
    cont.save('cont.jpg')

    lum = lumi(foto,ancho,alto)
    lum.save('luminosidad.jpg')
main()
