import spacy
import random
import requests
api_url = "https://api.openai.com/v1/engines/davinci-codex/completions"
api_key = "YOUR_API_KEY"

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}

prompt_first_round = ""

verbs_most_used = ["be","have","do","make","use","say","get","go","take","see","know","include","come","find","give","think","work","need","look","want","provide","help","become","start","follow","show","call","try","create","keep","leave","write","tell","play","add","feel","run","read","allow","put","mean","seem","lead","set","offer","ask","bring","hold","build","require","continue","learn","live","move","begin","like","receive","let","support","develop","consider","change","base","turn","pay","believe","meet","love","increase","happen","grow","serve","send","understand","remain","hear","lose","appear","accord","buy","win","expect","involve","produce","choose","speak","cause","improve","open","apply","talk","report","spend","join","sell","cover","enjoy","pass","reduce","stop","die"]

verbal_forms = {"VBG":"Present continous","VBN":"Past participle","VBD":"Past simple","VB":"Base form","VBZ":"Present simple(3rd Person)","VBP":"Present simple","VH":"Future","VHD":"Past perfect","VHN":"Past Participle","VHP":"Present Perfect","VHZ":"Present Perfect(3rd person)","VVN":"Past Participle"}
nlp = spacy.load("en_core_web_lg")

def choose_tense_and_verb():
    verb_chosen = random.choice(verbs_most_used)
    form_chosen_nlp = random.choice(list(verbal_forms.keys()))
    form_chosen = verbal_forms[form_chosen_nlp]
    return verb_chosen, form_chosen,form_chosen_nlp

def api_gpt_call(prompt, verb_chosen, form_chosen):
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

class Character:
    def __init__(self, name, hp, atk):
        self.name = name
        self.hp = hp
        self.atk = atk

    def take_damage(self, damage):  # damage is an integer      
        self.hp -= damage

    def attack(self, enemy):
        enemy.take_damage(self.atk)

class Protagonist(Character):
    def __init__(self, name):
        super().__init__(name, hp=100, atk=20)

class Enemy(Character):
    def __init__(self, name, difficulty):
        super().__init__(name, hp = 50 * difficulty, atk = 10 * difficulty)
        
def check_tense(input_text,form_chosen_nlp,verb_chosen):
    doc = nlp(input_text)
    for token in doc:
        if token.lemma_ == verb_chosen:
            if token.tag_ == form_chosen_nlp:
                return True
            else:
                print("You used the wrong tense")
                return False
        else:
            print("You used the wrong verb")
            return False

def level_1(protagonist, enemy):
    verb_result,form_result,form_nlp_result = choose_tense_and_verb()
    print(api_gpt_call(prompt_first_round,verb_result,form_result))
    input_text = input("Enter your phrase: ")
    success = check_tense(input_text,form_nlp_result,verb_result)
    if success == True:
        protagonist.attack(enemy)
        print(f"You have attacked the enemy with {verb_result} in {form_result}")
    """print("You have completed Level 1!")"""

# Define more levels and enemies for each level
def game_instructions():
    print("Welcome to the Legend of the Verbs!\nIn this game, you will control a protagonist and engage in battles with enemies")
    print("You will learn how to use the modal verbs\nYou will have to attack the enemies using modal verbs")
    print("You will have to use the correct modal verb to defeat the enemy\nIf you use the wrong modal verb, you will lose your turn")
    print("You will have 100HP and the enemy will have HP according to the difficulty level")

def main():
    protagonist_name = input("Enter the name of your protagonist: ")
    protagonist = Protagonist(protagonist_name)

    level_1(protagonist)
    # Call more level functions here

if __name__ == "__main__":
    main()
