import pygame
import random


# CERINTA 1: OBIECTELE JOCULUI
# Aici sunt create obiectele care apar pe ecran:
# bara, bila, caramizile si proiectilele.

# Creeaza obiectul bara si stabileste viteza cu care se misca
class Bara:
    def __init__(self):
        # pygame.Rect tine minte pozitia si dimensiunea barei
        # 395 si 590 sunt coordonatele de pornire(x,y)
        # 110 este latimea, iar 16 este inaltimea barei
        self.dreptunghi = pygame.Rect(395, 590, 110, 16)

        # viteza arata cu cati pixeli se muta bara la fiecare cadru
        self.viteza = 10

    # Deseneaza bara pe ecran
    def deseneaza(self, ecran, culoare):
        pygame.draw.rect(ecran, culoare, self.dreptunghi)


# Creeaza obiectul bila, cu pozitie, raza si viteza
class Bila:
    def __init__(self):
        # x si y reprezinta centrul bilei pe ecran
        self.x = 450
        self.y = 570

        # raza stabileste marimea bilei
        self.raza = 8

        # viteza_x misca bila stanga-dreapta
        # viteza_y misca bila sus-jos
        self.viteza_x = 4
        # valoarea negativa inseamna ca bila porneste in sus
        self.viteza_y = -4

    # Creeaza un dreptunghi invizibil in jurul bilei, folosit pentru coliziuni
    def dreptunghi_minge(self):
        return pygame.Rect(
            # coltul din stanga sus al dreptunghiului bilei
            int(self.x - self.raza),
            int(self.y - self.raza),

            # latimea si inaltimea sunt diametrul bilei
            self.raza * 2,
            self.raza * 2 #diametrul este de doua ori raza
        )

    # Deseneaza bila pe ecran
    def deseneaza(self, ecran, culoare):
        #(suprafata,culoare,centru,raza)
        pygame.draw.circle(ecran, culoare, (int(self.x), int(self.y)), self.raza)


# Creeaza o caramida cu pozitie, dimensiune si tip
class Caramida:
    def __init__(self, x, y, latime, inaltime, tip):
        # fiecare caramida este un dreptunghi cu pozitie si dimensiune
        self.dreptunghi = pygame.Rect(x, y, latime, inaltime)

        # tipul decide culoarea si comportamentul caramizii
        # poate fi: gri, orange, maro sau verde
        self.tip = tip

    def deseneaza(self, ecran, culori):
        # umple caramida cu culoarea potrivita tipului ei
        pygame.draw.rect(ecran, culoare_caramida(self.tip, culori), self.dreptunghi)

        # deseneaza o margine neagra ca sa se vada fiecare caramida de grosime 2 pixeli
        pygame.draw.rect(ecran, culori["negru"], self.dreptunghi, 2)


# Creeaza un proiectil care porneste din bara
class Proiectil:
    def __init__(self, x, y):
        # proiectilul este un dreptunghi mic, deasupra barei
        self.dreptunghi = pygame.Rect(x, y, 6, 16)

        # viteza proiectilului este separata de viteza bilei
        self.viteza = 9

    def deseneaza(self, ecran, culoare):
        pygame.draw.rect(ecran, culoare, self.dreptunghi)


# CERINTA 2: CULORILE CARAMIZILOR
# Gri nu se distruge, orange se sparge, maro devine orange,
# iar verde ofera bonus.
# Returneaza culoarea potrivita pentru fiecare tip de caramida
def culoare_caramida(tip, culori):
    # verificam tipul primit si returnam culoarea potrivita
    if tip == "gri":
        return culori["gri"]
    if tip == "orange":
        return culori["orange"]
    if tip == "maro":
        return culori["maro"]

    # daca nu este gri, orange sau maro, ramane verde
    return culori["verde"]


# CERINTA 3: CLASA PRINCIPALA A JOCULUI
# Aici se afla toate setarile jocului, harta, scorul,
# nivelurile, miscarea, coliziunile, bonusurile si desenarea.
class Joc:
    def __init__(self):
        # porneste modulele pygame pentru fereastra si desenare
        pygame.init()

        # dimensiunea ferestrei jocului
        self.latime = 900
        self.inaltime = 650

        # fereastra principala de latimea si inaltimea ferestrei in pixeli
        # va salva o suprafata pe care poti desena
        self.ecran = pygame.display.set_mode((self.latime, self.inaltime))
        #punem titlul ferestrei
        pygame.display.set_caption("Break-It")

        # ceasul controleaza numarul de FPS-uri
        self.ceas = pygame.time.Clock()

        # fonturile sunt folosite pentru scor, nivel, mesaje si final de joc
        self.font = pygame.font.SysFont("arial", 24)
        self.font_mare = pygame.font.SysFont("arial", 46)

        # dictionar cu toate culorile folosite in joc
        # fiecare culoare este scrisa in format RGB
        self.culori = {
            "negru": (0, 0, 0),
            "alb": (255, 255, 255),
            "rosu": (255, 0, 0),
            "verde": (0, 255, 0),
            "albastru": (0, 0, 255),
            "gri": (140, 140, 140),
            "orange": (255, 140, 0),
            "maro": (125, 70, 30),
            "galben": (255, 220, 70)
        }

        # limitele chenarului in care se misca bila si bara
        self.stanga = 55
        self.dreapta = 845
        self.sus = 90
        self.jos = 625

        # dimensiunile caramizilor si spatiul dintre ele
        self.latime_caramida = 82
        self.inaltime_caramida = 26
        self.spatiu = 14

        # nivelul curent, numarul total de nivele si scorul
        self.nivel = 1
        self.numar_nivele = 3
        self.scor = 0

        #jucatorul incepe jocul cu 3 vieti
        self.vieti = 3

        # dupa ce am setat valorile principale, creez obiectele jocului
        self.resetare()

    # CERINTA: harta proprie de caramizi
    # Fiecare nivel este o matrice de texte.
    # Fiecare text reprezinta tipul unei caramizi.
    def harta_nivelului(self):
        # daca suntem la nivelul 1, returnam harta pentru nivelul 1
        if self.nivel == 1:
            return [
                ["gri", "orange", "maro", "verde", "orange", "maro", "gri", "orange"],
                ["orange", "maro", "orange", "gri", "verde", "orange", "maro", "orange"],
                ["maro", "orange", "verde", "orange", "maro", "gri", "orange", "verde"],
                ["orange", "gri", "orange", "maro", "orange", "verde", "orange", "maro"]
            ]

        # daca suntem la nivelul 2, returnam harta pentru nivelul 2
        if self.nivel == 2:
            return [
                ["verde", "maro", "orange", "gri", "orange", "maro", "verde", "orange"],
                ["maro", "orange", "maro", "orange", "gri", "orange", "maro", "verde"],
                ["orange", "gri", "verde", "maro", "orange", "verde", "gri", "orange"],
                ["maro", "orange", "orange", "verde", "maro", "orange", "maro", "orange"],
                ["verde", "maro", "gri", "orange", "verde", "maro", "orange", "gri"]
            ]

        # daca nu este nivelul 1 sau 2, ramane harta pentru nivelul 3
        return [
            ["verde", "maro", "verde", "orange", "gri", "orange", "verde", "maro"],
            ["maro", "orange", "maro", "verde", "orange", "maro", "orange", "verde"],
            ["orange", "gri", "verde", "maro", "gri", "verde", "maro", "orange"],
            ["verde", "orange", "maro", "orange", "verde", "orange", "maro", "verde"],
            ["maro", "verde", "orange", "gri", "orange", "verde", "orange", "maro"]
        ]

    # Aici se creeaza caramizile in functie de nivel.
    # caramizile vor avea: pozitie, dimensiune si tip
    def creeaza_caramizi(self):
        # pastram caramizile create pentru nivelul curent
        lista_caramizi_noua = []

        # luam harta nivelului curent
        harta = self.harta_nivelului()

        # i reprezinta randul, iar j reprezinta coloana
        for i in range(len(harta)):
            for j in range(len(harta[i])):
                # calculam pozitia fiecarei caramizi pe ecran
                # 73 si 130 sunt pozitiile de inceput ale primei caramizi
                x = 73 + j * (self.latime_caramida + self.spatiu)
                y = 130 + i * (self.inaltime_caramida + self.spatiu)

                # cream caramida cu pozitie, dimensiune si tipul din harta
                caramida = Caramida(x, y, self.latime_caramida, self.inaltime_caramida, harta[i][j])
                lista_caramizi_noua.append(caramida)

        # returnam lista cu toate caramizile nivelului
        return lista_caramizi_noua

    
    # CERINTA: resetarea jocului
    # Se foloseste la inceput, dupa pierderea jocului sau la nivel nou.
    def resetare(self):
        # cream din nou bara si bila
        self.bara = Bara()
        self.minge = Bila()

        # cream caramizile pentru nivelul curent
        self.caramizi = self.creeaza_caramizi()

        # nu exista proiectile pe ecran
        self.proiectile = []

        # starile jocului se pun pe False la inceput de nivel
        self.pauza = False
        self.game_over = False
        self.castigat_nivel = False
        self.joc_terminat = False

        # la inceputul fiecarui nivel, bila sta pe bara
        # si porneste doar cand apasam Space
        self.minge_pornita = False

        # viteza jocului revine la normal la fiecare nivel
        self.viteza_joc = 1

        # bonusurile si proiectilele se reseteaza
        self.proiectile_ramase = 0
        self.timp_bara_mare = 0
        self.timp_exploziv = 0
        self.mesaj_bonus = ""

    # resetarea totala este folosita cand apasam R dupa finalul jocului
    def resetare_totala(self):
        self.nivel = 1
        self.scor = 0

        # refacem si vietile
        self.vieti = 3

        self.resetare()

    # CERINTA: miscarea barei
    # Bara se misca stanga-dreapta si nu poate iesi din chenar.
    def limiteaza_bara(self):
        # daca bara trece de marginea din stanga, o punem inapoi in chenar
        if self.bara.dreptunghi.left < self.stanga:
            self.bara.dreptunghi.left = self.stanga

        # daca bara trece de marginea din dreapta, o punem inapoi in chenar
        if self.bara.dreptunghi.right > self.dreapta:
            self.bara.dreptunghi.right = self.dreapta

    def misca_bara(self):
        # get_pressed verifica tastele care sunt tinute apasate
        taste = pygame.key.get_pressed()

        # daca apas sageata stanga, mut bara spre stanga
        if taste[pygame.K_LEFT]:
            # scad din axa x, deoarece x mai mic inseamna miscare spre stanga
            self.bara.dreptunghi.x -= self.bara.viteza

        # daca apas sageata dreapta, mut bara spre dreapta
        if taste[pygame.K_RIGHT]:
            # adaug la axa x, deoarece x mai mare inseamna miscare spre dreapta
            self.bara.dreptunghi.x += self.bara.viteza

        # dupa miscare verific sa nu iasa bara din chenar
        self.limiteaza_bara()

    # CERINTA: miscarea bilei si coliziunile cu chenarul
    # Bila se misca permanent dupa ce apasam Space.
    def misca_mingea(self):
        # daca bila nu a pornit, ea sta deasupra barei
        if not self.minge_pornita:
            #bila va sta pe centru
            self.minge.x = self.bara.dreptunghi.centerx
            self.minge.y = self.bara.dreptunghi.top - self.minge.raza
            return

        # modificam pozitia bilei in functie de viteza ei
        # viteza_joc poate mari sau micsora viteza generala a bilei
        self.minge.x += self.minge.viteza_x * self.viteza_joc
        self.minge.y += self.minge.viteza_y * self.viteza_joc

        # daca bila atinge peretele din stanga, o trimitem spre dreapta
        if self.minge.x - self.minge.raza <= self.stanga:
            self.minge.x = self.stanga + self.minge.raza
            self.minge.viteza_x = abs(self.minge.viteza_x)

        # daca bila atinge peretele din dreapta, o trimitem spre stanga
        if self.minge.x + self.minge.raza >= self.dreapta:
            self.minge.x = self.dreapta - self.minge.raza
            self.minge.viteza_x = -abs(self.minge.viteza_x)

        # daca bila atinge partea de sus, o trimitem in jos
        if self.minge.y - self.minge.raza <= self.sus:
            self.minge.y = self.sus + self.minge.raza
            self.minge.viteza_y = abs(self.minge.viteza_y)


    # CERINTA: coliziuni cu bara si caramizile
    # Bila ricoseaza cand loveste bara sau o caramida.
    def verifica_lovire_bara(self):
        # verificam daca dreptunghiul bilei se intersecteaza cu dreptunghiul barei
        # viteza_y > 0 inseamna ca bila vine de sus in jos
        #colliderect verifica daca doua dreptunghiuri se suprapun
        if self.minge.dreptunghi_minge().colliderect(self.bara.dreptunghi) and self.minge.viteza_y > 0:
            # schimbam directia bilei pe verticala, ca sa mearga inapoi in sus
            self.minge.viteza_y = -abs(self.minge.viteza_y)

            # punem bila exact deasupra barei ca sa nu ramana blocata in bara
            self.minge.y = self.bara.dreptunghi.top - self.minge.raza

            # calculam unde a lovit bila bara
            # daca loveste in centru, diferenta este aproape 0
            # daca loveste spre margini, bila pleaca mai mult in lateral
            diferenta = (self.minge.x - self.bara.dreptunghi.centerx) / (self.bara.dreptunghi.width / 2)
            self.minge.viteza_x = diferenta * 5

    # functie care sa ricoseze cand loveste din caramida
    def ricoseaza_din_caramida(self, caramida):
        raza = self.minge.raza

        # transformam bila intr-un dreptunghi pentru a verifica mai usor coliziunea
        minge = self.minge.dreptunghi_minge()

        # calculam cat de mult se suprapune bila cu fiecare parte a caramizii
        loveste_stanga = minge.right - caramida.dreptunghi.left
        loveste_dreapta = caramida.dreptunghi.right - minge.left
        loveste_sus = minge.bottom - caramida.dreptunghi.top
        loveste_jos = caramida.dreptunghi.bottom - minge.top

        # partea cu suprapunerea cea mai mica este partea din care a venit bila
        minim = min(loveste_dreapta, loveste_stanga, loveste_jos, loveste_sus)

        #inversam viteza pe X daca loveste stanga sau dreapta
        if minim == loveste_stanga:
            self.minge.viteza_x = -abs(self.minge.viteza_x)
            self.minge.x = caramida.dreptunghi.left - raza

        elif minim == loveste_dreapta:
            self.minge.viteza_x = abs(self.minge.viteza_x)
            self.minge.x = caramida.dreptunghi.right + raza

        #inverseaza viteza pe Y daca loveste sus sau jos
        elif minim == loveste_sus:
            self.minge.viteza_y = -abs(self.minge.viteza_y)
            self.minge.y = caramida.dreptunghi.top - raza

        else:
            self.minge.viteza_y = abs(self.minge.viteza_y)
            self.minge.y = caramida.dreptunghi.bottom + raza

    # distrugerea caramizilor la explozie
    def explodeaza(self, caramida_lovita):
        # luam centrul caramizii lovite, ca sa stim de unde porneste explozia
        x, y = caramida_lovita.dreptunghi.center

        # aici pastram doar caramizile care nu sunt distruse
        caramizi_ramase = []

        for caramida in self.caramizi:
            # centrul caramizii verificate
            cx, cy = caramida.dreptunghi.center

            # calculam distanta pe orizontala fata de caramida lovita
            distanta_x = abs(cx - x)
            distanta_permisa_x = self.latime_caramida + self.spatiu

            if distanta_x <= distanta_permisa_x:
                aproape_x = True
            else:
                aproape_x = False

            # calculam distanta pe verticala fata de caramida lovita
            distanta_y = abs(cy - y)
            distanta_permisa_y = self.inaltime_caramida + self.spatiu

            if distanta_y <= distanta_permisa_y:
                aproape_y = True
            else:
                aproape_y = False

            # daca o caramida este aproape si nu este gri, explozia o distruge
            if aproape_x and aproape_y and caramida.tip != "gri":
                self.scor += 10
            else:
                # caramizile gri sau cele prea indepartate raman in joc
                caramizi_ramase.append(caramida)

        # inlocuim lista veche cu lista caramizilor ramase
        self.caramizi = caramizi_ramase

    # Distruge caramida lovita de proiectil si activeaza bonus daca este verde
    def loveste_cu_proiectil(self, caramida):
        # daca proiectilul loveste o caramida verde, se activeaza bonusul
        if caramida.tip == "verde":
            self.activeaza_bonus()

        # scoatem caramida lovita din lista si crestem scorul
        self.caramizi.remove(caramida)
        self.scor += 10

    def lanseaza_proiectil(self):
        # daca nu mai avem proiectile disponibile, nu putem trage
        if self.proiectile_ramase <= 0:
            return

        # nu lansam proiectile cand jocul este oprit sau terminat
        if self.pauza:
            return

        if self.game_over:
            return

        if self.castigat_nivel:
            return

        if self.joc_terminat:
            return

        # in varianta aceasta permitem un singur proiectil pe ecran
        if len(self.proiectile) > 0:
            return

        # proiectilul porneste din centrul barei
        x = self.bara.dreptunghi.centerx - 3
        y = self.bara.dreptunghi.top - 16

        # cream proiectilul, il adaugam in lista si scadem numarul ramas
        proiectil = Proiectil(x, y)
        self.proiectile.append(proiectil)
        self.proiectile_ramase -= 1

    def misca_proiectile(self):
        # aici pastram doar proiectilele care mai raman pe ecran
        proiectile_ramase = []

        for proiectil in self.proiectile:
            # proiectilul merge in sus, deci scadem din coordonata y
            proiectil.dreptunghi.y -= proiectil.viteza
            caramida_lovita = None

            # verificam proiectilul doar cat timp se afla in interiorul chenarului
            if proiectil.dreptunghi.bottom >= self.sus:
                # cautam daca proiectilul a lovit o caramida
                for caramida in self.caramizi:
                    if proiectil.dreptunghi.colliderect(caramida.dreptunghi):
                        caramida_lovita = caramida
                        break

                # daca nu a lovit nimic, proiectilul continua sa existe
                if caramida_lovita is None:
                    proiectile_ramase.append(proiectil)
                else:
                    # daca a lovit o caramida, aplicam efectul si proiectilul dispare
                    self.loveste_cu_proiectil(caramida_lovita)

        # actualizam lista proiectilelor ramase
        self.proiectile = proiectile_ramase

    # CERINTA: caramizile verzi ofera bonusuri:
    # bara dubla, bila exploziva sau 5 proiectile.
    def activeaza_bonus(self):
        # alegem aleator unul dintre cele 3 bonusuri
        bonus = random.randint(1, 3)

        if bonus == 1:
            # salvam centrul barei ca sa ramana in acelasi loc dupa marire
            centru = self.bara.dreptunghi.centerx
            self.bara.dreptunghi.width = 220
            self.bara.dreptunghi.centerx = centru

            # 600 de cadre inseamna aproximativ 10 secunde la 60 FPS
            self.timp_bara_mare = 600
            self.mesaj_bonus = "Bonus: bara dubla"

            # verificam sa nu iasa bara marita din chenar
            self.limiteaza_bara()

        elif bonus == 2:
            # bila exploziva ramane activa pentru 600 de cadre
            self.timp_exploziv = 600
            self.mesaj_bonus = "Bonus: bila exploziva"

        else:
            # jucatorul primeste 5 proiectile pe care le poate lansa cu F
            self.proiectile_ramase += 5
            self.mesaj_bonus = "Bonus: 5 proiectile"

    def loveste_caramida(self, caramida):
        # mai intai bila trebuie sa ricoseze din caramida
        self.ricoseaza_din_caramida(caramida)

        # caramizile gri sunt obstacole, deci nu se distrug cu bila
        if caramida.tip == "gri":
            return

        # daca bonusul exploziv este activ, se distrug mai multe caramizi apropiate
        if self.timp_exploziv > 0:
            # daca lovim o caramida verde, bonusul se activeaza si inainte de explozie
            if caramida.tip == "verde":
                self.activeaza_bonus()

            self.explodeaza(caramida)
            return

        # caramida portocalie se sparge direct si creste scorul
        if caramida.tip == "orange":
            self.caramizi.remove(caramida)
            self.scor += 10

        # caramida maro nu se sparge din prima, ci devine portocalie
        elif caramida.tip == "maro":
            caramida.tip = "orange"
            self.scor += 5

        # caramida verde se sparge si activeaza un bonus
        elif caramida.tip == "verde":
            self.caramizi.remove(caramida)
            self.scor += 15
            self.activeaza_bonus()

    def verifica_lovire_caramizi(self):
        # la inceput presupunem ca nu a fost lovita nicio caramida
        caramida_lovita = None

        # cautam prima caramida care se intersecteaza cu bila
        for caramida in self.caramizi:
            if self.minge.dreptunghi_minge().colliderect(caramida.dreptunghi):
                caramida_lovita = caramida
                break

        # daca am gasit o caramida lovita, aplicam efectul ei
        if caramida_lovita is not None:
            self.loveste_caramida(caramida_lovita)

    def actualizeaza_bonusuri(self):
        # daca bonusul de bara mare este activ, scadem timpul ramas
        if self.timp_bara_mare > 0:
            self.timp_bara_mare -= 1

            # cand bonusul e 0, bara revine la marimea normala
            if self.timp_bara_mare == 0:
                #ii salvam centrul pentru a nu-l pierde cand micsoram bara
                centru = self.bara.dreptunghi.centerx
                #miscoram latimea barei
                self.bara.dreptunghi.width = 110
                #punem centrul barei unde era si inainte
                self.bara.dreptunghi.centerx = centru
                self.limiteaza_bara()

        # daca bonusul exploziv este activ, scadem timpul ramas
        if self.timp_exploziv > 0:
            self.timp_exploziv -= 1

    # CERINTA: tastele jocului
    # Space porneste/opreste jocul, + si - modifica viteza,
    # F lanseaza proiectile, R reseteaza, N trece la nivelul urmator.

    # Verifica tastele apasate: pauza, viteza, proiectil, restart, nivel urmator
    def verifica_evenimente(self):
        # ruleaza ramane True cat timp nu inchidem fereastra
        ruleaza = True

        # pygame.event.get() citeste toate evenimentele produse de utilizator
        for event in pygame.event.get():

            # daca apasam X la fereastra, jocul se opreste
            if event.type == pygame.QUIT:
                ruleaza = False

            # KEYDOWN inseamna ca o tasta a fost apasata o singura data
            if event.type == pygame.KEYDOWN:
                #KEYDOWN, obiectul event are atribute precum;
                # key=iti spune ce eveniment s-a intamplat exact
                # mod
                # unicode=verifica simboluri ale tastaturii
                # scancode
                if event.key == pygame.K_SPACE and not self.game_over and not self.castigat_nivel and not self.joc_terminat:
                    # daca bila nu a pornit, Space porneste bila
                    if not self.minge_pornita:
                        self.minge_pornita = True
                    else:
                        # daca bila este deja pornita, Space pune pauza sau reia jocul
                        self.pauza = not self.pauza

                # tasta + mareste viteza jocului, dar nu trece peste 2.2
                if event.unicode == "+" or event.key == pygame.K_KP_PLUS:
                    self.viteza_joc += 0.2
                    self.viteza_joc = min(self.viteza_joc, 2.2)

                # tasta - micsoreaza viteza jocului, dar nu scade sub 0.4
                if event.key == pygame.K_MINUS or event.key == pygame.K_KP_MINUS:
                    self.viteza_joc -= 0.2
                    self.viteza_joc = max(self.viteza_joc, 0.4)

                # tasta F lanseaza un proiectil, daca avem proiectile ramase
                if event.key == pygame.K_f:
                    self.lanseaza_proiectil()

                # dupa castigarea nivelului, tasta N trece la nivelul urmator
                if event.key == pygame.K_n and self.castigat_nivel:
                    self.nivel += 1
                    self.resetare()

                # dupa game over sau finalul jocului, R reseteaza tot jocul
                if event.key == pygame.K_r and (self.game_over or self.joc_terminat):
                    self.resetare_totala()

        # returnam daca jocul trebuie sa continue sau nu
        return ruleaza

    # CERINTA: final de nivel si final de joc
    # Castigi nivelul cand nu mai exista caramizi care pot fi sparte.
    # Pierzi cand bila cade si nu mai ai vieti.

    def a_castigat_nivelul(self):
        # daca mai exista o caramida care nu este gri, nivelul nu este terminat
        for caramida in self.caramizi:
            if caramida.tip != "gri":
                return False

        # daca au ramas doar caramizile gri, nivelul este castigat
        return True

    def verifica_final_joc(self):
        if self.minge.y - self.minge.raza > self.bara.dreptunghi.bottom:
            # cand bila cade, jucatorul pierde o viata
            self.vieti -= 1

            # daca mai are vieti, bila este pusa inapoi pe bara
            if self.vieti > 0:
                self.bara = Bara()
                self.minge = Bila()
                self.minge_pornita = False
                self.proiectile = []
                self.timp_bara_mare = 0
                self.timp_exploziv = 0
                self.mesaj_bonus = ""
                return

            # daca nu mai are vieti, jocul se termina
            self.game_over = True
            return

        # verificam daca toate caramizile care se pot sparge au disparut
        if self.a_castigat_nivelul():
            # daca mai exista nivele, afisam mesajul de nivel castigat
            if self.nivel < self.numar_nivele:
                self.castigat_nivel = True
            else:
                # daca era ultimul nivel, jocul este castigat complet
                self.joc_terminat = True

    # CERINTA: actualizarea jocului
    # apelarea miscarilor, coliziunilor si verificarilor.

    def actualizeaza_joc(self):
        # ordinea este importanta: mai intai miscam obiectele, apoi verificam loviturile
        self.misca_bara()
        self.misca_mingea()

        # verificam daca bila a lovit bara sau caramizile
        self.verifica_lovire_bara()
        self.verifica_lovire_caramizi()

        # actualizam proiectilele si bonusurile
        self.misca_proiectile()
        self.actualizeaza_bonusuri()

        # la final verificam daca s-a pierdut o viata sau s-a castigat nivelul
        self.verifica_final_joc()

    def deseneaza_text(self):
        # cream textele care apar sus pe ecran
        text_scor = self.font.render("Scor: " + str(self.scor), True, self.culori["alb"])
        text_nivel = self.font.render("Nivel: " + str(self.nivel), True, self.culori["alb"])
        text_viteza = self.font.render("Viteza: " + str(round(self.viteza_joc, 1)), True, self.culori["alb"])
        text_proiectile = self.font.render("Proiectile: " + str(self.proiectile_ramase), True, self.culori["alb"])

        # blit pune textul pe ecran la coordonatele date
        self.ecran.blit(text_scor, (45, 18))
        self.ecran.blit(text_nivel, (180, 18))
        self.ecran.blit(text_viteza, (315, 18))
        self.ecran.blit(text_proiectile, (465, 18))

        # afisam vietile ramase
        text_vieti = self.font.render("Vieti: " + str(self.vieti), True, self.culori["alb"])
        self.ecran.blit(text_vieti, (680, 18))

        if self.mesaj_bonus != "":
            text_bonus = self.font.render(self.mesaj_bonus, True, self.culori["galben"])
            self.ecran.blit(text_bonus, (45, 52))

        # mesaj afisat cand bila asteapta sa fie pornita
        if not self.minge_pornita and not self.game_over and not self.castigat_nivel and not self.joc_terminat:
            text = self.font.render("Apasa SPACE pentru start", True, self.culori["alb"])
            self.ecran.blit(text, (self.latime // 2 - text.get_width() // 2, 540))

        if self.pauza:
            text = self.font_mare.render("PAUZA", True, self.culori["alb"])
            self.ecran.blit(text, (self.latime // 2 - text.get_width() // 2, 260))

        if self.castigat_nivel:
            text = self.font_mare.render("AI CASTIGAT NIVELUL " + str(self.nivel), True, self.culori["alb"])
            text2 = self.font.render("Apasa N pentru nivelul urmator", True, self.culori["alb"])
            self.ecran.blit(text, (self.latime // 2 - text.get_width() // 2, 250))
            self.ecran.blit(text2, (self.latime // 2 - text2.get_width() // 2, 315))

        if self.joc_terminat:
            text = self.font_mare.render("AI CASTIGAT JOCUL!", True, self.culori["alb"])
            text2 = self.font.render("Apasa R pentru restart", True, self.culori["alb"])
            text3 = self.font.render("Scor final: " + str(self.scor), True, self.culori["alb"])
            self.ecran.blit(text, (self.latime // 2 - text.get_width() // 2, 250))
            self.ecran.blit(text2, (self.latime // 2 - text2.get_width() // 2, 315))
            self.ecran.blit(text3, (self.latime // 2 - text3.get_width() // 2, 350))

        if self.game_over:
            text = self.font_mare.render("JOC TERMINAT", True, self.culori["alb"])
            text2 = self.font.render("Apasa R pentru restart", True, self.culori["alb"])
            text3 = self.font.render("Scor final: " + str(self.scor), True, self.culori["alb"])
            self.ecran.blit(text, (self.latime // 2 - text.get_width() // 2, 250))
            self.ecran.blit(text2, (self.latime // 2 - text2.get_width() // 2, 315))
            self.ecran.blit(text3, (self.latime // 2 - text3.get_width() // 2, 350))

    # CERINTA: desenarea scenei
    # chenarul gri incomplet jos, caramizile,
    # bara, bila, proiectilele, scorul si mesajele.

    def deseneaza_joc(self):
        # stergem ecranul la fiecare cadru, ca sa nu ramana urme
        self.ecran.fill(self.culori["negru"])

        # desenam chenarul jocului: sus, stanga si dreapta
        # jos nu desenam linie, pentru ca bila trebuie sa poata cadea
        pygame.draw.line(self.ecran, self.culori["gri"], (self.stanga, self.sus), (self.dreapta, self.sus), 5)
        pygame.draw.line(self.ecran, self.culori["gri"], (self.stanga, self.sus), (self.stanga, self.jos), 5)
        pygame.draw.line(self.ecran, self.culori["gri"], (self.dreapta, self.sus), (self.dreapta, self.jos), 5)

        # desenam toate caramizile ramase
        for caramida in self.caramizi:
            caramida.deseneaza(self.ecran, self.culori)

        # desenam bara si bila
        self.bara.deseneaza(self.ecran, self.culori["alb"])
        self.minge.deseneaza(self.ecran, self.culori["alb"])

        # desenam proiectilele active
        for proiectil in self.proiectile:
            proiectil.deseneaza(self.ecran, self.culori["galben"])

        # la final desenam textele peste scena
        self.deseneaza_text()


    # CERINTA: bucla principala

    def porneste(self):
        # ruleaza controleaza daca bucla principala continua sau se opreste
        ruleaza = True

        while ruleaza:
            # jocul ruleaza cu aproximativ 60 de cadre pe secunda
            self.ceas.tick(60)

            # verificam evenimentele: taste, inchiderea ferestrei etc.
            ruleaza = self.verifica_evenimente()

            # actualizam jocul doar daca nu este pauza sau final
            if not self.pauza and not self.game_over and not self.castigat_nivel and not self.joc_terminat:
                self.actualizeaza_joc()

            # desenam tot ce apare pe ecran
            self.deseneaza_joc()

            # actualizam fereastra ca modificarile sa fie vizibile
            pygame.display.update()

        # inchidem pygame dupa iesirea din bucla
        pygame.quit()

def main():
    # cream un obiect de tip Joc
    joc = Joc()

    # pornim bucla principala a jocului
    joc.porneste()

# aceasta conditie porneste jocul doar cand fisierul este rulat direct
if __name__ == "__main__":
    main()