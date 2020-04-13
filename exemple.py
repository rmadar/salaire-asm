import asm

# Test de la classe 'contrat'
ChristineD = asm.contrat(
    taux_horaire          = 3.5, 
    frais_entretien       = 3.10,
    entretien_par_jour    = True,
    frais_repas           = 0.0,
    n_heures_jour         = 7,
    jours_semaine         = [0, 1, 1, 0, 1, 0, 0], 
    n_semaines_an         = 45, 
    n_mois_mensualisation = 12
)
print('Cout mensuel        : {:.2f} Euros'.format(ChristineD.cout_mensualise()))
print('Conges payes mensuel: {:.2f} Euros'.format(ChristineD.conges_payes_mensualises()))


avril_absence = asm.donnees_presence(date_debut = '20-04-01',
                                     date_fin = '20-04-30',
                                     heures_effectuees_par_jours = [0]*13,
                                     repas_pris_par_jours = [False]*13)

print('\nAvril ({} semaines incompletes et {} completes):'.format(avril_absence.N_semaines_incompletes(), avril_absence.N_semaines_completes()))
print('  - {:.0f} jours de fin de semaine'.format(avril_absence.N_jours_semaine1()))
print('  - {:.0f}x7 jours de semaines completes'.format(avril_absence.N_semaines_completes()))
print('  - {:.0f} jours de debut de semaine'.format(avril_absence.N_jours_semaineN()))
print('  - cout reel Avril si absence : {:.2f} Euros'.format(ChristineD.cout_reel_periode(avril_absence)))

avril_surpresence = asm.donnees_presence(date_debut = '20-04-01',
                                      date_fin = '20-04-30',
                                      heures_effectuees_par_jours = [15.5]*13,
                                      repas_pris_par_jours = [False]*13)

print('  - cout reel Avril si (sur)presence: {:.2f} Euros'.format(ChristineD.cout_reel_periode(avril_surpresence)))


