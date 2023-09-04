import spacy
import random
import openai


class Achievements:
    #This class is used to keep track of the achievements that the player has unlocked
    def __init__(self, protagonist):
        #This is a dictionary that stores the achievements that the player has unlocked
        self.streak = 0
        self.level = 1
        self.protagonist = protagonist
        self.achievements = {
            1: False,
            5: False,
            10: False,
            15: False
        }
#This method is used to check if the player has reached a certain level with certain conditions and protagonist earns extra damage.
    def check_level(self):
        if self.level == 2 and self.protagonist.hp == 100:
            self.protagonist.increase_dmg(10)
            print(
                "\n\nCongratulations!!! You have reached level 2 without taking any damage!")
        elif self.level == 4 and self.protagonist.hp >= 50:
            print(
                "\n\nCongratulations!!! You have reached level 4 with at least 50HP!")
        elif self.level == 6 and self.protagonist.hp == 100:
            print(
                "\n\nCongratulations!!! You are a beast!!! You have reached level 6 without taking any damage!")

    def increase_level(self):
        self.level += 1
        self.protagonist.increase_dmg(10)
        self.check_level()

    def increase_streak(self):
        self.streak += 1
        self.check_achievements()

    def reset_streak(self):
        self.streak = 0

#This method is used to check if the player has reached a certain achievement with certain conditions.
    def check_achievements(self):
        if self.streak >= 1 and not self.achievements[1]:
            self.protagonist.increase_dmg(5)
            print(
                "\n\nAchievement unlocked: Congratulations!!! You have casted your first spell! Your damage increased 5 points!!")
        if self.streak >= 5 and not self.achievements[5]:
            self.protagonist.increase_dmg(10)
            print(
                "\n\nAchievement unlocked: 5-streak! Your damage increased 5 points!!!")
            self.achievements[5] = True
        if self.streak >= 10 and not self.achievements[10]:
            self.protagonist.increase_dmg(20)
            print(
                "\n\nAchievement unlocked: 10-streak! Your damage increased 20 points!!!")
            self.achievements[10] = True
        if self.streak >= 15 and not self.achievements[20]:
            self.protagonist.increase_dmg(30)
            print(
                "\n\nAchievement unlocked: 15-streak! Your damage increased 30 points")
            self.achievements[15] = True


#This class is used to create the characters of the game
#The protagonist is the character that the player controls
#The enemy is the character that the player has to defeat
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
        super().__init__(name, hp=100, atk=30)

    def increase_dmg(self, amount):
        self.atk += amount


class Enemy(Character):
    def __init__(self, name, difficulty):
        super().__init__(name, hp=50 * difficulty, atk=10 * difficulty)

#This class is used to analyze the text that the player inputs
#It uses the spacy library to analyze the text
class TextAnalyzer:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_lg")

    def remove_auxiliary(self, doc):
        filtered_tokens = [
            token for token in doc if token.dep_ not in ["aux", "auxpass"] and not token.is_punct]
        return self.nlp(" ".join([token.text for token in filtered_tokens]))

    def compare_similarity(self, doc, doc2):
        filtered_doc2 = self.remove_auxiliary(doc2)
        filtered_doc = self.remove_auxiliary(doc)
        for token1, token2 in zip(filtered_doc, filtered_doc2):
            print(token1, "\n\n", token2)
            if token1.pos_ != "VERB" and token2.pos_ != "VERB":
                token_similarity = token1.similarity(token2)
                print(token_similarity)
                if token_similarity <= 0.98:
                    return False
        return True

    def check_tense(self, verb_chosen, chosen_form_nlp, input_text, original_phrase, chosen_form):
        doc = self.nlp(input_text)
        doc2 = self.nlp(original_phrase)

        if self.compare_similarity(doc, doc2):
            for i, token in enumerate(doc):
                if token.pos_ == "VERB" and token.lemma_ == verb_chosen and token.tag_ == chosen_form_nlp:
                    if chosen_form == "Future":
                        if i >= 1 and doc[i-1].lemma_ == "will":
                            return True
                        else:
                            print("\n\nYou have to use the modal verb 'will'")
                            return False
                    elif chosen_form == "Past continous":
                        if i >= 1 and doc[i-1].lemma_ == "be" and doc[i-1].tag_ == "VBD":
                            return True
                        else:
                            print("\n\nYou have to use the verb 'be' in past tense")
                            return False
                    elif chosen_form == "Present continous":
                        if i >= 1 and (doc[i-1].lemma_ == "be" and (doc[i-1].tag_ == "VBP" or doc[i-1].tag_ == "VBZ")):
                            return True
                        else:
                            print(
                                "\n\nYou have to use the verb 'be' in present tense")
                            return False
                    elif chosen_form == "Present perfect":
                        if i >= 1 and (doc[i-1].lemma_ == "have" and (doc[i-1].tag_ == "VBP" or doc[i-1].tag_ == "VBZ")):
                            return True
                        else:
                            print(
                                "\n\nYou have to use the verb 'have' in present tense")
                            return False
                    elif chosen_form == "Past perfect":
                        if i >= 1 and doc[i-1].lemma_ == "have" and doc[i-1].tag_ == "VBD":
                            return True
                        else:
                            print(
                                "\n\nYou have to use the verb 'have' in past tense")
                            return False
                    else:
                        return True
        else:
            print("\n\nYou used the wrong words")
            return False

#This class is used to call the OpenAI API
#It uses the OpenAI API to generate the text that the player will see
#It uses the OpenAI API to generate the phrase that the player will have to conjugate
class ApiGpt:
    def __init__(self):
        openai.api_key = ""

    def call_phrase(self, prompt):
        message = [
            {
                "role": "system",
                "content": "You are Stephen King writing a brief Lore of my game"
            },
            {
                "role": "user",
                "content": "Describe the area where the protagonist finds an enemy and speaks to the protagonist challenging him to a magic battle."
            },
            {
                "role": "assistant",
                "content": "In the fading light of dusk, the protagonist stumbled upon a forgotten graveyard nestled at the edge of the woods. The tombstones, weathered and leaning, whispered tales of long-forgotten souls. A mist hung in the air, weaving through the crooked trees like ghostly fingers. Suddenly, a rustling sound emerged from the shadows, and the enemy stepped forth, a figure clad in tattered rags with a malevolent gleam in their eyes.\"Seems you've gone into my domain,\\\" the enemy hissed, their voice like a chilling breeze. \\\"A place where lost souls rest eternally. And now, you shall face me in a battle of wills.\\\"\\n\\nProtagonist, your destiny shall be sealed once you will have confronted your fears. As the moon rises high above these ancient graves, the past and future converge in a dance of uncertainty. Will you emerge victorious, or will the shadows claim time yet to unfold.\\n\\nOriginal Phrase: You will use your magic.\\n\\nForm Chosen: Conjugate the phrase in the past simple tense.\" you? The choice, dear protagonist, lies in your hands and the echoes of"
            },
            {"role": "user", "content": prompt},
        ]
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=message,
            temperature=0.4,
            max_tokens=450,
            top_p=1,
            stop=None)
        return response.choices[0].message.content

    def call_area(self):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are Stephen King writing a brief Lore of my game"
                },
                {
                    "role": "user",
                    "content": "Describe the area where the protagonist finds an enemy and speaks to the protagonist challenging him to a magic battle."
                },
                {
                    "role": "assistant",
                    "content": "In the fading light of dusk, the protagonist stumbled upon a forgotten graveyard nestled at the edge of the woods. The tombstones, weathered and leaning, whispered tales of long-forgotten souls. A mist hung in the air, weaving through the crooked trees like ghostly fingers. Suddenly, a rustling sound emerged from the shadows, and the enemy stepped forth, a figure clad in tattered rags with a malevolent gleam in their eyes.\"Seems you've gone into my domain,\\\" the enemy hissed, their voice like a chilling breeze. \\\"A place where lost souls rest eternally. And now, you shall face me in a battle of wills.\\\"\\n\\nProtagonist, your destiny shall be sealed once you will have confronted your fears. As the moon rises high above these ancient graves, the past and future converge in a dance of uncertainty. Will you emerge victorious, or will the shadows claim time yet to unfold.\\n\\nOriginal Phrase: You will use your magic.\\n\\nForm Chosen: Conjugate the phrase in the past simple tense.\" you? The choice, dear protagonist, lies in your hands and the echoes of"
                },
                {
                    "role": "user",
                    "content": "Introduce the area where an enemy finds the protagonist and challenges the protagonist to a Batlle."
                }
            ],
            temperature=0.5,
            max_tokens=300,
            top_p=1,
            stop=None)
        return response.choices[0].message.content


#This class is used to create the levels of the game
#Each level has an enemy that the player has to defeat

class Level:
    def __init__(self, protagonist, level_number, achievements):
        self.enemy = Enemy("enemy", level_number)
        self.achievements = achievements
        self.protagonist = protagonist
        self.text_analyzer = TextAnalyzer()
        self.text_analyzer = self.text_analyzer
        self.api = ApiGpt()
        #This is a list of the most used verbs in the English language taken from enTenTen21 corpus
        self.verbs_most_used = ["be", "have", "do", "make", "use", "say", "get", "go", "take", "see", "know", "include", "come", "find", "give", "think", "work", "need", "look", "want", "provide", "help", "become", "start", "follow", "show", "call", "try", "create", "keep", "leave", "write", "tell", "play", "add", "feel", "run", "read", "allow", "put", "mean", "seem", "lead", "set", "offer", "ask", "bring", "hold", "build", "require", "continue", "learn",
                                "live", "move", "begin", "like", "receive", "let", "support", "develop", "consider", "change", "base", "turn", "pay", "believe", "meet", "love", "increase", "happen", "grow", "serve", "send", "understand", "remain", "hear", "lose", "appear", "accord", "buy", "win", "expect", "involve", "produce", "choose", "speak", "cause", "improve", "open", "apply", "talk", "report", "spend", "join", "sell", "cover", "enjoy", "pass", "reduce", "stop", "die"]
        #This is a dictionary that contains the verbal forms of the verbs that are used in the game, the key is the form in spacy
        self.verbal_forms = {
            "VB": "Future",
            "VBD": "Past simple",
            "VBG": ["Present continous", "Past continous"],
            "VBN": ["Present perfect", "Past perfect"],
            "VBP": "Present simple",
            "VBZ": "3rd person present simple"
        }
        self.prompt = "Generate a simple phrase with subject, verb, and complement using the verb: {verb_chosen}"
    #This method is used to choose a verb and a tense for the phrase that the player will have to conjugate
    def choose_tense_and_verb(self):
        self.verb_chosen = random.choice(self.verbs_most_used)
        self.chosen_form_nlp = random.choice(list(self.verbal_forms.keys()))
        self.tense_options = self.verbal_forms[self.chosen_form_nlp]
        if isinstance(self.tense_options, list):
            self.form_chosen = random.choice(self.tense_options)
        else:
            self.form_chosen = self.tense_options
    #This method contains the logic of the game
    def play(self):
        self.choose_tense_and_verb()
        self.formated_prompt = self.prompt.format(
            verb_chosen=self.verb_chosen, form_chosen=self.form_chosen)
        #This is the part where the area is generated
        gpt_msg = self.api.call_area()
        print("\n\n", gpt_msg)
        gpt_msg = self.api.call_phrase(self.formated_prompt)
        print("\n\n", gpt_msg)
        print("\n\nYou have to conjugate the phrase in the following form: ",
            self.form_chosen, "The main verb is: ", self.verb_chosen)
        input_text = input("\n\nEnter your phrase:")
        success = self.text_analyzer.check_tense(
            self.verb_chosen, self.chosen_form_nlp, input_text, gpt_msg, self.form_chosen)
        self.combat(success, self.protagonist, self.enemy)
        #This is the part where the combat is developed
        while self.enemy.hp > 0 and self.protagonist.hp > 0:
            self.choose_tense_and_verb()
            self.formated_prompt = self.prompt.format(
                verb_chosen=self.verb_chosen, form_chosen=self.form_chosen)
            gpt_msg = self.api.call_phrase(self.formated_prompt)
            print("\n\n", gpt_msg)
            print("\n\nYou have to conjugate the phrase in the following form: ",
                self.form_chosen, "The main verb is : ", self.verb_chosen)
            input_text = input("\n\nEnter your phrase:")
            success = self.text_analyzer.check_tense(
                self.verb_chosen, self.chosen_form_nlp, input_text, gpt_msg, self.form_chosen)
            self.combat(success, self.protagonist, self.enemy)
        if self.enemy.hp <= 0:
            print("\n\nYou defeated the enemy")
        else:
            print("\n\nYou lost the battle")
    #This method is used to calculate the damage that the player and the enemy will deal to each other
    def combat(self, success, protagonist, enemy):
        if success == True:
            protagonist.attack(enemy)
            self.achievements.increase_streak()
            print(
                "\n\nYour cast was successful!, you dealt damage to the enemy his hp is now: ", enemy.hp)
        else:
            enemy.attack(protagonist)
            self.achievements.reset_streak()
            print("\n\nYour cast was unsuccessful!, the enemy dealt damage to you, your hp is now: ", protagonist.hp)


def game_instructions():
    instructions = """
    **Game Objective:**
    You are the protagonist in a magical battle. Your goal is to defeat each enemy you encounter by correctly conjugating magical phrases in various tenses. As you progress through the levels, you'll face tougher enemies and more challenging conjugations.

    **Game Instructions:**

    1. **Enter Your Name:**
        - At the beginning of the game, enter your character's name when prompted.

    2. **Level Up:**
        - You start at Level 1 with full health (100 HP) and an initial damage of 30 points.

    3. **Game Levels:**
        - The game consists of 5 levels, each with a unique enemy to defeat.
        - To progress to the next level, you need to successfully defeat the current enemy by correctly conjugating magical phrases in the specified tense.

    4. **Battling an Enemy:**
        - Each level begins with a description of the area and the enemy challenging you to a magic battle.
        - You will be prompted to conjugate a magical phrase using a specific verb in a given tense.
        - Type your conjugated phrase in response to the prompt and hit Enter.

    5. **Conjugation Challenge:**
        - Conjugate the given verb in the specified tense.
        - If your conjugation is correct, you'll deal damage to the enemy based on your current damage points.
        - If your conjugation is incorrect, the enemy will attack, and your HP will decrease.

    6. **Achievements:**
        - You can earn achievements for casting successful spells in a streak.
        - Achievements grant you additional damage points.

    7. **Level Completion:**
        - Defeat the enemy by reducing their HP to zero to complete the level.
        - You'll automatically progress to the next level if you win.

    8. **Game Over:**
        - If your HP drops to zero at any point, you'll lose the game.
        - You can start a new game by rerunning the program.

    9. **Tense Types:**
        - You will encounter various verb tenses, including future, past simple, present continuous, past continuous, present perfect, and past perfect.

    10. **Use Verb Forms:**
        - Pay attention to the tense and form specified for each magical phrase prompt.
        - Make sure to use the correct verb form to cast the spell successfully.

    11. **Have Fun:**
        - Enjoy the magical battles and challenge yourself to progress through all five levels.

    Remember, your character's HP and damage points will carry over from one level to the next, so strategize and use your achievements wisely to conquer each level. Good luck and may your magical prowess lead you to victory!
    """

    print(instructions)


def main():
    protagonist_name = input("\n\nEnter your name:")
    protagonist = Protagonist(protagonist_name)
    achievements = Achievements(protagonist)
    game_instructions()
    for level_number in range(1, 6):
        level = Level(protagonist, level_number, achievements)
        level.play()
        if protagonist.hp <= 0:
            print("\n\nYou lost the game")
            break


if __name__ == "__main__":
    main()
