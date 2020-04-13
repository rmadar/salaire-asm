# Calculateur de salaire d'Assistante Maternelle

Ce depot contient un programme python capable de calculer le salaire d'une ASM en fonction du contrat et des heures de presence effectuees.

### Specifier le contrat

```python
MaNounou = asm.contrat(

    # Cout horaire net
    taux_horaire = 3.5, 

    # Frais d'entretien (par jour ou par heure)
    frais_entretien = 3.10,
    entretien_par_jour = True,

    # Cout des repas
    frais_repas = 0.0,

    # Nombre d'heures par jour
    n_heures_jour = 7,

    # Jours de garde dans la semaine
    jours_semaine = [0, 1, 1, 0, 1, 0, 0], 

    # Nombre de semaines par an (en fonction de ses propres conges)
    n_semaines_an = 45, 

    # Nombre de mois utilise pour mensualiser
    n_mois_mensualisation = 12
)
```

Le calcul du cout mensualise ou encore des conges payes est ensuite fait en interne:
```python
salaire_mensuel = MaNounou.cout_mensualise()
conges_payes_mois = MaNounou.conges_payes_mensualises()
```

```
Cout mensuel        : 310.50 Euros
Conges payes mensuel: 61.25 Euros
```

### Specifier une periode

```python
avril = asm.donnees_presence(date_debut = '20-04-01',
                             date_fin = '20-04-30',
                             heures_effectuees_par_jours = [10]*13,
                             repas_pris_par_jours = [False]*13)
```

Un appel de la fonction `nounou.cout_reel_periode(avril)` donne directement:

```
Avril (2 semaines incompletes et 3 completes):
  - 5 jours de fin de semaine
  - 3x7 jours de semaines completes
  - 4 jours de debut de semaine
  - cout reel Avril si (sur)presence: 495.30 Euros
```