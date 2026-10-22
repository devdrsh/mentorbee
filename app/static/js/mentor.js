let currentSyllabus = 'CBSE';
let currentTimeTab = 'today';
let mentorToken = localStorage.getItem('mentor_token');
let mentorName = localStorage.getItem('mentor_name') || 'Staff';
let mentorClass = 'ALL'; // Universal access: every mentor sees all sessions
let currentClassFilter = ''; // Empty string = all classes
let searchQuery = '';
let loadedSessionsCache = [];
let socket = null;
let toastTimeout = null;

document.addEventListener('DOMContentLoaded', () => {
    // Auth Check
    if (!mentorToken) {
        window.location.href = '/mentor/login';
        return;
    }

    // Populate Header Info
    const nameEl = document.getElementById('header-mentor-name');
    const classEl = document.getElementById('header-mentor-class');
    if (nameEl) nameEl.textContent = mentorName;
    if (classEl) classEl.textContent = 'ALL CLASSES';

    // Setup Grade chips for all classes
    setupGradeFilterChips();

    loadClasses();
    initWebSocket();
    updateBadgeCounts();
    
    // Auto-refresh every 4 seconds for instant live updates across all mentor devices
    setInterval(() => {
        loadClasses(true);
        updateBadgeCounts();
    }, 4000);
});

function logoutMentor() {
    localStorage.removeItem('mentor_token');
    localStorage.removeItem('mentor_name');
    localStorage.removeItem('mentor_class');
    window.location.href = '/mentor/login';
}

function handleSearch(val) {
    searchQuery = (val || '').trim().toLowerCase();
    const clearBtn = document.getElementById('search-clear-btn');
    if (clearBtn) {
        if (searchQuery) {
            clearBtn.classList.remove('hidden');
        } else {
            clearBtn.classList.add('hidden');
        }
    }
    renderFilteredSessions();
}

function clearSearch() {
    const input = document.getElementById('mentor-search-input');
    if (input) input.value = '';
    searchQuery = '';
    const clearBtn = document.getElementById('search-clear-btn');
    if (clearBtn) clearBtn.classList.add('hidden');
    renderFilteredSessions();
}

function setupGradeFilterChips() {
    const chips = [
        { label: 'All Classes', value: '' },
        { label: '8th', value: '8TH' },
        { label: '9th', value: '9TH' },
        { label: '10th', value: '10TH' },
        { label: '11th Sci', value: '11TH SCI' },
        { label: '11th Com', value: '11TH COM' },
        { label: '12th Sci', value: '12TH SCI' },
        { label: '12th Com', value: '12TH COM' }
    ];

    chips.forEach(chip => {
        const chipId = chip.value ? `chip-${chip.value.replace(/\s+/g, '-')}` : 'chip-all';
        const el = document.getElementById(chipId);
        if (el) {
            if (currentClassFilter === chip.value) {
                el.className = 'chip-active px-3 py-1.5 rounded-xl border transition-all flex-shrink-0';
            } else {
                el.className = 'chip-inactive px-3 py-1.5 rounded-xl border transition-all flex-shrink-0';
            }
        }
    });
}

function switchSyllabus(syllabus) {
    if (currentSyllabus === syllabus) return;
    currentSyllabus = syllabus;
    
    const tabCbse = document.getElementById('tab-syllabus-cbse');
    const tabState = document.getElementById('tab-syllabus-state');
    const tabExamKiller = document.getElementById('tab-syllabus-exam-killer');
    const indicator = document.getElementById('active-syllabus-indicator');

    const inactiveClass = 'syllabus-tab-inactive py-2.5 sm:py-3 px-2 sm:px-4 rounded-xl sm:rounded-2xl font-extrabold text-xs sm:text-base tracking-tight transition-all duration-200 flex items-center justify-center gap-1.5 border touch-manipulation';
    const activeClass = 'syllabus-tab-active py-2.5 sm:py-3 px-2 sm:px-4 rounded-xl sm:rounded-2xl font-extrabold text-xs sm:text-base tracking-tight transition-all duration-200 flex items-center justify-center gap-1.5 border touch-manipulation';
    const activeExamClass = 'syllabus-tab-active-exam py-2.5 sm:py-3 px-2 sm:px-4 rounded-xl sm:rounded-2xl font-extrabold text-xs sm:text-base tracking-tight transition-all duration-200 flex items-center justify-center gap-1.5 border touch-manipulation';

    if (tabCbse) tabCbse.className = inactiveClass;
    if (tabState) tabState.className = inactiveClass;
    if (tabExamKiller) tabExamKiller.className = inactiveClass;
    
    if (syllabus === 'CBSE') {
        if (tabCbse) tabCbse.className = activeClass;
        if (indicator) {
            indicator.textContent = 'CBSE Syllabus';
            indicator.className = 'text-[11px] font-extrabold uppercase px-2.5 py-1 rounded-full bg-blue-50 border border-blue-200 text-blue-900 shadow-sm hidden sm:inline-block';
        }
    } else if (syllabus === 'EXAM KILLER') {
        if (tabExamKiller) tabExamKiller.className = activeExamClass;
        if (indicator) {
            indicator.textContent = '⚡ EXAM KILLER SECTION';
            indicator.className = 'text-[11px] font-extrabold uppercase px-2.5 py-1 rounded-full bg-rose-50 border border-rose-300 text-rose-900 shadow-sm hidden sm:inline-block';
        }
    } else {
        if (tabState) tabState.className = activeClass;
        if (indicator) {
            indicator.textContent = 'STATE Syllabus';
            indicator.className = 'text-[11px] font-extrabold uppercase px-2.5 py-1 rounded-full bg-emerald-50 border border-emerald-200 text-emerald-900 shadow-sm hidden sm:inline-block';
        }
    }
    loadClasses();
}

function switchTimeTab(tab) {
    if (currentTimeTab === tab) return;
    currentTimeTab = tab;
    
    const tabToday = document.getElementById('tab-time-today');
    const tabUpcoming = document.getElementById('tab-time-upcoming');
    
    if (tab === 'today') {
        tabToday.className = 'time-tab-active pb-2.5 font-bold text-sm sm:text-base tracking-tight transition-all duration-200 flex items-center gap-2';
        tabUpcoming.className = 'time-tab-inactive pb-2.5 font-bold text-sm sm:text-base tracking-tight hover:text-amber-700 transition-all duration-200 flex items-center gap-2';
    } else {
        tabToday.className = 'time-tab-inactive pb-2.5 font-bold text-sm sm:text-base tracking-tight hover:text-amber-700 transition-all duration-200 flex items-center gap-2';
        tabUpcoming.className = 'time-tab-active pb-2.5 font-bold text-sm sm:text-base tracking-tight transition-all duration-200 flex items-center gap-2';
    }
    loadClasses();
}

function switchClassFilter(classCat) {
    currentClassFilter = classCat;
    setupGradeFilterChips();
    loadClasses();
}

function formatUpdatedAt(dateStr) {
    if (!dateStr) return '';
    let isoStr = dateStr;
    if (!isoStr.endsWith('Z') && !isoStr.includes('+')) {
        isoStr += 'Z';
    }
    const d = new Date(isoStr);
    return d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', hour12: true });
}

function formatDisplayDate(dateStr) {
    if (!dateStr) return '';
    try {
        const parts = dateStr.split('-');
        if (parts.length === 3) {
            const d = new Date(parts[0], parts[1] - 1, parts[2]);
            return d.toLocaleDateString('en-US', { weekday: 'short', month: 'short', day: 'numeric' });
        }
    } catch(e) {
        console.error(e);
    }
    return dateStr;
}

async function updateBadgeCounts() {
    try {
        let cbseUrl = `/api/sessions/${currentTimeTab}?syllabus=CBSE`;
        let stateUrl = `/api/sessions/${currentTimeTab}?syllabus=STATE`;
        let examUrl = `/api/sessions/${currentTimeTab}?syllabus=EXAM%20KILLER`;
        
        if (currentClassFilter && currentClassFilter !== 'ALL') {
            cbseUrl += `&class_category=${encodeURIComponent(currentClassFilter)}`;
            stateUrl += `&class_category=${encodeURIComponent(currentClassFilter)}`;
            examUrl += `&class_category=${encodeURIComponent(currentClassFilter)}`;
        }

        const [cbseRes, stateRes, examRes] = await Promise.all([
            fetch(cbseUrl),
            fetch(stateUrl),
            fetch(examUrl)
        ]);
        const cbseData = await cbseRes.json();
        const stateData = await stateRes.json();
        const examData = await examRes.json();

        const badgeCbse = document.getElementById('badge-cbse-count');
        const badgeState = document.getElementById('badge-state-count');
        const badgeExam = document.getElementById('badge-exam-killer-count');

        if (badgeCbse) {
            if (cbseData && cbseData.length > 0) {
                badgeCbse.textContent = cbseData.length;
                badgeCbse.classList.remove('hidden');
            } else {
                badgeCbse.classList.add('hidden');
            }
        }

        if (badgeState) {
            if (stateData && stateData.length > 0) {
                badgeState.textContent = stateData.length;
                badgeState.classList.remove('hidden');
            } else {
                badgeState.classList.add('hidden');
            }
        }

        if (badgeExam) {
            if (examData && examData.length > 0) {
                badgeExam.textContent = examData.length;
                badgeExam.classList.remove('hidden');
            } else {
                badgeExam.classList.add('hidden');
            }
        }
    } catch (e) {
        console.error('Error fetching badge counts:', e);
    }
}


async function logMentorAction(action, sessionId, batchName, details = '') {
    try {
        if (!mentorToken) return;
        await fetch('/api/mentor/log-action', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${mentorToken}`
            },
            body: JSON.stringify({
                action: action,
                session_id: sessionId,
                batch_name: batchName,
                details: details
            })
        });
    } catch (err) {
        console.error('Failed to log mentor action', err);
    }
}

async function loadClasses(isBackground = false) {
    if (!isBackground) {
        document.getElementById('loader').classList.remove('hidden');
        document.getElementById('class-list').innerHTML = '';
        document.getElementById('empty-state').classList.add('hidden');
    }
    
    try {
        let url = `/api/sessions/${currentTimeTab}?syllabus=${currentSyllabus}`;
        if (currentClassFilter && currentClassFilter !== 'ALL') {
            url += `&class_category=${encodeURIComponent(currentClassFilter)}`;
        }
        
        const res = await fetch(url);
        const classes = await res.json();
        
        document.getElementById('loader').classList.add('hidden');
        loadedSessionsCache = Array.isArray(classes) ? classes : [];
        
        renderFilteredSessions();
    } catch(err) {
        console.error('Error loading classes:', err);
    }
}

function escapeHtml(str) {
    if (!str) return '';
    return str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;').replace(/'/g, '&#039;');
}

function renderFilteredSessions() {
    const list = document.getElementById('class-list');
    const emptyState = document.getElementById('empty-state');
    const emptyTitle = document.getElementById('empty-title');
    const emptyDesc = document.getElementById('empty-desc');
    
    // Apply client-side search query
    let filtered = loadedSessionsCache;
    if (searchQuery) {
        filtered = loadedSessionsCache.filter(cls => {
            const batchName = (cls.batch ? cls.batch.name : '').toLowerCase();
            const topic = (cls.topic || '').toLowerCase();
            const startTime = (cls.start_time || '').toLowerCase();
            const category = (cls.class_category || (cls.batch ? cls.batch.class_category : '') || (cls.batch ? cls.batch.class_number : '') || '').toLowerCase();
            return batchName.includes(searchQuery) || topic.includes(searchQuery) || startTime.includes(searchQuery) || category.includes(searchQuery);
        });
    }

    // Update count badge for active time tab
    const countBadge = document.getElementById(currentTimeTab === 'today' ? 'today-count' : 'upcoming-count');
    if (countBadge) {
        if (loadedSessionsCache.length > 0) {
            countBadge.textContent = loadedSessionsCache.length;
            countBadge.classList.remove('hidden');
        } else {
            countBadge.classList.add('hidden');
        }
    }

    if (filtered.length === 0) {
        list.innerHTML = '';
        if (emptyTitle && emptyDesc) {
            if (searchQuery) {
                emptyTitle.textContent = "No matching classes found";
                emptyDesc.innerHTML = `No ${currentSyllabus} sessions match "<b>${escapeHtml(searchQuery)}</b>". <br><button onclick="clearSearch()" class="mt-2 inline-flex items-center gap-1 text-xs font-bold text-amber-700 bg-amber-50 hover:bg-amber-100 border border-amber-300 px-3 py-1.5 rounded-xl transition-all">Clear Search Query</button>`;
            } else {
                const filterNote = currentClassFilter ? ` for Class ${currentClassFilter}` : '';
                emptyTitle.textContent = `No ${currentSyllabus} classes ${currentTimeTab === 'today' ? 'today' : 'upcoming'}`;
                emptyDesc.textContent = `There are no scheduled ${currentSyllabus}${filterNote} sessions in this list right now.`;
            }
        }
        emptyState.classList.remove('hidden');
        return;
    }

    emptyState.classList.add('hidden');
    list.innerHTML = '';

    filtered.forEach((cls, index) => {
        const updatedAt = formatUpdatedAt(cls.updated_at);
        const card = document.createElement('div');
        card.className = "session-card bg-white p-4 sm:p-5 rounded-2xl sm:rounded-3xl border border-amber-200/70 shadow-sm relative overflow-hidden";
        
        // Format time in 12-hour IST format
        let displayTime = cls.start_time;
        if (cls.start_time && cls.start_time.includes(':')) {
            const timeTokens = cls.start_time.split(':');
            let h = parseInt(timeTokens[0]);
            let m = timeTokens[1];
            let ampm = h >= 12 ? 'PM' : 'AM';
            h = h % 12 || 12;
            displayTime = `${h.toString().padStart(2, '0')}:${m} ${ampm} IST`;
        }

        const formattedDate = currentTimeTab === 'upcoming' ? formatDisplayDate(cls.class_date) : '';
        const btnId = `copy-btn-${cls.id || index}`;
        const syllabus = cls.batch && cls.batch.syllabus ? cls.batch.syllabus : currentSyllabus;
        const isCbse = syllabus === 'CBSE';
        const isExamKiller = syllabus === 'EXAM KILLER' || (cls.batch && cls.batch.name && cls.batch.name.includes('EXAM KILLER'));

        const syllabusBadge = isCbse 
            ? `<span class="inline-flex items-center gap-1 bg-blue-50 text-blue-900 border border-blue-200 text-[10px] sm:text-[11px] font-black px-2 py-0.5 rounded-full uppercase tracking-wider">
                 <span class="w-1.5 h-1.5 rounded-full bg-blue-500"></span>CBSE
               </span>`
            : (isExamKiller
                ? `<span class="inline-flex items-center gap-1 bg-rose-50 text-rose-900 border border-rose-300 text-[10px] sm:text-[11px] font-black px-2 py-0.5 rounded-full uppercase tracking-wider">
                     <span class="w-1.5 h-1.5 rounded-full bg-rose-600 animate-pulse"></span>⚡ EXAM KILLER
                   </span>`
                : `<span class="inline-flex items-center gap-1 bg-emerald-50 text-emerald-900 border border-emerald-200 text-[10px] sm:text-[11px] font-black px-2 py-0.5 rounded-full uppercase tracking-wider">
                     <span class="w-1.5 h-1.5 rounded-full bg-emerald-500"></span>STATE
                   </span>`);


        const classCat = cls.class_category || (cls.batch ? cls.batch.class_category : '') || (cls.batch ? cls.batch.class_number : '');
        const classBadge = classCat ? `
            <span class="inline-flex items-center bg-amber-50 text-amber-900 border border-amber-200/80 text-[10px] sm:text-[11px] font-extrabold px-2 py-0.5 rounded-full uppercase">
                ${classCat}
            </span>` : '';

        const batchName = cls.batch ? cls.batch.name : 'Batch';

        card.innerHTML = `
            <!-- Top Row: Syllabus Badge, Class Badge, Batch Name and Updated Timestamp -->
            <div class="flex flex-wrap items-center justify-between gap-2 mb-2.5">
                <div class="flex items-center gap-1.5 flex-wrap">
                    ${syllabusBadge}
                    ${classBadge}
                    <span class="inline-flex items-center bg-amber-100/90 text-amber-900 border border-amber-300/50 text-[11px] sm:text-xs font-extrabold px-2.5 sm:px-3 py-0.5 rounded-full uppercase tracking-wider">
                        ${batchName}
                    </span>
                    ${formattedDate ? `
                    <span class="inline-flex items-center bg-slate-100 text-slate-700 text-[11px] sm:text-xs font-bold px-2.5 py-0.5 rounded-full">
                        ${formattedDate}
                    </span>` : ''}
                </div>
                
                ${updatedAt ? `
                <span class="text-[10px] sm:text-xs font-semibold text-slate-400 flex items-center gap-1 bg-slate-50 border border-slate-100 px-2 py-1 rounded-lg">
                    <svg class="w-3 h-3 text-amber-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                    <span>UPDATED ${updatedAt}</span>
                </span>` : ''}
            </div>

            <!-- Topic Heading -->
            <h3 class="text-lg sm:text-xl font-extrabold text-slate-900 mt-1 uppercase tracking-tight break-words">
                ${cls.topic}
            </h3>

            <!-- Time Details -->
            <div class="text-slate-600 font-semibold text-xs sm:text-sm mt-2 flex items-center gap-1.5">
                <svg class="w-4 h-4 text-amber-500 flex-shrink-0" fill="none" stroke="currentColor" stroke-width="2.2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                <span>${displayTime}</span>
            </div>

            <!-- Responsive Action Buttons -->
            <div class="mt-4 sm:mt-5 grid grid-cols-2 gap-2.5 sm:gap-3">
                <button id="${btnId}" onclick='handleCopy("${btnId}", ${JSON.stringify(cls.formatted_message || "").replace(/'/g, "&#39;")}, ${cls.id || 0}, "${batchName.replace(/"/g, "")}")' 
                    class="w-full bg-amber-400 hover:bg-amber-500 active:bg-amber-600 text-slate-950 font-bold py-2.5 sm:py-3 px-3 sm:px-4 rounded-xl sm:rounded-2xl shadow-sm hover:shadow-md transition-all flex items-center justify-center gap-1.5 sm:gap-2 text-xs sm:text-sm touch-manipulation select-none">
                    <svg class="w-4 h-4 sm:w-4.5 sm:h-4.5 flex-shrink-0" fill="none" stroke="currentColor" stroke-width="2.2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M8 5H6a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2v-1M8 5a2 2 0 002 2h2a2 2 0 002-2M8 5a2 2 0 012-2h2a2 2 0 012 2m0 0h2a2 2 0 012 2v3m2 4H10m0 0l3-3m-3 3l3 3"></path></svg>
                    <span class="btn-label truncate">Copy Message</span>
                </button>
                
                <a href="${cls.zoom_link}" target="_blank" rel="noopener noreferrer" onclick='handleJoinZoom(${cls.id || 0}, "${batchName.replace(/"/g, "")}")'
                    class="w-full bg-white border-2 border-amber-200/90 hover:border-amber-400 hover:bg-amber-50/50 active:bg-amber-100/50 text-slate-800 font-bold py-2.5 sm:py-3 px-3 sm:px-4 rounded-xl sm:rounded-2xl shadow-sm transition-all flex items-center justify-center gap-1.5 sm:gap-2 text-xs sm:text-sm touch-manipulation select-none">
                    <svg class="w-4 h-4 sm:w-4.5 sm:h-4.5 text-amber-600 flex-shrink-0" fill="currentColor" viewBox="0 0 24 24"><path d="M4.5 10.5L9 6v3h6v3H9v3l-4.5-4.5zM21 4H3a1 1 0 00-1 1v14a1 1 0 001 1h18a1 1 0 001-1V5a1 1 0 00-1-1zm-1 14H4V6h16v12z"/></svg>
                    <span class="truncate">Join Zoom</span>
                </a>
            </div>
        `;
        list.appendChild(card);
    });
}

function handleCopy(btnId, text, sessionId = 0, batchName = '') {
    if (!text) return;
    
    // Log audit trail with staff name accountability
    logMentorAction("COPY_MESSAGE", sessionId, batchName, `Copied by ${mentorName} to dispatch to ${batchName}`);

    // Copy to clipboard
    if (navigator.clipboard && window.isSecureContext) {
        navigator.clipboard.writeText(text).then(() => showFeedback(btnId)).catch(() => fallbackCopy(btnId, text));
    } else {
        fallbackCopy(btnId, text);
    }
}

function handleJoinZoom(sessionId = 0, batchName = '') {
    // Log audit trail with staff name accountability
    logMentorAction("JOIN_ZOOM", sessionId, batchName, `Zoom meeting launched by ${mentorName}`);
}

function fallbackCopy(btnId, text) {
    const textArea = document.createElement("textarea");
    textArea.value = text;
    textArea.style.position = "fixed";
    textArea.style.left = "-999999px";
    textArea.style.top = "-999999px";
    document.body.appendChild(textArea);
    textArea.focus();
    textArea.select();
    try {
        document.execCommand('copy');
        showFeedback(btnId);
    } catch (err) {
        console.error('Fallback copy failed', err);
    }
    textArea.remove();
}

function showFeedback(btnId) {
    // 1. Update button visual state
    const btn = document.getElementById(btnId);
    if (btn) {
        const label = btn.querySelector('.btn-label');
        if (label) {
            const originalText = label.textContent;
            label.textContent = "✓ Copied!";
            btn.classList.add('bg-emerald-400', 'text-slate-950');
            btn.classList.remove('bg-amber-400');
            setTimeout(() => {
                label.textContent = originalText;
                btn.classList.remove('bg-emerald-400');
                btn.classList.add('bg-amber-400');
            }, 1500);
        }
    }

    // 2. Show toast
    const toast = document.getElementById('toast');
    if (toast) {
        if (toastTimeout) clearTimeout(toastTimeout);
        toast.classList.remove('opacity-0', 'translate-y-2');
        toast.classList.add('opacity-100', 'translate-y-0');
        
        toastTimeout = setTimeout(() => {
            toast.classList.remove('opacity-100', 'translate-y-0');
            toast.classList.add('opacity-0', 'translate-y-2');
        }, 2200);
    }
}

function initWebSocket() {
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    socket = new WebSocket(`${protocol}//${window.location.host}/ws/mentor`);
    
    socket.onmessage = function(event) {
        if(event.data === 'update') {
            loadClasses(true);
            updateBadgeCounts();
        }
    };
    
    socket.onclose = function() {
        setTimeout(initWebSocket, 5000);
    };
}
