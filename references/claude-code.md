# Claude Code

Conferido na [documentação oficial](https://code.claude.com/docs/en/sub-agents) em 12/11/2026. Se a ferramenta exposta na sessão divergir, vale o que a sessão mostra.

## Instalação e invocação

- Pessoal: `~/.claude/skills/adaptive-orchestration/`. Projeto: `.claude/skills/adaptive-orchestration/`.
- Invocação explícita: `/adaptive-orchestration <pedido>`. Implícita: quando o pedido combina com `description`.
- `agents/openai.yaml` é ignorado pelo Claude Code.

## Delegar com modelo e esforço

A ferramenta `Agent` (antes `Task`) aceita:

| Parâmetro | Valores | Observação |
|---|---|---|
| `subagent_type` | `Explore`, `Plan`, `general-purpose` ou agentes próprios | `Explore` é somente leitura e serve para buscas amplas |
| `model` | apelidos `haiku`, `sonnet`, `opus`, `fable` | Sem ID completo nesta chamada |
| `effort` | `low`, `medium`, `high`, `xhigh`, `max` | Só quando a ferramenta expõe o campo |
| `isolation` | `worktree` | Cópia isolada do repositório para escrita em paralelo |
| `run_in_background` | `true` | O principal continua trabalhando enquanto espera |

Em condições normais, a precedência é chamada → arquivo do agente → `CLAUDE_CODE_SUBAGENT_MODEL` → principal; versões, regras administradas, força de modelo e agentes integrados podem alterá-la. Confira o modelo efetivo quando disponível.

Os apelidos dependem do provedor: segundo o [guia de escolha de modelos](https://claude.dev/blog/which-claude-model-should-you-build-with/#pick-a-model-by-task), `haiku` aponta para o Haiku 5.5 na API da Anthropic, mas para o Haiku 4.5 no Bedrock, Google Cloud, Foundry e Claude Platform on AWS. Confira o modelo efetivo antes de usar o retrato do Artificial Analysis; se precisar de uma versão exata, use o ID completo no arquivo do agente.

## Partida sem dados

Sem dados comparáveis ou autorização para alterar a seleção, preserve o modelo e esforço herdados e registre a incerteza. Só envie parâmetros expostos pela ferramenta e permitidos pelo host; valide a entrega antes de concluir que a escolha é adequada ou econômica.

## Agentes próprios

Arquivos `.claude/agents/<nome>.md` (projeto) ou `~/.claude/agents/<nome>.md` (pessoal):

```markdown
---
name: leitor-barato
description: Lê arquivos ou logs longos e devolve só os trechos pedidos.
model: haiku
effort: low
tools: Read, Grep, Glob
---
Leia o que for pedido e devolva só o resumo no formato solicitado.
```

`model` aceita apelido, ID completo ou `inherit`. Há relatos de versões que ignoram `effort` no arquivo do agente; se o esforço importar, passe-o na chamada e registre o valor efetivo. Limite `tools` ao necessário: isso é bloqueio técnico, ao contrário de instrução no contrato.

## Subdelegação e proxies

- Subdelegação depende do tipo de agente e dos recursos efetivamente expostos; não presuma suporte por incluir `Agent`. No modo padrão, proíba-a no contrato e restrinja ferramentas quando o runtime permitir.
- Agentes servidos por proxy (por exemplo, roteadores que expõem modelos de outros provedores como agentes) costumam fixar o modelo: o parâmetro `model` é ignorado. Escolha o agente pelo nome e registre o modelo declarado na descrição dele.

## Custo nesta CLI

Em assinatura, confira como cotas e créditos são contabilizados; não presuma cotas separadas ou economia. Em API, confira as tarifas aplicáveis e inclua tentativas e revisão.
