import smtplib
import ssl
from email.message import EmailMessage
from email.mime.image import MIMEImage

def loe_küsimused_vastused(failinimi):
    küs_vas = {}
    with open(failinimi, "r", encoding="utf-8") as fail:
        for line in fail:
            n = line.find(":")
            küs_vas[line[:n].strip()] = line[n + 1:].strip()
    return küs_vas

def kirjuta_küsimused_vastused(failinimi, küs_vas):
    with open(failinimi, "w", encoding="utf-8") as fail:
        for küs, vas in küs_vas.items():
            fail.write(f"{küs}:{vas}\n")

def esita_küsimustik(küs_vas, küsitavate_arv):
    õiged_vastused = 0
    küsimustik_edukad = {}
    küsimustik_ebaõnnestunud = {}

    for i in range(küsitavate_arv):
        küs = list(küs_vas.keys())[i]
        oodatud_vastus = küs_vas[küs]

        vastus = input(f"{küs}\nSinu vastus: ").strip()

        if vastus.lower() == oodatud_vastus.lower():
            print("Õige!\n")
            õiged_vastused += 1
        else:
            print(f"Vale! Õige vastus on: {oodatud_vastus}\n")

        if i == küsitavate_arv - 1:
            print("Viktoriin lõppenud!")

    if õiged_vastused > küsitavate_arv // 2:
        küsimustik_edukad["Edukalt läbitud"] = õiged_vastused
    else:
        küsimustik_ebaõnnestunud["Edukalt läbitud"] = õiged_vastused

    return küsimustik_edukad, küsimustik_ebaõnnestunud

def kuvada_nimekirjad(edukad, ebaõnnestunud):
    if edukad:
        print("\nEdukalt läbitud:")
        for nimi, õiged in sorted(edukad.items()):
            print(f"{nimi}: {õiged} õiget vastust")
    if ebaõnnestunud:
        print("\nEbaõnnestunud:")
        for nimi, õiged in sorted(ebaõnnestunud.items()):
            print(f"{nimi}: {õiged} õiget vastust")

def saada_email(points_earned):
    smtp_server = "smtp.gmail.com"
    port = 587
    saatja_email = "arturdombrovski94@gmail.com"
    parool = input("Sisestage oma parool: ")
    saaja_email = "marina.oleinik@tthk.ee"

    context = ssl.create_default_context()
    msg = EmailMessage()
    msg.set_content(f"Tere! See on testi tulemused. Teie tulemus: {points_earned} punkti.")
    msg["Subject"] = "Test"
    msg["From"] = "Artur Dombrovski"                #rxci awqn lcxs yvzu
    msg["To"] = saaja_email
    
    with open("kartonka.jpg", "rb") as fpilt:
        img_data = fpilt.read()

    img_part = MIMEImage(img_data, name="kartonka.jpg")
    msg.add_attachment(img_part)

    try:
        server = smtplib.SMTP(smtp_server, port)
        server.starttls(context=context)
        server.login(saatja_email, parool)
        server.send_message(msg)
        print("E-kiri saadetud edukalt!")
    except Exception as e:
        print(f"Viga e-kirja saatmisel: {e}")
    finally:
        server.quit()

if __name__ == "__main__":
    failinimi = "küsimused_vastused.txt"
    küs_vas = loe_küsimused_vastused(failinimi)

    küsitavate_arv = int(input("Mitu küsimust soovite esitada? "))

    edukad, ebaõnnestunud = esita_küsimustik(küs_vas, küsitavate_arv)

    kirjuta_küsimused_vastused("õiged1.txt", edukad)
    kirjuta_küsimused_vastused("valed1.txt", ebaõnnestunud)

    kuvada_nimekirjad(edukad, ebaõnnestunud) 

    saada_email(sum(edukad.values()))  
