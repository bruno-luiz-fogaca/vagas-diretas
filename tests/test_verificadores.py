import pytest

from vagas_diretas import verificadores

CFG = {
    "delay_segundos": 0,
    "localizacao": "Curitiba",
    "similaridade_titulo_minima": 0.6,
    "similaridade_empresa_minima": 0.8,
}
VAGA = {"titulo": "Estágio em Python", "empresa": "Acme", "link": "https://acme.com/1"}


@pytest.fixture(autouse=True)
def sem_espera(monkeypatch):
    monkeypatch.setattr(verificadores.time, "sleep", lambda s: None)


def simular(monkeypatch, linkedin, indeed):
    monkeypatch.setattr(verificadores, "existe_no_linkedin", lambda v, c: linkedin)
    monkeypatch.setattr(verificadores, "existe_no_indeed", lambda v, c: indeed)


def test_descarta_se_achou_no_linkedin(monkeypatch):
    simular(monkeypatch, True, False)
    assert verificadores.verificar(VAGA, CFG, {})["status"] == "descartada"


def test_descarta_se_achou_no_indeed(monkeypatch):
    simular(monkeypatch, False, True)
    assert verificadores.verificar(VAGA, CFG, {})["status"] == "descartada"


def test_exclusiva_se_nao_achou_em_nenhum(monkeypatch):
    simular(monkeypatch, False, False)
    assert verificadores.verificar(VAGA, CFG, {})["status"] == "exclusiva_do_site"


def test_nao_verificado_se_algum_falhou(monkeypatch):
    simular(monkeypatch, False, None)
    assert verificadores.verificar(VAGA, CFG, {})["status"] == "nao_verificado"


def test_descarta_mesmo_se_o_outro_falhou(monkeypatch):
    simular(monkeypatch, True, None)
    assert verificadores.verificar(VAGA, CFG, {})["status"] == "descartada"


def test_usa_cache_sem_consultar_de_novo(monkeypatch):
    def nao_deve_chamar(v, c):
        raise AssertionError("consultou de novo")

    monkeypatch.setattr(verificadores, "existe_no_linkedin", nao_deve_chamar)
    monkeypatch.setattr(verificadores, "existe_no_indeed", nao_deve_chamar)
    cache = {
        VAGA["link"]: {
            "linkedin": False,
            "indeed": False,
            "status": "exclusiva_do_site",
        }
    }

    assert verificadores.verificar(VAGA, CFG, cache)["status"] == "exclusiva_do_site"