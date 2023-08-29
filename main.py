import spacy
import random
import requests

api_url = "https://api.openai.com/v1/engines/davinci-codex/completions"

api_key = "YOUR_API_KEY"

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}

verbal_forms = {"VBG":"Present continous","VBN":"Past participle","VBD":"Past simple","VBZ":"Present simple(3rd Person)","VBP":"Present simple","VH":"Future","VHD":"Past perfect","VHN":"Past Participle","VHP":"Present Perfect","VHZ":"Present Perfect(3rd person)","VVN":"Past Participle"}

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
    def __init__(self,protagonist):
        self.streak = 0
        self.level = 1
        self.protagonist = protagonist
        self.achievements = {
            1: False,
            5: False,
            10: False,
            20: False
        }

    def check_level(self):
        if self.level == 2 and self.protagonist.hp == 100:
            print("Congratulations!!! You have reached level 2 without taking any damage!")
        elif self.level == 4 and self.protagonist.hp >= 50:
            print("Congratulations!!! You have reached level 4 with at least 50HP!")
        elif self.level == 6 and self.protagonist.hp == 100:
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
        print("Your cast was successful!, you dealt damage to the enemy his hp is now: ", enemy.hp)
    else:
        Achievements.reset_streak()
        enemy.attack(protagonist)
        print("Your cast was unsuccessful!, the enemy dealt damage to you, your hp is now: ", protagonist.hp)
        

class TextAnalyzer:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_lg")
    
    def remove_auxiliary(self, doc):
        filtered_tokens = [token for token in doc if token.dep_ not in ["aux", "auxpass"]]
        return self.nlp(" ".join([token.text for token in filtered_tokens]))
    
    def compare_similarity(self, doc, doc2):
        filtered_doc2 = self.remove_auxiliary(doc2)
        filtered_doc = self.remove_auxiliary(doc)
        for token1, token2 in zip(filtered_doc, filtered_doc2):
            if token1.pos_ != "VERB" and token2.pos_ != "VERB":
                token_similarity = token1.similarity(token2)
                if token_similarity <= 0.98:
                    return False
        return True
    
    def check_tense(self, verb_chosen, chosen_form_nlp, input_text, original_phrase):
        doc = self.nlp(input_text)
        doc2 = self.nlp(original_phrase)
        if self.compare_similarity(doc, doc2):
            for token in doc:
                if token.pos_ == "VERB":
                    if token.lemma_ == verb_chosen and token.tag_ == chosen_form_nlp:
                        return True
                    elif token.lemma_ != verb_chosen:
                        print("You used the wrong verb")
                        return False
                    else:
                        print("You used the wrong tense")
                        return False
        else:
            print("You used some different words")
            return False
    
    def find_original_phrase(self, gpt_msg):
        doc = self.nlp(gpt_msg)
        #localizar la frase original que ha generado gpt para que el jugador la reformmule

class Level:
    def __init__(self,protagonist,enemy_difficulty,text_analyzer):
        self.enemy = Enemy(enemy_difficulty)
        self.protagonist = protagonist
        self.text_analyzer = text_analyzer
        self.choose_tense_and_verb()
    def choose_tense_and_verb(self):
        self.verb_chosen = random.choice(verbs_most_used)
        self.chosen_form_nlp = random.choice(list(verbal_forms.keys()))
        self.form_chosen = verbal_forms[self.chosen_form_nlp]

    def play(self):
        gpt_msg = api_gpt_call(prompt_first_round)
        print(gpt_msg)
        original_phrase = self.text_analyzer.find_original_phrase(gpt_msg)
        input_text = input("Enter your phrase: ")
        success = self.text_analyzer.check_tense(TextAnalyzer,input_text,self.verb_chosen,self.chosen_form_nlp,original_phrase)
        combat(success,self.protagonist,self.enemy)
        
        while self.enemy.hp > 0 and self.protagonist.hp > 0:
            gpt_msg = api_gpt_call(prompt_second_rounds)
            input_text = input("Enter your phrase: ")
            original_phrase = self.text_analyzer.find_original_phrase(gpt_msg)
            success = self.text_analyzer.check_tense(input_text,self.verb_chosen,self.chosen_form_nlp,original_phrase)
            combat(success,self.protagonist,self.enemy)
        if self.enemy.hp == 0:
            print("You defeated the enemy")
        else:
            print("You lost the battle")

def main():
    text_analyzer = TextAnalyzer()
    protagonist_name = input("Enter your name: ")
    protagonist = Protagonist(protagonist_name)
    achievements = Achievements(protagonist)
    for level_number in range(1, 6):
        level = Level(protagonist,level_number,text_analyzer)
        level.play()
        achievements.check_level()

if __name__ == "__main__":
    main()
