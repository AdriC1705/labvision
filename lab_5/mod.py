from PIL import Image
import sys
import numpy as np
from math import floor

#---------Aumentar de tamanio la imagen original --------
def generar_nueva(foto,(ancho,alto)):
    pix = foto.load()
    arreglo = np.array(pix)
    print arreglo
    print 'Tamano Nuevo:' #nuevos tamanos
    x = int(raw_input('Nuevo alto:'))
    y = int(raw_input('Nuevo ancho:'))

    rat_x = (ancho * 1.0)/x 
    rat_y = (alto * 1.0)/y
    nuev = np.zeros((x,y,3))
    
    for i in range(x):
        for j in range(y):

            x_n = floor(i * rat_x)
            y_n = floor(j * rat_y)

            try:
                
                nuev[i,j] = arreglo[int(x_n),int(y_n)]
            except IndexError:
                nuev[i,j] = 0
    print 'ola'
    nueva = Image.fromarray(np.uint8(nuev))
    nueva.save('nueva.jpg')
    return nuev

#--------Funcion principal ------------------------------
def main():                
    img = str(raw_input('Imagen:'))
    foto = Image.open(img)
    ancho,alto = foto.size
    print 'Tamano actual:'
    print ancho , alto
    
    hacer_nueva = generar_nueva(foto,(ancho,alto))

main()
#--------- Fin del Programa -----------------------------
