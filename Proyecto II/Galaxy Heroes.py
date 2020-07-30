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
UP=False
DOWN=False
RIGHT=False
LEFT=False

#////////////////// CARGAR IMAGENES Y MULTIMEDIA ////////////////////////////////////////////

def Imagenes(Ubicacion):
    Ruta = os.path.join(Ubicacion)
    Img = PhotoImage(file=Ruta)
    return Img

def musica(archivo):
    if isinstance(archivo,str):
        pg.mixer.init()
        pg.mixer.music.load(archivo)
        pg.mixer.music.play(10)
    else:
        pg.mixer.quit()

def ImagenesAnim(x, Result):
    if x==[]:
        return Result
    else:
        Result.append(PhotoImage(file=x[0]))
        return ImagenesAnim(x[1:],Result)

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

musica('Audio\\MainTheme.mp3')

Fondo = Canvas(Menu, width=1200, height=650, bg='black')
Fondo.place(x=0, y=0)

MainTitle = Label(Menu, width=15, text='GALAXY HEROES', font=('Georgia',40), fg='lemonchiffon', bg='maroon')
MainTitle.place(x=350, y=80)

FondoImg = Imagenes('Imagenes\\Background\\FondoMenu.png')
Space = Fondo.create_image(0, 325, tags=('FONDO'), image=FondoImg)

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

def juego(Mode):
    Pant = Toplevel()
    Pant.minsize(1200,650)
    Pant.resizable(False, False)
    Pant.title('Galaxy Heroes')
    Pant.iconbitmap('Imagenes/Icono.ico')

    Menu.withdraw()
    musica(1)

    Bg = Canvas(Pant, width=1200, height=650, bg='maroon')
    Bg.place(x=0,y=0)

    Display = Canvas(Pant, width=1200, height=90, bg='dimgray')
    Display.place(x=0, y=0)

    global SHOWNAME

    Name = Label(Display, width=10, text=SHOWNAME, font=('Georgia',15), fg='lemonchiffon', bg='maroon')
    Name.place(x=700, y=50)

    def show_player():
        global PLAYERSHOW
        Display.create_image(900, 50, image=PLAYERSHOW)

    def back():         #<== RETORNO
        global OPEN, BATTERY, PLAYERSHOW, SHOWNAME
        OPEN=False
        BATTERY=100
        PLAYERSHOW=[]
        SHOWNAME=''
        Pant.destroy()
        musica('Audio\\MainTheme.mp3')
        Menu.deiconify()   

    #//////////////////////////////////////////Función para el temporizador, puntos y baterias///////////////////////////////////////////        
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

    def points(p):
        global POINTS
        POINTS+=p
        Cont = Label(Display, width=10, text='Puntos:'+str(POINTS), font=('Georgia',15), fg='lemonchiffon', bg='darkslategrey')
        Cont.place(x=350, y=50)
    
    Fullbattery = sprites('Imagenes/Spaceship/Combustible/Fullbattery*.png')
    
    def generate_battery(t):
        global OPEN
        if OPEN == True:
            try:
                if t == 25:
                    Bg.BatteryFull = Bg.create_image(random.uniform(100,1100),random.uniform(100,500),tags=('battery'))
                    move_fullbattery(0)
                    return generate_battery(0)
                else:
                    time.sleep(1)
                    return generate_battery(t+1)
            except:
                return
    
    def move_fullbattery(i):                #<== MOVER SOBRECARGA DE BATERÍA
        Coord = Bg.coords('battery')
        if Coord!=[]:
            if i==6:
                return Bg.delete('battery')
            else:
                Bg.itemconfig('battery', image=Fullbattery[i])
                time.sleep(1)
                return move_fullbattery(i+1)
        else:
            return None

    Thread(target=generate_battery, args=(0,)).start()
    
        
    Exit = Button(Display, text='Abandonar', font=('Helvatica'), command=back, fg='lemonchiffon', bg='darkslategrey')
    Exit.place(x=10, y=20)

    #///////////////////////////////////// CARGAR IMAGENES MISCELANEAS ////////////////////////////////////////////////////

    fondojuego = Imagenes('Imagenes\\Background\\GameBG.png') #<== Imagen del fondo de la pantalla de juego
    BgFondo = Bg.create_image(600, 325, image=fondojuego)
    
    Spaceship = Bg.create_image(600, 325, tags=('MYSHIP'))

    SpaceshipImg = sprites('Imagenes/Spaceship/playership*.png') #<== Sprites de la nave del jugador cuando va por el centro de la pantalla

    ShotCent = sprites('Imagenes\\Spaceship\\shotcenter*.png')

    BatteryFull = Imagenes('Imagenes\\Spaceship\\Combustible\\Battery1.png')
    BatteryMedium = Imagenes('Imagenes\\Spaceship\\Combustible\\Battery2.png')
    BatteryMedium1 = Imagenes('Imagenes\\Spaceship\\Combustible\\Battery3.png')
    BatteryEmpty = Imagenes('Imagenes\\Spaceship\\Combustible\\Battery4.png')
    BatteryDead = Imagenes('Imagenes\\Spaceship\\Combustible\\Battery5.png')

    #///////////////////////////////////// MODOS DE JUEGO //////////////////////////////////////////////////////////////
    #MODO DESTRUCCION DE ASTEROIDES
    if Mode==1:
        SpritesAst=sprites('Imagenes/Asteroides/ast*.png')

        def generate_ast(t):        #<== GENERAR ASTEROIDE
            global OPEN
            if OPEN==True:
                try:
                    if t==2:
                        Bg.Asteroid = Bg.create_image(random.uniform(100,1100), random.uniform(100,500), tags=('ast'))
                        ast_3D(0)
                        return generate_ast(0)
                    else:
                        time.sleep(1)
                        t+=1
                        return generate_ast(t)
                except:
                    return None
    
        def ast_3D(i):              #<== MOVER ASTEROIDE
            if i==10:
                return Bg.delete('ast')
            else:
                Bg.itemconfig('ast', image=SpritesAst[i])
                i+=1
            def call():
                ast_3D(i)
            Pant.after(150,call)

        Thread(target=generate_ast, args=(0,)).start()

    #MODO MANIOBRA DE PRUEBAS
    if Mode==2:
        Anillos=sprites('Imagenes/Anillos/Ring*.png')

        def generate_ring(t):       #<== GENERAR ANILLO
            global OPEN
            if OPEN==True:
                try:
                    if t==3:
                        Anillo = Bg.create_image(random.uniform(100,1100),random.uniform(100,550), tags=('RING'))
                        ring_3D(0)
                        return generate_ring(0)
                    else:
                        time.sleep(0.5)
                        return generate_ring(t+1)
                except:
                    return None
                    
        def ring_3D(i):             #<== MOVER ANILLO
            if i==5:
                return Bg.delete('RING')
            else:
                Bg.itemconfig('RING',image=Anillos[i])
                time.sleep(0.3)
                return ring_3D(i+1)

        Thread(target=generate_ring, args=(0,)).start()

    #/////////////////////////////////// FUNCIONES DE MOVIMIENTO DE LA NAVE ////////////////////////////////////////////////

    def anim(i):        #<== ANIMACION DE NAVE
        global OPEN
        if i==2:
            i=0
        if OPEN==True:
            Bg.itemconfig('MYSHIP', image=SpaceshipImg[i])
            time.sleep(0.15)
            Thread(target=anim, args=(i+1,)).start()

    def arriba():      #<== MOVER HACIA ARRIBA
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

    def abajo():       #<== MOVER HACIA ABAJO
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

    def derecha():     #<== MOVER A LA DERECHA
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

    def izquierda():   #<== MOVER A LA IZQUIERDA
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
        
    def shooting(event):
        global SHOT
        if SHOT==True:
            Loc = Bg.coords('MYSHIP')
            pg.mixer.init()
            Disp = pg.mixer.Sound('Audio\\disparo.wav')
            Disp.play()
            Bg.create_image(Loc[0], Loc[1]-50, tags=('shot1'))
            SHOT=False
            return mov_shot(0)
    def mov_shot(i):
        global SHOT
        Blast = Bg.coords('shot1')
        if Blast!=[]:
            if i==20:
                SHOT=True
                return Bg.delete('shot1')
            else:
                Bg.coords('shot1', Blast[0], Blast[1]-3)
                Bg.itemconfig('shot1', image=ShotCent[i])
                i+=1
        def call():
            mov_shot(i)
        Pant.after(15,call)
            
    #/////////////////////////////////////////// BATERIA /////////////////////////////////////////////////////////////////////
    
    Battery = Display.create_image(600, 50, tags=('battery'), image=BatteryFull)
    
    def empty_battery():
        global BATTERY, OPEN
        if BATTERY==0:
            Display.itemconfig('battery',image=BatteryDead)
            return
        elif 75<BATTERY<=100:
            BATTERY-=1
            return Display.after(1000,empty_battery)
        elif 50<BATTERY<=75:
            Display.itemconfig('battery',image=BatteryMedium)
            BATTERY-=1
            return Display.after(1000,empty_battery)
        elif 25<BATTERY<=50:
            Display.itemconfig('battery',image=BatteryMedium1)
            BATTERY-=1
            return Display.after(1000,empty_battery)
        elif 0<BATTERY<=25:
            Display.itemconfig('battery',image=BatteryEmpty)
            BATTERY-=1
            return Display.after(1000,empty_battery)
        

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
    Pant.bind('<space>',shooting)

    Pant.mainloop()

#//////////////////////////////////// SELECCION DE MODO DE JUEGO ///////////////////////////////////////////////////////////////

def select_juego1():
    global OPEN, PLAYERSHOW
    if PLAYERSHOW==[]:
        return print('ELIJA UN PILOTO EN CONFIGURACION')
    else:
        OPEN=True
        return juego(1)

def select_juego2():
    global OPEN, PLAYERSHOW
    if PLAYERSHOW==[]:
        return print('ELIJA UN PILOTO EN CONFIGURACION')
    else:
        OPEN=True
        return juego(2)

#/////////////////////////////////// PANTALLA DE CONFIGURACION ////////////////////////////////////////////////////////////////

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
    Eduardo = Imagenes('Imagenes/Pilotos/Eduardo.png')
    Max = Imagenes('Imagenes/Pilotos/Max.png')
    Pilot1img = Imagenes('Imagenes/Pilotos/Piloto1.png')
    Pilot2img = Imagenes('Imagenes/Pilotos/Piloto2.png')
    Pilot3img = Imagenes('Imagenes/Pilotos/Piloto3.png')
    Pilot4img = Imagenes('Imagenes/Pilotos/Piloto4.png')
    Pilot5img = Imagenes('Imagenes/Pilotos/Piloto5.png')
    Pilot6img = Imagenes('Imagenes/Pilotos/Piloto6.png')
    Pilot7img = Imagenes('Imagenes/Pilotos/Piloto7.png')
    Pilot8img = Imagenes('Imagenes/Pilotos/Piloto8.png')
    Pilot9img = Imagenes('Imagenes/Pilotos/Piloto9.png')
    Pilot10img = Imagenes('Imagenes/Pilotos/Piloto10.png')

    Select = Label(C_config, text='Selecciona un piloto', font=('Georgia',20), fg='lemonchiffon', bg='maroon')
    Select.place(x=240, y=30)

    #////////////////////////////////////////// SELECCIONAR PILOTOS //////////////////////////////////////////////////////
    def edu():
        global PLAYERSHOW, SHOWNAME
        print('Eduardo Seleccionado')
        PLAYERSHOW = Eduardo
        SHOWNAME+='Eduardo'
    def maX():
        global PLAYERSHOW, SHOWNAME
        print('Max Seleccionado')
        PLAYERSHOW = Max
        SHOWNAME+='Max'
    def pilot1():
        global PLAYERSHOW, SHOWNAME
        print('Reyes Seleccionado')
        PLAYERSHOW = Pilot1img
        SHOWNAME+='Reyes'
    def pilot2():
        global PLAYERSHOW, SHOWNAME
        print('Jill Seleccionado')
        PLAYERSHOW = Pilot2img
        SHOWNAME+='Jill'
    def pilot3():
        global PLAYERSHOW, SHOWNAME
        print('X Champion Seleccionado')
        PLAYERSHOW = Pilot3img
        SHOWNAME+='X Champion'
    def pilot4():
        global PLAYERSHOW, SHOWNAME
        print('Meteor Seleccionado')
        PLAYERSHOW = Pilot4img
        SHOWNAME+='Meteor'
    def pilot5():
        global PLAYERSHOW, SHOWNAME
        print('Mysterio seleccionado')
        PLAYERSHOW = Pilot5img
        SHOWNAME+='Mysterio'
    def pilot6():
        global PLAYERSHOW, SHOWNAME
        print('Astrid seleccionada')
        PLAYERSHOW = Pilot6img
        SHOWNAME+='Astrid'
    def pilot7():
        global PLAYERSHOW, SHOWNAME
        print('Peach seleccionada')
        PLAYERSHOW = Pilot7img
        SHOWNAME+='Peach'
    def pilot8():
        global PLAYERSHOW, SHOWNAME
        print('Sheeva seleccionada')
        PLAYERSHOW = Pilot8img
        SHOWNAME+='Sheeva'
    def pilot9():
        global PLAYERSHOW, SHOWNAME
        print('Riper seleccionado')
        PLAYERSHOW = Pilot9img
        SHOWNAME+='Riper'
    def pilot10():
        global PLAYERSHOW, SHOWNAME
        print('Ashoka seleccionada')
        PLAYERSHOW = Pilot10img
        SHOWNAME+='Ashoka'
        
    
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
            
    def back_config():       #<== VOLVER AL MENU PRINCIPAL
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

def scores():
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

ModoJuego1 = Button(Fondo, width=27, text='Destrucción de asteroides', command=select_juego1, font=('Times',15), fg='gold', bg='firebrick')     #BOTONES DE MENU
ModoJuego1.place(x=180, y=300)

ModoJuego2 = Button(Fondo, width=27, text='Maniobras de prueba', command=select_juego2, font=('Times',15), fg='gold', bg='firebrick')
ModoJuego2.place(x=690, y=300)

Confi = Button(Fondo, width=17, text='Configuración', command=config, font=('Times',15), fg='gold', bg='firebrick')
Confi.place(x=490, y=400)

Puntajes = Button(Fondo, width=17, text='Altos puntajes', command=scores, font=('Times',15), fg='gold', bg='firebrick')
Puntajes.place(x=490, y=450)

About = Button(Fondo, width=17, text='Acerca de', command=about, font=('Times',15), fg='gold', bg='firebrick')
About.place(x=490, y=500)

Cerrar = Button(Fondo, width=17, text='Salir del juego', command=salida, font=('Times',15), fg='gold', bg='firebrick')
Cerrar.place(x=490, y=550)

Menu.mainloop()

quit()
