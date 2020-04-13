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
    heures_effectuees_par_jours: liste de float (len=nombre de jours travaille prevus)
    repas_pris_par_jours: liste de boolean (len=nombre de jours travailles prevus)
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
      
    # Nombre de jours total
    self.n_jours = (np.datetime64(self.fin) - np.datetime64(self.debut)) / np.timedelta64(1,'D') + 1

    
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
      raise NameError('donnees_presence(): Nombre de semaine non-entier, alors que ca ne devrait pas!')
    else: 
      return int(Nsemaines)

    
  def N_semaines_incompletes(self):
    return int(self.N_jours_semaine1()>0) + int(self.N_jours_semaineN()>0)


  def indice_semaine_entiere_du_jour(self, j, weekmask):
    '''
    Calcul l'indice de la semaine entiere de la periode, 
    a laquelle le jour j appartient (en fonction du nombre de jour travailles)
    retourne int, bool: indice de la semaine, si elle est complete ou non
    '''

    if len(weekmask) != 7:
      raise NameError('weekmask doit etre contenir 7 elements (0 ou 1): ', weekmask)

    # Premier semaine (eventuellement incomplete)
    premier_lundi = np.busday_offset(self.debut, 0, roll='forward', weekmask='Mon')
    n_jours_prevus_1 = np.busday_count(self.debut, premier_lundi, weekmask=weekmask)

    # Derniere semaine (eventuellement incomplete)
    dernier_dimanche = np.busday_offset(self.fin, 0, roll='backward', weekmask='Sun')
    n_jours_prevus_N = np.busday_count(dernier_dimanche, self.fin, weekmask=weekmask)

    # Semaines completes au milieu
    n_jours_prevus = np.busday_count(premier_lundi, dernier_dimanche, weekmask=weekmask)

    if j<n_jours_prevus_1:
      isemaine, complete = 0, False

    elif j<n_jours_prevus_1+n_jours_prevus:
      isemaine, complete = (j+1) // sum(weekmask), True

    else:
      isemaine, complete = self.N_semaines_completes() + 1, False

    return isemaine, complete
      
      
  def lire_donnees(self, nom_fichier):
      pass
    


class contrat:

  def __init__(self, 
               taux_horaire=3.5, frais_entretien=3.10,
               entretien_par_jour=True, frais_repas=4.0, 
               jours_semaine=[1, 1, 1, 1, 1, 0, 0], n_heures_jour=7,
               taux_heures_supplementaires=1.50,
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
      if n_jours_prevus != len(d.n_heures_jour):
        err = 'donnees_presence: Il y a {} jours travailles (du {} au {} avec {}j/sem ), et {} horaires fournis.'
        err = err.format(n_jours_prevus, d.debut, d.fin, self.n_jours_s ,len(d.n_heures_jour))
        raise NameError(err)

      if n_jours_prevus != len(d.n_repas_jour):
        err = 'donnees_presence: Il y a {} jours travailles (du {} au {} avec {}j/sem ), et {} info repas.'
        err = err.format(n_jours_prevus, d.debut, d.fin, self.n_jours_s ,len(d.n_repas_jour))
        raise NameError(err)        
      
      # Analyse des jours de presence un par un
      garde, entretien, repas = 0, 0, 0
      heures_semaine = [[0, False] for i in range((d.N_semaines_completes() + d.N_semaines_incompletes()))]
      for ijour, (Nheures, AvecRepas) in enumerate(zip(d.n_heures_jour, d.n_repas_jour)):

        # Decompte des heures par semaine (heures complementaires/supplementaires)
        isemaine, est_complete = d.indice_semaine_entiere_du_jour(ijour, self.jours_semaine)
        heures_semaine[isemaine][0] += Nheures
        heures_semaine[isemaine][1] = est_complete
        
        # Une journee prevue non effectuee (ou plus courte) est due dans son entier
        garde += self.taux_h * self.n_heures_j

        # Une journee plus longue conduit a un cout supplementaire
        if Nheures > self.n_heures_j:
          garde += self.taux_h * (Nheures-self.n_heures_j)
            
        # Frais d'entretiens dus uniquement pour les jours de presence
        if Nheures > 0:
          entretien += self.frais_entretien_journalier(Nheures)
              
        # Repas
        if AvecRepas:
          repas += self.frais_repas

      # Affiche les heures supplementaires
      for i, (n, complete) in enumerate(heures_semaine):
        if complete:
          ncomp = int(n>self.n_heures_j*sum(self.jours_semaine)) * (n-self.n_heures_j*sum(self.jours_semaine))
          nsupp = int(n>45) * (n-45)  
          print('semaine {} (complete): {} heures -> {} comp et {} supp'.format(i, n, ncomp, nsupp))
          
      return garde + entretien + repas
