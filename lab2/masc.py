from Tkinter import *
from PIL import Image, ImageTk
import math
import sys

def convolucion(foto,mascara):
    ancho,alto = foto.size
    pos = foto.load()
    nueva_imagen = Image.new("RGB", (ancho,alto))
    pos_nueva = nueva_imagen.load() 
    for i in range(ancho):
        for j in range(alto):
            total = 0
            for n in range(i-1, i+2):
                for m in range(j-1, j+2):
                    if n >= 0 and m >= 0 and n < ancho and m < alto:
                        total += mascara[n - (i - 1)][ m - (j - 1)] * pos[n, m][0]
            pos_nueva[i, j] = (total, total, total)
    nueva_imagen.save("convol.jpg")
    return nueva_imagen
    #return otra    

def normalizar(foto):
    x, y = foto.size
    normalizada = Image.new("RGB", (x, y))
    pixeles = []
    for i in range(y):
        for j in range(x):
            pix = foto.getpixel((j, i))[0]
            pixeles.append(pix)
    maximo = max(pixeles) 
    minimo = min(pixeles)
    print maximo
    print minimo
    l = 256.0/(maximo - minimo)
    pixeles = []
    for a in range(y):
        for b in range(x):
            pix = foto.getpixel((b, a))[0]
            nuevo_pix = int(math.floor((pix-minimo)*l))
            pixeles.append((nuevo_pix, nuevo_pix, nuevo_pix))
    normalizada.putdata(pixeles)
    normalizada.save("normalizada.jpg")
    return normalizada		


def main():
    """funcion principal
    """
    img = str(raw_input('Imagen:'))
    foto = Image.open(img)

    norm = normalizar(foto)

#Mascaras
    mascara1 = [[-1,0,1],[-2,0,2],[-1,0,1]]#mascara sobel horizontal
    mascara2 = [[1,1,1],[0,0,0],[-1,-1,-1]]#mascara sobel vertical
    mascara3 = [[1,1,1],[-1,-2,1],[-1,-1,1]]#mascara prewitt h
    mascara4 = [[-1,1,1],[-1,-2,1],[-1,1,1]]#mascara prewitt v
    
    nueva = convolucion(norm, mascara1)
    nueva.save("sobelh.jpg")
    nueva = convolucion(norm, mascara2)
    nueva.save("sobelv.jpg")
    nueva = convolucion(norm, mascara3)
    nueva.save("prewith.jpg")
    nueva = convolucion(norm, mascara4)
    nueva.save("prewitv.jpg")


if __name__ == "__main__":
    main()


