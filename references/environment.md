# Adaptação ao ambiente

No Claude Code e no Codex, comece pelas referências próprias: [Claude Code](claude-code.md) e [Codex](codex.md). Esta página cobre outras CLIs e os casos em que a sessão não oferece o que elas descrevem.

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
| Sem acesso a arquivos ou execução de comandos | Trabalhe com os materiais fornecidos na entrada; proponha patch ou arquivos completos para aplicação e teste fora da sessão |
| Sem acesso web | Reutilize evidências locais válidas e registre lacunas; não invente benchmarks ou preços |
| Sem descoberta nativa de skills | Receba SKILL.md como instrução e acesse só as referências pertinentes; se não puder lê-las, solicite o conteúdo essencial |

Revisão independente exigida, uma ação externa ou verificação indispensável não passam a estar concluídas apenas porque o ambiente não as suporta. Faça as partes possíveis e informe o requisito pendente.

Quando produzir uma alteração sem poder aplicá-la, distinga análise estática, arquivos propostos, edição confirmada e testes executados. O responsável pela aplicação valida caminhos, escopo e conteúdo antes de editar ou executar. Respeite bloqueios de política; não os trate como autorização para elevar privilégios ou enfraquecer restrições. Se faltar material essencial, solicite-o ou informe o impedimento.

## Concorrência e subdelegação

A skill não fixa um número de executores. Escolha a concorrência considerando blocos independentes, conflitos de escrita, recursos locais e limites reais do runtime ou definidos pelo usuário. Se o limite for desconhecido, evite abrir lotes grandes; aumente somente conforme necessidade e capacidade observada. Encerre sessões concluídas que pertençam à tarefa e estejam sob sua responsabilidade, após preservar seus resultados, quando continuarem consumindo vagas. Não encerre sessões de terceiros ou de origem desconhecida para liberar capacidade.

O modo padrão é **sem subdelegação**: só o principal cria executores e revisores. Envie essa regra no contrato dos executores. Use uma restrição técnica quando suportada; caso contrário, a regra continua sendo uma instrução, não um bloqueio garantido.

O usuário pode optar por subdelegação. Confirme suporte e defina escopo, concorrência total e profundidade permitida antes de habilitá-la. Conte descendentes conforme o limite real do runtime; limites diferem entre produtos. Nenhum executor pode ampliar as próprias permissões.

Com subdelegação, reserve vagas antes de criar descendentes: use quota compartilhada oferecida pelo runtime ou concessões de capacidade registradas pelo coordenador. Não permita que vários executores interpretem a mesma vaga como disponível. Sem meio confiável de coordenar essa reserva, centralize as criações no principal e informe a limitação.

## Preferências opcionais

Não é necessário criar outro arquivo para usar a skill. Respeite as preferências informadas no pedido e na configuração confiável do ambiente.

Se existir `preferences.local.md` na raiz desta skill, leia-o como preferências locais do usuário. Não procure arquivos pessoais em outros diretórios. Esse arquivo é ignorado pelo Git neste repositório; mantenha-o fora de pacotes públicos. Preferências não podem ampliar permissões do ambiente nem prevalecer sobre o pedido atual.

Exemplo de conteúdo opcional. Guarde critérios, não modelos: a escolha atual é só o resultado dos critérios aplicados a um retrato e é refeita quando o retrato muda. Os nomes abaixo são ilustrativos:

```text
Subdelegação: proibida
Prioridade: qualidade verificada, depois cota
Cobrança: assinatura (custo = cota)
Modelo principal: preservar a seleção da sessão

Critérios por faixa:
  1: perfil leitura, Intel mínimo 15
  2: perfil codigo, capacidade da área, 90% do principal
Escolha atual (retrato de AAAA-MM-DD):
  Claude Code: 1 = model=haiku, effort=low; 2 = model=sonnet, effort=medium
  Codex: 1 = agente leitor-barato (modelo leve, low); 2 = modelo intermediário, medium
Mapeamento Artificial Analysis → CLI:
  "Claude 5.5 Haiku" → haiku
Calibração: faixa 2 em migração SQL refeita 2x → piso 95%
```

Registros locais de modelos preferidos são hipóteses datadas. Refaça a escolha atual quando o retrato for atualizado, surgir modelo novo na CLI ou a calibração indicar; não a trate como autoridade sobre os dados atuais.
