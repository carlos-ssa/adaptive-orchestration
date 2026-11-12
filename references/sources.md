# Fontes e adaptação entre ambientes

Esta skill é uma adaptação original dos conceitos abaixo, não uma cópia das implementações. Referências consultadas durante sua elaboração em 12/11/2026, com leituras anteriores dos guias de modelos e do notebook em 11/11/2026. Consulte as versões atuais quando a decisão depender de detalhes que mudam.

| Fonte | Conceitos incorporados | Limites da adaptação |
|---|---|---|
| [Which Claude model should you build with?](https://claude.dev/blog/which-claude-model-should-you-build-with/#pick-a-model-by-task) | Escolha por tarefa, esforço e verificação; custo por trabalho concluído; delegação proporcional | Modelos, preços, cache e parâmetros do Claude não se transferem automaticamente a outros provedores ou CLIs |
| [CMA: plan big, execute small](https://github.com/anthropics/claude-cookbooks/blob/main/managed_agents/CMA_plan_big_execute_small.ipynb) | Principal planeja e sintetiza; executores processam material em contexto próprio; premissas verificadas; comparação com igual rigor | Não impõe principal sem ferramentas nem promete economia; quotas e APIs do notebook não são implementadas |
| [A harness for every task: dynamic workflows](https://claude.dev/blog/a-harness-for-every-task-dynamic-workflows-in-claude-code/) | Fluxo específico por tarefa, classificação, divisão, pipeline, revisão independente, hipóteses, geração/seleção, cobertura e retomada | Usa recursos realmente disponíveis; não instala runtime do Claude nem ativa loops, metas ou orçamentos de tokens |
| [Artificial Analysis](https://artificialanalysis.ai/) | Avaliações por domínio, variante e esforço, custo e tempo por tarefa | Ranking não prova adequação; benchmarks de API não são cobrança ou latência do ambiente do usuário |

## Documentação oficial por ambiente

Escolha a documentação da CLI e do provedor realmente utilizados. Não restrinja a seleção a uma empresa. Os links abaixo oferecem pontos de partida, não uma lista exclusiva de modelos ou ambientes suportados.

- [Claude Code](https://code.claude.com/docs)
- [Claude Platform](https://platform.claude.com/docs)

Exemplos para ambientes OpenAI:

- [Modelos no Codex](https://learn.chatgpt.com/docs/models)
- [Subagentes e precedência de configuração](https://learn.chatgpt.com/docs/agent-configuration/subagents)
- [Referência de configuração](https://learn.chatgpt.com/docs/config-file/config-reference)
- [Model selection — OpenAI API](https://developers.openai.com/api/docs/guides/model-selection)
- [Raciocínio — OpenAI API](https://developers.openai.com/api/docs/guides/reasoning)
- [Preços da API](https://developers.openai.com/api/docs/pricing)
- [Preços de Codex e créditos](https://learn.chatgpt.com/docs/pricing)

Se um endereço mudar, encontre a página equivalente no domínio oficial. Atualize a evidência da tarefa; não substitua dados ausentes por memória ou por um catálogo desatualizado.
