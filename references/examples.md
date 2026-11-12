# Exemplos de aplicação

Os caminhos, nomes de modelos e comandos abaixo são fictícios; confirme os equivalentes no ambiente antes de agir.

## Contrato de migração delimitada

```text
Objetivo: atualizar os consumidores de fetchUser para getAccount no pacote billing.
Premissas: o principal já alterou a API compartilhada e confirmou o novo retorno.
Materiais: contrato de API, inventário de chamadas e decisão de compatibilidade.
Modelo: executor disponível adequado a alterações delimitadas; esforço padrão
        (a ferramenta deste exemplo não permite selecionar esforço).
Escrita: packages/billing/src e packages/billing/test.
Proibido: alterar API compartilhada, outros pacotes ou executar deploy.
Subdelegação: proibida; necessidades adicionais retornam ao principal.
Aceitação: chamadas inventariadas atualizadas, comportamento preservado,
           testes do pacote e análise de tipos aprovados.
Verificação: comandos documentados no projeto; registrar resultados e falhas prévias.
Correção: diante de falha, investigar e fazer uma correção; se persistir sem progresso,
          retornar o erro completo, hipótese e mudanças para o principal.
Entrega: diff, itens cobertos, comandos/códigos de saída, conflitos e pendências.
```

O principal valida o pacote, reconcilia o inventário e testa a integração. Uma contagem de arquivos alterados não substitui a evidência de comportamento.

## Seleção provisória sem internet

```text
Tarefa: extrair datas de documentos conhecidos.
Candidatos: leitor-A e geral-B (nomes fictícios).
Disponibilidade: ambos expostos pela ferramenta; principal escolhido preservado.
Evidência: leitor-A passou nas verificações locais recentes desta mesma transformação.
Esforço: herdado e não exposto; sem tentativa de inventar configuração.
Custos/benchmark externo: desconhecidos; rede indisponível nesta execução.
Escolha: leitor-A como candidato provisório, com validação das datas contra as fontes.
Reavaliar: falha de fidelidade, mudança de documentos ou evidência nova de capacidade.
Conclusão econômica: não estabelecida.
```

## Retomada e cobertura

Um relatório contém 40 afirmações. O resumo diz sucesso, mas o registro aponta 35 verificadas, três pendentes e duas sem fonte. O coordenador reconcilia os identificadores com o relatório e preserva verificações ainda válidas; as cinco restantes não viram sucesso por estarem mencionadas no resumo.

Um checkpoint útil contém:

```text
Objetivo/restrições: verificar 40 afirmações, sem publicar antes da conclusão.
Itens: IDs C01–C40, fonte, estado e resultado da revisão de cada um.
Estado: 35 verificadas, 3 pendentes, 2 sem fonte.
Artefatos: relatório e evidências, com versão/hash quando disponível.
Próximo passo: completar fontes e confirmar conflitos; sintetizar cobertura.
Efeitos externos: publicação não iniciada / confirmada / desconhecida.
```

Após interrupção, confira os artefatos. Se uma publicação já autorizada estiver em estado desconhecido, consulte o destino ou execução existente antes de repetir. Um efeito não confirmado permanece pendente.
