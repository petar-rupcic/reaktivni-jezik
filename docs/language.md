# ReactiveLang - opis jezika

ReactiveLang je mali reaktivni programski jezik.

Podržane naredbe:

## Obična varijabla

let a = 10

## Reaktivna varijabla

reactive b = a * 2

## Promjena vrijednosti

set a = 20

## Ispis

print b

## Vanjski izvor podataka

source temperature

## Emitiranje nove vrijednosti izvora

emit temperature = 35

## Ispis ovisnosti

dependencies b

## Objašnjenje izračuna

trace b

# Primjer

let a = 10
reactive b = a * 2
print b
set a = 20
print b