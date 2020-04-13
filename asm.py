class donnees_presence:
  
  '''
  Objet permettant de calculer les grandeures necessaire 
  a l'estimation des couts de la periode:
    - nombre de jours travailles
    - nombre de semaines completes / incompletes 
  '''


  def __init__(self,
               date_debut, date_fin,
               heures_effectuees_par_jours,
               repas_pris_par_jours,
               nom_fichier_donnees=None):
      
      '''
      date_debut, date_fin: 'JJ/MM/AA'
      heures_effectuees_par_jours: liste de float (len=nombre de jours ouvres)
      repas_pris_par_jours: liste de boolean (len=nombre de jours ouvres)
      nom_fichier_donnees: nom de fichier CSV - a implementer
      '''

      # Info manuelles
      self.debut = date_debut
      self.fin = date_fin
      self.n_heures_jour = heures_effectuees_par_jours
      self.n_repas_jour = repas_pris_par_jours

      # Info passee par un fichier csv
      if nom_fichier_donnees:
         self.lire_donnees(nom_fichier_donnees)

      # Calcul
      self.n_jours_ouvres = self.N_jours_ouvres()
      self.n_semaines_completes = self.N_semaines_completes()


  def N_jours_ouvres(self):
      return 30
  
  def N_semaines_completes(self):
      return 4



class contrat:

  def __init__(self, 
               taux_horaire=3.5, frais_entretient=3.10, frais_repas=4.0,
               n_jours_semaine=3, n_heures_jour=7,
               n_semaines_an=45, n_mois_mensualisation=12):

      self.taux_h = taux_horaire
      self.frais_j = frais_entretient
      self.frais_repas = frais_repas
      self.n_heures_j = n_heures_jour
      self.n_jours_s = n_jours_semaine
      self.n_semaines_an = n_semaines_an
      self.n_mois_mensualisation = n_mois_mensualisation


  # Cout journalier prevu par le contrat
  def cout_journalier(self):
      return self.taux_h * self.n_heures_j + self.frais_j + self.frais_repas


  # Cout annuel prevu par le contrat
  def cout_annuel(self):
      return self.cout_journalier() * self.n_jours_s * self.n_semaines_an


  # Cout mensualise prevu par le contrat
  def cout_mensualise(self):
    return self.cout_annuel() / self.n_mois_mensualisation


  # Cout journalier pris en compte pour le calcul des conges payes
  def cout_journalier_charges(self):
      return self.taux_h * self.n_heures_j


  # Cout annuel pris en compte pour le calcul des conges payes
  def cout_annuel_charges(self):
      return self.cout_journalier_charges() * self.n_jours_s * self.n_semaines_an


  # Calcul des conges payes annuels
  def conges_payes_annuel(self):
      c1 = 0.10 * self.cout_annuel_charges()
      c2 = 2.5 * self.cout_journalier_charges() * 12
      return max(c1, c2)


  # Calcul des conges payes mensualises
  def conges_payes_mensualises(self):
      return self.conges_payes_annuel() / 12.


  # Calcul du cout reel sur une periode donnee avec presence effectives
  def cout_reel_periode(self, n_jours_prevus, donnees_presence):
      '''
      Calcul le cout reel sur une periode precise compte tenu des heures
      de presence reelles.

      n_jours_prevus (int): nombre de jours de presence supposee par le contrat.
      donnees_presence (list): liste de taille n_jours_prevus dont chaque element
                               est [nbr heure effective (float), repas pris bool)]
      '''

      # Verifier que les donnees presentielles fournies sont coherentes
      if len(donnees_presence) != n_jours_prevus:
         err =  'ContratASM.cout_reel_periode(): \n \t la taille de la liste de presence'
         err += ' effective (ici, {}) n\'est \n \t pas egale au nombre de jours prevus (ici, {}).'
         print(err.format(len(donnees_presence), n_jours_prevus))
         return -1 

      # Analyse des jours de presence un par un
      garde, entretien, repas = 0, 0, 0
      for journee in donnees_presence:

          # Nombre d'heures et repas
          Nheures, AvecRepas = journee

          # Une journee prevue non effectuee est due, une journee plus longue 
          # se paie mais une journee plus courte reste due dans son entier.
          garde += self.taux_h * self.n_heures_j
          if Nheures > self.n_heures_j:
             garde += self.taux_h * (Nheures-self.n_heures_j)

          # Frais d'entretiens dus uniquement pour les jours de presence
          if Nheures > 0:
             entretien += self.frais_j

          # Repas
          if AvecRepas:
             repas += self.frais_repas

      return garde + entretien + repas
