# ✅ Checklist de Inicialização - pyFlaskUserKit

Use este checklist para garantir que tudo está configurado corretamente.

## 📋 Antes de Começar

- [ ] Python 3.8+ instalado
  ```bash
  python3 --version
  ```

- [ ] pip instalado
  ```bash
  pip --version
  ```

## 🛠️ Configuração Inicial

### 1. Ambiente Virtual
- [ ] Ambiente virtual criado
  ```bash
  python3 -m venv venv
  ```

- [ ] Ambiente virtual ativado
  ```bash
  # Linux/macOS
  source venv/bin/activate
  
  # Windows
  venv\Scripts\activate
  ```
  **Dica:** Você verá `(venv)` no início do prompt quando ativado

### 2. Dependências
- [ ] Dependências instaladas
  ```bash
  pip install -r requirements.txt
  ```

- [ ] Verificar instalação
  ```bash
  pip list | grep Flask
  ```
  **Esperado:** Ver Flask, Flask-SQLAlchemy, Flask-Migrate

### 3. Configuração
- [ ] Arquivo `.env` criado
  ```bash
  cp env.example .env
  ```

- [ ] Variáveis editadas (opcional neste momento)
  - [ ] SECRET_KEY alterado
  - [ ] Credenciais do admin personalizadas
  - [ ] Tipo de banco de dados definido

### 4. Banco de Dados
- [ ] Script de inicialização executado
  ```bash
  python scripts/init_db.py
  ```

- [ ] Grupos padrão criados
  - [ ] Administradores
  - [ ] Visualizadores
  - [ ] Editores

- [ ] Usuário admin criado
  - [ ] Username definido
  - [ ] Email configurado
  - [ ] Senha definida

### 5. Teste Inicial
- [ ] Servidor iniciado sem erros
  ```bash
  python run.py
  ```
  **Esperado:** Ver mensagem "Running on http://0.0.0.0:5000"

- [ ] Página inicial acessível
  - [ ] Abrir: http://localhost:5000
  - [ ] Verificar se carrega corretamente

## 🧪 Testes Funcionais

### Interface Web
- [ ] Página inicial carrega
  - [ ] http://localhost:5000
  - [ ] Cards informativos visíveis
  - [ ] Menu de navegação funcional

- [ ] Tema claro/escuro funciona
  - [ ] Clicar no ícone da lua/sol
  - [ ] Verificar mudança de cores
  - [ ] Preferência salva após reload

- [ ] Página de usuários funciona
  - [ ] http://localhost:5000/usuarios
  - [ ] Lista de usuários carrega
  - [ ] Admin aparece na lista
  - [ ] Botão "Adicionar Usuário" visível

- [ ] Página de grupos funciona
  - [ ] http://localhost:5000/grupos
  - [ ] 3 grupos padrão aparecem
  - [ ] Contadores de usuários corretos
  - [ ] Botão "Adicionar Grupo" visível

- [ ] Página de documentação funciona
  - [ ] http://localhost:5000/documentacao
  - [ ] Endpoints documentados
  - [ ] Exemplos de código visíveis

### Operações CRUD - Usuários

#### Criar Usuário
- [ ] Via interface web
  - [ ] Clicar em "Adicionar Usuário"
  - [ ] Preencher formulário
  - [ ] Selecionar grupo(s)
  - [ ] Salvar com sucesso
  - [ ] Mensagem de sucesso aparece
  - [ ] Usuário aparece na lista

- [ ] Via API
  ```bash
  curl -X POST http://localhost:5000/api/users \
    -H "Content-Type: application/json" \
    -d '{"username":"teste","email":"teste@example.com","password":"123456"}'
  ```
  **Esperado:** Status 201, dados do usuário retornados

#### Listar Usuários
- [ ] Via interface web
  - [ ] Todos os usuários visíveis
  - [ ] Informações corretas (email, grupos, status)

- [ ] Via API
  ```bash
  curl http://localhost:5000/api/users
  ```
  **Esperado:** Array JSON com usuários

#### Editar Usuário
- [ ] Via interface web
  - [ ] Clicar no botão editar (lápis)
  - [ ] Modal abre com dados corretos
  - [ ] Alterar informações
  - [ ] Salvar
  - [ ] Mudanças refletidas na lista

- [ ] Via API
  ```bash
  curl -X PUT http://localhost:5000/api/users/1 \
    -H "Content-Type: application/json" \
    -d '{"username":"admin_editado"}'
  ```

#### Ações Especiais
- [ ] Inativar usuário (botão toggle)
- [ ] Ativar usuário (botão toggle)
- [ ] Tornar admin (botão shield)
- [ ] Remover admin (botão shield)
- [ ] Resetar senha (botão chave)
- [ ] Ver grupos do usuário

#### Deletar Usuário
- [ ] Via interface web
  - [ ] Clicar no botão deletar (lixeira)
  - [ ] Modal de confirmação aparece
  - [ ] Confirmar exclusão
  - [ ] Usuário removido da lista
  - [ ] Mensagem de sucesso

- [ ] Via API
  ```bash
  curl -X DELETE http://localhost:5000/api/users/2
  ```

### Operações CRUD - Grupos

#### Criar Grupo
- [ ] Via interface web
  - [ ] Clicar em "Adicionar Grupo"
  - [ ] Preencher nome e descrição
  - [ ] Salvar
  - [ ] Grupo aparece na lista

- [ ] Via API
  ```bash
  curl -X POST http://localhost:5000/api/groups \
    -H "Content-Type: application/json" \
    -d '{"name":"Desenvolvedores","description":"Equipe dev"}'
  ```

#### Listar Grupos
- [ ] Via interface web
  - [ ] Todos os grupos visíveis
  - [ ] Contador de membros correto

- [ ] Via API
  ```bash
  curl http://localhost:5000/api/groups
  ```

#### Ver Membros do Grupo
- [ ] Via interface web
  - [ ] Clicar no botão "X usuário(s)"
  - [ ] Modal abre com lista de membros
  - [ ] Informações corretas (nome, email, status)

- [ ] Via API
  ```bash
  curl http://localhost:5000/api/groups/1/users
  ```

#### Editar Grupo
- [ ] Via interface web
  - [ ] Clicar no botão editar
  - [ ] Alterar nome ou descrição
  - [ ] Salvar
  - [ ] Mudanças refletidas

#### Deletar Grupo
- [ ] Via interface web
  - [ ] Clicar no botão deletar
  - [ ] Confirmar
  - [ ] Grupo removido

### Busca e Filtros

#### Usuários
- [ ] Busca por nome funciona
- [ ] Busca por email funciona
- [ ] Filtro por status (ativo/inativo)
- [ ] Filtro por tipo (admin/regular)
- [ ] Combinação de filtros

#### Grupos
- [ ] Busca por nome funciona
- [ ] Busca por descrição funciona

## 🔒 Segurança

- [ ] Senha armazenada com hash
  - [ ] Verificar no banco: senha não está em texto plano
  
- [ ] `.env` não está no Git
  - [ ] Verificar `.gitignore`

- [ ] SECRET_KEY foi alterado
  - [ ] Não está usando valor padrão do env.example

## 📱 Responsividade

- [ ] Testar em desktop
  - [ ] Layout correto
  - [ ] Todos os botões visíveis
  - [ ] Modais funcionais

- [ ] Testar em mobile (ou DevTools)
  - [ ] Menu hamburguer funciona
  - [ ] Tabelas rolam horizontalmente
  - [ ] Botões acessíveis

## 🎨 Temas

- [ ] Tema claro
  - [ ] Fundo branco
  - [ ] Texto preto
  - [ ] Cores legíveis

- [ ] Tema escuro
  - [ ] Fundo escuro
  - [ ] Texto branco
  - [ ] Cores legíveis
  - [ ] Cards com fundo diferenciado

- [ ] Persistência
  - [ ] Tema salvo após reload
  - [ ] Funciona em abas diferentes

## 🚨 Tratamento de Erros

### Usuários
- [ ] Criar usuário com username duplicado
  - [ ] Mensagem de erro aparece
  - [ ] HTTP 409

- [ ] Criar usuário com email duplicado
  - [ ] Mensagem de erro aparece
  - [ ] HTTP 409

- [ ] Criar usuário sem campos obrigatórios
  - [ ] Mensagem de erro aparece
  - [ ] HTTP 400

- [ ] Buscar usuário inexistente
  - [ ] HTTP 404

### Grupos
- [ ] Criar grupo com nome duplicado
  - [ ] Mensagem de erro aparece
  - [ ] HTTP 409

- [ ] Criar grupo sem nome
  - [ ] Mensagem de erro aparece
  - [ ] HTTP 400

## 📊 Performance

- [ ] Página inicial carrega rápido (< 2s)
- [ ] Lista de usuários carrega rápido
- [ ] Lista de grupos carrega rápido
- [ ] Busca é responsiva (não trava)
- [ ] Modais abrem instantaneamente

## 🔧 Troubleshooting

### Problemas Comuns

#### "ModuleNotFoundError"
- [ ] Ambiente virtual ativado?
- [ ] Dependências instaladas?
  ```bash
  pip install -r requirements.txt
  ```

#### "Address already in use"
- [ ] Outra aplicação na porta 5000?
- [ ] Processo Flask ainda rodando?
  ```bash
  # Linux/macOS
  lsof -i :5000
  kill -9 <PID>
  ```

#### Banco de dados vazio
- [ ] Script de inicialização executado?
  ```bash
  python scripts/init_db.py
  ```

#### Página não carrega estilos
- [ ] Verificar console do navegador (F12)
- [ ] Arquivos CSS/JS estão na pasta static?
- [ ] Servidor Flask está rodando?

## ✅ Checklist de Produção

Antes de colocar em produção:

- [ ] Alterar SECRET_KEY
- [ ] Alterar credenciais do admin
- [ ] Configurar FLASK_ENV=production
- [ ] Configurar FLASK_DEBUG=False
- [ ] Usar MySQL/PostgreSQL ao invés de SQLite
- [ ] Configurar servidor WSGI (Gunicorn/uWSGI)
- [ ] Configurar proxy reverso (Nginx/Apache)
- [ ] Configurar HTTPS/SSL
- [ ] Configurar backup do banco
- [ ] Configurar logs
- [ ] Implementar rate limiting
- [ ] Adicionar autenticação JWT
- [ ] Implementar autorização baseada em roles

## 📝 Notas Finais

### Tudo funcionando? 🎉
Parabéns! Seu pyFlaskUserKit está configurado e pronto para uso!

### Problemas?
1. Revise este checklist
2. Consulte o [README.md](README.md)
3. Consulte o [QUICKSTART.md](QUICKSTART.md)
4. Verifique os logs do servidor

### Próximos Passos
- Explore a documentação da API
- Personalize o visual (CSS)
- Adicione suas próprias funcionalidades
- Integre com outros sistemas

---

**Boa sorte com seu projeto! 🚀**


