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

## Processo de escolha

1. Identifique candidatos disponíveis e parâmetros suportados. Distinga catálogo local, acesso remoto e identidade efetivamente confirmada; um proxy pode não servir o modelo esperado.
2. Quando necessário e permitido, consulte [Artificial Analysis](https://artificialanalysis.ai/) e abra as páginas das variantes exatas. Priorize avaliações do domínio; ranking geral e snippets não bastam.
3. Confirme nomes, esforços, ferramentas e preços na documentação oficial atual do provedor e da CLI. Veja pontos de partida em [fontes](sources.md).
4. Registre data, versão, provedor, esforço/modo, metodologia, URLs e lacunas, conforme o [exemplo](examples.md). Compare qualidade, custo e tempo. Empates arredondados não provam equivalência ou significância estatística.
5. Escolha o candidato que atende aos critérios da tarefa. Preserve a seleção explícita do usuário, inclusive a do principal; a skill não autoriza trocá-la.

Se fontes ou preços estiverem indisponíveis, use evidências locais e preferências autorizadas para uma escolha provisória. Não invente economia nem bloqueie trabalho executável apenas por ausência de ranking. Peça informação quando ela for essencial ou a alternativa exigir nova autorização.

## Esforço e disponibilidade

- Esforços com o mesmo nome não equivalem entre famílias. Identifique variante e modo na comparação; esforço individual, velocidade do serviço e execução com vários agentes são dimensões distintas.
- Sem preferência explícita, use o padrão suportado pelo ambiente como ponto de partida quando faltar recomendação atual. Se não houver controle de esforço, registre essa limitação e prossiga quando viável. Aumente esforço por dificuldade ou evidência de benefício, conforme o contrato de correção.
- Mais raciocínio não corrige fonte ausente, falha de acesso ou ferramenta inadequada. Não percorra uma escala fixa de modelos ou esforços. Informe indisponibilidade e não substitua silenciosamente por opção mais cara.
- Reavalie por lançamento relevante, aposentadoria, mudança de custo/acesso, falha recorrente ou novo tipo de tarefa. Registre a seleção no trabalho; não mantenha ranking permanente na skill.

## Custo e avaliação

Distinga API, assinatura, créditos e proxy. Quando conhecidos, inclua entrada, cache, saída/raciocínio, ferramentas, executores, tentativas e revisão. Não converta tokens em dinheiro sem tarifas aplicáveis. Não conte duas vezes componentes já incluídos na cobrança total. Um custo publicado em benchmark não prevê a conta do usuário.

Se o pedido incluir avaliação do fluxo, compare solo e equipe com as mesmas tarefas, materiais, cobertura e verificação, incluindo casos típicos e difíceis. Isso não é pré-requisito para cada delegação. Diferencie simulação de decisões, execução real e medição de custo. Não use confiança autorrelatada como evidência.
