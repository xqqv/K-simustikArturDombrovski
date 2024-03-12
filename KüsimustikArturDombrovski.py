def loe_kusimused_vastused(failinimi):
    kus_vas = {}
      with open(failinimi, "r", encoding="utf-8") as fail:
        for line in fail:
            n = line.find(":")
            kus_vas[line[:n].strip()] = line[n + 1:].strip()
    return kus_vas

def kirjuta_kusimused_vastused(failinimi, kus_vas):
    with open(failinimi, "w", encoding="utf-8") as fail:
        for kus, vas in kus_vas.items():
            fail.write(f"{kus}:{vas}\n")

def esita_kusimustik(kus_vas, kusitavate_arv):
    oiged_vastused = 0
    kusimustik_edukad = {}
    kusimustik_ebaonnnestunud = {}

    for i in range(kusitavate_arv):
        kus = list(kus_vas.keys())[i]
        oodatud_vastus = kus_vas[kus]

        vastus = input(f"{kus}\nSinu vastus: ").strip()

        if vastus.lower() == oodatud_vastus.lower():
            print("Õige!\n")
            oiged_vastused += 1
        else:
            print(f"Vale! Õige vastus on: {oodatud_vastus}\n")

        if i == kusitavate_arv - 1:
            print("Küsimustik läbi!")

    if oiged_vastused > kusitavate_arv // 2:
        kusimustik_edukad = {"Küsitletu": oiged_vastused}
    else:
        kusimustik_ebaonnnestunud = {"Küsitletu": oiged_vastused}

    return kusimustik_edukad, kusimustik_ebaonnnestunud

def kuvada_nimekirjad(edukad, ebaonnnestunud):
    if edukad:
        print("\nEdukalt läbinud:")
        for nimi, oiged in sorted(edukad.items()):
            print(f"{nimi}: {oiged} õiget vastust")
    if ebaonnnestunud:
        print("\nEbaõnnestunud:")
        for nimi, oiged in sorted(ebaonnnestunud.items()):
            print(f"{nimi}: {oiged} õiget vastust")

if __name__ == "__main__":
    failinimi = "kusimused_vastused.txt"
    kus_vas = loe_kusimused_vastused(failinimi)

    kusitavate_arv = int(input("Mitu küsimust soovid esitada? "))

    edukad, ebaonnnestunud = esita_kusimustik(kus_vas, kusitavate_arv)

    kirjuta_kusimused_vastused("oiged.txt", edukad)
    kirjuta_kusimused_vastused("valed.txt", ebaonnnestunud)

    kuvada_nimekirjad(edukad, ebaonnnestunud)

