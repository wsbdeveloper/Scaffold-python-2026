# Motor de Decisão de Crédito

Sistema de análise e decisão de crédito desenvolvido com **FastAPI**, **Clean Code** e **Arquitetura Hexagonal**.

## Requisitos

- Python 3.11+
- PostgreSQL 15+ (ou usar Docker Compose)
- pip

## Instalação

### 1. Clone o repositório (ou navegue até o diretório)

```bash
cd teste-backend
```

### 2. Crie um ambiente virtual

```bash
python3 -m venv venv
source venv/bin/activate
venv\Scripts\activate  # Windows
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure as variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto:

```bash
cp .env.example .env
```

Edite o `.env` com suas configurações:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/credit_engine
DEBUG=True
```

### 5. Inicie o PostgreSQL

#### Opção A: Usando Docker Compose (Recomendado)

```bash
docker-compose up -d
```

#### Opção B: PostgreSQL local

Certifique-se de que o PostgreSQL está rodando e crie o banco:

```sql
CREATE DATABASE credit_engine;
```

### 6. Execute as migrations

```bash
alembic upgrade head
```

### 7. (Opcional) Seed da política padrão

O sistema cria automaticamente a política padrão na primeira execução, mas você pode executar manualmente se necessário. A política `DEFAULT_POLICY_V1` é criada automaticamente via seed no código.

## Executando a Aplicação

```bash
python main.py
```

Ou usando uvicorn diretamente:

```bash
uvicorn credit_engine.main:app --host 0.0.0.0 --port 8000 --reload
```


## Documentação da API

Após iniciar a aplicação, acesse:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc



### Exemplos Visuais

Algumas evidências dos testes via swagger, pode encontrar tbm nos arquivos que deixei na raiz do projeto.

#### 1. **ID da Decisão** (`decision_id`)

Exemplo de valor retornado para o campo `"id"` da decisão:

![Exemplo Decision ID](./decision_id.png)

#### 2. **ID da Proposta** (`proposta_id`)

Exemplo de valor retornado para o campo `"proposal_id"`:

![Exemplo Proposta ID](./proposta_id.png)

#### 3. **Swagger UI da API**

Acesse a documentação interativa da API (Swagger UI):

![Swagger UI](swagger.png)

## Executando os Testes

```bash
pytest
```

Para executar com cobertura:

```bash
pytest --cov=src/credit_engine --cov-report=html
```

## Qualidade de Código

O projeto utiliza **Ruff** (linter e formatter) e **MyPy** (type checker) para garantir qualidade e consistência do código.

### Ruff - Linter e Formatter

O Ruff é uma ferramenta rápida que combina funcionalidades de linter e formatter.

**Verificar problemas de lint:**
```bash
ruff check .
```

**Corrigir problemas automaticamente:**
```bash
ruff check --fix .
```

**Formatar código:**
```bash
ruff format .
```

**Verificar e formatar tudo:**
```bash
ruff check --fix . && ruff format .
```

### MyPy - Type Checker

O MyPy verifica a tipagem estática do código Python.

**Verificar tipos:**
```bash
mypy .
```

**Verificar tipos com mais detalhes:**
```bash
mypy . --show-error-codes
```

### Integração com VS Code

O projeto está configurado para usar Ruff e MyPy automaticamente no VS Code através do `.devcontainer/devcontainer.json`:

- **Ruff** é usado como formatter padrão (substitui Black/Isort)
- **Ruff** também funciona como linter
- **MyPy** verifica tipos automaticamente
- Formatação e organização de imports acontecem automaticamente ao salvar

### Comandos Úteis

**Executar todas as verificações:**
```bash
ruff check . && ruff format --check . && mypy .
```

**Corrigir e formatar tudo:**
```bash
ruff check --fix . && ruff format .
```

## Exemplos de Uso

### Submeter uma Proposta para Análise

**POST** `/credit_decisions`

```json
{
  "applicant": {
    "document_number": "12345678900",
    "name": "João Silva",
    "monthly_income": 5000.0,
    "age": 30
  },
  "requested_amount": 10000.0,
  "installments": 24,
  "product_type": "PERSONAL_LOAN",
  "channel": "APP"
}
```

**Resposta (201 Created):**

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "proposal_id": "550e8400-e29b-41d4-a716-446655440001",
  "status": "APPROVED",
  "policy_name": "DEFAULT_POLICY_V1",
  "policy_version": "1.0",
  "rejected_reasons": [],
  "rule_results": [
    {
      "rule_code": "MIN_INCOME_NOT_MET",
      "passed": true,
      "message": null,
      "metadata": {
        "min_income": 1000.0,
        "applicant_income": 5000.0
      }
    },
    {
      "rule_code": "MAX_INCOME_COMMITMENT_EXCEEDED",
      "passed": true,
      "message": null,
      "metadata": {
        "max_commitment": 0.3,
        "calculated_commitment": 0.1667,
        "monthly_payment": 416.67
      }
    },
    {
      "rule_code": "AGE_OUT_OF_RANGE",
      "passed": true,
      "message": null,
      "metadata": {
        "min_age": 18,
        "max_age": 65,
        "applicant_age": 30
      }
    },
    {
      "rule_code": "MAX_INSTALLMENTS_EXCEEDED",
      "passed": true,
      "message": null,
      "metadata": {
        "max_installments": 84,
        "requested_installments": 24
      }
    }
  ],
  "created_at": "2024-01-01T12:00:00"
}
```

### Consultar uma Decisão

**GET** `/credit_decisions/{proposal_id}`

**Resposta (200 OK):**

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "proposal_id": "550e8400-e29b-41d4-a716-446655440001",
  "status": "APPROVED",
  "policy_name": "DEFAULT_POLICY_V1",
  "policy_version": "1.0",
  "rejected_reasons": [],
  "rule_results": [...],
  "created_at": "2024-01-01T12:00:00"
}
```

### Exemplo de Proposta Rejeitada

```json
{
  "applicant": {
    "document_number": "98765432100",
    "name": "Maria Santos",
    "monthly_income": 500.0,
    "age": 30
  },
  "requested_amount": 5000.0,
  "installments": 12,
  "product_type": "PERSONAL_LOAN",
  "channel": "APP"
}
```

**Resposta (201 Created):**

```json
{
  "status": "REJECTED",
  "rejected_reasons": [
    "MIN_INCOME_NOT_MET"
  ],
  "rule_results": [
    {
      "rule_code": "MIN_INCOME_NOT_MET",
      "passed": false,
      "message": "Minimum income not met. Required: 1000.0, Provided: 500.0",
      "metadata": {
        "min_income": 1000.0,
        "applicant_income": 500.0
      }
    },
    ...
  ]
}
```

## Arquitetura

Para entender melhor a arquitetura do sistema, consulte [ARCHITECTURE.md](ARCHITECTURE.md).

## Comandos Úteis

### Migrations

```bash
# Criar nova migration
alembic revision --autogenerate -m "description"

# Aplicar migrations
alembic upgrade head

# Reverter última migration
alembic downgrade -1

# Ver histórico
alembic history
```

### Desenvolvimento

```bash
# Formatar código (se usar black)
black src/

# Ordenar imports (se usar isort)
isort src/

# Verificar tipos (se usar mypy)
mypy src/
```

## Docker

Para desenvolvimento, use o Docker Compose para o PostgreSQL:

```bash
# Iniciar
docker-compose up -d

# Parar
docker-compose down

# Ver logs
docker-compose logs -f postgres

# Remover volumes (limpar dados)
docker-compose down -v
```
