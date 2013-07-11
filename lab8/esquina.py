from PIL import Image, ImageTk, ImageDraw
import numpy as np
import math


#--------------------------------------------------------------------
def escala(foto,ancho,alto):#Creacion de imagen con escala de grises
    pixeles=foto.load()#Proceso igual que el del umbral pero sin las comparaciones
    for i in range(ancho):
        for a in range(alto):
            (r,g,b)=foto.getpixel((i,a))
            promedio=int((r+g+b)/3)
            pixeles[i,a]=(promedio,promedio,promedio)
    print "escala .."
    return foto
#--------------------------------------------------------------------
def filtro_medio(foto,ancho,alto):
    pixeles=foto.load()#Cargarimagen
    for i in range(ancho):#Se recogrrelaimagen                              
        for j in range(alto):                        
            (r,g,b)=foto.getpixel((i,j))
            cola=[]
            try:
                if(pixeles[i+1,j]):#Vecinos derecho                           
                    pix=pixeles[i+1,j][0]
                    cola.append((pix))
            except:
                pass
            try:
                if(pixeles[i-1,j]):#Vecino izq             
                    pix=pixeles[i-1,j][0]
                    cola.append((pix))
            except:
                pass
            try:
                if(pixeles[i,j+1]):#Vecino arriba                 
                    pix=pixeles[i,j+1][0]
                    cola.append((pix))
            except:
                pass
            try:
                if(pixeles[i,j-1]):#Vecino abajo        
                    pix=pixeles[i,j-1][0]
                    cola.append((pix))
            except:
                pass                        
            try:
                if(pixeles[i+1,j+1]):#esq derecha
                    pix=pixeles[i+1,j+1][0]
                    cola.append((pix))
            except:
                pass
            try:
                if(pixeles[i-1,j+1]):#esq izq 
                    pix=pixeles[i-1,j+1][0]
                    cola.append((pix))
            except:
                pass
            try:
                if(pixeles[i+1,j-1]):#esq der abajo
                    pix=pixeles[i+1,j-1][0]
                    cola.append((pix))
            except:
                pass
            try:
                if(pixeles[i-1,j-1]):#esq izq abajo
                    pix=pixeles[i-1,j-1][0]
                    cola.append((pix))
            except:
                pass
            cola.sort()
            mediano=int(np.median(cola))
            pixeles[i,j]=(mediano,mediano,mediano)
    print "filtro medio"
    return foto
#-------------------------------------------------------------
def diferencia(foto,foto2,ancho,alto):
    img=Image.open('escalada.png')
    pixeles=img.load()
    pixeles2=foto2.load()
    for i in range(ancho):
        for j in range(alto):
            (r,g,b)=foto.getpixel((i,j))
            (r,g,b)=foto2.getpixel((i,j))
            nueva=pixeles2[i,j][0]
            original=pixeles[i,j][0]
            dif=(nueva-original)
            pixeles[i,j]=(dif,dif,dif)
    print"diferenciando ..."
    return img
#-----------------------------------------------------------
def convolucion(foto,ancho,alto):
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
    print"Convolucion ...."
    return foto
#-----------------------------------------------------------------
def binarizacion(foto,ancho,alto):
    x=100
    #print "Valor maximo binarizacion:"+str(x)
    pixeles=foto.load()
    for i in range(ancho):
        for j in range(alto):
            (r,g,b)=foto.getpixel((i,j))
            promedio=int((r+g+b)/3)
            if promedio > x:
                pixeles[i,j]=(255,255,255)
            else:
                pixeles[i,j]=(0,0,0)
    print "Binarizando..."
    return foto
#-------------------------------------------------------------------
def pix_esquina(img,original,ancho,alto):
    pixel = img.load()
    foto2 = original.load()
    pix = ()
    for i in range (ancho):
        for j in range(alto):
            c = 0
            prom = 0.0
            try:
                if(pixel[i+1,j] == (255,255,255)):
                    #prom += pixel[i+1,j][0]
                    c +=1
                    pix.append(pixel[i+1,j])
            except:
                prom += 0
            try:
                if(pixel[i-1,j] == (255,255,255)):
                       #prom += pixel[i-1,j][0]
                    c +=1
                    pix.append(pixel[i-1,j])
            except:
                pass
            try:
                if(pixel[i,j+1] == (255,255,255)):
                       #prom += pixel[i,j+1][0]
                    c+=1
                    pix.append(pixel[i,j+1])
            except:
                pass
            try:
                if(pixel[i,j-1]==(255,255,255)):
                       #prom += pixel[i,j-1][0]
                    c+=1
                    pix.append(pixel[i,j-1])
            except:
                pass
            
    draw = ImageDraw.Draw(pixel)
    draw.rectangle(pix, fill = "green")
    
    print "eskina"
    return pixel
    
#--------------------------------------------------------------------
def main():
    img= str(raw_input('Nombre de imagen: '))         
    foto=Image.open(img)#Abrir la imagen   
    ancho,alto=foto.size
    escalada=escala(foto,ancho,alto)
    escalada.save('escalada.png')
    filtromedio=filtro_medio(escalada,ancho,alto)
    filtromedio.save('filtromedio.jpg')
    diferenciada=diferencia(escalada,filtromedio,ancho,alto)
    diferenciada.save('diferencia.jpg')
    bordes=convolucion(diferenciada,ancho,alto)
    bordes.save('convolucion.jpg')
    binaria=binarizacion(bordes,ancho,alto)
    binaria.save('Binarizacion.jpg') 
#------- Marcar las eskinas en la imagen original
    esquina = pix_esquina(binaria,foto,ancho,alto)
    esquina.save("esquina.py")
main()
