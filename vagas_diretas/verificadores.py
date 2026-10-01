import time
from urllib.parse import quote_plus

import requests
from bs4 import BeautifulSoup

from .rede import get
from .utils import similaridade


def casa(vaga, titulo, empresa, cfg):
    return (
        similaridade(empresa, vaga["empresa"]) >= cfg["similaridade_empresa_minima"]
        and similaridade(titulo, vaga["titulo"]) >= cfg["similaridade_titulo_minima"]
    )


def existe_no_linkedin(vaga, cfg):
    q = quote_plus(f"{vaga['titulo']} {vaga['empresa']}")
    loc = quote_plus(cfg["localizacao"])
    url = (
        "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobs/search"
        f"?keywords={q}&location={loc}&start=0"
    )
    try:
        r = get(url)
        if r.status_code != 200:
            return None
        soup = BeautifulSoup(r.text, "html.parser")
        for card in soup.select("li"):
            t = card.select_one(".base-search-card__title")
            e = card.select_one(".base-search-card__subtitle")
            if (
                t
                and e
                and casa(vaga, t.get_text(strip=True), e.get_text(strip=True), cfg)
            ):
                return True
        return False
    except requests.RequestException:
        return None


def existe_no_indeed(vaga, cfg):
    q = quote_plus(f"{vaga['titulo']} {vaga['empresa']}")
    loc = quote_plus(cfg["localizacao"])
    url = f"https://br.indeed.com/jobs?q={q}&l={loc}"
    try:
        r = get(url)
        if r.status_code != 200 or "captcha" in r.text.lower():
            return None
        soup = BeautifulSoup(r.text, "html.parser")
        for card in soup.select("div.job_seen_beacon"):
            t = card.select_one("h2.jobTitle")
            e = card.select_one("[data-testid='company-name']")
            if (
                t
                and e
                and casa(vaga, t.get_text(strip=True), e.get_text(strip=True), cfg)
            ):
                return True
        return False
    except requests.RequestException:
        return None


def verificar(vaga, cfg, cache):
    chave = vaga["link"]
    if chave in cache:
        return cache[chave]

    time.sleep(cfg["delay_segundos"])
    linkedin = existe_no_linkedin(vaga, cfg)
    time.sleep(cfg["delay_segundos"])
    indeed = existe_no_indeed(vaga, cfg)

    if linkedin or indeed:
        status = "descartada"
    elif linkedin is None or indeed is None:
        status = "nao_verificado"
    else:
        status = "exclusiva_do_site"

    resultado = {"linkedin": linkedin, "indeed": indeed, "status": status}
    cache[chave] = resultado
    return resultado