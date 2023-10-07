import tkinter as tk
import time
from . import disques

class Setup:
    def __init__(self, nbdisques):
        self.root = tk.Tk()
        self.canvas = tk.Canvas(self.root, width=800, height=250)
        self.canvas.pack()
        
        self.disques = [[], [], []]
        for taille in range(nbdisques):
            self.disques[0].append(disques.Setup(taille+1))
        self.nbdisques = len(self.disques[0])
        self.root.title(f"Hanoï : {self.nbdisques} disque.s")

    def __str__(self):
        return str(self.disques)
    
    def jouer(self):
        self.afficher()
        self.root.update()
        
        def bouge(x, y):
            """
            Fonction qui "déplace" les disques si c'est possible
            """
            if self.disques[x] != [] and self.disques[y] == []:
                self.disques[y].insert(0, self.disques[x].pop(0))
                self.afficher()
                self.root.update()
                return True
            
            elif self.disques[x] != [] and self.disques[x][0].taille < self.disques[y][0].taille:
                self.disques[y].insert(0, self.disques[x].pop(0))
                self.afficher()
                self.root.update()
                return True
            
            else:
                return False
            
        def deplace2pions(depart, arrivee, intermediaire):
            """
            Fonction qui permet de deplacer deux disques si c'est possible
            """
            if bouge(depart, intermediaire) == False:
                return f"Erreur 1 deplacer2pions() {self.disques[depart][0].taille, self.disques[intermediaire][0].taille}"
            if bouge(depart, arrivee) == False:
                bouge(intermediaire, depart)
                return f"Erreur 2 deplacer2pions() {self.disques[intermediaire][0].taille, self.disques[depart][0].taille}"
            if bouge(intermediaire, arrivee) == False:
                bouge(arrivee, depart)
                bouge(intermediaire, depart)
                return f"Erreur 1 deplacer2pions() {self.disques[intermediaire][0].taille, self.disques[arrivee][0].taille}"
            return "OK"
        
        def deplaceNpions(n, depart, arrivee, intermediaire):
            """
            La fameuse fonction récursive qui permet de déplacer N disques
            """
            if n > self.nbdisques:
                print(f'Impossible de deplacer {n} disques, puisqu\'il y en a {self.nbdisques}')
                return
            if n == 0:
                return
            if n == 1:
                bouge(depart, arrivee)
                return
            if n == 2:
                deplace2pions(depart, arrivee, intermediaire)
                return
            else:
                deplaceNpions(n-1, depart, intermediaire, arrivee)
                bouge(depart, arrivee)
                deplaceNpions(n-1, intermediaire, arrivee, depart)

        deplaceNpions(self.nbdisques, 0, 2, 1) # il y a surement mieux que ça mais voilà, tant que ça fonctionne c'est bon !
    
    def afficher(self):
        self.canvas.delete("all")
        self.canvas.create_rectangle(150, 200, 150, 50)
        self.canvas.create_rectangle(400, 200, 400, 50)
        self.canvas.create_rectangle(650, 200, 650, 50)
        self.canvas.create_rectangle(50, 200, 750, 200)

        for tour in range(len(self.disques)):
            for disque in range(len(self.disques[tour])):
                taille = self.disques[tour][-1-disque].taille
                largeur = taille * 20
                hauteur = 20
                x = 150 + tour * 250 - taille*10
                y = 200 - hauteur * (disque + 1)
                self.canvas.create_rectangle(x, y, x + largeur, y + hauteur, fill=self.disques[tour][-1-disque].couleur)
                
        self.root.update()
        time.sleep(0.5)