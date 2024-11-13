import random
import pickle
from colorama import init, Fore, Style

# Initialiser colorama
init(autoreset=True)


# Classe pour le personnage
class Perso:
    def __init__(self, nom):
        self.nom = nom
        self.vie = 50
        self.attaque = 10
        self.defense = 5
        self.xp = 0
        self.niveau = 1
        self.inventaire = []

    def gagner_xp(self, xp):
        self.xp += xp
        while self.xp >= self.niveau * 10:
            self.vie += 10
            self.attaque += 10
            self.defense += 5
            self.niveau += 1
            self.xp -= self.niveau * 10
            print(Fore.GREEN + f"Congratulations, you won a level. You are now level {self.niveau}.")

    def utiliser_item(self, item):
        if item in self.inventaire:
            item.utiliser(self)
            self.inventaire.remove(item)
        else:
            print("This item is not in your inventory.")

    def attaquer_monstre(self, monstre):
        attaque = max(0, self.attaque - monstre.defense)
        monstre.vie -= attaque
        print(Fore.RED + f"You attacked {monstre.nom} and inflicted {attaque} damage. The monster has now {monstre.vie}pv.")

# Classe pour le monstre
class Monstre:
    noms_des_monstre_par_niveau = {
        1: ["Goblin", "Ogre", "Skeleton"],
        2: ["Dragon", "Mortare", "Wicher"],
        3: ["Ninja", "Troll", "Gargoyle"],
        4: ["Zombie", "Giant", "Elf"],
        5: ["Felyne", "Diablos", "Rathalos"],
        6: ["Kirin", "Fatalis", "Kelbi"],
        7: ["Omega", "einherjar", "Wulver"],
        8: ["Anteka", "Ukanlos", "Baldur"]
    }

    def __init__(self, nom, niveau):
        self.nom = random.choice(self.noms_des_monstre_par_niveau.get(niveau, ["KRATOS"]))
        self.niveau = niveau
        self.vie = 40 + niveau * 10
        self.attaque = 5 + niveau * 5
        self.defense = 2 + niveau * 2

    def attaquer(self, perso):
        dommage = max(0, self.attaque - perso.defense)
        perso.vie -= dommage
        print(Fore.RED + f"{self.nom} attacked you and inflicted you {dommage} damage. You have now {perso.vie}pv")

# Classe pour la sauvegarde
class GameState:
    def __init__(self, perso, position, niveau_monstre):
        self.perso = perso
        self.position = position
        self.niveau_monstre = niveau_monstre

    def sauvegarder(self, fichier):
        with open(fichier, 'wb') as f:
            pickle.dump(self, f)

    @staticmethod
    def charger(fichier):
        with open(fichier, 'rb') as f:
            return pickle.load(f)

# Classe pour les objets
class Objet:
    def __init__(self, nom):
        self.nom = nom

    def utiliser(self, perso):
        pass

# Classe pour les potions et les boosts d'attaque et de défense
class Potion(Objet):
    def utiliser(self, perso):
        perso.vie += 20
        print(Fore.YELLOW + f"You use a potion and gain 20 pv. Your life is now {perso.vie} pv.")

class Attaque_boost(Objet):
    def utiliser(self, perso):
        perso.attaque += 5
        print(Fore.YELLOW + f"You used an item that increases your attack by 5. Your attack damage is now {perso.attaque} dmg.")

class Defense_boost(Objet):
    def utiliser(self, perso):
        perso.defense += 5
        print(Fore.YELLOW + f"You used an item that increases your defense by 5. Your defense is now {perso.defense}.")

# Fonction pour créer la carte
def creer_carte():
    carte = {
        (0, 0): Fore.MAGENTA + "You are in the middle of the forest, there are a lot of trees.",
        (1, 0): Fore.MAGENTA +"You find a glade with flowers.",
        (0, 1): Fore.MAGENTA +"You see a calm river.",
        (1, 1): Fore.MAGENTA +"You are in front of a cave.",
        (2, 0): Fore.MAGENTA +"You encounter a dense thicket.",
        (0, 2): Fore.MAGENTA +"You reach a small waterfall.",
        (1, 2): Fore.MAGENTA +"You discover an ancient ruin.",
        (2, 1): Fore.MAGENTA +"You find a hidden path leading deeper into the forest.",
        (2, 2): Fore.MAGENTA +"You are in a dark and eerie part of the forest.",
        (3, 0): Fore.MAGENTA +"You stumble upon a mysterious stone circle.",
        (0, 3): Fore.MAGENTA +"You see a bridge over the river.",
        (1, 3): Fore.MAGENTA +"You find a clearing with a campfire.",
        (2, 3): Fore.MAGENTA +"You encounter a group of friendly animals.",
        (3, 1): Fore.MAGENTA +"You discover a hidden treasure chest.",
        (3, 2): Fore.MAGENTA +"You are in a dense, foggy area.",
        (3, 3): Fore.MAGENTA +"You find a hidden entrance to a dungeon.",
        (4, 0): Fore.MAGENTA +"You see a tall, ancient tree.",
        (0, 4): Fore.MAGENTA +"You find a small pond with clear water.",
        (1, 4): Fore.MAGENTA + "You encounter a group of travelers.",
        (2, 4): Fore.MAGENTA +"You find a hidden path leading to a secret garden.",
        (3, 4): Fore.MAGENTA +"You see a mysterious statue.",
        (4, 1): Fore.MAGENTA +"You find a small hut with a wise old man.",
        (4, 2): Fore.MAGENTA +"You encounter a group of bandits.",
        (4, 3): Fore.MAGENTA +"You find a hidden entrance to a secret passage.",
        (4, 4): Fore.MAGENTA +"You find an house.",
        (5, 0): Fore.MAGENTA +"You see a large, ancient temple.",
        (0, 5): Fore.MAGENTA +"You find a hidden treasure map.",
        (1, 5): Fore.MAGENTA +"You encounter a group of adventurers.",
        (2, 5): Fore.MAGENTA +"You find a hidden path leading to a hidden village.",
        (3, 5): Fore.MAGENTA +"You see a mysterious altar.",
        (4, 5): Fore.MAGENTA +"You find a hidden entrance to a secret chamber.",
        (5, 1): Fore.MAGENTA +"You encounter a group of guards.",
        (5, 2): Fore.MAGENTA +"You find a hidden path leading to a hidden sanctuary.",
        (5, 3): Fore.MAGENTA +"You see a mysterious obelisk.",
        (5, 4): Fore.MAGENTA +"You find a hidden entrance to a secret library.",
        (5, 5): Fore.MAGENTA +"You are in front of the final boss in a dark cavern."
    }
    return carte


# Fonction pour déplacer le joueur
def deplacer_joueur(carte, position, direction):
    x, y = position
    if direction == "north":
        y += 1
    elif direction == "south":
        y -= 1
    elif direction == "east":
        x += 1
    elif direction == "west":
        x -= 1
    else:
        print("Invalid direction")

    if (x, y) in carte:
        return (x, y)
    else:
        print(Fore.CYAN +"You can't go there.")
        return position

# Fonction pour gérer les combats
def combat(perso, monstre, niveau_monstre):
    print(Fore.RED +f"You are attacked by a {monstre.nom} level {monstre.niveau}. He has {monstre.vie} pv and you have {perso.vie} pv")
    while perso.vie > 0 and monstre.vie > 0:
        print("\nPossibilities:")
        print("1. Attack the monster")
        print("2. Use an item")
        print("3. Run away")
        choix = input("Choose your action: ")

        if choix == "1":
            perso.attaquer_monstre(monstre)
        elif choix == "2":
            print("Items in your inventory:")
            for i, objet in enumerate(perso.inventaire):
                print(f"{i + 1}. {objet.nom}")
            choix_objet = input("Choose the item to use or 'return' to go back: ")
            if choix_objet.isdigit() and int(choix_objet) <= len(perso.inventaire):
                perso.utiliser_item(perso.inventaire[int(choix_objet) - 1])
            elif choix_objet == "return":
                continue
            else:
                print("Invalid choice")
        elif choix == "3":
            print("You ran away")
            return niveau_monstre  # Ca sert a retourne le niveau des monstres inchangé pour ne ps que le niveau change ou qu'elle agmente
        else:
            print("Invalid choice")

        if monstre.vie > 0:
            monstre.attaquer(perso)

    if perso.vie < 1:
        print(Fore.RED +f"You were defeated by the {monstre.nom}...")
        print("Returning to the MAIN MENU.")
        return jeu()
    else:
        print(Fore.RED +f"You won, you killed the {monstre.nom}")
        perso.gagner_xp(monstre.niveau * 10)
        return niveau_monstre + 1  # Cest pour incrémente le niveau des monstres

# Fonction pour le jeu
def jeu():
    print("Welcome")
    print("MAIN MENU:")
    print("1. Create new game")
    print("2. Load game")
    print("3. Exit")
    choix_menu = input("Select to continue: ")

    if choix_menu == "1":
        nom = input("Enter your name: ")
        print(Fore.BLUE +"Hello, You are here because I have chosen you HIHIHI. You woke up in the middle of the forest. You just have a knife as a weapon, and you have to kill monsters to upgrade your defense, attack, and level to kill the final boss. And for that, you have to find him. Good luck!!")
        print(Fore.BLUE +"And if you find the BOSS, you can't run away, you will fight with him for sure. HAHAHA")
        perso = Perso(nom)
        carte = creer_carte()
        position = (0, 0)
        niveau_monstre = 1

    elif choix_menu == "2":
        fichier = input("Enter the name of the save file: ")
        try:
            game_state = GameState.charger(fichier)
            perso = game_state.perso
            position = game_state.position
            niveau_monstre = game_state.niveau_monstre
            carte = creer_carte()
            print(f"Welcome back, {perso.nom}!")
        except FileNotFoundError:
            print("Save file not found. Returning to main menu.")
            return jeu()
    elif choix_menu == "3":
        print("Thank you for playing. Bye")
        return
    else:
        print("Invalid choice. Exiting the game.")
        return

    while True:
        print(carte[position])
        if position == (5, 5):
            boss = Monstre("BOSSE", 10)
            combat(perso, boss, niveau_monstre)
            if perso.vie < 1:
                print(Fore.RED +"You were defeated by the BOSS!")
                break
            elif boss.vie < 1:
                print(Fore.RED +"Congratulations, you defeated the BOSS! And you got out of the forest.")
                break
            else:
                continue
        direction = input(Fore.LIGHTCYAN_EX +"Enter a direction (north, south, east, west) or 'quit' to quit the game or 'save' to save the game: ")
        if direction == 'quit':
            print("Thank you for playing. Bye")
            break
        elif direction == 'save':
            fichier = input("Enter the name of the save file: ")
            game_state = GameState(perso, position, niveau_monstre)
            game_state.sauvegarder(fichier)
            print(Fore.GREEN + "Game saved successfully.")
            continue

        position = deplacer_joueur(carte, position, direction)

        if random.random() < 0.5:
            niveau_monstre = combat(perso, Monstre("Monstre", niveau_monstre), niveau_monstre)
        else:
            objet = random.choice([Potion("Potion"), Attaque_boost("Attack Boost"), Defense_boost("Defense Boost")])
            perso.inventaire.append(objet)
            print(f"You find a {objet.nom}!")

if __name__ == "__main__":
    jeu()  