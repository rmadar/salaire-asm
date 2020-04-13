import asm

# Test de la classe 'contrat'
ChristineD = asm.contrat(
    taux_horaire = 3.5, 
    frais_entretient = 3.10, 
    frais_repas = 0.0,
    n_heures_jour = 7,
    n_jours_semaine = 3, 
    n_semaines_an = 45, 
    n_mois_mensualisation = 12
)
print('Cout mensuel        : {:.2f} Euros'.format(ChristineD.cout_mensualise()))
print('Conges payes mensuel: {:.2f} Euros'.format(ChristineD.conges_payes_mensualises()))

avril = {
    'n_jours_prevus': 13, 
    'donnees_presence': [[0, False]]*13
}
print('Cout reel Avril: {:.2f} Euros'.format(ChristineD.cout_reel_periode(**avril)))


# Test de la classe 'donnees_presence'
avril = asm.donnees_presence(date_debut='20-04-01', date_fin='20-04-30',
                               heures_effectuees_par_jours = [7]*21,
                               repas_pris_par_jours = [True]*21)

print('Avril:')
print('  - {:.0f} jours de fin de semaine'.format(avril.n_jours_semaine1))
print('  - {:.0f}x7 jours de semaines completes'.format(avril.n_semaines_completes))
print('  - {:.0f} jours de debut de semaine'.format(avril.n_jours_semaineN))
