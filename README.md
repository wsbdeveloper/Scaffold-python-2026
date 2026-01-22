# Scaffold Python

Sistema de análise e decisão de crédito desenvolvido com **FastAPI**, **Clean Code** e **Arquitetura Hexagonal**.

## Requisitos

- Python 3.11+
- PostgreSQL 15+ (ou usar Docker Compose)
- pip

## Instalação

### 1. Clone o repositório (ou navegue até o diretório)

```bash
cd /path/to/your/project
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
-- se necessário, ajuste o nome do banco.
CREATE DATABASE table_scaffold;
```

### 6. Execute as migrations

```bash
alembic upgrade head
```

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

### Pre-commit Hooks

O projeto utiliza **pre-commit** para executar automaticamente o Ruff e MyPy antes de cada commit, garantindo que apenas código validado seja commitado.

**Instalar os hooks (após instalar as dependências):**
```bash
pre-commit install
```

**Executar os hooks manualmente em todos os arquivos:**
```bash
pre-commit run --all-files
```

**Pular os hooks em um commit específico (não recomendado):**
```bash
git commit --no-verify -m "mensagem"
```

Os hooks executam automaticamente:
- **Ruff linter** (com correções automáticas)
- **Ruff formatter**
- **MyPy type checker**
- Verificações básicas (whitespace, YAML, JSON, etc.)

### Comandos Úteis

**Executar todas as verificações:**
```bash
ruff check . && ruff format --check . && mypy .
```

**Corrigir e formatar tudo:**
```bash
ruff check --fix . && ruff format .
```

**Testar os hooks do pre-commit:**
```bash
pre-commit run --all-files
```

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
