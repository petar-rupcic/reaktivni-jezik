# Reaktivni jezik - dokumentacija jezika

Ovaj projekt implementira mali reaktivni programski jezik. Ideja jezika je omogućiti definiranje običnih varijabli, reaktivnih varijabli i jednostavnih vanjskih izvora podataka. Reaktivne varijable ovise o drugim varijablama i automatski se ponovno računaju kada se promijeni neka vrijednost o kojoj ovise.

Jezik je napravljen kao projekt iz PIP-a i uključuje lekser, parser, AST strukturu, semantičku analizu, interpreter i kompajler u Svelte.

---

## Osnovna ideja

U običnom programskom jeziku izraz se najčešće izračuna samo u trenutku kada se naredba izvrši. U ovom jeziku reaktivna varijabla pamti izraz iz kojeg je definirana.

Primjer:

```reactive
let a = 10
reactive b = a * 2

print b
set a = 20
print b
```

Očekivani ispis:

```text
20
40
```

Varijabla `b` ovisi o varijabli `a`. Kada se vrijednost `a` promijeni, `b` se ponovno izračunava.

---

## Tipovi podataka

Jezik trenutno podržava tri osnovna tipa podataka.

### Brojevi

```reactive
let a = 10
let price = 99.99
```

Brojevi se koriste u aritmetičkim izrazima.

### Stringovi

```reactive
let name = "Ana"
print name
```

Stringovi se zapisuju unutar dvostrukih navodnika.

### Boolean vrijednosti

```reactive
let active = true
let valid = false
```

Boolean vrijednosti koriste se za logičke izraze i rezultate usporedbi.

---

## Operatori

Podržani su osnovni aritmetički i usporedbeni operatori.

Aritmetički operatori:

| Operator | Značenje |
|---|---|
| `+` | zbrajanje |
| `-` | oduzimanje |
| `*` | množenje |
| `/` | dijeljenje |

Usporedbeni operatori:

| Operator | Značenje |
|---|---|
| `>` | veće od |
| `<` | manje od |
| `>=` | veće ili jednako |
| `<=` | manje ili jednako |
| `==` | jednako |
| `!=` | različito |

Primjer:

```reactive
let temperature = 35
reactive warning = temperature > 30
print warning
```

---

## Naredbe jezika

Jezik podržava sljedeće naredbe:

```text
let
reactive
set
print
source
emit
dependencies
trace
```

---

## Naredba `let`

Naredba `let` definira običnu varijablu.

Sintaksa:

```reactive
let ime = izraz
```

Primjer:

```reactive
let a = 10
let price = 100
let name = "Ana"
```

Vrijednost obične varijable može se kasnije promijeniti naredbom `set`.

---

## Naredba `reactive`

Naredba `reactive` definira reaktivnu varijablu.

Sintaksa:

```reactive
reactive ime = izraz
```

Primjer:

```reactive
let price = 100
let quantity = 3
reactive total = price * quantity
print total
```

Reaktivna varijabla se ponovno računa kada se promijeni neka od varijabli o kojima ovisi.

Primjer:

```reactive
let a = 10
reactive b = a * 2

print b
set a = 20
print b
```

Očekivani ispis:

```text
20
40
```

---

## Naredba `set`

Naredba `set` mijenja vrijednost postojeće varijable.

Sintaksa:

```reactive
set ime = izraz
```

Primjer:

```reactive
let a = 10
reactive b = a * 2

set a = 20
print b
```

Nakon promjene vrijednosti `a`, ponovno se računaju sve reaktivne varijable koje ovise o `a`.

---

## Naredba `print`

Naredba `print` ispisuje vrijednost izraza.

Sintaksa:

```reactive
print izraz
```

Primjer:

```reactive
let a = 10
print a
print a + 5
```

---

## Naredbe `source` i `emit`

Naredba `source` definira vanjski izvor podataka, a naredba `emit` simulira dolazak nove vrijednosti iz tog izvora.

Sintaksa:

```reactive
source ime
emit ime = izraz
```

Primjer:

```reactive
source temperature
reactive warning = temperature > 30

emit temperature = 25
print warning

emit temperature = 35
print warning
```

Očekivani ispis:

```text
false
true
```

Ovim se simulira ponašanje sustava koji reagira na vanjske događaje, primjerice poruke, senzore, promjene u bazi podataka ili druge izvore podataka.

---

## Naredba `dependencies`

Naredba `dependencies` ispisuje o kojim varijablama ovisi neka reaktivna varijabla.

Sintaksa:

```reactive
dependencies ime
```

Primjer:

```reactive
let price = 100
let quantity = 3
reactive total = price * quantity

dependencies total
```

Očekivani ispis:

```text
total depends on: price, quantity
```

Ova naredba služi za prikaz grafa ovisnosti i jedna je od glavnih dodatnih mogućnosti jezika.

---

## Naredba `trace`

Naredba `trace` prikazuje kako je dobivena vrijednost reaktivne varijable.

Sintaksa:

```reactive
trace ime
```

Primjer:

```reactive
let price = 100
let quantity = 3
reactive total = price * quantity

trace total
```

Primjer očekivanog ispisa:

```text
total = price * quantity
price = 100
quantity = 3
total = 300
```

Na ovaj način jezik ne prikazuje samo konačnu vrijednost, nego i objašnjava izračun.

---

## Gramatika jezika

Pojednostavljena gramatika jezika je:

```text
program ::= statement*

statement ::= letStmt
            | reactiveStmt
            | setStmt
            | printStmt
            | sourceStmt
            | emitStmt
            | dependenciesStmt
            | traceStmt

letStmt ::= "let" IDENT "=" expression

reactiveStmt ::= "reactive" IDENT "=" expression

setStmt ::= "set" IDENT "=" expression

printStmt ::= "print" expression

sourceStmt ::= "source" IDENT

emitStmt ::= "emit" IDENT "=" expression

dependenciesStmt ::= "dependencies" IDENT

traceStmt ::= "trace" IDENT

expression ::= comparison

comparison ::= addition ((">" | "<" | ">=" | "<=" | "==" | "!=") addition)?

addition ::= multiplication (("+" | "-") multiplication)*

multiplication ::= primary (("*" | "/") primary)*

primary ::= NUMBER
          | STRING
          | BOOLEAN
          | IDENT
          | "(" expression ")"
```

---

## Prioritet operatora

Parser poštuje uobičajeni prioritet operatora.

Redoslijed je:

```text
1. zagrade
2. množenje i dijeljenje
3. zbrajanje i oduzimanje
4. usporedbe
```

Primjer:

```reactive
let x = 2 + 3 * 4
print x
```

Rezultat je:

```text
14
```

Izraz se računa kao:

```text
2 + (3 * 4)
```

Ako želimo promijeniti redoslijed računanja, koristimo zagrade:

```reactive
let x = (2 + 3) * 4
print x
```

Rezultat je:

```text
20
```

---

## AST

Parser iz izvornog koda gradi AST, odnosno apstraktno sintaksno stablo. AST je unutarnji prikaz programa koji zatim koriste semantički analizator, interpreter, optimizator i kompajler.

Primjer programa:

```reactive
let a = 10
reactive b = a * 2
print b
```

može se prikazati ovako:

```text
Program
 ├── LetStatement
 │    ├── name: a
 │    └── expression: NumberLiteral(10)
 │
 ├── ReactiveStatement
 │    ├── name: b
 │    └── expression: BinaryExpression
 │         ├── left: VariableExpression(a)
 │         ├── operator: *
 │         └── right: NumberLiteral(2)
 │
 └── PrintStatement
      └── expression: VariableExpression(b)
```

Opći tijek obrade programa je:

```text
izvorni kod -> lekser -> parser -> AST -> semantička analiza -> interpreter ili kompajler
```

---

## Primjer s lancem ovisnosti

```reactive
let a = 10
reactive b = a * 2
reactive c = b + a

print c

set a = 20
print c

dependencies c
trace c
```

Očekivani ispis:

```text
30
60
```

Objašnjenje:

```text
a = 10
b = 20
c = 30

nakon set a = 20:

b = 40
c = 60
```

---

## Prednost u odnosu na Svelte

Svelte podržava reaktivne deklaracije pomoću oznake `$:`. Na primjer:

```svelte
<script>
  let a = 10;
  $: b = a * 2;
</script>
```

Naš jezik također podržava reaktivnost, ali dodatno omogućuje objašnjavanje reaktivnosti pomoću naredbi `dependencies` i `trace`.

Primjer:

```reactive
let a = 10
reactive b = a * 2

dependencies b
trace b
```

Time se može vidjeti o kojim varijablama neka vrijednost ovisi i kako je izračunata. Zbog toga jezik nije samo reaktivan, nego omogućuje i pregledniji uvid u graf ovisnosti.