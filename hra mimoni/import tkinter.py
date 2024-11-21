import tkinter

# Veľkosť hracej plochy
canvas_width = 300
canvas_height = 300

# Globálne premenné
restart_button = None

def posun_mimona(udalost):
    """Posúva obrázky na základe stlačených kláves."""
    klaves = udalost.keysym
    if klaves == "Left":
        platno.move(mimon_1, -10, 0)
    elif klaves == "Right":
        platno.move(mimon_1, 10, 0)
    elif klaves == "Up":
        platno.move(mimon_1, 0, -10)
    elif klaves == "Down":
        platno.move(mimon_1, 0, 10)
    elif klaves == "a":
        platno.move(mimon_2, -10, 0)
    elif klaves == "d":
        platno.move(mimon_2, 10, 0)
    elif klaves == "w":
        platno.move(mimon_2, 0, -10)
    elif klaves == "s":
        platno.move(mimon_2, 0, 10)

    kontrola_kolizie()

def kontrola_kolizie():
    """Kontroluje, či sa obrázky dostali na rovnakú pozíciu."""
    x1, y1, x2, y2 = platno.bbox(mimon_1)
    bx1, by1, bx2, by2 = platno.bbox(mimon_2)

    # Ak sa obrázky prekryjú, hra končí
    if (x1 < bx2 and x2 > bx1 and y1 < by2 and y2 > by1):
        platno.delete(mimon_1)
        platno.delete(mimon_2)
        ukaz_vyhercu("Hra skončila! Kolízia!")

def ukaz_vyhercu(vyherna_sprava):
    """Zobrazí správu o výhre a tlačidlo na reštart."""
    global restart_button
    platno.create_text(canvas_width // 2, canvas_height // 2, 
                       text=vyherna_sprava, font=("Helvetica", 16), fill="black")

    if restart_button is None:
        restart_button = tkinter.Button(okno, text="Zacat znova", command=reset_game)
        restart_button.pack()

def reset_game():
    """Resetuje hru do počiatočného stavu."""
    global restart_button, mimon_1, mimon_2

    platno.delete("all")
    mimon_1 = platno.create_image(150, 150, image=obr_mimon1, anchor="center")
    mimon_2 = platno.create_image(100, 100, image=obr_mimon2, anchor="center")

    restart_button.pack_forget()
    restart_button = None

# Inicializácia hlavného okna
okno = tkinter.Tk()
okno.title("Mimoni hra")

# Načítanie obrázkov
obr_mimon1 = tkinter.PhotoImage(file='mimon1.png')
obr_mimon2 = tkinter.PhotoImage(file='mimon2.png')

# Vytvorenie plátna
platno = tkinter.Canvas(okno, height=canvas_height, width=canvas_width, bg="lightgray")
platno.pack()

# Pridanie obrázkov na plátno
mimon_1 = platno.create_image(150, 150, image=obr_mimon1, anchor="center")
mimon_2 = platno.create_image(100, 100, image=obr_mimon2, anchor="center")

# Bind kláves na ovládanie
platno.bind_all("<Key>", posun_mimona)

# Spustenie hlavnej slučky
okno.mainloop()
