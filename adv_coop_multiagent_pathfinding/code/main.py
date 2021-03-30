import pygame
import sys
from stratCoopBase import CoopBase
from stratPathSlicing import Slicing
from stratTempsAvance import temporal_A
from stratTempsAvanceDepth import temporal_A_D
sys.path.append('../')
from pySpriteWorld.gameclass import Game
from pySpriteWorld.spritebuilder import SpriteBuilder
from pySpriteWorld.ontology import Ontology

# game doit être une variable globale
game = Game()

class Projet():
    """
    Classe principale du projet. Permet de faire les quatre simulations principales
    avec les fonctions mainSlicing, mainCoopBase, mainTempA, mainTempA_D.
    """
    def __init__(self, boardNumber = 1, boardName = None, fps = 5, iterations = 100):
        """
        boardNumber : identifiant de la carte de jeu à utiliser.
        fps : nombre de cadres par seconde.
        iterations : nombre maximal d'itérations.
        """
        global game
        if boardName is None:
            game = Game('Cartes/map' + str(boardNumber) + '.json', SpriteBuilder)
        else:
            game = Game('Cartes/' + str(boardName) + '.json', SpriteBuilder)
        game.O = Ontology(True, 'SpriteSheet-32x32/tiny_spritesheet_ontology.csv')
        game.populate_sprite_names(game.O)
        game.fps = fps  # frames per second
        game.mainiteration()
        game.mask.allow_overlaping_players = False
        self.iterations = iterations

    def mainSlicing(self, goalStates = None, m = 3, n = 2, max_slice = 10, verbose = True):
        """
        Stratégie de slicing. Prend en argument:
        goalStates : Positions des fioles. Doit être une permutation de la
                     position originale des fioles dans la carte.
        m : Longueur qu'on regarde dans le futur pour le slicing.
        n : Nombre de pas de temps entre deux slicing. On doit avoir m > n
        max_slice : La taille maximale du nouveau slice ne doit pas dépasser
                    max_slice * m. Si cela arrive, on recalcule le chemin
                    directement vers la fiole.
        verbose : Si True, fait des affichages.
        """
        sl = Slicing(game, self.iterations, m, n, max_slice, verbose)
        try:
            if goalStates is not None:
                sl.setGoalStates(goalStates)
            sl.run()
        finally:
            pygame.quit()

    def mainCoopBase(self, goalStates = None, verbose = True):
        """
        Stratégie coopérative de base. Prend en argument:
        goalStates : Positions des fioles. Doit être une permutation de la
                     position originale des fioles dans la carte.
        verbose : Si True, fait des affichages.
		Attention, pour cette stratégie, self.iterations est le nombre
		maximal d'itérations **par groupe**. Le nombre maximal d'itérations
		peut être au pire cas égal à nbPlayers * iterations.
        """
        cb = CoopBase(game, self.iterations, verbose)
        try:
            if goalStates is not None:
                cb.setGoalStates(goalStates)
            cb.run()
        finally:
            pygame.quit()

    def mainTempA(self, goalStates = None, verbose = True):
        """
        Stratégie coopérative avancée. Prend en argument:
        goalStates : Positions des fioles. Doit être une permutation de la
                     position originale des fioles dans la carte.
        verbose : Si True, fait des affichages.
        """
        ta = temporal_A(game, self.iterations, verbose)
        try:
            if goalStates is not None:
                ta.setGoalStates(goalStates)
            ta.run()
        finally:
            pygame.quit()

    def mainTempA_D(self, goalStates = None, d = 7, verbose = True):
        """
        Stratégie coopérative avancée avec profondeur de recherche fixée.
        Prend en argument:
        goalStates : Positions des fioles. Doit être une permutation de la
                     position originale des fioles dans la carte.
        d : profondeur de recherche.
        verbose : Si True, fait des affichages.
        """
        tad = temporal_A_D(game, self.iterations, d, verbose)
        try:
            if goalStates is not None:
                tad.setGoalStates(goalStates)
            tad.run()
        finally:
            pygame.quit()

# Permet de faire des tests directement depuis ce fichier.
if __name__ == '__main__':
    p = Projet(boardNumber = 2, fps = 5, iterations = 100)
    #p = Projet(boardName = "map0", fps = 5)
    
    # Exemple avec position fixe des fioles
    #p.mainTempA([(12, 6), (19, 8), (6, 7)], verbose = False)
    
    #p.mainCoopBase()
    #p.mainSlicing()
    p.mainTempA()
    #p.mainTempA_D([(9, 9), (4, 7)], d = 8)
