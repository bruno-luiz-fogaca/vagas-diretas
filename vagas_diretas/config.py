import json
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
ARQ_EMPRESAS = RAIZ / "empresas.json"
ARQ_SAIDA = RAIZ / "vagas_filtradas.json"
ARQ_CACHE = RAIZ / "cache_verificacoes.json"


def carregar_json(caminho, padrao=None):
    if caminho.exists():
        return json.loads(caminho.read_text(encoding="utf-8"))
    return padrao


def salvar_json(caminho, dados):
    caminho.write_text(
        json.dumps(dados, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def carregar_empresas():
    dados = carregar_json(ARQ_EMPRESAS)
    if not dados:
        raise SystemExit("empresas.json não encontrado")
    return dados["config"], dados["empresas"]