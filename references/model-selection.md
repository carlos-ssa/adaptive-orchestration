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

Os dados ficam em `data/aa-snapshot.md`, na raiz da skill, gerado por `scripts/aa_snapshot.py` a partir da [API gratuita](https://artificialanalysis.ai/data-api/docs) (exige `AA_API_KEY`; 100 requisições por dia; atribuição obrigatória; não redistribuir).

1. Rode `python scripts/aa_snapshot.py --check` a partir da raiz da skill. Código 0: use o arquivo existente.
2. Se estiver vencido ou ausente e houver rede e chave, rode `python scripts/aa_snapshot.py`. Sem chave ou rede, não navegue pelo site a cada tarefa: use `preferences.local.md` ou o conhecimento disponível como escolha provisória e registre a lacuna.
3. Leia só a tabela. As colunas que importam:
   - **US$/tarefa**: custo médio por tarefa do Intelligence Index, já com tokens de raciocínio. É a melhor medida de custo real; preço por token engana quando um modelo raciocina muito mais.
   - **Intel/US$**: pontos de índice por dólar de tarefa. É o critério de desempate dentro de uma faixa.
   - **Intel** para capacidade geral; **Eng** (Engineering Index) como sinal adicional para trabalho técnico.
   - **tok/s** e **TTFAT** quando o tempo de resposta importa.
4. Cruze a tabela com os modelos que a CLI realmente oferece. Nomes do Artificial Analysis e apelidos da CLI diferem; registre o mapeamento em `preferences.local.md` para não refazê-lo.

O Artificial Analysis não publica mais Coding Index nem Agentic Index; não os procure. Para domínios específicos, abra a página do modelo no site só quando a decisão depender disso.

## Processo de escolha

1. Liste os candidatos que a CLI expõe e os parâmetros suportados. Um proxy pode fixar o modelo servido.
2. Classifique o bloco na faixa do [SKILL.md](../SKILL.md) e use o mapeamento de `preferences.local.md` quando existir.
3. Sem mapeamento: na faixa 1, escolha o candidato com menor US$/tarefa entre os que têm Intel razoável para a tarefa; na faixa 2, o maior Intel/US$ entre os candidatos próximos do principal em Intel. Prefira o modelo de família igual ao principal quando a diferença for pequena: ferramentas e formato de resposta costumam ser mais estáveis.
4. Registre no trabalho: modelo, esforço, data do retrato e motivo em uma linha. Empates arredondados não provam equivalência.
5. Preserve a seleção explícita do usuário, inclusive a do principal; a skill não autoriza trocá-la.

Não invente economia nem bloqueie trabalho executável por falta de dados. Peça informação quando ela for essencial ou a alternativa exigir nova autorização.

## Assinatura, créditos e proxy

Em assinatura (Claude Pro/Max, ChatGPT), créditos ou proxy, o custo é cota e limite de uso, não dólar por token. O US$/tarefa continua útil como comparação relativa de consumo. Preserve a cota do modelo mais caro: leitura, triagem e extração vão para a faixa 1 mesmo quando o custo em dólar não aparece na conta.

## Esforço e disponibilidade

- Esforços com o mesmo nome não equivalem entre famílias. Identifique variante e modo na comparação; esforço individual, velocidade do serviço e execução com vários agentes são dimensões distintas.
- Sem preferência explícita, use o padrão suportado pelo ambiente como ponto de partida quando faltar recomendação atual. Se não houver controle de esforço, registre essa limitação e prossiga quando viável. Aumente esforço por dificuldade ou evidência de benefício, conforme o contrato de correção.
- Mais raciocínio não corrige fonte ausente, falha de acesso ou ferramenta inadequada. Não percorra uma escala fixa de modelos ou esforços. Informe indisponibilidade e não substitua silenciosamente por opção mais cara.
- Reavalie por lançamento relevante, aposentadoria, mudança de custo/acesso, falha recorrente ou novo tipo de tarefa. Registre a seleção no trabalho; não mantenha ranking permanente na skill.

## Custo e avaliação

Distinga API, assinatura, créditos e proxy. Quando conhecidos, inclua entrada, cache, saída/raciocínio, ferramentas, executores, tentativas e revisão. Não converta tokens em dinheiro sem tarifas aplicáveis. Não conte duas vezes componentes já incluídos na cobrança total. Um custo publicado em benchmark não prevê a conta do usuário.

Se o pedido incluir avaliação do fluxo, compare solo e equipe com as mesmas tarefas, materiais, cobertura e verificação, incluindo casos típicos e difíceis. Isso não é pré-requisito para cada delegação. Diferencie simulação de decisões, execução real e medição de custo. Não use confiança autorrelatada como evidência.
