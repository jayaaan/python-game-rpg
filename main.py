import random
import pickle

#class pour le perso
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
            print(f"Congratulations, you won a level. You are now level {self.niveau}.")

    def utiliser_item(self, item):
        if item in self.inventaire:
            item.utiliser(self)
            self.inventaire.remove(item)
        else:
            print("This item is not in your inventory.")

    def attaquer_monstre(self, monstre):
        attaque = max(0, self.attaque - monstre.defense)
        monstre.vie -= attaque
        print(f"You attacked {monstre.nom} and inflicted {attaque} dammage. The monster has now {monstre.vie}pv.")

#class pour le monstre
class Monstre:
    noms_des_monstre_par_niveau = {
        1 : ["Goblin", "Ogre", "Skeleton"],
        2 : ["Dragon", "Mortare", "Wicher"],
        3 : ["Ninja", "Troll", "Gargoyle"],
        4 : ["Zombie", "Giant", "Elf"],
        5 : ["Felyne", "Diablos", "Rathalos"],
        6 : ["Kirin", "Fatalis", "Kelbi"],
        7 : ["Omega", "einherjar", "Wulver"],
        8 : ["Anteka", "Ukanlos", "Baldur"]
    }

    def __init__(self, nom, niveau):
        self.nom = random.choice(self.noms_des_monstre_par_niveau.get(niveau, ["Unknown monster"]))
        self.niveau = niveau
        self.vie = 40 + niveau * 10
        self.attaque = 5 + niveau * 5
        self.defense = 2 + niveau * 3

    def attaquer(self, perso):
        dommage = max(0, self.attaque - perso.defense)
        perso.vie -= dommage
        print(f"{self.nom} attacked you and inflicted you {dommage} dammage. You have now {perso.vie}pv")

#class pour la sauvegarde
class GameState:
    def __init__(self, perso, position):
        self.perso = perso
        self.position = position

    def sauvegarder(self, fichier):
        with open(fichier, 'wb') as f:
            pickle.dump(self, f)

    @staticmethod
    def charger(fichier):
        with open(fichier, 'rb') as f:
            return pickle.load(f)


#class pour les objets
class Objet:
    def __init__(self, nom):
        self.nom = nom

    def utiliser(self, perso):
        pass

#class pour les potion et attaque boost etc (c'est mieux de faire des class pour les 3, je comprends mieux)
class Potion(Objet):
    def utiliser(self, perso):
        perso.vie += 20
        print(f"You use a potion and gain 20 points of life. Your life is now {perso.vie}pv.")


class Attaque_boost(Objet):

    def utiliser(self, perso):
        perso.attaque += 5
        print(f"You used an item that increase to 5 your attack. Your dammage of attack is now {perso.attaque} dmg.")


class Defense_boost(Objet):
    def utiliser(self, perso):
        perso.defense += 5
        print(f"You used an item that increase to 5 your defense. Your defense is now {perso.defense}.")

#la fonction pour creer la caarte
def creer_carte():
    carte = {
        (0, 0): "You are in the middle of the forest, there are a lot of trees.",
        (1, 0): "You find a glade with flowers.",
        (0, 1): "You see a calm river.",
        (1, 1): "You are in front of a cave.",
        (2, 0): "You encounter a dense thicket.",
        (0, 2): "You reach a small waterfall.",
        (1, 2): "You discover an ancient ruin.",
        (2, 1): "You find a hidden path leading deeper into the forest.",
        (2, 2): "You are in a dark and eerie part of the forest.",
        (3, 0): "You stumble upon a mysterious stone circle.",
        (0, 3): "You see a bridge over the river.",
        (1, 3): "You find a clearing with a campfire.",
        (2, 3): "You encounter a group of friendly animals.",
        (3, 1): "You discover a hidden treasure chest.",
        (3, 2): "You are in a dense, foggy area.",
        (3, 3): "You are in front of the final boss in a dark cavern."
    }
    return carte

#la fonction pour deplacer le joueur
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
        print("You can't go there.")
        return position

#fonction pour le combats et gerer le combat
def combat(perso, monstre):
    print(f"You attacked by a {monstre.nom} level {monstre.niveau}")
    while perso.vie > 0 and monstre.vie > 0:
        print("\n Possibilities :")
        print("1. Attack the monster")
        print("2. Use an item")
        print("3. Run away")
        choix = input("Choose your action : ")

        if choix == "1":
            perso.attaquer_monstre(monstre)
        elif choix == "2":
            print("Objets in your inventory :")
            for i, objet in enumerate(perso.inventaire):
                print(f"{i + 1}. {objet.nom}")
            choix_objet = input("Choose the item to use or 'return' for return back : ")
            if choix_objet.isdigit() and int(choix_objet) <= len(perso.inventaire):
                perso.utiliser_item(perso.inventaire[int(choix_objet) - 1])
            elif choix_objet == "Return":
                continue
            else:
                print("Doesn't find your choice")
                choix_objet
        elif choix == "3":
            print("You ran away")
            return
        else:
            print("Doesn't find your choice")
            return choix

        if monstre.vie > 0:
            monstre.attaquer(perso)

    if perso.vie < 1:
        print(f"You were defeated by the {monstre.nom}...")
        print("Returning to the MAIN MENU.")
    else:
        print(f"You won, you kill the {monstre.nom}")
        perso.gagner_xp(monstre.niveau * 10)

#fonction pour le jeu, son fonctonnement etc
def jeu():
    print("Welcome")
    print("MAIN MENU :")
    print("1. Create new game")
    print("2. Load game")
    print("3. Exit")
    choix_menu = input("Select to continue : ")

    if choix_menu == "1" :
        nom = input("Enter your name : ")
        print(
            "Hello, You are here beacause I have choosen you hihihi. You woke in the middle of the forest. You just have knife like weapon, and you have to kill monsters to upgrade you defense, attack and level to kill the final. And for that you have to find him. Good luck !!")
        perso = Perso(nom)
        carte = creer_carte()
        position = (0, 0)



    elif choix_menu == "2" :

        fichier = input("Enter the name of the save file: ")

        try:
            game_state = GameState.charger(fichier)
            perso = game_state.perso
            position = game_state.position
            carte = creer_carte()
            print(f"Welcome back, {perso.nom}!")

        except FileNotFoundError:

            print("Save file not found. Returning to main menu.")

            return jeu()
    elif choix_menu == "3" :
        print("Thank you for playing. Bye")
    else:
        print("Invalid choice. Exiting the game.")

    while True:
        print(carte[position])
        if position == (3, 3):
            boss = Monstre("BOSSE", 10)
            combat(perso, boss)
            if perso.vie < 1:
                print("You defeat, the BOSS wins!")
                break
            else:
                print("Congratulations, you won the BOSS ! And go out of the forest.")
                break
        direction = input("Enter a direction (north, south, east, west) or 'quit' to quit the game or 'save' to save the game : ")
        if direction == 'quit':
            print("Thank you for playing. Bye")
            break


        elif direction == 'save':

            fichier = input("Enter the name of the save file: ")
            game_state = GameState(perso, position,)
            game_state.sauvegarder(fichier)
            print("Game saved successfully.")
            continue

        position = deplacer_joueur(carte, position, direction)

        if random.random() < 0.5:
            monstre = Monstre("Monstre", random.randint(1, 4))
            combat(perso, monstre)
        else:
            objet = random.choice([Potion("Potion"), Attaque_boost("Attack Boost"), Defense_boost("Defense Boost")])
            perso.inventaire.append(objet)
            print(f"You find a {objet.nom}!")


if __name__ == "__main__":
    jeu()