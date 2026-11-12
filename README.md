# Adaptive Orchestration

Skill em português para escolher modelos por tarefa e coordenar execução, pesquisa e revisão em CLIs e assistentes de IA. Combina escolha por tarefa e esforço, planejamento no principal e execução delegada, fluxos dinâmicos e avaliações do Artificial Analysis.

## Uso

Peça ao assistente para aplicar `adaptive-orchestration`. Em ambientes que aceitam a sintaxe de skills por nome:

```text
Use $adaptive-orchestration para investigar esta falha e verificar a solução.
```

Outros exemplos:

- Comparar modelos disponíveis para uma migração, considerando qualidade, custo e tempo.
- Verificar todas as afirmações de um relatório e registrar itens sem evidência.
- Investigar hipóteses concorrentes de uma falha intermitente.
- Comparar alternativas de implementação com critérios comuns.

Tarefas simples continuam em execução direta. A descoberta automática depende do cliente; não é garantida em toda solicitação. Use o nome explicitamente ou forneça o SKILL.md quando precisar assegurar a aplicação.

## Instalação e portabilidade

```sh
git clone https://github.com/carlos-ssa/adaptive-orchestration.git
```

Coloque a pasta `adaptive-orchestration` no diretório de skills reconhecido pela sua CLI, conforme a documentação dela. Se ela não tiver descoberta de skills, forneça o [SKILL.md](SKILL.md) e mantenha as referências relativas acessíveis. Recarregue o cliente quando necessário.

A skill usa Markdown, frontmatter e referências locais. Ela não inclui um runtime universal: nomes de ferramentas, seleção de modelos, isolamento e persistência variam entre CLIs. O assistente deve verificar as capacidades disponíveis e adaptar o fluxo. Sem subagentes, pode executar diretamente as etapas que conseguir cumprir, informando limitações.

`agents/openai.yaml` contém metadados opcionais para clientes compatíveis com esse formato. Outros ambientes podem ignorá-lo; as instruções compartilhadas estão no SKILL.md e nas referências.

## Estrutura

- [SKILL.md](SKILL.md): orientação principal e critérios de uso.
- [Seleção de modelos](references/model-selection.md): capacidades atuais, fontes oficiais e Artificial Analysis.
- [Fluxos](references/workflows.md): padrões, revisão independente e retomada.
- [Contratos](references/contracts.md): autoridade, evidências e validação de decisões.
- [Fontes](references/sources.md): links de origem e limites da adaptação.

## Comportamento

O principal escolhe um fluxo apropriado e delega blocos verificáveis quando isso ajuda. Por padrão, até dois executores simultâneos, sem subdelegação. Pode usar ponytail e impeccable quando instaladas; elas não são distribuídas neste repositório.

Não mantém uma tabela fixa de modelos ou preços. Quando a escolha exigir comparação, consulta o catálogo disponível, a documentação oficial e avaliações relevantes. Modelos futuros entram pelo mesmo processo, sem atualizar instruções globais a cada lançamento.

## Limites

A skill não modifica instruções globais, arquivos de configuração, permissões ou a seleção do modelo principal. Não instala um roteador automático, sandbox ou runtime de workflows e não autoriza ações externas fora do pedido. Não contém limites de tokens.

Economia real, disponibilidade e qualidade precisam ser verificadas no ambiente de uso. Validação estrutural e cenários simulados não equivalem a um benchmark de produção ou a testes em todas as CLIs.
