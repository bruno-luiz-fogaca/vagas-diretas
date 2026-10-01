from .coletores import coletar_vagas
from .config import ARQ_CACHE, ARQ_SAIDA, carregar_empresas, carregar_json, salvar_json
from .verificadores import verificar


def main():
    cfg, empresas = carregar_empresas()
    cache = carregar_json(ARQ_CACHE, {})

    mantidas = []
    descartadas = 0
    for empresa in empresas:
        print(f"\n{empresa['nome']}")
        vagas = coletar_vagas(empresa, cfg)
        print(f"  {len(vagas)} vaga(s) de estágio na área")

        for vaga in vagas:
            res = verificar(vaga, cfg, cache)
            vaga.update(res)
            if res["status"] == "descartada":
                descartadas += 1
                print(f"  descartada: {vaga['titulo']}")
            else:
                mantidas.append(vaga)
                print(f"  mantida: {vaga['titulo']} ({res['status']})")

    salvar_json(ARQ_SAIDA, mantidas)
    salvar_json(ARQ_CACHE, cache)
    print(f"\nmantidas: {len(mantidas)} | descartadas: {descartadas}")
    print(f"resultado em {ARQ_SAIDA}")