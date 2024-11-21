import tkinter
import random

# Veľkosť hracej plochy
canvas_width = 600
canvas_height = 600

# Globálne premenné
restart_button = None
banany = []
jahody = []
skore_mimon_1 = 0
skore_mimon_2 = 0


def posun_mimona(udalost):
    """Posúva obrázky na základe stlačených kláves."""
    global skore_mimon_1, skore_mimon_2
    klaves = udalost.keysym
    if klaves == "a":
        platno.move(mimon_1, -10, 0)
    elif klaves == "d":
        platno.move(mimon_1, 10, 0)
    elif klaves == "w":
        platno.move(mimon_1, 0, -10)
    elif klaves == "s":
        platno.move(mimon_1, 0, 10)
    elif klaves == "Left":
        platno.move(mimon_2, -10, 0)
    elif klaves == "Right":
        platno.move(mimon_2, 10, 0)
    elif klaves == "Up":
        platno.move(mimon_2, 0, -10)
    elif klaves == "Down":
        platno.move(mimon_2, 0, 10)

    
    kontrola_bananov()

def kontrola_vyhercu():
    """Kontroluje, či niektorý Mimoň dosiahol 100 bodov, a ukončí hru."""
    if skore_mimon_1 >= 100:
        ukaz_vyhercu("Žltý mimoň vyhral! Dosiahol 100 banánov!")
        return True
    elif skore_mimon_2 >= 100:
        ukaz_vyhercu("Fialový mimoň vyhral! Dosiahol 100 banánov!")
        return True
    return False
   
def kontrola_bananov():
    """Kontroluje, či hráči zobrali banány."""
    global banany, skore_mimon_1, skore_mimon_2
    for banan in banany[:]:  # Iterácia cez kópiu zoznamu
        bx1, by1, bx2, by2 = platno.bbox(banan)
        mx1, my1, mx2, my2 = platno.bbox(mimon_1)
        mx21, my21, mx22, my22 = platno.bbox(mimon_2)

        if mx1 < bx2 and mx2 > bx1 and my1 < by2 and my2 > by1:
            platno.delete(banan)
            banany.remove(banan)
            skore_mimon_1 += 1
            aktualizuj_skore()

        elif mx21 < bx2 and mx22 > bx1 and my21 < by2 and my22 > by1:
            platno.delete(banan)
            banany.remove(banan)
            skore_mimon_2 += 1
            aktualizuj_skore()
    if kontrola_vyhercu():
        return


def ukaz_vyhercu(vyherna_sprava):
    """Zobrazí správu o výhre a tlačidlo na reštart."""
    global restart_button
    platno.create_text(canvas_width // 2, canvas_height // 2, 
                       text=vyherna_sprava, font=("Helvetica", 20), fill="red")

    if restart_button is None:
        restart_button = tkinter.Button(okno, text="Začať znova", command=reset_game)
        restart_button.pack()

def reset_game():
    """Resetuje hru do počiatočného stavu."""
    global restart_button, mimon_1, mimon_2, banany, skore_mimon_1, skore_mimon_2

    platno.delete("all")
    mimon_1 = platno.create_image(100, 300, image=obr_mimon1, anchor="center")
    mimon_2 = platno.create_image(500, 300, image=obr_mimon2, anchor="center")
    banany.clear()
    skore_mimon_1 = 0
    skore_mimon_2 = 0
    aktualizuj_skore()

    if restart_button is not None:
        restart_button.pack_forget()
        restart_button = None

def aktualizuj_skore():
    """Zobrazuje aktuálne skóre hráčov."""
    platno.delete("skore")
    platno.create_text(10, 10, text=f"Žltý mimoň: {skore_mimon_1}", 
                       font=("Helvetica", 16),fill="yellow", anchor="nw", tag="skore",)
    platno.create_text(420, 10, text=f"Fialový mimoň: {skore_mimon_2}", 
                       font=("Helvetica", 16),fill="purple", anchor="nw", tag="skore",)

def pridaj_banan():
    """Pridá nový banán na náhodnú pozíciu."""
    global banany
    x = random.randint(50, canvas_width - 50)
    y = random.randint(50, canvas_height - 50)
    banan = platno.create_image(x, y, image=obr_banan, anchor="center")
    banany.append(banan)
    okno.after(500, pridaj_banan)  # Pridáva banány každé 3 sekundy


def pridaj_jahodu():
    """Pridá nový banán na náhodnú pozíciu."""
    global jahody
    x = random.randint(50, canvas_width - 50)
    y = random.randint(50, canvas_height - 50)
    jahoda = platno.create_image(x, y, image=obr_jahoda3, anchor="center")
    jahody.append(jahoda)
    okno.after(15000, pridaj_jahodu)  # Pridáva banány každé 3 sekundy

# Inicializácia hlavného okna
okno = tkinter.Tk()
okno.title("Mimoni hra")

# Načítanie obrázkov
obr_mimon1 = tkinter.PhotoImage(file='mimon1.png')
obr_mimon2 = tkinter.PhotoImage(file='mimon2.png')
obr_banan = tkinter.PhotoImage(file='banan.png')
obr_jahoda3 = tkinter.PhotoImage(file='jahoda3.png')

# Vytvorenie plátna
platno = tkinter.Canvas(okno, height=canvas_height, width=canvas_width, bg="lightblue")
platno.pack()

# Pridanie obrázkov na plátno
mimon_1 = platno.create_image(100, 300, image=obr_mimon1, anchor="center")
mimon_2 = platno.create_image(500, 300, image=obr_mimon2, anchor="center")

# Bind kláves na ovládanie
platno.bind_all("<Key>", posun_mimona)

# Spustenie pridávania banánov
pridaj_banan()
pridaj_jahodu()



# Spustenie hlavnej slučky
okno.mainloop()
