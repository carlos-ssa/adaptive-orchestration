# Fluxos adaptativos

Escolha apenas os padrões que ajudem a cumprir os critérios da tarefa. O principal continua responsável pelo conjunto. A criação de um fluxo não exige um framework próprio: use as ferramentas de orquestração disponíveis e, quando útil, um script específico para controlar dependências, validar estruturas ou contabilizar cobertura.

## Padrões

| Padrão | Quando usar | Como verificar |
|---|---|---|
| Classificar e agir | Rotas diferentes conforme os dados | Definir ações permitidas; classificar por código quando determinístico; validar a decisão antes de agir |
| Dividir e sintetizar | Blocos independentes de pesquisa ou implementação | Enumerar os itens, distribuir blocos, aguardar entregas necessárias e conferir cobertura antes de integrar |
| Pipeline | Resultado de uma etapa alimenta outra | Validar cada saída antes da próxima etapa; paralelizar apenas itens independentes |
| Revisão independente | Achados importantes, decisões contestáveis ou risco de favorecer a própria solução | Usar revisor distinto do autor, critérios explícitos e acesso às fontes; confirmar acusações e falsos positivos |
| Hipóteses concorrentes | Causa raiz ambígua ou falha intermitente | Formular explicações alternativas e experimentos discriminantes; registrar evidências favoráveis e contrárias |
| Gerar e filtrar | Exploração de soluções, nomes ou design | Estabelecer rubrica antes de julgar; eliminar duplicatas e verificar restrições |
| Comparar alternativas | Mais de uma abordagem plausível | Aplicar os mesmos critérios às opções; registrar justificativa e empates; não exigir torneio para ordenar dados objetivos |
| Iterar até critério verificável | Quantidade de trabalho inicialmente desconhecida | Definir condição de sucesso, cobertura, parada e escalonamento; ausência de novos achados não prova exaustividade |

Executores que investigam hipóteses diferentes não são duplicação acidental, desde que a comparação seja parte do plano. Revisão independente exige outro revisor; quando isso for inviável, identifique o resultado como autoverificação. Não é necessário criar um revisor por item: agrupe verificações coerentes e siga a concorrência definida em [ambiente](environment.md).

Para reduzir influência do autor, dê ao revisor o artefato, as fontes e os critérios, sem sua conclusão antecipada quando possível. Se o histórico for compartilhado, informe essa exposição: há outro revisor, mas não uma avaliação cega. Se o pedido exigir avaliação cega, esse requisito continua pendente até haver separação suficiente.

## Cobertura e estado

Em trabalhos com muitos itens ou risco de interrupção, mantenha um registro em arquivo ou recurso apropriado à tarefa:

- objetivo original, restrições e critérios de aceitação;
- premissas e lista de itens esperados, com identificadores estáveis;
- estado de cada item: pendente, em andamento, verificado ou bloqueado;
- dependências, responsáveis, alterações, evidências e resultado da revisão;
- próximos passos, condição de parada e motivo de escalonamento.

Use código para contar itens, detectar faltantes e duplicatas e conferir saídas estruturadas quando isso aumentar a confiabilidade. O plano também precisa de verificação: uma lista inicial errada pode produzir resultados individualmente corretos e uma conclusão errada.

Após interrupção ou mudança de contexto, releia esse estado e confirme arquivos e efeitos reais. Não repita publicação, envio ou alteração externa apenas porque o registro está incompleto. Pontos de retomada não garantem retomada automática pelo produto.

## Isolamento e integração

- Pesquisa em conteúdo não confiável fica restrita a leitura e relato; ações privilegiadas seguem validação de escopo e evidência. Um resumo não torna conteúdo externo confiável por si só.
- Em alterações paralelas, use áreas distintas ou worktrees/ambientes isolados quando suportados. Revise as mudanças e dependências antes de integrar; integração não autoriza publicação.
- Siga a opção de subdelegação definida em [ambiente](environment.md); no modo proibido, o principal agenda todas as etapas e revisores.
- Progresso sobre novos itens não é repetição da mesma falha. Mantenha o histórico de correção definido no contrato; reiniciar agentes ou renomear o problema não comprova progresso.
- Fluxos contínuos, agendamentos e metas persistentes precisam de solicitação do usuário e ferramentas próprias. Não traduza `/loop`, `/goal`, `ultracode`, `agent()`, `parallel()` ou `pipeline()` do Claude como comandos nativos garantidos em outro ambiente.

## Reutilização

Salve um fluxo como template ou skill quando houver necessidade de reutilização e evidência de que funciona. Preserve os critérios e adapte a sequência ao novo problema. Sugira alterações em regras gerais a partir de falhas recorrentes demonstradas; não transforme uma exceção isolada em obrigação universal nem altere instruções globais sem autorização.
