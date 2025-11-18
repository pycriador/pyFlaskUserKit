#!/usr/bin/env python3
"""
Database initialization script for pyFlaskUserKit
This script initializes the database and creates default groups.
Run create_admin.py separately to create the admin user.
"""

import os
import sys

# Add parent directory to path to import app modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.models import Group
from config import Config


def create_default_groups():
    """Create default groups if they don't exist"""
    default_groups = [
        {
            'name': 'Administradores',
            'description': 'Grupo de administradores do sistema com privilégios totais'
        },
        {
            'name': 'Visualizadores',
            'description': 'Grupo de usuários com permissão apenas para visualização'
        },
        {
            'name': 'Editores',
            'description': 'Grupo de usuários com permissão para edição de conteúdo'
        }
    ]
    
    created_groups = []
    
    for group_data in default_groups:
        existing_group = Group.query.filter_by(name=group_data['name']).first()
        
        if not existing_group:
            group = Group(
                name=group_data['name'],
                description=group_data['description']
            )
            db.session.add(group)
            created_groups.append(group_data['name'])
            print(f"   ✓ Grupo '{group_data['name']}' criado")
        else:
            print(f"   → Grupo '{group_data['name']}' já existe")
    
    db.session.commit()
    return created_groups


def check_database_connection():
    """Check if database connection is working"""
    try:
        # Try to query the database
        db.session.execute('SELECT 1')
        return True
    except Exception as e:
        print(f"✗ Erro ao conectar ao banco de dados: {e}")
        return False


def main():
    """Main initialization function"""
    print("=" * 60)
    print("  pyFlaskUserKit - Inicialização do Banco de Dados")
    print("=" * 60)
    
    # Create Flask app
    app = create_app()
    
    with app.app_context():
        print("\n1. Verificando conexão com o banco de dados...")
        
        database_type = Config.DATABASE_TYPE
        print(f"   Tipo de banco: {database_type.upper()}")
        
        if database_type == 'sqlite':
            db_path = Config.SQLITE_DB_PATH
            print(f"   Caminho: {db_path}")
            
            # Create instance directory if it doesn't exist
            instance_dir = os.path.dirname(db_path)
            if instance_dir and not os.path.exists(instance_dir):
                os.makedirs(instance_dir)
                print(f"   ✓ Diretório '{instance_dir}' criado")
        else:
            print(f"   Host: {Config.MYSQL_HOST}:{Config.MYSQL_PORT}")
            print(f"   Database: {Config.MYSQL_DATABASE}")
        
        print("\n2. Criando tabelas no banco de dados...")
        try:
            db.create_all()
            print("   ✓ Tabelas criadas com sucesso")
        except Exception as e:
            print(f"   ✗ Erro ao criar tabelas: {e}")
            return
        
        print("\n3. Criando grupos padrão...")
        create_default_groups()
        
        print("\n" + "=" * 60)
        print("  ✓ Banco de dados inicializado com sucesso!")
        print("=" * 60)
        print("\nPróximos passos:")
        print("  1. Crie o usuário administrador:")
        print("     python scripts/create_admin.py")
        print()
        print("  2. Inicie o servidor:")
        print("     python run.py")
        print()
        print("  3. Acesse:")
        print("     http://localhost:5000/login")
        print("\n" + "=" * 60)


if __name__ == '__main__':
    main()


