import spacy

text = "She will go to the cinema tomorrow"
print (text)

def check_tense(text):
    nlp = spacy.load("en_core_web_lg")
    doc = nlp(text)
    for token in doc:
        if token.pos_ == "VERB":
            tense = token.tag_
            print(token.text)
            if tense.startswith("VB"):
                if "Fut" in tense:
                    print(tense, "This is the future tense")
                else:
                    print(tense, "This is a verb form, but not the future tense")
            else:
                print("Error")


def main():
    check_tense(text)
    return

if __name__ == "__main__":
    main()
