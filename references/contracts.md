# Contratos, decisões e evidências

## Contrato de execução

Antes de delegar, forneça:

```text
Objetivo e resultado esperado:
Premissas, materiais e referências:
Modelo e esforço selecionados, se suportados:
Subdelegação permitida ou proibida:
Arquivos e escopo de escrita:
Ações e ferramentas permitidas:
Dependências e restrições:
Critérios de aceitação e verificações:
Condição de parada e escalonamento:
Entrega esperada:
Skills aplicáveis e seus caminhos, quando disponíveis:
```

Adapte a forma ao trabalho; o contrato delimita a autoridade já concedida. Dê acesso aos dados necessários. Não trate esse texto como bloqueio técnico de ferramentas. Há um [contrato preenchido](examples.md) para referência.

Distinga parâmetros enviados à ferramenta, valores confirmados pelo runtime e preferências descritas em texto. Defina progresso por evidência do objetivo, como uma verificação que passou ou uma hipótese resolvida; nova mensagem, outro erro ou mais arquivos editados não bastam.

O retorno inclui `status` (`concluido`, `bloqueado` ou `escalar`), achados ou alterações, verificações realizadas e seus resultados, evidências, conflitos e pendências. Evidências devem permitir conferência: arquivo e linha, comando e código de saída, artefato, URL e trecho relevante. Uma afirmação de sucesso do executor não basta.

## Decisão isolada

Quando separar decisão e execução trouxer benefício, o coordenador define uma lista finita de ações autorizadas, sempre incluindo `ESCALAR`. O decisor apenas consulta evidências e retorna:

```json
{
  "acao": "ESCALAR",
  "evidencias": ["referência verificável ao fato observado"],
  "motivo_escalonamento": "falta de informação necessária"
}
```

Não acrescentar prosa fora do objeto nesse modo. Para outra ação autorizada, `motivo_escalonamento` pode ser nulo. O decisor não altera arquivos nem executa a ação escolhida.

O executor ou coordenador valida tipos, campos, ação permitida, evidências, precondições e autorização. Campos bem formados não comprovam verdade nem permissão. Ação desconhecida, evidência ausente ou precondição falsa deve impedir execução e levar à correção delimitada ou escalonamento.

Em automações, implemente essa validação em código antes de qualquer efeito externo. A instrução não cria um schema aplicado pelo runtime nem produz probabilidades calibradas. Use saída estruturada nativa se disponível e confirme o que ela efetivamente valida.

## Revisão final

O principal verifica cobertura, consistência entre entregas, mudanças integradas e critérios de aceitação. Pode aprovar, pedir uma correção delimitada ou assumir o ponto difícil. Consulte as fontes originais para achados críticos ou contestados; não repita pesquisas e testes válidos sem motivo concreto.

Informe verificações não realizadas e pendências. Um resultado bloqueado é uma entrega de estado, não o cumprimento do objetivo.
