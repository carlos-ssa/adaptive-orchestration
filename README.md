# Adaptive Orchestration

Skill em português para coordenação adaptativa em CLIs e assistentes de IA: escolher modelos por tarefa, delegar blocos verificáveis e integrar resultados com evidências. Combina [três guias de origem e Artificial Analysis](references/sources.md).

## Uso em diferentes CLIs

```sh
git clone https://github.com/carlos-ssa/adaptive-orchestration.git
```

Se sua CLI reconhece skills, instale a pasta no diretório indicado por ela. Se não reconhece, forneça [SKILL.md](SKILL.md) como instrução e mantenha as referências relativas acessíveis. Em ambientes que aceitam invocação por nome:

```text
Use $adaptive-orchestration para investigar esta falha e verificar a solução.
```

O formato de invocação e a descoberta automática dependem da CLI. `agents/openai.yaml` é metadado opcional para clientes compatíveis; outros podem ignorá-lo. Nenhuma instrução central depende desse arquivo.

## Adaptação por capacidade

| Ambiente | Comportamento |
|---|---|
| Subagentes, modelo e esforço configuráveis | Delegação com seleções suportadas e contratos explícitos |
| Subagentes com controles parciais | Usa o controle disponível, registra valores herdados/desconhecidos |
| Sem subagentes | Executa etapas sequenciais e distingue autoverificação de revisão independente |
| Sem internet | Usa evidência local, registra lacunas e evita inventar preços |
| Sem persistência | Mantém estado no recurso disponível, sem afirmar que salvou checkpoint |

Portabilidade significa adaptar o procedimento às ferramentas reais. Não existe um runtime universal neste repositório; comportamento nativo em todas as CLIs não foi comprovado.

## Preferências opcionais

A skill não fixa modelos nem quantidade de executores, não impõe limites de tokens e não depende de outras skills. Concorrência segue necessidade, recursos e limites do usuário ou do ambiente.

**Sem subdelegação é o modo padrão:** somente o coordenador cria agentes. O usuário pode habilitá-la com escopo e limites definidos. Isso é uma instrução; bloqueio técnico depende do runtime.

Preferências podem ser informadas no pedido ou em `preferences.local.md` na pasta da skill, quando autorizado pelo usuário. Esse arquivo é opcional e ignorado pelo Git. Não o inclua em pacotes públicos. Veja [adaptação ao ambiente](references/environment.md).

## Conteúdo

- [SKILL.md](SKILL.md): ponto de entrada e regras de coordenação.
- [Ambiente](references/environment.md): capacidades, concorrência e subdelegação.
- [Modelos](references/model-selection.md): seleção atual, esforço, qualidade, custo e tempo.
- [Fluxos](references/workflows.md): hipóteses, revisão, geração/seleção, cobertura e retomada.
- [Contratos](references/contracts.md) e [exemplos preenchidos](references/examples.md).
- [Fontes](references/sources.md) e [cenários de validação](evals/README.md).

Modelos e preços futuros entram pelo mesmo processo de consulta ao catálogo disponível, documentação oficial e avaliações do domínio. Nenhum ranking fica congelado na skill.

## Limites e licença

A skill não muda configuração global ou modelo principal, instala ferramentas, concede permissões ou autoriza ações externas fora do pedido. Rankings orientam candidatos; economia real depende dos resultados e da cobrança do ambiente.

Distribuída sob a [licença MIT](LICENSE). Conteúdos dos sites de referência pertencem aos respectivos autores; o repositório contém instruções e exemplos originais de adaptação.
