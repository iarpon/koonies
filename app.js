// Las Crónicas de Los Koonies - Interactive Campaign Portal

let activeTab = 'home';
let currentSessionId = 16;
let currentActFilter = 'all';
let currentAtlasFilter = 'all';

document.addEventListener('DOMContentLoaded', () => {
  initLucide();
  initAmbientParticles();
  initTimeline();
  renderSessionsList();
  renderSessionReader(currentSessionId);
  renderCharacters();
  renderNpcs();
  renderAtlas();
  renderMysteries();
  renderMagicItems();

  // Keyboard shortcut for search
  document.addEventListener('keydown', (e) => {
    if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
      e.preventDefault();
      openSearchModal();
    }
    if (e.key === 'Escape') {
      closeSearchModal();
      closeLightbox();
    }
  });
});

function initLucide() {
  if (window.lucide) {
    lucide.createIcons();
  }
}

// -------------------------------------------------------------
// TAB NAVIGATION
// -------------------------------------------------------------
function navigateTab(tabId) {
  activeTab = tabId;
  
  // Update Tab Content
  document.querySelectorAll('.tab-content').forEach(el => {
    el.classList.add('hidden');
    el.classList.remove('block');
  });
  const target = document.getElementById(`tab-${tabId}`);
  if (target) {
    target.classList.remove('hidden');
    target.classList.add('block');
  }

  // Update Nav Buttons
  document.querySelectorAll('.nav-btn').forEach(btn => {
    if (btn.dataset.tab === tabId) {
      btn.className = 'nav-btn px-3 py-1.5 rounded-lg text-xs font-semibold tracking-wide transition flex items-center gap-1.5 text-amber-300 bg-amber-500/10 border border-amber-500/30 shadow-sm';
    } else {
      btn.className = 'nav-btn px-3 py-1.5 rounded-lg text-xs font-semibold tracking-wide transition flex items-center gap-1.5 text-slate-300 hover:text-amber-200 hover:bg-slate-800/60';
    }
  });

  // Mobile Nav Buttons
  document.querySelectorAll('.nav-mobile-btn').forEach(btn => {
    if (btn.dataset.tab === tabId) {
      btn.className = 'nav-mobile-btn text-xs px-2 py-1 text-amber-300 font-bold';
    } else {
      btn.className = 'nav-mobile-btn text-xs px-2 py-1 text-slate-400 font-medium';
    }
  });

  window.scrollTo({ top: 0, behavior: 'smooth' });
  initLucide();
}

// -------------------------------------------------------------
// SESSIONS & TIMELINE
// -------------------------------------------------------------
function initTimeline() {
  const container = document.getElementById('timelineTrack');
  if (!container || !window.CAMPAIGN_DATA) return;

  const sessions = window.CAMPAIGN_DATA.sessions;
  container.innerHTML = '';

  sessions.forEach(s => {
    const dotBtn = document.createElement('button');
    const isActive = s.number === currentSessionId;
    dotBtn.className = `timeline-dot flex-shrink-0 flex items-center gap-2 px-3 py-1.5 rounded-xl border text-xs font-medium transition ${
      isActive 
        ? 'bg-amber-500/20 text-amber-200 border-amber-500/60 shadow-lg shadow-amber-500/20 active' 
        : 'bg-slate-900/80 text-slate-400 border-slate-700/60 hover:text-amber-300 hover:border-amber-500/40'
    }`;
    dotBtn.onclick = () => openSessionDetail(s.number);
    dotBtn.innerHTML = `
      <span class="w-2 h-2 rounded-full ${isActive ? 'bg-amber-400 animate-pulse' : 'bg-slate-500'}"></span>
      <span class="font-mono font-bold">S${s.number}</span>
      <span class="hidden xl:inline text-[11px] truncate max-w-[120px]">${s.in_game_date || s.title}</span>
    `;
    container.appendChild(dotBtn);
  });
}

function filterSessions(act) {
  currentActFilter = act;
  document.querySelectorAll('.session-filter-btn').forEach(btn => {
    if (btn.dataset.act === act) {
      btn.className = 'session-filter-btn active px-3 py-1.5 rounded-lg text-xs font-medium bg-amber-500/20 text-amber-300 border border-amber-500/40';
    } else {
      btn.className = 'session-filter-btn px-3 py-1.5 rounded-lg text-xs font-medium bg-slate-800 text-slate-300 hover:bg-slate-700';
    }
  });
  renderSessionsList();
}

function renderSessionsList() {
  const container = document.getElementById('sessionsListCol');
  if (!container || !window.CAMPAIGN_DATA) return;

  const sessions = window.CAMPAIGN_DATA.sessions;
  const filtered = currentActFilter === 'all' 
    ? sessions 
    : sessions.filter(s => s.act && s.act.startsWith(currentActFilter));

  container.innerHTML = '';

  filtered.forEach(s => {
    const isSelected = s.number === currentSessionId;
    const card = document.createElement('div');
    card.className = `p-4 rounded-xl cursor-pointer transition rpg-card border ${
      isSelected 
        ? 'border-amber-500/60 bg-amber-950/20 shadow-md shadow-amber-500/10' 
        : 'border-slate-800 hover:border-amber-500/30'
    }`;
    card.onclick = () => openSessionDetail(s.number);

    card.innerHTML = `
      <div class="flex items-start justify-between gap-2">
        <div>
          <span class="text-[10px] uppercase font-bold tracking-wider px-2 py-0.5 rounded-md ${
            isSelected ? 'bg-amber-500/20 text-amber-300 border border-amber-500/30' : 'bg-slate-800 text-slate-400'
          }">
            ${s.act || 'Crónica'}
          </span>
          <h4 class="font-cinzel font-bold text-sm text-slate-100 mt-1.5 ${isSelected ? 'text-amber-200' : ''}">
            Sesión ${s.number}: ${s.title}
          </h4>
        </div>
        <span class="text-[11px] font-mono text-slate-400 flex-shrink-0">${s.irl_date || ''}</span>
      </div>

      <p class="font-crimson text-xs text-slate-300 line-clamp-2 mt-2 leading-relaxed">
        ${s.summary}
      </p>

      <div class="flex items-center justify-between text-[11px] text-slate-400 mt-3 pt-2 border-t border-slate-800/60">
        <span class="truncate max-w-[200px] flex items-center gap-1">
          <i data-lucide="map-pin" class="w-3 h-3 text-amber-400"></i> ${s.location || 'Costa de los Naufragios'}
        </span>
        <span class="text-amber-400 font-mono">${s.xp || ''}</span>
      </div>
    `;

    container.appendChild(card);
  });

  initLucide();
}

function openSessionDetail(sessionNum) {
  currentSessionId = sessionNum;
  initTimeline();
  renderSessionsList();
  renderSessionReader(sessionNum);

  // If on mobile, scroll reader into view
  if (window.innerWidth < 1024) {
    const reader = document.getElementById('sessionReaderCol');
    if (reader) reader.scrollIntoView({ behavior: 'smooth' });
  }
}

function renderSessionReader(sessionNum) {
  const container = document.getElementById('sessionReaderCol');
  if (!container || !window.CAMPAIGN_DATA) return;

  const session = window.CAMPAIGN_DATA.sessions.find(s => s.number === sessionNum);
  if (!session) return;

  // Format full text nicely
  let formattedHtml = session.blocks.map(b => {
    let text = b.text;
    
    // Markdown-like parse
    text = text.replace(/# (.*)/g, '<h1 class="font-cinzel text-xl text-amber-200 font-bold mt-4 mb-2">$1</h1>');
    text = text.replace(/## (.*)/g, '<h2 class="font-cinzel text-lg text-slate-200 font-semibold mt-4 mb-2">$1</h2>');
    text = text.replace(/### (.*)/g, '<h3 class="font-cinzel text-base text-amber-300 font-semibold mt-3 mb-1">$1</h3>');
    text = text.replace(/\*\*(.*?)\*\*/g, '<strong class="text-white font-semibold">$1</strong>');
    text = text.replace(/\*(.*?)\*/g, '<em class="text-amber-100/90 italic">$1</em>');
    text = text.replace(/==(.*?)==/g, '<mark class="bg-amber-500/20 text-amber-200 px-1 rounded">$1</mark>');
    text = text.replace(/- (.*)/g, '<li class="ml-4 list-disc text-slate-300">$1</li>');

    // Split paragraphs
    const paragraphs = text.split('\n\n').map(p => {
      if (p.startsWith('<h') || p.startsWith('<li')) return p;
      return `<p class="mb-3 leading-relaxed">${p}</p>`;
    }).join('');

    // Attach block images if any
    let imgsHtml = '';
    if (b.images && b.images.length > 0) {
      imgsHtml = `<div class="grid grid-cols-1 sm:grid-cols-2 gap-3 my-4">` + 
        b.images.map(img => `
          <div class="relative group cursor-pointer overflow-hidden rounded-xl border border-amber-500/30" onclick="openLightbox('${img}', 'Ilustración de la Sesión ${session.number}')">
            <img src="${img}" alt="Ilustración" class="w-full h-44 object-cover group-hover:scale-105 transition duration-300">
            <div class="absolute inset-0 bg-black/40 opacity-0 group-hover:opacity-100 transition flex items-center justify-center text-xs text-amber-300 font-medium">
              <i data-lucide="zoom-in" class="w-4 h-4 mr-1"></i> Ampliar Ilustración
            </div>
          </div>
        `).join('') + `</div>`;
    }

    return paragraphs + imgsHtml;
  }).join('');

  container.innerHTML = `
    <!-- Reader Header -->
    <div class="border-b border-amber-500/20 pb-5 mb-6">
      <div class="flex items-center justify-between gap-2 text-xs text-slate-400 mb-2">
        <span class="px-2.5 py-1 rounded-full bg-amber-500/10 text-amber-300 border border-amber-500/30 font-semibold uppercase tracking-wider">
          ${session.act || 'Crónica de Campaña'}
        </span>
        <span class="font-mono text-slate-300">Sesión Real: ${session.irl_date || 'N/A'}</span>
      </div>

      <h2 class="font-cinzel text-2xl sm:text-3xl font-bold text-amber-100 leading-tight">
        Sesión ${session.number}: ${session.title}
      </h2>

      <div class="flex flex-wrap items-center gap-4 text-xs text-slate-300 mt-3 pt-3 border-t border-slate-800">
        <div class="flex items-center gap-1.5 text-amber-400 font-medium">
          <i data-lucide="calendar" class="w-3.5 h-3.5"></i> ${session.in_game_date || 'Fecha en el mundo no registrada'}
        </div>
        <div class="flex items-center gap-1.5 text-slate-300">
          <i data-lucide="map-pin" class="w-3.5 h-3.5 text-amber-500"></i> ${session.location || 'Costa de los Naufragios'}
        </div>
        <div class="flex items-center gap-1.5 text-emerald-400 font-mono">
          <i data-lucide="award" class="w-3.5 h-3.5"></i> ${session.xp || '200 PX'}
        </div>
      </div>
    </div>

    <!-- Reader Prose Body -->
    <div class="prose-rpg">
      ${formattedHtml}
    </div>

    <!-- Reader Footer Navigation -->
    <div class="mt-8 pt-5 border-t border-slate-800 flex items-center justify-between">
      ${session.number > 1 
        ? `<button onclick="openSessionDetail(${session.number - 1})" class="px-4 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-xs font-semibold text-slate-200 transition flex items-center gap-1.5">
             <i data-lucide="chevron-left" class="w-4 h-4"></i> Sesión Anterior
           </button>` 
        : `<div></div>`}

      ${session.number < window.CAMPAIGN_DATA.sessions.length 
        ? `<button onclick="openSessionDetail(${session.number + 1})" class="px-4 py-2 rounded-xl bg-amber-600 hover:bg-amber-500 text-xs font-bold text-slate-950 transition flex items-center gap-1.5">
             Siguiente Sesión <i data-lucide="chevron-right" class="w-4 h-4"></i>
           </button>` 
        : `<div></div>`}
    </div>
  `;

  initLucide();
}

// -------------------------------------------------------------
// CHARACTERS (LOS KOONIES)
// -------------------------------------------------------------
function renderCharacters() {
  const container = document.getElementById('charactersGrid');
  if (!container || !window.CAMPAIGN_DATA) return;

  container.innerHTML = '';
  const characters = window.CAMPAIGN_DATA.characters;

  characters.forEach(c => {
    const card = document.createElement('div');
    card.className = 'rpg-card rounded-2xl overflow-hidden border flex flex-col justify-between transition duration-300 group';
    card.style.borderColor = `${c.accent}40`;

    card.innerHTML = `
      <!-- Character Image Header -->
      <div class="relative h-56 w-full overflow-hidden bg-slate-950">
        <img src="${c.primary_image}" alt="${c.name}" class="w-full h-full object-cover group-hover:scale-105 transition duration-500">
        <div class="absolute inset-0 bg-gradient-to-t from-[#12161f] via-[#12161f]/40 to-transparent"></div>
        
        <div class="absolute top-3 right-3 px-2.5 py-1 rounded-full bg-black/60 backdrop-blur-md text-xs font-semibold uppercase tracking-wider flex items-center gap-1" style="color: ${c.accent}; border: 1px solid ${c.accent}50;">
          <i data-lucide="${c.icon || 'shield'}" class="w-3.5 h-3.5"></i> ${c.role}
        </div>

        <div class="absolute bottom-3 left-4 right-4">
          <h3 class="font-cinzel text-xl font-bold text-white tracking-wide">${c.name}</h3>
          <p class="text-xs font-medium text-amber-200">${c.title}</p>
        </div>
      </div>

      <!-- Character Info Body -->
      <div class="p-5 space-y-4 flex-1 flex flex-col justify-between">
        <div class="space-y-3">
          <blockquote class="font-crimson text-sm italic text-slate-300 border-l-2 pl-3 py-0.5" style="border-color: ${c.accent};">
            "${c.quote}"
          </blockquote>

          <p class="font-crimson text-xs text-slate-300 leading-relaxed">
            ${c.archetype}
          </p>

          ${c.curse_status ? `
            <div class="p-3 rounded-xl bg-purple-950/40 border border-purple-800/50 text-xs text-purple-200">
              <span class="font-bold flex items-center gap-1 text-purple-300"><i data-lucide="skull" class="w-3.5 h-3.5"></i> ${c.curse_status.split(':')[0]}</span>
              <p class="mt-1 text-[11px] text-purple-300/80">${c.curse_status}</p>
            </div>
          ` : ''}
        </div>

        <!-- Gallery / Lore Button -->
        <div class="pt-3 border-t border-slate-800 flex items-center justify-between">
          <span class="text-[11px] text-slate-400">${c.gallery.length} Ilustraciones</span>
          <button onclick="openCharacterModal('${c.id}')" class="text-xs font-semibold flex items-center gap-1 hover:underline" style="color: ${c.accent};">
            Ver Ficha Completa <i data-lucide="arrow-right" class="w-3.5 h-3.5"></i>
          </button>
        </div>
      </div>
    `;

    container.appendChild(card);
  });

  initLucide();
}

function openCharacterModal(charId) {
  const character = window.CAMPAIGN_DATA.characters.find(c => c.id === charId);
  if (!character) return;

  const modalHtml = `
    <div id="charDetailModal" class="fixed inset-0 z-50 flex items-center justify-center bg-black/85 backdrop-blur-md p-4" onclick="closeCharacterModal()">
      <div class="rpg-card max-w-3xl w-full max-h-[90vh] overflow-y-auto rounded-2xl border p-6 lg:p-8 space-y-6" style="border-color: ${character.accent}60;" onclick="event.stopPropagation()">
        
        <div class="flex items-start justify-between gap-4 border-b border-slate-800 pb-4">
          <div class="flex items-center gap-4">
            <img src="${character.primary_image}" class="w-16 h-16 rounded-2xl object-cover border" style="border-color: ${character.accent};">
            <div>
              <h3 class="font-cinzel text-2xl font-bold text-white">${character.name}</h3>
              <p class="text-xs font-medium text-amber-200">${character.title} • ${character.role}</p>
            </div>
          </div>
          <button onclick="closeCharacterModal()" class="text-slate-400 hover:text-white"><i data-lucide="x" class="w-6 h-6"></i></button>
        </div>

        <div class="space-y-4">
          <blockquote class="font-crimson text-base italic text-slate-200 border-l-3 pl-4 py-1" style="border-color: ${character.accent};">
            "${character.quote}"
          </blockquote>

          <div class="prose-rpg text-sm space-y-3">
            <h4 class="font-cinzel text-base font-bold text-amber-300">Notas de Campaña y Trasfondo</h4>
            <div class="text-slate-300 leading-relaxed whitespace-pre-line">${character.full_lore}</div>
          </div>

          ${character.gallery && character.gallery.length > 1 ? `
            <div>
              <h4 class="font-cinzel text-xs font-bold text-slate-400 uppercase tracking-wider mb-2">Galería de Ilustraciones</h4>
              <div class="grid grid-cols-2 sm:grid-cols-4 gap-2">
                ${character.gallery.map(img => `
                  <img src="${img}" class="h-24 w-full object-cover rounded-lg border border-slate-700 cursor-pointer hover:scale-105 transition" onclick="openLightbox('${img}', '${character.name}')">
                `).join('')}
              </div>
            </div>
          ` : ''}
        </div>

      </div>
    </div>
  `;

  document.body.insertAdjacentHTML('beforeend', modalHtml);
  initLucide();
}

function closeCharacterModal() {
  const modal = document.getElementById('charDetailModal');
  if (modal) modal.remove();
}

// -------------------------------------------------------------
// NPCS (DRAMATIS PERSONAE)
// -------------------------------------------------------------
function renderNpcs() {
  const container = document.getElementById('npcsGrid');
  if (!container || !window.CAMPAIGN_DATA) return;

  const npcs = window.CAMPAIGN_DATA.npcs;
  const search = document.getElementById('npcSearchInput')?.value.toLowerCase() || '';
  const locFilter = document.getElementById('npcLocationFilter')?.value || 'all';

  const filtered = npcs.filter(n => {
    const matchesSearch = !search || 
      n.name.toLowerCase().includes(search) || 
      n.nickname.toLowerCase().includes(search) || 
      n.role.toLowerCase().includes(search) ||
      n.notes.toLowerCase().includes(search);

    const matchesLoc = locFilter === 'all' || 
      (locFilter === 'Prófugo' && n.status.includes('busca')) ||
      n.location.includes(locFilter);

    return matchesSearch && matchesLoc;
  });

  container.innerHTML = '';

  filtered.forEach(n => {
    const card = document.createElement('div');
    card.className = 'rpg-card p-5 rounded-2xl border border-slate-800 hover:border-amber-500/30 transition flex flex-col justify-between space-y-4';

    let attitudeBadge = 'bg-slate-800 text-slate-300';
    if (n.attitude.toLowerCase().includes('aliad') || n.attitude.toLowerCase().includes('amig') || n.attitude.toLowerCase().includes('favorable')) {
      attitudeBadge = 'bg-emerald-500/10 text-emerald-300 border border-emerald-500/30';
    } else if (n.attitude.toLowerCase().includes('hostil') || n.attitude.toLowerCase().includes('traidor') || n.attitude.toLowerCase().includes('enemigo')) {
      attitudeBadge = 'bg-rose-500/10 text-rose-300 border border-rose-500/30';
    } else {
      attitudeBadge = 'bg-amber-500/10 text-amber-300 border border-amber-500/30';
    }

    card.innerHTML = `
      <div class="flex items-start gap-3.5">
        <img src="${n.image}" alt="${n.name}" class="w-16 h-16 rounded-xl object-cover border border-amber-500/30 cursor-pointer flex-shrink-0" onclick="openLightbox('${n.image}', '${n.name}')">
        <div class="flex-1 min-w-0">
          <div class="flex items-center justify-between gap-1">
            <span class="text-[10px] uppercase font-bold px-2 py-0.5 rounded ${attitudeBadge}">
              ${n.status || 'Estado Desconocido'}
            </span>
          </div>
          <h4 class="font-cinzel text-base font-bold text-white truncate mt-1">${n.name}</h4>
          <p class="text-xs text-amber-300/90 italic font-crimson">${n.nickname || n.role}</p>
        </div>
      </div>

      <div class="space-y-2 text-xs text-slate-300 font-crimson text-sm leading-relaxed">
        <p><strong>Rol:</strong> ${n.role}</p>
        <p><strong>Ubicación:</strong> ${n.location}</p>
        <p class="text-slate-400 bg-slate-900/40 p-2.5 rounded-lg border border-slate-800 text-xs">
          ${n.notes}
        </p>
      </div>

      <div class="pt-2 border-t border-slate-800 text-[11px] text-slate-400 flex items-center justify-between">
        <span>${n.faction}</span>
        <span class="italic text-amber-400">${n.attitude}</span>
      </div>
    `;

    container.appendChild(card);
  });

  initLucide();
}

function filterNpcs() {
  renderNpcs();
}

// -------------------------------------------------------------
// ATLAS & MAPS
// -------------------------------------------------------------
function filterAtlas(type) {
  currentAtlasFilter = type;
  document.querySelectorAll('.atlas-filter-btn').forEach(btn => {
    if (btn.dataset.type === type) {
      btn.className = 'atlas-filter-btn active px-3 py-1.5 rounded-lg text-xs font-medium bg-amber-500/20 text-amber-300 border border-amber-500/40';
    } else {
      btn.className = 'atlas-filter-btn px-3 py-1.5 rounded-lg text-xs font-medium bg-slate-800 text-slate-300 hover:bg-slate-700';
    }
  });
  renderAtlas();
}

function renderAtlas() {
  const container = document.getElementById('atlasGrid');
  if (!container || !window.CAMPAIGN_DATA) return;

  const atlas = window.CAMPAIGN_DATA.atlas;
  const filtered = currentAtlasFilter === 'all' 
    ? atlas 
    : atlas.filter(item => item.type === currentAtlasFilter);

  container.innerHTML = '';

  filtered.forEach(item => {
    const card = document.createElement('div');
    card.className = 'rpg-card rounded-2xl overflow-hidden border border-slate-800 hover:border-amber-500/40 transition group cursor-pointer';
    card.onclick = () => openLightbox(item.path, item.title);

    card.innerHTML = `
      <div class="relative h-48 w-full bg-slate-950 overflow-hidden">
        <img src="${item.path}" alt="${item.title}" class="w-full h-full object-cover group-hover:scale-105 transition duration-500">
        <div class="absolute inset-0 bg-black/40 opacity-0 group-hover:opacity-100 transition flex items-center justify-center text-xs text-amber-200 font-semibold gap-1.5">
          <i data-lucide="maximize-2" class="w-4 h-4"></i> Examinar Detalle
        </div>
        <div class="absolute top-2 left-2 px-2 py-0.5 rounded bg-black/70 backdrop-blur-md text-[10px] font-bold text-amber-300 uppercase">
          ${item.type}
        </div>
      </div>
      <div class="p-4 space-y-1">
        <h4 class="font-cinzel text-sm font-bold text-white">${item.title}</h4>
        <p class="font-crimson text-xs text-slate-400 line-clamp-2">${item.description}</p>
      </div>
    `;

    container.appendChild(card);
  });

  initLucide();
}

// -------------------------------------------------------------
// MYSTERIES (CABOS SUELTOS)
// -------------------------------------------------------------
function renderMysteries() {
  const container = document.getElementById('mysteriesGrid');
  if (!container || !window.CAMPAIGN_DATA) return;

  const mysteries = window.CAMPAIGN_DATA.mysteries;
  container.innerHTML = '';

  mysteries.forEach(m => {
    const card = document.createElement('div');
    card.className = 'rpg-card p-6 rounded-2xl border border-amber-500/20 space-y-4';

    let priorityBadge = 'bg-slate-800 text-slate-300';
    if (m.priority === 'Alta') priorityBadge = 'bg-rose-500/20 text-rose-300 border border-rose-500/40';
    else if (m.priority === 'Media') priorityBadge = 'bg-amber-500/20 text-amber-300 border border-amber-500/40';

    card.innerHTML = `
      <div class="flex items-start justify-between gap-3">
        <div class="space-y-1">
          <div class="flex items-center gap-2">
            <span class="text-[10px] font-bold uppercase px-2 py-0.5 rounded ${priorityBadge}">
              Prioridad ${m.priority}
            </span>
            <span class="text-xs text-purple-300 font-mono">${m.category}</span>
          </div>
          <h3 class="font-cinzel text-lg font-bold text-amber-100">${m.title}</h3>
        </div>
        <span class="text-xs text-slate-400 font-semibold px-2.5 py-1 rounded-full bg-slate-900 border border-slate-800">
          ${m.status}
        </span>
      </div>

      <p class="font-crimson text-slate-300 text-sm leading-relaxed">
        ${m.description}
      </p>

      <div class="space-y-1.5 pt-2 border-t border-slate-800/80">
        <p class="text-[11px] font-bold text-slate-400 uppercase tracking-wider font-cinzel">Pistas y Hechos Conocidos:</p>
        <ul class="space-y-1">
          ${m.clues.map(c => `
            <li class="text-xs text-slate-300 flex items-start gap-2">
              <span class="text-amber-400 mt-1">•</span>
              <span>${c}</span>
            </li>
          `).join('')}
        </ul>
      </div>
    `;

    container.appendChild(card);
  });

  initLucide();
}

// -------------------------------------------------------------
// MAGIC ITEMS & TREASURY
// -------------------------------------------------------------
function renderMagicItems() {
  const container = document.getElementById('magicItemsGrid');
  if (!container || !window.CAMPAIGN_DATA) return;

  const items = window.CAMPAIGN_DATA.treasury.magic_items;
  container.innerHTML = '';

  items.forEach(item => {
    const card = document.createElement('div');
    card.className = 'p-4 rounded-xl bg-slate-900/60 border border-purple-500/20 space-y-1.5';
    card.innerHTML = `
      <div class="flex items-center justify-between">
        <h4 class="font-cinzel font-bold text-sm text-purple-200">${item.name}</h4>
        <span class="text-[10px] px-2 py-0.5 rounded bg-purple-950/60 text-purple-300 border border-purple-800/40">${item.holder}</span>
      </div>
      <p class="font-crimson text-xs text-slate-300">${item.desc}</p>
    `;
    container.appendChild(card);
  });
}

// -------------------------------------------------------------
// LIGHTBOX MODAL
// -------------------------------------------------------------
function openLightbox(src, caption) {
  const modal = document.getElementById('lightboxModal');
  const img = document.getElementById('lightboxImg');
  const cap = document.getElementById('lightboxCaption');
  if (!modal || !img) return;

  img.src = src;
  cap.textContent = caption || '';
  modal.classList.remove('hidden');
}

function closeLightbox(event) {
  const modal = document.getElementById('lightboxModal');
  if (modal) modal.classList.add('hidden');
}

// -------------------------------------------------------------
// GLOBAL SEARCH MODAL (CMD + K)
// -------------------------------------------------------------
function openSearchModal() {
  const modal = document.getElementById('searchModal');
  const input = document.getElementById('globalSearchInput');
  if (!modal || !input) return;

  modal.classList.remove('hidden');
  input.value = '';
  input.focus();
  handleGlobalSearch();
}

function closeSearchModal() {
  const modal = document.getElementById('searchModal');
  if (modal) modal.classList.add('hidden');
}

function handleGlobalSearch() {
  const input = document.getElementById('globalSearchInput');
  const container = document.getElementById('searchResultsContainer');
  if (!input || !container || !window.CAMPAIGN_DATA) return;

  const query = input.value.trim().toLowerCase();
  if (query.length < 2) {
    container.innerHTML = '<p class="text-xs text-slate-500 text-center py-6">Escribe al menos 2 letras para buscar en toda la crónica...</p>';
    return;
  }

  const results = [];

  // Search Sessions
  window.CAMPAIGN_DATA.sessions.forEach(s => {
    if (s.title.toLowerCase().includes(query) || s.full_text.toLowerCase().includes(query)) {
      results.push({
        type: 'Sesión',
        title: `Sesión ${s.number}: ${s.title}`,
        snippet: s.summary,
        action: () => {
          navigateTab('sessions');
          openSessionDetail(s.number);
          closeSearchModal();
        }
      });
    }
  });

  // Search Characters
  window.CAMPAIGN_DATA.characters.forEach(c => {
    if (c.name.toLowerCase().includes(query) || c.full_lore.toLowerCase().includes(query)) {
      results.push({
        type: 'Protagonista',
        title: `${c.name} — ${c.title}`,
        snippet: c.quote,
        action: () => {
          navigateTab('characters');
          openCharacterModal(c.id);
          closeSearchModal();
        }
      });
    }
  });

  // Search NPCs
  window.CAMPAIGN_DATA.npcs.forEach(n => {
    if (n.name.toLowerCase().includes(query) || n.notes.toLowerCase().includes(query) || n.role.toLowerCase().includes(query)) {
      results.push({
        type: 'PNJ',
        title: `${n.name} (${n.role})`,
        snippet: n.notes,
        action: () => {
          navigateTab('npcs');
          closeSearchModal();
        }
      });
    }
  });

  // Search Mysteries
  window.CAMPAIGN_DATA.mysteries.forEach(m => {
    if (m.title.toLowerCase().includes(query) || m.description.toLowerCase().includes(query)) {
      results.push({
        type: 'Misterio',
        title: m.title,
        snippet: m.description,
        action: () => {
          navigateTab('mysteries');
          closeSearchModal();
        }
      });
    }
  });

  if (results.length === 0) {
    container.innerHTML = `<p class="text-xs text-slate-400 text-center py-6">No se encontraron resultados para "<strong>${query}</strong>".</p>`;
    return;
  }

  container.innerHTML = results.slice(0, 10).map((r, idx) => `
    <div class="p-3 rounded-xl bg-slate-900/60 hover:bg-amber-500/10 border border-slate-800 hover:border-amber-500/30 transition cursor-pointer" onclick="window._searchResults[${idx}].action()">
      <div class="flex items-center justify-between text-xs mb-1">
        <span class="font-bold text-amber-300 font-cinzel">${r.title}</span>
        <span class="text-[10px] px-2 py-0.5 rounded bg-slate-800 text-slate-400 font-mono">${r.type}</span>
      </div>
      <p class="font-crimson text-xs text-slate-400 line-clamp-2">${r.snippet}</p>
    </div>
  `).join('');

  window._searchResults = results;
}

// -------------------------------------------------------------
// AMBIENT PARTICLES (CANVAS)
// -------------------------------------------------------------
function initAmbientParticles() {
  const canvas = document.getElementById('ambientCanvas');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');

  let width = canvas.width = window.innerWidth;
  let height = canvas.height = window.innerHeight;

  window.addEventListener('resize', () => {
    width = canvas.width = window.innerWidth;
    height = canvas.height = window.innerHeight;
  });

  const particles = [];
  for (let i = 0; i < 45; i++) {
    particles.push({
      x: Math.random() * width,
      y: Math.random() * height,
      size: Math.random() * 2 + 0.8,
      speedY: Math.random() * 0.4 + 0.15,
      speedX: (Math.random() - 0.5) * 0.25,
      opacity: Math.random() * 0.5 + 0.2,
      color: Math.random() > 0.4 ? '212, 168, 83' : '168, 85, 247' // Gold or Purple
    });
  }

  function animate() {
    ctx.clearRect(0, 0, width, height);

    particles.forEach(p => {
      p.y -= p.speedY;
      p.x += p.speedX;

      if (p.y < 0) {
        p.y = height + 10;
        p.x = Math.random() * width;
      }

      ctx.beginPath();
      ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
      ctx.fillStyle = `rgba(${p.color}, ${p.opacity})`;
      ctx.shadowBlur = 8;
      ctx.shadowColor = `rgba(${p.color}, 0.8)`;
      ctx.fill();
    });

    requestAnimationFrame(animate);
  }

  animate();
}

// -------------------------------------------------------------
// AMBIENT SOUND SYNTHESIZER (WEB AUDIO API)
// -------------------------------------------------------------
let audioCtx = null;
let isAudioPlaying = false;
let noiseNode = null;
let gainNode = null;

function toggleAmbientAudio() {
  const btn = document.getElementById('ambientSoundBtn');
  const icon = document.getElementById('soundIcon');

  if (!isAudioPlaying) {
    startAmbientAudio();
    isAudioPlaying = true;
    if (btn) btn.classList.add('bg-amber-500/20', 'text-amber-300', 'border-amber-500/40');
    if (icon) icon.setAttribute('data-lucide', 'volume-2');
  } else {
    stopAmbientAudio();
    isAudioPlaying = false;
    if (btn) btn.classList.remove('bg-amber-500/20', 'text-amber-300', 'border-amber-500/40');
    if (icon) icon.setAttribute('data-lucide', 'volume-x');
  }
  initLucide();
}

function startAmbientAudio() {
  try {
    const AudioContext = window.AudioContext || window.webkitAudioContext;
    audioCtx = new AudioContext();

    // Generate procedural warm rain/fire noise
    const bufferSize = audioCtx.sampleRate * 2;
    const noiseBuffer = audioCtx.createBuffer(1, bufferSize, audioCtx.sampleRate);
    const output = noiseBuffer.getChannelData(0);

    let lastOut = 0.0;
    for (let i = 0; i < bufferSize; i++) {
      const white = Math.random() * 2 - 1;
      output[i] = (lastOut + (0.02 * white)) / 1.02; // Brown noise filter
      lastOut = output[i];
      output[i] *= 3.5;
    }

    noiseNode = audioCtx.createBufferSource();
    noiseNode.buffer = noiseBuffer;
    noiseNode.loop = true;

    // Filter to warm tone
    const filter = audioCtx.createBiquadFilter();
    filter.type = 'lowpass';
    filter.frequency.value = 450;

    gainNode = audioCtx.createGain();
    gainNode.gain.setValueAtTime(0.01, audioCtx.currentTime);
    gainNode.gain.exponentialRampToValueAtTime(0.12, audioCtx.currentTime + 2);

    noiseNode.connect(filter);
    filter.connect(gainNode);
    gainNode.connect(audioCtx.destination);

    noiseNode.start();
  } catch (e) {
    console.log("Audio Web API not supported or blocked: ", e);
  }
}

function stopAmbientAudio() {
  if (gainNode && audioCtx) {
    gainNode.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 1);
    setTimeout(() => {
      if (noiseNode) noiseNode.stop();
      if (audioCtx) audioCtx.close();
      audioCtx = null;
    }, 1000);
  }
}
