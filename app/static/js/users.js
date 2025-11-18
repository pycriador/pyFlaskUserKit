// ===== Users Page JavaScript =====

let allUsers = [];
let allGroups = [];

$(document).ready(function() {
    loadUsers();
    loadGroupsForSelects();
    
    // Search functionality
    $('#searchUser').on('input', debounce(filterUsers, 300));
    $('#filterStatus').on('change', filterUsers);
    $('#filterAdmin').on('change', filterUsers);
    
    // Add user
    $('#saveUserBtn').click(saveUser);
    
    // Update user
    $('#updateUserBtn').click(updateUser);
    
    // Reset password
    $('#resetPasswordBtn').click(resetPassword);
    
    // Delete user
    $('#confirmDeleteBtn').click(deleteUser);
    
    // Clear forms when modals close
    $('#addUserModal').on('hidden.bs.modal', function() {
        $('#addUserForm')[0].reset();
    });
    
    $('#editUserModal').on('hidden.bs.modal', function() {
        $('#editUserForm')[0].reset();
    });
    
    $('#resetPasswordModal').on('hidden.bs.modal', function() {
        $('#resetPasswordForm')[0].reset();
    });
});

// ===== Load Users =====
function loadUsers() {
    showLoading('loadingUsers');
    
    apiGet('/api/users')
        .done(function(data) {
            allUsers = data;
            renderUsers(data);
        })
        .fail(function(xhr) {
            showError('Erro ao carregar usuários: ' + (xhr.responseJSON?.error || 'Erro desconhecido'));
        })
        .always(function() {
            hideLoading('loadingUsers');
        });
}

// ===== Render Users =====
function renderUsers(users) {
    const tbody = $('#usersTableBody');
    tbody.empty();
    
    if (users.length === 0) {
        tbody.append('<tr><td colspan="7" class="text-center">Nenhum usuário encontrado</td></tr>');
        return;
    }
    
    users.forEach(function(user) {
        const statusBadge = user.is_active 
            ? '<span class="badge bg-success">Ativo</span>' 
            : '<span class="badge bg-danger">Inativo</span>';
        
        const adminBadge = user.is_admin
            ? '<span class="badge bg-primary">Admin</span>'
            : '<span class="badge bg-secondary">Regular</span>';
        
        const groups = user.groups.map(g => `<span class="badge bg-info me-1">${g.name}</span>`).join(' ');
        
        const row = `
            <tr>
                <td>${user.id}</td>
                <td><strong>${user.username}</strong></td>
                <td>${user.email}</td>
                <td>${groups || '<span class="text-muted">Nenhum</span>'}</td>
                <td>${statusBadge}</td>
                <td>${adminBadge}</td>
                <td>
                    <div class="btn-group btn-group-sm" role="group">
                        <button class="btn btn-outline-primary" onclick="openEditUserModal(${user.id})" title="Editar">
                            <i class="bi bi-pencil"></i>
                        </button>
                        <button class="btn btn-outline-warning" onclick="openResetPasswordModal(${user.id})" title="Resetar Senha">
                            <i class="bi bi-key"></i>
                        </button>
                        ${user.is_active 
                            ? `<button class="btn btn-outline-secondary" onclick="toggleUserStatus(${user.id}, false)" title="Inativar">
                                <i class="bi bi-toggle-off"></i>
                               </button>`
                            : `<button class="btn btn-outline-success" onclick="toggleUserStatus(${user.id}, true)" title="Ativar">
                                <i class="bi bi-toggle-on"></i>
                               </button>`
                        }
                        ${!user.is_admin
                            ? `<button class="btn btn-outline-info" onclick="toggleAdmin(${user.id}, true)" title="Tornar Admin">
                                <i class="bi bi-shield-fill-check"></i>
                               </button>`
                            : `<button class="btn btn-outline-dark" onclick="toggleAdmin(${user.id}, false)" title="Remover Admin">
                                <i class="bi bi-shield-fill-x"></i>
                               </button>`
                        }
                        <button class="btn btn-outline-danger" onclick="openDeleteUserModal(${user.id})" title="Deletar">
                            <i class="bi bi-trash"></i>
                        </button>
                    </div>
                </td>
            </tr>
        `;
        
        tbody.append(row);
    });
}

// ===== Filter Users =====
function filterUsers() {
    const searchTerm = $('#searchUser').val().toLowerCase();
    const statusFilter = $('#filterStatus').val();
    const adminFilter = $('#filterAdmin').val();
    
    let filtered = allUsers.filter(function(user) {
        // Search filter
        const matchesSearch = !searchTerm || 
            user.username.toLowerCase().includes(searchTerm) ||
            user.email.toLowerCase().includes(searchTerm);
        
        // Status filter
        const matchesStatus = !statusFilter ||
            (statusFilter === 'active' && user.is_active) ||
            (statusFilter === 'inactive' && !user.is_active);
        
        // Admin filter
        const matchesAdmin = !adminFilter ||
            (adminFilter === 'admin' && user.is_admin) ||
            (adminFilter === 'regular' && !user.is_admin);
        
        return matchesSearch && matchesStatus && matchesAdmin;
    });
    
    renderUsers(filtered);
}

// ===== Load Groups for Selects =====
function loadGroupsForSelects() {
    apiGet('/api/groups')
        .done(function(data) {
            allGroups = data;
            populateGroupSelects(data);
        })
        .fail(function(xhr) {
            showError('Erro ao carregar grupos: ' + (xhr.responseJSON?.error || 'Erro desconhecido'));
        });
}

function populateGroupSelects(groups) {
    const addSelect = $('#addGroups');
    const editSelect = $('#editGroups');
    
    addSelect.empty();
    editSelect.empty();
    
    groups.forEach(function(group) {
        const option = `<option value="${group.id}">${group.name}</option>`;
        addSelect.append(option);
        editSelect.append(option);
    });
}

// ===== Save User =====
function saveUser() {
    const username = $('#addUsername').val().trim();
    const email = $('#addEmail').val().trim();
    const password = $('#addPassword').val();
    const isAdmin = $('#addIsAdmin').is(':checked');
    const isActive = $('#addIsActive').is(':checked');
    const groupIds = $('#addGroups').val() || [];
    
    if (!username || !email || !password) {
        showError('Por favor, preencha todos os campos obrigatórios');
        return;
    }
    
    const userData = {
        username: username,
        email: email,
        password: password,
        is_admin: isAdmin,
        is_active: isActive,
        group_ids: groupIds.map(Number)
    };
    
    apiPost('/api/users', userData)
        .done(function() {
            showSuccess('Usuário criado com sucesso!');
            closeModal('addUserModal');
            loadUsers();
        })
        .fail(function(xhr) {
            showError('Erro ao criar usuário: ' + (xhr.responseJSON?.error || 'Erro desconhecido'));
        });
}

// ===== Open Edit User Modal =====
function openEditUserModal(userId) {
    const user = allUsers.find(u => u.id === userId);
    if (!user) return;
    
    $('#editUserId').val(user.id);
    $('#editUsername').val(user.username);
    $('#editEmail').val(user.email);
    $('#editIsAdmin').prop('checked', user.is_admin);
    $('#editIsActive').prop('checked', user.is_active);
    
    // Select user's groups
    const groupIds = user.groups.map(g => g.id.toString());
    $('#editGroups').val(groupIds);
    
    openModal('editUserModal');
}

// ===== Update User =====
function updateUser() {
    const userId = $('#editUserId').val();
    const username = $('#editUsername').val().trim();
    const email = $('#editEmail').val().trim();
    const isAdmin = $('#editIsAdmin').is(':checked');
    const isActive = $('#editIsActive').is(':checked');
    const groupIds = $('#editGroups').val() || [];
    
    if (!username || !email) {
        showError('Por favor, preencha todos os campos obrigatórios');
        return;
    }
    
    const userData = {
        username: username,
        email: email,
        is_admin: isAdmin,
        is_active: isActive,
        group_ids: groupIds.map(Number)
    };
    
    apiPut(`/api/users/${userId}`, userData)
        .done(function() {
            showSuccess('Usuário atualizado com sucesso!');
            closeModal('editUserModal');
            loadUsers();
        })
        .fail(function(xhr) {
            showError('Erro ao atualizar usuário: ' + (xhr.responseJSON?.error || 'Erro desconhecido'));
        });
}

// ===== Toggle User Status =====
function toggleUserStatus(userId, activate) {
    const endpoint = activate ? 'activate' : 'deactivate';
    const message = activate ? 'ativado' : 'inativado';
    
    apiPost(`/api/users/${userId}/${endpoint}`)
        .done(function() {
            showSuccess(`Usuário ${message} com sucesso!`);
            loadUsers();
        })
        .fail(function(xhr) {
            showError(`Erro ao ${message} usuário: ` + (xhr.responseJSON?.error || 'Erro desconhecido'));
        });
}

// ===== Toggle Admin =====
function toggleAdmin(userId, makeAdmin) {
    const endpoint = makeAdmin ? 'make-admin' : 'remove-admin';
    const message = makeAdmin ? 'promovido a administrador' : 'removido de administrador';
    
    apiPost(`/api/users/${userId}/${endpoint}`)
        .done(function() {
            showSuccess(`Usuário ${message} com sucesso!`);
            loadUsers();
        })
        .fail(function(xhr) {
            showError(`Erro: ` + (xhr.responseJSON?.error || 'Erro desconhecido'));
        });
}

// ===== Open Reset Password Modal =====
function openResetPasswordModal(userId) {
    $('#resetUserId').val(userId);
    openModal('resetPasswordModal');
}

// ===== Reset Password =====
function resetPassword() {
    const userId = $('#resetUserId').val();
    const newPassword = $('#newPassword').val();
    const confirmPassword = $('#confirmPassword').val();
    
    if (!newPassword || !confirmPassword) {
        showError('Por favor, preencha todos os campos');
        return;
    }
    
    if (newPassword !== confirmPassword) {
        showError('As senhas não coincidem');
        return;
    }
    
    apiPost(`/api/users/${userId}/reset-password`, { new_password: newPassword })
        .done(function() {
            showSuccess('Senha resetada com sucesso!');
            closeModal('resetPasswordModal');
        })
        .fail(function(xhr) {
            showError('Erro ao resetar senha: ' + (xhr.responseJSON?.error || 'Erro desconhecido'));
        });
}

// ===== Open Delete User Modal =====
function openDeleteUserModal(userId) {
    $('#deleteUserId').val(userId);
    openModal('deleteUserModal');
}

// ===== Delete User =====
function deleteUser() {
    const userId = $('#deleteUserId').val();
    
    apiDelete(`/api/users/${userId}`)
        .done(function() {
            showSuccess('Usuário deletado com sucesso!');
            closeModal('deleteUserModal');
            loadUsers();
        })
        .fail(function(xhr) {
            showError('Erro ao deletar usuário: ' + (xhr.responseJSON?.error || 'Erro desconhecido'));
        });
}


