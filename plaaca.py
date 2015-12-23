#!/usr/bin/env python2
# -*- coding: utf-8 -*-

# -------------------------- plaaca ------------------------------------+
#                                                                       |
# Neslužbeni izračun plaće za zaposlenike u osnovnom školstvu, visokom  |
# obrazovanju i znanosti.                                               |
#   Krešimir Kumerički (kkumer@phy.hr)                                  |
#                                                                       |
# Verzija: 2.1  2015-12-23    Nakon 1.1.2015. (neoprorezivo+razredi)    |
# Verzija: 2.0  2014-07-22    Nakon ukidanja kolektivnog ugovora        |
# Verzija: 1.3  2012-03-15    Korekcija poreznih razreda NN 22/12       |
# Verzija: 1.2  2011-07-18    Update za novu definiciju osnovice        |
# Verzija: 1.1  2006-11-13    Update prema KPMG brosuri                 |
# Verzija: 1.0  2004-02-15    Prva verzija                              |
#                                                                       |
# TODO:                                                                 |
#  - dodaci na uzdržavane osobe                                         |
#  - ratni i vojni invalidi etc.                                        |
# ----------------------------------------------------------------------+
                                                                        

# -----------  OSOBNI PARAMETRI  --------------

                  
# Uredba o koeficijentima 
#  ima PDF na http://www.nsz.hr/pravo-i-propisi/dokumenti/
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
KOEFICIJENT = 2.037   # Linić i Milanović umanjili za 3% 2013.
#KOEFICIJENT = 2.5   # Redoviti profesor, znanstveni savjetnik (1. izbor)
#KOEFICI3ENT = 3.05   # Redoviti profesor, znanstveni savjetnik (2. izbor)

STAZ = 21  # godine staža

# Dodatak za znanstveni stupanj:
DOKTORAT = 0.15  # Doktori u znanstveno-nastavnim zvanjima 
                 # trebaju staviti 0.15. Inače 0.

FAKTOR_ODBITKA = 3.2   # Jedno dijete: 1.5     Troje djece: 3.2
                       # Dvoje djece: 2.2      Četvoro djece: 4.6
                       # Petero djece: 6.5
                       # Uzdržavani supružnik (ili alimentacija):
                       #  +0.5 na gornje brojke  (dakle 1.5 ako nema djece)

CLAN_SINDIKATA = 1 # 1=član  0=nečlan

# Prirez:
# Zagreb = 18, Dubrovnik = 15, Varaždin = 10, Karlovac = 12, Osijek = 13,
# Samobor, Stubičke Toplice = 0 ...
# Pogledajte stopu prireza za svoje prebivalište

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
#OSNOVICA = 5557.13 
OSNOVICA =  5679.39   # 2.2% porasta pocevsi od place 01.08.2011. (Zasto ne 2%?)
OSNOVICA =  5810.03   # 2.3% porasta pocevsi od place 01.08.2012.
STARA_OSNOVICA = OSNOVICA
OSNOVICA =  5108.84   # Ujedinjenje osnovica javnih sluzbi od 2011.

PRIJEVOZ = 270.

KOREKCIJA_OSNOVICE = STARA_OSNOVICA/OSNOVICA - 1

DOPRINOSI = 17.2  # Doprinosi na bruto (zdravstvo, ozljede, zaposljavanje etc.)
MIO = 20   # Mirovinsko osiguranje (15% prvi stup i 5% drugi stup)

# porez
STARI_OSNOVNI_ODBITAK = 2200  # još uvijek se koristi za porezne razrede
OSNOVNI_ODBITAK = 2600  # minimalni neoporezivi iznos za područja
                        # koja NISU od posebne državne skrbi
# Za područja posebne državne skrbi treba staviti (čl. 54)
#  prva skupina: 3840
#  druga skupina: 3200
#  treća skupina: 2400

# Stope oporezivanja (čl. 8)
STOPA1 = 12 # do 1X osnovnog odbitka
GRANICA1 = 1 * STARI_OSNOVNI_ODBITAK
STOPA2 = 25 # 1X - 6X
GRANICA2 = 6 * STARI_OSNOVNI_ODBITAK
STOPA3 = 40 # 6X - beskonačno
GRANICA3 = 1000 * OSNOVNI_ODBITAK
HARAC = 0  # harac

SINDIKAT = 1.3


import sys, math

BODOVI = KOEFICIJENT * (1 + STAZ*0.5/100)

fsr =  '{:>35s} = {:9.2f}'
f3sr = '{:>35s} = {:9.3f}'
psr =  '{:>28s} ({:d} %) = {:9.2f}'
isr =  '{:>35s} = {:9d}'
ln  =  50*'-'
lln  =  50*'='

print ln
print fsr.format('Osnovica', OSNOVICA)
print f3sr.format('Koeficijent', KOEFICIJENT)
print isr.format('Staz (god.)', STAZ)

REDOVNIRAD = KOEFICIJENT * OSNOVICA
MINULIRAD = REDOVNIRAD * STAZ * 0.5/100
print fsr.format('Redovni rad (+neradni dani i g.o)', REDOVNIRAD)
print fsr.format('Minuli rad', MINULIRAD)

# Do 2014. je bilo:
#DRKOEF = BODOVI * DOKTORAT * (1+KOREKCIJA_OSNOVICE) 
DRKOEF = BODOVI * DOKTORAT
DR_UVECANJE = DRKOEF * OSNOVICA
print fsr.format('Dodatak za doktorat', DR_UVECANJE)

# Uvećanja
KORKOEF = BODOVI * KOREKCIJA_OSNOVICE
KOR_UVECANJE = KORKOEF * OSNOVICA
print fsr.format('Dodatak po sporazumu', KOR_UVECANJE)



OSTVARENO = REDOVNIRAD + MINULIRAD + DR_UVECANJE + KOR_UVECANJE 

print fsr.format('Bruto', OSTVARENO)
print ln
print fsr.format('Mirovinsko', OSTVARENO*MIO/100.)
DOHODAK = OSTVARENO * (1 - MIO/100.0)
print fsr.format('Dohodak', DOHODAK)


NEOPOREZIVO = OSNOVNI_ODBITAK * FAKTOR_ODBITKA

DOH = DOHODAK - NEOPOREZIVO

if DOH < 0:
    sys.stderr.write("Premala plaća!!\n")
    sys.exit(1)

POREZ2 = 0
POREZ3 = 0
print ln
print fsr.format('Neoporezivi dio', NEOPOREZIVO)
if DOH < GRANICA1:
    POREZ1 = DOH * STOPA1/100.0
    print psr.format('Porez', STOPA1, POREZ1)
else:
    POREZ1 = GRANICA1 * STOPA1/100.0
    print psr.format('Porez', STOPA1, POREZ1)
    if DOH < GRANICA2:
        POREZ2 = (DOH - GRANICA1) * STOPA2/100.0
        print psr.format('Porez', STOPA2, POREZ2)
    else:
        POREZ2 = (GRANICA2 - GRANICA1) * STOPA2/100.0
        print psr.format('Porez', STOPA2, POREZ2)
        if DOH < GRANICA3:
            POREZ3 = (DOH - GRANICA2) * STOPA3/100.0
            print psr.format('Porez', STOPA3, POREZ3)
        else:
            sys.stderr.write('Prevelika plaća!!\n')
            sys.exit(1)

POREZ = POREZ1 + POREZ2 + POREZ3


PRIREZ_IZNOS = POREZ * PRIREZ/100.0

print psr.format('Prirez', PRIREZ, PRIREZ_IZNOS)

POREZ += PRIREZ_IZNOS

print fsr.format('Ukupni porez i prirez', POREZ)
print ln

NETOPRIJE = DOHODAK - POREZ

NETO = NETOPRIJE * (1.- HARAC/100.0)

print fsr.format('Neto', NETO)

#print "Harac = %.2f"  % (NETOPRIJE * HARAC/100.)
print fsr.format('Prijevoz', PRIJEVOZ)

if CLAN_SINDIKATA:
    SINDIKAT_IZNOS = NETO*SINDIKAT/100.0
    print fsr.format('Obustave', SINDIKAT_IZNOS)
    NETO = NETO - SINDIKAT_IZNOS

NETO = NETO + PRIJEVOZ
print lln
print fsr.format('Iznos za isplatu', NETO)
print lln

print fsr.format('Doprinosi na placu', OSTVARENO*DOPRINOSI/100.)
print fsr.format('Ukupan trosak place', OSTVARENO*(1.+DOPRINOSI/100.)+PRIJEVOZ)
print ln

