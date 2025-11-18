// ===== Groups Page JavaScript =====

let allGroups = [];

$(document).ready(function() {
    loadGroups();
    
    // Search functionality
    $('#searchGroup').on('input', debounce(filterGroups, 300));
    
    // Add group
    $('#saveGroupBtn').click(saveGroup);
    
    // Update group
    $('#updateGroupBtn').click(updateGroup);
    
    // Delete group
    $('#confirmDeleteGroupBtn').click(deleteGroup);
    
    // Clear forms when modals close
    $('#addGroupModal').on('hidden.bs.modal', function() {
        $('#addGroupForm')[0].reset();
    });
    
    $('#editGroupModal').on('hidden.bs.modal', function() {
        $('#editGroupForm')[0].reset();
    });
});

// ===== Load Groups =====
function loadGroups() {
    showLoading('loadingGroups');
    
    apiGet('/api/groups')
        .done(function(data) {
            allGroups = data;
            renderGroups(data);
        })
        .fail(function(xhr) {
            showError('Erro ao carregar grupos: ' + (xhr.responseJSON?.error || 'Erro desconhecido'));
        })
        .always(function() {
            hideLoading('loadingGroups');
        });
}

// ===== Render Groups =====
function renderGroups(groups) {
    const tbody = $('#groupsTableBody');
    tbody.empty();
    
    if (groups.length === 0) {
        tbody.append('<tr><td colspan="6" class="text-center">Nenhum grupo encontrado</td></tr>');
        return;
    }
    
    groups.forEach(function(group) {
        const row = `
            <tr>
                <td>${group.id}</td>
                <td><strong>${group.name}</strong></td>
                <td>${group.description || '<span class="text-muted">Sem descrição</span>'}</td>
                <td>
                    <button class="btn btn-sm btn-outline-info" onclick="viewGroupUsers(${group.id})">
                        <i class="bi bi-people"></i> ${group.user_count} usuário(s)
                    </button>
                </td>
                <td>${formatDate(group.created_at)}</td>
                <td>
                    <div class="btn-group btn-group-sm" role="group">
                        <button class="btn btn-outline-primary" onclick="openEditGroupModal(${group.id})" title="Editar">
                            <i class="bi bi-pencil"></i>
                        </button>
                        <button class="btn btn-outline-info" onclick="viewGroupUsers(${group.id})" title="Ver Membros">
                            <i class="bi bi-people"></i>
                        </button>
                        <button class="btn btn-outline-danger" onclick="openDeleteGroupModal(${group.id})" title="Deletar">
                            <i class="bi bi-trash"></i>
                        </button>
                    </div>
                </td>
            </tr>
        `;
        
        tbody.append(row);
    });
}

// ===== Filter Groups =====
function filterGroups() {
    const searchTerm = $('#searchGroup').val().toLowerCase();
    
    let filtered = allGroups.filter(function(group) {
        return !searchTerm || 
            group.name.toLowerCase().includes(searchTerm) ||
            (group.description && group.description.toLowerCase().includes(searchTerm));
    });
    
    renderGroups(filtered);
}

// ===== Save Group =====
function saveGroup() {
    const name = $('#addGroupName').val().trim();
    const description = $('#addGroupDescription').val().trim();
    
    if (!name) {
        showError('Por favor, informe o nome do grupo');
        return;
    }
    
    const groupData = {
        name: name,
        description: description
    };
    
    apiPost('/api/groups', groupData)
        .done(function() {
            showSuccess('Grupo criado com sucesso!');
            closeModal('addGroupModal');
            loadGroups();
        })
        .fail(function(xhr) {
            showError('Erro ao criar grupo: ' + (xhr.responseJSON?.error || 'Erro desconhecido'));
        });
}

// ===== Open Edit Group Modal =====
function openEditGroupModal(groupId) {
    const group = allGroups.find(g => g.id === groupId);
    if (!group) return;
    
    $('#editGroupId').val(group.id);
    $('#editGroupName').val(group.name);
    $('#editGroupDescription').val(group.description || '');
    
    openModal('editGroupModal');
}

// ===== Update Group =====
function updateGroup() {
    const groupId = $('#editGroupId').val();
    const name = $('#editGroupName').val().trim();
    const description = $('#editGroupDescription').val().trim();
    
    if (!name) {
        showError('Por favor, informe o nome do grupo');
        return;
    }
    
    const groupData = {
        name: name,
        description: description
    };
    
    apiPut(`/api/groups/${groupId}`, groupData)
        .done(function() {
            showSuccess('Grupo atualizado com sucesso!');
            closeModal('editGroupModal');
            loadGroups();
        })
        .fail(function(xhr) {
            showError('Erro ao atualizar grupo: ' + (xhr.responseJSON?.error || 'Erro desconhecido'));
        });
}

// ===== Open Delete Group Modal =====
function openDeleteGroupModal(groupId) {
    $('#deleteGroupId').val(groupId);
    openModal('deleteGroupModal');
}

// ===== Delete Group =====
function deleteGroup() {
    const groupId = $('#deleteGroupId').val();
    
    apiDelete(`/api/groups/${groupId}`)
        .done(function() {
            showSuccess('Grupo deletado com sucesso!');
            closeModal('deleteGroupModal');
            loadGroups();
        })
        .fail(function(xhr) {
            showError('Erro ao deletar grupo: ' + (xhr.responseJSON?.error || 'Erro desconhecido'));
        });
}

// ===== View Group Users =====
function viewGroupUsers(groupId) {
    $('#viewGroupId').val(groupId);
    const group = allGroups.find(g => g.id === groupId);
    
    if (!group) return;
    
    // Update modal title
    $('#viewGroupUsersModal .modal-title').html(`<i class="bi bi-people"></i> Membros do Grupo: ${group.name}`);
    
    // Show loading
    $('#groupUsersContent').html(`
        <div class="text-center py-4">
            <div class="spinner-border text-info" role="status">
                <span class="visually-hidden">Carregando...</span>
            </div>
        </div>
    `);
    
    openModal('viewGroupUsersModal');
    
    // Load available users for dropdown
    loadAvailableUsersForGroup(groupId);
    
    // Load current users
    loadGroupUsers(groupId);
}

// ===== Load Available Users for Group =====
function loadAvailableUsersForGroup(groupId) {
    apiGet('/api/users')
        .done(function(users) {
            const select = $('#addUserToGroup');
            select.empty();
            select.append('<option value="">Selecione um usuário...</option>');
            
            users.forEach(function(user) {
                select.append(`<option value="${user.id}">${user.username} (${user.email})</option>`);
            });
        })
        .fail(function() {
            showError('Erro ao carregar lista de usuários');
        });
}

// ===== Load Group Users =====
function loadGroupUsers(groupId) {
    apiGet(`/api/groups/${groupId}/users`)
        .done(function(users) {
            renderGroupUsers(users, groupId);
        })
        .fail(function(xhr) {
            $('#groupUsersContent').html(`
                <div class="alert alert-danger">
                    Erro ao carregar usuários: ${xhr.responseJSON?.error || 'Erro desconhecido'}
                </div>
            `);
        });
}

// ===== Render Group Users =====
function renderGroupUsers(users, groupId) {
    const container = $('#groupUsersContent');
    
    if (users.length === 0) {
        container.html(`
            <div class="alert alert-info">
                <i class="bi bi-info-circle"></i> Este grupo ainda não possui membros.
            </div>
        `);
        return;
    }
    
    let html = '<div class="list-group">';
    
    users.forEach(function(user) {
        const statusBadge = user.is_active 
            ? '<span class="badge bg-success">Ativo</span>' 
            : '<span class="badge bg-danger">Inativo</span>';
        
        const adminBadge = user.is_admin
            ? '<span class="badge bg-primary ms-1">Admin</span>'
            : '';
        
        html += `
            <div class="list-group-item">
                <div class="d-flex w-100 justify-content-between align-items-center">
                    <div>
                        <h6 class="mb-1">
                            <i class="bi bi-person"></i> ${user.username}
                            ${statusBadge}
                            ${adminBadge}
                        </h6>
                        <p class="mb-0 text-muted small">
                            <i class="bi bi-envelope"></i> ${user.email}
                        </p>
                    </div>
                    <div>
                        <button class="btn btn-sm btn-danger" onclick="removeUserFromGroup(${user.id}, ${groupId})" title="Remover do grupo">
                            <i class="bi bi-person-dash"></i> Remover
                        </button>
                    </div>
                </div>
            </div>
        `;
    });
    
    html += '</div>';
    
    container.html(html);
}

// ===== Add User to Current Group =====
function addUserToCurrentGroup() {
    const groupId = $('#viewGroupId').val();
    const userId = $('#addUserToGroup').val();
    
    if (!userId) {
        showError('Por favor, selecione um usuário');
        return;
    }
    
    // Add user to group via API
    apiPost(`/api/users/${userId}/groups`, { group_ids: [parseInt(groupId)] })
        .done(function() {
            showSuccess('Usuário adicionado ao grupo com sucesso!');
            // Reload group users
            loadGroupUsers(groupId);
            // Reset dropdown
            $('#addUserToGroup').val('');
            // Reload groups to update count
            loadGroups();
        })
        .fail(function(xhr) {
            showError('Erro ao adicionar usuário: ' + (xhr.responseJSON?.error || 'Erro desconhecido'));
        });
}

// ===== Remove User from Group =====
function removeUserFromGroup(userId, groupId) {
    if (!confirm('Tem certeza que deseja remover este usuário do grupo?')) {
        return;
    }
    
    apiDelete(`/api/users/${userId}/groups/${groupId}`)
        .done(function() {
            showSuccess('Usuário removido do grupo com sucesso!');
            // Reload group users
            loadGroupUsers(groupId);
            // Reload groups to update count
            loadGroups();
        })
        .fail(function(xhr) {
            showError('Erro ao remover usuário: ' + (xhr.responseJSON?.error || 'Erro desconhecido'));
        });
}


