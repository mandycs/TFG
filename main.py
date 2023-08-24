

class Character:
    def __init__(self, name, hp, atk):
        self.name = name
        self.hp = hp
        self.atk = atk

    def take_damage(self, damage):
        self.hp -= damage

    def attack(self, enemy):
        enemy.take_damage(self.atk)

class Protagonist(Character):
    def __init__(self, name):
        super().__init__(name, hp=100, atk=20)

class Enemy(Character):
    def __init__(self, name, difficulty):
        super().__init__(name, hp = 50 * difficulty, atk = 10 * difficulty)

def battle(protagonist, enemy):
    while protagonist.hp > 0 and enemy.hp > 0:
        protagonist.attack(enemy)
        if enemy.hp <= 0:
            break
        enemy.attack(protagonist)
        if protagonist.hp <= 0:
            break

def game_instructions():
    print("Welcome to the Legend of the Modals!\nIn this game, you will control a protagonist and engage in battles with enemies")
    print("You will learn how to use the modal verbs\nYou will have to attack the enemies using modal verbs")
    print("You will have to use the correct modal verb to defeat the enemy\nIf you use the wrong modal verb, you will lose your turn")
    print("You will have 100HP and the enemy will have HP according to the difficulty level")

def level_1(protagonist):
    enemy1 = Enemy("Goblin", hp=30, atk=10)
    enemy2 = Enemy("Skeleton", hp=25, atk=15)

    print("Welcome to Level 1!")
    print("You will face a Goblin and a Skeleton.")
    input("Press Enter to start the battle...")
    
    battle(protagonist, enemy1)
    if protagonist.hp > 0:
        battle(protagonist, enemy2)

    """print("You have completed Level 1!")"""

# Define more levels and enemies for each level

def main():
    protagonist_name = input("Enter the name of your protagonist: ")
    protagonist = Protagonist(protagonist_name)

    level_1(protagonist)
    # Call more level functions here

if __name__ == "__main__":
    main()
