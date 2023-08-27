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

def game_instructions():
    print("Welcome to the Legend of the Verbs!\nIn this game, you will control a protagonist and engage in battles with enemies")
    print("You will learn how to use the modal verbs\nYou will have to attack the enemies using modal verbs")
    print("You will have to use the correct modal verb to defeat the enemy\nIf you use the wrong modal verb, you will lose your turn")
    print("You will have 100HP and the enemy will have HP according to the difficulty level")


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
class Achievements:
    def __init__(self):
        self.streak = 0
        self.achievements = {
            1: False,
            5: False,
            10: False,
            20: False
        }

    def check_level(self):
        if self.level == 2 and Character.Protagonist.hp == 100:
            print("Congratulations!!! You have reached level 2 without taking any damage!")
        elif self.level == 4 and Character.Protagonist.hp >= 50:
            print("Congratulations!!! You have reached level 4 with at least 50HP!")
        elif self.level == 6 and Character.Protagonist.hp == 100:
            print("Congratulations!!! You are a beast!!! You have reached level 6 without taking any damage!")
    def increase_level(self):
        self.level += 1
        self.check_level()

    def increase_streak(self):
        self.streak += 1
        self.check_achievements()

    def reset_streak(self):
        self.streak = 0

    def check_achievements(self):
        if self.streak >= 1 and not self.achievements[1]:
            print("Achievement unlocked: Congratulations!!! You have casted your first spell!")
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

def combat(success,protagonist,enemy):
    if success == True:
        Achievements.increase_streak()
        protagonist.attack(enemy)
        """Añadir un output de cuanto daño ha hecho al enemigo y cuanto le queda de vida al enemigo"""
    else:
        Achievements.reset_streak()
        enemy.attack(protagonist)
        """Añadir un output de cuanto daño ha hecho al protagonista y cuanto le queda de vida al protagonista"""
        


class Level:
    def __init__(self,protagonist,enemy_difficulty):
        self.enemy = Enemy(enemy_difficulty)
        self.protagonist = protagonist
        self.choose_tense_and_verb()
    def choose_tense_and_verb(self):
        self.verb_chosen = random.choice(verbs_most_used)
        self.chosen_form_nlp = random.choice(list(verbal_forms.keys()))
        self.form_chosen = verbal_forms[self.chosen_form_nlp]

    def play(self):
        print(api_gpt_call(prompt_first_round))
        input_text = input("Enter your phrase: ")
        success = self.check_tense(input_text)
        combat(success,self.protagonist,self.enemy)
        
        while self.enemy.hp > 0 and self.protagonist.hp > 0:
            print(api_gpt_call(prompt_second_rounds))
            input_text = input("Enter your phrase: ")
            success = self.check_tense(input_text)
            combat(success,self.protagonist,self.enemy)
        if self.enemy.hp == 0:
            print("You defeated the enemy")
        else:
            print("You lost the battle")
    def check_tense(self,input_text):
        doc = nlp(input_text)
        for token in doc:
            if token.lemma_ == self.verb_chosen:
                if token.tag_ == self.chosen_form_nlp:
                    return True
                else:
                    print("You used the wrong tense")
                    return False
            else:
                print("You used the wrong verb")
                return False

def main():
    Achievements()
    protagonist_name = input("Enter your name: ")
    protagonist = Protagonist(protagonist_name)
    for level_number in range(1, 6):
        level = Level(protagonist,level_number)
        level.play()
        Achievements.check_level()

if __name__ == "__main__":
    main()
