// Las Crónicas de Los Koonies - Interactive Campaign Portal

let activeTab = 'home';
let currentSessionId = 16;
let currentActFilter = 'all';
let currentAtlasFilter = 'all';
let mobileSessionView = 'reader'; // 'list' or 'reader'

document.addEventListener('DOMContentLoaded', () => {
  initLucide();
  initAmbientParticles();
  renderHomePartyLineup();
  initTimeline();
  renderSessionsList();
  renderSessionReader(currentSessionId);
  renderCharacters();
  renderNpcs();
  renderAtlas();
  renderMysteries();
  renderMagicItems();

  // Initialize mobile session view
  updateMobileSessionView();

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
  
  document.querySelectorAll('.tab-content').forEach(el => {
    el.classList.add('hidden');
    el.classList.remove('block');
  });
  const target = document.getElementById(`tab-${tabId}`);
  if (target) {
    target.classList.remove('hidden');
    target.classList.add('block');
  }

  // Update Nav Buttons (Desktop)
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
      btn.className = 'nav-mobile-btn flex-shrink-0 flex items-center gap-1 text-xs px-3 py-1.5 rounded-full bg-amber-500/20 text-amber-300 border border-amber-500/40 font-bold';
    } else {
      btn.className = 'nav-mobile-btn flex-shrink-0 flex items-center gap-1 text-xs px-3 py-1.5 rounded-full bg-slate-900/80 text-slate-300 border border-slate-800 font-medium';
    }
  });

  window.scrollTo({ top: 0, behavior: 'smooth' });
  initLucide();
}

// -------------------------------------------------------------
// HOME: PARTY LINEUP (THE 5 KOONIES)
// -------------------------------------------------------------
function renderHomePartyLineup() {
  const container = document.getElementById('homePartyLineup');
  if (!container || !window.CAMPAIGN_DATA) return;

  const characters = window.CAMPAIGN_DATA.characters;
  container.innerHTML = '';

  characters.forEach(c => {
    const card = document.createElement('div');
    card.className = 'rpg-card rounded-2xl overflow-hidden border p-3 flex flex-col items-center text-center cursor-pointer hover:border-amber-500/60 transition group';
    card.style.borderColor = `${c.accent}40`;
    const targetUrl = c.id === 'kazgrim' ? 'kazrim.html' : `${c.id}.html`;
    card.onclick = () => {
      window.location.href = targetUrl;
    };

    const roleTag = c.tag || c.role.split('/')[0].trim();

    card.innerHTML = `
      <div class="relative w-16 h-16 sm:w-20 sm:h-20 rounded-full overflow-hidden border-2 mb-2 shadow-lg group-hover:scale-105 transition" style="border-color: ${c.accent};">
        <img src="${c.primary_image}" alt="${c.name}" class="w-full h-full object-cover">
        <div class="absolute inset-0 bg-black/20 group-hover:opacity-0 transition"></div>
      </div>
      <h4 class="font-cinzel text-sm sm:text-base font-bold text-white group-hover:text-amber-200 transition truncate w-full">${c.name}</h4>
      <p class="text-xs font-semibold text-slate-400 truncate w-full mt-0.5">${c.title}</p>
      <span class="mt-2 text-xs font-semibold font-bold px-2.5 py-0.5 rounded-full uppercase tracking-wider" style="background-color: ${c.accent}25; color: ${c.accent}; border: 1px solid ${c.accent}40;">
        ${roleTag}
      </span>
    `;

    container.appendChild(card);
  });
}

// -------------------------------------------------------------
// SESSIONS & MOBILE RESPONSIVE NAVIGATION
// -------------------------------------------------------------
function setMobileSessionView(view) {
  mobileSessionView = view;
  updateMobileSessionView();
}

function updateMobileSessionView() {
  const listCol = document.getElementById('sessionsListCol');
  const readerCol = document.getElementById('sessionReaderCol');
  const listBtn = document.getElementById('mobileViewListBtn');
  const readerBtn = document.getElementById('mobileViewReaderBtn');
  const sessionNumLabel = document.getElementById('mobileSessionNumberLabel');

  if (sessionNumLabel) sessionNumLabel.textContent = currentSessionId;

  if (window.innerWidth >= 1024) {
    if (listCol) { listCol.classList.remove('hidden'); listCol.classList.add('block'); }
    if (readerCol) { readerCol.classList.remove('hidden'); readerCol.classList.add('block'); }
    return;
  }

  if (mobileSessionView === 'list') {
    if (listCol) { listCol.classList.remove('hidden'); listCol.classList.add('block'); }
    if (readerCol) { readerCol.classList.add('hidden'); readerCol.classList.remove('block'); }
    if (listBtn) {
      listBtn.className = 'flex-1 py-2 rounded-lg text-xs font-bold text-center transition flex items-center justify-center gap-1.5 bg-amber-500/20 text-amber-300 border border-amber-500/40';
    }
    if (readerBtn) {
      readerBtn.className = 'flex-1 py-2 rounded-lg text-xs font-bold text-center transition flex items-center justify-center gap-1.5 text-slate-400';
    }
  } else {
    if (listCol) { listCol.classList.add('hidden'); listCol.classList.remove('block'); }
    if (readerCol) { readerCol.classList.remove('hidden'); readerCol.classList.add('block'); }
    if (readerBtn) {
      readerBtn.className = 'flex-1 py-2 rounded-lg text-xs font-bold text-center transition flex items-center justify-center gap-1.5 bg-amber-500/20 text-amber-300 border border-amber-500/40';
    }
    if (listBtn) {
      listBtn.className = 'flex-1 py-2 rounded-lg text-xs font-bold text-center transition flex items-center justify-center gap-1.5 text-slate-400';
    }
  }

  initLucide();
}

window.addEventListener('resize', () => {
  updateMobileSessionView();
});

function initTimeline() {
  const container = document.getElementById('timelineTrack');
  if (!container || !window.CAMPAIGN_DATA) return;

  const sessions = window.CAMPAIGN_DATA.sessions;
  container.innerHTML = '';

  sessions.forEach(s => {
    const dotBtn = document.createElement('button');
    const isActive = s.number === currentSessionId;
    dotBtn.className = `timeline-dot flex-shrink-0 flex items-center gap-2 px-3 py-1.5 rounded-xl border text-xs font-semibold transition ${
      isActive 
        ? 'bg-amber-500/20 text-amber-200 border-amber-500/60 shadow-lg shadow-amber-500/20 active' 
        : 'bg-slate-900/80 text-slate-400 border-slate-700/60 hover:text-amber-300 hover:border-amber-500/40'
    }`;
    dotBtn.onclick = () => openSessionDetail(s.number);
    dotBtn.innerHTML = `
      <span class="w-2 h-2 rounded-full ${isActive ? 'bg-amber-400 animate-pulse' : 'bg-slate-500'}"></span>
      <span class="font-sans font-bold">S${s.number}</span>
      <span class="hidden xl:inline text-xs sm:text-sm truncate max-w-[120px]">${s.in_game_date || s.title}</span>
    `;
    container.appendChild(dotBtn);
  });
}

function filterSessions(act) {
  currentActFilter = act;
  document.querySelectorAll('.session-filter-btn').forEach(btn => {
    if (btn.dataset.act === act) {
      btn.className = 'session-filter-btn active px-3 py-1.5 rounded-lg text-xs font-medium bg-amber-500/20 text-amber-300 border border-amber-500/40 flex-shrink-0';
    } else {
      btn.className = 'session-filter-btn px-3 py-1.5 rounded-lg text-xs font-medium bg-slate-900/80 text-slate-300 hover:bg-slate-800 flex-shrink-0';
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
    card.className = `p-3.5 sm:p-4 rounded-2xl cursor-pointer transition rpg-card border flex gap-3.5 items-center ${
      isSelected 
        ? 'border-amber-500/60 bg-amber-950/20 shadow-md shadow-amber-500/10' 
        : 'border-slate-800 hover:border-amber-500/30'
    }`;
    card.onclick = () => openSessionDetail(s.number);

    card.innerHTML = `
      <!-- Thumbnail Image -->
      <div class="relative w-16 h-16 sm:w-20 sm:h-20 rounded-xl overflow-hidden bg-slate-950 flex-shrink-0 border border-amber-500/20">
        <img src="${s.cover_image}" alt="S${s.number}" class="w-full h-full object-cover">
        <div class="absolute top-1 left-1 px-1.5 py-0.5 rounded bg-black/80 text-xs font-semibold font-sans font-bold text-amber-300">
          S${s.number}
        </div>
      </div>

      <!-- Info -->
      <div class="flex-1 min-w-0 space-y-1">
        <div class="flex items-center justify-between gap-1">
          <span class="text-xs uppercase font-bold tracking-wider px-2 py-0.5 rounded-md ${
            isSelected ? 'bg-amber-500/20 text-amber-300 border border-amber-500/30' : 'bg-slate-800 text-slate-400'
          }">
            ${s.act.split(':')[0] || 'Crónica'}
          </span>
          <span class="text-xs font-semibold font-sans text-slate-400 font-medium">${s.irl_date || ''}</span>
        </div>

        <h4 class="font-cinzel font-bold text-base sm:text-lg text-slate-100 truncate ${isSelected ? 'text-amber-200' : ''}">
          ${s.title}
        </h4>

        <p class="font-crimson text-sm sm:text-base text-slate-300 line-clamp-2 leading-relaxed">
          ${s.summary}
        </p>

        <div class="flex items-center justify-between text-xs font-semibold text-slate-400 pt-1">
          <span class="truncate max-w-[150px] flex items-center gap-1">
            <i data-lucide="map-pin" class="w-3 h-3 text-amber-400"></i> ${s.location.split('—')[0]}
          </span>
          <span class="text-amber-400 font-sans font-bold">${s.xp || ''}</span>
        </div>
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

  // Switch to reader view on mobile and scroll to top
  setMobileSessionView('reader');

  const reader = document.getElementById('sessionReaderCol');
  if (reader) {
    if (window.innerWidth < 1024) {
      reader.scrollIntoView({ behavior: 'smooth' });
    } else {
      reader.scrollTop = 0;
    }
  }
}

function renderSessionReader(sessionNum) {
  const container = document.getElementById('sessionReaderCol');
  if (!container || !window.CAMPAIGN_DATA) return;

  const session = window.CAMPAIGN_DATA.sessions.find(s => s.number === sessionNum);
  if (!session) return;

  let formattedHtml = session.blocks.map(b => {
    let text = b.text;

    // Clean long hyphen strings that destroy layouts
    text = text.replace(/-{3,}/g, '<hr class="my-6 border-slate-700/60">');
    // Normalize excessive tabs
    text = text.replace(/\t+/g, ' ');

    // Special callout formatting for in-game letters/notes
    if (text.includes('Mr. Izen,') || text.includes('Harvey,') || text.includes('Señor Izen,')) {
      text = `<div class="rpg-callout-letter my-4"><i data-lucide="mail" class="w-4 h-4 text-amber-400 mb-1 inline mr-1"></i>${text}</div>`;
    } else if (text.startsWith('PX:') || text.startsWith('PX ')) {
      text = `<div class="rpg-callout-reward my-4"><strong class="font-cinzel text-emerald-300 block mb-1">⚔️ Recompensas de Experiencia:</strong>${text}</div>`;
    }

    // Markdown-like parse
    text = text.replace(/# (.*)/g, '<h1 class="font-cinzel text-2xl sm:text-3xl text-amber-200 font-bold mt-5 mb-3">$1</h1>');
    text = text.replace(/## (.*)/g, '<h2 class="font-cinzel text-xl sm:text-2xl text-slate-200 font-bold mt-5 mb-2.5">$1</h2>');
    text = text.replace(/### (.*)/g, '<h3 class="font-cinzel text-lg sm:text-xl text-amber-300 font-semibold mt-4 mb-2">$1</h3>');
    text = text.replace(/\*\*(.*?)\*\*/g, '<strong class="text-white font-semibold">$1</strong>');
    text = text.replace(/\*(.*?)\*/g, '<em class="text-amber-100/90 italic">$1</em>');
    text = text.replace(/==(.*?)==/g, '<mark class="bg-amber-500/20 text-amber-200 px-1.5 py-0.5 rounded">$1</mark>');
    text = text.replace(/- (.*)/g, '<li class="ml-4 list-disc text-slate-300 mb-1">$1</li>');

    const paragraphs = text.split('\n\n').map(p => {
      p = p.trim();
      if (!p) return '';
      if (p.startsWith('<h') || p.startsWith('<li') || p.startsWith('<hr') || p.startsWith('<div')) return p;
      return `<p class="mb-4 leading-relaxed text-slate-100 text-base sm:text-lg">${p}</p>`;
    }).join('');

    let imgsHtml = '';
    if (b.images && b.images.length > 0) {
      imgsHtml = `<div class="grid grid-cols-1 sm:grid-cols-2 gap-3.5 my-5">` + 
        b.images.map(img => `
          <div class="relative group cursor-pointer overflow-hidden rounded-xl border border-amber-500/30 shadow-lg" onclick="openLightbox('${img}', 'Ilustración de la Sesión ${session.number}')">
            <img src="${img}" alt="Ilustración" class="w-full h-48 object-cover group-hover:scale-105 transition duration-500">
            <div class="absolute inset-0 bg-black/40 opacity-0 group-hover:opacity-100 transition flex items-center justify-center text-xs text-amber-200 font-semibold gap-1">
              <i data-lucide="zoom-in" class="w-4 h-4"></i> Ampliar Ilustración
            </div>
          </div>
        `).join('') + `</div>`;
    }

    return paragraphs + imgsHtml;
  }).join('');

  container.innerHTML = `
    <!-- Mobile Fast Switcher Bar inside reader -->
    <div class="lg:hidden flex items-center justify-between p-3 bg-slate-900 border-b border-slate-800 text-xs">
      <button onclick="setMobileSessionView('list')" class="px-2.5 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-amber-300 flex items-center gap-1.5 font-bold border border-slate-700">
        <i data-lucide="list" class="w-3.5 h-3.5"></i> Ver Índice de Capítulos
      </button>
      <div class="flex items-center gap-1 text-slate-400 text-xs sm:text-sm font-sans font-semibold">
        <span>Capítulo ${session.number} de 16</span>
      </div>
    </div>

    <!-- Top Hero Banner for Session -->
    <div class="relative h-56 sm:h-72 w-full overflow-hidden bg-slate-950">
      <img src="${session.cover_image}" alt="${session.title}" class="w-full h-full object-cover">
      <div class="absolute inset-0 bg-gradient-to-t from-[#121826] via-[#121826]/75 to-black/30"></div>
      
      <div class="absolute top-3 left-3 right-3 sm:top-4 sm:left-4 sm:right-4 flex items-center justify-between">
        <span class="px-2.5 py-1 rounded-full bg-amber-500/20 backdrop-blur-md text-amber-200 border border-amber-500/40 text-xs font-semibold sm:text-xs font-bold uppercase tracking-wider">
          ${session.act || 'Crónica de Campaña'}
        </span>
        <span class="px-2.5 py-1 rounded-full bg-black/70 backdrop-blur-md font-sans font-semibold text-xs font-semibold sm:text-xs text-slate-300 border border-slate-700">
          Fecha real: ${session.irl_date || 'N/A'}
        </span>
      </div>

      <div class="absolute bottom-3 left-3 right-3 sm:bottom-4 sm:left-4 sm:right-4 space-y-1">
        <h2 class="font-cinzel text-2xl sm:text-3xl lg:text-4xl font-black text-white drop-shadow-md leading-tight">
          Sesión ${session.number}: ${session.title}
        </h2>
        <div class="flex flex-wrap items-center gap-2.5 sm:gap-3 text-xs text-amber-300/90 pt-1">
          <span class="flex items-center gap-1"><i data-lucide="calendar" class="w-3.5 h-3.5 text-amber-400"></i> ${session.in_game_date || 'Fecha en el mundo no registrada'}</span>
          <span class="flex items-center gap-1"><i data-lucide="map-pin" class="w-3.5 h-3.5 text-amber-400"></i> ${session.location || 'Costa de los Naufragios'}</span>
          <span class="flex items-center gap-1 text-emerald-400 font-sans font-bold"><i data-lucide="award" class="w-3.5 h-3.5"></i> ${session.xp || '250 PX'}</span>
        </div>
      </div>
    </div>

    <!-- Reader Prose Body -->
    <div class="p-4 sm:p-7 space-y-4">
      <div class="prose-rpg">
        ${formattedHtml}
      </div>

      <!-- Reader Footer Navigation -->
      <div class="mt-8 pt-5 border-t border-slate-800 flex items-center justify-between gap-2">
        ${session.number > 1 
          ? `<button onclick="openSessionDetail(${session.number - 1})" class="px-3.5 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-xs font-semibold text-slate-200 transition flex items-center gap-1.5 border border-slate-700">
               <i data-lucide="chevron-left" class="w-4 h-4"></i> S${session.number - 1}
             </button>` 
          : `<div></div>`}

        <button onclick="setMobileSessionView('list')" class="lg:hidden px-3 py-2 rounded-xl bg-slate-800 text-amber-300 text-xs font-bold border border-slate-700 flex items-center gap-1">
          <i data-lucide="list" class="w-3.5 h-3.5"></i> Índice
        </button>

        ${session.number < window.CAMPAIGN_DATA.sessions.length 
          ? `<button onclick="openSessionDetail(${session.number + 1})" class="px-3.5 py-2 rounded-xl bg-gradient-to-r from-amber-500 to-amber-600 hover:from-amber-400 hover:to-amber-500 text-xs font-bold text-slate-950 transition flex items-center gap-1.5 shadow-md shadow-amber-500/20">
               S${session.number + 1} <i data-lucide="chevron-right" class="w-4 h-4"></i>
             </button>` 
          : `<div></div>`}
      </div>
    </div>
  `;

  initLucide();
}

// -------------------------------------------------------------
// CHARACTERS (LOS 5 KOONIES)
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

    const s = c.stats || {};
    const saves = c.saves || {};

    const abilityGrid = `
      <div class="grid grid-cols-6 gap-1 text-center bg-black/40 p-2 rounded-xl border border-slate-800 text-xs">
        <div><span class="block text-xs sm:text-sm text-slate-400 font-bold uppercase">FUE</span><span class="font-bold text-white">${s.fue ? s.fue.split(' ')[0] : '10'}</span></div>
        <div><span class="block text-xs sm:text-sm text-slate-400 font-bold uppercase">DES</span><span class="font-bold text-white">${s.des ? s.des.split(' ')[0] : '10'}</span></div>
        <div><span class="block text-xs sm:text-sm text-slate-400 font-bold uppercase">CON</span><span class="font-bold text-white">${s.con ? s.con.split(' ')[0] : '10'}</span></div>
        <div><span class="block text-xs sm:text-sm text-slate-400 font-bold uppercase">INT</span><span class="font-bold text-amber-200">${s.int ? s.int.split(' ')[0] : '10'}</span></div>
        <div><span class="block text-xs sm:text-sm text-slate-400 font-bold uppercase">SAB</span><span class="font-bold text-white">${s.sab ? s.sab.split(' ')[0] : '10'}</span></div>
        <div><span class="block text-xs sm:text-sm text-slate-400 font-bold uppercase">CAR</span><span class="font-bold text-white">${s.car ? s.car.split(' ')[0] : '10'}</span></div>
      </div>
      <div class="grid grid-cols-3 gap-1.5 text-center text-xs sm:text-sm mt-1.5">
        <div class="p-1.5 rounded-lg bg-slate-900 border border-slate-800"><span class="text-xs text-slate-400 block uppercase">Armadura</span><span class="font-bold text-amber-300">CA ${s.ca || '10'}</span></div>
        <div class="p-1.5 rounded-lg bg-slate-900 border border-slate-800"><span class="text-xs text-slate-400 block uppercase">Vida</span><span class="font-bold text-emerald-400">${s.pg || '10'} PG</span></div>
        <div class="p-1.5 rounded-lg bg-slate-900 border border-slate-800"><span class="text-xs text-slate-400 block uppercase">GAC0</span><span class="font-bold text-slate-200">${s.thac0 ? s.thac0.split(' ')[0] : '20'}</span></div>
      </div>
    `;

    const roleTag = c.tag || c.role.split('/')[0].trim();

    card.innerHTML = `
      <!-- Character Image Header -->
      <div class="relative h-60 sm:h-64 w-full overflow-hidden bg-slate-950">
        <img src="${c.primary_image}" alt="${c.name}" class="w-full h-full object-cover group-hover:scale-105 transition duration-500">
        <div class="absolute inset-0 bg-gradient-to-t from-[#121826] via-[#121826]/40 to-transparent"></div>
        
        <div class="absolute top-3 right-3 px-3 py-1 rounded-full bg-black/80 backdrop-blur-md text-xs font-bold uppercase tracking-wider flex items-center gap-1 shadow-lg" style="color: ${c.accent}; border: 1px solid ${c.accent}50;">
          <i data-lucide="${c.icon || 'shield'}" class="w-3.5 h-3.5"></i> ${roleTag}
        </div>

        <div class="absolute bottom-3 left-4 right-4">
          <h3 class="font-cinzel text-2xl sm:text-3xl font-bold text-white tracking-wide">${c.name}</h3>
          <p class="text-xs font-medium text-amber-200">${c.title}</p>
        </div>
      </div>

      <!-- Character Info Body -->
      <div class="p-4 sm:p-5 space-y-4 flex-1 flex flex-col justify-between">
        <div class="space-y-3">
          <blockquote class="font-crimson text-base sm:text-lg italic text-slate-200 border-l-2 pl-3 py-0.5 bg-slate-900/40 rounded-r-lg" style="border-color: ${c.accent};">
            "${c.quote}"
          </blockquote>

          <div class="grid grid-cols-2 gap-2">
            ${abilityGrid}
          </div>

          <p class="font-crimson text-sm sm:text-base text-slate-200 leading-relaxed">
            ${c.archetype}
          </p>

          ${c.curse_status ? `
            <div class="p-3 rounded-xl bg-purple-950/40 border border-purple-800/50 text-xs text-purple-200">
              <span class="font-bold flex items-center gap-1 text-purple-300"><i data-lucide="skull" class="w-3.5 h-3.5"></i> ${c.curse_status.split(':')[0]}</span>
              <p class="mt-1 text-xs sm:text-sm text-purple-300/80">${c.curse_status}</p>
            </div>
          ` : ''}
        </div>

        <!-- Lore Button -->
        <div class="pt-3 border-t border-slate-800 flex items-center justify-between">
          <span class="text-xs sm:text-sm text-slate-400 font-sans font-semibold">${roleTag} oficial</span>
          <a href="${c.id === 'kazgrim' ? 'kazrim.html' : c.id + '.html'}" class="text-xs font-bold flex items-center gap-1 hover:underline" style="color: ${c.accent};">
            Ficha Completa & Lore <i data-lucide="arrow-right" class="w-3.5 h-3.5"></i>
          </a>
        </div>
      </div>
    `;

    container.appendChild(card);
  });

  initLucide();
}

function openCharacterModal(charId) {
  const url = charId === 'kazgrim' ? 'kazrim.html' : `${charId}.html`;
  window.location.href = url;
  return;
  const character = window.CAMPAIGN_DATA.characters.find(c => c.id === charId);
  if (!character) return;

  const modalHtml = `
    <div id="charDetailModal" class="fixed inset-0 z-50 flex items-center justify-center bg-black/85 backdrop-blur-md p-3 sm:p-4" onclick="closeCharacterModal()">
      <div class="rpg-card max-w-3xl w-full max-h-[90vh] overflow-y-auto rounded-2xl border p-5 sm:p-8 space-y-5" style="border-color: ${character.accent}60;" onclick="event.stopPropagation()">
        
        <div class="flex items-start justify-between gap-4 border-b border-slate-800 pb-4">
          <div class="flex items-center gap-3 sm:gap-4">
            <img src="${character.primary_image}" class="w-14 h-14 sm:w-16 sm:h-16 rounded-2xl object-cover border-2 flex-shrink-0" style="border-color: ${character.accent};">
            <div>
              <h3 class="font-cinzel text-xl sm:text-2xl font-bold text-white">${character.name}</h3>
              <p class="text-xs font-semibold text-amber-200">${character.title} • <span class="px-2 py-0.5 rounded uppercase text-xs font-semibold" style="background-color: ${character.accent}20; color: ${character.accent}; border: 1px solid ${character.accent}40;">${character.tag || character.role}</span></p>
            </div>
          </div>
          <button onclick="closeCharacterModal()" class="text-slate-400 hover:text-white p-1"><i data-lucide="x" class="w-6 h-6"></i></button>
        </div>

        <div class="space-y-4">
          <blockquote class="font-crimson text-sm sm:text-base italic text-slate-200 border-l-3 pl-4 py-1 bg-slate-900/50 rounded-r-xl" style="border-color: ${character.accent};">
            "${character.quote}"
          </blockquote>

          <!-- Full Character Sheet Tabulation -->
          <div class="space-y-3 bg-slate-900/70 p-4 rounded-2xl border border-slate-800">
            <h4 class="font-cinzel text-sm font-bold text-amber-300 uppercase tracking-wider flex items-center gap-1.5">
              <i data-lucide="shield" class="w-4 h-4 text-amber-400"></i> Ficha Oficial de AD&D 2ª Edición
            </h4>
            
            <div class="grid grid-cols-2 sm:grid-cols-4 gap-2 text-xs">
              <div class="p-2 rounded-xl bg-black/40 border border-slate-800"><span class="text-xs text-slate-400 uppercase block font-bold">Clase / Nivel</span><span class="font-bold text-slate-200">${character.stats?.clase || character.role}</span></div>
              <div class="p-2 rounded-xl bg-black/40 border border-slate-800"><span class="text-xs text-slate-400 uppercase block font-bold">Raza</span><span class="font-bold text-slate-200">${character.stats?.raza || 'Humano'}</span></div>
              <div class="p-2 rounded-xl bg-black/40 border border-slate-800"><span class="text-xs text-slate-400 uppercase block font-bold">Clase de Armadura</span><span class="font-bold text-amber-300">CA ${character.stats?.ca || '10'}</span></div>
              <div class="p-2 rounded-xl bg-black/40 border border-slate-800"><span class="text-xs text-slate-400 uppercase block font-bold">Puntos de Golpe</span><span class="font-bold text-emerald-400">${character.stats?.pg || '10'} PG</span></div>
            </div>

            <!-- 6 Abilities with breakdowns -->
            <div class="grid grid-cols-2 sm:grid-cols-3 gap-2 text-xs">
              <div class="p-2 rounded-xl bg-black/40 border border-slate-800"><span class="text-xs text-slate-400 uppercase block font-bold">Fuerza (FUE)</span><span class="font-bold text-white">${character.stats?.fue || '10'}</span></div>
              <div class="p-2 rounded-xl bg-black/40 border border-slate-800"><span class="text-xs text-slate-400 uppercase block font-bold">Destreza (DES)</span><span class="font-bold text-white">${character.stats?.des || '10'}</span></div>
              <div class="p-2 rounded-xl bg-black/40 border border-slate-800"><span class="text-xs text-slate-400 uppercase block font-bold">Constitución (CON)</span><span class="font-bold text-white">${character.stats?.con || '10'}</span></div>
              <div class="p-2 rounded-xl bg-black/40 border border-slate-800"><span class="text-xs text-slate-400 uppercase block font-bold">Inteligencia (INT)</span><span class="font-bold text-amber-200">${character.stats?.int || '10'}</span></div>
              <div class="p-2 rounded-xl bg-black/40 border border-slate-800"><span class="text-xs text-slate-400 uppercase block font-bold">Sabiduría (SAB)</span><span class="font-bold text-white">${character.stats?.sab || '10'}</span></div>
              <div class="p-2 rounded-xl bg-black/40 border border-slate-800"><span class="text-xs text-slate-400 uppercase block font-bold">Carisma (CAR)</span><span class="font-bold text-white">${character.stats?.car || '10'}</span></div>
            </div>

            <!-- Tiradas de Salvacion -->
            ${character.saves ? `
              <div class="pt-2 border-t border-slate-800">
                <span class="text-xs font-semibold text-slate-400 uppercase tracking-wider block font-bold mb-1.5 font-cinzel">Tiradas de Salvación:</span>
                <div class="grid grid-cols-5 gap-1.5 text-center text-xs">
                  <div class="p-1.5 rounded-lg bg-black/40 border border-slate-800"><span class="text-xs sm:text-sm text-slate-400 block uppercase">Veneno/Muerte</span><span class="font-bold text-emerald-300">${character.saves.paralisis_veneno_muerte || 14}</span></div>
                  <div class="p-1.5 rounded-lg bg-black/40 border border-slate-800"><span class="text-xs sm:text-sm text-slate-400 block uppercase">Varas/Varitas</span><span class="font-bold text-amber-300">${character.saves.varas_bastones_varitas || 16}</span></div>
                  <div class="p-1.5 rounded-lg bg-black/40 border border-slate-800"><span class="text-xs sm:text-sm text-slate-400 block uppercase">Petrificación</span><span class="font-bold text-amber-300">${character.saves.petrificacion_polimorfia || 15}</span></div>
                  <div class="p-1.5 rounded-lg bg-black/40 border border-slate-800"><span class="text-xs sm:text-sm text-slate-400 block uppercase">Aliento</span><span class="font-bold text-rose-300">${character.saves.armas_aliento || 17}</span></div>
                  <div class="p-1.5 rounded-lg bg-black/40 border border-slate-800"><span class="text-xs sm:text-sm text-slate-400 block uppercase">Conjuros</span><span class="font-bold text-purple-300">${character.saves.conjuros || 17}</span></div>
                </div>
              </div>
            ` : ''}
          </div>

          <div class="prose-rpg text-sm space-y-3">
            <h4 class="font-cinzel text-base font-bold text-amber-300">Notas de Campaña y Trasfondo</h4>
            <div class="text-slate-300 leading-relaxed whitespace-pre-line">${character.full_lore}</div>
          </div>
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
    card.className = 'rpg-card p-4 sm:p-5 rounded-2xl border border-slate-800 hover:border-amber-500/30 transition flex flex-col justify-between space-y-4';

    let attitudeBadge = 'bg-slate-800 text-slate-300';
    if (n.attitude.toLowerCase().includes('aliad') || n.attitude.toLowerCase().includes('amig') || n.attitude.toLowerCase().includes('favorable') || n.attitude.toLowerCase().includes('devota')) {
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
            <span class="text-xs font-semibold uppercase font-bold px-2 py-0.5 rounded ${attitudeBadge}">
              ${n.status || 'Estado Desconocido'}
            </span>
          </div>
          <h4 class="font-cinzel text-base sm:text-lg font-bold text-white truncate mt-1">${n.name}</h4>
          <p class="text-xs text-amber-300/90 italic font-crimson">${n.nickname || n.role}</p>
        </div>
      </div>

      <div class="space-y-2 text-xs text-slate-300 font-crimson text-sm leading-relaxed">
        <p><strong>Rol:</strong> ${n.role}</p>
        <p><strong>Ubicación:</strong> ${n.location}</p>
        <p class="text-slate-400 bg-slate-900/50 p-2.5 rounded-lg border border-slate-800/80 text-xs leading-relaxed">
          ${n.notes}
        </p>
      </div>

      <div class="pt-2 border-t border-slate-800 text-xs sm:text-sm text-slate-400 flex items-center justify-between">
        <span class="truncate max-w-[150px]">${n.faction}</span>
        <span class="italic text-amber-400">${n.attitude.split('/')[0]}</span>
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
// ATLAS & MAPS (5 OFFICIAL MAPS)
// -------------------------------------------------------------
function filterAtlas(type) {
  currentAtlasFilter = type;
  document.querySelectorAll('.atlas-filter-btn').forEach(btn => {
    if (btn.dataset.type === type) {
      btn.className = 'atlas-filter-btn active px-3.5 py-1.5 rounded-xl text-xs font-medium bg-amber-500/20 text-amber-300 border border-amber-500/40';
    } else {
      btn.className = 'atlas-filter-btn px-3.5 py-1.5 rounded-xl text-xs font-medium bg-slate-900/80 text-slate-300 hover:bg-slate-800';
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
        <div class="absolute top-2 left-2 px-2.5 py-0.5 rounded bg-black/75 backdrop-blur-md text-xs font-semibold font-bold text-amber-300 uppercase">
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
    card.className = 'rpg-card rounded-2xl border border-amber-500/20 overflow-hidden flex flex-col justify-between';

    let priorityBadge = 'bg-slate-800 text-slate-300';
    if (m.priority === 'Alta') priorityBadge = 'bg-rose-500/20 text-rose-300 border border-rose-500/40';
    else if (m.priority === 'Media') priorityBadge = 'bg-amber-500/20 text-amber-300 border border-amber-500/40';

    card.innerHTML = `
      ${m.image ? `
        <div class="relative h-40 w-full overflow-hidden bg-slate-950">
          <img src="${m.image}" alt="${m.title}" class="w-full h-full object-cover">
          <div class="absolute inset-0 bg-gradient-to-t from-[#121826] to-transparent"></div>
          <div class="absolute top-3 left-3">
            <span class="text-xs font-semibold font-bold uppercase px-2.5 py-1 rounded-full ${priorityBadge} backdrop-blur-md">
              Prioridad ${m.priority}
            </span>
          </div>
        </div>
      ` : ''}

      <div class="p-4 sm:p-5 space-y-4 flex-1 flex flex-col justify-between">
        <div class="space-y-2">
          <div class="flex items-center justify-between">
            <span class="text-xs text-purple-300 font-sans font-semibold">${m.category}</span>
            <span class="text-xs text-slate-300 font-semibold px-2 py-0.5 rounded-full bg-slate-900 border border-slate-800">
              ${m.status}
            </span>
          </div>
          <h3 class="font-cinzel text-lg sm:text-xl font-bold text-amber-100">${m.title}</h3>
          <p class="font-crimson text-slate-300 text-sm leading-relaxed">
            ${m.description}
          </p>
        </div>

        <div class="space-y-1.5 pt-3 border-t border-slate-800/80">
          <p class="text-xs sm:text-sm font-bold text-slate-400 uppercase tracking-wider font-cinzel">Pistas y Hechos Conocidos:</p>
          <ul class="space-y-1">
            ${m.clues.map(c => `
              <li class="text-xs text-slate-300 flex items-start gap-2">
                <span class="text-amber-400 mt-1">•</span>
                <span>${c}</span>
              </li>
            `).join('')}
          </ul>
        </div>
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
    card.className = 'rpg-card rounded-xl overflow-hidden border border-purple-500/30 flex flex-col sm:flex-row items-center gap-3.5 p-3.5 hover:border-purple-500/60 transition';
    
    card.innerHTML = `
      <img src="${item.image || 'images/asset_1843595399.jpg'}" class="w-16 h-16 sm:w-20 sm:h-20 rounded-lg object-cover border border-purple-500/40 flex-shrink-0 cursor-pointer" onclick="openLightbox('${item.image}', '${item.name}')">
      <div class="space-y-1 flex-1 w-full">
        <div class="flex items-center justify-between gap-1">
          <h4 class="font-cinzel font-bold text-sm text-purple-200">${item.name}</h4>
          <span class="text-xs font-semibold px-2 py-0.5 rounded bg-purple-950/60 text-purple-300 border border-purple-800/40 font-sans font-medium">${item.holder}</span>
        </div>
        <p class="font-crimson text-xs text-slate-300 leading-snug">${item.desc}</p>
      </div>
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
        <span class="text-xs font-semibold px-2 py-0.5 rounded bg-slate-800 text-slate-400 font-sans">${r.type}</span>
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
  for (let i = 0; i < 40; i++) {
    particles.push({
      x: Math.random() * width,
      y: Math.random() * height,
      size: Math.random() * 2 + 0.8,
      speedY: Math.random() * 0.4 + 0.15,
      speedX: (Math.random() - 0.5) * 0.25,
      opacity: Math.random() * 0.5 + 0.2,
      color: Math.random() > 0.4 ? '212, 168, 83' : '168, 85, 247'
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

    const bufferSize = audioCtx.sampleRate * 2;
    const noiseBuffer = audioCtx.createBuffer(1, bufferSize, audioCtx.sampleRate);
    const output = noiseBuffer.getChannelData(0);

    let lastOut = 0.0;
    for (let i = 0; i < bufferSize; i++) {
      const white = Math.random() * 2 - 1;
      output[i] = (lastOut + (0.02 * white)) / 1.02;
      lastOut = output[i];
      output[i] *= 3.5;
    }

    noiseNode = audioCtx.createBufferSource();
    noiseNode.buffer = noiseBuffer;
    noiseNode.loop = true;

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
    console.log("Audio Web API error: ", e);
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
