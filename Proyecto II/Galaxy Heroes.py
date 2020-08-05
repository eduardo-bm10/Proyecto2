#////////////////////// BIBLIOTECAS //////////////////////////////////////////////////////////
from tkinter import *
import pygame as pg
import os
import glob
import time
from threading import Thread
import random

#////////////////// GLOBALES ////////////////////////////////////////////////////////////////

OPEN=True
POINTS=0
SHOT=True
PLAYERSHOW= []
BATTERY=100
SHOWNAME=''
DIFF=2

UP=False
DOWN=False
RIGHT=False
LEFT=False

#////////////////// CARGAR IMAGENES Y MULTIMEDIA ////////////////////////////////////////////

#CARGADOR DE IMAGENES INMOVILES
def Imagenes(Ubicacion):
    Ruta = os.path.join(Ubicacion)
    Img = PhotoImage(file=Ruta)
    return Img

#CARGADOR DE BANDA SONORA
def musica(archivo):
    if isinstance(archivo,str):
        pg.mixer.init()
        pg.mixer.music.load(archivo)
        pg.mixer.music.play(10)
    else:
        pg.mixer.quit()
        
#CREADOR DE IMAGENES PARA ANIMACION
def ImagenesAnim(x, Result):
    if x==[]:
        return Result
    else:
        Result.append(PhotoImage(file=x[0]))
        return ImagenesAnim(x[1:],Result)

#CARGARDOR DE SPRITES PARA ANIMAR
def sprites(Ruta):
    x = glob.glob(Ruta)
    x.sort()
    return ImagenesAnim(x,[])    

#////////////////////// VENTANA PRINCIPAL //////////////////////////////////////////////////////////////////////////////

Menu = Tk()
Menu.minsize(1200, 650)
Menu.resizable(False, False)
Menu.title('Galaxy Heroes')
Menu.iconbitmap('Imagenes/Icono.ico')

musica('Audio\\LEGO Star Wars II DS Soundtrack.mp3')

Fondo = Canvas(Menu, width=1200, height=650, bg='black')
Fondo.place(x=0, y=0)

MainTitle = Label(Menu, width=15, text='GALAXY HEROES', font=('Georgia',40), fg='lemonchiffon', bg='maroon')
MainTitle.place(x=350, y=80)

FondoImg = Imagenes('Imagenes\\Background\\FondoMenu.png')
Space = Fondo.create_image(0, 325, tags=('FONDO'), image=FondoImg)

#MOVIMIENTO DEL MENU PRINCIPAL
def mov_fondo():
    Centro = Fondo.coords('FONDO')
    if Centro!=[]:
        Fondo.coords('FONDO', Centro[0]+5, Centro[1])
        if Centro[0]==1200:
            Fondo.coords('FONDO', 0, Centro[1])
    def call():
        mov_fondo()
    Fondo.after(40,call)

mov_fondo()

#///////////////////////////// PANTALLA DE JUEGO //////////////////////////////////////////////////////////////////////////

#INICIO DE LA JUGABILIDAD/GAMEPLAY
def juego(Mode):
    Pant = Toplevel()
    Pant.minsize(1200,650)
    Pant.resizable(False, False)
    Pant.title('Galaxy Heroes')
    Pant.iconbitmap('Imagenes/Icono.ico')

    Menu.withdraw()
    musica(1)
    musica('Audio\\Star Force (NES) Music - Stage Theme.mp3')

    Bg = Canvas(Pant, width=1200, height=650, bg='maroon')
    Bg.place(x=0,y=0)

    Display = Canvas(Pant, width=1200, height=90, bg='dimgray')
    Display.place(x=0, y=0)

    global SHOWNAME
    Name = Label(Display, width=10, text=SHOWNAME, font=('Georgia',15), fg='lemonchiffon', bg='maroon')
    Name.place(x=700, y=50)

    #MUESTRA IMAGEN DEL PILOTO ESCOGIDO EN LA PANTALLA DE JUEGO
    def show_player():
        global PLAYERSHOW
        Display.create_image(900, 50, image=PLAYERSHOW)

    #RETORNO AL MENU PRINCIPAL
    def back():
        global OPEN, BATTERY, PLAYERSHOW, SHOWNAME, POINTS
        OPEN=False
        BATTERY=100
        PLAYERSHOW=[]
        SHOWNAME=''
        POINTS=0
        Pant.destroy()
        musica(1)
        musica('Audio\\LEGO Star Wars II DS Soundtrack.mp3')
        Menu.deiconify()   
            
    #//////////////////////////////////////////TIEMPO, PUNTOS Y FIN DE JUEGO///////////////////////////////////////////////////////////////////

    #CONTADOR DE TIEMPO DE JUEGO EN SEGUNDOS
    def tiempo(Seg):
        global OPEN
        if OPEN == True:
            try:
                time.sleep(1)
                time_label = Label(Pant, width=10, text='Tiempo:'+ str(Seg), font=('Georgia',15), fg='lemonchiffon', bg='darkslategrey')
                time_label.place(x=150,y=50)
                Thread(target=tiempo,args=(Seg+1,)).start()
            except:
                return

    #ACUMULADOR DE PUNTOS DE PARTIDA ACTUAL
    def points(p):
        global POINTS
        POINTS+=p
        Cont = Label(Display, width=10, text='Puntos:'+str(POINTS), font=('Georgia',15), fg='lemonchiffon', bg='darkslategrey')
        Cont.place(x=350, y=50)
        
    #GUARDADO DE PUNTOS ACUMULADOS EN UN ARCHIVO SECUENCIAL 
    def enter_puntos():
        global POINTS
        print(POINTS)
        updatetxt(str(POINTS) + "\n")

    #AUXILIAR DEL GUARDADO DE PUNTOS ACUMULADOS
    def updatetxt(Texto):
        file = open("PUNTUACIONES.txt", "a")
        file.write(Texto)
        file.close()
        
    #FIN DE LA PARTIDA
    def game_over():
        global POINTS, OPEN
        End = Label(Pant, width=25, text='FIN DEL JUEGO', font=('Times', 25), fg='ghostwhite', bg='darkslategray')
        End.place(x=587.5, y=325)
        TotPun = Label(Pant, width=25, text='OBTUVISTE '+str(POINTS)+' PUNTOS', font=('Times', 25), fg='ghostwhite', bg='darkslategray')
        TotPun.place(x=587.5, y=425)
        enter_puntos()
        musica(1)
        OPEN=False

    #AUMENTO PROGRESIVO DE LA DIFICULTAD
    def dificultad(): 
        global DIFF, OPEN
        if OPEN == True:
            if DIFF == 1:
                print('Fácil')
                time.sleep(60)
                DIFF += 1
                return dificultad()
            elif DIFF == 2:
                print('Medio')
                time.sleep(60)
                DIFF += 1
                return dificultad()
            elif DIFF == 3:
                print('Difícil')
                return None
            
    Thread(target=dificultad).start()
        
    Exit = Button(Display, text='Abandonar', font=('Helvatica'), command=back, fg='lemonchiffon', bg='darkslategrey')
    Exit.place(x=10, y=20)

    #///////////////////////////////////// CARGAR IMAGENES MISCELANEAS ////////////////////////////////////////////////////

    fondojuego = Imagenes('Imagenes\\Background\\GameBG.png') #IMAGEN DE FONDO DE LA PANTALLA DE JUEGO
    BgFondo = Bg.create_image(600, 325, image=fondojuego)
    
    Spaceship = Bg.create_image(600, 325, tags=('MYSHIP'))  #CREACION DE LA IMAGEN DE LA NAVE

    SpaceshipImg = sprites('Imagenes/Spaceship/playership*.png') #SPRITES DE LA NAVE DEL JUGADOR

    ShotCent = sprites('Imagenes\\Spaceship\\shotcenter*.png')  #SPRITES PARA EL DISPARO DE LA NAVE

    RechargeImg = Imagenes('Imagenes/Spaceship/Combustible/RechargeIcon.png')   #COMBUSTIBLE LLENO COLECCIONABLE
    BatteryFull = Imagenes('Imagenes\\Spaceship\\Combustible\\Battery1.png')    #COMBUSTIBLE LLENO
    BatteryMedium = Imagenes('Imagenes\\Spaceship\\Combustible\\Battery2.png')  #COMBUSTIBLE MEDIO LLENO
    BatteryMedium1 = Imagenes('Imagenes\\Spaceship\\Combustible\\Battery3.png') #COMBUSTIBLE MEDIO VACIO
    BatteryEmpty = Imagenes('Imagenes\\Spaceship\\Combustible\\Battery4.png')   #COMBUSTIBLE CASI VACIO
    BatteryDead = Imagenes('Imagenes\\Spaceship\\Combustible\\Battery5.png')    #COMBUSTIBLE VACIO

    #///////////////////////////////////// MODOS DE JUEGO //////////////////////////////////////////////////////////////

    #/////////////////////////////////MODO DESTRUCCION DE ASTEROIDES/////////////////////////////////////////////////////
    
    if Mode==1:
        global SHOT
        SHOT=True
        SpritesAst=sprites('Imagenes/Asteroides/ast*.png')  #SPRITES DE LOS ASTEROIDES

        #GENERADOR ALEATORIO DE ASTEROIDES
        def generate_ast(t):        
            global OPEN, DIFF
            if OPEN==True:
                try:
                    Ast1 = Bg.create_image(random.randint(100,1100),random.randint(100,500), tags=('ast1')) #CREA LA IMAGEN DEL PRIMER ASTEROIDE
                    Ast2 = Bg.create_image(random.randint(100,1100),random.randint(100,500), tags=('ast2')) #CREA LA IMAGEN DEL SEGUNDO ASTEROIDE
                    Ast3 = Bg.create_image(random.randint(100,1100),random.randint(100,500), tags=('ast3')) #CREA LA IMAGEN DEL TERCER ASTEROIDE
                    Ast4 = Bg.create_image(random.randint(100,1100),random.randint(100,500), tags=('ast4')) #CREA LA IMAGEN DEL CUARTO ASTEROIDE
                    Ast5 = Bg.create_image(random.randint(100,1100),random.randint(100,500), tags=('ast5')) #CREA LA IMAGEN DEL QUINTO ASTEROIDE
                    Ast6 = Bg.create_image(random.randint(100,1100),random.randint(100,500), tags=('ast6')) #CREA LA IMAGEN DEL SEXTO ASTEROIDE
                    Ast7 = Bg.create_image(random.randint(100,1100),random.randint(100,500), tags=('ast7')) #CREA LA IMAGEN DEL SEPTIMO ASTEROIDE
                    Ast8 = Bg.create_image(random.randint(100,1100),random.randint(100,500), tags=('ast8')) #CREA LA IMAGEN DEL OCTAVO ASTEROIDE
                    Ast9 = Bg.create_image(random.randint(100,1100),random.randint(100,500), tags=('ast9')) #CREA LA IMAGEN DEL NOVENO ASTEROIDE

                    ListAst = [Ast1, Ast2, Ast3, Ast4, Ast5, Ast6, Ast7, Ast8, Ast9]                       
                    if t==5:
                        if DIFF>=1:
                            ast_3D(0,ListAst[0])    #INVOCA AL PRIMER ASTEROIDE
                            time.sleep(1)
                            ast_3D(0,ListAst[1])    #INVOCA AL SEGUNDO ASTEROIDE
                            time.sleep(1)
                            ast_3D(0,ListAst[2])    #INVOCA AL TERCER ASTEROIDE
                        if DIFF>=2:
                            time.sleep(1)
                            ast_3D(0,ListAst[3])    #INVOCA AL CUARTO ASTEROIDE
                            time.sleep(1)
                            ast_3D(0,ListAst[4])    #INVOCA AL QUINTO ASTEROIDE
                            time.sleep(1)
                            ast_3D(0,ListAst[5])    #INVOCA AL SEXTO ASTEROIDE
                        if DIFF==3:
                            time.sleep(1)
                            ast_3D(0,ListAst[6])    #INVOCA AL SEPTIMO ASTEROIDE
                            time.sleep(1)
                            ast_3D(0,ListAst[7])    #INVOCA AL OCTAVO ASTEROIDE
                            time.sleep(1)
                            ast_3D(0,ListAst[8])    #INVOCA AL NOVENO ASTEROIDE
                        return generate_ast(0)
                    else:
                        time.sleep(1)
                        t+=1
                        return generate_ast(t)
                except:
                    return None

        #EFECTO 3D DE LOS ASTEROIDES
        def ast_3D(i, tag):              
            global OPEN
            if OPEN==True:
                if i==20:
                    colision_ship_ast()
                    return Bg.delete(tag)
                else:
                    Bg.itemconfig(tag, image=SpritesAst[i]) #AUMENTA EL TAMANO DEL ASTEROIDE
                    i+=1
                def call():
                    ast_3D(i, tag)
                Pant.after(100,call)

        #UN ASTEROIDE COLISIONA CONTRA LA NAVE
        def colision_ship_ast():
            Ship = Bg.bbox(Spaceship)
            Ast1 = Bg.bbox('ast1')
            Ast2 = Bg.bbox('ast2')
            Ast3 = Bg.bbox('ast3')
            Ast4 = Bg.bbox('ast4')
            Ast5 = Bg.bbox('ast5')
            Ast6 = Bg.bbox('ast6')
            Ast7 = Bg.bbox('ast7')
            Ast8 = Bg.bbox('ast8')
            Ast9 = Bg.bbox('ast9')
            if Ship != None and Ast1 != None:
                if (Ast1[0]<Ship[0]<Ast1[2] or Ast1[0]<Ship[2]<Ast1[2]) and (Ast1[1]<Ship[3]<Ast1[3] or Ast1[1]<Ship[1]<Ast1[3]):   #SE EVALUA EL CHOQUE DEL PRIMER ASTEROIDE
                    return game_over()
            if Ship!=None and Ast2!=None:
                if (Ast2[0]<Ship[0]<Ast2[2] or Ast2[0]<Ship[2]<Ast2[2]) and (Ast2[1]<Ship[3]<Ast2[3] or Ast2[1]<Ship[1]<Ast2[3]):   #SE EVALUA EL CHOQUE DEL SEGUNDO ASTEROIDE
                    return game_over()
            if Ship!=None and Ast3!=None:
                if (Ast3[0]<Ship[0]<Ast3[2] or Ast3[0]<Ship[2]<Ast3[2]) and (Ast3[1]<Ship[3]<Ast3[3] or Ast3[1]<Ship[1]<Ast3[3]):   #SE EVALUA EL CHOQUE DEL TERCER ASTEROIDE
                    return game_over()
            if Ship!=None and Ast4!=None:
                if (Ast4[0]<Ship[0]<Ast4[2] or Ast4[0]<Ship[2]<Ast4[2]) and (Ast4[1]<Ship[3]<Ast4[3] or Ast4[1]<Ship[1]<Ast4[3]):   #SE EVALUA EL CHOQUE DEL CUARTO ASTEROIDE
                    return game_over()
            if Ship!=None and Ast5!=None:
                if (Ast5[0]<Ship[0]<Ast5[2] or Ast5[0]<Ship[2]<Ast5[2]) and (Ast5[1]<Ship[3]<Ast5[3] or Ast5[1]<Ship[1]<Ast5[3]):   #SE EVALUA EL CHOQUE DEL QUINTO ASTEROIDE
                    return game_over()
            if Ship!=None and Ast6!=None:
                if (Ast6[0]<Ship[0]<Ast6[2] or Ast6[0]<Ship[2]<Ast6[2]) and (Ast6[1]<Ship[3]<Ast6[3] or Ast6[1]<Ship[1]<Ast6[3]):   #SE EVALUA EL CHOQUE DEL SEXTO ASTEROIDE
                    return game_over()
            if Ship!=None and Ast7!=None:
                if (Ast7[0]<Ship[0]<Ast7[2] or Ast7[0]<Ship[2]<Ast7[2]) and (Ast7[1]<Ship[3]<Ast7[3] or Ast7[1]<Ship[1]<Ast7[3]):   #SE EVALUA EL CHOQUE DEL SEPTIMO ASTEROIDE
                    return game_over()
            if Ship!=None and Ast8!=None:
                if (Ast8[0]<Ship[0]<Ast8[2] or Ast8[0]<Ship[2]<Ast8[2]) and (Ast8[1]<Ship[3]<Ast8[3] or Ast8[1]<Ship[1]<Ast8[3]):   #SE EVALUA EL CHOQUE DEL OCTAVO ASTEROIDE
                    return game_over()
            if Ship!=None and Ast9!=None:
                if (Ast9[0]<Ship[0]<Ast9[2] or Ast9[0]<Ship[2]<Ast9[2]) and (Ast9[1]<Ship[3]<Ast9[3] or Ast9[1]<Ship[1]<Ast9[3]):   #SE EVALUA EL CHOQUE DEL NOVENO ASTEROIDE
                    return game_over()
            else:
                return None

        #EL DISPARO COLISIONA CONTRA UN ASTEROIDE
        def colision_disp():
            global DIFF
            Disp=Bg.bbox('shot1')
            Ast1 = Bg.bbox('ast1')
            Ast2 = Bg.bbox('ast2')
            Ast3 = Bg.bbox('ast3')
            Ast4 = Bg.bbox('ast4')
            Ast5 = Bg.bbox('ast5')
            Ast6 = Bg.bbox('ast6')
            Ast7 = Bg.bbox('ast7')
            Ast8 = Bg.bbox('ast8')
            Ast9 = Bg.bbox('ast9')
            if Disp!=None and Ast1!=None:
                if Ast1[0]<Disp[0]<Disp[2]<Ast1[2] and Ast1[1]<Disp[1]<Disp[3]<Ast1[3]: #EVALUA EL DISPARO CONTRA EL PRIMER ASTEROIDE
                    if DIFF==1:
                        points(50)
                    if DIFF==2:
                        points(20)
                    if DIFF==3:
                        points(15)
                    return Bg.delete('ast1')
            if Disp!=None and Ast2!=None:
                if Ast2[0]<Disp[0]<Disp[2]<Ast2[2] and Ast2[1]<Disp[1]<Disp[3]<Ast2[3]: #EVALUA EL DISPARO CONTRA EL SEGUNDO ASTEROIDE
                    if DIFF==1:
                        points(50)
                    if DIFF==2:
                        points(20)
                    if DIFF==3:
                        points(15)
                    return Bg.delete('ast2')
            if Disp!=None and Ast3!=None:
                if Ast3[0]<Disp[0]<Disp[2]<Ast3[2] and Ast3[1]<Disp[1]<Disp[3]<Ast3[3]: #EVALUA EL DISPARO CONTRA EL TERCER ASTEROIDE
                    if DIFF==1:
                        points(50)
                    if DIFF==2:
                        points(20)
                    if DIFF==3:
                        points(15)
                    return Bg.delete('ast3')
            if Disp!=None and Ast4!=None:
                if Ast4[0]<Disp[0]<Disp[2]<Ast4[2] and Ast4[1]<Disp[1]<Disp[3]<Ast4[3]: #EVALUA EL DISPARO CONTRA EL CUARTO ASTEROIDE
                    if DIFF==1:
                        points(50)
                    if DIFF==2:
                        points(20)
                    if DIFF==3:
                        points(15)
                    return Bg.delete('ast4')
            if Disp!=None and Ast5!=None:
                if Ast5[0]<Disp[0]<Disp[2]<Ast5[2] and Ast5[1]<Disp[1]<Disp[3]<Ast5[3]: #EVALUA EL DISPARO CONTRA EL QUINTO ASTEROIDE
                    if DIFF==1:
                        points(50)
                    if DIFF==2:
                        points(20)
                    if DIFF==3:
                        points(15)
                    return Bg.delete('ast5')
            if Disp!=None and Ast6!=None:
                if Ast6[0]<Disp[0]<Disp[2]<Ast6[2] and Ast6[1]<Disp[1]<Disp[3]<Ast6[3]: #EVALUA EL DISPARO CONTRA EL SEXTO ASTEROIDE
                    if DIFF==1:
                        points(50)
                    if DIFF==2:
                        points(20)
                    if DIFF==3:
                        points(15)                   
                    return Bg.delete('ast6')
            if Disp!=None and Ast7!=None:
                if Ast7[0]<Disp[0]<Disp[2]<Ast7[2] and Ast7[1]<Disp[1]<Disp[3]<Ast7[3]: #EVALUA EL DISPARO CONTRA EL SEPTIMO ASTEROIDE
                    if DIFF==1:
                        points(50)
                    if DIFF==2:
                        points(20)
                    if DIFF==3:
                        points(15)
                    return Bg.delete('ast7')
            if Disp!=None and Ast8!=None:
                if Ast8[0]<Disp[0]<Disp[2]<Ast8[2] and Ast8[1]<Disp[1]<Disp[3]<Ast8[3]: #EVALUA EL DISPARO CONTRA EL OCTAVO ASTEROIDE
                    if DIFF==1:
                        points(50)
                    if DIFF==2:
                        points(20)
                    if DIFF==3:
                        points(15)
                    return Bg.delete('ast8')
            if Disp!=None and Ast9!=None:
                if Ast9[0]<Disp[0]<Disp[2]<Ast9[2] and Ast9[1]<Disp[1]<Disp[3]<Ast9[3]: #EVALUA EL DISPARO CONTRA EL NOVENO ASTEROIDE
                    if DIFF==1:
                        points(50)
                    if DIFF==2:
                        points(20)
                    if DIFF==3:
                        points(15)
                    return Bg.delete('ast9')
            else:
                return None
            
        Thread(target=generate_ast, args=(0,)).start()

    #///////////////////////////////////////////////////// MODO MANIOBRA DE PRUEBAS ///////////////////////////////////////////////////////////////////
        
    if Mode==2:
        SHOT=False
        Anillos=sprites('Imagenes/Anillos/Ring*.png')

        #GENERADOR ALEATORIO DE ANILLOS
        def generate_ring(t):       
            global OPEN, DIFF
            if OPEN==True:
                try:
                    Ring1 = Bg.create_image(random.randint(100,1100), random.randint(100,500), tags=('ring1'))  #CREA EL PRIMER ANILLO
                    Ring2 = Bg.create_image(random.randint(100,1100), random.randint(100,500), tags=('ring2'))  #CREA EL SEGUNDO ANILLO
                    Ring3 = Bg.create_image(random.randint(100,1100), random.randint(100,500), tags=('ring3'))  #CREA EL TERCER ANILLO
                    Ring4 = Bg.create_image(random.randint(100,1100), random.randint(100,500), tags=('ring4'))  #CREA EL CUARTO ANILLO
                    Ring5 = Bg.create_image(random.randint(100,1100), random.randint(100,500), tags=('ring5'))  #CREA EL QUINTO ANILLO
                    Ring6 = Bg.create_image(random.randint(100,1100), random.randint(100,500), tags=('ring6'))  #CREA EL SEXTO ANILLO
                    Ring7 = Bg.create_image(random.randint(100,1100), random.randint(100,500), tags=('ring7'))  #CREA EL SEPTIMO ANILLO
                    Ring8 = Bg.create_image(random.randint(100,1100), random.randint(100,500), tags=('ring8'))  #CREA EL OCTAVO ANILLO
                    Ring9 = Bg.create_image(random.randint(100,1100), random.randint(100,500), tags=('ring9'))  #CREA EL NOVENO ANILLO

                    ListRing = [Ring1, Ring2, Ring3, Ring4, Ring5, Ring6, Ring7, Ring8, Ring9]
                    if t==5:
                        if DIFF>=1:
                            ring_3D(0,ListRing[0])  #INVOCA EL PRIMER ANILLO
                            time.sleep(1)
                            ring_3D(0,ListRing[1])  #INVOCA EL SEGUNDO ANILLO
                            time.sleep(1)
                            ring_3D(0,ListRing[2])  #INVOCA EL TERCER ANILLO
                        if DIFF>=2:
                            time.sleep(1)
                            ring_3D(0,ListRing[3])  #INVOCA EL CUARTO ANILLO
                            time.sleep(1)
                            ring_3D(0,ListRing[4])  #INVOCA EL QUINTO ANILLO
                            time.sleep(1)
                            ring_3D(0,ListRing[5])  #INVOCA EL SEXTO ANILLO
                        if DIFF==3:
                            time.sleep(1)   
                            ring_3D(0,ListRing[6])  #INVOCA EL SEPTIMO ANILLO
                            time.sleep(1)
                            ring_3D(0,ListRing[7])  #INVOCA EL OCTAVO ANILLO
                            time.sleep(1)
                            ring_3D(0,ListRing[8])  #INVOCA EL NOVENO ANILLO
                        return generate_ring(0)
                    else:
                        time.sleep(1)
                        return generate_ring(t+1)
                except:
                    return None

        #EFECTO 3D DE LOS ANILLOS
        def ring_3D(i, tag):        
            global OPEN
            if OPEN==True:
                if i==20:
                    colision_ring()
                    return Bg.delete(tag)
                else:
                    Bg.itemconfig(tag,image=Anillos[i]) #AUMENTA EL TAMANO DEL ANILLO
                    i+=1
                def call():
                    ring_3D(i,tag)
                Pant.after(120,call)

        #COLISION DE LOS ANILLOS CONTRA LA NAVE
        def colision_ring():
            Ship = Bg.bbox(Spaceship)
            Ring1 = Bg.bbox('ring1')
            Ring2 = Bg.bbox('ring2')
            Ring3 = Bg.bbox('ring3')
            Ring4 = Bg.bbox('ring4')
            Ring5 = Bg.bbox('ring5')
            Ring6 = Bg.bbox('ring6')
            Ring7 = Bg.bbox('ring7')
            Ring8 = Bg.bbox('ring8')
            Ring9 = Bg.bbox('ring9')
            if Ship!=None and Ring1!=None:      #EVALUA LA COLISION DEL PRIMER ANILLO
                Ring1In = (Ring1[0]+10, Ring1[1]+10, Ring1[2]-10, Ring1[3]-10)
                if Ship[0]<Ring1[0]<Ring1In[0]<Ship[2] or Ship[0]<Ring1In[2]<Ring1[2]<Ship[2] and Ship[1]<Ring1[1]<Ring1In[1]<Ship[3] or Ship[1]<Ring1In[3]<Ring1[3]<Ship[3]:
                    return game_over()
                if Ring1In[0]<Ship[0]<Ring1In[2] and Ring1In[1]<Ship[1]<Ring1In[3]:
                    if DIFF==1:
                        points(50)
                    if DIFF==2:
                        points(20)
                    if DIFF==3:
                        points(15)
                else:
                    return 
            if Ship!=None and Ring2!=None:      #EVALUA LA COLISION DEL SEGUNDO ANILLO
                Ring2In = (Ring2[0]+10, Ring2[1]+10, Ring2[2]-10, Ring2[3]-10)
                if Ship[0]<Ring2[0]<Ring2In[0]<Ship[2] or Ship[0]<Ring2In[2]<Ring2[2]<Ship[2] and Ship[1]<Ring2[1]<Ring2In[1]<Ship[3] or Ship[1]<Ring2In[3]<Ring2[3]<Ship[3]:
                    return game_over()
                if Ring2In[0]<Ship[0]<Ring2In[2] and Ring2In[1]<Ship[1]<Ring2In[3]:
                    if DIFF==1:
                        points(50)
                    if DIFF==2:
                        points(20)
                    if DIFF==3:
                        points(15)
                else:
                    return 
            if Ship!=None and Ring3!=None:      #EVALUA LA COLISION DEL TERCER ANILLO
                Ring3In = (Ring3[0]+10, Ring3[1]+10, Ring3[2]-10, Ring3[3]-10)
                if Ship[0]<Ring3[0]<Ring3In[0]<Ship[2] or Ship[0]<Ring3In[2]<Ring3[2]<Ship[2] and Ship[1]<Ring3[1]<Ring3In[1]<Ship[3] or Ship[1]<Ring3In[3]<Ring3[3]<Ship[3]:
                    return game_over()
                if Ring3In[0]<Ship[0]<Ring3In[2] and Ring3In[1]<Ship[1]<Ring3In[3]:
                    if DIFF==1:
                        points(50)
                    if DIFF==2:
                        points(20)
                    if DIFF==3:
                        points(15)
                else:
                    return 
            if Ship!=None and Ring4!=None:      #EVALUA LA COLISION DEL CUARTO ANILLO 
                Ring4In = (Ring4[0]+10, Ring4[1]+10, Ring4[2]-10, Ring4[3]-10)
                if Ship[0]<Ring4[0]<Ring4In[0]<Ship[2] or Ship[0]<Ring4In[2]<Ring4[2]<Ship[2] and Ship[1]<Ring4[1]<Ring4In[1]<Ship[3] or Ship[1]<Ring4In[3]<Ring4[3]<Ship[3]:
                    return game_over()
                if Ring4In[0]<Ship[0]<Ring4In[2] and Ring4In[1]<Ship[1]<Ring4In[3]:
                    if DIFF==1:
                        points(50)
                    if DIFF==2:
                        points(20)
                    if DIFF==3:
                        points(15)
                else:
                    return 
            if Ship!=None and Ring5!=None:      #EVALUA LA COLISION DEL QUINTO ANILLO
                Ring5In = (Ring5[0]+10, Ring5[1]+10, Ring5[2]-10, Ring5[3]-10)
                if Ship[0]<Ring5[0]<Ring5In[0]<Ship[2] or Ship[0]<Ring5In[2]<Ring5[2]<Ship[2] and Ship[1]<Ring5[1]<Ring5In[1]<Ship[3] or Ship[1]<Ring5In[3]<Ring5[3]<Ship[3]:
                    return game_over()
                if Ring5In[0]<Ship[0]<Ring5In[2] and Ring5In[1]<Ship[1]<Ring5In[3]:
                    if DIFF==1:
                        points(50)
                    if DIFF==2:
                        points(20)
                    if DIFF==3:
                        points(15)
                else:
                    return 
            if Ship!=None and Ring6!=None:      #EVALUA LA COLISION DEL SEXTO ANILLO
                Ring6In = (Ring6[0]+10, Ring6[1]+10, Ring6[2]-10, Ring6[3]-10)
                if Ship[0]<Ring6[0]<Ring6In[0]<Ship[2] or Ship[0]<Ring6In[2]<Ring6[2]<Ship[2] and Ship[1]<Ring6[1]<Ring6In[1]<Ship[3] or Ship[1]<Ring6In[3]<Ring6[3]<Ship[3]:
                    return game_over()
                if Ring6In[0]<Ship[0]<Ring6In[2] and Ring6In[1]<Ship[1]<Ring6In[3]:
                    if DIFF==1:
                        points(50)
                    if DIFF==2:
                        points(20)
                    if DIFF==3:
                        points(15)
                else:
                    return 
            if Ship!=None and Ring7!=None:      #EVALUA LA COLISION DEL SEPTIMO ANILLO
                Ring7In = (Ring7[0]+10, Ring7[1]+10, Ring7[2]-10, Ring7[3]-10)
                if Ship[0]<Ring7[0]<Ring7In[0]<Ship[2] or Ship[0]<Ring7In[2]<Ring7[2]<Ship[2] and Ship[1]<Ring7[1]<Ring7In[1]<Ship[3] or Ship[1]<Ring7In[3]<Ring7[3]<Ship[3]:
                    return game_over()
                if Ring7In[0]<Ship[0]<Ring7In[2] and Ring7In[1]<Ship[1]<Ring7In[3]:
                    if DIFF==1:
                        points(50)
                    if DIFF==2:
                        points(20)
                    if DIFF==3:
                        points(15)
                else:
                    return 
            if Ship!=None and Ring8!=None:      #EVALUA LA COLISION DEL OCTAVO ANILLO
                Ring8In = (Ring8[0]+10, Ring8[1]+10, Ring8[2]-10, Ring8[3]-10)
                if Ship[0]<Ring8[0]<Ring8In[0]<Ship[2] or Ship[0]<Ring8In[2]<Ring8[2]<Ship[2] and Ship[1]<Ring8[1]<Ring8In[1]<Ship[3] or Ship[1]<Ring8In[3]<Ring8[3]<Ship[3]:
                    return game_over()
                if Ring8In[0]<Ship[0]<Ring8In[2] and Ring8In[1]<Ship[1]<Ring8In[3]:
                    if DIFF==1:
                        points(50)
                    if DIFF==2:
                        points(20)
                    if DIFF==3:
                        points(15)
                else:
                    return 
            if Ship!=None and Ring9!=None:      #EVALUA LA COLISION DEL NOVENO ANILLO
                Ring9In = (Ring9[0]+10, Ring9[1]+10, Ring9[2]-10, Ring9[3]-10)
                if Ship[0]<Ring9[0]<Ring9In[0]<Ship[2] or Ship[0]<Ring9In[2]<Ring9[2]<Ship[2] and Ship[1]<Ring9[1]<Ring9In[1]<Ship[3] or Ship[1]<Ring9In[3]<Ring9[3]<Ship[3]:
                    return game_over()
                if Ring9In[0]<Ship[0]<Ring9In[2] and Ring9In[1]<Ship[1]<Ring9In[3]:
                    if DIFF==1:
                        points(50)
                    if DIFF==2:
                        points(20)
                    if DIFF==3:
                        points(15)
                else:
                    return 
            else:
                return 

        Thread(target=generate_ring, args=(0,)).start()

    #/////////////////////////////////// FUNCIONES DE MOVIMIENTO DE LA NAVE ////////////////////////////////////////////////

    #ANIMACION DE LA NAVE PRINCIPAL
    def anim(i):    
        global OPEN
        if i==2:
            i=0
        if OPEN==True:
            try:
                Bg.itemconfig('MYSHIP', image=SpaceshipImg[i])
                time.sleep(0.15)
                Thread(target=anim, args=(i+1,)).start()
            except:
                return None

    #MOVIMIENTO DE LA NAVE HACIA ARRIBA
    def arriba():      
        global UP
        if UP==True:
            Ubi = Bg.coords('MYSHIP')
            if Ubi!=[]:
                Bg.coords('MYSHIP', Ubi[0], Ubi[1]-10)
                if (Ubi[1]-10)==145:
                    Bg.coords('MYSHIP', Ubi[0], Ubi[1])
        Pant.after(20,arriba)
    def UpT(event):
        global UP
        UP=True
    def UpF(event):
        global UP
        UP=False

    #MOVIMIENTO DE LA NAVE HACIA ABAJO
    def abajo():       
        global DOWN
        if DOWN==True:
            Ubi = Bg.coords('MYSHIP')
            if Ubi!=[]:
                Bg.coords('MYSHIP', Ubi[0], Ubi[1]+10)
                if (Ubi[1]+10)==585:
                    Bg.coords('MYSHIP', Ubi[0], Ubi[1])
        Pant.after(20,abajo)
    def DownT(event):
        global DOWN
        DOWN=True
    def DownF(event):
        global DOWN
        DOWN=False

    #MOVIMIENTO DE LA NAVE HACIA LA DERECHA
    def derecha():     
        global RIGHT
        if RIGHT==True:
            Ubi = Bg.coords('MYSHIP')
            if Ubi!=[]:
                Bg.coords('MYSHIP', Ubi[0]+10, Ubi[1])
                if (Ubi[0]+10)==1100:
                    Bg.coords('MYSHIP', Ubi[0], Ubi[1])
        Pant.after(20,derecha)
    def RightT(event):
        global RIGHT
        RIGHT=True
    def RightF(event):
        global RIGHT
        RIGHT=False

    #MOVIMIENTO DE LA NAVE HACIA LA IZQUIERDA
    def izquierda():
        global LEFT
        if LEFT==True:
            Ubi = Bg.coords('MYSHIP')
            if Ubi!=[]:
                Bg.coords('MYSHIP', Ubi[0]-10, Ubi[1])
                if (Ubi[0]-10)==100:
                    Bg.coords('MYSHIP', Ubi[0], Ubi[1])
        Pant.after(20,izquierda)
    def LeftT(event):
        global LEFT
        LEFT=True
    def LeftF(event):
        global LEFT
        LEFT=False

    #DISPARO DE LA NAVE PRINCIPAL
    def shooting(event):
        global SHOT
        if SHOT==True:
            Loc = Bg.coords('MYSHIP')
            Bg.create_image(Loc[0], Loc[1]-50, tags=('shot1'))
            SHOT=False
            return mov_shot(0)
    def mov_shot(i):    #MOVIMIENTO DEL DISPARO
        global SHOT
        Blast = Bg.coords('shot1')
        if Blast!=[]:
            if i==20:
                SHOT=True
                colision_disp()
                return Bg.delete('shot1')
            else:
                Bg.coords('shot1', Blast[0], Blast[1]-3)
                Bg.itemconfig('shot1', image=ShotCent[i])
                i+=1
        def call():
            mov_shot(i)
        Pant.after(15,call)
            
    #/////////////////////////////////////////// BATERIA /////////////////////////////////////////////////////////////////////
    
    Battery = Display.create_image(600, 50, tags=('battery'), image=BatteryFull) #CREA LA IMAGEN DE LA BATERIA COLECCIONABLE

    #DURACION DE COMBUSTIBLE
    def empty_battery():
        global BATTERY, OPEN
        if OPEN==True:
            if BATTERY==0:
                Display.itemconfig('battery',image=BatteryDead) #COMBUSTIBLE VACIO
                return game_over()
            elif 75<BATTERY<=100:
                Display.itemconfig('battery',image=BatteryFull) #COMBUSTIBLE LLENO
                BATTERY-=1
                return Display.after(500,empty_battery)
            elif 50<BATTERY<=75:
                Display.itemconfig('battery',image=BatteryMedium)   #COMBUSTIBLE MEDIO LLENO
                BATTERY-=1
                return Display.after(500,empty_battery)
            elif 25<BATTERY<=50:
                Display.itemconfig('battery',image=BatteryMedium1)  #COMBUSTIBLE MEDIO VACIO
                BATTERY-=1
                return Display.after(500,empty_battery)
            elif 0<BATTERY<=25:
                Display.itemconfig('battery',image=BatteryEmpty)    #COMBUSTIBLE CASI VACIO
                BATTERY-=1
                return Display.after(500,empty_battery)

    #GENERADOR DE BATERIAS FLOTANTES
    def generate_battery(t,r):
        global OPEN
        if OPEN == True:
            if t == 25:
                if r==0:    
                    Bg.create_image(0,random.uniform(100,500),tags=('battery'), image=RechargeImg)`#GENERA LA BATERIA A LA DERECHA
                    move_fullbattery(0)
                    return generate_battery(0,random.randint(0,3))
                elif r==1:  
                    Bg.create_image(1200,random.uniform(100,500),tags=('battery'), image=RechargeImg)   #GENERA LA BATERIA A LA IZQUIERDA
                    move_fullbattery(1)
                    return generate_battery(0,random.randint(0,3))
                elif r==2:
                    Bg.create_image(random.uniform(100,1100),0,tags=('battery'), image=RechargeImg) #GENERA LA BATERIA ARRIBA
                    move_fullbattery(2)
                    return generate_battery(0,random.randint(0,3))
                elif r==3:
                    Bg.create_image(random.uniform(100,1100),650,tags=('battery'), image=RechargeImg)   #GENERA LA BATERIA ABAJO
                    move_fullbattery(3)
                    return generate_battery(0,random.randint(0,3))
            else:
                time.sleep(1)
                return generate_battery(t+1,r)

    #MOVIMIENTO DE LA BATERIA FLOTANTE
    def move_fullbattery(S):
        Coord = Bg.coords('battery')
        if Coord!=[]:
            if S==0:
                Bg.coords('battery', Coord[0]+5, Coord[1])
                if Coord[0]+5==600:
                    return Bg.delete('battery')
            elif S==1:
                Bg.coords('battery', Coord[0]-5, Coord[1])
                if Coord[0]-5==600:
                    return Bg.delete('battery')
            elif S==2:
                Bg.coords('battery', Coord[0], Coord[1]+5)
                if Coord[1]+5==325:
                    return Bg.delete('battery')
            elif S==3:
                Bg.coords('battery', Coord[0], Coord[1]-5)
                if Coord[1]-5==325:
                    return Bg.delete('battery')
            def call():
                move_fullbattery(S)
            Bg.after(40, call)

    #COLISION PARA RECOLECTAR LA BATERIA FLOTANTE
    def colision_battery():
        global BATTERY
        Ship = Bg.bbox('MYSHIP')
        Batt = Bg.bbox('battery')
        if Ship!=None and Batt!=None:
            if (Ship[0]<Batt[0]<Ship[2] or Ship[0]<Batt[2]<Ship[2]) and (Ship[1]<Batt[3]<Ship[3] or Ship[1]<Batt[1]<Ship[3]):
                BATTERY+=50
                Bg.delete('battery')
                return Bg.after(10,colision_battery)
            else:
                return Bg.after(10,colision_battery)
        else:
            return Bg.after(10,colision_battery)

    Thread(target=generate_battery, args=(0,random.randint(0,1),)).start()
    colision_battery()
        

    #//////////////////////////////////////////// BINDS Y LLAMADAS ///////////////////////////////////////////////////////////

    arriba()
    abajo()
    derecha()
    izquierda()

    show_player()
    anim(0)
    empty_battery()
    points(0)

    Thread(target = tiempo, args = (0,)).start()

    Pant.bind('<w>',UpT)
    Pant.bind('<KeyRelease w>',UpF)
    Pant.bind('<s>',DownT)
    Pant.bind('<KeyRelease s>',DownF)
    Pant.bind('<d>',RightT)
    Pant.bind('<KeyRelease d>',RightF)
    Pant.bind('<a>',LeftT)
    Pant.bind('<KeyRelease a>',LeftF)
    Pant.bind('<Control_R>',shooting)

    Pant.mainloop()

#//////////////////////////////////// SELECCION DE MODO DE JUEGO ///////////////////////////////////////////////////////////////  

#SELECCIONA EL MODO DE DESTRUCCION DE ASTEROIDES
def select_juego1():
    global OPEN, PLAYERSHOW
    if PLAYERSHOW==[]:
        return print('ELIJA UN PILOTO EN CONFIGURACION')
    else:
        OPEN=True
        return dificultad(1)

#SELECCIONA EL MODO DE MANIOBRA DE PRUEBAS
def select_juego2():
    global OPEN, PLAYERSHOW
    if PLAYERSHOW==[]:
        return print('ELIJA UN PILOTO EN CONFIGURACION')
    else:
        OPEN=True
        return dificultad(2)

#/////////////////////////////////// PANTALLA DE CONFIGURACION ////////////////////////////////////////////////////////////////

#VENTANA DE CONFIGURACION Y SELECCION DE PILOTOS
def config():
    Config = Toplevel()
    Config.minsize(700,500)
    Config.resizable(False, False)
    Config.title('Galaxy Heroes')
    Config.iconbitmap('Imagenes/Icono.ico')
    
    C_config = Canvas(Config,width=700,height=500,bg='white')
    C_config.place(x=0,y=0)

    ImgFondo = Imagenes('Imagenes/Background/playbg.png')
    imgCanvas_config = C_config.create_image(350,250,image= ImgFondo)

    #/////////////////////////////////////////// CARGAR PILOTOS ////////////////////////////////////////////////////////
    
    Eduardo = Imagenes('Imagenes/Pilotos/Eduardo.png')      #CARGA LA IMAGEN DE EDUARDO
    Max = Imagenes('Imagenes/Pilotos/Max.png')              #CARGA LA IMAGEN DE MAX
    Pilot1img = Imagenes('Imagenes/Pilotos/Piloto1.png')    #CARGA LA IMAGEN DE REYES
    Pilot2img = Imagenes('Imagenes/Pilotos/Piloto2.png')    #CARGA LA IMAGEN DE JILL
    Pilot3img = Imagenes('Imagenes/Pilotos/Piloto3.png')    #CARGA LA IMAGEN DE X CHAMPION
    Pilot4img = Imagenes('Imagenes/Pilotos/Piloto4.png')    #CARGA LA IMAGEN DE METEOR
    Pilot5img = Imagenes('Imagenes/Pilotos/Piloto5.png')    #CARGA LA IMAGEN DE MYSTERIO
    Pilot6img = Imagenes('Imagenes/Pilotos/Piloto6.png')    #CARGA LA IMAGEN DE ASTRID
    Pilot7img = Imagenes('Imagenes/Pilotos/Piloto7.png')    #CARGA LA IMAGEN DE PEACH
    Pilot8img = Imagenes('Imagenes/Pilotos/Piloto8.png')    #CARGA LA IMAGEN DE SHEEVA
    Pilot9img = Imagenes('Imagenes/Pilotos/Piloto9.png')    #CARGA LA IMAGEN DE RIPER
    Pilot10img = Imagenes('Imagenes/Pilotos/Piloto10.png')  #CARGA LA IMAGEN DE ASHOKA

    Select = Label(C_config, text='Selecciona un piloto', font=('Georgia',20), fg='lemonchiffon', bg='maroon')
    Select.place(x=240, y=30)

    #////////////////////////////////////////// SELECCIONAR PILOTOS //////////////////////////////////////////////////////

    #SELECCION DE EDUARDO
    def edu():
        global PLAYERSHOW, SHOWNAME
        print('Eduardo Seleccionado')
        SHOWNAME=''
        PLAYERSHOW = Eduardo
        SHOWNAME+='Eduardo'
    #SELECCION DE MAX
    def maX():
        global PLAYERSHOW, SHOWNAME
        print('Max Seleccionado')
        SHOWNAME=''
        PLAYERSHOW = Max
        SHOWNAME+='Max'
    #SELECCION DE REYES
    def pilot1():
        global PLAYERSHOW, SHOWNAME
        print('Reyes Seleccionado')
        SHOWNAME=''
        PLAYERSHOW = Pilot1img
        SHOWNAME+='Reyes'
    #SELECCION DE JILL
    def pilot2():
        global PLAYERSHOW, SHOWNAME
        print('Jill Seleccionado')
        SHOWNAME=''
        PLAYERSHOW = Pilot2img
        SHOWNAME+='Jill'
    #SELECCION DE X CHAMPION
    def pilot3():
        global PLAYERSHOW, SHOWNAME
        print('X Champion Seleccionado')
        SHOWNAME=''
        PLAYERSHOW = Pilot3img
        SHOWNAME+='X Champion'
    #SELECCION DE METEOR
    def pilot4():
        global PLAYERSHOW, SHOWNAME
        print('Meteor Seleccionado')
        SHOWNAME=''
        PLAYERSHOW = Pilot4img
        SHOWNAME+='Meteor'
    #SELECCION DE MYSTERIO
    def pilot5():
        global PLAYERSHOW, SHOWNAME
        print('Mysterio seleccionado')
        SHOWNAME=''
        PLAYERSHOW = Pilot5img
        SHOWNAME+='Mysterio'
    #SELECCION DE ASTRID
    def pilot6():
        global PLAYERSHOW, SHOWNAME
        print('Astrid seleccionada')
        SHOWNAME=''
        PLAYERSHOW = Pilot6img
        SHOWNAME+='Astrid'
    #SELECCION DE PEACH
    def pilot7():
        global PLAYERSHOW, SHOWNAME
        print('Peach seleccionada')
        SHOWNAME=''
        PLAYERSHOW = Pilot7img
        SHOWNAME+='Peach'
    #SELECCION DE SHEEVA
    def pilot8():
        global PLAYERSHOW, SHOWNAME
        print('Sheeva seleccionada')
        SHOWNAME=''
        PLAYERSHOW = Pilot8img
        SHOWNAME+='Sheeva'
    #SELECCION DE RIPER
    def pilot9():
        global PLAYERSHOW, SHOWNAME
        print('Riper seleccionado')
        SHOWNAME=''
        PLAYERSHOW = Pilot9img
        SHOWNAME+='Riper'
    #SELECCION DE ASHOKA
    def pilot10():
        global PLAYERSHOW, SHOWNAME
        print('Ashoka seleccionada')
        SHOWNAME=''
        PLAYERSHOW = Pilot10img
        SHOWNAME+='Ashoka'
        
    #BOTONES DE CADA PILOTO A ELIGIR
    PilotEdu = Button(C_config, command=edu, image=Eduardo)
    PilotEdu.place(x=100, y=85)
    PilotMax = Button(C_config, command=maX, image=Max)
    PilotMax.place(x=300, y=85)
    Pilot1 = Button(C_config, command=pilot1, image=Pilot1img)
    Pilot1.place(x=500, y=85)
    Pilot2 = Button(C_config, command=pilot2, image=Pilot2img)
    Pilot2.place(x=100, y=285)
    Pilot3 = Button(C_config, command=pilot3, image=Pilot3img)
    Pilot3.place(x=300, y=285)
    Pilot4 = Button(C_config, command=pilot4, image=Pilot4img)
    Pilot4.place(x=500, y=285)

    #NOMBRES DE LOS PILOTOS A ELEGIR
    NameEdu = Label(C_config, width=10, text='Eduardo', font=('Helvatica',15), fg='gold', bg='darkslategrey')
    NameEdu.place(x=100, y=200)
    NameMax = Label(C_config, width=10, text='Max', font=('Helvatica',15), fg='gold', bg='darkslategrey')
    NameMax.place(x=300, y=200)
    NameReyes = Label(C_config, width=10, text='Reyes', font=('Helvatica',15), fg='gold', bg='darkslategrey')
    NameReyes.place(x=500, y=200)
    NameJill = Label(C_config, width=10, text='Jill', font=('Helvatica',15), fg='gold', bg='darkslategrey')
    NameJill.place(x=100, y=400)
    NameX = Label(C_config, width=10, text='X Champion', font=('Helvatica',15), fg='gold', bg='darkslategrey')
    NameX.place(x=300, y=400)
    NameMeteor = Label(C_config, width=10, text='Meteor', font=('Helvatica',15), fg='gold', bg='darkslategrey')
    NameMeteor.place(x=500, y=400)

    NEXT=True

    #//////////////////////////////////////////// CAMBIAR CONJUNTO DE PILOTOS ////////////////////////////////////////////////

    #CAMBIAR A LA SEGUNDA PAGINA DE PILOTOS
    def next_page():
        nonlocal NEXT,ImgFondo
        if NEXT==True:
            Set2 = Canvas(Config, width=700, height=500, bg='white')
            Set2.place(x=0, y=0)

            Select = Label(Set2, text='Selecciona un piloto', font=('Georgia',20), fg='lemonchiffon', bg='maroon')
            Select.place(x=240, y=30)
            
            Pilot5 = Button(Set2, command=pilot5, image=Pilot5img)
            Pilot5.place(x=100, y=85)
            Pilot6 = Button(Set2, command=pilot6, image=Pilot6img)
            Pilot6.place(x=300, y=85)
            Pilot7 = Button(Set2, command=pilot7, image=Pilot7img)
            Pilot7.place(x=500, y=85)
            Pilot8 = Button(Set2, command=pilot8, image=Pilot8img)
            Pilot8.place(x=100, y=285)
            Pilot9 = Button(Set2, command=pilot9, image=Pilot9img)
            Pilot9.place(x=300, y=285)
            Pilot10 = Button(Set2, command=pilot10, image=Pilot10img)
            Pilot10.place(x=500, y=285)

            NameMysterio = Label(Set2, width=10, text='Mysterio', font=('Helvatica',15), fg='gold', bg='darkslategrey')
            NameMysterio.place(x=100, y=200)
            NameAstrid = Label(Set2, width=10, text='Astrid', font=('Helvatica',15), fg='gold', bg='darkslategrey')
            NameAstrid.place(x=300, y=200)
            NamePeach = Label(Set2, width=10, text='Peach', font=('Helvatica',15), fg='gold', bg='darkslategrey')
            NamePeach.place(x=500, y=200)
            NameSheeva = Label(Set2, width=10, text='Sheeva', font=('Helvatica',15), fg='gold', bg='darkslategrey')
            NameSheeva.place(x=100, y=400)
            NameRiper = Label(Set2, width=10, text='Riper', font=('Helvatica',15), fg='gold', bg='darkslategrey')
            NameRiper.place(x=300, y=400)
            NameAshoka = Label(Set2, width=10, text='Ashoka', font=('Helvatica',15), fg='gold', bg='darkslategrey')
            NameAshoka.place(x=500, y=400)

            Fondo = Set2.create_image(350,250,image=ImgFondo)

            PrevPilot = Button(Set2, width=15, text='Anterior', font=('Helvatica',15), command=back_page, fg='gold', bg='darkred')
            PrevPilot.place(x=80, y=450)
            
            NextPilot = Button(Set2, width=15, text='Siguiente', font=('Helvatica',15), command=next_page, fg='gold', bg='darkred')
            NextPilot.place(x=470, y=450)

            quit_config = Button(Config,text = 'Volver al inicio',command=back_config)
            quit_config.place(x=0,y=0)

            NEXT=False

    #RETORNO A LA PRIMERA PAGINA DE PILOTOS
    def back_page():
        nonlocal NEXT,ImgFondo
        if NEXT==False:
            Set1 = Canvas(Config, width=700, height=500, bg='white')
            Set1.place(x=0, y=0)

            Select = Label(Set1, text='Selecciona un piloto', font=('Georgia',20), fg='lemonchiffon', bg='maroon')
            Select.place(x=240, y=30)
            
            PilotEdu = Button(Set1, command=edu, image=Eduardo)
            PilotEdu.place(x=100, y=85)
            PilotMax = Button(Set1, command=maX, image=Max)
            PilotMax.place(x=300, y=85)
            Pilot1 = Button(Set1, command=pilot1, image=Pilot1img)
            Pilot1.place(x=500, y=85)
            Pilot2 = Button(Set1, command=pilot2, image=Pilot2img)
            Pilot2.place(x=100, y=285)
            Pilot3 = Button(Set1, command=pilot3, image=Pilot3img)
            Pilot3.place(x=300, y=285)
            Pilot4 = Button(Set1, command=pilot4, image=Pilot4img)
            Pilot4.place(x=500, y=285)

            NameEdu = Label(Set1, width=10, text='Eduardo', font=('Helvatica',15), fg='gold', bg='darkslategrey')
            NameEdu.place(x=100, y=200)
            NameMax = Label(Set1, width=10, text='Max', font=('Helvatica',15), fg='gold', bg='darkslategrey')
            NameMax.place(x=300, y=200)
            NameReyes = Label(Set1, width=10, text='Reyes', font=('Helvatica',15), fg='gold', bg='darkslategrey')
            NameReyes.place(x=500, y=200)
            NameJill = Label(Set1, width=10, text='Jill', font=('Helvatica',15), fg='gold', bg='darkslategrey')
            NameJill.place(x=100, y=400)
            NameX = Label(Set1, width=10, text='X Champion', font=('Helvatica',15), fg='gold', bg='darkslategrey')
            NameX.place(x=300, y=400)
            NameMeteor = Label(Set1, width=10, text='Meteor', font=('Helvatica',15), fg='gold', bg='darkslategrey')
            NameMeteor.place(x=500, y=400)

            Fondo = Set1.create_image(350,250,image=ImgFondo)

            PrevPilot = Button(Set1, width=15, text='Anterior', font=('Helvatica',15), command=back_page, fg='gold', bg='darkred')
            PrevPilot.place(x=80, y=450)

            NextPilot = Button(Set1, width=15, text='Siguiente', font=('Helvatica',15), command=next_page, fg='gold', bg='darkred')
            NextPilot.place(x=470, y=450)

            quit_config = Button(Config,text = 'Volver al inicio',command=back_config)
            quit_config.place(x=0,y=0)

            NEXT=True

    #RETORNO AL MENU PRINCIPAL
    def back_config():       
        Config.destroy()
        Menu.deiconify()
        
    quit_config = Button(Config,text = 'Volver al inicio',command=back_config)
    quit_config.place(x=0,y=0)

    PrevPilot = Button(C_config, width=15, text='Anterior', font=('Helvatica',15), command=back_page, fg='gold', bg='darkred')
    PrevPilot.place(x=80, y=450)

    NextPilot = Button(C_config, width=15, text='Siguiente', font=('Helvatica',15), command=next_page, fg='gold', bg='darkred')
    NextPilot.place(x=470, y=450)


    Menu.withdraw()

    Config.mainloop()

#/////////////////////////////////// PANTALLA DE PUNTAJES ////////////////////////////////////////////////////////////////////////

#VENTANA DE MEJORES PUNTAJES DE DESTRUCCION DE ASTEROIDES
def scores_ast():
    Scores = Toplevel()
    Scores.minsize(700,500)
    Scores.resizable(False, False)
    Scores.title('Galaxy Heroes')
    Scores.iconbitmap('Imagenes/Icono.ico')
    
    C_scores = Canvas(Scores,width=700,height=500,bg='white')
    C_scores.place(x=0,y=0)

    C_scores.image1 = Imagenes('Imagenes/Background/playbg.png')
    imgCanvas_Scores = C_scores.create_image(350,250,image= C_scores.image1)


    ScoOrder = [str(random.randint(0,300))+': EDUARDO', str(random.randint(0,300))+': MAX', str(random.randint(0,300))+': REYES', str(random.randint(0,300))+': JILL', str(random.randint(0,300))+': X CHAMPION', str(random.randint(0,300))+': METEOR', str(random.randint(0,300))+': MYSTERIO', str(random.randint(0,300))+': ASTRID', str(random.randint(0,300))+': PEACH', str(random.randint(0,300))+': SHEEVA', str(random.randint(0,300))+': RIPER', str(random.randint(0,300))+': ASHOKA']  

    def order(Lista):
        return order_aux(Lista,1,len(Lista))

    def order_aux(Lista,i,n):
        if i==n:
            return Lista
        Aux=Lista[i]
        j=incluye_orden(Lista,i,Aux)
        Lista[j]=Aux
        return order_aux(Lista,i+1,n)

    def incluye_orden(Lista,j,Aux):
        if j<=0 or Lista[j-1]<=Aux:
            return j
        Lista[j]=Lista[j-1]
        return incluye_orden(Lista,j-1,Aux)

    PuntOrdenados = order(ScoOrder)
    
    Pos1 = Label(Scores, text=PuntOrdenados[0], fg='black', bg='white')
    Pos1.place(x=50, y=50)

    Pos2 = Label(Scores, text=PuntOrdenados[1], fg='black', bg='white')
    Pos2.place(x=50, y=100)

    Pos3 = Label(Scores, text=PuntOrdenados[2], fg='black', bg='white')
    Pos3.place(x=50,y=150)

    Pos4 = Label(Scores, text=PuntOrdenados[3], fg='black', bg='white')
    Pos4.place(x=50, y=200)

    Pos5 = Label(Scores, text=PuntOrdenados[4], fg='black', bg='white')
    Pos5.place(x=50, y=250)
    
    Pos6 = Label(Scores, text=PuntOrdenados[5], fg='black', bg='white')
    Pos6.place(x=50, y=300)

    Pos7 = Label(Scores, text=PuntOrdenados[6], fg='black', bg='white')
    Pos7.place(x=50, y=350)
    
    def back_scores():       #<== VOLVER AL MENU PRINCIPAL
        Scores.destroy()
        Menu.deiconify()        
    quit_scores = Button(Scores,text = 'Volver al inicio',command=back_scores)
    quit_scores.place(x=0,y=0)
    Menu.withdraw()


    Scores.mainloop()

def scores_ring():
    Scores = Toplevel()
    Scores.minsize(700,500)
    Scores.resizable(False, False)
    Scores.title('Galaxy Heroes')
    Scores.iconbitmap('Imagenes/Icono.ico')
    
    C_scores = Canvas(Scores,width=700,height=500,bg='white')
    C_scores.place(x=0,y=0)

    C_scores.image1 = Imagenes('Imagenes/Background/playbg.png')
    imgCanvas_Scores = C_scores.create_image(350,250,image= C_scores.image1)    

    
    def back_scores():       #<== VOLVER AL MENU PRINCIPAL
        Scores.destroy()
        Menu.deiconify()        
    quit_scores = Button(Scores,text = 'Volver al inicio',command=back_scores)
    quit_scores.place(x=0,y=0)
    Menu.withdraw()


    Scores.mainloop()

#//////////////////////////////////// PANTALLA DE INFORMACION /////////////////////////////////////////////////////////////////////

def about():
    info = Toplevel()
    info.minsize(700,500)
    info.resizable(False, False)
    info.title('Galaxy Heroes')
    info.iconbitmap('Imagenes/Icono.ico')
    
    C_info = Canvas(info,width=700,height=500,bg='white')
    C_info.place(x=0,y=0)

    C_info.image1 = Imagenes('Imagenes/Background/playbg.png')
    imgCanvas_info = C_info.create_image(350,250,image= C_info.image1)    

    Label1 = Label(C_info,text = "Instituto Tecnológico de Costa Rica", font =('Times New Roman',12))
    Label1.place(x=50,y=50)

    Label2 = Label(C_info,text = "Ingeniería en Computadores", font =('Times New Roman',12))
    Label2.place(x=50,y=100)

    Label3 = Label(C_info,text = "Profesor: Milton Villegas Lemus", font =('Times New Roman',12))
    Label3.place(x=50,y=150)

    Label4 = Label(C_info,text = "Autores", font =('Times New Roman',12))
    Label4.place(x=400,y=25)

    Label5 = Label(C_info,text = "Max Garro Mora", font =('Times New Roman',12))
    Label5.place(x=300,y=150)

    Label6 = Label(C_info,text = "Eduardo Bolívar Minguet", font =('Times New Roman',12))
    Label6.place(x=425,y=150)

    maxgm = Imagenes('Imagenes/FOTO.png')
    maxgm_image = C_info.create_image(350, 100, image=maxgm)

    eduardobm = Imagenes('Imagenes/FOTO2.png')
    eduardobm_image = C_info.create_image(500, 100, image=eduardobm)

    def back_about():       #<== VOLVER AL MENU PRINCIPAL
        info.destroy()
        Menu.deiconify()        
    quit_info = Button(info,text = 'Volver al inicio',command=back_about)
    quit_info.place(x=0,y=0)
    Menu.withdraw()

    info.mainloop()

def salida():       #<== CERRAR DEL JUEGO
    musica(1)
    Menu.destroy()

#//////////////////////////////////////////////////////Ventana selección dificultad////////////////////////////////////////////////////////
def dificultad(m):
    dif = Toplevel()
    dif.minsize(500,400)
    dif.resizable(False, False)
    dif.title('Galaxy Heroes')
    dif.iconbitmap('Imagenes/Icono.ico')
    
    
    C_dif = Canvas(dif,width=500,height=400,bg='white')
    C_dif.place(x=0,y=0)

    C_dif.image1 = Imagenes('Imagenes/Background/playbg.png')
    imgCanvas_dif = C_dif.create_image(350,250,image= C_dif.image1)
    
    if m==1:
        def easy():
            global DIFF
            DIFF=1
            Dificulty.configure(text='Facil elegido')
            dif.destroy()
            return juego(1)

        def normal():
            global DIFF
            DIFF=2
            Dificulty.configure(text='Normal elegido')
            dif.destroy()
            return juego(1)

        def hard():
            global DIFF
            DIFF=3
            Dificulty.configure(text='Dificil elegido')
            return juego(1)
    if m==2:
        def easy():
            global DIFF
            DIFF=1
            Dificulty.configure(text='Facil elegido')
            dif.destroy()
            return juego(2)

        def normal():
            global DIFF
            DIFF=2
            Dificulty.configure(text='Normal elegido')
            dif.destroy()
            juego(2)

        def hard():
            global DIFF
            DIFF=3
            Dificulty.configure(text='Dificil elegido')
            dif.destroy()
            return juego(2)
        
    Facil = Button(C_dif, width=10, text='Facil', command=easy, font=('Times',15), fg='gold', bg='midnightblue')
    Facil.place(x=250, y=100)

    Medio = Button(C_dif, width=10, text='Medio', command=normal, font=('Times',15), fg='gold', bg='midnightblue')
    Medio.place(x=250, y=150)

    Dificil = Button(C_dif, width=10, text='Dificil', command=hard, font=('Times',15), fg='gold', bg='midnightblue')
    Dificil.place(x=250, y=200)
    
    Dificulty = Label(C_dif, width=15, text='Dificultad', font=('Times',15), fg='cyan', bg='darkslategray')
    Dificulty.place(x=250, y=50)
    
    def back_dificultad():       #<== VOLVER AL MENU PRINCIPAL
        dif.destroy()
        Menu.deiconify()
    quit_dif = Button(dif,text = 'Volver al inicio',command=back_dificultad)
    quit_dif.place(x=0,y=0)
    Menu.withdraw()
        
    dif.mainloop()
        
def salida():       #<== CERRAR DEL JUEGO
    musica(1)
    Menu.destroy()


ModoJuego1 = Button(Fondo, width=27, text='Destrucción de asteroides', command=select_juego1, font=('Times',15), fg='gold', bg='firebrick')     #BOTONES DE MENU
ModoJuego1.place(x=180, y=300)

ModoJuego2 = Button(Fondo, width=27, text='Maniobras de prueba', command=select_juego2, font=('Times',15), fg='gold', bg='firebrick')
ModoJuego2.place(x=690, y=300)

Confi = Button(Fondo, width=17, text='Configuración', command=config, font=('Times',15), fg='gold', bg='firebrick')
Confi.place(x=490, y=400)

Puntajes1 = Button(Fondo, text='Puntajes Destruccion de Asteroides', command=scores_ast, font=('Times',15), fg='gold', bg='firebrick')
Puntajes1.place(x=440, y=450)

Puntajes2 = Button(Fondo, text='Puntajes Maniobra de Pruebas', command=scores_ring, font=('Times',15), fg='gold', bg='firebrick')
Puntajes2.place(x=460, y=500)

About = Button(Fondo, width=17, text='Acerca de', command=about, font=('Times',15), fg='gold', bg='firebrick')
About.place(x=490, y=550)

Cerrar = Button(Fondo, width=17, text='Salir del juego', command=salida, font=('Times',15), fg='gold', bg='firebrick')
Cerrar.place(x=490, y=600)


Menu.mainloop()

quit()
