# vagas-diretas

Script em Python que procura vagas de estágio direto nas páginas de carreiras das empresas e descarta as que também aparecem no LinkedIn e no Indeed.

## Instalação

```
git clone https://github.com/SEU-USUARIO/vagas-diretas.git
cd vagas-diretas
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

No Linux e Mac, ative com `source .venv/bin/activate`.

## Uso

```
python -m vagas_diretas
```

O resultado fica em `vagas_filtradas.json`.

## Configuração

Tudo fica no `empresas.json`.

| Campo | O que faz |
|---|---|
| `palavras_chave` | termos que identificam estágio no título |
| `areas_de_interesse` | termos de área que o título precisa ter |
| `locais_aceitos` | só vagas cujo local contém um desses termos |
| `localizacao` | cidade usada na busca no LinkedIn e Indeed |
| `delay_segundos` | pausa entre as consultas |
| `similaridade_titulo_minima` | quão parecido o título precisa ser para contar como a mesma vaga |
| `similaridade_empresa_minima` | o mesmo para o nome da empresa |

Tipos de empresa:

| Tipo | Campos | Exemplo |
|---|---|---|
| `greenhouse` | `nome`, `token` | `job-boards.greenhouse.io/ebanx` usa o token `ebanx` |
| `lever` | `nome`, `token` | `jobs.lever.co/ciandt` usa o token `ciandt` |
| `html` | `nome`, `url` | página de carreiras com os links das vagas |

Para adicionar uma empresa, inclua uma linha em `empresas`:

```json
{ "nome": "Empresa X", "tipo": "html", "url": "https://empresax.com.br/carreiras" }
```

## Saída

```json
[
  {
    "titulo": "Estágio em Dados",
    "link": "https://job-boards.greenhouse.io/ebanx/jobs/123",
    "local": "Curitiba | On-site",
    "empresa": "Ebanx",
    "linkedin": false,
    "indeed": false,
    "status": "exclusiva_do_site"
  }
]
```

`exclusiva_do_site` significa que a vaga não foi achada no LinkedIn nem no Indeed. `nao_verificado` significa que alguma das consultas falhou e a vaga ficou na lista para conferir à mão.

## Testes

```
pip install -r requirements-dev.txt
python -m pytest
```

## Limitações

- LinkedIn e Indeed não têm API pública para isso. O script usa a busca pública deles, que pode mudar ou bloquear.
- O tipo `html` não funciona em páginas que carregam as vagas por JavaScript.

## Licença

MIT