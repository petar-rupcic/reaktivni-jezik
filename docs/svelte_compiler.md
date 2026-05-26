# Kompajler u Svelte

Ovaj dio projekta prevodi program napisan u reaktivnom jeziku u Svelte komponentu.

Kompajler ne izvršava program, nego iz AST-a generira tekstualni Svelte kod. Drugim riječima, nakon što lekser i parser obrade ulazni program, dobiveni AST može se predati kompajleru koji ga pretvara u `.svelte` datoteku.

---

## Uloga kompajlera

Ulaz u kompajler je AST programa.

Izlaz iz kompajlera je Svelte komponenta.

Opći tijek je:

```text
izvorni kod -> lekser -> parser -> AST -> Svelte kompajler -> .svelte datoteka
```

Primjer ulaza u reaktivnom jeziku:

```reactive
let price = 100
let quantity = 3
reactive total = price * quantity
print total
```

Primjer generiranog Svelte koda:

```svelte
<script>
  let price = 100;
  let quantity = 3;

  $: total = price * quantity;
</script>

<p>{total}</p>
```

---

## Prevođenje naredbe `let`

Naredba `let` u reaktivnom jeziku definira običnu varijablu.

Primjer:

```reactive
let a = 10
```

prevodi se u Svelte kao:

```svelte
let a = 10;
```

Ako imamo više običnih varijabli:

```reactive
let price = 100
let quantity = 3
```

dobivamo:

```svelte
let price = 100;
let quantity = 3;
```

---

## Prevođenje naredbe `reactive`

Naredba `reactive` definira reaktivnu varijablu.

Primjer:

```reactive
reactive total = price * quantity
```

prevodi se u Svelte reaktivnu deklaraciju:

```svelte
$: total = price * quantity;
```

Svelte koristi oznaku `$:` za reaktivne izraze. To znači da će se izraz ponovno izračunati kada se promijeni neka vrijednost o kojoj ovisi.

Zato se naredba iz našeg jezika:

```reactive
reactive b = a * 2
```

može prirodno prevesti u:

```svelte
$: b = a * 2;
```

---

## Prevođenje naredbe `print`

Naredba `print` u našem jeziku označava ispis izraza.

Primjer:

```reactive
print total
```

u Svelteu se prevodi u HTML prikaz:

```svelte
<p>{total}</p>
```

Ako se ispisuje izraz:

```reactive
print price + quantity
```

može se prevesti kao:

```svelte
<p>{price + quantity}</p>
```

---

## Prevođenje izraza

Kompajler mora znati prevesti izraze koji se nalaze u naredbama `let`, `reactive`, `set`, `emit` i `print`.

Primjeri izraza:

```reactive
a + b
price * quantity
temperature > 30
(a + b) * 2
```

U većini slučajeva izrazi se u Svelte mogu prevesti gotovo izravno jer naš jezik koristi operatore koji postoje i u JavaScriptu.

Primjer:

```reactive
reactive warning = temperature > 30
```

prevodi se u:

```svelte
$: warning = temperature > 30;
```

---

## Prevođenje naredbe `set`

Naredba `set` mijenja vrijednost postojeće varijable.

Primjer:

```reactive
set a = 20
```

U Svelteu se takva promjena može prikazati kao obična dodjela vrijednosti:

```svelte
a = 20;
```

Ako se želi prikazati kroz korisničko sučelje, moguće je generirati funkciju ili gumb koji mijenja vrijednost.

Primjer moguće generiranog koda:

```svelte
<button on:click={() => a = 20}>Set a = 20</button>
```

U osnovnoj verziji kompajlera dovoljno je da se `set` prevede kao promjena vrijednosti u skriptnom dijelu ili kao jednostavan gumb za demonstraciju.

---

## Prevođenje `source` i `emit`

Naredba `source` označava vanjski izvor podataka.

Primjer:

```reactive
source temperature
```

U Svelteu se može prevesti kao obična varijabla:

```svelte
let temperature;
```

Naredba `emit` simulira dolazak nove vrijednosti iz vanjskog izvora.

Primjer:

```reactive
emit temperature = 35
```

može se prevesti kao promjena vrijednosti:

```svelte
temperature = 35;
```

ili kao gumb za demonstraciju:

```svelte
<button on:click={() => temperature = 35}>Emit temperature = 35</button>
```

Na taj način se u Svelte komponenti može pokazati kako promjena vanjskog izvora automatski utječe na reaktivne izraze.

---

## Prevođenje `dependencies` i `trace`

Naredbe `dependencies` i `trace` prvenstveno pripadaju interpreteru jer služe za objašnjavanje izvođenja programa.

U Svelte kompajleru mogu se preskočiti ili prikazati kao komentar u generiranom kodu.

Primjer:

```reactive
dependencies total
trace total
```

mogu se prevesti kao:

```svelte
<!-- dependencies total -->
<!-- trace total -->
```

Time se zadržava informacija da su naredbe postojale u izvornom programu, ali se stvarna analiza ovisnosti i objašnjenje izračuna izvode u interpreteru.

---

## Primjer cijelog prijevoda

Ulazni program:

```reactive
let a = 10
reactive b = a * 2
print b

set a = 20
print b
```

Mogući generirani Svelte kod:

```svelte
<script>
  let a = 10;

  $: b = a * 2;

  function update_a() {
    a = 20;
  }
</script>

<p>{b}</p>

<button on:click={update_a}>Set a = 20</button>

<p>{b}</p>
```

Ovaj primjer pokazuje kako se reaktivnost iz našeg jezika prevodi u Svelteovu reaktivnost pomoću oznake `$:`.

---

## Ograničenja kompajlera

Kompajler je namijenjen za demonstraciju prijevoda osnovnih konstrukata jezika u Svelte. Ne pokušava pokriti sve mogućnosti Svelte frameworka.

Trenutno je cilj podržati:

```text
let -> obična Svelte varijabla
reactive -> Svelte reaktivna deklaracija $:
print -> HTML prikaz izraza
set -> promjena vrijednosti ili gumb
source -> varijabla koja predstavlja vanjski izvor
emit -> simulirana promjena vrijednosti izvora
```

Naredbe `dependencies` i `trace` ostaju primarno dio interpretera jer se odnose na objašnjenje grafa ovisnosti i izračuna.

---

## Zaključak

Svelte kompajler pokazuje da se program napisan u reaktivnom jeziku može prevesti u postojeći reaktivni okvir.

Najvažnije prevođenje je:

```reactive
reactive ime = izraz
```

u:

```svelte
$: ime = izraz;
```

Na taj način se osnovna ideja našeg jezika povezuje sa Svelteovim mehanizmom reaktivnosti.