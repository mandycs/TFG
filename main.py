import spacy
import random
import openai


def game_instructions():
    print("Welcome to the Legend of the Verbs!\nIn this game, you will control a protagonist and engage in battles with enemies")
    print("You will learn how to use the modal verbs\nYou will have to attack the enemies using modal verbs")
    print("You will have to use the correct modal verb to defeat the enemy\nIf you use the wrong modal verb, you will lose your turn")
    print("You will have 100HP and the enemy will have HP according to the difficulty level")


class Achievements:
    def __init__(self, protagonist):
        self.streak = 0
        self.level = 1
        self.protagonist = protagonist
        self.achievements = {
            1: False,
            5: False,
            10: False,
            15: False
        }

    def check_level(self):
        if self.level == 2 and self.protagonist.hp == 100:
            self.protagonist.increase_dmg(10)
            print(
                "\n\nCongratulations!!! You have reached level 2 without taking any damage!\n\n")
        elif self.level == 4 and self.protagonist.hp >= 50:
            print(
                "\n\nCongratulations!!! You have reached level 4 with at least 50HP!\n\n")
        elif self.level == 6 and self.protagonist.hp == 100:
            print(
                "\n\nCongratulations!!! You are a beast!!! You have reached level 6 without taking any damage!\n\n")

    def increase_level(self):
        self.level += 1
        self.protagonist.increase_dmg(10)
        self.check_level()

    def increase_streak(self):
        self.streak += 1
        self.check_achievements()

    def reset_streak(self):
        self.streak = 0

    def check_achievements(self):
        if self.streak >= 1 and not self.achievements[1]:
            self.protagonist.increase_dmg(5)
            print(
                "\n\nAchievement unlocked: Congratulations!!! You have casted your first spell! Your damage increased 5 points!!\n\n")
        if self.streak >= 5 and not self.achievements[5]:
            self.protagonist.increase_dmg(10)
            print(
                "\n\nAchievement unlocked: 5-streak! Your damage increased 5 points!!!\n\n")
            self.achievements[5] = True
        if self.streak >= 10 and not self.achievements[10]:
            self.protagonist.increase_dmg(20)
            print(
                "\n\nAchievement unlocked: 10-streak! Your damage increased 20 points!!!\n\n")
            self.achievements[10] = True
        if self.streak >= 15 and not self.achievements[20]:
            self.protagonist.increase_dmg(30)
            print(
                "\n\nAchievement unlocked: 15-streak! Your damage increased 30 points\n\n")
            self.achievements[15] = True


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
                            print("You have to use the modal verb 'will'")
                            return False
                    elif chosen_form == "Past continous":
                        if i >= 1 and doc[i-1].lemma_ == "be" and doc[i-1].tag_ == "VBD":
                            return True
                        else:
                            print("You have to use the verb 'be' in past tense")
                            return False
                    elif chosen_form == "Present continous":
                        if i >= 1 and (doc[i-1].lemma_ == "be" and (doc[i-1].tag_ == "VBP" or doc[i-1].tag_ == "VBZ")):
                            return True
                        else:
                            print("You have to use the verb 'be' in present tense")
                            return False
                    elif chosen_form == "Present perfect":
                        if i >= 1 and (doc[i-1].lemma_ == "have" and (doc[i-1].tag_ == "VBP" or doc[i-1].tag_ == "VBZ")):
                            return True
                        else:
                            print("You have to use the verb 'have' in present tense")
                            return False
                    elif chosen_form == "Past perfect":
                        if i >= 1 and doc[i-1].lemma_ == "have" and doc[i-1].tag_ == "VBD":
                            return True
                        else:
                            print("You have to use the verb 'have' in past tense")
                            return False
                    else:
                        print("You used the correct verb")
                        return True
        else:
            print("You used the wrong words")
            return False


class Game:
    def __init__(self):
        openai.api_key = ""

    def api_gpt_call_phrase(self, prompt):
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

    def api_gpt_call_area(self):
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

    def combat(self, success, protagonist, enemy):
        if success == True:
            protagonist.attack(enemy)
            print(
                "\n\nYour cast was successful!, you dealt damage to the enemy his hp is now: ", enemy.hp, "\n\n")
        else:
            enemy.attack(protagonist)
            print(
                "\n\nYour cast was unsuccessful!, the enemy dealt damage to you, your hp is now: ", protagonist.hp, "\n\n")


class Level:
    def __init__(self, protagonist, level_number, achievements):
        self.enemy = Enemy("enemy", level_number)
        self.achievements = achievements
        self.protagonist = protagonist
        self.text_analyzer = TextAnalyzer()
        self.text_analyzer = self.text_analyzer
        self.game = Game()
        self.verbs_most_used = ["be", "have", "do", "make", "use", "say", "get", "go", "take", "see", "know", "include", "come", "find", "give", "think", "work", "need", "look", "want", "provide", "help", "become", "start", "follow", "show", "call", "try", "create", "keep", "leave", "write", "tell", "play", "add", "feel", "run", "read", "allow", "put", "mean", "seem", "lead", "set", "offer", "ask", "bring", "hold", "build", "require", "continue", "learn",
                                "live", "move", "begin", "like", "receive", "let", "support", "develop", "consider", "change", "base", "turn", "pay", "believe", "meet", "love", "increase", "happen", "grow", "serve", "send", "understand", "remain", "hear", "lose", "appear", "accord", "buy", "win", "expect", "involve", "produce", "choose", "speak", "cause", "improve", "open", "apply", "talk", "report", "spend", "join", "sell", "cover", "enjoy", "pass", "reduce", "stop", "die"]
        self.verbal_forms = {
            "VB": "Future",
            "VBD": "Past simple",
            "VBG": ["Present continous", "Past continous"],
            "VBN": ["Present perfect", "Past perfect"],
            "VBP": "Present simple",
            "VBZ": "3rd person present simple"
        }
        self.prompt = "Generate a simple phrase with subject, verb, and complement using the verb: {verb_chosen}"

    def choose_tense_and_verb(self):
        self.verb_chosen = random.choice(self.verbs_most_used)
        self.chosen_form_nlp = random.choice(list(self.verbal_forms.keys()))
        self.tense_options = self.verbal_forms[self.chosen_form_nlp]
        if isinstance(self.tense_options, list):
            self.form_chosen = random.choice(self.tense_options)
        else:
            self.form_chosen = self.tense_options

    def play(self):
        self.choose_tense_and_verb()
        self.formated_prompt = self.prompt.format(
            verb_chosen=self.verb_chosen, form_chosen=self.form_chosen)
        gpt_msg = self.game.api_gpt_call_area()
        print("\n\n", gpt_msg, "\n\n")
        gpt_msg = self.game.api_gpt_call_phrase(self.formated_prompt)
        print("\n\n", gpt_msg)
        print("\n\nYou have to conjugate the phrase in the following form: ",
            self.form_chosen, "\n\n")
        input_text = input("\n\nEnter your phrase:")
        success = self.text_analyzer.check_tense(
            self.verb_chosen, self.chosen_form_nlp, input_text, gpt_msg, self.form_chosen)
        if success == True:
            self.achievements.increase_streak()
        else:
            self.achievements.reset_streak()
        self.game.combat(success, self.protagonist, self.enemy)

        while self.enemy.hp > 0 and self.protagonist.hp > 0:
            self.choose_tense_and_verb()
            self.formated_prompt = self.prompt.format(
                verb_chosen=self.verb_chosen, form_chosen=self.form_chosen)
            gpt_msg = self.game.api_gpt_call_phrase(self.formated_prompt)
            print("\n\n", gpt_msg)
            print("\n\nYou have to conjugate the phrase in the following form: ",
                self.form_chosen, "\n\n")
            input_text = input("\n\nEnter your phrase:")
            success = self.text_analyzer.check_tense(
                self.verb_chosen, self.chosen_form_nlp, input_text, gpt_msg, self.form_chosen)
            if success == True:
                self.achievements.increase_streak()
            else:
                self.achievements.reset_streak()
            self.game.combat(success, self.protagonist, self.enemy)
        if self.enemy.hp <= 0:
            print("\n\nYou defeated the enemy\n\n")
        else:
            print("\n\nYou lost the battle\n\n")


def main():
    protagonist_name = input("\n\nEnter your name: ")
    protagonist = Protagonist(protagonist_name)
    achievements = Achievements(protagonist)
    for level_number in range(1, 6):
        level = Level(protagonist, level_number, achievements)
        level.play()


if __name__ == "__main__":
    main()
