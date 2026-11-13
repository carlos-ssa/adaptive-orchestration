# Seleção de modelos por evidência

Use esta referência quando houver uma escolha real de executor ou revisão de modelos. Reutilize evidências ainda válidas; não faça pesquisa externa para cada operação trivial.

## Adequação à tarefa

| Trabalho | O que comparar |
|---|---|
| Contagem, filtro e transformação exata | Ferramenta determinística antes de modelo adicional |
| Extração e classificação delimitadas | Fidelidade, resultado verificável e custo de erro |
| Leitura extensa e síntese | Recuperação de detalhes, fontes, contexto suportado, entrada/cache e saída |
| Escrita, visão e aplicativos | Modalidades, ferramentas e qualidade do resultado salvo |
| Código, terminal e migração | Avaliações relevantes, dependências e testes da tarefa |
| Pesquisa aberta e decisões difíceis | Julgamento do principal e capacidade de resolver ambiguidades |

O modelo mais barato por token pode consumir mais raciocínio e tentativas; o mais capaz pode terminar antes. Verifique o resultado por tarefa.

## Retrato do Artificial Analysis

Os dados ficam em `data/`, na raiz da skill, gerados por `scripts/aa_snapshot.py` a partir da [API gratuita](https://artificialanalysis.ai/data-api/docs) (exige `AA_API_KEY`; 100 requisições por dia; atribuição obrigatória; não redistribuir). `aa-snapshot.json` guarda todos os campos; `aa-snapshot.md` traz tabelas de capacidade, custo e velocidade para leitura humana.

1. Rode `python scripts/aa_snapshot.py --check` a partir da raiz da skill. Código 0: use o retrato existente.
2. Se estiver vencido ou ausente e houver rede e chave, rode `python scripts/aa_snapshot.py --creators <provedores da CLI>` (por exemplo `anthropic,openai`; o filtro vale só para o Markdown). Sem chave ou rede, não navegue pelo site a cada tarefa: reutilize o retrato datado disponível ou `preferences.local.md` e registre a lacuna; sem ambos, use a tabela provisória datada da CLI ([Claude Code](claude-code.md#partida-sem-retrato), [Codex](codex.md#partida-sem-retrato)).
3. Para escolher, rode `scripts/aa_rank.py` em vez de ler as tabelas inteiras (veja abaixo).
4. Cruze o resultado com os modelos que a CLI realmente oferece. Nomes do Artificial Analysis e apelidos da CLI diferem; registre o mapeamento em `preferences.local.md` para não refazê-lo.

### O que o retrato informa

| Dimensão | Campos | Uso |
|---|---|---|
| Capacidade geral | Intel (Intelligence Index) | Piso de qualidade para qualquer bloco |
| Capacidade por área | Eng (engenharia), Fin (finanças e contabilidade), Estr (estratégia e operações), Jur (jurídico), Saúde, Econ (economia) | Piso na área do bloco; Eng para código e trabalho técnico |
| Preço por token | Entrada, cache (leitura), cache (gravação), saída, em US$/1M | Custo de contexto: domina leitura extensa e sessões longas |
| Verbosidade | US$/tarefa do índice e saída/tarefa estimada | Quanto o modelo gera e raciocina; domina geração e código |
| Velocidade | tok/s, 1º token, 1º token de resposta, ponta a ponta | Tarefas interativas ou caminho crítico |

O plano gratuito não traz janela de contexto, modalidades (imagem, áudio), avaliações individuais, uso de ferramentas nem preços diferenciados para contexto longo. Confira esses requisitos na documentação do provedor ou na página do modelo quando a tarefa depender deles. O Artificial Analysis não publica mais Coding Index nem Agentic Index; não os procure.

### Custo por perfil de uso

O custo de uma chamada delegada é: entrada nova × preço de gravação de cache (ou de entrada, sem cache) + entrada em cache × preço de leitura de cache + saída × preço de saída. A saída de cada modelo é escalada pela verbosidade dele em relação à mediana do retrato, porque modelos que raciocinam mais geram mais tokens para o mesmo pedido.

| Perfil | Entrada | Cache | Saída (modelo mediano) | Exemplo |
|---|---|---|---|---|
| `leitura` | 200 mil | 50% | 4 mil | Ler arquivos ou logs e devolver resumo |
| `codigo` | 150 mil | 85% | 15 mil | Alteração delimitada com testes, várias rodadas |
| `agente` | 1 milhão | 90% | 30 mil | Sessão longa com contexto reenviado |
| `geracao` | 10 mil | 0% | 20 mil | Texto ou código novo a partir de pouco contexto |

Os volumes são ilustrativos. Quando souber o tamanho real, use `--entrada`, `--cache` e `--saida`. Em leitura e sessões longas, o preço de entrada e de cache pesa mais que a verbosidade; em geração, o contrário.

Alguns provedores cobram mais acima de um limite de contexto: detalhe datado de 12/11/2026, segundo o [guia de escolha de modelos da Anthropic](https://claude.dev/blog/which-claude-model-should-you-build-with/#pick-a-model-by-task), prompts acima de 100 mil tokens no Haiku 5.5 custam 5 vezes a taxa base. O retrato não traz essas faixas; o script avisa quando a entrada passa de 100 mil tokens, mas não corrige o custo. Sem a tabela do provedor, trate a sobretaxa como desconhecida para qualquer modelo e prefira blocos abaixo de 100 mil tokens. Nesses casos, confira a tabela do provedor, divida a leitura em blocos menores ou registre a sobretaxa conhecida em `preferences.local.md`.

Inclua também os casos difíceis: no mesmo guia, 2 de 20 problemas responderam por 43% do gasto. Um perfil médio subestima tarefas com cauda longa.

### Consulta

```sh
python scripts/aa_rank.py --perfil leitura --creators anthropic,openai --min 15
python scripts/aa_rank.py --perfil codigo --capacidade eng --ref <slug do principal> --pct 90
python scripts/aa_rank.py --perfil agente --min 45 --max-ttfat 30
```

`--capacidade` escolhe o índice da área (padrão: Intel) e `--min` define o piso nele. Em `--ref`, use o slug da variante no esforço em que o principal roda (ex.: `claude-opus-5-5-high`); o slug sem sufixo costuma ser a variante Max e eleva o piso. `--ref` e `--pct` definem o piso como porcentagem da nota do principal na mesma área e mostram quanto o principal custaria no perfil; assim o piso acompanha novas versões sem fixar nomes. Com `--min`, a lista vem ordenada pelo menor custo no perfil; sem ele, por pontos por dólar (`--ordem` altera). `--max-ttfat` e `--min-tps` excluem modelos lentos. O nome da variante (Low, Medium, High, Xhigh, Max) indica o esforço a passar para a CLI.

`--cli claude-code` acrescenta `model` pela família (haiku/sonnet/opus/fable) e `effort` pelo sufixo; candidatos sem apelido ficam como “não exposto nesta CLI”, sem filtragem nem mudança na ordem.
`--cli codex` usa o slug como `model` e o sufixo como `model_reasoning_effort`; confira o nome e os valores aceitos em `/model`. Sem sufixo, o esforço fica sem dados, não é inferido como Max.
O mapeamento fica em `scripts/aa_common.py`; é uma sugestão de parâmetros, não confirmação do modelo servido pelo provedor ou proxy.

## Custo esperado: o que conta é a tarefa concluída

Nenhum modelo fica fixo na skill. Modelos novos entram pelo retrato e são avaliados pelos mesmos critérios. O objetivo é o menor custo para concluir o bloco com o resultado aceito, não o menor custo por chamada:

custo esperado = custo da tentativa + chance de falha × (correção, nova tentativa e revisão do principal) + tempo perdido

- Um modelo barato que não dá conta da tarefa desperdiça tokens, cota e, principalmente, tempo: a entrega precisa ser revista, corrigida ou refeita, muitas vezes pelo modelo caro.
- Um modelo caro em tarefa simples desperdiça cota sem ganho de qualidade.
- Por isso a capacidade é filtro, não critério de desempate: primeiro o piso, depois o custo. Na dúvida entre dois candidatos, fique com o que tem margem acima do piso.

O piso depende de quanto custa errar:

| Situação do bloco | Piso |
|---|---|
| Verificação automática e barata (testes, script, contagem) | Mais baixo: tente o candidato barato e refaça só as falhas com esforço ou faixa maior |
| Verificação manual ou cara, caminho crítico, retrabalho caro | Mais alto: perto do principal na área do bloco |
| Falha silenciosa possível (erro plausível que ninguém confere) | Não delegue abaixo da faixa 3 sem verificação independente |

Compare também com o próprio principal: `--ref` mostra quanto ele custaria no perfil. Se o candidato economiza pouco, o contrato, a espera e a revisão anulam a diferença; resolva no principal. Ponto de partida, a calibrar: economia abaixo de 25% no perfil é pouca. Em assinatura, entre candidatos com custo até 10% diferente, prefira o que não gasta a cota do modelo do principal.

Pisos de partida, a calibrar pelos resultados: na faixa 1, Intel suficiente para extrair e resumir (`--min`), a partir do candidato mais barato que já entregou bem; na faixa 2, 85 a 90% do principal na área do bloco (`--ref`, `--pct`) com verificação manual, e 75 a 80% quando testes automáticos cobrem a alteração.

### Esforço

O esforço faz parte da escolha. Cada variante do retrato (Low, Medium, High, Xhigh, Max) é um par de modelo e esforço com capacidade, verbosidade e latência próprias. Compare variantes entre si: o esforço médio de um modelo maior pode superar o esforço alto de um menor e custar menos, e o esforço máximo costuma multiplicar saída e espera por pouco ganho. Passe à CLI o esforço da variante escolhida quando ela aceitar.

Troque de modelo em pontos naturais da tarefa. O cache pertence ao modelo que o gravou, então a troca reenvia o contexto a preço cheio; descer de modelo perde o raciocínio anterior. Antes de trocar o principal, resuma ou compacte o contexto. Um executor novo sempre começa sem cache: o perfil de custo já cobra a gravação da entrada nova.

### Calibração

Registre por bloco a data, faixa, tipo de tarefa, modelo, esforço, consumo real quando a CLI o mostrar (tokens, cota ou US$) e resultado: aceito, corrigido ou refeito. Use `scripts/aa_log.py`, que acrescenta uma linha em `data/calibracao.jsonl` (local, ignorado pelo Git). Para corrigido/refeito, `--motivo` é obrigatório: `capacidade|contexto|acesso|ferramenta|infra`; `--consumo` é texto opcional com unidade, sem conversão automática.

```sh
python scripts/aa_log.py --faixa 2 --tipo codigo --modelo executor --esforco medium --resultado corrigido --motivo capacidade --consumo "12000 tokens"
python scripts/aa_log.py --resumo
```

O resumo agrega por faixa/tipo/modelo e sinaliza duas falhas por capacidade na mesma faixa/tipo, inclusive entre modelos diferentes; não altera o piso automaticamente. `--arquivo <caminho>` permite separar registros e `--data AAAA-MM-DD` substitui a data de hoje. O consumo real substitui a estimativa do perfil nas escolhas seguintes. Duas falhas por capacidade na mesma faixa e tipo de tarefa elevam o piso dessa faixa; entregas aceitas com folga permitem testar um candidato mais barato. Falhas por contexto, acesso, ferramenta ou infraestrutura não contam: corrija o contrato ou a condição de execução.

## Processo de escolha

Analise o modelo como um todo para o bloco, nesta ordem:

1. **Requisitos rígidos.** Liste os candidatos que a CLI expõe e os parâmetros suportados. Descarte os que não atendem a contexto, modalidade, ferramentas ou política de dados exigidos. Um proxy pode fixar o modelo servido.
2. **Capacidade na área.** Classifique o bloco na faixa do [SKILL.md](../SKILL.md) e defina o piso no índice relevante conforme o custo de errar (seção anterior): na faixa 1, Intel suficiente para extrair e resumir; na faixa 2, perto do principal na área do bloco (Eng para código). Use os critérios de `preferences.local.md` quando existirem.
3. **Custo no perfil.** Entre os que atingem o piso, escolha o menor custo no perfil de uso do bloco, não só o US$/tarefa nem só o preço por token. Variantes do mesmo modelo concorrem entre si: a escolhida define também o esforço.
4. **Velocidade.** Desempate por tok/s e 1º token de resposta quando o bloco estiver no caminho crítico ou for interativo.
5. Prefira a família do principal quando a diferença for pequena: ferramentas e formato de resposta costumam ser mais estáveis. Diferenças pequenas e arredondadas não provam equivalência.
6. Registre a linha obrigatória do `SKILL.md`: modelo/esforço, capacidade/piso, custo no perfil e 1º token de resposta; acrescente data do retrato e motivo. Depois, registre o resultado para a calibração.
7. Preserve a seleção explícita do usuário, inclusive a do principal; a skill não autoriza trocá-la.

Não invente economia nem bloqueie trabalho executável por falta de dados. Peça informação quando ela for essencial ou a alternativa exigir nova autorização.

## Assinatura, créditos e proxy

Em assinatura (Claude Pro/Max, ChatGPT), créditos ou proxy, o custo é cota e limite de uso, não dólar por token. Os custos do retrato continuam úteis como comparação relativa de consumo. Preserve a cota do modelo mais caro: leitura, triagem e extração vão para a faixa 1 mesmo quando o custo em dólar não aparece na conta.

Um teto em dólar dado pelo usuário vira estimativa por executor com `aa_rank.py` (`--entrada`, `--cache`, `--saida` do bloco). Se a CLI não informar o consumo, o executor relata os tokens aproximados lidos e gerados (bytes ÷ 4 serve de ordem de grandeza) e o principal soma e compara com o teto.

## Esforço e disponibilidade

- Esforços com o mesmo nome não equivalem entre famílias. Identifique variante e modo na comparação; esforço individual, velocidade do serviço e execução com vários agentes são dimensões distintas.
- Sem preferência explícita, use o padrão suportado pelo ambiente como ponto de partida quando faltar recomendação atual. Se não houver controle de esforço, registre essa limitação e prossiga quando viável. Aumente esforço por dificuldade ou evidência de benefício, conforme o contrato de correção.
- Mais raciocínio não corrige fonte ausente, falha de acesso ou ferramenta inadequada. Não percorra uma escala fixa de modelos ou esforços. Informe indisponibilidade e não substitua silenciosamente por opção mais cara.
- Reavalie por lançamento relevante, aposentadoria, mudança de custo/acesso, falha recorrente ou novo tipo de tarefa. Registre a seleção no trabalho; não mantenha ranking permanente na skill.

## Custo e avaliação

Distinga API, assinatura, créditos e proxy. Quando conhecidos, inclua entrada, cache, saída/raciocínio, ferramentas, executores, tentativas e revisão. Não converta tokens em dinheiro sem tarifas aplicáveis. Não conte duas vezes componentes já incluídos na cobrança total. Um custo publicado em benchmark não prevê a conta do usuário.

Se o pedido incluir avaliação do fluxo, compare solo e equipe com as mesmas tarefas, materiais, cobertura e verificação, incluindo casos típicos e difíceis. Isso não é pré-requisito para cada delegação. Diferencie simulação de decisões, execução real e medição de custo. Não use confiança autorrelatada como evidência.
