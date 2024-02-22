from tkinter import *   # Importieren von Tkinter; nötig für die graphische Oberfläche
import math             # fügt viele Mathematische Fuktionen hinzu (z.b. math.floor (s. move))
from typing import List # macht den Code übersichtlich und sagt aus was in die Liste soll 
import os, sys          # ist für die Funktion restart notwendig (os= operating system; sys= System)
import json             # ist für die Speicherung des Spielstandes notwendig (s. load_game und save_game)

# Setzen aller globalen Variablen
global mx, my, pieces_x, pieces_y, pos_piecex, pos_piecey, dame_move, dame_text, turn, chained, cur_piece, x_change, y_change, selected, turn_display_white, turn_display_black, piece_coords_x, piece_coords_y, canvas_width, canvas_height, blocking_piece_s, taken_piece, blocking_piece

pieces_x = None
pieces_y = None
pos_piecex = None
pos_piecey = None
dame_text = []
dame_move = None
cur_piece = None
blocking_piece_s = None
taken_piece = None
blocking_piece = None

mx=0
my=0
turn = 0
chained = 0
x_change=0
y_change=0
selected=0
piece_coords_x = 0
piece_coords_y = 0

# Erstellt das Fenster für das Spiel Dame
# master ist die Variable fürs Fenster 
master = Tk()
# gibt an ob die Möglichkeit bestehen soll ob man die Fenstergröße ändern darf
master.resizable(False, False) 
# gibt die Fenstergröße
canvas_width = 900
canvas_height = 900
master.title('Dame')


w = Canvas(master, width=canvas_width, height=canvas_height)
w.pack()

def exit():
    w.quit()
    w.destroy()

# Funktion für das Regelwerk 
def Regeln():
    # Toplevel bis scrollbar stellt das neue Fenster auf indem der Text von Regelwerk enthalten ist 
    # scrollbar ist fÜr den kleinen Text nicht notwendig und wurde daher auskommentiert 
    Toplevel
    w= Toplevel()
    w.resizable(True, False)
    w.geometry('1500x800')
    #scrollbar = Scrollbar(w)
    #scrollbar.pack( side = RIGHT, fill=Y )

    # Hier werden Schriftgröße, Schriftart(font), Schriftfarbe des folgenden Textes definiert 
    text1 = Text(w, height=20, width=30) 
    text1.insert(END,'\n')
    text2 = Text(w, height=200, width=500)
    scroll = Scrollbar(w, command=text2.yview)
    text2.configure(yscrollcommand=scroll.set)
    text2.tag_configure('bold_italics', font=('Arial', 12, 'bold', 'italic'))
    text2.tag_configure('big', font=('Verdana', 20, 'bold'))
    text2.tag_configure('color', foreground='#000000', 
						font=('Italic Text bold', 12, 'bold'))
    text2.insert(END,'\nRegelwerk\n', 'big')
    
    # Der Text der in dem Fenster ausgegeben werden soll
    quote = '''
    1. Das Ziel des Spieles ist, dass Sie am Ende der Partie alle Figuren Ihres Gegenübers in Besitz haben.
    2. Dazu bewegen Sie Ihre Figuren diagonal, immer nur auf den schwarzen Feldern verbleibend über das Spielfeld.
    3. Gehen Sie immer so vor, oder versuchen Sie es zumindest, dass Sie alle Figuren Ihres Gegners schlagen können.
    4. Gelingt dies nicht, ist es schon hilfreich, wenn Sie diese Figuren blockieren, so dass diese quasi vom Spiel ausgeschlossen sind, auch wenn diese noch am Tisch sind.
    5. Sie sind dann die Gewinnerin oder der Gewinner, wenn Ihr Gegner nicht mehr ziehen kann. Sei es, weil er keine Steine mehr hat, oder weil Sie ihn bewegungsunfähig auf dem Feld machten.
    6. Die Steine dürfen bei Dame nur in Einzelschritten nach vorne bewegt werden – immer diagonal, nie rückwärts.
    7. Sie dürfen dann zwei oder mehr Felder springen, wenn Sie eine gegnerische Figur schlagen, also überspringen können.
    8. Beim Schlagen dürfen Sie sich nicht auf das besetzte Feld stellen, auf dem der Gegner stand.
    9. Ebensowenig dürfen Sie schlagen, wenn das Feld hinter der Figur geblockt ist. Sei es durch einen Spielstein Ihres Gegners oder Ihren eigenen.
    10. Das Feld hinter der Figur muss also frei sein.
    11. Ist das Feld frei und steht noch eine Figur Ihres Gegners mit einem freien Feld dahinter, können Sie beide Figuren schlagen.
    12. Natürlich ist dies erweiterbar auf drei oder vier Steine, was aber eher selten vorkommt.
    13. Ist eine Figur schlagbar, so müssen Sie diese schlagen, ansonsten wird Ihr eigener Stein automatisch von Ihrem Gegner vom Feld genommen.
    14. Gelingt es Ihnen, Ihre Spielfigur bis an die letzte Spiellinie Ihres Gegners zu bringen, erhalten Sie bei diesem Zug eine Dame, die Sie ab dem folgenden Zug einsetzen dürfen.
    15. Die Dame ist im Spiel eigenen Regeln unterworfen. Sie darf sich in alle Richtungen bewegen und dazu über so viele Felder, wie Sie es möchten, wie es Ihnen möglich ist.
    16. Sie muss sich Schlagen einer Figur auch nicht auf das nächste freie Feld gesetzt werden.
    17. Sie können die ganze spielbare Reihe in einem Zug durchziehen, bis zum nächsten freien Feld. Auch die Dame unterliegt dem Schlagzwang, wie eine übliche Figur.
    18. Jeder schlagbare Stein ist zu nehmen – egal in welcher Richtung.
    19. Wird ein Spiel beendet und kein Gewinner ist gegeben, nennt es sich wie im Schach schlicht remis.
          '''  
    # Hier sind der zweite Text (in unserem Beispiel die Quelle) und unser Regelwerk enthalten 
    # Info: Da text1, text2 und der title unterschiedlich von Schriftgröße, Schriftart und Schriftfarbe definiert werden können ist es wichtig diese Unterscheidung für die vielen Wörter zu nutzen 
    text2.insert(END, quote, 'color')
    text2.insert(END, 'Quelle: https://praxistipps.focus.de/dame-spielanleitung-regeln-einfach-erklaert_99106\n', 'follow')
    text2.pack(side=LEFT)
    scroll.pack(side=RIGHT, fill=Y)
    w.title('Regelwerk')

# Funktion bei denen die Funktionen der Spielsteine für die Farbänderung darauf zugreifen 
global new_color1, new_color2
def change_piece_color(piece_id, new_color):
    w.itemconfig(piece_id, fill=new_color)

# Funktionen für die hellen Steine Farbe
# Helle Steine Farbe
def colour_s_hell1():
    global new_color2
    # Farbe für schwarz
    new_color2 = '#f7efb0'  
    for i in range(12): 
        change_piece_color(getPiece(i), new_color2)

def colour_s_hell2():
    # Farbe für schwarz
    global new_color2
    new_color2 = '#f0fcf3'  
    for i in range(12): 
        change_piece_color(getPiece(i), new_color2)

def colour_s_hell3():
    # Farbe für schwarz
    global new_color2
    new_color2 = '#b30404'  
    for i in range(12): 
        change_piece_color(getPiece(i), new_color2)

# Funktionen für die dunklen Steine Farbe
# Farbe für schwarz
def colour_s_dunkel1():
    global new_color1
    new_color1 = '#000000'  
    for i in range(12, 24):  
        change_piece_color(getPiece(i), new_color1)
# Farbe für Grau
def colour_s_dunkel2():
    global new_color1
    new_color1 = '#6e6d6d'  
    for i in range(12, 24): 
        change_piece_color(getPiece(i), new_color1)
# Farbe für schwarz
def colour_s_dunkel3():
    global new_color1
    new_color1 = '#0d3d1a'  
    for i in range(12, 24): 
        change_piece_color(getPiece(i), new_color1)

# Funktion für die Änderung der Farbe des Spielbrettes 
def colour_t_1():
    ct1="#ffdba1"
    ct2="#914c01"
    print('Farbe Spielbrett')  

def colour_t_1():
    ct1="#ffffff"
    ct2="#000000"
    print('Farbe Spielbrett')  

def color_spielbrettfarben1(new_colort1, new_colort2):
    global ct1, ct2
    ct1 = new_colort1        # Setzt die neue Farbe für die hellen Felder
    ct2 = new_colort2        # Setzt die neue Farbe für die dunklen Felder
    w.delete("field")        # Löscht das aktuelle Spielfeld also alles mit tags="field"
    checkered(w, field_size) # Das spielfeld wird neu gezeichnet 
    #initPieces()

# Funktion um das Spiel neuzustarten 
def restart(): 
    python = sys.executable
    os.execl(python,python, * sys.argv)
    restart()

# Funktion - Aufgeben
def aufgeben():
    if turn == 1:
        w.create_rectangle(0, 0, canvas_width, canvas_height, fill=new_color1)
        w.create_text(canvas_width/2, canvas_height/2, text="Schwarz gewinnt!", fill="#FFFFFF", font=('Akkurat 20'))
        restart_button = Button(master, text="Erneut spielen?", command=restart)
        restart_button.place(x=canvas_width/2, y=canvas_height/2)
        restart_button.pack()
        
    if turn == 0:
        w.create_rectangle(0, 0, canvas_width, canvas_height, fill=new_color2)
        w.create_text(canvas_width/2, canvas_height/2, text="Weiß gewinnt!", fill="#000000", font=('Akkurat 20'))
        restart_button = Button(master, text="Erneut spielen?", command=restart)
        restart_button.place(x=canvas_width/2, y=canvas_height/2)
        restart_button.pack()

# Funktion - Remis (Unentschieden)
# def remis():
#     back_button = None
#     rem_white = 0
#     rem_black = 0
#     rem_black=w.create_rectangle(0, 0, canvas_width/2, canvas_height, fill=new_color1)
#     rem_white=w.create_rectangle(canvas_width/2, 0, canvas_width, canvas_height, fill=new_color2)
#     white_button = Button(master, text="Unentschieden akzeptieren?", command= (rem_white == 1))
#     white_button.place(x=canvas_width/5, y=canvas_height/2)
#     white_button.pack()
#     
#     black_button = Button(master, text="Unentschieden akzeptieren?", command= (rem_black == 1))
#     black_button.place(x=3*canvas_width/5, y=canvas_height/2)
#     black_button.pack()
#     
#     back_button = Button(master, text="Zurück zum Spiel", command= w.delete(rem_black,rem_white,back_button))
#     back_button.place(x=canvas_width/2, y=canvas_height/2)
#     back_button.pack()


# "Spielfeld"
# Farben des Spielfeldes 
global ct1, ct2
ct1 = "#ffdba1"
ct2 = "#914c01"
# Funktion um das Spielfeld aufzustellen 
field_size=100
def checkered(canvas, line_distance):
    count=0
    x_count=0
    y_count=0
    while count <= 63:
        if x_count < 8:
            if (y_count%2) == 0:
                if (count%2) == 0:
                    field_white = w.create_rectangle(x_count*field_size,y_count*field_size,x_count*field_size+field_size,y_count*field_size+field_size,fill=ct1, tags="field")
                if (count%2) == 1:
                    field_black = w.create_rectangle(x_count*field_size,y_count*field_size,x_count*field_size+field_size,y_count*field_size+field_size,fill=ct2, tags="field")
            
            if (y_count%2) == 1:
                if (count%2) == 1:
                    field_white = w.create_rectangle(x_count*field_size,y_count*field_size,x_count*field_size+field_size,y_count*field_size+field_size,fill=ct1, tags="field")
                if (count%2) == 0:
                    field_black = w.create_rectangle(x_count*field_size,y_count*field_size,x_count*field_size+field_size,y_count*field_size+field_size,fill=ct2, tags="field")
            
            x_count+=1
            count+=1
            
        if x_count == 8:
            y_count+=1
            x_count=0

# Stellt die Beschrifung des Spielfeldes auf 
def field_descr():
    global field_size, turn_display_white, turn_display_black
    
    # Spalten
    w.create_text(field_size*7+(0.5*field_size), field_size*8+(0.2*field_size), text="A", fill="#000000", font=('Akkurat 20'))
    w.create_text(field_size*6+(0.5*field_size), field_size*8+(0.2*field_size), text="B", fill="#000000", font=('Akkurat 20'))
    w.create_text(field_size*5+(0.5*field_size), field_size*8+(0.2*field_size), text="C", fill="#000000", font=('Akkurat 20'))
    w.create_text(field_size*4+(0.5*field_size), field_size*8+(0.2*field_size), text="D", fill="#000000", font=('Akkurat 20'))
    w.create_text(field_size*3+(0.5*field_size), field_size*8+(0.2*field_size), text="E", fill="#000000", font=('Akkurat 20'))
    w.create_text(field_size*2+(0.5*field_size), field_size*8+(0.2*field_size), text="F", fill="#000000", font=('Akkurat 20'))
    w.create_text(field_size*1+(0.5*field_size), field_size*8+(0.2*field_size), text="G", fill="#000000", font=('Akkurat 20'))
    w.create_text(field_size*0+(0.5*field_size), field_size*8+(0.2*field_size), text="H", fill="#000000", font=('Akkurat 20'))
    
    # Zeilen
    w.create_text(field_size*8+(0.2*field_size), field_size*7+(0.5*field_size), text="1", fill="#000000", font=('Akkurat 20'))
    w.create_text(field_size*8+(0.2*field_size), field_size*6+(0.5*field_size), text="2", fill="#000000", font=('Akkurat 20'))
    w.create_text(field_size*8+(0.2*field_size), field_size*5+(0.5*field_size), text="3", fill="#000000", font=('Akkurat 20'))
    w.create_text(field_size*8+(0.2*field_size), field_size*4+(0.5*field_size), text="4", fill="#000000", font=('Akkurat 20'))
    w.create_text(field_size*8+(0.2*field_size), field_size*3+(0.5*field_size), text="5", fill="#000000", font=('Akkurat 20'))
    w.create_text(field_size*8+(0.2*field_size), field_size*2+(0.5*field_size), text="6", fill="#000000", font=('Akkurat 20'))
    w.create_text(field_size*8+(0.2*field_size), field_size*1+(0.5*field_size), text="7", fill="#000000", font=('Akkurat 20'))
    w.create_text(field_size*8+(0.2*field_size), field_size*0+(0.5*field_size), text="8", fill="#000000", font=('Akkurat 20'))
    
    # Spieleranzeige
    turn_display_white=w.create_text(canvas_width/2, canvas_height+field_size, text="Am Zug: Weiß", fill="#000000", font=('Akkurat 20'))
    turn_display_black=w.create_text(canvas_width/2, canvas_height-(0.25*field_size), text="Am Zug: Schwarz", fill="#000000", font=('Akkurat 20'))
    
    # Bedienungserklärung
    w.create_text(canvas_width*0.85, canvas_height*0.96, text="RMB: Spielstein aus-/abwählen", fill="#000000", font=('Akkurat 15'))
    w.create_text(canvas_width*0.825, canvas_height*0.96+25, text="LMB: Spielstein bewegen", fill="#000000", font=('Akkurat 15'))


# "Spielsteine"
# Definiert die Spielsteine 
def place_pieces():
    
    #Weiße Steine
    global piece1, piece2, piece3, piece4, piece5, piece6, piece7, piece8, piece9, piece10, piece11, piece12
    piece1 = w.create_oval(mx * field_size, my * field_size, mx * field_size + field_size, my * field_size + field_size, fill="#f7efb0", tags=('w'))
    piece2 = w.create_oval(mx * field_size, my * field_size, mx * field_size + field_size, my * field_size + field_size, fill="#f7efb0", tags=('w'))
    piece3 = w.create_oval(mx * field_size, my * field_size, mx * field_size + field_size, my * field_size + field_size, fill="#f7efb0", tags=('w'))
    piece4 = w.create_oval(mx * field_size, my * field_size, mx * field_size + field_size, my * field_size + field_size, fill="#f7efb0", tags=('w'))
    piece5 = w.create_oval(mx * field_size, my * field_size, mx * field_size + field_size, my * field_size + field_size, fill="#f7efb0", tags=('w'))
    piece6 = w.create_oval(mx * field_size, my * field_size, mx * field_size + field_size, my * field_size + field_size, fill="#f7efb0", tags=('w'))
    piece7 = w.create_oval(mx * field_size, my * field_size, mx * field_size + field_size, my * field_size + field_size, fill="#f7efb0", tags=('w'))
    piece8 = w.create_oval(mx * field_size, my * field_size, mx * field_size + field_size, my * field_size + field_size, fill="#f7efb0", tags=('w'))
    piece9 = w.create_oval(mx * field_size, my * field_size, mx * field_size + field_size, my * field_size + field_size, fill="#f7efb0", tags=('w'))
    piece10 = w.create_oval(mx * field_size, my * field_size, mx * field_size + field_size, my * field_size + field_size, fill="#f7efb0", tags=('w'))
    piece11 = w.create_oval(mx * field_size, my * field_size, mx * field_size + field_size, my * field_size + field_size, fill="#f7efb0", tags=('w'))
    piece12 = w.create_oval(mx * field_size, my * field_size, mx * field_size + field_size, my * field_size + field_size, fill="#f7efb0", tags=('w'))

    #Schwarze Steine 
    global piece13, piece14, piece15, piece16, piece17, piece18, piece19, piece20, piece21, piece22, piece23, piece24

    piece13 = w.create_oval(mx * field_size, my * field_size, mx * field_size + field_size, my * field_size + field_size, fill="#000000", tags='b')
    piece14 = w.create_oval(mx * field_size, my * field_size, mx * field_size + field_size, my * field_size + field_size, fill="#000000", tags='b')
    piece15 = w.create_oval(mx * field_size, my * field_size, mx * field_size + field_size, my * field_size + field_size, fill="#000000", tags='b')
    piece16 = w.create_oval(mx * field_size, my * field_size, mx * field_size + field_size, my * field_size + field_size, fill="#000000", tags='b')
    piece17 = w.create_oval(mx * field_size, my * field_size, mx * field_size + field_size, my * field_size + field_size, fill="#000000", tags='b')
    piece18 = w.create_oval(mx * field_size, my * field_size, mx * field_size + field_size, my * field_size + field_size, fill="#000000", tags='b')
    piece19 = w.create_oval(mx * field_size, my * field_size, mx * field_size + field_size, my * field_size + field_size, fill="#000000", tags='b')
    piece20 = w.create_oval(mx * field_size, my * field_size, mx * field_size + field_size, my * field_size + field_size, fill="#000000", tags='b')
    piece21 = w.create_oval(mx * field_size, my * field_size, mx * field_size + field_size, my * field_size + field_size, fill="#000000", tags='b')
    piece22 = w.create_oval(mx * field_size, my * field_size, mx * field_size + field_size, my * field_size + field_size, fill="#000000", tags='b')
    piece23 = w.create_oval(mx * field_size, my * field_size, mx * field_size + field_size, my * field_size + field_size, fill="#000000", tags='b')
    piece24 = w.create_oval(mx * field_size, my * field_size, mx * field_size + field_size, my * field_size + field_size, fill="#000000", tags='b')
    
    global pos_piecex, pos_piecey, pieces_x, pieces_y
    # Spielsteine werden nach der Liste platziert 
    if pos_piecex == None or pos_piecey == None:
        pieces_x = [0, 2, 4, 6, 1, 3, 5, 7, 0, 2, 4, 6, 1, 3, 5, 7, 0, 2, 4, 6, 1, 3, 5, 7]
        pieces_y = [5, 5, 5, 5, 6, 6, 6, 6, 7, 7, 7, 7, 0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2]


    #def initPieces(): 
    # Diese Schleife platziert die Steine nach der Liste nacheinander 
    #i bezieht sich auf case (s. getPiece)
    i=0
    while(i < len(pieces_x)): #len=länge das arrays 
        w.moveto(getPiece(i), pieces_x[i]*100, pieces_y[i]*100)

        i+=1
    #initPieces()

# Platziert die Steine anhand von der while-Schleife 
def getPiece(pieceNumber):
    match pieceNumber:
        case 0:
            return piece1
        case 1:
            return piece2
        case 2:
            return piece3
        case 3:
            return piece4
        case 4:
            return piece5
        case 5:
            return piece6
        case 6:
            return piece7
        case 7:
            return piece8
        case 8:
            return piece9
        case 9:
            return piece10
        case 10:
            return piece11
        case 11:
            return piece12
        case 12:
            return piece13
        case 13:
            return piece14
        case 14:
            return piece15
        case 15:
            return piece16
        case 16:
            return piece17
        case 17:
            return piece18
        case 18:
            return piece19
        case 19:
            return piece20
        case 20:
            return piece21
        case 21:
            return piece22
        case 22:
            return piece23
        case 23:
            return piece24

print(pieces_x == None, pieces_y == None)
print(pieces_x, pieces_y)


#gibt die Spielsteinnummer anhand von Koordinaten zurück
def findPiece(x,y):
    i = 0
    for i in range(len(pieces_x)): # i zählt von 0 bis 11
        if pieces_x[i] == x: # sucht aus der liste den wert 
            if pieces_y[i] == y:
                return i # gibt dir den index zurück wenn beide übereinstimmen
    #Kein Spielstein an den Koordinaten gefunden
    return -420

def cur_pos():
    global pos_piecex
    global pos_piecey
    pos_piecex=[w.coords(piece1)[0],
                w.coords(piece2)[0],
                w.coords(piece3)[0],
                w.coords(piece4)[0],
                w.coords(piece5)[0],
                w.coords(piece6)[0],
                w.coords(piece7)[0],
                w.coords(piece8)[0],
                w.coords(piece9)[0],
                w.coords(piece10)[0],
                w.coords(piece11)[0],
                w.coords(piece12)[0],
                w.coords(piece13)[0],
                w.coords(piece14)[0],
                w.coords(piece15)[0],
                w.coords(piece16)[0],
                w.coords(piece17)[0],
                w.coords(piece18)[0],
                w.coords(piece19)[0],
                w.coords(piece20)[0],
                w.coords(piece21)[0],
                w.coords(piece22)[0],
                w.coords(piece23)[0],
                w.coords(piece24)[0]]

    pos_piecey=[w.coords(piece1)[1],
                w.coords(piece2)[1],
                w.coords(piece3)[1],
                w.coords(piece4)[1],
                w.coords(piece5)[1],
                w.coords(piece6)[1],
                w.coords(piece7)[1],
                w.coords(piece8)[1],
                w.coords(piece9)[1],
                w.coords(piece10)[1],
                w.coords(piece11)[1],
                w.coords(piece12)[1],
                w.coords(piece13)[1],
                w.coords(piece14)[1],
                w.coords(piece15)[1],
                w.coords(piece16)[1],
                w.coords(piece17)[1],
                w.coords(piece18)[1],
                w.coords(piece19)[1],
                w.coords(piece20)[1],
                w.coords(piece21)[1],
                w.coords(piece22)[1],
                w.coords(piece23)[1],
                w.coords(piece24)[1]]

    pos_piecex=[round(x/field_size) for x in pos_piecex]
    pos_piecey=[round(x/field_size) for x in pos_piecey]

    #print("Xs: ", pos_piecex, "Ys: ", pos_piecey)

#gibt die Spielsteinnummer anhand von koords back
def find_cur_Piece(x,y):
    global pos_piecex
    global pos_piecey
    i = 0
    cur_pos()
    for i in range(len(pos_piecex)): # i zählt von 0 bis 11
        if pos_piecex[i] == x: # sucht aus der liste den wert 
            if pos_piecey[i] == y:
                return i # ´gibt dir den index zurück wenn beide übereinstimmen
    #Kein Spielstein an den Koordinaten gefunden
    return -420

# Anzeige des ziehenden Spieler
def turn_display():
    global turn, turn_display_white, turn_display_black, canvas_width, canvas_height
    print(turn)
    
    if turn == 0:
        w.moveto(turn_display_black, canvas_width/2-100, canvas_height-(0.25*field_size)-15)
        w.moveto(turn_display_white, canvas_width/2, canvas_height+400*field_size)
        
    if turn == 1:
        w.moveto(turn_display_white, canvas_width/2-100, canvas_height-(0.25*field_size)-15)
        w.moveto(turn_display_black, canvas_width/2, canvas_height+400*field_size)

# Beschriftung der Dame-Spielsteine
def dame_desrc():
    global dame_text
    # Löschen aller bestehenden Beschriftungen
    for id in dame_text:
        w.delete(id)
    dame_text = []  # Leeren der Liste

    for t in range(0,  24):
        if (w.itemcget(getPiece(t), "tags") == "w d" or w.itemcget(getPiece(t), "tags") == "w d current"):
            # Erstellen einer neuen Beschriftung und speichern der ID
            id = w.create_text(w.coords(getPiece(t))[0] + field_size /  2, w.coords(getPiece(t))[1] + field_size /  2, text="D", font=("Akkurat",  40), fill="#000000")
            dame_text.append(id)
        if (w.itemcget(getPiece(t), "tags") == "b d" or w.itemcget(getPiece(t), "tags") == "b d current"):
            # Erstellen einer neuen Beschriftung und speichern der ID
            id = w.create_text(w.coords(getPiece(t))[0] + field_size /  2, w.coords(getPiece(t))[1] + field_size /  2, text="D", font=("Akkurat",  40), fill="#FFFFFF")
            dame_text.append(id)

def new_game():
    w.delete("all")
    checkered(w,field_size)
    field_descr()
    place_pieces()
    turn_display()
    cur_pos()
    
    
new_game()

new_color1= '#000000'
new_color2= '#f7efb0'

# Funktion, zuständig für die Auswahl eines einzelnen Spielsteines
def select(event):
    global selected, mx, my, piece_coords_x, piece_coords_y, x_change, y_change, cur_piece, turn, chained, cur_piece_tags, dame_move
    
    
    # Gibt die Mausposition im Rahmen des Spielfeldes an.
    mx=math.floor(event.x/field_size)
    my=math.floor(event.y/field_size)
    print("Mouse position: (%s %s)" % (event.x, event.y))
    print("Field: ",mx,",",my)
    
    # Setzt einen ausgewählten Spielstein im Mehrfachzug zurück. (Die Move-Funktion macht diesen Schritt rückgängig, wenn ein weiterer Zug möglich ist)
    if chained == 1:
        if cur_piece_tags[0] == "w":
            w.itemconfigure(cur_piece, fill=new_color2)
            turn = 0
            w.moveto(cur_piece, field_size*400, field_size*400)
        
        if cur_piece_tags[0] == "b":
            w.itemconfigure(cur_piece, fill=new_color1)
            turn = 1
            w.moveto(cur_piece, field_size*400, field_size*400)
        chained = 0
        dame_move = 0
        cur_piece = None
        turn_display()
    
    # Wählt einen ausgewählten Stein ab, wenn die Select-Funktion bei ausgewähltem Stein erneut auf dem Stein ausgeführt wird.
    if cur_piece != None:
        print("CP: ",cur_piece)
        print("Turn: ",turn)
        if mx == w.coords(cur_piece)[0] and my == w.coords(cur_piece)[1]:
            chained = 0
            dame_move = 0
            turn_display()
    
    # Eigentliche Select-Funktion; bei initialem Ausführen
    if chained == 0:
        print("CUT --- CUT --- CUT --- SELECT --- CUT --- CUT --- CUT")
        if selected == 1 and cur_piece != None:
            if cur_piece_tags[0] == "w":
                w.itemconfigure(cur_piece, fill=new_color2)
            if cur_piece_tags[0] == "b":
                w.itemconfigure(cur_piece, fill=new_color1)
        
        # Gibt die Mausposition im Rahmen des Spielfeldes an
        mx=math.floor(event.x/field_size)
        my=math.floor(event.y/field_size)
        print("Mouse position: (%s %s)" % (event.x, event.y))
        print("Field: ",mx,",",my)
        
        # Überprüft, ob sich an der Mausposition ein Spielstein befindet -> wird zum ausgewählten Spielstein
        cur_piece=(getPiece(find_cur_Piece(mx,my)))
        cur_piece_tags=w.itemcget(cur_piece, "tags")
        print("CP: ",cur_piece)
        print("Turn: ",turn)
        print("Piece Tags: ",w.itemcget(cur_piece, "tags"))
        
        # Überprüfung, ob ausgewählter Spielstein "weiß" ist + ob "weiß" am Zug ist
        if cur_piece_tags[0] == "w" and turn == 1:
            
            # Berechnung der Spielsteinkoordinaten
            piece_coords_x=round(w.coords(cur_piece)[0]/field_size)
            piece_coords_y=round(w.coords(cur_piece)[1]/field_size)
            print("Piece coords: ",piece_coords_x,",",piece_coords_y)
            
            # Berechnung der Veränderung zwischen Mausposition und Spielsteinkoordinaten
            x_change=math.floor(piece_coords_x)-mx
            y_change=math.floor(piece_coords_y)-my
            print("X_change: ", x_change, ", Y_Change: ", y_change)
            
            # Auswählen des Spielsteines (+ Einfärbung)
            if x_change == 0 and y_change == 0:
                w.itemconfigure(cur_piece, fill="#009900")
                selected = 1
                
                if w.itemcget(cur_piece, "tags") == "w d" or w.itemcget(cur_piece, "tags") == "w d current":
                    dame_move = 1
        
        # Überprüfung, ob ausgewählter Spielstein "schwarz" ist + ob "schwarz" am Zug ist
        if cur_piece_tags[0] == "b" and turn == 0:
            
            # Berechnung der Spielsteinkoordinaten
            piece_coords_x=round(w.coords(cur_piece)[0]/field_size)
            piece_coords_y=round(w.coords(cur_piece)[1]/field_size)
            print("Piece coords: ",piece_coords_x,",",piece_coords_y)
            
            # Berechnung der Veränderung zwischen Mausposition und Spielsteinkoordinaten
            x_change=math.floor(piece_coords_x)-mx
            y_change=math.floor(piece_coords_y)-my
            print("X_change: ", x_change, ", Y_Change: ", y_change)
            
            # Auswählen des Spielsteines (+ Einfärbung)
            if x_change == 0 and y_change == 0:
                w.itemconfigure(cur_piece, fill="#009900")
                selected = 1
                
                if w.itemcget(cur_piece, "tags") == "b d" or w.itemcget(cur_piece, "tags") == "b d current":
                    dame_move = 1

# Select-Funktion wird an Klick der "rechten Maustaste" gebunden
w.bind("<Button-3>", select)


# Funktion, zuständig für die Bewegung des ausgewählten Spielsteines
def move(event):
    print("CUT --- CUT --- CUT --- Move --- CUT --- CUT --- CUT")
    global selected, cur_piece, turn, piece_coords_x, piece_coords_y, chained, cur_piece_tags, dame_move
    
    # Funktionsteil, zuständig für alle nicht-Damen
    if selected == 1 and not(w.itemcget(cur_piece, "tags") == "w d" or w.itemcget(cur_piece, "tags") == "b d" or w.itemcget(cur_piece, "tags") == "w d current" or w.itemcget(cur_piece, "tags") == "b d current"):
        
        # Zurücksetzen der Spielsteineinfärbung
        if cur_piece_tags[0] == "w":
            w.itemconfigure(cur_piece, fill=new_color2)
        if cur_piece_tags[0] == "b":
            w.itemconfigure(cur_piece, fill=new_color1)
        
        # Gibt die Mausposition im Rahmen des Spielfeldes an
        mx=math.floor(event.x/field_size)
        my=math.floor(event.y/field_size)
        print("Mouse position: (%s %s)" % (event.x, event.y))
        print("Field: %s, %s" % (mx, my))
        
        # Berechnung der Veränderung zwischen Mausposition und Spielsteinkoordinaten
        x_change=math.floor(piece_coords_x)-mx
        y_change=math.floor(piece_coords_y)-my
        print("X_change: ", x_change, ", Y_Change: ", y_change)
        
        # Spielsteinbewegung und -blockierung
        print("CUT --- CUT --- CUT --- Blockierung --- CUT --- CUT --- CUT")
        
        # Überprüfung, ob ausgewählter Spielstein "weiß" ist + ob "weiß" am Zug ist
        if cur_piece_tags[0] == "w" and turn == 1 and chained == 0:
            
            # Berechnung eines möglichen blockierenden Spielsteines
            blocking_piece=getPiece(find_cur_Piece(piece_coords_x-x_change,piece_coords_y-abs(y_change)))
            print("Blocking White Piece: ", blocking_piece, ", X: %s, Y: %s" % (piece_coords_x-x_change,(piece_coords_y-abs(y_change))))
            
            # Überprüfung ob gewähltes Feld = valider Spielzug + Ausführung des Spielzugs
            if abs(x_change) == 1 and y_change == 1:
                if blocking_piece == None:
                    if (piece_coords_y > 0) and (piece_coords_x+(x_change*(-1)) < 8) and (piece_coords_x+(x_change*(-1)) > -1):
                        w.move(cur_piece,x_change*field_size*(-1),y_change*field_size*(-1))
                        turn = 0

        # Überprüfung, ob ausgewählter Spielstein "schwarz" ist + ob "schwarz" am Zug ist
        if cur_piece_tags[0] == "b" and turn == 0 and chained == 0:
            
            # Berechnung eines möglichen blockierenden Spielsteines
            blocking_piece=getPiece(find_cur_Piece(piece_coords_x-x_change,piece_coords_y+abs(y_change)))
            print("Blocking Black Piece: ", blocking_piece, ", X: %s, Y: %s" % (piece_coords_x-x_change,(piece_coords_y+abs(y_change))))
            
            # Überprüfung ob gewähltes Feld = valider Spielzug + Ausführung des Spielzugs
            if abs(x_change) == 1 and y_change == -1:
                if blocking_piece == None:
                    if (piece_coords_y < 7) and (piece_coords_x+(x_change*(-1)) < 8) and (piece_coords_x+(x_change*(-1)) > -1):
                        w.move(cur_piece,x_change*field_size*(-1),y_change*field_size*(-1))
                        turn = 1
        
        # Spielstein überspringen
        print("CUT --- CUT --- CUT --- Überspringen --- CUT --- CUT --- CUT")
        
        # Überprüfung, ob ausgewählter Spielstein "weiß" ist + ob ausgewähltes Feld einen möglichen Zug zur Folge hat
        if cur_piece_tags[0] == "w" and (piece_coords_x+(x_change*(-1)) < 8) and (piece_coords_x+(x_change*(-1)) > -1) and turn == 1:
            
            # Berechnung eines möglichen blockierenden und eines möglichen eingenommenen Spielsteines
            blocking_piece=getPiece(find_cur_Piece(piece_coords_x-x_change,piece_coords_y-abs(y_change)))
            taken_piece=getPiece(find_cur_Piece(piece_coords_x-math.floor(x_change/2),piece_coords_y-abs(y_change-1)))
            print("Blocking White Piece: ", blocking_piece, ", X: %s, Y: %s" % (piece_coords_x-x_change,piece_coords_y-abs(y_change)))
            print("Taken Piece by White: ", taken_piece, ", X: %s, Y: %s" % (piece_coords_x-math.floor(x_change/2),piece_coords_y-abs(y_change-1)))
            
            taken_piece_tags=w.itemcget(taken_piece, "tags")
            print("Taken Piece Tags: ", taken_piece_tags)
            
            x_future = piece_coords_x-x_change
            y_future = piece_coords_y-y_change
                            
            print("X_change: ", x_change, ", Y_Change: ", y_change)
            print("FUTURE: ", x_future, y_future)
            
            # Überprüfung ob gewähltes Feld = valider Spielzug + Ausführung des Spielzugs
            if abs(x_change) == 2 and y_change == 2:
                if taken_piece != None and blocking_piece == None:
                    if (y_future < 8 and y_future > -1) and (x_future < 8 and x_future > -1) and taken_piece_tags[0] != "w":
                        w.move(cur_piece,x_change*field_size*(-1),y_change*field_size*(-1))
                        w.moveto(taken_piece, field_size*400, field_size*400)
                        
                        print("CUT --- CUT --- CUT --- Werte aktualisiert --- CUT --- CUT --- CUT")
                        
                        # Gibt die Mausposition im Rahmen des Spielfeldes an
                        mx=math.floor(event.x/field_size)
                        my=math.floor(event.y/field_size)
                        print("Mouse position: (%s %s)" % (event.x, event.y))
                        print("Field: %s, %s" % (mx, my))
                        
                        # Neuberechnung der Spielsteinkoordinaten
                        piece_coords_x=round(w.coords(cur_piece)[0]/field_size)
                        piece_coords_y=round(w.coords(cur_piece)[1]/field_size)
                        print("Piece coords: ",piece_coords_x,",",piece_coords_y)
                        
                        # Neuberechnung eines möglichen blockierenden und eines möglichen eingenommenen Spielsteines
                        def white_schlag():
                            for x in range(-1,2):
                                for y in range(-1,2):
                                    if x > 0 and y < 0:
                                        blocking_piece = None
                                        taken_piece = None
                                        blocking_piece=getPiece(find_cur_Piece(piece_coords_x+2,piece_coords_y-2))
                                        taken_piece=getPiece(find_cur_Piece(piece_coords_x+1,piece_coords_y-1))
                                        
                                        print("1Blocking White Piece: ", blocking_piece, ", X: %s, Y: %s" % (piece_coords_x+2,piece_coords_y-2))
                                        print("1Taken Piece by White: ", taken_piece, ", X: %s, Y: %s" % (piece_coords_x+1,piece_coords_y-1))
                                        if piece_coords_y-1 < 0:
                                            return [None, None]
                                        
                                        else:
                                            return [blocking_piece, taken_piece]
                                        
                                    if x < 0 and y < 0:
                                        blocking_piece=getPiece(find_cur_Piece(piece_coords_x-2,piece_coords_y-2))
                                        taken_piece=getPiece(find_cur_Piece(piece_coords_x-1,piece_coords_y-1))
                                        
                                        print("2Blocking White Piece: ", blocking_piece, ", X: %s, Y: %s" % (piece_coords_x-2,piece_coords_y-2))
                                        print("2Taken Piece by White: ", taken_piece, ", X: %s, Y: %s" % (piece_coords_x-1,piece_coords_y-1))
                                        if piece_coords_y-1 < 0:
                                            return [None, None]
                                        
                                        else:
                                            return [blocking_piece, taken_piece]
                                        
                        if white_schlag()[1] != None:
                            taken_piece = white_schlag()[1]
                        else:
                            taken_piece = None
                        
                        if white_schlag()[0] != None:
                            blocking_piece = white_schlag()[0]
                        else:
                            blocking_piece = None
                        
                        
                        if taken_piece != None:
                            taken_piece_tags=w.itemcget(taken_piece, "tags")
                            print("Taken Piece Tags: ", taken_piece_tags)
                        
                            #Berechnung einer möglichen Zugrichtung
                            cur_piece_x = w.coords(cur_piece)[0]  # x-Koordinate der Dame
                            taken_piece_x = w.coords(taken_piece)[0]  # x-Koordinate des geschlagenen Spielsteins

                            # Berechnen Sie die Richtung des Übersprungs
                            direction = cur_piece_x - taken_piece_x

                            # Aktualisieren Sie x_change basierend auf der Richtung
                            if direction >  0:
                                x_change =  2  # Dame schlägt nach rechts
                            elif direction <  0:
                                x_change = -2  # Dame schlägt nach links
                            
                            y_change=-2
                            x_future = piece_coords_x+x_change
                            y_future = piece_coords_y+y_change
                            
                            print("X_change: ", x_change, ", Y_Change: ", y_change)
                            print("FUTURE: ", x_future, y_future)
                            
                            print("Blocking: %s, Taken: %s" % (blocking_piece, taken_piece))
                            
                            # Überprüfung ob ein Mehrfachzug möglich ist
                            if blocking_piece == None and taken_piece != None:
                                if (y_future < 8 and y_future > -1) and (x_future < 8 and x_future > -1) and taken_piece_tags[0] != "w":
                                        chained = 1
                                        w.itemconfigure(cur_piece, fill="#009900")
                                
                            # Neuberechnung der Spielsteinkoordinaten
                            piece_coords_x=round(w.coords(cur_piece)[0]/field_size)
                            piece_coords_y=round(w.coords(cur_piece)[1]/field_size)
                            print("Piece coords: ",piece_coords_x,",",piece_coords_y)
                            
                            x_future = piece_coords_x+x_change
                            y_future = piece_coords_y+y_change
                            print("FUTURE: ", x_future, y_future)
                            
                            # Unterbrechungsüberprüfung eines Mehrfachzugs
                            if not(blocking_piece == None and taken_piece != None) or not((y_future <= 7 and y_future >= 0) or (x_future <= 7 and x_future >= 0)) or taken_piece_tags[0] == "w":
                                w.itemconfigure(cur_piece, fill=new_color2)
                                turn = 0
                                chained = 0
                                selected = 0
                        else:
                            w.itemconfigure(cur_piece, fill=new_color2)
                            turn = 0
                            chained = 0
                            selected = 0

        # Überprüfung, ob ausgewählter Spielstein "schwarz" ist + ob ausgewähltes Feld einen möglichen Zug zur Folge hat
        if cur_piece_tags[0] == "b" and (piece_coords_x+(x_change*(-1)) < 8) and (piece_coords_x+(x_change*(-1)) > -1)  and turn == 0:
            
            # Berechnung eines möglichen blockierenden und eines möglichen eingenommenen Spielsteines
            blocking_piece=getPiece(find_cur_Piece(piece_coords_x-x_change,piece_coords_y+abs(y_change)))
            taken_piece=getPiece(find_cur_Piece(piece_coords_x-math.floor(x_change/2),piece_coords_y+abs(y_change+1)))
            print("Blocking Black Piece: ", blocking_piece, ", X: %s, Y: %s" % (piece_coords_x-x_change,piece_coords_y+abs(y_change)))
            print("Taken Piece by black: ", taken_piece, ", X: %s, Y: %s" % (piece_coords_x-math.floor(x_change/2),piece_coords_y+abs(y_change+1)))
            
            taken_piece_tags=w.itemcget(taken_piece, "tags")
            print("Taken Piece Tags: ", taken_piece_tags)
            
            x_future = piece_coords_x-x_change
            y_future = piece_coords_y-y_change
                            
            print("X_change: ", x_change, ", Y_Change: ", y_change)
            print("FUTURE: ", x_future, y_future)
            
            # Überprüfung ob gewähltes Feld = valider Spielzug + Ausführung des Spielzugs
            if abs(x_change) == 2 and y_change == -2:
                if taken_piece != None and blocking_piece == None:
                    if (y_future < 8 and y_future > -1) and (x_future < 8 and x_future > -1) and taken_piece_tags[0] != "b":
                        w.move(cur_piece,x_change*field_size*(-1),y_change*field_size*(-1))
                        w.moveto(taken_piece, field_size*400, field_size*400)
                        
                        print("CUT --- CUT --- CUT --- Werte aktualisiert --- CUT --- CUT --- CUT")
                        
                        # Gibt die Mausposition im Rahmen des Spielfeldes an
                        mx=math.floor(event.x/field_size)
                        my=math.floor(event.y/field_size)
                        print("Mouse position: (%s %s)" % (event.x, event.y))
                        print("Field: %s, %s" % (mx, my))
                        
                        # Neuberechnung der Spielsteinkoordinaten
                        piece_coords_x=round(w.coords(cur_piece)[0]/field_size)
                        piece_coords_y=round(w.coords(cur_piece)[1]/field_size)
                        print("Piece coords: ",piece_coords_x,",",piece_coords_y)
                        
                        # Neuberechnung eines möglichen blockierenden und eines möglichen eingenommenen Spielsteines
                        def black_schlag():
                            for x in range(-1,2):
                                for y in range(-1,2):
                                    if x > 0 and y > 0:
                                        blocking_piece = None
                                        taken_piece = None
                                        blocking_piece=getPiece(find_cur_Piece(piece_coords_x+2,piece_coords_y+2))
                                        taken_piece=getPiece(find_cur_Piece(piece_coords_x+1,piece_coords_y+1))
                                        
                                        print("1Blocking Black Piece: ", blocking_piece, ", X: %s, Y: %s" % (piece_coords_x+2,piece_coords_y+2))
                                        print("1Taken Piece by Black: ", taken_piece, ", X: %s, Y: %s" % (piece_coords_x+1,piece_coords_y+1))
                                        if piece_coords_y+1 > 7:
                                            return [None, None]
                                        
                                        else:
                                            return [blocking_piece, taken_piece]
                                        
                                    if x < 0 and y > 0:
                                        blocking_piece=getPiece(find_cur_Piece(piece_coords_x-2,piece_coords_y+2))
                                        taken_piece=getPiece(find_cur_Piece(piece_coords_x-1,piece_coords_y+1))
                                        
                                        print("2Blocking Black Piece: ", blocking_piece, ", X: %s, Y: %s" % (piece_coords_x-2,piece_coords_y+2))
                                        print("2Taken Piece by Black: ", taken_piece, ", X: %s, Y: %s" % (piece_coords_x-1,piece_coords_y+1))
                                        if piece_coords_y+1 > 7:
                                            return [None, None]
                                        
                                        else:
                                            return [blocking_piece, taken_piece]
                            
                        print(black_schlag())
                        if black_schlag()[1] != None:
                            taken_piece = black_schlag()[1]
                        else:
                            taken_piece = None
                        
                        if black_schlag()[0] != None:
                            blocking_piece = black_schlag()[0]
                        else:
                            blocking_piece = None
                        
                        if taken_piece != None:
                            taken_piece_tags=w.itemcget(taken_piece, "tags")
                            print("Taken Piece Tags: ", taken_piece_tags)
                        
                            #Berechnung einer möglichen Zugrichtung
                            cur_piece_x = w.coords(cur_piece)[0]  # x-Koordinate der Dame
                            taken_piece_x = w.coords(taken_piece)[0]  # x-Koordinate des geschlagenen Spielsteins

                            # Berechnen Sie die Richtung des Übersprungs
                            direction = cur_piece_x - taken_piece_x

                            # Aktualisieren Sie x_change basierend auf der Richtung
                            if direction >  0:
                                x_change =  2  # Dame schlägt nach rechts
                            elif direction <  0:
                                x_change = -2  # Dame schlägt nach links
                            
                            y_change=2
                            x_future = piece_coords_x+x_change
                            y_future = piece_coords_y+y_change
                            
                            print("X_change: ", x_change, ", Y_Change: ", y_change)
                            print("FUTURE: ", x_future, y_future)
                            
                            print("Blocking: %s, Taken: %s" % (blocking_piece, taken_piece))
                            
                            # Überprüfung ob ein Mehrfachzug möglich ist
                            if blocking_piece == None and taken_piece != None:
                                if (y_future < 8 and y_future > -1) and (x_future < 8 and x_future > -1) and taken_piece_tags[0] != "b":
                                    chained = 1
                                    w.itemconfigure(cur_piece, fill="#009900")
                            
                            # Neuberechnung der Spielsteinkoordinaten
                            piece_coords_x=round(w.coords(cur_piece)[0]/field_size)
                            piece_coords_y=round(w.coords(cur_piece)[1]/field_size)
                            print("Piece coords: ",piece_coords_x,",",piece_coords_y)
                            
                            x_future = piece_coords_x+x_change
                            y_future = piece_coords_y+y_change
                            print("FUTURE: ", x_future, y_future)
                            
                            # Unterbrechungsüberprüfung eines Mehrfachzugs
                            if not(blocking_piece == None and taken_piece != None) or not((y_future <= 7 and y_future >= 0) or (x_future <= 7 and x_future >= 0)) or taken_piece_tags[0] == "b":
                                w.itemconfigure(cur_piece, fill=new_color1)
                                turn = 1
                                chained = 0
                                selected = 0
                        else:
                            w.itemconfigure(cur_piece, fill=new_color1)
                            turn = 1
                            chained = 0
                            selected = 0
        
        # Neuberechnung der Spielsteinkoordinaten
        piece_coords_x=round(w.coords(cur_piece)[0]/field_size)
        piece_coords_y=round(w.coords(cur_piece)[1]/field_size)
        print("Piece coords: ",piece_coords_x,",",piece_coords_y)
        
        # Tag-Verwaltung der Dame
        if (piece_coords_y == 0) and cur_piece_tags[0] == "w":
            w.addtag_withtag("d", cur_piece)
            print("DAME WEIß ALARM!!")
            print("Tags:", w.gettags(cur_piece))
            
        if (piece_coords_y == 7) and cur_piece_tags[0] == "b":
            w.addtag_withtag("d", cur_piece)
            print("DAME SCHWARZ ALARM!!")
            print("Tags:", w.gettags(cur_piece))
        
        cur_piece_tags=w.itemcget(cur_piece, "tags")
        print("Piece Tags: ",cur_piece_tags)
        print("Turn: ",turn)
        
    # Movement für die Dame
    # Funktionsteil, zuständig für alle Damen
    if selected == 1 and (w.itemcget(cur_piece, "tags") == "w d" or w.itemcget(cur_piece, "tags") == "b d" or w.itemcget(cur_piece, "tags") == "w d current" or w.itemcget(cur_piece, "tags") == "b d current"):
        
        # Zurücksetzen der Spielsteineinfärbung
        if cur_piece_tags[0] == "w":
            w.itemconfigure(cur_piece, fill=new_color2)
        if cur_piece_tags[0] == "b":
            w.itemconfigure(cur_piece, fill=new_color1)
            
        print("Turn: ",turn)
        
        # Gibt die Mausposition im Rahmen des Spielfeldes an
        mx=math.floor(event.x/field_size)
        my=math.floor(event.y/field_size)
        print("Mouse position: (%s %s)" % (event.x, event.y))
        print("Field: %s, %s" % (mx, my))
        
        # Berechnung der Veränderung zwischen Mausposition und Spielsteinkoordinaten
        x_change=math.floor(piece_coords_x)-mx
        y_change=math.floor(piece_coords_y)-my
        print("X_change: ", x_change, ", Y_Change: ", y_change)
        
        x_future = piece_coords_x-x_change
        y_future = piece_coords_y-y_change
        print("FUTURE: ", x_future, y_future)
        
        #Spielsteinbewegung und -blockierung
        print("CUT --- CUT --- CUT --- Blockierung --- CUT --- CUT --- CUT")
        print("Turn: ",turn)
        # Berechnung eines möglichen blockierenden Spielsteines auf der gesamten Wegstrecke der Damebewegung
        def simple_block_dame():
            for f in range(1,abs(x_change)+1):
                if x_change*(-1) >= 0 and y_change*(-1) >= 0:
                    blocking_piece_s=getPiece(find_cur_Piece(piece_coords_x+f,piece_coords_y+f))
                    print("1Blocking Dame Piece simple: ", blocking_piece_s, ", X: %s, Y: %s" % (piece_coords_x+f,piece_coords_y+f), f)
                    if blocking_piece_s != None:
                        return blocking_piece_s
                    
                if x_change*(-1) >= 0 and y_change*(-1) < 0:
                    blocking_piece_s=getPiece(find_cur_Piece(piece_coords_x+f,piece_coords_y-f))
                    print("2Blocking Dame Piece simple: ", blocking_piece_s, ", X: %s, Y: %s" % (piece_coords_x+f,piece_coords_y-f), f)
                    if blocking_piece_s != None:
                        return blocking_piece_s
                    
                if x_change*(-1) < 0 and y_change*(-1) >= 0:
                    blocking_piece_s=getPiece(find_cur_Piece(piece_coords_x-f,piece_coords_y+f))
                    print("3Blocking Dame Piece simple: ", blocking_piece_s, ", X: %s, Y: %s" % (piece_coords_x-f,piece_coords_y+f), f)
                    if blocking_piece_s != None:
                        return blocking_piece_s
                    
                if x_change*(-1) < 0 and y_change*(-1) < 0:
                    blocking_piece_s=getPiece(find_cur_Piece(piece_coords_x-f,piece_coords_y-f))
                    print("4Blocking Dame Piece simple: ", blocking_piece_s, ", X: %s, Y: %s" % (piece_coords_x-f,piece_coords_y-f), f)
                    if blocking_piece_s != None:
                        return blocking_piece_s
        
        def block_dame():
            if x_change*(-1) >= 0 and y_change*(-1) >= 0:
                blocking_piece=getPiece(find_cur_Piece(piece_coords_x+2,piece_coords_y+2))
                print("1Blocking Dame Piece: ", blocking_piece, ", X: %s, Y: %s" % (piece_coords_x+2,piece_coords_y+2))
                if blocking_piece != None:
                        return blocking_piece
                
            if x_change*(-1) >= 0 and y_change*(-1) < 0:
                blocking_piece=getPiece(find_cur_Piece(piece_coords_x+2,piece_coords_y-2))
                print("2Blocking Dame Piece: ", blocking_piece, ", X: %s, Y: %s" % (piece_coords_x+2,piece_coords_y-2))
                if blocking_piece != None:
                        return blocking_piece
                
            if x_change*(-1) < 0 and y_change*(-1) >= 0:
                blocking_piece=getPiece(find_cur_Piece(piece_coords_x-2,piece_coords_y+2))
                print("3Blocking Dame Piece: ", blocking_piece, ", X: %s, Y: %s" % (piece_coords_x-2,piece_coords_y+2))
                if blocking_piece != None:
                        return blocking_piece
                
            if x_change*(-1) < 0 and y_change*(-1) < 0:
                blocking_piece=getPiece(find_cur_Piece(piece_coords_x-2,piece_coords_y-2))
                print("4Blocking Dame Piece: ", blocking_piece, ", X: %s, Y: %s" % (piece_coords_x-2,piece_coords_y-2))
                if blocking_piece != None:
                        return blocking_piece
        
        def taken_by_dame():
            if x_change*(-1) >= 0 and y_change*(-1) >= 0:
                taken_piece=getPiece(find_cur_Piece(piece_coords_x+1,piece_coords_y+1))
                print("1Taken Piece by Dame: ", taken_piece, ", X: %s, Y: %s" % (piece_coords_x+1,piece_coords_y+1))
                if taken_piece != None:
                        return taken_piece
            
            if x_change*(-1) >= 0 and y_change*(-1) < 0:
                taken_piece=getPiece(find_cur_Piece(piece_coords_x+1,piece_coords_y-1))
                print("2Taken Piece by Dame: ", taken_piece, ", X: %s, Y: %s" % (piece_coords_x+1,piece_coords_y-1))
                if taken_piece != None:
                        return taken_piece
                
            if x_change*(-1) < 0 and y_change*(-1) >= 0:
                taken_piece=getPiece(find_cur_Piece(piece_coords_x-1,piece_coords_y+1))
                print("3Taken Piece by Dame: ", taken_piece, ", X: %s, Y: %s" % (piece_coords_x-1,piece_coords_y+1))
                if taken_piece != None:
                        return taken_piece
                
            if x_change*(-1) < 0 and y_change*(-1) < 0:
                taken_piece=getPiece(find_cur_Piece(piece_coords_x-1,piece_coords_y-1))
                print("4Taken Piece by Dame: ", taken_piece, ", X: %s, Y: %s" % (piece_coords_x-1,piece_coords_y-1))
                if taken_piece != None:
                        return taken_piece
        
        # Überprüfung ob gewähltes Feld = valider Spielzug + Ausführung des Spielzugs
        global dame_move
        blocking_piece_s = simple_block_dame()
        taken_piece = taken_by_dame()
        blocking_piece = block_dame()
        if taken_piece != None:
            taken_piece_tags=w.itemcget(taken_piece, "tags")
            print("Taken Piece Tags: ", taken_piece_tags)
        print(blocking_piece,taken_piece)
        
        if abs(x_change) <= 7 and abs(y_change) <= 7 and abs(x_change) == abs(y_change):
            if blocking_piece_s == None and taken_piece == None and dame_move == 1:
                dame_move = 0
                if (y_future < 8 and y_future > -1) and (x_future < 8 and x_future > -1):
                    w.move(cur_piece,x_change*field_size*(-1),y_change*field_size*(-1))
                    if cur_piece_tags[0] == "w" and turn == 1:
                        turn = 0
                    if cur_piece_tags[0] == "b" and turn == 0:
                        turn = 1
        print("Turn: ",turn)
        #Spielstein überspringen
        print("CUT --- CUT --- CUT --- Überspringen --- CUT --- CUT --- CUT")
        
        # Überprüfen, ob Zug im Spielfeld stattfindet
        if (y_future < 8 and y_future > -1) and (x_future < 8 and x_future > -1):
            
            # Überprüfung ob gewähltes Feld = valider Spielzug + Ausführung des Spielzugs
            if abs(x_change) == 2 and abs(y_change) == 2:
                if taken_piece != None and blocking_piece == None and (dame_move == 1 or chained == 1):
                    multi_path = None
                    if cur_piece_tags[0] != taken_piece_tags[0]:
                            w.move(cur_piece,x_change*field_size*(-1),y_change*field_size*(-1))
                            w.moveto(taken_piece, field_size*400, field_size*400)
                            multi_path = 1
                            dame_move = 0
                    
                    print("Turn: ",turn)
                    print("CUT --- CUT --- CUT --- Werte aktualisiert --- CUT --- CUT --- CUT")
                    
                    # Gibt die Mausposition im Rahmen des Spielfeldes an
                    mx=math.floor(event.x/field_size)
                    my=math.floor(event.y/field_size)
                    print("Mouse position: (%s %s)" % (event.x, event.y))
                    print("Field: %s, %s" % (mx, my))
                    
                    # Neuberechnung der Spielsteinkoordinaten
                    piece_coords_x=round(w.coords(cur_piece)[0]/field_size)
                    piece_coords_y=round(w.coords(cur_piece)[1]/field_size)
                    print("Piece coords: ",piece_coords_x,",",piece_coords_y)
                    
                    # Neuberechnung eines möglichen blockierenden und eines möglichen eingenommenen Spielsteines
                    x_change=math.floor(piece_coords_x)-mx
                    y_change=math.floor(piece_coords_y)-my
                    print("X_change: ", x_change, ", Y_Change: ", y_change)
                    
                    for x in range(-1,2):
                        for y in range(-1,2):
                            if x > 0 and y < 0:
                                blocking_piece=getPiece(find_cur_Piece(piece_coords_x+2,piece_coords_y-2))
                                taken_piece=getPiece(find_cur_Piece(piece_coords_x+1,piece_coords_y-1))
                                print("Blocking Dame Piece: ", blocking_piece, ", X: %s, Y: %s" % (piece_coords_x+2,piece_coords_y-2))
                                print("Taken Piece by Dame: ", taken_piece, ", X: %s, Y: %s" % (piece_coords_x+1,piece_coords_y-1))
                                
                            if x < 0 and y < 0:
                                blocking_piece=getPiece(find_cur_Piece(piece_coords_x-2,piece_coords_y-2))
                                taken_piece=getPiece(find_cur_Piece(piece_coords_x-1,piece_coords_y-1))
                                print("Blocking Dame Piece: ", blocking_piece, ", X: %s, Y: %s" % (piece_coords_x-2,piece_coords_y-2))
                                print("Taken Piece by Dame: ", taken_piece, ", X: %s, Y: %s" % (piece_coords_x-1,piece_coords_y-1))
                                
                            if x > 0 and y > 0:
                                blocking_piece=getPiece(find_cur_Piece(piece_coords_x+2,piece_coords_y+2))
                                taken_piece=getPiece(find_cur_Piece(piece_coords_x+1,piece_coords_y+1))
                                print("Blocking Dame Piece: ", blocking_piece, ", X: %s, Y: %s" % (piece_coords_x+2,piece_coords_y+2))
                                print("Taken Piece by Dame: ", taken_piece, ", X: %s, Y: %s" % (piece_coords_x+1,piece_coords_y+1))
                                
                            if x < 0 and y > 0:
                                blocking_piece=getPiece(find_cur_Piece(piece_coords_x-2,piece_coords_y+2))
                                taken_piece=getPiece(find_cur_Piece(piece_coords_x-1,piece_coords_y+1))
                                print("Blocking Dame Piece: ", blocking_piece, ", X: %s, Y: %s" % (piece_coords_x-2,piece_coords_y+2))
                                print("Taken Piece by Dame: ", taken_piece, ", X: %s, Y: %s" % (piece_coords_x-1,piece_coords_y+1))
                    
                    print("Blocking: %s, Taken: %s" % (blocking_piece, taken_piece))
                    
                    # Überprüfung ob ein Mehrfachzug möglich ist
                    if blocking_piece == None and taken_piece != None and multi_path == 1:
                        chained = 1
                        w.itemconfigure(cur_piece, fill="#009900")
                        
                    else:
                        print("FEHLER!")
                        if cur_piece_tags[0] == "w":
                            turn = 0
                            w.itemconfigure(cur_piece, fill=new_color2)
                        if cur_piece_tags[0] == "b":
                            turn = 1
                            w.itemconfigure(cur_piece, fill=new_color1)
            
                    # Neuberechnung der Spielsteinkoordinaten
                    piece_coords_x=round(w.coords(cur_piece)[0]/field_size)
                    piece_coords_y=round(w.coords(cur_piece)[1]/field_size)
                    print("Piece coords: ",piece_coords_x,",",piece_coords_y)
                    
                    x_future = piece_coords_x+x_change
                    y_future = piece_coords_y+y_change
                    print("FUTURE: ", x_future, y_future)
                    
                    # Unterbrechungsüberprüfung eines Mehrfachzugs
                    if not(blocking_piece == None or taken_piece != None or multi_path == 1):
                        if (y_future < 8 and y_future > -1) and (x_future < 8 and x_future > -1):
                            chained = 0
                            selected = 0
                            multi_path = 0
                            dame_move = 0
                        
                            if cur_piece_tags[0] == "w":
                                turn = 0
                                w.itemconfigure(cur_piece, fill=new_color2)
                            if cur_piece_tags[0] == "b":
                                turn = 1
                                w.itemconfigure(cur_piece, fill=new_color1)
        
        # Neuberechnung der Spielsteinkoordinaten
        piece_coords_x=round(w.coords(cur_piece)[0]/field_size)
        piece_coords_y=round(w.coords(cur_piece)[1]/field_size)
        print("Piece coords: ",piece_coords_x,",",piece_coords_y)
    
    dame_desrc()
    game_end()
    turn_display()

# Move-Funktion wird an Klick der "linken Maustaste" gebunden
w.bind('<Button-1>', move)

def game_end():
    global canvas_width, canvas_height
    if pos_piecex[:12].count(400) == 12:
        w.create_rectangle(0, 0, canvas_width, canvas_height, fill=new_color1)
        w.create_text(canvas_width/2, canvas_height/2, text="Schwarz gewinnt!", fill="#FFFFFF", font=('Akkurat 20'))
        restart_button = Button(master, text="Erneut spielen?", command=restart)
        restart_button.place(x=canvas_width/2, y=canvas_height/2)
        restart_button.pack()
        
    if pos_piecex[12:].count(400) == 12:
        w.create_rectangle(0, 0, canvas_width, canvas_height, fill=new_color2)
        w.create_text(canvas_width/2, canvas_height/2, text="Weiß gewinnt!", fill="#000000", font=('Akkurat 20'))
        restart_button = Button(master, text="Erneut spielen?", command=restart)
        restart_button.place(x=canvas_width/2, y=canvas_height/2)
        restart_button.pack()

# Funktion zum Laden eines Spielstandes
def load_game():
    global pos_piecex, pos_piecey, new_color1, new_color2, turn, piece1, piece2, piece3, piece4, piece5, piece6, piece7, piece8, piece9, piece10, piece11, piece12, piece13, piece14, piece15, piece16, piece17, piece18, piece19, piece20, piece21, piece22, piece23, piece24
    w.delete("all")
    with open('saved_game.json', 'r') as file:
        game_data = json.load(file)
        pos_piecex = game_data['pos_piecex']
        pos_piecey = game_data['pos_piecey']
        new_color1 = game_data['new_color1']
        new_color2 = game_data['new_color2']
        turn = game_data['turn']
        piece1 = game_data['piece1']
        piece2 = game_data['piece2']
        piece3 = game_data['piece3']
        piece4 = game_data['piece4']
        piece5 = game_data['piece5']
        piece6 = game_data['piece6']
        piece7 = game_data['piece7']
        piece8 = game_data['piece8']
        piece9 = game_data['piece9']
        piece10 = game_data['piece10']
        piece11 = game_data['piece11']
        piece12 = game_data['piece12']
        piece13 = game_data['piece13']
        piece14 = game_data['piece14']
        piece15 = game_data['piece15']
        piece16 = game_data['piece16']
        piece17 = game_data['piece17']
        piece18 = game_data['piece18']
        piece19 = game_data['piece19']
        piece20 = game_data['piece20']
        piece21 = game_data['piece21']
        piece22 = game_data['piece22']
        piece23 = game_data['piece23']
        piece24 = game_data['piece24']
        dame_text = game_data['dame_text']
        
    print("Spiel geladen.")
    print(pos_piecex, pos_piecey, new_color1, new_color2, turn, dame_text)
    
    checkered(w,field_size)
    field_descr()
    turn_display()
    dame_desrc()
    
    def piece_create_al(x, y, tags, farbe):
        global field_size
        return w.create_oval(x * field_size, y * field_size, x * field_size + field_size, y * field_size + field_size, fill=farbe, tags=tags)
    
    piece1 = piece_create_al(pos_piecex[0], pos_piecey[0], piece1, new_color2)
    piece2 = piece_create_al(pos_piecex[1], pos_piecey[1], piece2, new_color2)
    piece3 = piece_create_al(pos_piecex[2], pos_piecey[2], piece3, new_color2)
    piece4 = piece_create_al(pos_piecex[3], pos_piecey[3], piece4, new_color2)
    piece5 = piece_create_al(pos_piecex[4], pos_piecey[4], piece5, new_color2)
    piece6 = piece_create_al(pos_piecex[5], pos_piecey[5], piece6, new_color2)
    piece7 = piece_create_al(pos_piecex[6], pos_piecey[6], piece7, new_color2)
    piece8 = piece_create_al(pos_piecex[7], pos_piecey[7], piece8, new_color2)
    piece9 = piece_create_al(pos_piecex[8], pos_piecey[8], piece9, new_color2)
    piece10 = piece_create_al(pos_piecex[9], pos_piecey[9], piece10, new_color2)
    piece11 = piece_create_al(pos_piecex[10], pos_piecey[10], piece11, new_color2)
    piece12 = piece_create_al(pos_piecex[11], pos_piecey[11], piece12, new_color2)
    piece13 = piece_create_al(pos_piecex[12], pos_piecey[12], piece13, new_color1)
    piece14 = piece_create_al(pos_piecex[13], pos_piecey[13], piece14, new_color1)
    piece15 = piece_create_al(pos_piecex[14], pos_piecey[14], piece15, new_color1)
    piece16 = piece_create_al(pos_piecex[15], pos_piecey[15], piece16, new_color1)
    piece17 = piece_create_al(pos_piecex[16], pos_piecey[16], piece17, new_color1)
    piece18 = piece_create_al(pos_piecex[17], pos_piecey[17], piece18, new_color1)
    piece19 = piece_create_al(pos_piecex[18], pos_piecey[18], piece19, new_color1)
    piece20 = piece_create_al(pos_piecex[19], pos_piecey[19], piece20, new_color1)
    piece21 = piece_create_al(pos_piecex[20], pos_piecey[20], piece21, new_color1)
    piece22 = piece_create_al(pos_piecex[21], pos_piecey[21], piece22, new_color1)
    piece23 = piece_create_al(pos_piecex[22], pos_piecey[22], piece23, new_color1)
    piece24 = piece_create_al(pos_piecex[23], pos_piecey[23], piece24, new_color1)


# Funktion zum Speichern eines Spielstandes
def save_game():
    global pos_piecex, pos_piecey, new_color1, new_color2, turn, piece1, piece2, piece3, piece4, piece5, piece6, piece7, piece8, piece9, piece10, piece11, piece12, piece13, piece14, piece15, piece16, piece17, piece18, piece19, piece20, piece21, piece22, piece23, piece24
    cur_pos()
    game_data = {
        'pos_piecex': pos_piecex,
        'pos_piecey': pos_piecey,
        'new_color1': new_color1,
        'new_color2': new_color2,
        'turn': turn,
        'dame_text': dame_text,
        'piece1' : w.gettags(piece1),
        'piece2' : w.gettags(piece2),
        'piece3' : w.gettags(piece3),
        'piece4' : w.gettags(piece4),
        'piece5' : w.gettags(piece5),
        'piece6' : w.gettags(piece6),
        'piece7' : w.gettags(piece7),
        'piece8' : w.gettags(piece8),
        'piece9' : w.gettags(piece9),
        'piece10' : w.gettags(piece10),
        'piece11' : w.gettags(piece11),
        'piece12' : w.gettags(piece12),
        'piece13' : w.gettags(piece13),
        'piece14' : w.gettags(piece14),
        'piece15' : w.gettags(piece15),
        'piece16' : w.gettags(piece16),
        'piece17' : w.gettags(piece17),
        'piece18' : w.gettags(piece18),
        'piece19' : w.gettags(piece19),
        'piece20' : w.gettags(piece20),
        'piece21' : w.gettags(piece21),
        'piece22' : w.gettags(piece22),
        'piece23' : w.gettags(piece23),
        'piece24' : w.gettags(piece24)

    }
    with open('saved_game.json', 'w') as file:
        json.dump(game_data, file)
    print("Spiel gespeichert.")
    print(pos_piecex, pos_piecey, new_color1, new_color2, turn, "Spielsteintags", dame_text)



# "Menüs"
# Definiert die Menüs/ Untermenüs 
menubar = Menu(master)
master.config(menu=menubar)
Einstellungen_menu = Menu(menubar,tearoff=0)
game_action_menu = Menu(Einstellungen_menu,tearoff=0)
colour_menu = Menu(menubar,tearoff=0)
colour_menu = Menu(Einstellungen_menu, tearoff=0)
colour_menu_Steine_1 = Menu(colour_menu, tearoff=0)
colour_menu_Steine_2 = Menu(colour_menu, tearoff=0)
colour_menu_Spielbrett = Menu(colour_menu, tearoff=0)

# Ordnet den großen Menüs die Namen zu 
menubar.add_cascade(label="Einstellungen", menu=Einstellungen_menu)
menubar.add_cascade(label="Farben", menu=colour_menu)

# Stellt die verschiedenen Funktionen von Einstellungen auf und definiert sie mit Funktionen 
Einstellungen_menu.add_command(label='Spielregeln', command = Regeln )
Einstellungen_menu.add_command(label='Speichern', command=save_game)
Einstellungen_menu.add_command(label='Laden', command=load_game)
Einstellungen_menu.add_cascade(label="Spielaktion",menu=game_action_menu)
Einstellungen_menu.add_command(label='Neustart', command = restart)
Einstellungen_menu.add_command(label='Beenden',command=master.destroy)

# Stellt die Untermenüs auf und gibt ihnen Namen 
colour_menu.add_cascade(label="Spieler Dunkel",menu=colour_menu_Steine_2)
colour_menu.add_cascade(label="Spieler Hell",menu=colour_menu_Steine_1)
'''colour_menu.add_cascade(label="Spielbrett",menu=colour_menu_Spielbrett)'''

# Belegt die Untermenüs mit weiteren funktionen und dazugehöroger Beschriftung 
# Farbe > Spieler 1 
colour_menu_Steine_1.add_command(label="Beage",command= colour_s_hell1)
colour_menu_Steine_1.add_command(label="Weiß",command=colour_s_hell2)
colour_menu_Steine_1.add_command(label="Rot",command=colour_s_hell3)
# Farbe > Spieler 2 
colour_menu_Steine_2.add_command(label="Schwarz",command= colour_s_dunkel1)
colour_menu_Steine_2.add_command(label="Grau",command=colour_s_dunkel2)
colour_menu_Steine_2.add_command(label="Grün",command=colour_s_dunkel3)

# Einstellungen > Spielaktion
game_action_menu.add_command(label="Aufgeben", command = aufgeben)
#game_action_menu.add_command(label="Remis", command = remis())

'''# Farbe Spielbrett 
colour_menu_Spielbrett.add_command(label="Standartspielfeld",command=lambda: color_spielbrettfarben1("#ffeebb", "#8a2be2") ) 
colour_menu_Spielbrett.add_command(label="Weinachten",command=lambda: color_spielbrettfarben1("#000000", "#ffffff"))
# Erklärung zu lambda: erstellt eine anonyme Funktion und erwartet keine Ardumente, ist wichtig wegen den Klammern '''


w.pack()
w.mainloop()
master.mainloop()