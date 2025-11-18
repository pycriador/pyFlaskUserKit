# 🚀 Guia de Início Rápido - pyFlaskUserKit

Este guia vai te ajudar a colocar o sistema no ar em **menos de 5 minutos**!

## 📋 Pré-requisitos

- Python 3.8+ instalado
- Terminal/Prompt de comando

## 🎯 Passos Rápidos

### 1. Navegue até o diretório do projeto

```bash
cd pyFlaskUserKit
```

### 2. Crie um ambiente virtual

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

### 4. Configure o ambiente

```bash
# Copie o arquivo de exemplo
cp env.example .env

# O arquivo .env já vem com configurações padrão para SQLite
# Você pode editá-lo depois se quiser usar MySQL
```

### 5. Inicialize o banco de dados

```bash
python scripts/init_db.py
```

Quando perguntado, pressione **Enter** para aceitar as configurações padrão do `.env`.

### 6. Inicie o servidor

```bash
python run.py
```

### 7. Acesse a aplicação

Abra seu navegador em: **http://localhost:5000**

**Credenciais padrão:**
- Username: `admin`
- Password: `admin123`

## ✅ Pronto!

Agora você pode:
- 👥 Gerenciar usuários em: http://localhost:5000/usuarios
- 📁 Gerenciar grupos em: http://localhost:5000/grupos
- 📖 Ver a documentação em: http://localhost:5000/documentacao

## 🎨 Recursos Principais

### Interface Web
- ✨ Clique no **ícone da lua/sol** no canto superior direito para alternar entre tema claro e escuro
- 🔍 Use a **busca** para filtrar usuários e grupos
- ➕ Clique em **"Adicionar Usuário"** ou **"Adicionar Grupo"** para criar novos

### API REST
Teste a API diretamente:

```bash
# Listar usuários
curl http://localhost:5000/api/users

# Listar grupos
curl http://localhost:5000/api/groups

# Criar novo usuário
curl -X POST http://localhost:5000/api/users \
  -H "Content-Type: application/json" \
  -d '{
    "username": "teste",
    "email": "teste@example.com",
    "password": "senha123"
  }'
```

## 🛑 Parar o servidor

Pressione `Ctrl + C` no terminal onde o servidor está rodando.

## 🔄 Reiniciar tudo do zero

Se quiser começar com um banco de dados limpo:

```bash
# Remova o banco de dados
rm -rf instance/

# Execute novamente o script de inicialização
python scripts/init_db.py

# Inicie o servidor
python run.py
```

## 🆘 Problemas?

### Erro: "ModuleNotFoundError"
Certifique-se de que ativou o ambiente virtual e instalou as dependências:
```bash
source venv/bin/activate  # Linux/macOS
pip install -r requirements.txt
```

### Erro: "Address already in use"
Outra aplicação está usando a porta 5000. Você pode:
1. Parar a outra aplicação
2. Ou mudar a porta no `run.py` (linha: `app.run(host='0.0.0.0', port=5000)`)

### Erro de banco de dados
Delete a pasta `instance/` e execute `python scripts/init_db.py` novamente.

## 📚 Próximos Passos

1. **Leia o [README.md](README.md)** para entender melhor o projeto
2. **Explore a [documentação](http://localhost:5000/documentacao)** da API
3. **Personalize** o `.env` com suas próprias configurações
4. **Altere** as credenciais padrão do administrador

## 🎓 Dicas

- 💡 Mantenha o terminal aberto para ver os logs da aplicação
- 💡 Use o tema escuro para desenvolvimento noturno 🌙
- 💡 Experimente os filtros na página de usuários
- 💡 Teste a API com Postman ou qualquer cliente HTTP

---

**Divirta-se! 🎉**


