# Adaptação ao ambiente

Antes de orquestrar, confira ferramentas expostas, documentação local e restrições efetivas. Não teste capacidades com ações externas desnecessárias. Registre apenas as capacidades que influenciam o trabalho.

| Capacidade observada | Como agir |
|---|---|
| Delegação com modelo e esforço selecionáveis | Escolha valores suportados e envie-os explicitamente |
| Delegação sem seleção de modelo ou esforço | Use o que a ferramenta oferece; registre valores herdados ou não confirmados |
| Agentes com contexto separado | Envie contrato, decisões e referências necessárias |
| Histórico compartilhado obrigatório | Identifique escopos e fontes; não prometa isolamento de contexto |
| Sem subagentes | Execute as etapas sequencialmente no principal; não invente agentes ou nomes de ferramentas |
| Sem revisor independente | Faça autoverificação e identifique-a como tal; revisão independente permanece não realizada se era requisito |
| Sem escrita ou persistência | Mantenha registro na resposta ou recurso disponível; não prometa checkpoint salvo |
| Sem acesso web | Reutilize evidências locais válidas e registre lacunas; não invente benchmarks ou preços |
| Sem descoberta nativa de skills | Receba SKILL.md como instrução e acesse só as referências pertinentes; se não puder lê-las, solicite o conteúdo essencial |

Revisão independente exigida, uma ação externa ou verificação indispensável não passam a estar concluídas apenas porque o ambiente não as suporta. Faça as partes possíveis e informe o requisito pendente.

## Concorrência e subdelegação

A skill não fixa um número de executores. Escolha a concorrência considerando blocos independentes, conflitos de escrita, recursos locais e limites reais do runtime ou definidos pelo usuário. Se o limite for desconhecido, evite abrir lotes grandes; aumente somente conforme necessidade e capacidade observada. Encerre sessões concluídas que pertençam à tarefa e estejam sob sua responsabilidade, após preservar seus resultados, quando continuarem consumindo vagas. Não encerre sessões de terceiros ou de origem desconhecida para liberar capacidade.

O modo padrão é **sem subdelegação**: só o principal cria executores e revisores. Envie essa regra no contrato dos executores. Use uma restrição técnica quando suportada; caso contrário, a regra continua sendo uma instrução, não um bloqueio garantido.

O usuário pode optar por subdelegação. Confirme suporte e defina escopo, concorrência total e profundidade permitida antes de habilitá-la. Os agentes descendentes contam para o limite total. Nenhum executor pode ampliar as próprias permissões.

Com subdelegação, reserve vagas antes de criar descendentes: use quota compartilhada oferecida pelo runtime ou concessões de capacidade registradas pelo coordenador. Não permita que vários executores interpretem a mesma vaga como disponível. Sem meio confiável de coordenar essa reserva, centralize as criações no principal e informe a limitação.

## Preferências opcionais

Não é necessário criar outro arquivo para usar a skill. Respeite as preferências informadas no pedido e na configuração confiável do ambiente.

Se existir `preferences.local.md` na raiz desta skill e sua origem for autorizada pelo usuário, leia-o como preferências locais. Não procure arquivos pessoais em outros diretórios. Esse arquivo é ignorado pelo Git neste repositório; mantenha-o fora de pacotes públicos. Preferências não podem ampliar permissões do ambiente nem prevalecer sobre o pedido atual.

Exemplo de conteúdo opcional, sem modelos ou valores numéricos obrigatórios:

```text
Subdelegação: proibida
Prioridade: qualidade verificada, depois tempo de resposta
Modelo principal: preservar a seleção da sessão
Seleção dos executores: candidatos disponíveis no ambiente
Concorrência: respeitar os limites do runtime
```

Registros locais de modelos preferidos são hipóteses datadas. Reavalie-os por mudança de versão, preço, disponibilidade ou resultados; não os trate como autoridade sobre os dados atuais.
