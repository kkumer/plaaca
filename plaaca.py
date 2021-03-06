#!/usr/bin/env python
# -*- coding: utf-8 -*-

# -------------------------- plaaca ------------------------------------+
#                                                                       |
# Neslužbeni izračun plaće za zaposlenike u osnovnom školstvu, visokom  |
# obrazovanju i znanosti.                                               |
#   Krešimir Kumerički (kkumer@gmail.com)                               |
#                                                                       |
# cf. http://www.isplate.info/kalkulator-place-2017.aspx                |
# Verzija: 2.6  2019-11-18    Nakon jeseni 2019. (doprinosi)            |
# Verzija: 2.5  2017-02-01    Nakon 1.1.2017. (neoprorezivo+razredi)    |
# Verzija: 2.1  2015-12-23    Nakon 1.1.2015. (neoprorezivo+razredi)    |
# Verzija: 2.0  2014-07-22    Nakon ukidanja kolektivnog ugovora        |
# Verzija: 1.3  2012-03-15    Korekcija poreznih razreda NN 22/12       |
# Verzija: 1.2  2011-07-18    Update za novu definiciju osnovice        |
# Verzija: 1.1  2006-11-13    Update prema KPMG brosuri                 |
# Verzija: 1.0  2004-02-15    Prva verzija                              |
#                                                                       |
# TODO:                                                                 |
#  - dodaci na uzdržavane osobe, invalidnost                            |
# ----------------------------------------------------------------------+
                                                                        

# -----------  OSOBNI PARAMETRI  --------------

                  
# Uredba o koeficijentima 
#  ima PDF na http://www.nsz.hr/pravo-i-propisi/dokumenti/
# Namještenici u javnim službama (visoka učilišta i javni instituti)
#  dolje uvijek vrijedi standardna korespondencija docent=zn. suradnik itd.
#### Položaji I. vrste
#KOEFICIJENT = 3.395   # Dekan iznad 500 zaposlenika
#KOEFICIJENT = 3.201   # Prodekan iznad 500 zaposlenika
#KOEFICIJENT = 3.104   # Pročelnik odsjeka, predstojnik zavoda (20+), red. prof. trajno
#KOEFICIJENT = 2.716   # Pročelnik odsjeka, predstojnik zavoda (20+), red. prof. 
#KOEFICIJENT = 2.328   # Pročelnik odsjeka, predstojnik zavoda (20+), izv. prof. 
#KOEFICIJENT = 3.055   # Pročelnik odsjeka, predstojnik zavoda (<20), red. prof. trajno
#KOEFICIJENT = 2.619   # Pročelnik odsjeka, predstojnik zavoda (<20), red. prof. 
#KOEFICIJENT = 2.231   # Pročelnik odsjeka, predstojnik zavoda (<20), izv. prof. 
#KOEFICIJENT = 3.007   # Voditelj laborat, šef katedre, red. prof. trajno
#KOEFICIJENT = 2.570   # Voditelj laborat, šef katedre, red. prof.
#KOEFICIJENT = 2.182   # Voditelj laborat, šef katedre, izv. prof.
#### Radna mjesta I. vrste u visokim učilištima i javnim institutima
#KOEFICIJENT = 2.958   # Red. prof. / zn. savj. - trajno zvanje
KOEFICIJENT = 2.425   # Red. prof. / zn. savj.
#KOEFICIJENT = 2.037   # Izv. prof. / v. zn. sur.
#KOEFICIJENT = 1.843   # Doc. / zn. sur. / prof. visoke škole
#KOEFICIJENT = 1.843   # Knjižničarski savjetnik
#KOEFICIJENT = 1.6     # Poslijedoktorand, viši predavač, viši knjižničar, stručni savj.
#KOEFICIJENT = 1.406   # Asistent, dipl. knjižničar, viši stručni surad.
#KOEFICIJENT = 1.261   # Stručni surad. u sustavu znanosti
#KOEFICIJENT = 1.358   # Predavač
#### Radna mjesta II. vrste u visokim učilištima i javnim institutima
#KOEFICIJENT = 1.067   # Viši tehničar, viši laborant
#KOEFICIJENT = 1.018   # Knjižničar
#### Radna mjesta III. vrste u visokim učilištima i javnim institutima
#KOEFICIJENT = 0.970   # Laborant, tehnički suradnik
#KOEFICIJENT = 0.873   # Pomoćni knjižničar


STAZ = 26  # godine staža

# Dodatak za znanstveni stupanj:
DOKTORAT = 0.15  # Doktori u znanstveno-nastavnim zvanjima 
                 # trebaju staviti 0.15. Inače 0.

FAKTOR_ODBITKA = 3.1   # Jedno dijete: 0.7     Troje djece: 3.1
                       # Dvoje djece: 1.7      Četvoro djece: 5.0
                       # Uzdržavani supružnik (ili alimentacija):
                       #  +0.7 na gornje brojke 

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
OSNOVICA =  5108.84   # Ujedinjenje osnovica javnih sluzbi od 2011.
OSNOVICA =  5211.02   # Nova osnovica 1.1.2017. (odluka Vlade RH)
OSNOVICA =  5421.54   # Nova osnovica oko kraja 2017.
OSNOVICA =  5584.19   # Nova osnovica od 2019. (novi kolektivni)
OSNOVICA =  5695.87   # Nova osnovica od jeseni (?) 2019. 
OSNOVICA =  5809.79   # Nova osnovica od kraja 2019.

PRIJEVOZ = 290.

DOPRINOSI = 16.5  # Doprinosi na bruto (zdravstvo, ozljede, zaposljavanje etc.)
MIO = 20   # Mirovinsko osiguranje (15% prvi stup i 5% drugi stup)

# porez
OSNOVICA_ZA_ODBITAK = 2500
OSNOVNI_ODBITAK = 4000  # minimalni neoporezivi iznos za područja
                        # koja NISU od posebne državne skrbi
# FIXME: da li se ovo mijenjalo 2017?
# Za područja posebne državne skrbi treba staviti (čl. 54)
#  prva skupina: 3840
#  druga skupina: 3200
#  treća skupina: 2400

# Stope oporezivanja
#STOPA1 = 24 
STOPA1 = 20 # nakon 1.1.2021.
GRANICA1 = 17500.
#STOPA2 = 36 
STOPA2 = 30 # nakon 1.1.2021

SINDIKAT = 1.3


import math
import sys

BODOVI = KOEFICIJENT * (1 + STAZ*0.5/100)

fsr =  '{:>35s} = {:9.2f}'
f3sr = '{:>35s} = {:9.3f}'
psr =  '{:>28s} ({:d} %) = {:9.2f}'
isr =  '{:>35s} = {:9d}'
ln  =  50*'-'
lln  =  50*'='

print(ln)
print(fsr.format('Osnovica', OSNOVICA))
print(f3sr.format('Koeficijent', KOEFICIJENT))
print(isr.format('Staz (god.)', STAZ))

REDOVNIRAD = KOEFICIJENT * OSNOVICA
MINULIRAD = REDOVNIRAD * STAZ * 0.5/100
# Ako se se nakon 25/31 dana povecava staz:
# MINULIRAD = REDOVNIRAD * (STAZ*25/31.+(STAZ+1)*6/31.) * 0.5/100
print(fsr.format('Redovni rad (+neradni dani i g.o)', REDOVNIRAD))
print(fsr.format('Minuli rad', MINULIRAD))

# Do 2014. je bilo:
DRKOEF = BODOVI * DOKTORAT
DR_UVECANJE = DRKOEF * OSNOVICA
print(fsr.format('Dodatak za doktorat', DR_UVECANJE))

# Uvećanje po Sporazumu o dodacima iz studenog 2006.
KOR_UVECANJE =  BODOVI * OSNOVICA * 13.725/100
print(fsr.format('Dodatak po sporazumu', KOR_UVECANJE))


OSTVARENO = REDOVNIRAD + MINULIRAD + DR_UVECANJE + KOR_UVECANJE 

print(fsr.format('Bruto', OSTVARENO))
print(ln)
print(fsr.format('Mirovinsko', OSTVARENO*MIO/100.))
DOHODAK = OSTVARENO * (1 - MIO/100.0)
print(fsr.format('Dohodak', DOHODAK))


NEOPOREZIVO = OSNOVNI_ODBITAK + OSNOVICA_ZA_ODBITAK * FAKTOR_ODBITKA

DOH = DOHODAK - NEOPOREZIVO

print(ln)
print(fsr.format('Neoporezivi dio', NEOPOREZIVO))
if DOH < 0:
    sys.stderr.write("Cijela plaća je neoporeziva!!\n")
    POREZ = 0
else:
    POREZ2 = 0
    POREZ3 = 0
    if DOH < GRANICA1:
        POREZ1 = DOH * STOPA1/100.0
        print(psr.format('Porez', STOPA1, POREZ1))
    else:
        POREZ1 = GRANICA1 * STOPA1/100.0
        print(psr.format('Porez', STOPA1, POREZ1))
        POREZ2 = (DOH - GRANICA1) * STOPA2/100.0
        print(psr.format('Porez', STOPA2, POREZ2))

    POREZ = POREZ1 + POREZ2


PRIREZ_IZNOS = POREZ * PRIREZ/100.0

print(psr.format('Prirez', PRIREZ, PRIREZ_IZNOS))

POREZ += PRIREZ_IZNOS

print(fsr.format('Ukupni porez i prirez', POREZ))
print(ln)

NETO = DOHODAK - POREZ

print(fsr.format('Neto', NETO))

print(fsr.format('Prijevoz', PRIJEVOZ))

if CLAN_SINDIKATA:
    SINDIKAT_IZNOS = NETO*SINDIKAT/100.0
    print(fsr.format('Obustave', SINDIKAT_IZNOS))
    NETO = NETO - SINDIKAT_IZNOS

NETO = NETO + PRIJEVOZ
print(lln)
print(fsr.format('Iznos za isplatu', NETO))
print(lln)

print(fsr.format('Doprinosi na placu', OSTVARENO*DOPRINOSI/100.))
print(fsr.format('Ukupan trosak place', OSTVARENO*(1.+DOPRINOSI/100.)+PRIJEVOZ))
print(ln)

