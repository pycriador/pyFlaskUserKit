from functools import wraps
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app import db
from app.models import User, Group

web_bp = Blueprint('web', __name__)


# Authentication decorator
def login_required(f):
    """Decorator to require login for routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Você precisa fazer login para acessar esta página.', 'warning')
            return redirect(url_for('web.login'))
        return f(*args, **kwargs)
    return decorated_function


# Admin decorator
def admin_required(f):
    """Decorator to require admin privileges"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Você precisa fazer login para acessar esta página.', 'warning')
            return redirect(url_for('web.login'))
        if not session.get('is_admin', False):
            flash('Você não tem permissão para acessar esta página.', 'danger')
            return redirect(url_for('web.index'))
        return f(*args, **kwargs)
    return decorated_function


# ============= AUTHENTICATION ROUTES =============

@web_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Login page"""
    if 'user_id' in session:
        return redirect(url_for('web.index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            if not user.is_active:
                flash('Usuário inativo. Contate o administrador.', 'danger')
                return redirect(url_for('web.login'))
            
            session['user_id'] = user.id
            session['username'] = user.username
            session['is_admin'] = user.is_admin
            
            flash(f'Bem-vindo, {user.username}!', 'success')
            return redirect(url_for('web.index'))
        else:
            flash('Usuário ou senha incorretos.', 'danger')
            return redirect(url_for('web.login'))
    
    return render_template('login.html')


@web_bp.route('/logout')
def logout():
    """Logout"""
    session.clear()
    flash('Você saiu do sistema.', 'info')
    return redirect(url_for('web.login'))


@web_bp.route('/')
@login_required
def index():
    """Home page"""
    user_count = User.query.count()
    group_count = Group.query.count()
    active_users = User.query.filter_by(is_active=True).count()
    admin_count = User.query.filter_by(is_admin=True).count()
    
    return render_template('index.html', 
                         user_count=user_count,
                         group_count=group_count,
                         active_users=active_users,
                         admin_count=admin_count)


# ============= USER ROUTES =============

@web_bp.route('/usuarios')
@admin_required
def users_list():
    """List all users - Admin only"""
    users = User.query.order_by(User.id).all()
    return render_template('users_list.html', users=users)


@web_bp.route('/usuarios/<int:user_id>')
@admin_required
def user_detail(user_id):
    """View user details - Admin only"""
    user = User.query.get_or_404(user_id)
    return render_template('user_detail.html', user=user)


@web_bp.route('/usuarios/novo', methods=['GET', 'POST'])
@admin_required
def user_create():
    """Create new user - Admin only"""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password')
        is_admin = request.form.get('is_admin') == 'on'
        is_active = request.form.get('is_active') == 'on'
        group_ids = request.form.getlist('groups')
        
        # Validation
        if not username or not email or not password:
            flash('Todos os campos obrigatórios devem ser preenchidos.', 'danger')
            return redirect(url_for('web.user_create'))
        
        # Check if username or email already exists
        if User.query.filter_by(username=username).first():
            flash('Nome de usuário já existe.', 'danger')
            return redirect(url_for('web.user_create'))
        
        if User.query.filter_by(email=email).first():
            flash('Email já existe.', 'danger')
            return redirect(url_for('web.user_create'))
        
        # Create user
        user = User(
            username=username,
            email=email,
            is_admin=is_admin,
            is_active=is_active
        )
        user.set_password(password)
        
        # Add groups
        if group_ids:
            groups = Group.query.filter(Group.id.in_(group_ids)).all()
            user.groups = groups
        
        db.session.add(user)
        db.session.commit()
        
        flash(f'Usuário {username} criado com sucesso!', 'success')
        return redirect(url_for('web.users_list'))
    
    groups = Group.query.order_by(Group.name).all()
    return render_template('user_form.html', groups=groups, user=None)


@web_bp.route('/usuarios/<int:user_id>/editar', methods=['GET', 'POST'])
@admin_required
def user_edit(user_id):
    """Edit user - Admin only"""
    user = User.query.get_or_404(user_id)
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        is_admin = request.form.get('is_admin') == 'on'
        is_active = request.form.get('is_active') == 'on'
        group_ids = request.form.getlist('groups')
        
        # Validation
        if not username or not email:
            flash('Nome de usuário e email são obrigatórios.', 'danger')
            return redirect(url_for('web.user_edit', user_id=user_id))
        
        # Check if username already exists (except for this user)
        existing = User.query.filter(User.username == username, User.id != user_id).first()
        if existing:
            flash('Nome de usuário já existe.', 'danger')
            return redirect(url_for('web.user_edit', user_id=user_id))
        
        # Check if email already exists (except for this user)
        existing = User.query.filter(User.email == email, User.id != user_id).first()
        if existing:
            flash('Email já existe.', 'danger')
            return redirect(url_for('web.user_edit', user_id=user_id))
        
        # Update user
        user.username = username
        user.email = email
        user.is_admin = is_admin
        user.is_active = is_active
        
        # Update password if provided
        if password:
            user.set_password(password)
        
        # Update groups
        if group_ids:
            groups = Group.query.filter(Group.id.in_(group_ids)).all()
            user.groups = groups
        else:
            user.groups = []
        
        db.session.commit()
        
        flash(f'Usuário {username} atualizado com sucesso!', 'success')
        return redirect(url_for('web.user_detail', user_id=user_id))
    
    groups = Group.query.order_by(Group.name).all()
    return render_template('user_form.html', groups=groups, user=user)


@web_bp.route('/usuarios/<int:user_id>/deletar', methods=['POST'])
@admin_required
def user_delete(user_id):
    """Delete user - Admin only"""
    user = User.query.get_or_404(user_id)
    
    # Prevent deleting yourself
    if user.id == session.get('user_id'):
        flash('Você não pode deletar seu próprio usuário.', 'danger')
        return redirect(url_for('web.users_list'))
    
    username = user.username
    db.session.delete(user)
    db.session.commit()
    
    flash(f'Usuário {username} deletado com sucesso!', 'success')
    return redirect(url_for('web.users_list'))


@web_bp.route('/usuarios/<int:user_id>/alternar-status', methods=['POST'])
@admin_required
def user_toggle_status(user_id):
    """Toggle user active status - Admin only"""
    user = User.query.get_or_404(user_id)
    
    user.is_active = not user.is_active
    db.session.commit()
    
    status = 'ativado' if user.is_active else 'inativado'
    flash(f'Usuário {user.username} {status} com sucesso!', 'success')
    return redirect(url_for('web.user_detail', user_id=user_id))


@web_bp.route('/usuarios/<int:user_id>/alternar-admin', methods=['POST'])
@admin_required
def user_toggle_admin(user_id):
    """Toggle user admin status - Admin only"""
    user = User.query.get_or_404(user_id)
    
    user.is_admin = not user.is_admin
    db.session.commit()
    
    status = 'promovido a administrador' if user.is_admin else 'removido de administrador'
    flash(f'Usuário {user.username} {status} com sucesso!', 'success')
    return redirect(url_for('web.user_detail', user_id=user_id))


# ============= GROUP ROUTES =============

@web_bp.route('/grupos')
@login_required
def groups_list():
    """List all groups"""
    groups = Group.query.order_by(Group.name).all()
    return render_template('groups_list.html', groups=groups)


@web_bp.route('/grupos/<int:group_id>')
@login_required
def group_detail(group_id):
    """View group details"""
    group = Group.query.get_or_404(group_id)
    all_users = User.query.order_by(User.username).all() if session.get('is_admin') else []
    return render_template('group_detail.html', group=group, all_users=all_users)


@web_bp.route('/grupos/novo', methods=['GET', 'POST'])
@admin_required
def group_create():
    """Create new group - Admin only"""
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        description = request.form.get('description', '').strip()
        
        if not name:
            flash('Nome do grupo é obrigatório.', 'danger')
            return redirect(url_for('web.group_create'))
        
        # Check if group already exists
        if Group.query.filter_by(name=name).first():
            flash('Grupo já existe.', 'danger')
            return redirect(url_for('web.group_create'))
        
        # Create group
        group = Group(name=name, description=description)
        db.session.add(group)
        db.session.commit()
        
        flash(f'Grupo {name} criado com sucesso!', 'success')
        return redirect(url_for('web.groups_list'))
    
    return render_template('group_form.html', group=None)


@web_bp.route('/grupos/<int:group_id>/editar', methods=['GET', 'POST'])
@admin_required
def group_edit(group_id):
    """Edit group - Admin only"""
    group = Group.query.get_or_404(group_id)
    
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        description = request.form.get('description', '').strip()
        
        if not name:
            flash('Nome do grupo é obrigatório.', 'danger')
            return redirect(url_for('web.group_edit', group_id=group_id))
        
        # Check if name already exists (except for this group)
        existing = Group.query.filter(Group.name == name, Group.id != group_id).first()
        if existing:
            flash('Nome do grupo já existe.', 'danger')
            return redirect(url_for('web.group_edit', group_id=group_id))
        
        # Update group
        group.name = name
        group.description = description
        db.session.commit()
        
        flash(f'Grupo {name} atualizado com sucesso!', 'success')
        return redirect(url_for('web.group_detail', group_id=group_id))
    
    return render_template('group_form.html', group=group)


@web_bp.route('/grupos/<int:group_id>/deletar', methods=['POST'])
@admin_required
def group_delete(group_id):
    """Delete group - Admin only"""
    group = Group.query.get_or_404(group_id)
    
    name = group.name
    db.session.delete(group)
    db.session.commit()
    
    flash(f'Grupo {name} deletado com sucesso!', 'success')
    return redirect(url_for('web.groups_list'))


@web_bp.route('/grupos/<int:group_id>/adicionar-usuario/<int:user_id>', methods=['POST'])
@admin_required
def group_add_user(group_id, user_id):
    """Add user to group - Admin only"""
    group = Group.query.get_or_404(group_id)
    user = User.query.get_or_404(user_id)
    
    if user not in group.users:
        group.users.append(user)
        db.session.commit()
        flash(f'Usuário {user.username} adicionado ao grupo {group.name}!', 'success')
    else:
        flash(f'Usuário {user.username} já está no grupo {group.name}.', 'info')
    
    return redirect(url_for('web.group_detail', group_id=group_id))


@web_bp.route('/grupos/<int:group_id>/remover-usuario/<int:user_id>', methods=['POST'])
@admin_required
def group_remove_user(group_id, user_id):
    """Remove user from group - Admin only"""
    group = Group.query.get_or_404(group_id)
    user = User.query.get_or_404(user_id)
    
    if user in group.users:
        group.users.remove(user)
        db.session.commit()
        flash(f'Usuário {user.username} removido do grupo {group.name}!', 'success')
    else:
        flash(f'Usuário {user.username} não está no grupo {group.name}.', 'info')
    
    return redirect(url_for('web.group_detail', group_id=group_id))


# ============= DOCUMENTATION =============

@web_bp.route('/documentacao')
def documentation():
    """API documentation page - Public"""
    return render_template('docs.html')
