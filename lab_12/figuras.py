import Image
import math
import ImageDraw
from sys import argv
import random

MINIMUM_LINE_LENGTH = 4

def convolucion(im, g):
  w, h = im.size
  pix = im.load()
  out_im = Image.new("RGB", (w, h))
  out = out_im.load()
  for i in xrange(1, w-2):
    for j in xrange(1, h-1):
      suma1, suma2, suma3 = 0, 0, 0
      for n in xrange(i-1, i+2):
        for m in xrange(j-1, j+2):
            if n >= 0 and m >= 0 and n < w and m < h:
              suma1 += g[n - (i - 1)][ m - (j - 1)] * pix[n, m][0]
              suma2 += g[n - (i - 1)][ m - (j - 1)] * pix[n, m][1]
              suma3 += g[n - (i - 1)][ m - (j - 1)] * pix[n, m][2]
      out[i, j] = int(suma1), int(suma2), int(suma3)
  out_im.save('conv.png', "png")
  return out_im

def normalize(im):
  w, h = im.size
  pix1 = im.load()
  im2 = Image.new("RGB", (w, h))
  pix2 = im2.load()
  max_ = 0
  min_ = 256
  for i in range(w):
    for j in range(h):
      if pix1[i, j][0] > max_:
        max_ = pix1[i, j][0]
      if pix1[i, j][0] < min_:
        min_ = pix1[i, j][0]
  #print max_, min_
  prop = 256.0/(max_ - min_);
  for i in range(w):
    for j in range(h):
      curr = int(math.floor((pix1[i, j][0] - min_)*prop))
      pix2[i, j] = curr, curr, curr
  im2.save('norm.png', "png") 
  return im2 

def difference(im1, im2):
  w, h = im1.size
  pix1 = im1.load()
  pix2 = im2.load()
  output = Image.new('RGB', (w, h))
  out = output.load()
  for i in range(w): 
    for j in range(h):
      rgb = []
      for k in range(3):
        rgb.append(pix1[i, j][k] - pix2[i, j][k])
      out[i, j] = tuple(rgb)
  output.save('dife.png')
  return output

def to_binary(image, umb):
  w, h = image.size
  pix = image.load() 
  output = Image.new("RGB", (w, h))
  out_pix = output.load()
  for i in range(w):
    for j in range(h):
      if image.mode == "RGB":
        if max(pix[i, j]) >= umb: out_pix[i, j] = (255, 255, 255)
        else: out_pix[i, j] = (0, 0, 0)
      elif image.mode == "L":
        if pix[i, j] >= umb: out_pix[i, j] = 255
        else: out_pix[i, j] = 0
  output.save('bina.png', 'PNG')
  return output

def blur(image, n):
  w, h = image.size
  pix = image.load() 
  output = Image.new("RGB", (w, h))
  out_pix = output.load()
  for k in range(n):
    for i in range(w):
      for j in range(h):
        prom = []
        prom.append(list(pix[i, j]))
        if i > 0: prom.append(list(pix[i-1, j]))
        if i < w-1: prom.append(list(pix[i+1, j]))
        if j < h-1: prom.append(list(pix[i, j+1]))
        if j > 0: prom.append(list(pix[i, j-1]))
        col_totals = [ sum(x) for x in zip(*prom) ]
        out_pix[i, j] = col_totals[0]/len(prom), col_totals[1]/len(prom), col_totals[2]/len(prom)
  output.save('blur.png', "png")
  return output

def get_bordes(im1):
  im2 = blur(im1, 2)
  im3 = difference(im1, im2)
  im3 = normalize(im3)
  im3 = to_binary(im3, 70)
  im3.save('bordes.png', 'PNG')
  return im3

def modified_bfs(im, origen, color, angles):
  pix = im.load()
  w, h = im.size
  q = []
  coords = []
  init_angle = angles[origen]
  q.append(origen)
  original = pix[origen]
  while len(q) > 0:
    (x, y) = q.pop(0)
    actual = pix[x, y]
    if actual == original or actual == color:
      for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
          i, j = (x + dx, y + dy)
          if i >= 0 and i < w and j >= 0 and j < h:
            contenido = pix[i, j]
            if contenido == original and init_angle == angles[i, j]:
              pix[i, j] = color
              coords.append((i, j))
              q.append((i, j))
  im.save('output_bfs.png', 'png')
  return len(coords), coords

def bfs(im, origen, color, rewrite_file="output_bfs.png"):
  pix = im.load()
  w, h = im.size
  q = []
  coords = []
  q.append(origen)
  original = pix[origen]
  while len(q) > 0:
    (x, y) = q.pop(0)
    actual = pix[x, y]
    if actual == original or actual == color:
      for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
          i, j = (x + dx, y + dy)
          if i >= 0 and i < w and j >= 0 and j < h:
            contenido = pix[i, j]
            if contenido == original:
              pix[i, j] = color
              coords.append((i, j))
              q.append((i, j))
  im.save(rewrite_file, 'png')
  return im, len(coords), coords

def vicinity(p1, p2, limits):
  w, h = limits
  for x in range(p1[0] - 1, p1[0] + 2):
    for y in range(p1[1] - 1, p1[1] + 2):
      if x > 0 and x < w and y > 0 and y < w:
        if (x, y) == p2:
          return True
  return False

def line_in_object(obj, line, limits):
  count = 0
  for p1 in obj:
    for p2 in line:
      if vicinity(p1, p2, limits):
        count +=1
      if count > MINIMUM_LINE_LENGTH:
        return True
  return False

def get_center(obj):
  sums = [sum(x) for x in zip(*obj)]
  return (sums[0]/len(obj), sums[1]/len(obj))

def hough_transform(im, umb):
  maskx = [[-1, -1, -1], [2, 2, 2], [-1, -1, -1]]
  masky = [[-1, 2, -1], [-1, 2, -1], [-1, 2, -1]]
  #maskx = multiply(maskx, 1.0/8.0)
  #masky = multiply(masky, 1.0/8.0)
  bordes = get_bordes(im)
  pix_bor = bordes.load()
  gradx = convolucion(im, maskx)
  grady = convolucion(im, masky)
  gx = gradx.load()
  gy = grady.load()
  matrix = []
  combination = {}
  w, h = im.size
  points = {}
  bias = 12.0
  for i in range(w):
    tmp = list()
    for j in range(h):
      r, g, b = gx[i, j]
      x = r + g + b /3.0
      r, g, b = gy[i, j]
      y = r + g + b /3.0
      if (x < -1*bias or x > bias) or (y < -1*bias or y > bias):
        theta = 0.0
        if x > 0.0 and y == 0.0:
          theta = 0.0
        elif x < 0.0 and y == 0.0:
          theta = 180.0
        if x == 0.0 and y > 0.0:
          theta = 90.0
        elif x == 0.0 and y < 0.0:
          theta = 270.0
        else:
          theta = int(math.degrees( math.atan(y/x) )/10)*10
        if theta is not None:
          points[(i, j)] = theta
          rho = int( (i*math.cos(theta)) + (j*math.sin(theta))/10)*10
          if i > 0 and i < w-1 and j > 0 and j < h - 1:
            if (rho, theta) in combination:
              combination[(rho, theta)] += 1
            else:
              combination[(rho, theta)] = 1
          tmp.append((rho, theta))
      else:
        tmp.append((None, None))
    matrix.append(tmp)

  pix = im.load()
  output = Image.new('RGB', (w, h))
  lines_original = im.copy()
  lines_pix = lines_original.load()
  out = output.load()
  
  for i in range(w):
    for j in range(h):
      if i > 0 and j > 0 and i < w and j < h:
        rho, theta = matrix[i][j]
        if (rho, theta) in combination:
          out[i, j] = (255, 255, 255)
          lines_pix[i, j] = (255, 0, 0)

  lines_original.save('normal_lines.png', 'PNG')
  output.save('output_lines1.png', 'png')

  colors = []
  lines = []
  objects = []
  for i in range(w):
    for j in range(h):
      if pix_bor[i, j] == (255, 255, 255):
        _, n, coords = bfs(bordes, (i, j), (255, 0, 0))
        objects.append(coords)
      if out[i, j] == (255, 255, 255):
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        while color in colors:
          color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        colors.append(color)
        n, coords = modified_bfs(output, (i, j), color, points)
        if n > MINIMUM_LINE_LENGTH:
          lines.append(coords)
  polygons = {}
  centers = []
  act = 0

  colors = {3: (153,50,204), 4: (139,121,94), 5: (255,185,15), 6: (255,255,0), 7: (255,69,0) } 
  figures ={3: 'Triangulo', 4: 'Cuadrado', 5 : 'circulo', 6 : 'Hexagono', 7 : 'Heptagon', 8 : 'Octagono', 9 : 'desconocida'}

  draw = ImageDraw.Draw(im)
  total = w*h

  for i in range(len(objects)):

    obj = objects[i]

    polygons[i] = 0

    centro = get_center(obj)
    t = True
    for c in centers:
      if centro[0] in range(c[0]-5, c[0]+5) and centro[1] in range(c[1]-5, c[1]+5):
        t = False

    if t:
      centers.append(centro)
      for j in range(len(lines)):
        line = lines[j]
        if line_in_object(obj, line, (w, h)):
          polygons[i] += 1

      if polygons[i] > 2:
        print "Poligono %d detectado en %s. Es de %d lados"%(act+1, str(centers[act]), polygons[i])
        if polygons[i] not in colors:
          colors[polygons[i]] = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        im, n, _ = bfs(im, centers[act], colors[polygons[i]])
        #print "Porcentaje de pixeles con respecto a la imagen: %.2f%%"%((n/float(total))*100.0)
        draw.text(centers[act], "%s (%s)"%(act+1, figures[polygons[i]]), fill=(0, 0, 0))
      else:
        print "Figura desconocida %d detectada en %s"%(act+1, str(centers[act])) 
      act += 1

  output.save('output_lines.png', 'png')
  im.save('output.png', 'png')

  return im
im = Image.open(argv[1]).convert('RGB')

hough_transform(im, 1.0)
