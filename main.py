import spacy
import random
import requests

api_url = "https://api.openai.com/v1/engines/davinci-codex/completions"

api_key = "YOUR_API_KEY"

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}

nlp = spacy.load("en_core_web_lg")

verbal_forms = {"VBG":"Present continous","VBN":"Past participle","VBD":"Past simple","VB":"Base form","VBZ":"Present simple(3rd Person)","VBP":"Present simple","VH":"Future","VHD":"Past perfect","VHN":"Past Participle","VHP":"Present Perfect","VHZ":"Present Perfect(3rd person)","VVN":"Past Participle"}

verbs_most_used = ["be","have","do","make","use","say","get","go","take","see","know","include","come","find","give","think","work","need","look","want","provide","help","become","start","follow","show","call","try","create","keep","leave","write","tell","play","add","feel","run","read","allow","put","mean","seem","lead","set","offer","ask","bring","hold","build","require","continue","learn","live","move","begin","like","receive","let","support","develop","consider","change","base","turn","pay","believe","meet","love","increase","happen","grow","serve","send","understand","remain","hear","lose","appear","accord","buy","win","expect","involve","produce","choose","speak","cause","improve","open","apply","talk","report","spend","join","sell","cover","enjoy","pass","reduce","stop","die"]

prompt_first_round = ""

prompt_second_rounds = ""

global_protagonist = None

global_protagonist_name = None

global_enemy = None

global_verb_chosen = None

global_form_chosen = None

global_chosen_form_nlp = None

def game_instructions():
    print("Welcome to the Legend of the Verbs!\nIn this game, you will control a protagonist and engage in battles with enemies")
    print("You will learn how to use the modal verbs\nYou will have to attack the enemies using modal verbs")
    print("You will have to use the correct modal verb to defeat the enemy\nIf you use the wrong modal verb, you will lose your turn")
    print("You will have 100HP and the enemy will have HP according to the difficulty level")

def choose_tense_and_verb():
    global global_form_chosen
    global global_chosen_form_nlp
    global global_verb_chosen
    global_verb_chosen = random.choice(verbs_most_used)
    global_chosen_form_nlp = random.choice(list(verbal_forms.keys()))
    global_form_chosen = verbal_forms[global_chosen_form_nlp]

def api_gpt_call(prompt):
    data = {
    "prompt": prompt,
    "max_tokens": 100
    }
    
    response = requests.post(api_url, json=data, headers=headers)
    result = response.json()
    
    if response.status_code == 200:
        return response.json()["choices"][0]["text"]
    else:
        return "Error: Failed to call GPT API"
class Game:
    def __init__(self):
        self.streak = 0
        self.achievements = {
            5: False,
            10: False,
            20: False
        }

    def increase_streak(self):
        self.streak += 1
        self.check_achievements()

    def reset_streak(self):
        self.streak = 0

    def check_achievements(self):
        if self.streak >= 5 and not self.achievements[5]:
            print("Achievement unlocked: 5-streak!")
            self.achievements[5] = True
        if self.streak >= 10 and not self.achievements[10]:
            print("Achievement unlocked: 10-streak!")
            self.achievements[10] = True
        if self.streak >= 20 and not self.achievements[20]:
            print("Achievement unlocked: 20-streak!")
            self.achievements[20] = True
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
    def __init__(self, difficulty):
        super().__init__(hp = 50 * difficulty, atk = 10 * difficulty)

def combat(success):
    global global_protagonist
    global global_enemy
    if success == True:
        Game.increase_streak()
        global_protagonist.attack(global_enemy)
        global_enemy.take_damage(global_protagonist.atk)
        """Añadir un output de cuanto daño ha hecho al enemigo y cuanto le queda de vida al enemigo"""
    else:
        Game.reset_streak()
        global_enemy.attack(global_protagonist)
        global_protagonist.take_damage(global_enemy.atk)
        """Añadir un output de cuanto daño ha hecho al protagonista y cuanto le queda de vida al protagonista"""
        
def check_tense(input_text):
    global global_verb_chosen
    global global_form_chosen_nlp
    doc = nlp(input_text)
    for token in doc:
        if token.lemma_ == global_verb_chosen:
            if token.tag_ == global_form_chosen_nlp:
                return True
            else:
                print("You used the wrong tense")
                return False
        else:
            print("You used the wrong verb")
            return False

def level_1():
    global_enemy = Enemy(1)
    choose_tense_and_verb()
    print(api_gpt_call(prompt_first_round))
    input_text = input("Enter your phrase: ")
    success = check_tense(input_text)
    combat(success)
    while global_enemy.hp > 0 and global_protagonist.hp > 0:
        print(api_gpt_call(prompt_second_rounds))
        input_text = input("Enter your phrase: ")
        success = check_tense(input_text)
        combat(success)
    if global_enemy.hp == 0:
        print("You defeated the enemy")
    else:
        print("You lost the battle")

def main():
    game = Game()
    global_protagonist_name = input("Enter the name of your protagonist: ")
    global_protagonist = Protagonist(global_protagonist_name)
    level_1()

if __name__ == "__main__":
    main()
