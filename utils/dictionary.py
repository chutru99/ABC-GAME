import pickle

def load_words():
    """Carga el diccionario de palabras desde resources/words.pkl."""
    with open("resources/words.pkl", "rb") as f:
        return pickle.load(f)
