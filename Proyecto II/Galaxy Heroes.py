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
BATTERY=100

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

    Display = Canvas(Pant, width=1200, height=60, bg='silver')
    Display.place(x=0, y=0)

    def back():         #<== RETORNO
        global OPEN, BATTERY
        OPEN=False
        BATTERY=100
        Pant.destroy()
        musica('Audio\\MainTheme.mp3')
        Menu.deiconify()   

    #//////////////////////////////////////////Función para el temporizador///////////////////////////////////////////        
    def tiempo(Seg):
        global OPEN
        if OPEN == True:
            try:
                time.sleep(1)
                time_label = Label(Pant, text='Tiempo:'+ str(Seg), font=('Georgia',20), fg='gold', bg='darkslategray')
                time_label.place(x=650,y=20)
                Thread(target=tiempo,args=(Seg+1,)).start()
            except:
                return
            
    Thread(target = tiempo, args = (0,)).start()
    
    SpriteBattery = sprites('Imagenes/Spaceship/Fullbattery*.png')
    
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
    
    def move_fullbattery(i):              #<== MOVER SOBRECARGA DE BATERÍA
            if i==12:
                return Bg.delete('battery')
            else:
                Bg.itemconfig('battery', image=Fullbattery[i])
                time.sleep(1)
                return move_fullbattery(i+1)

    Thread(target=move_fullbattery, args=(0,)).start()
    
        
    Exit = Button(Display, text='Abandonar', font=('Helvatica'), command=back, fg='gold', bg='darkslategray')
    Exit.place(x=10, y=20)

    #///////////////////////////////////// MODOS DE JUEGO //////////////////////////////////////////////////////////////
    #MODO DESTRUCCION DE ASTEROIDES
    if Mode==1:
        SpritesAst=sprites('Imagenes/Asteroides/ast*.png')

        def generate_ast(t):        #<== GENERAR ASTEROIDE
            global OPEN
            if OPEN==True:
                try:
                    if t==5:
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
            if i==12:
                return Bg.delete('ast')
            else:
                Bg.itemconfig('ast', image=SpritesAst[i])
                time.sleep(0.3)
                return ast_3D(i+1)

        Thread(target=generate_ast, args=(0,)).start()

    #MODO MANIOBRA DE PRUEBAS
    if Mode==2:
        Anillos=sprites('Imagenes/Anillos/Ring*.png')

        def generate_ring(t):       #<== GENERAR ANILLO
            global OPEN
            if OPEN==True:
                if t==3:
                    Anillo = Bg.create_image(random.uniform(100,1100),random.uniform(100,550), tags=('RING'))
                    ring_3D(0)
                    return generate_ring(0)
                else:
                    time.sleep(0.5)
                    return generate_ring(t+1)
                    
        def ring_3D(i):             #<== MOVER ANILLO
            if i==5:
                return Bg.delete('RING')
            else:
                Bg.itemconfig('RING',image=Anillos[i])
                time.sleep(0.3)
                return ring_3D(i+1)

        Thread(target=generate_ring, args=(0,)).start()

    #///////////////////////////////////// CARGAR IMAGENES MISCELANEAS ////////////////////////////////////////////////////

    fondojuego = Imagenes('Imagenes\\Background\\GameBG.png') #<== Imagen del fondo de la pantalla de juego
    BgFondo = Bg.create_image(600, 325, image=fondojuego)
    
    Bg.Spaceship0 = Bg.create_image(600, 325, tags=('MYSHIP'))

    Bg.Spaceship = sprites('Imagenes/Spaceship/playership*.png') #<== Sprites de la nave del jugador cuando va por el centro de la pantalla
    Bg.Right = sprites('Imagenes/Spaceship/right*.png') #<== Sprites de la nave del jugador cuando va por el lado derecho de la pantalla
    Bg.Left = sprites('Imagenes/Spaceship/left*.png') #<== Sprites de la nave del jugador cuando va por el lado izquierdo de la pantalla

    #/////////////////////////////////// FUNCIONES DE MOVIMIENTO DE LA NAVE ////////////////////////////////////////////////

    def anim(i):        #<== ANIMACION DE NAVE
        global OPEN
        if i==2:
            i=0
        if OPEN==True:
            loc = Bg.coords('MYSHIP')
            if 400<loc[0]<800:
                Bg.itemconfig('MYSHIP', image=Bg.Spaceship[i])
            if loc[0]<=400:
                Bg.itemconfig('MYSHIP', image=Bg.Right[i])
            if loc[0]>=800:
                Bg.itemconfig('MYSHIP', image=Bg.Left[i])
            time.sleep(0.15)
            Thread(target=anim, args=(i+1,)).start()

    def arriba(event):      #<== MOVER HACIA ARRIBA
        Ubi = Bg.coords('MYSHIP')
        if Ubi!=[]:
            Bg.coords('MYSHIP', Ubi[0], Ubi[1]-25)
            if (Ubi[1]-25)==125:
                Bg.coords('MYSHIP', Ubi[0], Ubi[1])

    def abajo(event):       #<== MOVER HACIA ABAJO
        Ubi = Bg.coords('MYSHIP')
        if Ubi!=[]:
            Bg.coords('MYSHIP', Ubi[0], Ubi[1]+25)
            if (Ubi[1]+25)==575:
                Bg.coords('MYSHIP', Ubi[0], Ubi[1])

    def derecha(event):     #<== MOVER A LA DERECHA
        Ubi = Bg.coords('MYSHIP')
        if Ubi!=[]:
            Bg.coords('MYSHIP', Ubi[0]+25, Ubi[1])
            if (Ubi[0]+25)==1100:
                Bg.coords('MYSHIP', Ubi[0], Ubi[1])

    def izquierda(event):   #<== MOVER A LA IZQUIERDA
        Ubi = Bg.coords('MYSHIP')
        if Ubi!=[]:
            Bg.coords('MYSHIP', Ubi[0]-25, Ubi[1])
            if (Ubi[0]-25)==100:
                Bg.coords('MYSHIP', Ubi[0], Ubi[1])

    #/////////////////////////////////////////// BATERIA /////////////////////////////////////////////////////////////////////

    BatteryFull = Imagenes('Imagenes\\Spaceship\\Battery1.png')
    BatteryMedium = Imagenes('Imagenes\\Spaceship\\Battery2.png')
    BatteryMedium1 = Imagenes('Imagenes\\Spaceship\\Battery3.png')
    BatteryEmpty = Imagenes('Imagenes\\Spaceship\\Battery4.png')
    BatteryDead = Imagenes('Imagenes\\Spaceship\\Battery5.png')
    
    Battery = Display.create_image(500, 30, tags=('battery'), image=BatteryFull)
    
    def empty_battery():
        global BATTERY
        if BATTERY==0:
            Display.itemconfig('battery',image=BatteryDead)
            return 'Game Over'
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

    empty_battery()
        

    #//////////////////////////////////////////// BINDS Y LLAMADAS ///////////////////////////////////////////////////////////

    anim(0)

    Pant.bind('<w>',arriba)
    Pant.bind('<s>',abajo)
    Pant.bind('<d>',derecha)
    Pant.bind('<a>',izquierda)        

    Pant.mainloop()

#//////////////////////////////////// SELECCION DE MODO DE JUEGO ///////////////////////////////////////////////////////////////

def select_juego1():
    global OPEN
    OPEN=True
    return juego(1)

def select_juego2():
    global OPEN
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

    C_config.image1 = Imagenes('Imagenes/Background/playbg.png')
    imgCanvas_config = C_config.create_image(350,250,image= C_config.image1)

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
    
    Pilot1 = C_config.create_image(180, 150, tags=('pilot1'), image=Pilot1img)
    Pilot2 = C_config.create_image(360, 150, tags=('pilot2'), image=Pilot2img)
    Pilot3 = C_config.create_image(540, 150, tags=('pilot3'), image=Pilot3img)
    Pilot4 = C_config.create_image(270, 310, tags=('pilot4'), image=Pilot4img)
    Pilot5 = C_config.create_image(450, 310, tags=('pilot5'), image=Pilot5img)

    NEXT=True

    def next_page():
        nonlocal NEXT
        if NEXT==True:
            C_config.delete('pilot1')
            C_config.delete('pilot2')
            C_config.delete('pilot3')
            C_config.delete('pilot4')
            C_config.delete('pilot5')
            Pilot6 = C_config.create_image(180, 150, tags=('pilot6'), image=Pilot6img)
            Pilot7 = C_config.create_image(360, 150, tags=('pilot7'), image=Pilot7img)
            Pilot8 = C_config.create_image(540, 150, tags=('pilot8'), image=Pilot8img)
            Pilot9 = C_config.create_image(270, 310, tags=('pilot9'), image=Pilot9img)
            Pilot10 = C_config.create_image(450, 310, tags=('pilot10'), image=Pilot10img)         
            NEXT=False
    
    def back_page():
        nonlocal NEXT
        if NEXT==False:
            C_config.delete('pilot6')
            C_config.delete('pilot7')
            C_config.delete('pilot8')
            C_config.delete('pilot9')
            C_config.delete('pilot10')
            Pilot1 = C_config.create_image(180, 150, tags=('pilot1'), image=Pilot1img)
            Pilot2 = C_config.create_image(360, 150, tags=('pilot2'), image=Pilot2img)
            Pilot3 = C_config.create_image(540, 150, tags=('pilot3'), image=Pilot3img)
            Pilot4 = C_config.create_image(270, 310, tags=('pilot4'), image=Pilot4img)
            Pilot5 = C_config.create_image(450, 310, tags=('pilot5'), image=Pilot5img)
            NEXT=True
            
    def back_config():       #<== VOLVER AL MENU PRINCIPAL
        Config.destroy()
        Menu.deiconify()
        
    quit_config = Button(Config,text = 'Volver al inicio',command=back_config)
    quit_config.place(x=0,y=0)

    NextPilot = Button(Config, text='Siguiente', command=next_page)
    NextPilot.place(x=640, y=310)

    PrevPilot = Button(Config, text='Anterior', command=back_page)
    PrevPilot.place(x=60, y=310)


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
