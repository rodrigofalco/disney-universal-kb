function getAssetUrl(file) {
  const current = new URL(window.location.href);
  const basePath = current.pathname.endsWith('/') ? current.pathname : current.pathname.replace(/[^/]+$/, '');
  const rootPath = basePath.endsWith('/assets/') ? basePath.slice(0, -7) : basePath;
  return `${current.origin}${rootPath}assets/${file}`;
}

async function loadItinerary() {
  const response = await fetch(getAssetUrl('itinerary.json'), { cache: 'no-store' });
  if (!response.ok) throw new Error(`No se pudo cargar el itinerario (${response.status})`);
  return response.json();
}

function fmtText(value) {
  return String(value || '').replace(/[&<>"']/g, (m) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[m]));
}

function badge(text, cls = '') {
  return `<span class="badge ${cls}">${fmtText(text)}</span>`;
}

function getTripCountdown(days) {
  const firstDay = [...days].sort((a, b) => a.date.localeCompare(b.date))[0];
  if (!firstDay?.date) return null;

  const target = new Date(`${firstDay.date}T00:00:00Z`);
  const now = new Date();
  const todayUtc = Date.UTC(now.getUTCFullYear(), now.getUTCMonth(), now.getUTCDate());
  const targetUtc = Date.UTC(target.getUTCFullYear(), target.getUTCMonth(), target.getUTCDate());
  return Math.round((targetUtc - todayUtc) / 86400000);
}

function createHero(meta, days) {
  const parqueDays = days.filter((d) => d.type === 'Parque').length;
  const descansoDays = days.filter((d) => d.type === 'Descanso').length;
  const countdown = getTripCountdown(days);
  const countdownLabel = countdown === null
    ? 'sin fecha'
    : countdown > 1
      ? `faltan ${countdown} días`
      : countdown === 1
        ? 'falta 1 día'
        : countdown === 0
          ? 'el viaje empieza hoy'
          : `viaje iniciado hace ${Math.abs(countdown)} días`;
  return `
    <div class="hero-card">
      <span class="eyebrow">🏰 Itinerario del viaje</span>
      <h1>${fmtText(meta.titulo)}</h1>
      <p class="lead">${fmtText(meta.subtitulo)} · ${fmtText(meta.rango)} · ${fmtText(meta.estado)}</p>
      <div class="stats">
        <div class="stat countdown-stat"><strong>${fmtText(countdownLabel)}</strong><span>contador hasta el inicio</span></div>
        <div class="stat"><strong>${days.length}</strong><span>días cargados</span></div>
        <div class="stat"><strong>${parqueDays}</strong><span>jornadas de parque</span></div>
        <div class="stat"><strong>${descansoDays}</strong><span>día de descanso</span></div>
      </div>
    </div>`;
}

function createTopbar(title) {
  return `
  <div class="topbar">
    <div class="container">
      <strong>${fmtText(title)}</strong>
      <nav class="topnav">
        <a href="./index.html">Itinerario</a>
      </nav>
    </div>
  </div>`;
}

function createFooter() {
  return `<footer class="footer container">Basado en <code>docs/Itinerary.md</code> · versión estática para compartir</footer>`;
}

function renderItinerary(data) {
  document.body.innerHTML = `
    ${createTopbar('Itinerario Orlando 2026')}
    <main>
      <section class="hero"><div class="container">${createHero(data.meta, data.days)}</div></section>
      <section class="section">
        <div class="container panel">
          <h2>Itinerario día por día</h2>
          <p class="muted">Cada día se puede expandir para ver prioridades, ideas secundarias y notas de ejecución.</p>
          <div class="timeline-actions">
            <button id="expandAll">Expandir todo</button>
            <button id="collapseAll" class="secondary-btn">Contraer todo</button>
          </div>
          <div class="timeline">
            ${data.days.map((d, index) => `
              <article class="timeline-item timeline-collapsible ${index === 0 ? 'expanded' : ''}" data-index="${index}">
                <button class="timeline-toggle" type="button" aria-expanded="${index === 0 ? 'true' : 'false'}">
                  <div class="timeline-toggle-main">
                    <div class="badges">
                      ${badge(d.displayDate)}
                      ${badge(d.phase, `phase-${d.phase}`)}
                      ${badge(d.type)}
                    </div>
                    <h3>${fmtText(d.title)}</h3>
                    <p class="muted">${fmtText(d.location)} · ${fmtText(d.hotel)}</p>
                  </div>
                  <span class="timeline-chevron">▾</span>
                </button>
                <div class="timeline-summary">
                  <div class="chips">
                    ${badge(`Ritmo: ${d.pace}`)}
                    ${badge(d.ticket)}
                    ${badge(d.status, `status-${(d.status || '').split(' ')[0]}`)}
                  </div>
                  <p class="timeline-short-note">${fmtText(d.notes)}</p>
                </div>
                <div class="timeline-details">
                  <div class="detail-grid">
                    <div class="detail-card"><strong>Fecha</strong><span>${fmtText(d.displayDate)}</span></div>
                    <div class="detail-card"><strong>Fase</strong><span>${fmtText(d.phase)}</span></div>
                    <div class="detail-card"><strong>Tipo</strong><span>${fmtText(d.type)}</span></div>
                    <div class="detail-card"><strong>Ubicación</strong><span>${fmtText(d.location)}</span></div>
                    <div class="detail-card"><strong>Hotel</strong><span>${fmtText(d.hotel)}</span></div>
                    <div class="detail-card"><strong>Transporte</strong><span>${fmtText(d.transport)}</span></div>
                    <div class="detail-card"><strong>Ritmo</strong><span>${fmtText(d.pace)}</span></div>
                    <div class="detail-card"><strong>Ticket</strong><span>${fmtText(d.ticket)}</span></div>
                    <div class="detail-card"><strong>Estado</strong><span>${fmtText(d.status)}</span></div>
                  </div>
                  <div class="timeline-block">
                    <h4>Prioridades del día</h4>
                    <ul class="clean">${(d.highlights || []).map((x) => `<li>${fmtText(x)}</li>`).join('')}</ul>
                  </div>
                  ${(d.interesting || []).length ? `
                  <div class="timeline-block">
                    <h4>Otras atracciones o ideas interesantes</h4>
                    <ul class="clean">${d.interesting.map((x) => `<li>${fmtText(x)}</li>`).join('')}</ul>
                  </div>` : ''}
                  ${(d.optional || []).length ? `
                  <div class="timeline-block">
                    <h4>Opcionales si sobra energía</h4>
                    <ul class="clean">${d.optional.map((x) => `<li>${fmtText(x)}</li>`).join('')}</ul>
                  </div>` : ''}
                  <div class="timeline-block">
                    <h4>Notas completas</h4>
                    <p>${fmtText(d.notes)}</p>
                  </div>
                </div>
              </article>`).join('')}
          </div>
        </div>
      </section>
    </main>
    ${createFooter()}`;

  const items = Array.from(document.querySelectorAll('.timeline-collapsible'));
  const setExpanded = (item, expanded) => {
    item.classList.toggle('expanded', expanded);
    const btn = item.querySelector('.timeline-toggle');
    if (btn) btn.setAttribute('aria-expanded', expanded ? 'true' : 'false');
  };

  items.forEach((item) => {
    const btn = item.querySelector('.timeline-toggle');
    btn.addEventListener('click', () => setExpanded(item, !item.classList.contains('expanded')));
  });

  document.getElementById('expandAll').addEventListener('click', () => items.forEach((item) => setExpanded(item, true)));
  document.getElementById('collapseAll').addEventListener('click', () => items.forEach((item) => setExpanded(item, false)));
}

async function boot() {
  const data = await loadItinerary();
  renderItinerary(data);
}

boot().catch((error) => {
  document.body.innerHTML = `<main class="container" style="padding:48px 0"><div class="panel"><h1>Error</h1><p>No se pudo cargar la visualización.</p><pre>${fmtText(error.message)}</pre><p style="margin-top:12px"><a href="./index.html">Volver al itinerario</a></p></div></main>`;
});
