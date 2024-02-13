#!/usr/bin/env python
"""Neslužbeni izračun plaće za zaposlenike u obrazovanju i znanosti.

+--------------------------- plaaca ------------------------------------+
|                                                                       |
|                                                                       |
|                                                                       |
| cf. http://www.isplate.info/kalkulator-place-2017.aspx                |
| Verzija: 2.9  2023-01-11    Prelazak na Euro 1. 1. 2023.                          |
| Verzija: 2.8  2022-07-25    Nakon svibnja 2022. (nova osnovica)       |
| Verzija: 2.7  2021-01-14    Nakon 1.1. 2021. (nove stope)             |
| Verzija: 2.6  2019-11-18    Nakon jeseni 2019. (doprinosi)            |
| Verzija: 2.5  2017-02-01    Nakon 1.1.2017. (neoprorezivo+razredi)    |
| Verzija: 2.1  2015-12-23    Nakon 1.1.2015. (neoprorezivo+razredi)    |
| Verzija: 2.0  2014-07-22    Nakon ukidanja kolektivnog ugovora        |
| Verzija: 1.3  2012-03-15    Korekcija poreznih razreda NN 22/12       |
| Verzija: 1.2  2011-07-18    Update za novu definiciju osnovice        |
| Verzija: 1.1  2006-11-13    Update prema KPMG brosuri                 |
| Verzija: 1.0  2004-02-15    Prva verzija                              |
|                                                                       |
| TODO:                                                                 |
|  - dodaci na uzdržavane osobe, invalidnost                            |
|  - područja posebne državne skrbi                                     |
|                                                                       |
| dostupno na: https://github.com/kkumer/plaaca                         |
| autor : Krešimir Kumerički (kkumer@gmail.com)                         |
+-----------------------------------------------------------------------+
"""
# -*- coding: utf-8 -*-


# -----------  OSOBNI PARAMETRI  --------------

# Uredba o koeficijentima
#  ima PDF na http://www.nsz.hr/pravo-i-propisi/dokumenti/
# Namještenici u javnim službama (visoka učilišta i javni instituti)
#  dolje uvijek vrijedi standardna korespondencija docent=zn. suradnik itd.
# ### Položaji I. vrste
# KOEFICIJENT = 3.395   # Dekan iznad 500 zaposlenika
# KOEFICIJENT = 3.201   # Prodekan iznad 500 zaposlenika
# KOEFICIJENT = 3.104   # Pročelnik odsjeka, predstojnik zavoda (20+), red. prof. trajno
# KOEFICIJENT = 2.716   # Pročelnik odsjeka, predstojnik zavoda (20+), red. prof.
# KOEFICIJENT = 2.328   # Pročelnik odsjeka, predstojnik zavoda (20+), izv. prof.
# KOEFICIJENT = 3.055   # Pročelnik odsjeka, predstojnik zavoda (<20), red. prof. trajno
# KOEFICIJENT = 2.619   # Pročelnik odsjeka, predstojnik zavoda (<20), red. prof.
# KOEFICIJENT = 2.231   # Pročelnik odsjeka, predstojnik zavoda (<20), izv. prof.
# KOEFICIJENT = 3.007   # Voditelj laborat, šef katedre, red. prof. trajno
# KOEFICIJENT = 2.570   # Voditelj laborat, šef katedre, red. prof.
# KOEFICIJENT = 2.182   # Voditelj laborat, šef katedre, izv. prof.
# ### Radna mjesta I. vrste u visokim učilištima i javnim institutima
KOEFICIJENT = 2.958   # Red. prof. / zn. savj. - trajno zvanje
# KOEFICIJENT = 2.425   # Red. prof. / zn. savj.
# KOEFICIJENT = 2.037   # Izv. prof. / v. zn. sur.
# KOEFICIJENT = 1.843   # Doc. / zn. sur. / prof. visoke škole
# KOEFICIJENT = 1.843   # Knjižničarski savjetnik
# KOEFICIJENT = 1.6     # Poslijedoktorand, viši predavač, viši knjižničar, struč. savj.
# KOEFICIJENT = 1.406   # Asistent, dipl. knjižničar, viši stručni surad.
# KOEFICIJENT = 1.261   # Stručni surad. u sustavu znanosti
# KOEFICIJENT = 1.358   # Predavač
# ### Radna mjesta II. vrste u visokim učilištima i javnim institutima
# KOEFICIJENT = 1.067   # Viši tehničar, viši laborant
# KOEFICIJENT = 1.018   # Knjižničar
# ### Radna mjesta III. vrste u visokim učilištima i javnim institutima
# KOEFICIJENT = 0.970   # Laborant, tehnički suradnik
# KOEFICIJENT = 0.873   # Pomoćni knjižničar


STAZ = 30  # godine staža

# Dodatak za znanstveni stupanj:
# Doktori u znanstveno-nastavnim zvanjima trebaju staviti 0.15. Inače 0.

DOKTORAT = 0.15

# Faktor odbitka:
# Osnovni: 1.0
# Jedno dijete: 1.5     Dvoje djece: 2.2     Troje djece: 3.2
# Uzdržavani supružnik (ili alimentacija):  +0.5 na gornje brojke
# Za dalje vidi https://www.isplate.info/Osobni-odbitak-2024.aspx

FAKTOR_ODBITKA = 3.2

CLAN_SINDIKATA = 1  # 1=član  0=nečlan

# -- Porezni parametri  --

# Za Zagreb i druga područja koja NISU od posebne državne skrbi:
OSNOVNI_ODBITAK = 560

# Stope oporezivanja za Zagreb
# Za ostale gradove vidi npr. https://isplate.info/porez-na-dohodak-porezne-stope.aspx
STOPA1 = 23.6
GRANICA1 = 4200  # Nisam siguran ni u iznos ni koji je to iznos
STOPA2 = 35.4

# Ima pravo na uvećanje po Sporazumu iz NN122:
NN122 = False

# ------------  GLOBALNI PARAMETRI   ---------------------

OSNOVICA = 947.18   # od listopada 2023.

PRIJEVOZ = 38.49

DOPRINOSI = 16.5  # Doprinosi na bruto (zdravstvo, ozljede, zaposljavanje etc.)
MIO = 20   # Mirovinsko osiguranje (15% prvi stup i 5% drugi stup)


SINDIKAT = 1.3

# -----------  IZRAČUN i PRINTOUT  ------------

import sys

BODOVI = KOEFICIJENT * (1 + STAZ*0.5/100)

fsr = '{:>35s} = {:9.2f}'
f3sr = '{:>35s} = {:9.3f}'
psr = '{:>26s} ({:2.1f} %) = {:9.2f}'
isr = '{:>35s} = {:9d}'
ln = 50*'-'
lln = 50*'='

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
KOR_UVECANJE = BODOVI * OSNOVICA * 13.725/100
print(fsr.format('Dodatak po sporazumu', KOR_UVECANJE))

# Uvećanje po Sporazumu NN122/2019
if NN122:
    KOR_UVECANJE_NN122 = BODOVI * OSNOVICA * 6.11/100
    print(fsr.format('Dodatak po sporazumu NN122', KOR_UVECANJE_NN122))
else:
    KOR_UVECANJE_NN122 = 0


OSTVARENO = REDOVNIRAD + MINULIRAD + DR_UVECANJE + KOR_UVECANJE + KOR_UVECANJE_NN122

print(fsr.format('Bruto', OSTVARENO))
print(ln)
print(fsr.format('Mirovinsko', OSTVARENO*MIO/100.))
DOHODAK = OSTVARENO * (1 - MIO/100.0)
print(fsr.format('Dohodak', DOHODAK))


NEOPOREZIVO = OSNOVNI_ODBITAK * FAKTOR_ODBITKA

DOH = DOHODAK - NEOPOREZIVO

print(ln)
print(fsr.format('Neoporezivi dio', NEOPOREZIVO))
if DOH < 0:
    sys.stderr.write("Cijela plaća je neoporeziva!!\n")
    POREZ = 0.
else:
    POREZ2 = 0.
    print(fsr.format('Osnovica za porez', DOH))
    if DOH < GRANICA1:
        POREZ1 = DOH * STOPA1/100.0
        print(psr.format('Porez', STOPA1, POREZ1))
    else:
        POREZ1 = GRANICA1 * STOPA1/100.0
        print(psr.format('Porez', STOPA1, POREZ1))
        POREZ2 = (DOH - GRANICA1) * STOPA2/100.0
        print(psr.format('Porez', STOPA2, POREZ2))

    POREZ = POREZ1 + POREZ2


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
