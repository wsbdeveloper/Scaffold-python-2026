# Arquitetura do Motor de Crédito

## Visão Geral

Este documento descreve a arquitetura do Motor de Decisão de Crédito, desenvolvido seguindo os princípios de **Clean Code** e **Arquitetura Hexagonal** (Ports and Adapters).

## Princípios Arquiteturais

### Arquitetura Hexagonal

A arquitetura hexagonal separa a aplicação em três camadas principais:

1. **Domain (Domínio)**: Contém as entidades de negócio e regras puras, sem dependências externas
2. **Application (Aplicação)**: Contém os serviços de aplicação e DTOs
3. **Infrastructure (Infraestrutura)**: Implementações concretas (banco de dados, APIs externas)
4. **Interfaces**: Portas de entrada (API REST, Engine)

O domínio está no centro e não depende de nada externo. As camadas externas dependem do domínio.

## Principais Entidades do Domínio

### Applicant (Solicitante)
Representa um solicitante de crédito com:
- `document_number`: CPF ou documento similar
- `name`: Nome completo
- `monthly_income`: Renda mensal
- `age`: Idade

### Proposal (Proposta)
Representa uma proposta de crédito com:
- `applicant`: Dados do solicitante
- `requested_amount`: Valor solicitado
- `installments`: Número de parcelas
- `product_type`: Tipo de produto (PERSONAL_LOAN, etc.)
- `channel`: Canal de origem (APP, BACKOFFICE, PARTNER_X)

### Policy (Política)
Representa uma política de crédito com:
- `name`: Nome da política (ex: DEFAULT_POLICY_V1)
- `version`: Versão da política
- `product_types`: Lista de tipos de produto que a política cobre
- `channels`: Lista de canais que a política cobre
- `is_active`: Se a política está ativa

### Decision (Decisão)
Representa uma decisão de crédito com:
- `proposal_id`: ID da proposta analisada
- `status`: Status (APPROVED, REJECTED, PENDING_DOCS)
- `policy_name`: Nome da política aplicada
- `policy_version`: Versão da política aplicada
- `rule_results`: Lista de resultados das regras avaliadas

### RuleResult (Resultado de Regra)
Resultado da avaliação de uma regra específica:
- `rule_code`: Código único da regra
- `passed`: Se a regra passou ou não
- `message`: Mensagem descritiva (opcional)
- `metadata`: Metadados adicionais (opcional)

## Motor de Decisão

### DecisionEngine

O `DecisionEngine` é o coração do sistema. Ele:
1. Recebe uma `Proposal` e uma `Policy`
2. Executa todas as regras configuradas
3. Coleta os resultados de cada regra
4. Determina o status final (APPROVED se todas passaram, REJECTED caso contrário)
5. Retorna uma `Decision`

### Regras (Rules)

As regras implementam a interface `Rule` e são independentes entre si. Cada regra:
- Tem um código único (`code`)
- Tem um nome (`name`)
- Implementa `evaluate(proposal)` que retorna um `RuleResult`

**Regras Implementadas:**
1. `MinIncomeRule`: Verifica renda mínima (R$ 1.000,00)
2. `MaxIncomeCommitmentRule`: Verifica comprometimento máximo de renda (30%)
3. `AgeRangeRule`: Verifica faixa etária (18-65 anos)
4. `MaxInstallmentsRule`: Verifica número máximo de parcelas (84)

**Como adicionar uma nova regra:**
1. Criar uma classe que herda de `Rule`
2. Implementar `code`, `name` e `evaluate`
3. Adicionar a regra à lista de regras no `DecisionEngine` (no router)

## Fluxo de Decisão

```
1. Cliente faz requisição POST /credit_decisions
   ↓
2. Controller recebe ProposalRequestDTO
   ↓
3. CreditDecisionService.analyze_proposal():
   a. Converte DTO para entidade Proposal
   b. Busca Policy aplicável (via PolicyRepository)
   c. Salva Proposal (via ProposalRepository)
   d. Executa DecisionEngine.evaluate()
   e. Salva Decision (via DecisionRepository)
   ↓
4. Retorna DecisionResponseDTO
```

## Extensibilidade

### Adicionar Novo Tipo de Produto

1. Adicionar novo valor ao enum `ProductType`
2. Criar/atualizar política no banco que inclua o novo produto
3. (Opcional) Criar regras específicas para o produto

**Exemplo:**
```python
# domain/value_objects/product_type.py
class ProductType(str, Enum):
    PERSONAL_LOAN = "PERSONAL_LOAN"
    PAYROLL_LOAN = "PAYROLL_LOAN"  # Novo
    CREDIT_CARD = "CREDIT_CARD"     # Novo
```

### Adicionar Nova Política

1. Criar registro na tabela `policies` com:
   - `name`: Nome único (ex: CONVENIO_ABC_POLICY_V1)
   - `version`: Versão (ex: 1.0)
   - `product_types`: JSON array dos produtos
   - `channels`: JSON array dos canais
   - `is_active`: true

2. O sistema automaticamente seleciona a política baseado em produto + canal

**Exemplo SQL:**
```sql
INSERT INTO policies (id, name, version, product_types, channels, is_active)
VALUES (
    gen_random_uuid(),
    'CONVENIO_ABC_POLICY_V1',
    '1.0',
    '["PERSONAL_LOAN"]',
    '["APP", "BACKOFFICE"]',
    true
);
```

### Adicionar Nova Regra

1. Criar classe que herda de `Rule`
2. Implementar métodos obrigatórios
3. Adicionar à lista de regras no router (ou em um factory/configuração futura)

**Exemplo:**
```python
class NewCustomRule(Rule):
    @property
    def code(self) -> str:
        return "CUSTOM_RULE_CODE"

    @property
    def name(self) -> str:
        return "Custom Rule"

    async def evaluate(self, proposal: Proposal) -> RuleResult:
        # Lógica da regra
        passed = ...
        return RuleResult(rule_code=self.code, passed=passed, ...)
```

### Versionamento de Políticas

O sistema suporta versionamento através dos campos `name` e `version` da `Policy`. Para criar uma nova versão:

1. Criar novo registro com mesmo `name` mas `version` diferente
2. Desativar versão antiga (`is_active = false`)
3. O sistema seleciona a política ativa mais recente (poderia ser melhorado com ordenação por versão)

**Futuras melhorias:**
- Adicionar campo `effective_date` para controle de vigência
- Ordenar políticas por versão/data
- Suportar múltiplas políticas ativas simultaneamente com prioridade

### Desativar Regras

Para desativar uma regra sem remover código:
1. Remover a regra da lista no router/factory
2. Ou criar um sistema de configuração de regras por política (futuro)

**Futuras melhorias:**
- Tabela `policy_rules` que mapeia políticas para regras ativas
- Configuração de regras por política via banco de dados
- Desativação sem deploy

## Modelagem de Banco de Dados

### Tabelas Principais

1. **applicants**: Dados dos solicitantes
2. **proposals**: Propostas de crédito
3. **policies**: Políticas de crédito
4. **decisions**: Decisões de crédito

### Relacionamentos

- `proposals.applicant_id` → `applicants.id` (N:1)
- `decisions.proposal_id` → `proposals.id` (1:1)
- `policies` é independente (tabela de configuração)

### Extensibilidade no Banco

- `policies.product_types` e `policies.channels` são JSON para flexibilidade
- `decisions.rule_results` é JSON para armazenar resultados dinâmicos
- Campos genéricos podem ser adicionados sem breaking changes

## Decisões de Design

### Por que Arquitetura Hexagonal?

- **Testabilidade**: Domínio pode ser testado sem banco/API
- **Flexibilidade**: Fácil trocar implementações (ex: PostgreSQL → MongoDB)
- **Manutenibilidade**: Separação clara de responsabilidades
- **Extensibilidade**: Novas funcionalidades não quebram código existente

### Por que FastAPI?

- Type hints nativos (compatível com nossa abordagem)
- Async/await (preparado para escalabilidade)
- Documentação automática (Swagger)
- Performance

### Por que SQLAlchemy + Alembic?

- ORM maduro e flexível
- Migrations versionadas
- Suporte a múltiplos bancos
- Type hints com SQLAlchemy 2.0

### Por que Regras como Classes Separadas?

- **Single Responsibility**: Cada regra tem uma responsabilidade
- **Open/Closed**: Abrir para extensão, fechado para modificação
- **Fácil Teste**: Regras podem ser testadas isoladamente
- **Fácil Desativação**: Remover da lista sem modificar código

### Estrutura de Regras

Optamos por regras como classes ao invés de funções para:
- Poder adicionar configuração por regra (ex: limites diferentes)
- Facilitar injeção de dependências futuras
- Manter interface consistente

## Fluxo de Dados

```
API Request (JSON)
    ↓
DTO (Pydantic)
    ↓
Service (Application Layer)
    ↓
Domain Entities
    ↓
Repository (Interface)
    ↓
Repository Implementation (Infrastructure)
    ↓
Database Model (SQLAlchemy)
    ↓
Database (PostgreSQL)
```

## Testes

### Estrutura de Testes

- `tests/unit/`: Testes de unidades (regras, entidades)
- `tests/integration/`: Testes de integração (serviços, repositórios)

### Estratégia

- **Unit Tests**: Testam regras isoladamente
- **Integration Tests**: Testam fluxo completo com banco em memória (SQLite)
