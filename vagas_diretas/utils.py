import re
import unicodedata
from difflib import SequenceMatcher


def normalizar(texto):
    texto = unicodedata.normalize("NFKD", texto or "")
    texto = "".join(c for c in texto if not unicodedata.combining(c)).lower()
    texto = re.sub(r"\b(ltda|s\.?a\.?|me|eireli|inc|corp)\b", " ", texto)
    return " ".join(re.sub(r"[^a-z0-9 ]+", " ", texto).split())


def similaridade(a, b):
    return SequenceMatcher(None, normalizar(a), normalizar(b)).ratio()


def contem_algum(texto, termos):
    t = normalizar(texto)
    return any(normalizar(x) in t for x in termos)