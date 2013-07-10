from PIL import Image, ImageDraw, ImageFont
import sys, time, random, math

def prod(v,vv):
    return float(sum((a*b) for a, b in zip(v, vv)))

def angulo(p1,p2,p3):
    v = (p1[0]-p1[0], p2[1]-p1[1])
    vv = (p2[0] - p3[0], p2[1] - p3[1])

    producto = prod(v,vv)
    producto_dom = math.sqrt(prod(v,v))*math.sqrt(prod(vv,vv))
    angulo = 0.0
    if producto_dom !=9:
        angulo = producto/producto_dom
        if angulo>=1.0:
            return 0.0
        elif angulo <= -1.0:
            return math.pi
        else:
            angulo = math.degrees(math.acos(angulo))
    return angulo
#------------------------------------------------------------------
def jarvis(puntos,img):
    puntos_hull = min(puntos)
    wrap_pts = list()
    i = 0
    
    while False is not True:
        wrap_pts.append(puntos_hull)
        fin_pts = [puntos[0],0.0]
        #----------------
        for a in range(0,len(puntos)):
            if len(wrap_pts)>1:
                obtener_angulo = angulo(wrap_pts[i-1], wrap_pts[i], puntos[a])
            else:
                tmp = (wrap_pts[0][0], wrap_pts[0][1]-1)
                obtener_angulo = angulo(tmp, wrap_pts[i], puntos[a])
            if(fin_pts[0] == puntos_hull) or angulo > fin_pts[1]:
                fin_pts[0] = puntos[a]
                fin_pts[1] = angulo
        i = i+1
        puntos_hull = fin_pts[0]
        if fin_pts[0] == wrap_pts[0]:
            break
    draw = ImageDraw.Draw(img)
    for i in range(1,len(wrap_pts)):
        draw.line((wrap_pts[len(wrap_pts)-1][0], wrap_pts[i-1][1], wrap_pts[i][0],wrap_pts[i][1]), fill = (255,0,0))
    draw.line((wrap_pts[len(wrap_pts)-1][0], wrap_pts[len(wrap_pts)-1][1],wrap_pts[0][0], wrap_pts[0][1]), fill = (255,0,0))

#------------------------------------------------------------------
def dfs(img, visitados, inicio, output="convex.jpg"):
    pixeles = img.load()
    sig = list()
    sig.append(inicio)
    puntos = list()
    color = pixeles[tuple(inicio)]
    if color !=(255,255,255):
        return
    while len(sig)>0:
        actual = sig.pop(0)
        puntos.append(actual)
        visitados[tuple(actual)] = True
        
        for i in range(actual[0]-1,actual[0]+2):
            for j in range(actual[1]-1,actual[1]+2):
                if i>=0 and j>=0 and i<img.size[0] and j<img.size[1]:
                    if not visitados[i,j]:
                        if color == pixeles[i,j]:
                            if not [i,j] in sig:
                                sig.append([i,j])
    jarvis(puntos,img)
#------------------------------------------------------------------
def nuevo_visitados(tamano):
    visitados = dict()
    for i in range(tamano[0]):
        for j in range(tamano[1]):
            visitados[i,j] = False
    return visitados

#------------------------------------------------------------------
def main(output= "convex.jpg"):
    img = str(raw_input('Nombre de la imagen:'))
    foto = Image.open(img)
    
    visitados = nuevo_visitados(foto.size)
    
    for i in range(foto.size[0]):
        for j in range(foto.size[1]):
            if not visitados[i,j]:
                dfs(foto,[i,j],visitados)
    foto.save(output)
main()
