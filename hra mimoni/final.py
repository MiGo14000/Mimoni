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
zivoty_mimon_1 = 3
zivoty_mimon_2 = 3
keys_pressed = set()  # Track currently pressed keys

def update_positions():
    """Moves the Mimon characters based on pressed keys."""
    global skore_mimon_1, skore_mimon_2

    # Pohyb zlty mimon 1
    if "a" in keys_pressed:
        platno.move(mimon_1, -10, 0)
    if "d" in keys_pressed:
        platno.move(mimon_1, 10, 0)
    if "w" in keys_pressed:
        platno.move(mimon_1, 0, -10)
    if "s" in keys_pressed:
        platno.move(mimon_1, 0, 10)

    # Pohyb fialovy mimon 2
    if "Left" in keys_pressed:
        platno.move(mimon_2, -10, 0)
    if "Right" in keys_pressed:
        platno.move(mimon_2, 10, 0)
    if "Up" in keys_pressed:
        platno.move(mimon_2, 0, -10)
    if "Down" in keys_pressed:
        platno.move(mimon_2, 0, 10)

    # Kontrola banánov a jahôd
    kontrola_bananov()
    kontrola_jahod()

    # Plan next update
    okno.after(20, update_positions)

def on_key_press(event):
    """Adds the pressed key to the key state set."""
    keys_pressed.add(event.keysym)

def on_key_release(event):
    """Removes the released key from the key state set."""
    keys_pressed.discard(event.keysym)

def kontrola_jahod():
    """Kontroluje, či hráči zobrali jahody a odoberá životy."""
    global jahody, zivoty_mimon_1, zivoty_mimon_2
    for jahoda in jahody[:]:
        jx1, jy1, jx2, jy2 = platno.bbox(jahoda)
        mx1, my1, mx2, my2 = platno.bbox(mimon_1)
        mx21, my21, mx22, my22 = platno.bbox(mimon_2)

        if mx1 < jx2 and mx2 > jx1 and my1 < jy2 and my2 > jy1:
            platno.delete(jahoda)
            jahody.remove(jahoda)
            zivoty_mimon_1 -= 1
            aktualizuj_zivoty()
            kontrola_prehrania()

        elif mx21 < jx2 and mx22 > jx1 and my21 < jy2 and my22 > jy1:
            platno.delete(jahoda)
            jahody.remove(jahoda)
            zivoty_mimon_2 -= 1
            aktualizuj_zivoty()
            kontrola_prehrania()

def kontrola_prehrania():
    """Kontroluje, či niektorý hráč stratil všetky životy."""
    if zivoty_mimon_1 <= 0:
        ukaz_vyhercu("Fialový mimoň vyhral!")
    elif zivoty_mimon_2 <= 0:
        ukaz_vyhercu("Žltý mimoň vyhral!")

def aktualizuj_zivoty():
    """Zobrazuje aktuálny počet životov hráčov."""
    platno.delete("zivoty")
    platno.create_text(10, 35, text=f"Životy: {zivoty_mimon_1}",
                       font=("Helvetica", 16), fill="red", anchor="nw", tag="zivoty")
    platno.create_text(420, 35, text=f"Životy: {zivoty_mimon_2}",
                       font=("Helvetica", 16), fill="red", anchor="nw", tag="zivoty")

def aktualizuj_skore():
    """Zobrazuje aktuálne skóre hráčov na obrazovke."""
    platno.delete("skore")  # Odstráni predchádzajúce skóre
    platno.create_text(10, 10, text=f"Žltý mimoň: {skore_mimon_1}", 
                       font=("Helvetica", 16), fill="yellow", anchor="nw", tag="skore")
    platno.create_text(420, 10, text=f"Fialový mimoň: {skore_mimon_2}", 
                       font=("Helvetica", 16), fill="purple", anchor="nw", tag="skore")

def zmizni_banan(banan):
    """Odstráni banán po sekunde."""
    if banan in banany:
        platno.delete(banan)
        banany.remove(banan)

def pridaj_banan():
    """Pridá nový banán na náhodnú pozíciu."""
    global banany
    x = random.randint(50, canvas_width - 50)
    y = random.randint(50, canvas_height - 50)
    banan = platno.create_image(x, y, image=obr_banan, anchor="center")
    banany.append(banan)
    okno.after(5000, lambda: zmizni_banan(banan))  # Banán zmizne po 5 sekundách
    okno.after(1000, pridaj_banan)  # Pridáva banány každé 3 sekundy

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

def pridaj_jahodu():
    """Pridá novú jahodu na náhodnú pozíciu a nastaví, aby zmizla po 3 sekundách."""
    global jahody
    x = random.randint(50, canvas_width - 50)
    y = random.randint(50, canvas_height - 50)
    jahoda = platno.create_image(x, y, image=obr_jahoda3, anchor="center")
    jahody.append(jahoda)
    okno.after(6000, lambda: zmizni_jahodu(jahoda))
    okno.after(5000, pridaj_jahodu)

def zmizni_jahodu(jahoda):
    """Odstráni jahodu z plátna, ak ešte nebola odstránená."""
    if jahoda in jahody:
        platno.delete(jahoda)
        jahody.remove(jahoda)

def ukaz_vyhercu(vyherna_sprava):
    """Zobrazí správu o výhre a tlačidlo na reštart hry."""
    global restart_button
    platno.create_text(canvas_width // 2, canvas_height // 2, 
                       text=vyherna_sprava, font=("Helvetica", 20), fill="red", tag="vyhra")

    if restart_button is None:
        restart_button = tkinter.Button(okno, text="Začať znova", command=reset_game)
        restart_button.pack()
        
def reset_game():
    """Resetuje hru do počiatočného stavu."""
    global restart_button, mimon_1, mimon_2, banany, jahody, skore_mimon_1, skore_mimon_2, zivoty_mimon_1, zivoty_mimon_2

    platno.delete("all")
    mimon_1 = platno.create_image(100, 300, image=obr_mimon1, anchor="center")
    mimon_2 = platno.create_image(500, 300, image=obr_mimon2, anchor="center")
    banany.clear()
    jahody.clear()
    skore_mimon_1 = 0
    skore_mimon_2 = 0
    zivoty_mimon_1 = 3
    zivoty_mimon_2 = 3
    aktualizuj_skore()
    aktualizuj_zivoty()

    if restart_button is not None:
        restart_button.pack_forget()
        restart_button = None
    

      
# Inicializácia hlavného okna
okno = tkinter.Tk()
okno.title("Mimoni Hra")
pocet_bananov_frame = tkinter.Frame(okno)
pocet_bananov_frame.pack()

tkinter.Label(pocet_bananov_frame, text="Mimoni hra", font=("Arial", 16), fg="blue", bg="yellow").pack()

# Plátno pre hru
platno = tkinter.Canvas(okno, width=canvas_width, height=canvas_height, bg="lightblue")
platno.pack()


# Načítanie obrázkov
obr_mimon1 = tkinter.PhotoImage(file='mimon1.png')
obr_mimon2 = tkinter.PhotoImage(file='mimon2.png')
obr_banan = tkinter.PhotoImage(file='banan.png')
obr_jahoda3 = tkinter.PhotoImage(file='jahoda3.png')

# Pridanie obrázkov na plátno
mimon_1 = platno.create_image(100, 300, image=obr_mimon1, anchor="center")
mimon_2 = platno.create_image(500, 300, image=obr_mimon2, anchor="center")

# Zobrazenie počiatočného skóre a životov
aktualizuj_skore()
aktualizuj_zivoty()

# Bind klávesy na ovládanie
okno.bind("<KeyPress>", on_key_press)
okno.bind("<KeyRelease>", on_key_release)

# Spustenie pohybu a pridávanie banánov
update_positions()
pridaj_banan()
pridaj_jahodu()

# Spustenie hlavnej slučky
okno.mainloop()
