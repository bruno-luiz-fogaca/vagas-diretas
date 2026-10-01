from vagas_diretas import coletores

CFG = {
    "palavras_chave": ["estágio", "estagio"],
    "areas_de_interesse": ["python", "dados"],
    "locais_aceitos": ["curitiba", "remoto"],
}


class RespostaFalsa:
    def __init__(self, json_data=None, text=""):
        self._json_data = json_data
        self.text = text

    def json(self):
        return self._json_data


def test_greenhouse_filtra_estagio_area_e_local(monkeypatch):
    dados = {
        "jobs": [
            {
                "title": "Estágio em Python",
                "absolute_url": "https://x.com/1",
                "location": {"name": "Curitiba | On-site"},
            },
            {
                "title": "Estágio em Marketing",
                "absolute_url": "https://x.com/2",
                "location": {"name": "Curitiba"},
            },
            {
                "title": "Estágio em Dados",
                "absolute_url": "https://x.com/3",
                "location": {"name": "São Paulo"},
            },
            {
                "title": "Desenvolvedor Python Sênior",
                "absolute_url": "https://x.com/4",
                "location": {"name": "Curitiba"},
            },
        ]
    }
    monkeypatch.setattr(
        coletores, "get", lambda url, **kw: RespostaFalsa(json_data=dados)
    )
    empresa = {"nome": "Acme", "tipo": "greenhouse", "token": "acme"}

    vagas = coletores.coletar_vagas(empresa, CFG)

    assert [v["titulo"] for v in vagas] == ["Estágio em Python"]
    assert vagas[0]["empresa"] == "Acme"


def test_lever_aceita_vaga_remota(monkeypatch):
    dados = [
        {
            "text": "Estágio em Dados",
            "hostedUrl": "https://jobs.lever.co/acme/1",
            "categories": {"location": "Remoto, Brasil"},
        },
        {
            "text": "Gerente Comercial",
            "hostedUrl": "https://jobs.lever.co/acme/2",
            "categories": {},
        },
    ]
    monkeypatch.setattr(
        coletores, "get", lambda url, **kw: RespostaFalsa(json_data=dados)
    )
    empresa = {"nome": "Acme", "tipo": "lever", "token": "acme"}

    vagas = coletores.coletar_vagas(empresa, CFG)

    assert [v["titulo"] for v in vagas] == ["Estágio em Dados"]


def test_html_resolve_links_e_remove_duplicados(monkeypatch):
    html = """
        <a href="/vagas/1">Estágio em Dados</a>
        <a href="/vagas/1">Estágio em Dados</a>
        <a href="/sobre">Sobre nós</a>
    """
    monkeypatch.setattr(coletores, "get", lambda url, **kw: RespostaFalsa(text=html))
    empresa = {"nome": "Acme", "tipo": "html", "url": "https://acme.com/carreiras"}

    vagas = coletores.coletar_vagas(empresa, CFG)

    assert len(vagas) == 1
    assert vagas[0]["link"] == "https://acme.com/vagas/1"


def test_erro_de_rede_retorna_lista_vazia(monkeypatch):
    def falha(url, **kw):
        raise RuntimeError("sem conexão")

    monkeypatch.setattr(coletores, "get", falha)
    empresa = {"nome": "Acme", "tipo": "lever", "token": "acme"}

    assert coletores.coletar_vagas(empresa, CFG) == []


def test_tipo_desconhecido_retorna_lista_vazia():
    empresa = {"nome": "Acme", "tipo": "inexistente"}

    assert coletores.coletar_vagas(empresa, CFG) == []