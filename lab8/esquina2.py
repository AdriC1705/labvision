import Tkinter
import Image, ImageTk, ImageDraw, ImageFont
from sys import argv
import math
import random

file = argv[1]

im = Image.open(file).convert("RGB")
grayscaleim = Image.open(file).convert("RGB")
original = im
(x,y) = im.size

def bfs(pixel, imagen, pintura):
    k=0
    (w,h)=imagen.size
    lista = []
    lista.append(pixel)
    (r,g,b)=imagen.getpixel(pixel)
    color = r #Suponiendo que la imagen esta en blanco y negro.
    for x,y in lista:
        for i in range(x, x+1):
            for j in range(y, y+1):
                if i >= 0 and j >= 0 and i < w and j < h:
                    if imagen.getpixel((i,j))==(r,g,b):
                        lista.append((i,j))
                        imagen.putpixel((i,j), pintura)
                        #im.save(str(k)+".png")
                        k+=1
                    try:
                        if imagen.getpixel((i-1,j))==(r,g,b):
                            lista.append((i-1,j))
                            imagen.putpixel((i-1,j), pintura)
                            #im.save(str(k)+".png")
                            k+=1
                    except:
                        None
                    try:
                        if imagen.getpixel((i,j-1))==(r,g,b):
                            lista.append((i,j-1))
                            imagen.putpixel((i,j-1), pintura)
                            #im.save(str(k)+".png")
                            k+=1
                    except:
                        None   
                    try:
                        if imagen.getpixel((i+1,j))==(r,g,b):
                            lista.append((i+1,j))
                            imagen.putpixel((i+1,j), pintura)
                            #im.save(str(k)+".png")
                            k+=1
                    except:
                        None
                    try:
                        if imagen.getpixel((i,j+1))==(r,g,b):
                            lista.append((i,j+1))
                            imagen.putpixel((i,j+1), pintura) 
                            #im.save(str(k)+".png")
                            k+=1
                    except:
                        None
    return lista

def centros(objs):
    centroides = []
    for obj in objs:
        xobj = []
        yobj = []
        for coord in obj:
            xobj.append(coord[0])
            yobj.append(coord[1])
        centroides.append(((sum(xobj)/len(xobj)), (sum(yobj)/len(yobj))))
    return centroides

def dilation(image, iter):
    k=0
    while k<iter:
        for i in range(x):
            for j in range(y):
                if image.getpixel((i,j))==(255,255,255):
                    try:
                        image.putpixel((i-1,j),(255,255,255))
                    except:
                        pass
        for i in reversed(range(x)):
            for j in reversed(range(y)):
                if image.getpixel((i,j))==(255,255,255):
                    try:
                        image.putpixel((i+1,j),(255,255,255))
                    except:
                        pass
        for i in range(x):
            for j in range(y):
                if image.getpixel((i,j))==(255,255,255):
                    try:
                        image.putpixel((i,j-1),(255,255,255))
                    except:
                        pass
        for i in reversed(range(x)):
            for j in reversed(range(y)):
                if image.getpixel((i,j))==(255,255,255):
                    try:
                        image.putpixel((i,j+1),(255,255,255))
                    except:
                        pass
        k+=1
    return image

def b_and_w(scale):
    grayscale("prom",im)
    for i in range(x):
        for j in range(y):
            pixel = im.getpixel((i,j))[0]
            if(pixel<scale):
                pixel = 0
            else:
                pixel = 255
            im.putpixel((i,j), (pixel,pixel,pixel))
    

def grayscale(tipo, im):
    for i in range(x):
        for j in range(y):
            (r,g,b)=original.getpixel((i, j))
            if tipo == "min":
                gray = min((r,g,b))
            if tipo == "max":
                gray = max((r,g,b))
            if tipo == "r":
                gray = r
            if tipo == "g":
                gray = g
            if tipo == "b":
                gray = b
            if tipo == "prom":
                gray = (r+g+b)/3
            im.putpixel((i,j), (gray,gray,gray))
    return im

def puntos(imagen):
    lista = []
    for i in range(x):
        for j in range(y):
            if imagen.getpixel((i,j))!=(0,255,0) and imagen.getpixel((i,j))!=(0,0,0):
                lista.append(bfs((i,j), imagen, (0,255,0)))
    return lista

def median_blur(maxiter):
    imagen = Image.open(file).convert("RGB")
    imagen = grayscale("prom",imagen)
    iter = 0
    while iter < maxiter:
        print "Iteracion: ", iter+1
        for i in range(x):
            for j in range(y):
                prom = []
                k=1
                pixel=imagen.getpixel((i, j))[0]
                prom.append(imagen.getpixel((i, j))[0])
                try:
                    prom.append(imagen.getpixel((i-1, j))[0])
                    k+=1
                except:
                    pass
                try:
                    prom.append(imagen.getpixel((i-1 ,j-1))[0])
                    prom.append(imagen.getpixel((i, j-1))[0])
                    k+=2
                except:
                    pass
                try:
                    prom.append(imagen.getpixel((i+1, j-1))[0])
                    prom.append(imagen.getpixel((i+1, j))[0])
                    k+=2
                except:
                    pass
                try:
                    prom.append(imagen.getpixel((i-1, j+1))[0])
                    prom.append(imagen.getpixel((i, j+1))[0])
                    prom.append(imagen.getpixel((i+1, j+1))[0])
                    k+=3
                except:
                    pass
                promedio = 0;
                prom.sort()
                promedio=prom[k/2]
                im.putpixel((i,j), (pixel-promedio,pixel-promedio,pixel-promedio))
        iter+=1

def esquinas():
    median_blur(1)
    b_and_w(20)
    dilation(im,2)
    points = puntos(im)
    coords = []
    for lista in points:
        coords.append(max(lista))
    algo = centros([coords])
    print algo
    grados = {}
    for coord in coords:
        dx = algo[0][0] - coord[0]
        dy = algo[0][1] - coord[1]
        rads = math.atan2(-dy,dx)
        rads %= 2*math.pi
        gr = math.degrees(rads)
        grados.update({gr:coord})
    keys = grados.keys()
    keys.sort()
    lineas = []
    ln = ImageDraw.Draw(im)
    for key in keys:
        lineas.append(grados[key])
    lineas.append(grados[keys[0]])
    ln.line(lineas, fill="red")
    im.save("B_"+file)

esquinas()

ventana = Tkinter.Tk()
im2 = ImageTk.PhotoImage(im)
Tkinter.Label(ventana, image=im2).pack()

ventana.mainloop()
