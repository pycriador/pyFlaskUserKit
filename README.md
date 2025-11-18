# pyFlaskUserKit

Sistema completo de gerenciamento de usuários e grupos desenvolvido em Python com Flask, SQLAlchemy e interface web moderna.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-Latest-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 📋 Índice

- [Sobre](#sobre)
- [Características](#características)
- [Tecnologias](#tecnologias)
- [Requisitos](#requisitos)
- [Instalação](#instalação)
- [Configuração](#configuração)
- [Inicialização](#inicialização)
- [Uso](#uso)
- [API REST](#api-rest)
- [Exemplos de Código](#exemplos-de-código)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Segurança](#segurança)
- [Licença](#licença)

## 🎯 Sobre

O **pyFlaskUserKit** é uma aplicação web completa que serve como bootstrap para sistemas que necessitam de gerenciamento de usuários e grupos. Oferece tanto uma API REST quanto uma interface web moderna, 100% server-side, sem dependência de JavaScript para operações CRUD.

## ✨ Características

### Gerenciamento de Usuários
- ✅ Criar, editar e deletar usuários
- ✅ Ativar/inativar usuários
- ✅ Resetar senhas
- ✅ Promover usuários a administradores
- ✅ Associar usuários a múltiplos grupos
- ✅ Autenticação segura com hash de senhas (Werkzeug/PBKDF2)
- ✅ Acesso direto por ID na URL (`/usuarios/1`)

### Gerenciamento de Grupos
- ✅ Criar, editar e deletar grupos
- ✅ Visualizar membros de cada grupo
- ✅ Adicionar/remover usuários de grupos
- ✅ Grupos padrão pré-configurados
- ✅ Acesso direto por ID na URL (`/grupos/1`)

### Interface Web
- ✅ Design moderno e responsivo (Bootstrap 5)
- ✅ Tema claro e escuro com alternador
- ✅ 100% server-side rendering (sem JavaScript para CRUD)
- ✅ Formulários HTML tradicionais
- ✅ Mensagens de feedback com flash messages
- ✅ Funciona em desktop e mobile
- ✅ Tela de login elegante

### API REST
- ✅ Endpoints completos para usuários e grupos
- ✅ Formato JSON
- ✅ Operações CRUD completas
- ✅ Protegida por autenticação (apenas admin)
- ✅ Documentação pública integrada
- ✅ Exemplos em 4 linguagens (Python, cURL, PHP, Node.js)

### Configuração
- ✅ Suporte a SQLite (padrão)
- ✅ Suporte a MySQL/MariaDB
- ✅ Configuração via arquivo .env
- ✅ Script de inicialização do banco
- ✅ Script interativo para criar admin
- ✅ **SEM credenciais hardcoded no código**

## 🛠 Tecnologias

### Backend
- **Python 3.8+**
- **Flask** - Framework web
- **Flask-SQLAlchemy** - ORM
- **Flask-Migrate** - Migrações de banco
- **Werkzeug** - Segurança e hash de senhas
- **python-dotenv** - Gerenciamento de variáveis de ambiente

### Frontend
- **HTML5**
- **CSS3** com variáveis CSS para temas
- **Bootstrap 5** - Framework CSS
- **Bootstrap Icons** - Ícones
- **Formulários HTML tradicionais** (sem JavaScript para CRUD)

### Banco de Dados
- **SQLite** (padrão, sem configuração adicional)
- **MySQL/MariaDB** (opcional)

## 📦 Requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)
- Git (opcional)
- MySQL/MariaDB (opcional, apenas se não usar SQLite)

## 🚀 Instalação

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/pyFlaskUserKit.git
cd pyFlaskUserKit
```

### 2. Crie um ambiente virtual (recomendado)

```bash
# Linux/macOS
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

## ⚙️ Configuração

### 1. Configure as variáveis de ambiente

Copie o arquivo de exemplo e edite conforme necessário:

```bash
cp env.example .env
```

Edite o arquivo `.env`:

```env
# Database Configuration
DATABASE_TYPE=sqlite

# SQLite Configuration (default)
SQLITE_DB_PATH=instance/app.db

# MySQL/MariaDB Configuration (only if DATABASE_TYPE=mysql)
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=your_mysql_user
MYSQL_PASSWORD=your_mysql_password
MYSQL_DATABASE=userkit_db

# Application Configuration
SECRET_KEY=seu-secret-key-seguro-aqui
FLASK_ENV=development
FLASK_DEBUG=True
```

**⚠️ IMPORTANTE:** Altere o `SECRET_KEY` em produção!

### 2. Opções de Banco de Dados

#### Opção A: SQLite (Padrão - Recomendado para desenvolvimento)

Não precisa de configuração adicional. O banco será criado automaticamente em `instance/app.db`.

```env
DATABASE_TYPE=sqlite
SQLITE_DB_PATH=instance/app.db
```

#### Opção B: MySQL/MariaDB (Produção)

1. Crie o banco de dados:

```sql
CREATE DATABASE userkit_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'userkit_user'@'localhost' IDENTIFIED BY 'sua_senha_segura';
GRANT ALL PRIVILEGES ON userkit_db.* TO 'userkit_user'@'localhost';
FLUSH PRIVILEGES;
```

2. Configure no `.env`:

```env
DATABASE_TYPE=mysql
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=userkit_user
MYSQL_PASSWORD=sua_senha_segura
MYSQL_DATABASE=userkit_db
```

## 🎬 Inicialização

### Passo 1: Inicializar o Banco de Dados

Execute o script de inicialização para criar as tabelas e grupos padrão:

```bash
python scripts/init_db.py
```

Este script irá:
- ✅ Criar as tabelas no banco de dados
- ✅ Criar os grupos padrão (Administradores, Visualizadores, Editores)

**Saída esperada:**
```
============================================================
  pyFlaskUserKit - Inicialização do Banco de Dados
============================================================

1. Verificando conexão com o banco de dados...
   Tipo de banco: SQLITE
   Caminho: instance/app.db

2. Criando tabelas no banco de dados...
   ✓ Tabelas criadas com sucesso

3. Criando grupos padrão...
   ✓ Grupo 'Administradores' criado
   ✓ Grupo 'Visualizadores' criado
   ✓ Grupo 'Editores' criado

============================================================
  ✓ Banco de dados inicializado com sucesso!
============================================================
```

### Passo 2: Criar Usuário Administrador

Execute o script interativo para criar o primeiro usuário administrador:

```bash
python scripts/create_admin.py
```

O script solicitará:
- **Nome de usuário** (ex: admin)
- **Email** (ex: admin@example.com)
- **Senha** (mínimo 6 caracteres, será solicitada confirmação)

**Exemplo de execução:**
```
============================================================
  pyFlaskUserKit - Criação do Usuário Administrador
============================================================

Verificando usuários administradores existentes...

============================================================
  Dados do Novo Administrador
============================================================

Nome de usuário: admin
Email: admin@example.com
Senha (mínimo 6 caracteres): ********
Confirme a senha: ********

------------------------------------------------------------
Criando usuário administrador...
✓ Adicionado ao grupo 'Administradores'
✓ Usuário 'admin' criado com sucesso!

============================================================
  ✓ Administrador criado com sucesso!
============================================================

Próximos passos:
  1. Inicie o servidor: python run.py
  2. Acesse: http://localhost:5000/login
  3. Faça login com: admin
```

**⚠️ IMPORTANTE:** 
- As senhas NÃO aparecem no terminal durante a digitação (segurança)
- Não há credenciais hardcoded no código
- Você pode criar múltiplos administradores executando o script novamente

### Passo 3: Iniciar o Servidor

```bash
python run.py
```

A aplicação estará disponível em: **http://localhost:5000**

## 🎮 Uso

### Acessar a interface web

Abra seu navegador e acesse:

- **Login:** http://localhost:5000/login
- **Dashboard:** http://localhost:5000
- **Gerenciar Usuários:** http://localhost:5000/usuarios (admin only)
- **Ver Usuário por ID:** http://localhost:5000/usuarios/1 (admin only)
- **Gerenciar Grupos:** http://localhost:5000/grupos
- **Ver Grupo por ID:** http://localhost:5000/grupos/1
- **Documentação da API:** http://localhost:5000/documentacao (público)

### Fazer Login

Use as credenciais criadas no Passo 2:

- **URL:** http://localhost:5000/login
- **Username:** (o que você definiu no script)
- **Password:** (o que você definiu no script)

## 🔌 API REST

### ⚠️ Importante: Apenas Administradores

**Todas as rotas da API requerem:**
1. Estar autenticado (fazer login primeiro)
2. Ter privilégios de administrador

**Respostas de erro:**
- `401 Unauthorized` - Não autenticado (precisa fazer login)
- `403 Forbidden` - Não tem privilégios de administrador

### Base URL

```
http://localhost:5000/api
```

### Autenticação

A API usa sessões baseadas em cookies. Você precisa fazer login primeiro:

```bash
# Fazer login e salvar cookies
curl -X POST http://localhost:5000/login \
  -d "username=admin&password=sua_senha" \
  -c cookies.txt

# Usar cookies nas requisições subsequentes
curl http://localhost:5000/api/users \
  -b cookies.txt
```

### Endpoints Principais

#### Usuários

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/api/users` | Listar todos os usuários |
| GET | `/api/users/{id}` | Obter usuário específico |
| POST | `/api/users` | Criar novo usuário |
| PUT | `/api/users/{id}` | Atualizar usuário |
| DELETE | `/api/users/{id}` | Deletar usuário |
| POST | `/api/users/{id}/activate` | Ativar usuário |
| POST | `/api/users/{id}/deactivate` | Inativar usuário |
| POST | `/api/users/{id}/make-admin` | Tornar administrador |
| POST | `/api/users/{id}/remove-admin` | Remover privilégios admin |
| POST | `/api/users/{id}/reset-password` | Resetar senha |
| POST | `/api/users/{id}/groups` | Adicionar a grupos |
| DELETE | `/api/users/{id}/groups/{group_id}` | Remover de grupo |

#### Grupos

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/api/groups` | Listar todos os grupos |
| GET | `/api/groups/{id}` | Obter grupo específico |
| POST | `/api/groups` | Criar novo grupo |
| PUT | `/api/groups/{id}` | Atualizar grupo |
| DELETE | `/api/groups/{id}` | Deletar grupo |
| GET | `/api/groups/{id}/users` | Listar usuários do grupo |

## 💻 Exemplos de Código

### Python (usando requests)

#### Autenticação e Listar Usuários

```python
import requests

# Criar sessão para manter cookies
session = requests.Session()

# Fazer login
login_data = {
    'username': 'admin',
    'password': 'sua_senha'
}
response = session.post('http://localhost:5000/login', data=login_data)

if response.status_code == 200:
    print("✓ Login bem-sucedido!")
    
    # Listar usuários (requer admin)
    users = session.get('http://localhost:5000/api/users')
    
    if users.status_code == 200:
        for user in users.json():
            print(f"ID: {user['id']}, Username: {user['username']}, Email: {user['email']}")
    elif users.status_code == 403:
        print("✗ Acesso negado: privilégios de administrador necessários")
else:
    print("✗ Falha no login")
```

#### Criar Novo Usuário

```python
new_user = {
    "username": "joao",
    "email": "joao@example.com",
    "password": "senha123",
    "is_admin": False,
    "is_active": True,
    "group_ids": [1, 2]  # IDs dos grupos
}

response = session.post('http://localhost:5000/api/users', json=new_user)

if response.status_code == 201:
    user = response.json()
    print(f"✓ Usuário criado: {user['username']}")
elif response.status_code == 409:
    print("✗ Erro: Username ou email já existe")
else:
    print(f"✗ Erro: {response.json()}")
```

#### Atualizar Usuário

```python
user_id = 1
updates = {
    "username": "joao_atualizado",
    "email": "joao.novo@example.com",
    "is_active": True
}

response = session.put(f'http://localhost:5000/api/users/{user_id}', json=updates)

if response.status_code == 200:
    print("✓ Usuário atualizado com sucesso")
```

#### Ver Usuário Específico por ID

```python
user_id = 1
response = session.get(f'http://localhost:5000/api/users/{user_id}')

if response.status_code == 200:
    user = response.json()
    print(f"Username: {user['username']}")
    print(f"Email: {user['email']}")
    print(f"Admin: {user['is_admin']}")
    print(f"Ativo: {user['is_active']}")
```

### cURL

#### Autenticação

```bash
# Fazer login e salvar cookies
curl -X POST http://localhost:5000/login \
  -d "username=admin&password=sua_senha" \
  -c cookies.txt

# Verificar se login foi bem-sucedido
echo "✓ Login realizado"
```

#### Listar Usuários

```bash
curl http://localhost:5000/api/users \
  -b cookies.txt \
  | python -m json.tool
```

#### Ver Usuário por ID

```bash
curl http://localhost:5000/api/users/1 \
  -b cookies.txt \
  | python -m json.tool
```

#### Criar Usuário

```bash
curl -X POST http://localhost:5000/api/users \
  -b cookies.txt \
  -H "Content-Type: application/json" \
  -d '{
    "username": "maria",
    "email": "maria@example.com",
    "password": "senha456",
    "is_admin": false,
    "is_active": true,
    "group_ids": [2]
  }'
```

#### Atualizar Usuário

```bash
curl -X PUT http://localhost:5000/api/users/2 \
  -b cookies.txt \
  -H "Content-Type: application/json" \
  -d '{
    "email": "maria.novo@example.com",
    "is_active": true
  }'
```

#### Deletar Usuário

```bash
curl -X DELETE http://localhost:5000/api/users/2 \
  -b cookies.txt
```

#### Adicionar Usuário a Grupos

```bash
curl -X POST http://localhost:5000/api/users/1/groups \
  -b cookies.txt \
  -H "Content-Type: application/json" \
  -d '{"group_ids": [1, 2, 3]}'
```

### PHP

#### Autenticação e Listar Usuários

```php
<?php
// Inicializar cURL com gerenciamento de cookies
$cookieFile = tempnam(sys_get_temp_dir(), 'cookie');

// Fazer login
$ch = curl_init('http://localhost:5000/login');
curl_setopt($ch, CURLOPT_POST, true);
curl_setopt($ch, CURLOPT_POSTFIELDS, [
    'username' => 'admin',
    'password' => 'sua_senha'
]);
curl_setopt($ch, CURLOPT_COOKIEJAR, $cookieFile);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
$response = curl_exec($ch);
curl_close($ch);

echo "✓ Login realizado\n";

// Listar usuários
$ch = curl_init('http://localhost:5000/api/users');
curl_setopt($ch, CURLOPT_COOKIEFILE, $cookieFile);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
$response = curl_exec($ch);
$httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
curl_close($ch);

if ($httpCode == 200) {
    $users = json_decode($response, true);
    foreach ($users as $user) {
        echo "ID: {$user['id']}, Username: {$user['username']}\n";
    }
} elseif ($httpCode == 403) {
    echo "✗ Acesso negado: privilégios de administrador necessários\n";
}
?>
```

#### Criar Usuário

```php
<?php
$newUser = [
    'username' => 'pedro',
    'email' => 'pedro@example.com',
    'password' => 'senha789',
    'is_admin' => false,
    'is_active' => true,
    'group_ids' => [2, 3]
];

$ch = curl_init('http://localhost:5000/api/users');
curl_setopt($ch, CURLOPT_POST, true);
curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($newUser));
curl_setopt($ch, CURLOPT_HTTPHEADER, ['Content-Type: application/json']);
curl_setopt($ch, CURLOPT_COOKIEFILE, $cookieFile);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
$response = curl_exec($ch);
$httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
curl_close($ch);

if ($httpCode == 201) {
    echo "✓ Usuário criado com sucesso\n";
    $user = json_decode($response, true);
    print_r($user);
}
?>
```

### Node.js (usando axios)

#### Instalação de Dependências

```bash
npm install axios axios-cookiejar-support tough-cookie
```

#### Autenticação e Listar Usuários

```javascript
const axios = require('axios');
const wrapper = require('axios-cookiejar-support').wrapper;
const tough = require('tough-cookie');

// Criar cliente com suporte a cookies
const cookieJar = new tough.CookieJar();
const client = wrapper(axios.create({ jar: cookieJar }));

async function main() {
    try {
        // Fazer login
        await client.post('http://localhost:5000/login', 
            'username=admin&password=sua_senha',
            {
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
            }
        );
        console.log('✓ Login bem-sucedido!');
        
        // Listar usuários
        const response = await client.get('http://localhost:5000/api/users');
        
        if (response.status === 200) {
            response.data.forEach(user => {
                console.log(`ID: ${user.id}, Username: ${user.username}, Email: ${user.email}`);
            });
        }
    } catch (error) {
        if (error.response?.status === 403) {
            console.error('✗ Acesso negado: privilégios de administrador necessários');
        } else {
            console.error('✗ Erro:', error.message);
        }
    }
}

main();
```

#### Criar Usuário

```javascript
async function createUser() {
    const newUser = {
        username: 'carlos',
        email: 'carlos@example.com',
        password: 'senha999',
        is_admin: false,
        is_active: true,
        group_ids: [1, 3]
    };
    
    try {
        const response = await client.post('http://localhost:5000/api/users', newUser);
        
        if (response.status === 201) {
            console.log('✓ Usuário criado:', response.data);
        }
    } catch (error) {
        if (error.response?.status === 409) {
            console.error('✗ Erro: Username ou email já existe');
        } else {
            console.error('✗ Erro:', error.response?.data || error.message);
        }
    }
}
```

#### Ver Usuário por ID

```javascript
async function getUser(userId) {
    try {
        const response = await client.get(`http://localhost:5000/api/users/${userId}`);
        console.log('Usuário:', response.data);
    } catch (error) {
        if (error.response?.status === 404) {
            console.error('✗ Usuário não encontrado');
        }
    }
}

// Exemplo de uso
getUser(1);
```

## 📁 Estrutura do Projeto

```
pyFlaskUserKit/
├── app/
│   ├── __init__.py              # Factory da aplicação Flask
│   ├── models.py                # Modelos SQLAlchemy (User, Group)
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── api.py               # Rotas da API REST (protegidas)
│   │   └── web.py               # Rotas da interface web
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css        # Estilos personalizados + temas
│   │   └── js/
│   │       └── main.js          # JavaScript mínimo (tema toggle)
│   └── templates/
│       ├── base.html            # Template base
│       ├── login.html           # Página de login
│       ├── index.html           # Dashboard
│       ├── users_list.html      # Lista de usuários
│       ├── user_detail.html     # Detalhes do usuário
│       ├── user_form.html       # Form criar/editar usuário
│       ├── groups_list.html     # Lista de grupos
│       ├── group_detail.html    # Detalhes do grupo
│       ├── group_form.html      # Form criar/editar grupo
│       └── docs.html            # Documentação da API (pública)
├── scripts/
│   ├── init_db.py               # Script de inicialização do banco
│   └── create_admin.py          # Script para criar admin (interativo)
├── instance/                    # Banco SQLite (criado automaticamente)
│   └── app.db
├── config.py                    # Configurações da aplicação
├── run.py                       # Script para iniciar o servidor
├── requirements.txt             # Dependências Python
├── env.example                  # Exemplo de arquivo .env (SEM credenciais)
├── .gitignore                   # Arquivos ignorados pelo Git
├── LICENSE                      # Licença MIT
└── README.md                    # Este arquivo
```

## 🎨 Grupos Padrão

O sistema cria automaticamente 3 grupos:

### 1. Administradores
- Usuários com privilégios totais no sistema
- Podem gerenciar todos os usuários e grupos
- Únicos que podem acessar a API

### 2. Visualizadores
- Usuários com permissão apenas para visualização
- Podem ver grupos e seus membros

### 3. Editores
- Usuários com permissão para edição de conteúdo
- Podem ver e interagir com grupos

Você pode criar grupos adicionais conforme necessário.

## 🔒 Segurança

### ✅ Já Implementado
- Senhas armazenadas com hash (Werkzeug/PBKDF2)
- SECRET_KEY configurável via variável de ambiente
- Sem credenciais hardcoded no código
- Script interativo para criar admin
- Validação de dados em todas as rotas
- Tratamento de erros adequado
- Proteção contra SQL Injection (SQLAlchemy ORM)
- Autenticação baseada em sessões
- Autorização granular (admin vs regular)
- API 100% protegida (apenas admin)

### ⚠️ Para Produção
- Altere o SECRET_KEY para um valor forte e único
- Use MySQL/PostgreSQL ao invés de SQLite
- Configure HTTPS/SSL
- Adicione rate limiting
- Implemente CSRF protection adicional
- Configure logs de auditoria
- Use um servidor WSGI (Gunicorn, uWSGI)
- Configure um proxy reverso (Nginx, Apache)

## 🚀 Deploy em Produção

### Considerações importantes:

1. **Altere o SECRET_KEY**
2. **Use um banco de dados robusto** (MySQL/PostgreSQL)
3. **Configure FLASK_ENV=production**
4. **Use um servidor WSGI** (Gunicorn, uWSGI)
5. **Configure um proxy reverso** (Nginx, Apache)
6. **Implemente HTTPS**
7. **Configure backups regulares**

### Exemplo com Gunicorn:

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 run:app
```

## 📝 Códigos de Resposta HTTP

| Código | Descrição | Quando Ocorre |
|--------|-----------|---------------|
| 200 | OK | Requisição bem-sucedida (GET, PUT, DELETE) |
| 201 | Created | Recurso criado com sucesso (POST) |
| 400 | Bad Request | Dados inválidos ou faltantes |
| 401 | Unauthorized | Não autenticado (sem login) |
| 403 | Forbidden | Sem permissões de administrador |
| 404 | Not Found | Recurso não encontrado |
| 409 | Conflict | Username ou email já existe |
| 500 | Internal Server Error | Erro interno do servidor |

## 📚 Documentação da API

Para documentação completa e interativa da API, acesse:

**http://localhost:5000/documentacao** (página pública)

A documentação inclui:
- ✅ Introdução e autenticação
- ✅ Todos os endpoints documentados
- ✅ Exemplos em 4 linguagens (Python, cURL, PHP, Node.js)
- ✅ Parâmetros obrigatórios e opcionais
- ✅ Códigos de resposta HTTP
- ✅ Boas práticas de segurança

## 🆘 Troubleshooting

### Erro: ModuleNotFoundError
```bash
# Ative o ambiente virtual
source venv/bin/activate  # Linux/macOS
# ou
venv\Scripts\activate  # Windows

# Instale as dependências
pip install -r requirements.txt
```

### Erro: Address already in use
```bash
# Mate o processo na porta 5000
lsof -i :5000  # Linux/macOS
kill -9 <PID>

# Ou use outra porta editando run.py
```

### Banco de dados vazio ou corrompido
```bash
# Remova o banco e recrie
rm -rf instance/
python scripts/init_db.py
python scripts/create_admin.py
```

### Erro 401 ao acessar API
- Você precisa fazer login primeiro
- Use cookies/sessões para manter a autenticação

### Erro 403 ao acessar API
- Apenas administradores podem acessar a API
- Verifique se seu usuário tem `is_admin=True`

## 🤝 Contribuindo

Contribuições são bem-vindas! Sinta-se livre para:

1. Fazer um Fork do projeto
2. Criar uma branch para sua feature (`git checkout -b feature/NovaFeature`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/NovaFeature`)
5. Abrir um Pull Request

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 👨‍💻 Autor

Desenvolvido com ❤️ usando Python e Flask

## 📞 Suporte

Se você encontrar algum problema ou tiver dúvidas:

1. Verifique a [documentação integrada](http://localhost:5000/documentacao)
2. Revise este README
3. Abra uma issue no GitHub

---

**Desenvolvido com Python 🐍 e Flask ⚡**

**Sem JavaScript para CRUD | 100% Server-Side | API Protegida | Sem Credenciais no Código**
