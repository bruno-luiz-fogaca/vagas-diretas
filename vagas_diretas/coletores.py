from urllib.parse import urljoin

from bs4 import BeautifulSoup

from .rede import get
from .utils import contem_algum


def vagas_greenhouse(empresa):
    url = f"https://boards-api.greenhouse.io/v1/boards/{empresa['token']}/jobs"
    dados = get(url).json()
    return [
        {
            "titulo": j["title"],
            "link": j["absolute_url"],
            "local": (j.get("location") or {}).get("name", ""),
        }
        for j in dados.get("jobs", [])
    ]


def vagas_lever(empresa):
    url = f"https://api.lever.co/v0/postings/{empresa['token']}?mode=json"
    dados = get(url).json()
    return [
        {
            "titulo": j["text"],
            "link": j["hostedUrl"],
            "local": (j.get("categories") or {}).get("location", ""),
        }
        for j in dados
    ]


def vagas_html(empresa):
    resp = get(empresa["url"])
    soup = BeautifulSoup(resp.text, "html.parser")
    vagas, vistos = [], set()
    for a in soup.find_all("a", href=True):
        titulo = " ".join(a.get_text(" ", strip=True).split())
        link = urljoin(empresa["url"], a["href"])
        if len(titulo) < 4 or link in vistos:
            continue
        vistos.add(link)
        vagas.append({"titulo": titulo, "link": link, "local": ""})
    return vagas


COLETORES = {
    "greenhouse": vagas_greenhouse,
    "lever": vagas_lever,
    "html": vagas_html,
}


def local_aceito(local, locais):
    if not locais or not local:
        return True
    return contem_algum(local, locais)


def coletar_vagas(empresa, cfg):
    coletor = COLETORES.get(empresa["tipo"])
    if not coletor:
        print(f"  tipo desconhecido: {empresa['tipo']}")
        return []
    try:
        todas = coletor(empresa)
    except Exception as e:
        print(f"  erro ao coletar {empresa['nome']}: {e}")
        return []

    vagas = []
    for v in todas:
        if not contem_algum(v["titulo"], cfg["palavras_chave"]):
            continue
        if not contem_algum(v["titulo"], cfg["areas_de_interesse"]):
            continue
        if not local_aceito(v["local"], cfg.get("locais_aceitos")):
            continue
        v["empresa"] = empresa["nome"]
        vagas.append(v)
    return vagas