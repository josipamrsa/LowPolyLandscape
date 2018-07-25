import pygame
from pygame.locals import *
from pygame.constants import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

# FLOAT BROJEVI ZA GLAĐE KRETNJE PO EKRANU
from random import uniform
# OBJECT LOADER MODUL ZA IMPORTANJE OBJ MODELA IZ BLENDERA
from objloader import *                                                                 

# GLOBALNE VARIJABLE #

# VARIJABLE OKOLISA I ZVIJEZDA
rpx, rpy = (180,272)
star_flag = False

# VARIJABLE ZA POLOZAJ I ROTACIJU PAUKA
rsx, rsy = (180,272)
roty, rotx = 1, -3
xs, ys, zs = 2, -0.9, -4.0
x, z = 0, 0

# VARIJABLE ZA POLOZAJ I ROTACIJU LEPTIRA
xl = 0.05
yl = 0.0
xmov = 1
rotly, rotlx = 3, 1
leptir_flag = False

# PYGAME VARIJABLE
clock = pygame.time.Clock()
viewport = (800,600)



# OSVJETLJENJE #

def osvjetljenje(): 
    glEnable(GL_LIGHTING)
    glEnable(GL_COLOR_MATERIAL)
    glEnable(GL_DEPTH_TEST)
    glShadeModel(GL_SMOOTH)
    
def dnevno_osvjetljenje():
    glClearColor(0.5, 0.7, 1.0, 0.7)    
    osvjetljenje()
    glLightfv(GL_LIGHT0, GL_POSITION,  (120, 1, 0, 0.0))
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (1.0, 0.8, 1.0, 0.5))
    glEnable(GL_LIGHT0)  
    glLightfv(GL_LIGHT0, GL_AMBIENT, (1.0, 1.0, 1.0, 0.5))
    
def nocno_osvjetljenje():
    glClearColor(0.1, 0.2, 0.5, 0.7)
    osvjetljenje()
    glLightfv(GL_LIGHT1, GL_POSITION,  (0, 1, 120, 0.0))
    glLightfv(GL_LIGHT1, GL_DIFFUSE, (0.0, 0.0, 1.0, 1.0))
    glEnable(GL_LIGHT1)
    glLightfv(GL_LIGHT0, GL_AMBIENT, (0.1, 0.2, 0.5, 0.5))
      

def dobaDana():
    global xs, star_flag

    if xs < 0.5:          
        nocno_osvjetljenje()
        star_flag = True
    else:
        dnevno_osvjetljenje()
        star_flag = False


# KONTROLE #

def kontrole():
    global rpx, rpy, rsx, rsy
    global clock, leptir_flag
    global xs, yz, zs, roty, rotx
    global x, z, xl, xmov
      
    clock.tick(30)                      # INTERVAL OSVJEŽAVANJA PROZORA
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.display.quit()       # GASENJE PROZORA
            pygame.quit()
            sys.exit()
        elif e.type == KEYDOWN and e.key == K_ESCAPE:
            pygame.display.quit()
            pygame.quit()
            sys.exit()
        
        # PAUK #
        
        # KRETANJE LIJEVO (A)
        elif e.type == KEYDOWN and e.key == K_a:
            x = -5
            z = 0
            roty = 1
            rotx = -3
            dobaDana()

        # KRETANJE DOLJE (S)
        elif e.type == KEYDOWN and e.key == K_s:    
            x = 0
            z = 5
            roty = 3
            rotx = -1
            dobaDana()

        # KRETANJE DESNO (D)
        elif e.type == KEYDOWN and e.key == K_d:
            x = 5
            z = 0
            roty = 3
            rotx = 1
            dobaDana()

        # KRETANJE GORE (W)
        elif e.type == KEYDOWN and e.key == K_w:
            x = 0
            z = -5       
            roty = 1
            rotx = 3
            dobaDana()

        # ZAUSTAVI KRETANJE (X)
        elif e.type == KEYDOWN and e.key == K_x:
            x = 0
            z = 0

        # LEPTIR #
        
        # ZAUSTAVI / POKRENI LEPTIRA (C / C)
        elif e.type == KEYDOWN and e.key == K_c:
            if xmov == 1:
                xmov = 0
                leptir_flag = True
                
            elif xmov == -1:
                xmov = 0
                leptir_flag = False

            elif xmov == 0:
                if leptir_flag:
                    xmov = 1
                else:
                    xmov -= 1

        
# INICIJALIZACIJSKE FUNKCIJE ZA PYOPENGL I PYGAME #
                    
def InitGL(viewport):
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    width, height = viewport
    gluPerspective(45.0, width/float(height), 1, 50.0)
    glClearColor(0.5, 0.7, 1.0, 0.7)
    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_MODELVIEW)
    

def InitPyGame():
    global viewport, zpos, zvijezde   
    pygame.init()
    srf = pygame.display.set_mode(viewport, OPENGL | DOUBLEBUF)


# POMICANJE PO EKRANU #
    
def pauk_pomak():
    global xs, zs, x, z, roty, rotx
    # UKOLIKO PAUK DODJE DO RUBA ON SE OKREĆE U SUPROTNOM SMJERU SVE DO IDUĆEG PRITISKA KONTROLNE TIPKE #
    if xs > 2.0:
        # LIJEVO
        x = -5
        z = 0
        roty = 1
        rotx = -3
             
    if xs < -2.0:        
        # DESNO
        x = 5
        z = 0
        roty = 3
        rotx = 1        

    if zs < -5.0:
        # GORE
        x = 0
        z = 5
        roty = 3
        rotx = -1
        
    if zs > -2.5:
        # DOLJE
        x = 0
        z = -5       
        roty = 1
        rotx = 3
               
    xs = xs + 0.03 * x
    zs = zs + 0.03 * z

def leptir_pomak():
    global xl, yl, xmov, rotly, rotlx

    if xl > 2.0:
        # ROTIRAJ LIJEVO KRAJ DESNOG RUBA EKRANA
        xmov = -1
        rotly = 1
        rotlx = -3  
        
    if xl < -2.0:
        # ROTIRAJ DESNO KRAJ LIJEVOG RUBA EKRANA
        xmov = 1     
        rotly = 3
        rotlx = 1
        
    xl = xl + 0.1 * xmov
    yl = uniform(0.0, 0.1)


# OBJEKTI #
    
def pauk():
    global xs, ys, zs, roty, x, z
    glLoadIdentity()
    paukObj = OBJ(b"spider.obj", swapyz=True)
    glTranslatef(xs, ys, zs)
    glRotate(rsy, -1, 0, 0)
    glRotate(rsx, rotx, roty, 0)
    glScale(0.2, 0.2, 0.2)
    pauk_pomak() 
    glCallList(paukObj.gl_list)
    
def leptir():
    global xl, yl, xmov
    glLoadIdentity()
    leptirObj = OBJ(b"butterfly3.obj", swapyz=True)
    glTranslate(xl, yl, -4.0)
    glRotate(rpy, -1, 0, 0)
    glRotate(rpx, rotlx, rotly, 0)
    glScale(0.1, 0.1, 0.1)
    glCallList(leptirObj.gl_list)
    leptir_pomak()
      
def okolis():
    glLoadIdentity()
    okolisObj = OBJ(b"lowpoly.obj", swapyz=True)
    glTranslate(0.0, -1.0, -4.0)
    glRotate(rpy, -1, 0, 0)
    glRotate(rpx, 0, -1, 0)
       
    glCallList(okolisObj.gl_list)

def zvijezda():
    glLoadIdentity()   
    trzx = uniform(-5.0, 5.0)
    trzy = uniform(-0.5, 5.0)
    zvijezdaObj = OBJ(b"star.obj", swapyz=True)
    glTranslate(trzx, trzy, -9.0)
    glRotate(rpy, 0, 1, 0)
    glRotate(rpx, 1, 0, 0)
    glScale(0.1, 0.1, 0.1)    
    glCallList(zvijezdaObj.gl_list)
    
    
# POSTAVLJANJE SCENE

def postaviScenu():
    global viewport, star_flag, xs
    InitPyGame() 
    dnevno_osvjetljenje()
    InitGL(viewport)

    while 1:      
        kontrole()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        if star_flag:
            for i in range(30):
                zvijezda()
        pauk()
        okolis()
        leptir()
        
        pygame.display.flip()

postaviScenu()

