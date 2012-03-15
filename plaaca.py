#!/usr/bin/env python
# -*- coding: utf-8 -*-

# -------------------------- plaaca ------------------------------------+
#                                                                       |
# Neslužbeni izračun plaće za zaposlenike u osnovnom školstvu, visokom  |
# obrazovanju i znanosti.                                               |
#   Krešimir Kumerički (kkumer@phy.hr)                                  |
#                                                                       |
# Verzija: 1.2  2011-07-18    Update za novu definiciju osnovice        |
# Verzija: 1.1  2006-11-13    Update prema KPMG brosuri                 |
# Verzija: 1.0  2004-02-15    Prva verzija                              |
#                                                                       |
# TODO:                                                                 |
#  - područja posebne državne skrbi                                     |
#  - porez 45% (iznad 21 000 kuna)                                      |
#  - dodaci na uzdržavane osobe                                         |
#  - ratni i vojni invalidi etc.                                        |
#  - otkud tih 1-2 promila razlike prema kadrovskoj službi?             |
# ----------------------------------------------------------------------+
                                                                        

# -----------  OSOBNI PARAMETRI  --------------

                  
# Uredba o koeficijentima 
#  ima PDF na http://www.nsz.hr/propisi-zakoni.php
# Namještenici u javnim službama
#KOEFICIJENT = 0.62   # Radna mjesta IV vrste
#KOEFICIJENT = 0.80   # Radna mjesta III vrste, daktilograf
#KOEFICIJENT = 0.90   # Radna mjesta II vrste
# Radna mjesta I vrste u visokim učilištima i javnim institutima
#KOEFICIJENT = 1.25   # Predavač, dipl. knjižničar, stručni suradnik II
#KOEFICIJENT = 1.30   # Stručni suradnik I
#KOEFICIJENT = 1.45   # Asistent
#KOEFICIJENT = 1.65   # Viši asistent, viši predavač, viši knjižničar
#KOEFICIJENT = 1.9   # Docent, znanstveni suradnik, knjižničarski savjetnik
KOEFICIJENT = 2.1   # Izvanredni profesor, viši znanstveni suradnik
#KOEFICIJENT = 2.5   # Redoviti profesor, znanstveni savjetnik (1. izbor)
#KOEFICI3ENT = 3.05   # Redoviti profesor, znanstveni savjetnik (2. izbor)

STAZ = 18  # godine staža

DOKTORAT = 15  # Od 2004. godine doktori u znanstveno-nastavnim zvanjima 
               # trebaju staviti 15. Inace 0.

FAKTOR_ODBITKA = 2.2   # Jedno dijete: 1.5     Troje djece: 3.2
                       # Dvoje djece: 2.2      Cetvoro djece: 4.6
                       # Uzdržavani supružnik: +0.5

CLAN_SINDIKATA = 1 # 1=član  0=nečlan

# Prirez:
# Zagreb = 18, Dubrovnik = 15, Varaždin = 10, Karlovac = 12, Osijek = 13,
# Samobor, Stubičke Toplice = 0 ...
# Pogledajte stopu prireza za svoje prebivalište
# na adresi http://www.ijf.hr//HPS/gradski.pdf

PRIREZ = 18

# ------------  GLOBALNI PARAMETRI   ---------------------

#OSNOVICA = 4232.43   # za 2003. 
#OSNOVICA = 4414.42   # za 2004. prema novom Kolektivnom ugovoru
#OSNOVICA = 4546.85   # pise na mom obračunskom listiću za 10/2006
#OSNOVICA = 4819.66   # 6% porasta u 01/2007 (nakon strajka)
#OSNOVICA = 4916.05   # 2% porasta pocevsi od place 08/2007
#OSNOVICA = 5211.01   # 6% porasta pocevsi od place 12/2007
#OSNOVICA = 5320.45    # 2% porasta pocevsi od place 01.08.2008.
#OSNOVICA = 5639.67   # 6% porasta pocevsi od place 01.08.2009. (OCEKIVANO)
#OSNOVICA = 5320.45   # famoznih -6% zbog krize, prema sporazumu sa Sindikatima
OSNOVICA = 5557.13 
OSNOVICA =  5679.39   # 2.2% porasta pocevsi od place 01.08.2011. (Zasto ne 2%?)
STARA_OSNOVICA = OSNOVICA
OSNOVICA =  5108.84   # Ujedinjenje osnovica javnih sluzbi od 2011.


KOREKCIJA_OSNOVICE = STARA_OSNOVICA/OSNOVICA - 1

DOPRINOSI = 17.3  # Doprinosi na bruto (zdravstvo etc.)
MIO = 20   # Mirovinsko osiguranje (15% prvi stup i 5% drugi stup)

# porez
OSNOVNI_ODBITAK = 1800  # minimalni neoporezivi iznos za područja
                        # koja NISU od posebne državne skrbi
STOPA1 = 12 # do 2X osnovnog odbitka
GRANICA1 = 2 * OSNOVNI_ODBITAK
STOPA2 = 25 # 2X - 5X
GRANICA2 = 5 * OSNOVNI_ODBITAK
STOPA3 = 35 # 5X - 14X
GRANICA3 = 14 * OSNOVNI_ODBITAK
HARAC = 0  # harac

SINDIKAT = 1.3

# --------------------------------------------------------

import sys, math

print 72*"-"
BODOVI = KOEFICIJENT * (1 + STAZ*0.5/100)
# Zaokruzivanje na tri decimale (na čudan način!)
BODOVI = math.floor(BODOVI*1000.+0.500001)/1000.

print "Osnovica (vrijednost boda) = %.2f" % OSNOVICA
print "Staž = %i godina" % STAZ
print "Broj bodova = %.3f" % BODOVI   # Prije uvećanja

REDOVNIRAD = BODOVI * OSNOVICA
print "Redovni rad MZOS = %.2f" % REDOVNIRAD
# Uvećanja
KORKOEF = BODOVI * KOREKCIJA_OSNOVICE
KOR_UVECANJE = KORKOEF * OSNOVICA
print "Uvecanje = %.2f (%.2f bod.)" % (KOR_UVECANJE, KORKOEF)

DRKOEF = BODOVI * DOKTORAT/100. * (1+KOREKCIJA_OSNOVICE) 
DR_UVECANJE = DRKOEF * OSNOVICA
print "Uvecanje (PhD) = %.2f (%.2f bod)" % (DR_UVECANJE, DRKOEF)


OSTVARENO = REDOVNIRAD + KOR_UVECANJE + DR_UVECANJE 
print "Ostvareni dio = %.2f" % OSTVARENO


DOHODAK = OSTVARENO * (1 - MIO/100.0)
#DOHODAK = OSNOVICA * BODOVI
#DOHODAK = 10542.09

print "Dohodak = %.2f" % DOHODAK

NEOPOREZIVO = OSNOVNI_ODBITAK * FAKTOR_ODBITKA

DOH = DOHODAK - NEOPOREZIVO

if DOH < 0:
    sys.stderr.write("Premala plaća!!\n")
    sys.exit(1)

POREZ2 = 0
POREZ3 = 0
print 30*'-'
print "Neoporezivi dio = %.2f" % NEOPOREZIVO
if DOH < GRANICA1:
    POREZ1 = DOH * STOPA1/100.0
    print "porez (%d %%) = %.2f" % (STOPA1, POREZ1)
else:
    POREZ1 = GRANICA1 * STOPA1/100.0
    print "porez (%d %%) = %.2f" % (STOPA1, POREZ1)
    if DOH < GRANICA2:
        POREZ2 = (DOH - GRANICA1) * STOPA2/100.0
        print "porez (%d %%) = %.2f" % (STOPA2, POREZ2)
    else:
        POREZ2 = (GRANICA2 - GRANICA1) * STOPA2/100.0
        print "porez (%d %%) = %.2f" % (STOPA2, POREZ2)
        if DOH < GRANICA3:
            POREZ3 = (DOH - GRANICA2) * STOPA3/100.0
            print "porez (%d %%) = %.2f" % (STOPA3, POREZ3)
        else:
            sys.stderr.write('Prevelika plaća!!\n')
            sys.exit(1)

POREZ = POREZ1 + POREZ2 + POREZ3

print "Ukupni porez = %.2f"  % POREZ
print 30*'-'

PRIREZ_IZNOS = POREZ * PRIREZ/100.0

print "Prirez = %.2f (%.2f posto)" % (PRIREZ_IZNOS, PRIREZ)

NETOPRIJE = DOHODAK - POREZ - PRIREZ_IZNOS

NETO = NETOPRIJE * (1.- HARAC/100.0)

print "Ukupno primanja = %.2f " % NETO

#print "Harac = %.2f"  % (NETOPRIJE * HARAC/100.)

if CLAN_SINDIKATA:
    SINDIKAT_IZNOS = NETO*SINDIKAT/100.0
    print "Obustave = %.2f" % SINDIKAT_IZNOS
    NETO = NETO - SINDIKAT_IZNOS

print 72*"-"
print "Plaća na tekući račun:   %.2f  HRK"  % NETO
print 72*"-" + '\n'
