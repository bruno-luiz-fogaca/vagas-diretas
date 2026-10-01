from vagas_diretas.utils import contem_algum, normalizar, similaridade


def test_normalizar_remove_acentos_e_sufixos():
    assert normalizar("Açaí Tecnologia LTDA") == "acai tecnologia"


def test_similaridade_titulos_parecidos():
    assert similaridade("Estágio Python", "Estagiario Python") >= 0.6


def test_similaridade_titulos_diferentes():
    assert similaridade("Estágio Python", "Analista Financeiro Sênior") < 0.6


def test_contem_algum_encontra_termo():
    assert contem_algum("Estágio em Desenvolvimento", ["estagio"])


def test_contem_algum_sem_termo():
    assert not contem_algum("Analista Sênior", ["estagio", "trainee"])