# Calculateur de salaire d'Assistante Maternel

Calcul du salaire d'une assitante maternelle en fonction des heures de presence et du contrat

```python
MaNounou = asm.contrat(
    taux_horaire          = 3.5, 
    frais_entretien       = 3.10,
    entretien_par_jour    = True,
    frais_repas           = 0.0,
    n_heures_jour         = 7,
    jours_semaine         = [0, 1, 1, 0, 1, 0, 0], 
    n_semaines_an         = 45, 
    n_mois_mensualisation = 12
)


```