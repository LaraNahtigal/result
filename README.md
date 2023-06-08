# result

## Opis projekta:
V datoteki app.py lahko najdete preprosto stateless aplikacijo, s katero lahko pridobivate, dodajate in brišete objekte iz podatkovne baze.
V podatkovni bazi se v tabelah users, comments, todos in posts nahajajo podatki iz spletne strani https://jsonplaceholder.typicode.com/.

## Zaganjanje projekta:
Aplikacijo je mogoče zagnati s pomočjo Docker-ja. V bash terminalu morate uporabiti komando:
- docker compose up -d postgres
- docker compose build
- docker compose up app
Za uporabo funkcij, ki jih nudi aplikacija, potrebujete API platformo kot je naprimer **POSTMAN**.

## Funkcije: 
Aplikacija vam omogoča več funkcij:
- kreirati nov post z dodajanjem naslova, bodyja in user-ja s komando ('POST') *http://localhost:5004/kreiraj-post/<title>/<'body'>/<user_id>*
- izbisati post glede na njegov id s komando ('DELETE') *http://localhost:5004/brisanje-posta/<id_posta>*
- spreminjane že obstoječega posta s komando ('POST') *http://localhost:5004/posodabljanje-posta/<id_posta>/<title>/<body>*, kjer napišemo nov title in body
- pridobivanje vseh obstoječih post-ov s komando ('GET') *http://localhost:5004/posti*
- pridobivanje vseh obstoječih komentarjev s komando ('GET') *http://localhost:5004/komentarji*
- pridobivanje vseh obstoječih uporabnikov s komando ('GET') *http://localhost:5004/userji*
- pridobivanje vseh obstoječih todos-ov s komando ('GET') *http://localhost:5004/todosi*
- pridobivanje vseh post-ov enega userja glede na user-jev id s komando ('GET') *http://localhost:5004/pridobi-poste-userja/<id_userja:int>*
- pridobivanje posta z vsemi njegovimi komentarji s komando ('GET') *http://localhost:5004/pridobi-poste/<id_posta:int>*
- pridobivanje specifičnih komentarjev glede na id posta s komando ('GET') *http://localhost:5004/specificni-komentarji/<zeljen_id>*
V okvirčke *< >* morate vnesti željeno številko ali besedilo. 

