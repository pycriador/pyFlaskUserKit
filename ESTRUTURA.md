# 📁 Estrutura do Projeto pyFlaskUserKit

## 🌳 Árvore de Diretórios

```
pyFlaskUserKit/
│
├── 📄 README.md                    # Documentação completa do projeto
├── 📄 QUICKSTART.md                # Guia de início rápido
├── 📄 ESTRUTURA.md                 # Este arquivo
├── 📄 LICENSE                      # Licença MIT
├── 📄 requirements.txt             # Dependências Python
├── 📄 env.example                  # Exemplo de configuração .env
├── 📄 .gitignore                   # Arquivos ignorados pelo Git
├── 📄 config.py                    # Configurações da aplicação
├── 📄 run.py                       # Script para iniciar o servidor
│
├── 📁 app/                         # Pacote principal da aplicação
│   ├── 📄 __init__.py              # Factory da aplicação Flask
│   ├── 📄 models.py                # Modelos de dados (User, Group)
│   │
│   ├── 📁 routes/                  # Rotas da aplicação
│   │   ├── 📄 __init__.py
│   │   ├── 📄 api.py               # Endpoints da API REST
│   │   └── 📄 web.py               # Rotas da interface web
│   │
│   ├── 📁 static/                  # Arquivos estáticos
│   │   ├── 📁 css/
│   │   │   └── 📄 style.css        # Estilos customizados + temas
│   │   └── 📁 js/
│   │       ├── 📄 main.js          # Funções JavaScript globais
│   │       ├── 📄 users.js         # JavaScript da página de usuários
│   │       └── 📄 groups.js        # JavaScript da página de grupos
│   │
│   └── 📁 templates/               # Templates HTML
│       ├── 📄 base.html            # Template base (navbar, footer, etc)
│       ├── 📄 index.html           # Página inicial
│       ├── 📄 users.html           # Página de gerenciamento de usuários
│       ├── 📄 groups.html          # Página de gerenciamento de grupos
│       └── 📄 docs.html            # Documentação da API
│
├── 📁 scripts/                     # Scripts utilitários
│   └── 📄 init_db.py               # Script de inicialização do banco
│
└── 📁 instance/                    # Criado automaticamente
    └── 📄 app.db                   # Banco de dados SQLite (criado na inicialização)
```

## 📊 Estatísticas do Projeto

### Arquivos Criados
- **Python:** 8 arquivos
- **JavaScript:** 3 arquivos
- **HTML:** 5 templates
- **CSS:** 1 arquivo
- **Documentação:** 3 arquivos
- **Configuração:** 4 arquivos

### Total: 24 arquivos principais

## 🎯 Principais Componentes

### Backend (Python/Flask)

#### `config.py`
- Gerencia todas as configurações da aplicação
- Suporte para SQLite e MySQL/MariaDB
- Lê variáveis de ambiente do arquivo `.env`

#### `app/__init__.py`
- Factory pattern para criação da aplicação
- Inicializa extensões (SQLAlchemy, Migrate)
- Registra blueprints (rotas)
- Cria grupos padrão automaticamente

#### `app/models.py`
- **User:** Modelo de usuário com autenticação
- **Group:** Modelo de grupo
- Relacionamento many-to-many entre User e Group
- Métodos auxiliares (`to_dict()`, `set_password()`, etc)

#### `app/routes/api.py`
- **16 endpoints** para gerenciamento de usuários
- **6 endpoints** para gerenciamento de grupos
- Retorna dados em formato JSON
- Tratamento de erros completo

#### `app/routes/web.py`
- Rotas para renderização de páginas HTML
- 4 rotas principais: home, usuários, grupos, documentação

#### `scripts/init_db.py`
- Cria tabelas do banco de dados
- Cria grupos padrão (Administradores, Visualizadores, Editores)
- Cria usuário administrador
- Modo interativo ou via variáveis de ambiente

### Frontend (HTML/CSS/JavaScript)

#### Templates HTML
- **base.html:** Layout base com navbar, tema toggle, alertas
- **index.html:** Dashboard com cards informativos
- **users.html:** Interface completa de gerenciamento de usuários
- **groups.html:** Interface completa de gerenciamento de grupos
- **docs.html:** Documentação detalhada da API

#### CSS (`style.css`)
- Variáveis CSS para temas (claro/escuro)
- Estilos customizados para Bootstrap
- Animações e transições
- Responsivo para desktop e mobile
- ~400 linhas de CSS

#### JavaScript
- **main.js:** Funções globais (tema, alertas, API helpers)
- **users.js:** Lógica da página de usuários (CRUD, filtros, modais)
- **groups.js:** Lógica da página de grupos (CRUD, visualização de membros)
- jQuery para manipulação DOM e AJAX

## 🔐 Segurança

### Implementado
- ✅ Hash de senhas com Werkzeug (PBKDF2)
- ✅ SECRET_KEY via variável de ambiente
- ✅ Validação de dados em todas as rotas
- ✅ SQLAlchemy ORM (proteção contra SQL Injection)
- ✅ Sem credenciais hardcoded no código

### Recomendado para Produção
- 🔸 Adicionar autenticação JWT ou sessões
- 🔸 Implementar autorização baseada em roles
- 🔸 Rate limiting
- 🔸 HTTPS/SSL
- 🔸 CSRF protection
- 🔸 Logs de auditoria

## 🎨 Recursos da Interface

### Tema Claro/Escuro
- Alternância com um clique
- Persistência via localStorage
- Cores otimizadas para legibilidade
- Transições suaves

### Modais
- Adicionar usuário/grupo
- Editar usuário/grupo
- Resetar senha
- Confirmar exclusão
- Visualizar membros do grupo

### Filtros e Busca
- Busca em tempo real (debounced)
- Filtro por status (ativo/inativo)
- Filtro por tipo (admin/regular)
- Busca por nome, email, descrição

### Feedback Visual
- Alertas coloridos (sucesso, erro, aviso, info)
- Ícones do Bootstrap Icons
- Loading spinners
- Badges de status

## 📡 API REST

### Categorias de Endpoints

#### Usuários - CRUD Básico
- GET `/api/users` - Listar todos
- GET `/api/users/{id}` - Obter um
- POST `/api/users` - Criar
- PUT `/api/users/{id}` - Atualizar
- DELETE `/api/users/{id}` - Deletar

#### Usuários - Ações Especiais
- POST `/api/users/{id}/activate` - Ativar
- POST `/api/users/{id}/deactivate` - Inativar
- POST `/api/users/{id}/make-admin` - Tornar admin
- POST `/api/users/{id}/remove-admin` - Remover admin
- POST `/api/users/{id}/reset-password` - Resetar senha

#### Usuários - Grupos
- POST `/api/users/{id}/groups` - Adicionar a grupos
- DELETE `/api/users/{id}/groups/{group_id}` - Remover de grupo

#### Grupos - CRUD Completo
- GET `/api/groups` - Listar todos
- GET `/api/groups/{id}` - Obter um
- POST `/api/groups` - Criar
- PUT `/api/groups/{id}` - Atualizar
- DELETE `/api/groups/{id}` - Deletar
- GET `/api/groups/{id}/users` - Listar membros

## 🗄️ Banco de Dados

### SQLite (Padrão)
- Arquivo: `instance/app.db`
- Sem configuração adicional
- Ideal para desenvolvimento
- Portável

### MySQL/MariaDB (Opcional)
- Configurável via `.env`
- Ideal para produção
- Suporte a múltiplos usuários simultâneos

### Esquema de Tabelas

#### Users
- id (PK)
- username (unique)
- email (unique)
- password_hash
- is_admin (boolean)
- is_active (boolean)
- created_at
- updated_at

#### Groups
- id (PK)
- name (unique)
- description
- created_at
- updated_at

#### user_groups (Associação)
- user_id (FK → users.id)
- group_id (FK → groups.id)

## 🚀 Comandos Úteis

### Desenvolvimento
```bash
# Ativar ambiente virtual
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt

# Inicializar banco
python scripts/init_db.py

# Iniciar servidor
python run.py
```

### Testar API
```bash
# Listar usuários
curl http://localhost:5000/api/users

# Criar usuário
curl -X POST http://localhost:5000/api/users \
  -H "Content-Type: application/json" \
  -d '{"username":"teste","email":"teste@example.com","password":"123"}'
```

## 📝 Arquivos de Configuração

### `.env` (criar a partir do env.example)
```env
DATABASE_TYPE=sqlite              # ou mysql
SQLITE_DB_PATH=instance/app.db
SECRET_KEY=chave-secreta-aqui
ADMIN_USERNAME=admin
ADMIN_EMAIL=admin@example.com
ADMIN_PASSWORD=admin123
```

### `requirements.txt`
```
Flask
Flask-SQLAlchemy
Flask-Migrate
python-dotenv
pymysql
cryptography
Werkzeug
```

## 🎓 Tecnologias Utilizadas

### Backend
- Python 3.8+
- Flask (framework web)
- SQLAlchemy (ORM)
- Werkzeug (segurança)

### Frontend
- HTML5
- CSS3 (variáveis, grid, flexbox)
- Bootstrap 5 (framework CSS)
- jQuery 3.7 (AJAX, DOM)
- Bootstrap Icons

### Banco de Dados
- SQLite (desenvolvimento)
- MySQL/MariaDB (produção)

## 📦 Dependências

Todas listadas em `requirements.txt`:
- Flask - Framework web
- Flask-SQLAlchemy - ORM
- Flask-Migrate - Migrações
- python-dotenv - Variáveis de ambiente
- pymysql - Driver MySQL
- cryptography - Criptografia
- Werkzeug - Segurança

## 🌟 Destaques

### Código Limpo
- Estrutura organizada em módulos
- Comentários em inglês (padrão de código)
- PEP 8 compliant
- Factory pattern

### UX/UI Moderna
- Design responsivo
- Tema claro/escuro
- Feedback imediato
- Animações suaves

### Segurança
- Senhas com hash
- Validações
- Sem credenciais no código
- ORM (proteção SQL Injection)

### Documentação
- README completo
- QUICKSTART para início rápido
- Documentação da API integrada
- Comentários no código

---

**🎉 Projeto completo e pronto para uso!**


