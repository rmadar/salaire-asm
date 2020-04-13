# Calculateur de salaire d'Assistante Maternelle

Ce depot contient un programme python capable de calculer le salaire d'une ASM en fonction du contrat et des heures de presence effectuees.

### Specifier le contrat

```python
MaNounou = asm.contrat(

    # Cout horaire
    taux_horaire          = 3.5, 

    # Frais d'entretien (par jour ou par heure)
    frais_entretien       = 3.10,
    entretien_par_jour    = True,

    # Cout des repas
    frais_repas           = 0.0,

    # Nombre d'heures par jour
    n_heures_jour         = 7,

    # Jours de garde dans la semaine
    jours_semaine         = [0, 1, 1, 0, 1, 0, 0], 

    # Nombre de semaines par an (en fonction de ses propres conges)
    n_semaines_an         = 45, 

    # Nombre de mois utilise pour mensualiser
    n_mois_mensualisation = 12
)
```