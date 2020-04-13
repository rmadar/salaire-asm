import asm

ChristineD = asm.contrat(
    taux_horaire = 3.5, 
    frais_entretient = 3.10, 
    frais_repas = 0.0,
    n_heures_jour = 7,
    n_jours_semaine = 3, 
    n_semaines_an = 45, 
    n_mois_mensualisation = 12
)
print(ChristineD.cout_mensualise())
print(ChristineD.conges_payes_annuel(), ChristineD.conges_payes_mensualises())
