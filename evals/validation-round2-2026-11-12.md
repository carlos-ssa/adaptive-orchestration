# Segunda rodada de validação — 12/11/2026

Versão inicial avaliada: `f0fed3d`. Objetivo: verificar comportamento com artefatos reais, seleção de modelos por critérios e adaptação a recursos indisponíveis. Não é uma comparação estatística com/sem skill nem teste de todas as CLIs.

## Estrutura e distribuição

Validador estrutural aprovado; referências relativas resolvidas; os três guias e Artificial Analysis continuam presentes. Instalação local, checkout e versão remota conferidos antes dos testes. Nenhuma dependência pessoal ou quantidade fixa de executores foi reintroduzida.

## Migração de código

Uma nova sessão de Codex CLI foi iniciada com subagentes, plugins e pesquisa web desativados, usando modelo solicitado GPT-6.1 Terra/medium. A política local bloqueou leituras e comandos. A sessão informou o impedimento e não declarou ter feito a alteração. O retorno do processo foi zero: esse código sozinho não comprova conclusão da tarefa do agente.

Em uma segunda sessão, o conteúdo da skill, referências pertinentes e arquivos foi fornecido na entrada, com ferramentas de shell desativadas e saída estruturada. O pedido era renomear uma API Python e todos os consumidores, mantendo o valor de um evento de analytics e sem fazer deploy. A CLI produziu sete arquivos propostos e registrou que não os havia aplicado nem executado testes.

O coordenador conferiu a proposta antes de aplicar no diretório de teste:

- caminhos limitados aos sete arquivos autorizados;
- comparação da árvore sintática: apenas a renomeação de definição, imports, chamadas e exportações esperadas, preservando lógica e asserções;
- documentação do evento legado preservada;
- sete testes passaram depois da aplicação;
- casos adicionais de importação e comportamento passaram;
- marcador de deploy permaneceu intacto.

Os testes foram executados pelo coordenador, fora da sessão limitada da CLI. Isso demonstra o fluxo de proposta, verificação e aplicação nesse ambiente, não a capacidade da sessão bloqueada de editar diretamente.

## Escolha de executor

Um subagente recebeu um conjunto local de quatro modelos fictícios, quantidade fixa de documentos, tarifas e requisito mínimo de acurácia. Rede e chamadas aos candidatos não eram permitidas.

O resultado selecionou Reader-B, o candidato elegível mais econômico, e calculou USD 3,024 para 600 documentos. A conferência independente confirmou a conta. O agente descartou o candidato abaixo do requisito, não confundiu índice geral com evidência específica de extração e não presumiu cache para reduzir o preço de outro candidato. O esforço ficou nulo porque esse candidato não oferecia controle.

Os valores são dados do exercício, não resultados públicos ou preços reais. A estimativa exclui tentativas, revisão e outras cobranças não fornecidas, conforme declarado no artefato.

## Melhoria incorporada

O teste de CLI limitada exigiu um contrato explícito de entrega de arquivos propostos. Esse caminho foi acrescentado à referência de ambiente: fornecer patch/arquivos quando possível, distinguir proposta de aplicação e teste, e validar antes de agir. A orientação acompanha o comportamento observado; não houve nova inferência após essa edição documental.

## O que permanece sem comprovação

- Execução nativa em Claude Code, Gemini CLI ou OpenCode: esses clientes não estavam disponíveis.
- Benefício incremental, economia e redução de falhas em produção: exigem amostras e medições comparáveis.
- Delegação multinível concorrente real: a opção foi avaliada por cenários, não por um runtime com descendentes nesta rodada.
- Descoberta automática da skill em todos os clientes: depende do carregador de cada CLI.

Próximos testes de maior valor: repetir as mesmas tarefas nos clientes efetivamente usados e automatizar a conferência dos artefatos. Uma skill de instruções não substitui controles técnicos de permissões, isolamento ou concorrência.
