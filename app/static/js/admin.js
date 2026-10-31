let token = localStorage.getItem('admin_token');
if (!token) window.location.href = '/admin';

let currentAdmin = null;
let batches = [];
let sessions = [];
let auditLogs = [];

document.addEventListener('DOMContentLoaded', async () => {
    await loadAdminProfile();
    await loadBatches();
    await loadSessions();
});

function logout() {
    localStorage.removeItem('admin_token');
    window.location.href = '/admin';
}

async function api(url, options = {}) {
    options.headers = options.headers || {};
    options.headers['Authorization'] = `Bearer ${token}`;
    if (options.body && typeof options.body !== 'string') {
        options.body = JSON.stringify(options.body);
        options.headers['Content-Type'] = 'application/json';
    }
    const res = await fetch(url, options);
    if (res.status === 401) logout();
    if (!res.ok) throw await res.json();
    return res.json();
}

async function loadAdminProfile() {
    try {
        currentAdmin = await api('/api/admin/me');
        const nameEl = document.getElementById('admin-name');
        const roleEl = document.getElementById('admin-role-badge');
        const tabAudit = document.getElementById('tab-audit-logs');
        if (nameEl) nameEl.textContent = currentAdmin.name;
        if (roleEl) {
            roleEl.textContent = currentAdmin.role === 'SUPER_ADMIN' ? 'SUPER ADMIN' : `COORD: ${currentAdmin.assigned_classes}`;
        }
        if (tabAudit) {
            if (currentAdmin.role === 'SUPER_ADMIN') {
                tabAudit.classList.remove('hidden');
            } else {
                tabAudit.classList.add('hidden');
            }
        }
    } catch(e) {
        console.error('Error loading admin profile', e);
    }
}

function switchTab(tab) {
    if (tab === 'audit-logs' && (!currentAdmin || currentAdmin.role !== 'SUPER_ADMIN')) {
        tab = 'sessions';
    }

    document.getElementById('sessions-view').classList.add('hidden');
    document.getElementById('batches-view').classList.add('hidden');
    document.getElementById('audit-logs-view').classList.add('hidden');

    document.getElementById('tab-sessions').className = 'font-bold text-base sm:text-lg text-slate-400 hover:text-amber-700 px-2 pb-2 transition-all whitespace-nowrap';
    document.getElementById('tab-batches').className = 'font-bold text-base sm:text-lg text-slate-400 hover:text-amber-700 px-2 pb-2 transition-all whitespace-nowrap';
    
    const tabAudit = document.getElementById('tab-audit-logs');
    if (tabAudit) {
        tabAudit.className = 'font-bold text-base sm:text-lg text-slate-400 hover:text-amber-700 px-2 pb-2 transition-all whitespace-nowrap flex items-center gap-1.5' + (currentAdmin && currentAdmin.role === 'SUPER_ADMIN' ? '' : ' hidden');
    }
    
    const createBtn = document.getElementById('btn-create-main');
    const createLabel = document.getElementById('btn-create-label');

    if (tab === 'sessions') {
        document.getElementById('sessions-view').classList.remove('hidden');
        document.getElementById('tab-sessions').className = 'font-extrabold text-base sm:text-lg text-amber-700 border-b-2 border-amber-500 px-2 pb-2 transition-all whitespace-nowrap';
        if (createBtn) createBtn.classList.remove('hidden');
        if (createLabel) createLabel.innerText = 'Create Session';
        loadSessions();
    } else if (tab === 'batches') {
        document.getElementById('batches-view').classList.remove('hidden');
        document.getElementById('tab-batches').className = 'font-extrabold text-base sm:text-lg text-amber-700 border-b-2 border-amber-500 px-2 pb-2 transition-all whitespace-nowrap';
        if (createBtn) createBtn.classList.remove('hidden');
        if (createLabel) createLabel.innerText = 'Create Batches';
        loadBatches();
    } else if (tab === 'audit-logs' && currentAdmin && currentAdmin.role === 'SUPER_ADMIN') {
        document.getElementById('audit-logs-view').classList.remove('hidden');
        if (tabAudit) {
            tabAudit.className = 'font-extrabold text-base sm:text-lg text-amber-700 border-b-2 border-amber-500 px-2 pb-2 transition-all whitespace-nowrap flex items-center gap-1.5';
        }
        if (createBtn) createBtn.classList.add('hidden');
        loadAuditLogs();
    }
}

let adminBatchSearchQuery = '';

function handleAdminBatchSearch(val) {
    adminBatchSearchQuery = (val || '').trim().toLowerCase();
    const clearBtn = document.getElementById('admin-batch-search-clear');
    if (clearBtn) {
        clearBtn.classList.toggle('hidden', !adminBatchSearchQuery);
    }
    filterAdminBatches();
}

function clearAdminBatchSearch() {
    const searchInput = document.getElementById('admin-batch-search');
    if (searchInput) searchInput.value = '';
    adminBatchSearchQuery = '';
    const clearBtn = document.getElementById('admin-batch-search-clear');
    if (clearBtn) clearBtn.classList.add('hidden');
    filterAdminBatches();
}

function filterAdminBatches() {
    const syl = document.getElementById('admin-batch-syllabus')?.value || 'ALL';
    const cls = document.getElementById('admin-batch-class')?.value || 'ALL';

    const filtered = (batches || []).filter(b => {
        if (adminBatchSearchQuery) {
            const name = (b.name || '').toLowerCase();
            const syllabus = (b.syllabus || '').toLowerCase();
            const cat = (b.class_category || '').toLowerCase();
            if (!name.includes(adminBatchSearchQuery) && !syllabus.includes(adminBatchSearchQuery) && !cat.includes(adminBatchSearchQuery)) {
                return false;
            }
        }
        if (syl !== 'ALL') {
            if (syl === 'EXAM KILLER') {
                const isExamKiller = b.syllabus === 'EXAM KILLER' || (b.name && b.name.includes('EXAM KILLER'));
                if (!isExamKiller) return false;
            } else if (b.syllabus !== syl) {
                return false;
            }
        }
        if (cls !== 'ALL') {
            if (cls === 'EXAM KILLER') {
                const isExam = b.class_category === 'EXAM KILLER' || (b.name && b.name.includes('EXAM KILLER'));
                if (!isExam) return false;
            } else if (b.class_category !== cls) {
                return false;
            }
        }
        return true;
    });

    renderBatchesTable(filtered);
}

function resetAdminBatchFilters() {
    const searchInput = document.getElementById('admin-batch-search');
    if (searchInput) searchInput.value = '';
    adminBatchSearchQuery = '';
    const clearBtn = document.getElementById('admin-batch-search-clear');
    if (clearBtn) clearBtn.classList.add('hidden');
    const sylElem = document.getElementById('admin-batch-syllabus');
    if (sylElem) sylElem.value = 'ALL';
    const clsElem = document.getElementById('admin-batch-class');
    if (clsElem) clsElem.value = 'ALL';
    renderBatchesTable(batches);
}

function renderBatchesTable(list) {
    const tbody = document.getElementById('batches-tbody');
    if (!tbody) return;
    tbody.innerHTML = '';

    const countElem = document.getElementById('admin-batch-count');
    if (countElem) {
        countElem.innerText = `${list.length} Batches`;
    }

    if (!list || list.length === 0) {
        tbody.innerHTML = `<tr><td colspan="6" class="p-8 text-center text-slate-400">No batches available for this class scope.</td></tr>`;
        return;
    }

    list.forEach(b => {
        const isCbse = b.syllabus === 'CBSE';
        const isExamKiller = b.syllabus === 'EXAM KILLER' || (b.name && b.name.includes('EXAM KILLER'));
        const sylBadge = isCbse 
            ? `<span class="bg-blue-50 text-blue-800 border border-blue-200 px-2 py-0.5 rounded-full text-xs font-bold">CBSE</span>`
            : (isExamKiller 
                ? `<span class="bg-rose-50 text-rose-700 border border-rose-300 px-2 py-0.5 rounded-full text-xs font-extrabold">⚡ EXAM KILLER</span>`
                : `<span class="bg-emerald-50 text-emerald-800 border border-emerald-200 px-2 py-0.5 rounded-full text-xs font-bold">STATE</span>`);

        const catBadge = b.class_category ? `
            <span class="bg-amber-100 text-amber-900 border border-amber-300/80 px-2 py-0.5 rounded-md text-xs font-extrabold">
                ${b.class_category}
            </span>` : '<span class="text-slate-400">-</span>';

        tbody.innerHTML += `
            <tr class="hover:bg-amber-50/30 transition-colors">
                <td class="p-4 text-slate-400 font-mono text-xs">#${b.id}</td>
                <td class="p-4">${catBadge}</td>
                <td class="p-4 font-bold text-slate-800 flex items-center gap-2">
                    <span>${b.name}</span>
                </td>
                <td class="p-4">${sylBadge}</td>
                <td class="p-4">
                    <span class="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-extrabold ${b.is_active ? 'bg-emerald-50 text-emerald-700 border border-emerald-200' : 'bg-red-50 text-red-700 border border-red-200'}">
                        ${b.is_active ? 'Active' : 'Inactive'}
                    </span>
                </td>
                <td class="p-4 text-right space-x-2 whitespace-nowrap">
                    <button onclick="editBatch(${b.id})" class="text-xs font-bold text-amber-700 hover:text-amber-900 bg-amber-50 hover:bg-amber-100 px-3 py-1.5 rounded-lg border border-amber-200 transition-colors">Edit</button>
                    <button onclick="deleteBatch(${b.id})" class="text-xs font-bold text-red-600 hover:text-red-800 bg-red-50 hover:bg-red-100 px-3 py-1.5 rounded-lg border border-red-200 transition-colors">Delete</button>
                </td>
            </tr>
        `;
    });
}

async function loadBatches() {
    try {
        let url = '/api/batches';
        if (currentAdmin && currentAdmin.assigned_classes && currentAdmin.assigned_classes !== 'ALL') {
            url += `?class_category=${encodeURIComponent(currentAdmin.assigned_classes)}`;
        }
        batches = await api(url);
        filterAdminBatches();
    } catch(e) {
        console.error(e);
    }
}

let adminSessionSearchQuery = '';

function handleAdminSessionSearch(val) {
    adminSessionSearchQuery = (val || '').trim().toLowerCase();
    const clearBtn = document.getElementById('admin-session-search-clear');
    if (clearBtn) {
        if (adminSessionSearchQuery) clearBtn.classList.remove('hidden');
        else clearBtn.classList.add('hidden');
    }
    renderSessionsTable();
}

function clearAdminSessionSearch() {
    const input = document.getElementById('admin-session-search');
    if (input) input.value = '';
    adminSessionSearchQuery = '';
    const clearBtn = document.getElementById('admin-session-search-clear');
    if (clearBtn) clearBtn.classList.add('hidden');
    renderSessionsTable();
}

function filterAdminSessions() {
    renderSessionsTable();
}

function resetAdminSessionFilters() {
    const searchInput = document.getElementById('admin-session-search');
    const syllabusSel = document.getElementById('admin-session-syllabus');
    const classSel = document.getElementById('admin-session-class');
    const dateSel = document.getElementById('admin-session-date');
    const clearBtn = document.getElementById('admin-session-search-clear');

    if (searchInput) searchInput.value = '';
    adminSessionSearchQuery = '';
    if (clearBtn) clearBtn.classList.add('hidden');
    if (syllabusSel) syllabusSel.value = 'ALL';
    if (classSel) classSel.value = 'ALL';
    if (dateSel) dateSel.value = 'ALL';

    renderSessionsTable();
}

async function loadSessions() {
    try {
        let url = '/api/sessions';
        if (currentAdmin && currentAdmin.assigned_classes && currentAdmin.assigned_classes !== 'ALL') {
            url += `?class_category=${encodeURIComponent(currentAdmin.assigned_classes)}`;
        }
        sessions = await api(url);
        renderSessionsTable();
    } catch(e) {
        console.error(e);
    }
}

function getAdminLocalDateStr() {
    const now = new Date();
    const y = now.getFullYear();
    const m = String(now.getMonth() + 1).padStart(2, '0');
    const d = String(now.getDate()).padStart(2, '0');
    return `${y}-${m}-${d}`;
}

function renderSessionsTable() {
    const tbody = document.getElementById('sessions-tbody');
    const countBadge = document.getElementById('admin-session-count');
    if (!tbody) return;
    tbody.innerHTML = '';

    const syllabusFilter = document.getElementById('admin-session-syllabus')?.value || 'ALL';
    const classFilter = document.getElementById('admin-session-class')?.value || 'ALL';
    const dateFilter = document.getElementById('admin-session-date')?.value || 'ALL';

    const todayStr = getAdminLocalDateStr();

    let filtered = sessions.filter(s => {
        // 1. Syllabus filter
        if (syllabusFilter !== 'ALL') {
            const syl = (s.batch && s.batch.syllabus ? s.batch.syllabus : '').toUpperCase();
            if (syllabusFilter === 'EXAM KILLER') {
                const batchName = (s.batch && s.batch.name ? s.batch.name : '').toUpperCase();
                if (syl !== 'EXAM KILLER' && !batchName.includes('EXAM KILLER')) return false;
            } else if (syl !== syllabusFilter) {
                return false;
            }
        }


        // 2. Class filter
        if (classFilter !== 'ALL') {
            const classCat = (s.class_category || (s.batch ? s.batch.class_category : '') || (s.batch ? s.batch.class_number : '') || '').toUpperCase();
            if (classCat !== classFilter) return false;
        }

        // 3. Date filter
        if (dateFilter === 'TODAY') {
            if (s.class_date !== todayStr) return false;
        } else if (dateFilter === 'UPCOMING') {
            if (s.class_date <= todayStr) return false;
        } else if (dateFilter === 'PAST') {
            if (s.class_date >= todayStr) return false;
        }

        // 4. Search query
        if (adminSessionSearchQuery) {
            const batchName = (s.batch ? s.batch.name : '').toLowerCase();
            const topic = (s.topic || '').toLowerCase();
            const startTime = (s.start_time || '').toLowerCase();
            const classCat = (s.class_category || (s.batch ? s.batch.class_category : '') || '').toLowerCase();
            const matches = batchName.includes(adminSessionSearchQuery) || 
                            topic.includes(adminSessionSearchQuery) || 
                            startTime.includes(adminSessionSearchQuery) || 
                            classCat.includes(adminSessionSearchQuery);
            if (!matches) return false;
        }

        return true;
    });

    if (countBadge) {
        countBadge.textContent = `${filtered.length} of ${sessions.length} Sessions`;
    }

    if (filtered.length === 0) {
        tbody.innerHTML = `
            <tr>
                <td colspan="7" class="p-8 text-center text-slate-400">
                    No sessions match the selected filters.
                    <button onclick="resetAdminSessionFilters()" class="text-amber-600 font-bold ml-1.5 underline hover:text-amber-700">Reset Filters</button>
                </td>
            </tr>`;
        return;
    }

    filtered.forEach(s => {
        const syllabus = s.batch && s.batch.syllabus ? s.batch.syllabus : '';
        const sylBadge = syllabus === 'CBSE' 
            ? `<span class="bg-blue-50 text-blue-800 border border-blue-200 px-1.5 py-0.5 rounded text-[10px] font-black mr-1">CBSE</span>`
            : (syllabus === 'EXAM KILLER' || (s.batch && s.batch.name && s.batch.name.includes('EXAM KILLER'))
                ? `<span class="bg-rose-50 text-rose-700 border border-rose-300 px-1.5 py-0.5 rounded text-[10px] font-black mr-1">⚡ EXAM KILLER</span>`
                : (syllabus === 'STATE' ? `<span class="bg-emerald-50 text-emerald-800 border border-emerald-200 px-1.5 py-0.5 rounded text-[10px] font-black mr-1">STATE</span>` : ''));


        const classCat = s.class_category || (s.batch ? s.batch.class_category : '') || (s.batch ? s.batch.class_number : '');
        const classBadge = classCat ? `
            <span class="bg-amber-100 text-amber-900 border border-amber-300/80 px-2 py-0.5 rounded-md text-xs font-black uppercase">
                ${classCat}
            </span>` : '<span class="text-slate-400">-</span>';

        tbody.innerHTML += `
            <tr class="hover:bg-amber-50/30 transition-colors">
                <td class="p-4 font-semibold text-slate-800">${s.class_date}</td>
                <td class="p-4">${classBadge}</td>
                <td class="p-4 text-slate-600">
                    <span class="bg-amber-50 text-amber-900 border border-amber-200 px-2.5 py-1 rounded-full font-bold text-xs inline-flex items-center gap-1">
                        ${sylBadge}
                        <span>${s.batch ? s.batch.name : 'Unknown'}</span>
                    </span>
                </td>
                <td class="p-4 font-extrabold text-slate-900">${s.topic}</td>
                <td class="p-4 font-medium text-slate-600">${s.start_time}</td>
                <td class="p-4">
                    <span class="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-extrabold ${s.is_active ? 'bg-emerald-50 text-emerald-700 border border-emerald-200' : 'bg-red-50 text-red-700 border border-red-200'}">
                        ${s.is_active ? 'Active' : 'Inactive'}
                    </span>
                </td>
                <td class="p-4 text-right space-x-2">
                    <button onclick="editSession(${s.id})" class="text-xs font-bold text-amber-700 hover:text-amber-900 bg-amber-50 hover:bg-amber-100 px-3 py-1.5 rounded-lg border border-amber-200 transition-colors">Edit</button>
                    <button onclick="deleteSession(${s.id})" class="text-xs font-bold text-red-600 hover:text-red-800 bg-red-50 hover:bg-red-100 px-3 py-1.5 rounded-lg border border-red-200 transition-colors">Delete</button>
                </td>
            </tr>
        `;
    });
}

async function loadAuditLogs() {
    try {
        auditLogs = await api('/api/admin/audit-logs?limit=100');
        const tbody = document.getElementById('audit-logs-tbody');
        tbody.innerHTML = '';
        if (auditLogs.length === 0) {
            tbody.innerHTML = `<tr><td colspan="6" class="p-8 text-center text-slate-400">No mentor access actions recorded yet.</td></tr>`;
            return;
        }
        auditLogs.forEach(log => {
            let actionBadge = `<span class="bg-slate-100 text-slate-800 px-2 py-0.5 rounded font-bold uppercase">${log.action}</span>`;
            if (log.action === 'COPY_MESSAGE' || log.action === 'COPY_LINK') {
                actionBadge = `<span class="bg-emerald-100 text-emerald-900 border border-emerald-300/80 px-2 py-0.5 rounded font-extrabold uppercase">✓ Copied Message</span>`;
            } else if (log.action === 'JOIN_ZOOM') {
                actionBadge = `<span class="bg-blue-100 text-blue-900 border border-blue-300/80 px-2 py-0.5 rounded font-extrabold uppercase">⚡ Launched Zoom</span>`;
            } else if (log.action === 'LOGIN') {
                actionBadge = `<span class="bg-amber-100 text-amber-900 border border-amber-300/80 px-2 py-0.5 rounded font-extrabold uppercase">🔑 Staff Login</span>`;
            }

            const timeStr = log.created_at ? new Date(log.created_at).toLocaleString([], { dateStyle: 'short', timeStyle: 'medium' }) : '-';

            tbody.innerHTML += `
                <tr class="hover:bg-slate-50 transition-colors">
                    <td class="p-4 font-mono text-slate-500">${timeStr}</td>
                    <td class="p-4 font-extrabold text-slate-900">${log.mentor_name}</td>
                    <td class="p-4">
                        <span class="bg-amber-50 text-amber-900 border border-amber-200 px-2 py-0.5 rounded font-bold">${log.assigned_class}</span>
                    </td>
                    <td class="p-4">${actionBadge}</td>
                    <td class="p-4 font-medium text-slate-700">${log.batch_name || log.details || '-'}</td>
                    <td class="p-4 font-mono text-slate-400">${log.ip_address || '-'}</td>
                </tr>
            `;
        });
    } catch(e) {
        console.error(e);
    }
}

function updateBatchDropdownOptions(selectedCategory, selectedSyllabus) {
    const batchSelect = document.getElementById('s_batch');
    if (!batchSelect) return;

    let filtered = batches;
    if (selectedCategory && selectedCategory !== 'ALL') {
        filtered = filtered.filter(b => {
            if (selectedCategory === 'EXAM KILLER') {
                return (b.syllabus === 'EXAM KILLER') || (b.class_category === 'EXAM KILLER') || (b.name && b.name.includes('EXAM KILLER'));
            }
            if (b.class_category === selectedCategory) return true;
            if (b.class_number === selectedCategory) return true;
            if (b.class_number && selectedCategory.startsWith(b.class_number)) return true;
            return false;
        });
    }
    if (selectedSyllabus && selectedSyllabus !== 'ALL') {
        filtered = filtered.filter(b => {
            if (selectedSyllabus === 'EXAM KILLER') {
                return (b.syllabus === 'EXAM KILLER') || (b.name && b.name.includes('EXAM KILLER'));
            }
            return b.syllabus === selectedSyllabus;
        });
    }

    if (filtered.length === 0) {
        batchSelect.innerHTML = `<option value="" disabled selected>No matching batches found (${selectedCategory} - ${selectedSyllabus})</option>`;
        return;
    }

    batchSelect.innerHTML = filtered.map(b => {
        const sylTag = b.syllabus ? `[${b.syllabus}]` : '';
        return `<option value="${b.id}">${sylTag} ${b.name}</option>`;
    }).join('');
}

function onClassCategoryOrSyllabusChange() {
    const cat = document.getElementById('s_class_category')?.value || 'ALL';
    const syl = document.getElementById('s_syllabus_filter')?.value || 'ALL';
    updateBatchDropdownOptions(cat, syl);
}

function showCreateModal() {
    const isBatchesTab = !document.getElementById('batches-view').classList.contains('hidden');
    if (isBatchesTab) {
        document.getElementById('modal-title').innerText = 'Create Batch';
        document.getElementById('modal-body').innerHTML = `
            <form id="createForm" onsubmit="submitBatch(event)">
                <div class="space-y-3.5">
                    <div>
                        <label class="block text-xs font-bold text-slate-700 mb-1">Batch Name</label>
                        <input required type="text" id="b_name" placeholder="e.g. 10TH EXAM KILLER SSLC BATCH" class="w-full px-4 py-2.5 border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-amber-400 text-xs font-bold">
                    </div>
                    <div>
                        <label class="block text-xs font-bold text-slate-700 mb-1">Syllabus / Program Category</label>
                        <select id="b_syllabus" class="w-full px-4 py-2.5 border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-amber-400 text-xs font-bold bg-white">
                            <option value="CBSE">CBSE Syllabus</option>
                            <option value="STATE">State Syllabus</option>
                            <option value="EXAM KILLER">⚡ Exam Killer Program</option>
                        </select>
                    </div>
                    <div>
                        <label class="block text-xs font-bold text-slate-700 mb-1">Class / Grade Category</label>
                        <select id="b_class_category" class="w-full px-4 py-2.5 border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-amber-400 text-xs font-bold bg-white">
                            <option value="8TH">8th Class</option>
                            <option value="9TH">9th Class</option>
                            <option value="10TH">10th Class</option>
                            <option value="11TH SCI">11th Science</option>
                            <option value="11TH COM">11th Commerce</option>
                            <option value="12TH SCI">12th Science</option>
                            <option value="12TH COM">12th Commerce</option>
                            <option value="EXAM KILLER">⚡ Exam Killer (All Streams)</option>
                        </select>
                    </div>
                    <button type="submit" class="w-full bg-amber-400 hover:bg-amber-500 text-slate-950 font-bold py-3 rounded-xl mt-4 shadow-sm transition-all text-sm">Save Batch</button>
                </div>
            </form>
        `;
    } else {
        document.getElementById('modal-title').innerText = 'Create Class Session';
        
        // Determine default class category based on coordinator
        let defaultCategory = '8TH';
        let isCategoryLocked = false;
        if (currentAdmin && currentAdmin.assigned_classes && currentAdmin.assigned_classes !== 'ALL') {
            const allowed = currentAdmin.assigned_classes.split(',')[0].trim();
            defaultCategory = allowed;
            if (!currentAdmin.assigned_classes.includes(',')) {
                isCategoryLocked = true;
            }
        }

        const categories = [
            { val: '8TH', label: '8th Class' },
            { val: '9TH', label: '9th Class' },
            { val: '10TH', label: '10th Class' },
            { val: '11TH SCI', label: '11th Science' },
            { val: '11TH COM', label: '11th Commerce' },
            { val: '12TH SCI', label: '12th Science' },
            { val: '12TH COM', label: '12th Commerce' },
            { val: 'EXAM KILLER', label: '⚡ Exam Killer (All Streams)' }
        ];

        const catOptionsHtml = categories.map(c => {
            const isSelected = c.val === defaultCategory ? 'selected' : '';
            return `<option value="${c.val}" ${isSelected}>${c.label}</option>`;
        }).join('');

        document.getElementById('modal-body').innerHTML = `
            <!-- Quick Zoom Paste Auto-Fill -->
            <div class="mb-4 p-4 bg-amber-50/80 border border-amber-200 rounded-2xl shadow-xs">
                <label class="block text-xs font-extrabold text-amber-950 mb-1 flex items-center justify-between">
                    <span class="flex items-center gap-1.5">⚡ Quick Zoom Paste Auto-Fill</span>
                    <span class="text-[10px] text-amber-700 font-semibold hidden sm:inline">Paste raw link or full WhatsApp invite</span>
                </label>
                <textarea id="z_paste" rows="2" oninput="clientParseZoom(this.value)" placeholder="Paste full Zoom meeting invitation or raw link here to auto-parse..." class="w-full px-3 py-2 border border-amber-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-amber-400 font-mono text-xs bg-white"></textarea>
                <div class="flex items-center gap-2 mt-2">
                    <button type="button" onclick="parseZoom()" class="text-xs bg-amber-400 hover:bg-amber-500 text-slate-950 px-3.5 py-1.5 rounded-lg font-bold shadow-sm transition-all flex items-center gap-1">
                        <span>🔍 Auto Parse Link & Credentials</span>
                    </button>
                    <span id="z_status" class="text-xs font-bold text-emerald-700 hidden"></span>
                </div>
                <div id="z_error" class="text-xs mt-2 hidden font-bold"></div>
            </div>

            <form id="createForm" onsubmit="submitSession(event)">
                <div class="space-y-3.5 grid grid-cols-2 gap-x-3.5">
                    
                    <!-- Class Stream / Category Selection -->
                    <div>
                        <label class="block text-xs font-bold text-slate-700 mb-1">Assigned Class Stream</label>
                        <select id="s_class_category" onchange="onClassCategoryOrSyllabusChange()" class="w-full px-3.5 py-2.5 border border-slate-200 rounded-xl bg-white focus:outline-none focus:ring-2 focus:ring-amber-400 text-xs font-bold">
                            ${catOptionsHtml}
                        </select>
                    </div>

                    <!-- Syllabus Selector -->
                    <div>
                        <label class="block text-xs font-bold text-slate-700 mb-1">Syllabus Filter</label>
                        <select id="s_syllabus_filter" onchange="onClassCategoryOrSyllabusChange()" class="w-full px-3.5 py-2.5 border border-slate-200 rounded-xl bg-white focus:outline-none focus:ring-2 focus:ring-amber-400 text-xs font-bold">
                            <option value="ALL">All Syllabuses / Programs</option>
                            <option value="CBSE">CBSE Batches Only</option>
                            <option value="STATE">STATE Batches Only</option>
                            <option value="EXAM KILLER">⚡ Exam Killer Batches Only</option>
                        </select>
                    </div>

                    <!-- Filtered Batch Selection -->
                    <div class="col-span-2">
                        <div class="flex justify-between items-center mb-1">
                            <label class="block text-xs font-bold text-slate-700">Select Batch (Filtered to Class)</label>
                            <button type="button" onclick="switchToCreateBatchModal()" class="text-xs text-amber-700 hover:text-amber-900 font-extrabold">+ New Batch</button>
                        </div>
                        <select required id="s_batch" class="w-full px-3.5 py-2.5 border border-slate-200 rounded-xl bg-white focus:outline-none focus:ring-2 focus:ring-amber-400 text-xs font-semibold"></select>
                    </div>

                    <div class="col-span-2">
                        <label class="block text-xs font-bold text-slate-700 mb-1">Class Topic / Subject</label>
                        <input required type="text" id="s_topic" placeholder="e.g. 10th Math - Trigonometry & Quad Equations" class="w-full px-3.5 py-2.5 border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-amber-400 text-sm font-medium">
                    </div>
                    <div>
                        <label class="block text-xs font-bold text-slate-700 mb-1">Date</label>
                        <input required type="date" id="s_date" class="w-full px-3.5 py-2.5 border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-amber-400 text-sm font-medium">
                    </div>
                    <div>
                        <label class="block text-xs font-bold text-slate-700 mb-1">Start Time</label>
                        <input required type="time" id="s_time" class="w-full px-3.5 py-2.5 border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-amber-400 text-sm font-medium">
                    </div>
                    <div class="col-span-2">
                        <label class="block text-xs font-bold text-slate-700 mb-1">Zoom Meeting Link</label>
                        <input required type="url" id="s_link" oninput="onZoomLinkInput(this.value)" placeholder="https://zoom.us/j/..." class="w-full px-3.5 py-2.5 border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-amber-400 text-sm font-medium">
                    </div>
                    <div>
                        <label class="block text-xs font-bold text-slate-700 mb-1">Meeting ID</label>
                        <input required type="text" id="s_id" placeholder="872 3421 9912" class="w-full px-3.5 py-2.5 border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-amber-400 text-sm font-medium">
                    </div>
                    <div>
                        <label class="block text-xs font-bold text-slate-700 mb-1">Passcode</label>
                        <input required type="text" id="s_pass" placeholder="123456" class="w-full px-3.5 py-2.5 border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-amber-400 text-sm font-medium">
                    </div>
                    <div class="col-span-2">
                        <button type="submit" class="w-full bg-amber-400 hover:bg-amber-500 text-slate-950 font-bold py-3 rounded-xl mt-3 shadow-sm transition-all text-sm">Save & Broadcast Session</button>
                    </div>
                </div>
            </form>
        `;

        // Populate initial batch dropdown
        updateBatchDropdownOptions(defaultCategory, 'ALL');
        // Set local today's date as default
        document.getElementById('s_date').value = getAdminLocalDateStr();
    }
    document.getElementById('modal').classList.remove('hidden');
}

function switchToCreateBatchModal() {
    switchTab('batches');
    showCreateModal();
}

function closeModal() {
    document.getElementById('modal').classList.add('hidden');
}

function clientParseZoom(text) {
    if (!text || !text.trim()) return;
    text = text.trim();

    // 1. Zoom link extraction
    const linkMatch = text.match(/https:\/\/[a-zA-Z0-9.-]*zoom\.us\/[^\s*<>"')]+/i);
    let zoomLink = linkMatch ? linkMatch[0].replace(/[\.,\*\>\)"'`]+$/, '') : '';

    // Mask URL from text to prevent false positives from query strings
    let cleanText = text;
    if (zoomLink) {
        cleanText = cleanText.replace(zoomLink, ' [ZOOM_LINK] ');
    }

    // 2. Meeting ID extraction
    let meetingId = '';
    const idLabelMatch = cleanText.match(/(?:meeting\s*id|webinar\s*id|conf\s*id|\bid)\s*[:=\-]?\s*\*?\s*([\d\s]{9,15})\b/i);
    if (idLabelMatch) {
        meetingId = idLabelMatch[1].trim().replace(/\s+/g, ' ');
    } else if (zoomLink) {
        const urlIdMatch = zoomLink.match(/zoom\.us\/(?:j|w|my)\/(\d{9,12})/i);
        if (urlIdMatch) {
            const rawId = urlIdMatch[1];
            if (rawId.length === 11) {
                meetingId = `${rawId.slice(0, 3)} ${rawId.slice(3, 7)} ${rawId.slice(7)}`;
            } else if (rawId.length === 10) {
                meetingId = `${rawId.slice(0, 3)} ${rawId.slice(3, 6)} ${rawId.slice(6)}`;
            } else {
                meetingId = rawId;
            }
        }
    }

    // 3. Passcode extraction
    let passcode = '';
    const passLabelMatch = cleanText.match(/(?:passcode|password|pass\s*code|\bpwd|\bpin|security\s*code)\s*[:=\-]?\s*\*?\s*([^\s*<>"'`]+)/i);
    if (passLabelMatch) {
        passcode = passLabelMatch[1].trim().replace(/[\.,\*\>\)"'`]+$/, '');
    } else if (zoomLink) {
        const urlPwdMatch = zoomLink.match(/[?&]pwd=([a-zA-Z0-9._~-]+)/i);

        if (urlPwdMatch) {
            try {
                passcode = decodeURIComponent(urlPwdMatch[1]);
            } catch(e) {
                passcode = urlPwdMatch[1];
            }
        }
    }

    const linkInput = document.getElementById('s_link');
    const idInput = document.getElementById('s_id');
    const passInput = document.getElementById('s_pass');

    if (linkInput && zoomLink) linkInput.value = zoomLink;
    if (idInput && meetingId) idInput.value = meetingId;
    if (passInput && passcode) passInput.value = passcode;

    const err = document.getElementById('z_error');
    if (err && zoomLink && meetingId) {
        err.innerHTML = '<span class="text-emerald-700 font-bold flex items-center gap-1"><span>✅</span> Auto-parsed link & credentials!</span>';
        err.classList.remove('hidden');
    }
}

function onZoomLinkInput(val) {
    if (!val) return;
    clientParseZoom(val);
}

async function parseZoom() {
    const textElem = document.getElementById('z_paste');
    const text = textElem ? textElem.value.trim() : '';
    if (!text) {
        alert("Please paste the Zoom invitation or link in the box first.");
        return;
    }
    
    // Immediate client extraction
    clientParseZoom(text);

    // Call server endpoint for advanced extraction
    try {
        const res = await api('/api/zoom/parse', { method: 'POST', body: { text } });
        if (res) {
            if (res.zoom_link) document.getElementById('s_link').value = res.zoom_link;
            if (res.meeting_id) document.getElementById('s_id').value = res.meeting_id;
            if (res.passcode) document.getElementById('s_pass').value = res.passcode;

            const err = document.getElementById('z_error');
            if (res.zoom_link && res.meeting_id) {
                err.innerHTML = '<span class="text-emerald-700 font-bold flex items-center gap-1"><span>✅</span> Successfully parsed! Link and credentials auto-filled.</span>';
                err.classList.remove('hidden');
                setTimeout(() => err.classList.add('hidden'), 5000);
            } else if (res.errors && res.errors.length > 0) {
                err.innerHTML = `<span class="text-amber-700 font-bold">${res.errors.join(' | ')}</span>`;
                err.classList.remove('hidden');
            }
        }
    } catch(e) {
        console.error("API parse error (client fallback used):", e);
    }
}

async function submitBatch(e) {
    e.preventDefault();
    const payload = {
        name: document.getElementById('b_name').value
    };
    const sylElem = document.getElementById('b_syllabus');
    if (sylElem) payload.syllabus = sylElem.value;
    const catElem = document.getElementById('b_class_category');
    if (catElem) payload.class_category = catElem.value;

    try {
        await api('/api/batches', { method: 'POST', body: payload });
        closeModal();
        loadBatches();
    } catch(err) {
        alert(err.detail || 'Error saving');
    }
}


async function submitSession(e) {
    e.preventDefault();
    const payload = {
        batch_id: parseInt(document.getElementById('s_batch').value),
        class_category: document.getElementById('s_class_category').value,
        topic: document.getElementById('s_topic').value,
        class_date: document.getElementById('s_date').value,
        start_time: document.getElementById('s_time').value,
        zoom_link: document.getElementById('s_link').value,
        meeting_id: document.getElementById('s_id').value,
        passcode: document.getElementById('s_pass').value
    };
    try {
        await api('/api/sessions', { method: 'POST', body: payload });
        closeModal();
        loadSessions();
    } catch(err) {
        alert(err.detail || 'Error saving');
    }
}

async function editSession(id) {
    const s = sessions.find(x => x.id === id);
    if (!s) return;
    showCreateModal();
    document.getElementById('modal-title').innerText = 'Edit Session';
    
    if (s.class_category) {
        document.getElementById('s_class_category').value = s.class_category;
    }
    updateBatchDropdownOptions(document.getElementById('s_class_category').value, 'ALL');

    document.getElementById('s_batch').value = s.batch_id;
    document.getElementById('s_topic').value = s.topic;
    document.getElementById('s_date').value = s.class_date;
    document.getElementById('s_time').value = s.start_time;
    document.getElementById('s_link').value = s.zoom_link;
    document.getElementById('s_id').value = s.meeting_id;
    document.getElementById('s_pass').value = s.passcode;
    
    document.getElementById('createForm').onsubmit = async (e) => {
        e.preventDefault();
        const payload = {
            batch_id: parseInt(document.getElementById('s_batch').value),
            class_category: document.getElementById('s_class_category').value,
            topic: document.getElementById('s_topic').value,
            class_date: document.getElementById('s_date').value,
            start_time: document.getElementById('s_time').value,
            zoom_link: document.getElementById('s_link').value,
            meeting_id: document.getElementById('s_id').value,
            passcode: document.getElementById('s_pass').value
        };
        try {
            await api(`/api/sessions/${id}`, { method: 'PUT', body: payload });
            closeModal();
            loadSessions();
        } catch(err) {
            alert(err.detail || 'Error saving');
        }
    }
}

async function editBatch(id) {
    const b = batches.find(x => x.id === id);
    if (!b) return;
    showCreateModal();
    document.getElementById('modal-title').innerText = 'Edit Batch';
    document.getElementById('b_name').value = b.name;
    if (document.getElementById('b_syllabus') && b.syllabus) {
        document.getElementById('b_syllabus').value = b.syllabus;
    }
    if (document.getElementById('b_class_category') && b.class_category) {
        document.getElementById('b_class_category').value = b.class_category;
    }

    const form = document.getElementById('createForm');
    if (form) {
        const submitBtn = form.querySelector('button[type="submit"]');
        if (submitBtn) {
            const btnContainer = document.createElement('div');
            btnContainer.className = 'flex items-center justify-between gap-3 mt-4';

            const deleteBtn = document.createElement('button');
            deleteBtn.type = 'button';
            deleteBtn.className = 'px-4 py-2.5 rounded-xl font-bold text-xs text-red-600 hover:text-red-800 bg-red-50 hover:bg-red-100 border border-red-200 transition-colors';
            deleteBtn.innerText = 'Delete Batch';
            deleteBtn.onclick = () => deleteBatch(id, b.name);

            submitBtn.innerText = 'Save Changes';
            submitBtn.className = 'flex-1 bg-amber-400 hover:bg-amber-500 text-slate-950 font-bold py-2.5 rounded-xl shadow-sm transition-all text-xs';

            submitBtn.parentNode.insertBefore(btnContainer, submitBtn);
            btnContainer.appendChild(deleteBtn);
            btnContainer.appendChild(submitBtn);
        }

        form.onsubmit = async (e) => {
            e.preventDefault();
            const payload = {
                name: document.getElementById('b_name').value
            };
            const sylElem = document.getElementById('b_syllabus');
            if (sylElem) payload.syllabus = sylElem.value;
            const catElem = document.getElementById('b_class_category');
            if (catElem) payload.class_category = catElem.value;

            try {
                await api(`/api/batches/${id}`, { method: 'PUT', body: payload });
                closeModal();
                loadBatches();
            } catch(err) {
                alert(err.detail || 'Error saving');
            }
        };
    }
}

async function deleteBatch(id, batchName = '') {
    const b = batches.find(x => x.id === id);
    const name = batchName || (b ? b.name : `Batch #${id}`);
    if (!confirm(`Are you sure you want to delete batch "${name}"?`)) {
        return;
    }
    try {
        await api(`/api/batches/${id}`, { method: 'DELETE' });
        closeModal();
        loadBatches();
    } catch(err) {
        if (err && err.detail && err.detail.includes('associated session')) {
            if (confirm(`${err.detail}\n\nDo you want to permanently delete this batch and all its sessions?`)) {
                try {
                    await api(`/api/batches/${id}?force=true`, { method: 'DELETE' });
                    closeModal();
                    loadBatches();
                } catch(e) {
                    alert(e.detail || 'Error deleting batch');
                }
            }
        } else {
            alert(err.detail || 'Error deleting batch');
        }
    }
}

async function deleteSession(id) {
    if(confirm('Are you sure you want to delete this session?')) {
        await api(`/api/sessions/${id}`, { method: 'DELETE' });
        loadSessions();
    }
}
