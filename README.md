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
python scripts/aa_snapshot.py
```

O script usa só a biblioteca padrão do Python e grava `data/aa-snapshot.md` (ignorado pelo Git). Ele só chama a API se o retrato tiver mais de 7 dias. A métrica central é o custo por tarefa do Intelligence Index, que já inclui os tokens de raciocínio. Sem chave, a skill continua funcionando com escolhas provisórias. Os dados exigem atribuição ao Artificial Analysis e não devem ser redistribuídos.

## Como escolhe

| Faixa | Trabalho | Executor |
|---|---|---|
| 0 | Contagem, filtro, busca exata | Script, sem modelo |
| 1 | Leitura extensa, extração, triagem | Modelo leve, esforço baixo |
| 2 | Código delimitado, migração mecânica, revisão | Modelo intermediário, esforço médio |
| 3 | Ambiguidade, arquitetura, integração, decisão | Principal |

Os modelos de cada faixa vêm de `preferences.local.md` (opcional, ignorado pelo Git) ou do retrato cruzado com o que a CLI oferece. Em assinatura, o custo é cota, e a skill preserva a do modelo mais caro. Veja [seleção de modelos](references/model-selection.md) e o [exemplo de preferências](references/environment.md#preferências-opcionais).

## Conteúdo

- [SKILL.md](SKILL.md): ponto de entrada, faixas e regras de coordenação.
- [Claude Code](references/claude-code.md) e [Codex](references/codex.md): parâmetros de delegação de cada CLI.
- [Modelos](references/model-selection.md): retrato, métricas e escolha sem dados.
- [Ambiente](references/environment.md): outras CLIs, concorrência, subdelegação e preferências.
- [Fluxos](references/workflows.md), [contratos](references/contracts.md) e [exemplos](references/examples.md).
- [Fontes](references/sources.md) e [cenários de validação](evals/README.md).

## Limites e licença

A skill não muda configuração global nem o modelo principal, não instala ferramentas e não autoriza ações externas fora do pedido. Rankings orientam candidatos; a economia real depende dos resultados e da cobrança do ambiente. Execução nativa no Claude Code ainda não foi validada; veja [evals](evals/README.md).

Distribuída sob a [licença MIT](LICENSE). Conteúdos dos sites de referência pertencem aos respectivos autores.
