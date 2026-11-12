# Seleção de modelos sem catálogo fixo

Use esta referência quando escolher um executor ou revisar a configuração de modelos. Não pesquise rankings para cada operação trivial. Reutilize evidências recentes enquanto versão, tarefa e condições de execução permanecerem comparáveis.

## Identifique o trabalho

| Necessidade | Critério de seleção |
|---|---|
| Contagem, filtro, transformação exata | Preferir script ou ferramenta determinística |
| Extração, classificação e decisões semânticas delimitadas | Modelo eficiente com resultado verificável; menor esforço que atenda à qualidade necessária |
| Leitura extensa e síntese | Fidelidade às fontes, recuperação de detalhes, preço de entrada/cache e capacidade de detectar incerteza |
| Escrita, visão e aplicativos | Evidências nas modalidades e ferramentas usadas; confirmar o resultado salvo |
| Código, terminal e migrações | Avaliações relevantes, testes da tarefa, extensão das dependências e custo de erro |
| Pesquisa aberta, planejamento e alto risco | Capacidade de julgamento do principal; escolher esforço que corresponda à dificuldade |

O modelo com menor preço por token pode consumir mais raciocínio, ferramentas e tentativas. Um modelo mais caro pode resolver antes. Nenhum desses efeitos deve ser presumido sem evidência.

## Verifique candidatos e fontes

1. Consulte o catálogo e as ferramentas realmente disponíveis. Distinga nome solicitado, configuração registrada e modelo efetivamente confirmado. Um catálogo local não comprova acesso remoto nem identidade do modelo servido por um proxy.
2. Consulte [Artificial Analysis](https://artificialanalysis.ai/) para variantes exatas e avaliações pertinentes ao domínio. Abra as páginas; não trate snippets, rótulos de gráficos ou nomes parecidos como medições suficientes.
3. Confirme nomes, esforços, suporte de ferramentas e preços na documentação oficial atual do provedor. Consulte as referências oficiais do provedor e da CLI em [sources.md](sources.md); os links da OpenAI são exemplos para ambientes que a utilizam. Se houver skill de documentação adequada, use-a.
4. Registre data de consulta, modelo/versão, provedor, esforço, modo de execução, metodologia e URLs. Marque dados ausentes. Divergências entre páginas ou versões devem ficar explícitas.
5. Escolha candidatos que atendam aos critérios da tarefa. Compare qualidade, custo e tempo juntos. Índices agregados são triagem; um empate arredondado não demonstra equivalência em todos os domínios nem significância estatística.

Se pesquisa externa estiver proibida ou fontes/preços não estiverem acessíveis, respeite a restrição. Use evidências locais válidas e as preferências do usuário para uma escolha provisória dentro do escopo, deixando a incerteza explícita. Ausência de benchmark não exige bloquear uma tarefa executável; escale somente quando a informação faltante for essencial à decisão ou a alternativa exigir nova autorização. Não invente economia.

Níveis como low, medium e high não são unidades comparáveis entre famílias. Não compare um resultado em max com outro em medium sem identificar a diferença. Modos com subagentes, modos pro, velocidade de serviço e esforço individual são dimensões distintas; confirme sua semântica atual.

## Esforço e escalonamento

- Preserve a escolha explícita do usuário e o principal selecionado. Para trabalho rotineiro, comece no esforço recomendado pelo provedor para a tarefa, se suportado. Para tarefas difíceis, escolha maior capacidade desde o início quando a evidência justificar.
- Antes de elevar esforço após uma falha, verifique especificação, fontes, ferramentas e critério de teste. Mais raciocínio não corrige falta de acesso ou dados ausentes.
- Se uma tarefa excede a capacidade do executor, devolva ao principal. Não aumente indefinidamente o esforço de um modelo menor nem crie uma sequência obrigatória de tentativas.
- A mudança do modelo principal continua uma escolha explícita do usuário. Informe indisponibilidade; não substitua silenciosamente por opção mais cara. Se a ferramenta não permite confirmar ou mudar esforço, diga isso.
- Reavalie quando surgirem modelos relevantes, mudança de preço/acesso, aposentadoria de versão, falhas recorrentes ou mudança de tarefa. Não reescreva a skill apenas para trocar nomes de modelos: ela define o método; a seleção atual fica no registro do trabalho.

## Comparação econômica correta

Separe preços de API, uso incluído em assinatura, créditos e cobrança do proxy. Registre modo de serviço, contexto e cache quando afetarem a comparação. Preço em dólares não equivale a crédito, e custo publicado no benchmark não é uma previsão da conta do usuário.

Quando houver dados, considere entrada, cache, saída/raciocínio, ferramentas cobradas e todos os executores e tentativas. Não converta volume de tokens em custo sem conhecer as tarifas e regras aplicáveis. Não invente dados ausentes.

Quando a tarefa incluir avaliação ou otimização do fluxo, compare solo e equipe em tarefas típicas e difíceis, com os mesmos materiais e critérios de verificação. Esse benchmark não é obrigatório para cada delegação. Inclua o tempo de coordenação e revisão. Qualidade deve ser avaliada com resultados observáveis, não com confiança autorrelatada do modelo. Executar avaliações que ampliem o trabalho ou tenham custo significativo exige escopo apropriado; pesquisar documentação não exige chamadas de inferência.
