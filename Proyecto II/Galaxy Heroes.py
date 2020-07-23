import tkinter as tk
import pygame as pg
import os
import glob
import time
from threading import Thread

OPEN=True

def Imagenes(Ubicacion):
    Ruta = os.path.join(Ubicacion)
    Img = tk.PhotoImage(file=Ruta)
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
        Result.append(tk.PhotoImage(file=x[0]))
        return ImagenesAnim(x[1:],Result)

def sprites(Ruta):
    x = glob.glob(Ruta)
    x.sort()
    return ImagenesAnim(x,[])
    
    
Menu = tk.Tk()
Menu.minsize(1200, 650)
Menu.resizable(False, False)
Menu.title('Galaxy Heroes')
Menu.iconbitmap('Imagenes/Icono.ico')

musica('Audio\\MainTheme.mp3')

Fondo = tk.Canvas(Menu, width=1200, height=650, bg='black')
Fondo.place(x=0, y=0)

MainTitle = tk.Label(Menu, width=15, text='GALAXY HEROES', font=('Georgia',40), fg='lemonchiffon', bg='maroon')
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

def juego(Mode):
    Pant = tk.Toplevel()
    Pant.minsize(1200,650)
    Pant.resizable(False, False)
    Pant.title('Galaxy Heroes')
    Pant.iconbitmap('Imagenes/Icono.ico')

    Menu.withdraw()
    musica(1)

    Bg = tk.Canvas(Pant, width=1200, height=650, bg='black')
    Bg.place(x=0,y=0)

    Display = tk.Canvas(Pant, width=1200, height=60, bg='olive')
    Display.place(x=0, y=0)

    def back():
        Pant.destroy()
        musica('Audio\\MainTheme.mp3')
        Menu.deiconify()
        

    Exit = tk.Button(Display, text='Abandonar', font=('Helvatica'), command=back, fg='gold', bg='darkslategray')
    Exit.place(x=10, y=20)

    fondojuego = Imagenes('Imagenes\\Background\\GameBG.png')
    BgFondo = Bg.create_image(600, 325, image=fondojuego)
    
    Spaceship0 = Bg.create_image(600, 325, tags=('MYSHIP'))

    Spaceship = sprites('Imagenes/Spaceship/playership*.png')
    Right = sprites('Imagenes/Spaceship/right*.png')
    Left = sprites('Imagenes/Spaceship/left*.png')

    def anim(i):
        global OPEN
        if i==2:
            i=0
        if OPEN==True:
            loc = Bg.coords('MYSHIP')
            if 400<loc[0]<800:
                Bg.itemconfig('MYSHIP', image=Spaceship[i])
            if loc[0]<=400:
                Bg.itemconfig('MYSHIP', image=Right[i])
            if loc[0]>=800:
                Bg.itemconfig('MYSHIP', image=Left[i])
            time.sleep(0.15)
            Thread(target=anim, args=(i+1,)).start()

    def arriba(event):
        Ubi = Bg.coords('MYSHIP')
        if Ubi!=[]:
            Bg.coords('MYSHIP', Ubi[0], Ubi[1]-25)
            if (Ubi[1]-25)==125:
                Bg.coords('MYSHIP', Ubi[0], Ubi[1])

    def abajo(event):
        Ubi = Bg.coords('MYSHIP')
        if Ubi!=[]:
            Bg.coords('MYSHIP', Ubi[0], Ubi[1]+25)
            if (Ubi[1]+25)==605:
                Bg.coords('MYSHIP', Ubi[0], Ubi[1])

    def derecha(event):
        Ubi = Bg.coords('MYSHIP')
        if Ubi!=[]:
            Bg.coords('MYSHIP', Ubi[0]+25, Ubi[1])
            if (Ubi[0]+25)==1100:
                Bg.coords('MYSHIP', Ubi[0], Ubi[1])

    def izquierda(event):
        Ubi = Bg.coords('MYSHIP')
        if Ubi!=[]:
            Bg.coords('MYSHIP', Ubi[0]-25, Ubi[1])
            if (Ubi[0]-25)==100:
                Bg.coords('MYSHIP', Ubi[0], Ubi[1])

    if Mode==1:
        Asteroide = Bg.create_image(404, 300, tags=('AST'))
        Asteroids = sprites('Imagenes/Asteroids and obstacles/ast*.png')
    
        def ast_3D(i):
            if i==6:
                return Bg.delete('AST')
            else:
                Bg.itemconfig('AST', image=Asteroids[i])
                time.sleep(2)
                Thread(target=ast_3D, args=(i+1,)).start()

        ast_3D(0)

    if Mode==2:
        Anillo = Bg.create_image(400,500, tags=('RING'))
        Anillos = sprites('Imagenes/Asteroids and obstacles/Ring*.png')

        def anillo_3D(i):
            if i==5:
                return Bg.delete('RING')
            else:
                Bg.itemconfig('RING',image=Anillos[i])
                time.sleep(2)
                Thread(target=anillo_3D, args=(i+1,)).start()

        anillo_3D(0)
    
    anim(0)

    Pant.bind('<w>',arriba)
    Pant.bind('<s>',abajo)
    Pant.bind('<d>',derecha)
    Pant.bind('<a>',izquierda)        

    Pant.mainloop()

def select_juego1():
    return juego(1)

def select_juego2():
    return juego(2)

def config():
    Pant = tk.Toplevel()
    Pant.minsize(700,500)
    Pant.resizable(False, False)
    Pant.title('Galaxy Heroes')
    Pant.iconbitmap('Imagenes/Icono.ico')

    Pant.mainloop()

def scores():
    Pant = tk.Toplevel()
    Pant.minsize(700,500)
    Pant.resizable(False, False)
    Pant.title('Galaxy Heroes')
    Pant.iconbitmap('Imagenes/Icono.ico')

    Pant.mainloop()

def about():
    info = tk.Toplevel()
    info.minsize(700,500)
    info.resizable(False, False)
    info.title('Galaxy Heroes')
    info.iconbitmap('Imagenes/Icono.ico')
    
    C_info = tk.Canvas(info,width=700,height=500,bg='white')
    C_info.place(x=0,y=0)

    C_info.image1 = Imagenes('Imagenes/backgrounds/playbg.png')
    imgCanvas_info = C_info.create_image(0,0,anchor=NW,image= C_info.image1)    

    Label1 = tk.Label(C_info,text = "Instituto Tecnológico de Costa Rica", font =('Times New Roman',12))
    Label1.place(x=50,y=50)

    Label2 = tk.Label(C_info,text = "Ingeniería en Computadores", font =('Times New Roman',12))
    Label2.place(x=50,y=100)

    Label3 = tk.Label(C_info,text = "Profesor: Milton Villegas Lemus", font =('Times New Roman',12))
    Label3.place(x=50,y=150)

    Label4 = tk.Label(C_info,text = "Autores", font =('Times New Roman',12))
    Label4.place(x=400,y=25)

    Label5 = tk.Label(C_info,text = "Max Garro Mora", font =('Times New Roman',12))
    Label5.place(x=300,y=150)

    Label6 = tk.Label(C_info,text = "Eduardo Bolívar Minguet", font =('Times New Roman',12))
    Label6.place(x=425,y=150)

    maxgm = Imagenes('Imagenes/FOTO.png')
    maxgm_image = C_info.create_image(350, 100, image=maxgm)

    eduardobm = Imagenes('Imagenes/FOTO2.png')
    eduardobm_image = C_info.create_image(500, 100, image=eduardobm)

    def back_about():
        info.destroy()
        Menu.deiconify()        
    quit_info = Button(info,text = 'Volver al inicio',command=back_about)
    quit_info.place(x=0,y=0)
    Menu.withdraw()

    Pant.mainloop()

def salida():
    musica(1)
    Menu.destroy()

ModoJuego1 = tk.Button(Fondo, width=27, text='Destrucción de asteroides', command=select_juego1, font=('Times',15), fg='gold', bg='firebrick')
ModoJuego1.place(x=180, y=300)

ModoJuego2 = tk.Button(Fondo, width=27, text='Maniobras de prueba', command=select_juego2, font=('Times',15), fg='gold', bg='firebrick')
ModoJuego2.place(x=690, y=300)

Confi = tk.Button(Fondo, width=17, text='Configuración', command=config, font=('Times',15), fg='gold', bg='firebrick')
Confi.place(x=490, y=400)

Puntajes = tk.Button(Fondo, width=17, text='Altos puntajes', command=scores, font=('Times',15), fg='gold', bg='firebrick')
Puntajes.place(x=490, y=450)

About = tk.Button(Fondo, width=17, text='Acerca de', command=about, font=('Times',15), fg='gold', bg='firebrick')
About.place(x=490, y=500)

Cerrar = tk.Button(Fondo, width=17, text='Salir del juego', command=salida, font=('Times',15), fg='gold', bg='firebrick')
Cerrar.place(x=490, y=550)

Menu.mainloop()

quit()
