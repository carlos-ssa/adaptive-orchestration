# Codex

Conferido na [documentação oficial de skills](https://learn.chatgpt.com/docs/build-skills) e de [subagentes](https://learn.chatgpt.com/docs/agent-configuration/subagents) em 12/11/2026. Se a sessão expuser outra coisa, vale o que a sessão mostra.

## Instalação e invocação

- Pessoal: `$HOME/.agents/skills/adaptive-orchestration/`. Repositório: `.agents/skills/adaptive-orchestration/` (procurado da pasta atual até a raiz do repositório).
- Instalações antigas em `~/.codex/skills/` não aparecem na documentação atual; confira em `/skills` se a skill foi carregada.
- Invocação explícita: `$adaptive-orchestration <pedido>` ou pelo menu `/skills`. Implícita: pela `description`, controlada por `policy.allow_implicit_invocation` em `agents/openai.yaml`.

## Partida sem dados

Preserve o modelo e esforço herdados quando não houver evidência ou escolha autorizada. Não exija `/model`: uma política do host pode permitir troca apenas por solicitação explícita do usuário. Em delegação autorizada, consulte o schema real da ferramenta; `model_reasoning_effort` abaixo é chave de configuração TOML, não um campo de spawn presumido. Registre parâmetros solicitados e valores efetivos separadamente.

## Agentes próprios

Arquivos TOML em `~/.codex/agents/` (pessoal) ou `.codex/agents/` (projeto). Campos obrigatórios: `name`, `description`, `developer_instructions`. Valores omitidos seguem a precedência documentada: pedido explícito, padrões de `[agents]` e pai; uma definição personalizada pode prevalecer. Se outro modelo for selecionado sem esforço definido, pode usar o padrão desse modelo.

```toml
name = "leitor-barato"
description = "Lê arquivos ou logs longos e devolve só os trechos pedidos."
developer_instructions = "Leia o que for pedido e devolva só o resumo no formato solicitado. Não crie outros agentes."
model = "<modelo leve disponível>"
model_reasoning_effort = "low"
```

Os valores de `model_reasoning_effort` variam por modelo (por exemplo `low`, `medium`, `high`, `xhigh`, `max`, `ultra`). Confira os aceitos pelo modelo escolhido em [modelos no Codex](https://learn.chatgpt.com/docs/models).

## Padrões globais em `config.toml`

```toml
[agents]
enabled = true
default_subagent_model = "<modelo leve disponível>"
default_subagent_reasoning_effort = "medium"
max_concurrent_threads_per_session = 4
```

`max_concurrent_threads_per_session` é o limite técnico de concorrência; respeite-o em vez de estimar. A skill não altera esse arquivo: sugira a mudança ao usuário quando ela ajudar.

## Custo nesta CLI

No plano ChatGPT, o custo é a cota ou os créditos do Codex ([preços](https://learn.chatgpt.com/docs/pricing)); na API, as tarifas por token. Uma seleção diferente pode alterar consumo ou cota; confirme a política de cobrança e os valores efetivos antes de afirmar economia.
