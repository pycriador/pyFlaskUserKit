import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

db = SQLAlchemy()
migrate = Migrate()


def create_app(config_class=Config):
    """Application factory pattern"""
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Ensure instance directory exists for SQLite
    if config_class.DATABASE_TYPE == 'sqlite':
        db_path = config_class.SQLITE_DB_PATH
        db_dir = os.path.dirname(db_path)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir, exist_ok=True)
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Register blueprints
    from app.routes.web import web_bp
    from app.routes.api import api_bp
    
    app.register_blueprint(web_bp)
    app.register_blueprint(api_bp, url_prefix='/api')
    
    # Create tables and default groups
    with app.app_context():
        db.create_all()
        from app.models import Group
        
        # Create default groups if they don't exist
        default_groups = ['Administradores', 'Visualizadores', 'Editores']
        for group_name in default_groups:
            if not Group.query.filter_by(name=group_name).first():
                group = Group(name=group_name, description=f'Grupo de {group_name}')
                db.session.add(group)
        
        db.session.commit()
    
    return app


