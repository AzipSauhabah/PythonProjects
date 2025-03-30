# Python Projects - Games 🎮

Bienvenue dans **Python Projects**, un dépôt dédié aux jeux développés en **Python** ! Ce projet rassemble une collection de jeux classiques créés à l'aide de **Pygame** et d'autres bibliothèques Python. Chaque jeu a été conçu pour renforcer mes compétences en programmation tout en explorant des concepts amusants.

🔧 **Technologies utilisées** :
- **Python 3.x**
- **Pygame**

---

## 🕹️ Liste des jeux

Voici la liste complète des jeux inclus dans ce dépôt :

- **Kirby**
- **Mario Level 1**
- **Metal Python**
- **OutRun**
- **Pacman**
- **PyTetris**
- **R-Typo**
- **RealTime3D with Python**
- **Royal Ordains**
- **Street Fighter**
- **Zelda with Python**
- **Sonic Pygame**
- **Super Mario Python**

---

## 📸 Aperçu des jeux

![Mario](https://upload.wikimedia.org/wikipedia/commons/0/0b/Mario_bros_logo.svg)  
*Mario Level 1*

![Pacman](https://upload.wikimedia.org/wikipedia/commons/4/47/Pac-Man_Logo.svg)  
*Pacman*

![Zelda](https://upload.wikimedia.org/wikipedia/commons/d/d4/Zelda_Logo.svg)  
*Zelda with Python*

---

## ⚙️ Prérequis

Avant de commencer à jouer, vous devez installer les bibliothèques suivantes :

- **Python 3.x** : [Télécharger Python](https://www.python.org/downloads/)
- **Pygame** : Utilisez la commande ci-dessous pour installer **Pygame**.

```bash
pip install pygame

🚀 Lancer les jeux

1. Clonez le dépôt sur votre machine locale :
git clone https://github.com/AzipSauhabah/PythonProjects.git

2. Naviguez vers le dossier du jeu que vous souhaitez lancer :

Par exemple, pour jouer à Mario Level 1 :
cd PythonProjects/Mario-Level-1-master

3. Exécutez le script Python pour démarrer le jeu :
python mario_game.py

🛠️ Explication du Code
Exemple : Mario Level 1
Voici une vue d'ensemble du code de base pour démarrer un jeu comme Mario Level 1.

import pygame

# Initialisation de Pygame
pygame.init()

# Dimensions de la fenêtre du jeu
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Mario Level 1")

# Boucle de jeu
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Mettre à jour l'affichage
    screen.fill((255, 255, 255))  # Remplir l'écran de blanc
    pygame.display.update()

pygame.quit()

```
##  Explication :

- **Initialisation : Le module Pygame est initialisé avec pygame.init().

- **Fenêtre du jeu : Nous créons une fenêtre avec les dimensions 800x600 pixels en utilisant pygame.display.set_mode().

- **Boucle principale : Le jeu s'exécute dans une boucle infinie (while running:), où il écoute les événements comme la fermeture de la fenêtre.

- ** Mise à jour de l'affichage : À chaque itération de la boucle, l'écran est rempli de blanc et la fenêtre est mise à jour avec pygame.display.update().

📝 Contributions
Si vous avez des suggestions, des améliorations ou des corrections à proposer, n'hésitez pas à soumettre une pull request !

👤 Auteurs
AzipSauhabah - Développeur principal du projet

📜 Licence
Ce projet est sous la licence MIT. Voir le fichier LICENSE pour plus d'informations.

🔗 Liens utiles
- **Documentation Pygame
- ** Python 3.x

💬 Contact
Pour toute question, contactez-moi via mon profil GitHub

### Ce README comprend maintenant :

- **Tous les jeux** de votre projet, bien détaillés sous la section "Liste des jeux".
- **Instructions pour lancer** chaque jeu, y compris la partie pour cloner le dépôt, naviguer dans le dossier du jeu, et exécuter les scripts Python.
- **Exemple de code** avec une explication détaillée pour comprendre comment les jeux sont lancés et structurés (exemple avec **Mario Level 1**).
- **Liens utiles** pour aider l'utilisateur à installer **Pygame** et **Python**, ainsi que des ressources supplémentaires.
- **Section de contributions** et des informations de contact.

Cela permet à vos utilisateurs de rapidement comprendre comment interagir avec votre dépôt et commencer à jouer à vos projets ! Si vous avez d'autres questions ou ajustements à faire, je suis là pour aider.
