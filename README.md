# Adaptive Orchestration

Skill em português para escolher o modelo de melhor custo-benefício em cada parte de um trabalho e coordenar subagentes com contratos e verificação. Funciona no Claude Code e no Codex com o mesmo `SKILL.md`. Combina [três guias de origem e o Artificial Analysis](references/sources.md).

## Instalação

| CLI | Pasta pessoal | Pasta do projeto | Invocação |
|---|---|---|---|
| Claude Code | `~/.claude/skills/adaptive-orchestration/` | `.claude/skills/adaptive-orchestration/` | `/adaptive-orchestration <pedido>` |
| Codex | `~/.agents/skills/adaptive-orchestration/` | `.agents/skills/adaptive-orchestration/` | `$adaptive-orchestration <pedido>` |

```sh
git clone https://github.com/carlos-ssa/adaptive-orchestration.git ~/.claude/skills/adaptive-orchestration
```

Troque o destino para a pasta do Codex se for o caso. Em outra CLI, forneça [SKILL.md](SKILL.md) como instrução e mantenha as referências acessíveis. `agents/openai.yaml` só é lido pelo Codex.

## Dados de custo-benefício

A escolha de modelos usa um retrato local do [Artificial Analysis](https://artificialanalysis.ai/), gerado pela API gratuita:

```sh
export AA_API_KEY=...   # chave gratuita em artificialanalysis.ai
python scripts/aa_snapshot.py --creators anthropic,openai
```

Os scripts usam só a biblioteca padrão do Python. O retrato fica em `data/` (ignorado pelo Git) e só é atualizado se tiver mais de 7 dias. Para escolher um modelo, cruze capacidade na área, custo no perfil de uso (entrada, cache, saída e verbosidade) e velocidade:

```sh
python scripts/aa_rank.py --perfil codigo --capacidade eng --min 50 --creators anthropic,openai --cli claude-code
```

`--cli claude-code` sugere apelido e esforço; `--cli codex` sugere slug e a chave TOML `model_reasoning_effort`. Confirme o schema e a política da sessão antes de enviar parâmetros. `--available slug-a,slug-b` restringe aos slugs previamente mapeados para modelos disponíveis; sem ele, a lista não confirma disponibilidade. Retratos com mais de sete dias são rejeitados; `--allow-stale` permite uso identificado como hipótese datada. Sem dados comparáveis, veja [Claude Code](references/claude-code.md#partida-sem-dados) ou [Codex](references/codex.md#partida-sem-dados). Os dados exigem atribuição ao Artificial Analysis e não devem ser redistribuídos.

Registre cada bloco em `data/calibracao.jsonl` e consulte o resumo para calibrar os pisos (detalhes em [Calibração](references/model-selection.md#calibração)):

```sh
python scripts/aa_log.py --faixa 2 --tipo codigo --modelo executor --esforco medium --resultado aceito
python scripts/aa_log.py --resumo
```

## Testes dos scripts

Testes locais com retrato sintético, só com a biblioteca padrão e sem API:

```sh
python -m unittest discover -s tests -v
```

## Como escolhe

| Faixa | Trabalho | Executor |
|---|---|---|
| 0 | Contagem, filtro, busca exata | Script, sem modelo |
| 1 | Leitura extensa, extração, triagem | Modelo leve, esforço baixo |
| 2 | Código delimitado, migração mecânica, revisão | Modelo intermediário, esforço médio |
| 3 | Ambiguidade, arquitetura, integração, decisão | Principal |

Os modelos de cada faixa vêm de `preferences.local.md` (opcional, ignorado pelo Git) ou do retrato cruzado com o que a CLI oferece e permite selecionar. Sem evidência suficiente, preserve a seleção herdada. Em assinatura, confirme cotas e créditos aplicáveis; preço de API não prova consumo de assinatura. Veja [seleção de modelos](references/model-selection.md) e o [exemplo de preferências](references/environment.md#preferências-opcionais).

## Conteúdo

- [SKILL.md](SKILL.md): ponto de entrada, faixas e regras de coordenação.
- [Claude Code](references/claude-code.md) e [Codex](references/codex.md): parâmetros de delegação de cada CLI.
- [Modelos](references/model-selection.md): retrato, métricas e escolha sem dados.
- [Ambiente](references/environment.md): outras CLIs, concorrência, subdelegação e preferências.
- [Fluxos](references/workflows.md), [contratos](references/contracts.md) e [exemplos](references/examples.md).
- [Fontes](references/sources.md) e [cenários de validação](evals/README.md).

## Limites e licença

A [auditoria de 13/11/2026](evals/audit-2026-11-13.md) registra correções, testes e limites da comparação. O piloto reproduzível `python evals/run_pilot.py --output <pasta-nova> --cli codex` também aceita `--cli claude`; requer a CLI instalada e autenticada. Não instala ferramentas. A execução A/B no Codex CLI local encontrou falha de infraestrutura; não há comprovação de redução de 20% em tokens ou cota.

A skill não muda configuração global nem o modelo principal, não instala ferramentas e não autoriza ações externas fora do pedido. Rankings orientam candidatos; a economia real depende dos resultados e da cobrança do ambiente. A [rodada 3, Parte C](evals/round3-2026-11-12.md#parte-c-execução-nativa-no-claude-code) validou neste ambiente a delegação nativa no Claude Code com modelo/esforço selecionados e verificação por script, em logs sintéticos. A economia de cota em tarefas reais continua sem comprovação; veja [evals](evals/README.md).

Distribuída sob a [licença MIT](LICENSE). Conteúdos dos sites de referência pertencem aos respectivos autores.
