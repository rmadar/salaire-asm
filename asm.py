import numpy as np


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
               jours_feries=0,
               nom_fichier_donnees=None):
      
      '''
      date_debut, date_fin: 'AA-MM-DD'
      heures_effectuees_par_jours: liste de float (len=nombre de jours ouvres)
      repas_pris_par_jours: liste de boolean (len=nombre de jours ouvres)
      nom_fichier_donnees: nom de fichier CSV - a implementer
      '''

      # Info manuelles
      self.debut = date_debut
      self.fin = date_fin
      self.jours_feries = jours_feries
      self.n_heures_jour = heures_effectuees_par_jours
      self.n_repas_jour = repas_pris_par_jours

      # Info passee par un fichier csv
      if nom_fichier_donnees:
         self.lire_donnees(nom_fichier_donnees)

      # Calcul jours/semaines entieres/terminees/entammees
      self.n_jours = (np.datetime64(self.fin) - np.datetime64(self.debut)) / np.timedelta64(1,'D') + 1
      self.n_jours_ouvres = self.N_jours_ouvres()
      self.n_jours_semaine1 = self.N_jours_semaine1()
      self.n_jours_semaineN = self.N_jours_semaineN()
      self.n_semaines_completes = self.N_semaines_completes()
      

  def N_jours_ouvres(self):
      return np.busday_count(self.debut, self.fin) - self.jours_feries


  def N_jours_semaine1(self):
      premier_lundi = np.busday_offset(self.debut, 0, roll='forward', weekmask='Mon')
      dt = (np.datetime64(premier_lundi) - np.datetime64(self.debut)) / np.timedelta64(1,'D')
      return dt

    
  def N_jours_semaineN(self):
      dernier_dimanche = np.busday_offset(self.fin, 0, roll='backward', weekmask='Sun')
      dt = (np.datetime64(self.fin) - np.datetime64(dernier_dimanche)) / np.timedelta64(1,'D')
      return dt
    
    
  def N_semaines_completes(self):
      Ntot = self.n_jours 
      Ndebut = self.N_jours_semaine1()
      Nfin = self.N_jours_semaineN()
      Nsemaines = (Ntot - (Ndebut+Nfin)) // 7
      if (Ntot - (Ndebut+Nfin)) % 7 !=0 :
         raise NameError('donnees_presence(): Nombre de semaine non entiere, attention!')
      else: 
         return Nsemaines
      

  def lire_donnees(self, nom_fichier):
      pass
    


class contrat:

  def __init__(self, 
               taux_horaire=3.5, frais_entretien=3.10,
               entretien_par_jour=True, frais_repas=4.0, 
               jours_semaine=[1, 1, 1, 1, 1, 0, 0], n_heures_jour=7,
               n_semaines_an=45, n_mois_mensualisation=12):

      self.taux_h = taux_horaire
      self.frais_entretien = frais_entretien
      self.entretien_par_jour = entretien_par_jour
      self.frais_repas = frais_repas
      self.n_heures_j = n_heures_jour
      self.n_jours_s = sum(jours_semaine)
      self.jours_semaine = jours_semaine
      self.n_semaines_an = n_semaines_an
      self.n_mois_mensualisation = n_mois_mensualisation


  # Cout journalier prevu par le contrat
  def cout_journalier(self):
      return self.taux_h * self.n_heures_j + self.frais_entretien_journalier() + self.frais_repas


  # Cout annuel prevu par le contrat
  def cout_annuel(self):
      return self.cout_journalier() * self.n_jours_s * self.n_semaines_an


  # Cout mensualise prevu par le contrat
  def cout_mensualise(self):
    return self.cout_annuel() / self.n_mois_mensualisation


  # Cout journalier pris en compte pour le calcul des conges payes
  def cout_journalier_charges(self):
      return self.taux_h * self.n_heures_j

    
  # Frais entretien journaliers
  def frais_entretien_journalier(self, n_heures=None):
      if self.entretien_par_jour:
          return self.frais_entretien
      elif n_heures:
          return self.frais_entretien * n_heures
      else:
          return self.frais_entretien * self.n_heures_j
    

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
  def cout_reel_periode(self, donnees_periode):
      '''
      Calcul le cout reel sur une periode precise compte tenu des heures
      de presence reelles.

      donnees_periode (asm.donnees_presence)
      '''
      d = donnees_periode

      # Coherence des donnees fournies
      n_jours_prevus = np.busday_count(d.debut, d.fin, weekmask=self.jours_semaine)
      if  n_jours_prevus != len(d.n_heures_jour):
         err = 'donnees_presence: Il y a {} jours travailles (du {} au {} avec {}j/sem ), et {} horaires fournis.'
         err = err.format(n_jours_prevus, d.debut, d.fin, self.n_jours_s ,len(d.n_heures_jour))
         raise NameError(err)

      if n_jours_prevus != len(d.n_repas_jour):
        err = 'donnees_presence: Il y a {} jours travailles (du {} au {} avec {}j/sem ), et {} info repas.'
        err = err.format(n_jours_prevus, d.debut, d.fin, self.n_jours_s ,len(d.n_repas_jour))
        raise NameError(err)        
      
      # Analyse des jours de presence un par un
      garde, entretien, repas = 0, 0, 0
      for Nheures, AvecRepas in zip(d.n_heures_jour, d.n_repas_jour):

          # Une journee prevue non effectuee est due, une journee plus longue 
          # se paie mais une journee plus courte reste due dans son entier.
          garde += self.taux_h * self.n_heures_j
          if Nheures > self.n_heures_j:
             garde += self.taux_h * (Nheures-self.n_heures_j)

          # Frais d'entretiens dus uniquement pour les jours de presence
          if Nheures > 0:
             entretien += self.frais_entretien_journalier(Nheures)

          # Repas
          if AvecRepas:
             repas += self.frais_repas

      return garde + entretien + repas
