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
    
    if (tab === 'sessions') {
        document.getElementById('sessions-view').classList.remove('hidden');
        document.getElementById('tab-sessions').className = 'font-extrabold text-base sm:text-lg text-amber-700 border-b-2 border-amber-500 px-2 pb-2 transition-all whitespace-nowrap';
        loadSessions();
    } else if (tab === 'batches') {
        document.getElementById('batches-view').classList.remove('hidden');
        document.getElementById('tab-batches').className = 'font-extrabold text-base sm:text-lg text-amber-700 border-b-2 border-amber-500 px-2 pb-2 transition-all whitespace-nowrap';
        loadBatches();
    } else if (tab === 'audit-logs' && currentAdmin && currentAdmin.role === 'SUPER_ADMIN') {
        document.getElementById('audit-logs-view').classList.remove('hidden');
        if (tabAudit) {
            tabAudit.className = 'font-extrabold text-base sm:text-lg text-amber-700 border-b-2 border-amber-500 px-2 pb-2 transition-all whitespace-nowrap flex items-center gap-1.5';
        }
        loadAuditLogs();
    }
}

async function loadBatches() {
    try {
        let url = '/api/batches';
        if (currentAdmin && currentAdmin.assigned_classes && currentAdmin.assigned_classes !== 'ALL') {
            url += `?class_category=${encodeURIComponent(currentAdmin.assigned_classes)}`;
        }
        batches = await api(url);
        const tbody = document.getElementById('batches-tbody');
        tbody.innerHTML = '';
        if (batches.length === 0) {
            tbody.innerHTML = `<tr><td colspan="6" class="p-8 text-center text-slate-400">No batches available for this class scope.</td></tr>`;
            return;
        }
        batches.forEach(b => {
            const isCbse = b.syllabus === 'CBSE';
            const sylBadge = isCbse 
                ? `<span class="bg-blue-50 text-blue-800 border border-blue-200 px-2 py-0.5 rounded-full text-xs font-bold">CBSE</span>`
                : `<span class="bg-emerald-50 text-emerald-800 border border-emerald-200 px-2 py-0.5 rounded-full text-xs font-bold">STATE</span>`;

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
                    <td class="p-4 text-right">
                        <button onclick="editBatch(${b.id})" class="text-xs font-bold text-amber-700 hover:text-amber-900 bg-amber-50 hover:bg-amber-100 px-3 py-1.5 rounded-lg border border-amber-200 transition-colors">Edit</button>
                    </td>
                </tr>
            `;
        });
    } catch(e) {
        console.error(e);
    }
}

async function loadSessions() {
    try {
        let url = '/api/sessions';
        if (currentAdmin && currentAdmin.assigned_classes && currentAdmin.assigned_classes !== 'ALL') {
            url += `?class_category=${encodeURIComponent(currentAdmin.assigned_classes)}`;
        }
        sessions = await api(url);
        const tbody = document.getElementById('sessions-tbody');
        tbody.innerHTML = '';
        if (sessions.length === 0) {
            tbody.innerHTML = `<tr><td colspan="7" class="p-8 text-center text-slate-400">No sessions scheduled yet. Click "+ Create Session" above.</td></tr>`;
            return;
        }
        sessions.forEach(s => {
            const syllabus = s.batch && s.batch.syllabus ? s.batch.syllabus : '';
            const sylBadge = syllabus === 'CBSE' 
                ? `<span class="bg-blue-50 text-blue-800 border border-blue-200 px-1.5 py-0.5 rounded text-[10px] font-black mr-1">CBSE</span>`
                : (syllabus === 'STATE' ? `<span class="bg-emerald-50 text-emerald-800 border border-emerald-200 px-1.5 py-0.5 rounded text-[10px] font-black mr-1">STATE</span>` : '');

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
    } catch(e) {
        console.error(e);
    }
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
        filtered = filtered.filter(b => b.class_category === selectedCategory || b.class_number === selectedCategory);
    }
    if (selectedSyllabus && selectedSyllabus !== 'ALL') {
        filtered = filtered.filter(b => b.syllabus === selectedSyllabus);
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
    const cat = document.getElementById('s_class_category').value;
    const syl = document.getElementById('s_syllabus_filter').value;
    updateBatchDropdownOptions(cat, syl);
}

function showCreateModal() {
    const isBatchesTab = !document.getElementById('batches-view').classList.contains('hidden');
    if (isBatchesTab) {
        document.getElementById('modal-title').innerText = 'Create Batch';
        document.getElementById('modal-body').innerHTML = `
            <form id="createForm" onsubmit="submitBatch(event)">
                <div class="space-y-4">
                    <div>
                        <label class="block text-xs font-bold text-slate-700 mb-1">Batch Name</label>
                        <input required type="text" id="b_name" placeholder="e.g. 10TH CBSE MNG KL BATCH" class="w-full px-4 py-2.5 border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-amber-400">
                    </div>
                    <button type="submit" class="w-full bg-amber-400 hover:bg-amber-500 text-slate-950 font-bold py-3 rounded-xl mt-4 shadow-sm transition-all">Save Batch</button>
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
            { val: '8TH', label: '8th Class (State & CBSE)' },
            { val: '9TH', label: '9th Class (State & CBSE)' },
            { val: '10TH', label: '10th Class (State & CBSE)' },
            { val: '11TH SCI', label: '11th Science (State & CBSE)' },
            { val: '11TH COM', label: '11th Commerce (State & CBSE)' },
            { val: '12TH SCI', label: '12th Science (State & CBSE)' },
            { val: '12TH COM', label: '12th Commerce (State & CBSE)' }
        ];

        const catOptionsHtml = categories.map(c => {
            const isSelected = c.val === defaultCategory ? 'selected' : '';
            return `<option value="${c.val}" ${isSelected}>${c.label}</option>`;
        }).join('');

        document.getElementById('modal-body').innerHTML = `
            <!-- Quick Zoom Paste Auto-Fill -->
            <div class="mb-4 p-4 bg-amber-50/70 border border-amber-200/80 rounded-2xl">
                <label class="block text-xs font-extrabold text-amber-950 mb-1.5 flex items-center gap-1.5">
                    <span>⚡ Quick Zoom Paste Auto-Fill</span>
                </label>
                <textarea id="z_paste" rows="2" placeholder="Paste full Zoom meeting invitation text here to auto-parse..." class="w-full px-3 py-2 border border-amber-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-amber-400 font-mono text-xs bg-white"></textarea>
                <button type="button" onclick="parseZoom()" class="mt-2 text-xs bg-amber-400 hover:bg-amber-500 text-slate-950 px-3.5 py-1.5 rounded-lg font-bold shadow-sm transition-all">Auto Parse Link & Credentials</button>
                <div id="z_error" class="text-red-600 text-xs mt-2 hidden font-bold"></div>
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
                            <option value="ALL">All Syllabuses</option>
                            <option value="CBSE">CBSE Batches Only</option>
                            <option value="STATE">STATE Batches Only</option>
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
                        <input required type="text" id="s_topic" placeholder="e.g. 12th Physics - Ray Optics & Waves" class="w-full px-3.5 py-2.5 border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-amber-400 text-sm font-medium">
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
                        <input required type="url" id="s_link" placeholder="https://zoom.us/j/..." class="w-full px-3.5 py-2.5 border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-amber-400 text-sm font-medium">
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
        // Set today's date as default
        const todayStr = new Date().toISOString().split('T')[0];
        document.getElementById('s_date').value = todayStr;
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

async function parseZoom() {
    const text = document.getElementById('z_paste').value;
    if (!text) return;
    try {
        const res = await api('/api/zoom/parse', { method: 'POST', body: { text } });
        if (res.success) {
            document.getElementById('s_link').value = res.zoom_link || '';
            document.getElementById('s_id').value = res.meeting_id || '';
            document.getElementById('s_pass').value = res.passcode || '';
            document.getElementById('z_error').classList.add('hidden');
        } else {
            const err = document.getElementById('z_error');
            err.innerText = res.errors.join(' | ');
            err.classList.remove('hidden');
        }
    } catch(e) {
        console.error(e);
    }
}

async function submitBatch(e) {
    e.preventDefault();
    const payload = {
        name: document.getElementById('b_name').value
    };
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
    showCreateModal();
    document.getElementById('modal-title').innerText = 'Edit Batch';
    document.getElementById('b_name').value = b.name;
    document.getElementById('createForm').onsubmit = async (e) => {
        e.preventDefault();
        try {
            await api(`/api/batches/${id}`, { method: 'PUT', body: { name: document.getElementById('b_name').value } });
            closeModal();
            loadBatches();
        } catch(err) {
            alert(err.detail || 'Error saving');
        }
    }
}

async function deleteSession(id) {
    if(confirm('Are you sure you want to delete this session?')) {
        await api(`/api/sessions/${id}`, { method: 'DELETE' });
        loadSessions();
    }
}
