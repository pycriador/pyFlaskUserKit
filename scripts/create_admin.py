#!/usr/bin/env python3
"""
Script to create the first admin user for pyFlaskUserKit
This script must be run AFTER initializing the database.
"""

import os
import sys
from getpass import getpass

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.models import User, Group


def create_admin_user():
    """Create admin user interactively"""
    print("=" * 60)
    print("  pyFlaskUserKit - Criação do Usuário Administrador")
    print("=" * 60)
    print()
    
    app = create_app()
    
    with app.app_context():
        # Check if admin already exists
        print("Verificando usuários administradores existentes...")
        existing_admins = User.query.filter_by(is_admin=True).all()
        
        if existing_admins:
            print(f"\n✓ Já existem {len(existing_admins)} administrador(es):")
            for admin in existing_admins:
                print(f"  - {admin.username} ({admin.email})")
            
            create_another = input("\nDeseja criar outro administrador? (s/n) [n]: ").lower()
            if create_another != 's':
                print("\nOperação cancelada.")
                return
        
        print("\n" + "=" * 60)
        print("  Dados do Novo Administrador")
        print("=" * 60)
        
        # Get username
        while True:
            username = input("\nNome de usuário: ").strip()
            if not username:
                print("❌ Nome de usuário não pode ser vazio!")
                continue
            
            # Check if username exists
            if User.query.filter_by(username=username).first():
                print(f"❌ Usuário '{username}' já existe!")
                continue
            
            break
        
        # Get email
        while True:
            email = input("Email: ").strip()
            if not email:
                print("❌ Email não pode ser vazio!")
                continue
            
            if '@' not in email:
                print("❌ Email inválido!")
                continue
            
            # Check if email exists
            if User.query.filter_by(email=email).first():
                print(f"❌ Email '{email}' já está em uso!")
                continue
            
            break
        
        # Get password
        while True:
            password = getpass("Senha (mínimo 6 caracteres): ")
            if not password:
                print("❌ Senha não pode ser vazia!")
                continue
            
            if len(password) < 6:
                print("❌ Senha deve ter no mínimo 6 caracteres!")
                continue
            
            password_confirm = getpass("Confirme a senha: ")
            if password != password_confirm:
                print("❌ Senhas não coincidem!")
                continue
            
            break
        
        # Create user
        print("\n" + "-" * 60)
        print("Criando usuário administrador...")
        
        admin_user = User(
            username=username,
            email=email,
            is_admin=True,
            is_active=True
        )
        admin_user.set_password(password)
        
        # Add to Administradores group if it exists
        admin_group = Group.query.filter_by(name='Administradores').first()
        if admin_group:
            admin_user.groups.append(admin_group)
            print(f"✓ Adicionado ao grupo 'Administradores'")
        
        db.session.add(admin_user)
        db.session.commit()
        
        print(f"✓ Usuário '{username}' criado com sucesso!")
        print("\n" + "=" * 60)
        print("  ✓ Administrador criado com sucesso!")
        print("=" * 60)
        print("\nCredenciais:")
        print(f"  Username: {username}")
        print(f"  Email: {email}")
        print(f"  Senha: {'*' * len(password)}")
        print("\n" + "=" * 60)
        print("\nPróximos passos:")
        print("  1. Inicie o servidor: python run.py")
        print("  2. Acesse: http://localhost:5000/login")
        print(f"  3. Faça login com: {username}")
        print("\n" + "=" * 60)


def main():
    try:
        create_admin_user()
    except KeyboardInterrupt:
        print("\n\nOperação cancelada pelo usuário.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()


