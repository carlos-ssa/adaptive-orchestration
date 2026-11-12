# Codex

Conferido na [documentação oficial de skills](https://learn.chatgpt.com/docs/build-skills) e de [subagentes](https://learn.chatgpt.com/docs/agent-configuration/subagents) em 12/11/2026. Se a sessão expuser outra coisa, vale o que a sessão mostra.

## Instalação e invocação

- Pessoal: `$HOME/.agents/skills/adaptive-orchestration/`. Repositório: `.agents/skills/adaptive-orchestration/` (procurado da pasta atual até a raiz do repositório).
- Instalações antigas em `~/.codex/skills/` não aparecem na documentação atual; confira em `/skills` se a skill foi carregada.
- Invocação explícita: `$adaptive-orchestration <pedido>` ou pelo menu `/skills`. Implícita: pela `description`, controlada por `policy.allow_implicit_invocation` em `agents/openai.yaml`.

## Agentes próprios

Arquivos TOML em `~/.codex/agents/` (pessoal) ou `.codex/agents/` (projeto). Campos obrigatórios: `name`, `description`, `developer_instructions`. Campos omitidos herdam do agente pai.

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

No plano ChatGPT, o custo é a cota ou os créditos do Codex ([preços](https://learn.chatgpt.com/docs/pricing)); na API, as tarifas por token. Subagente com modelo leve e esforço baixo em leitura e triagem preserva a cota do modelo principal.
