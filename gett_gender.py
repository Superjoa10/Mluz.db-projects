import gender_guesser.detector as gender, pyautogui as gui
def get_gender(prompt):
    L = gender.Detector()
    result = (L.get_gender(prompt))
    if result  == "male":
        return["senhor", "do", "o"]
    elif result == "mostly male":
        return["senhor", "do", "o"]
    elif result == "female":
        return["senhora", "da", "a"]
    elif result == "mostly female":
        return["senhora", "da", "a"]
    elif result == "andy":
        real_result = gui.prompt(f"""Erro ao detectar pronome! especifique o mesmo. Nome {prompt}:
        Como gostaria de ser referido? Senhor ou senhora? """)
        if real_result == "senhor":
            return ["senhor", "do", "o"]
        elif real_result == "senhora":
            return ["senhora", "da", "a"]
    else:
        gui.alert(text='Erro ao detectar pronome! Retorne ao console e especifique o mesmo.', title='Erro!!', button='OK')
        real_result = gui.prompt(f"""Erro ao detectar pronome! especifique o mesmo. Nome {prompt}:
        Como gostaria de ser referido? Senhor ou senhora? """)
        if real_result == "senhor":
            return ["senhor", "do", "o"]
        elif real_result == "senhora":
            return ["senhora", "da", "a"]