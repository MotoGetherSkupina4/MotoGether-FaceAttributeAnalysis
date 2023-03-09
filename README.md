# MotoGether-FaceAttributeAnalysis
> Analiza profilnih slik za pridobitev različnih podatkov o uporabnikih

Primarne tehnologije:
- *DeepFace* knjižnica za analizo
- *Gkt* knjižnica za vmesnik (in *Glade* orodje za generiranje)

---

## GUI program

Zaganjanje GUI programa:
```
$ python3 app.py
```

![Example](./assets/Example_001.png)

Primerno za demonstracijo storitve.

---

## CLI program

> Program je namenjen za uporabo kot ločena storitev v Dokerju

Še v obdelavi ...

---

## Iskanje prijateljev

> Algoritem omogoča iskanje prijateljstev preko klasičnih parametrov iz baze (ime, priimek) kot tudi analize slike (starost, spol, izražena čustva, ...). Išče čim več podobnosti, katere pa imajo različen vpliv na izbiro prijateljev.

### Uporabljene uteži za prijateljstva:
- starost
- spol
- etnična skupina
- izražena čustva na sliki
