import json, html
from pathlib import Path

root = Path('/home/rfalco/.openclaw/workspace-trip-disney/site-publish/disney-universal-kb/itinerary')
data = json.loads((root / 'assets/itinerary.json').read_text())


def esc(s):
    return html.escape('' if s is None else str(s), quote=True)


def badge(text, cls=''):
    cls_attr = f' {cls}' if cls else ''
    return f'<span class="badge{cls_attr}">{esc(text)}</span>'


def list_items(items):
    return ''.join(f'<li>{esc(x)}</li>' for x in items)


def grouped_items(groups):
    parts = []
    for area, items in groups.items():
        parts.append(f'<div class="attraction-group"><h4>{esc(area)}</h4><ul class="clean attractions-list">{list_items(items)}</ul></div>')
    return ''.join(parts)


def lightning_lane_html(ll):
    cards = []
    for x in ll:
        cls = 'status-confirmado' if x.get('type') == 'Individual' else 'status-aprobado'
        label = 'Individual' if x.get('type') == 'Individual' else 'Multi Pass'
        cards.append(
            f'<div class="mini-card"><div class="badges"><span class="badge {cls}">{label}</span>'
            f'<span class="badge">{esc(x.get("timeWindow"))}</span></div><h4>{esc(x.get("attraction"))}</h4></div>'
        )
    return f'<div class="timeline-block"><h3>Lightning Lane Reservadas</h3><div class="card-grid">{"".join(cards)}</div></div>'


LIGHTBOX_SCRIPT = """
  <script>
    (function () {
      const lightbox = document.getElementById('imageLightbox');
      if (!lightbox) return;
      const img = lightbox.querySelector('.lightbox-image');
      const caption = lightbox.querySelector('.lightbox-caption');
      const dialog = lightbox.querySelector('.lightbox-dialog');
      const zoomInBtn = document.createElement('button');
      zoomInBtn.type = 'button';
      zoomInBtn.className = 'lightbox-tool';
      zoomInBtn.textContent = '+';
      const zoomOutBtn = document.createElement('button');
      zoomOutBtn.type = 'button';
      zoomOutBtn.className = 'lightbox-tool';
      zoomOutBtn.textContent = '−';
      const resetBtn = document.createElement('button');
      resetBtn.type = 'button';
      resetBtn.className = 'lightbox-tool lightbox-tool-reset';
      resetBtn.textContent = 'Reset';
      const controls = document.createElement('div');
      controls.className = 'lightbox-controls';
      controls.append(zoomOutBtn, zoomInBtn, resetBtn);
      dialog.appendChild(controls);
      let panzoom = null;
      const destroyPanzoom = () => {
        if (panzoom && panzoom.destroy) panzoom.destroy();
        panzoom = null;
        img.style.transform = '';
      };
      const close = () => {
        lightbox.hidden = true;
        destroyPanzoom();
        img.src = '';
        img.alt = '';
        caption.textContent = '';
      };
      const openers = document.querySelectorAll('.park-map-trigger');
      openers.forEach((btn) => btn.addEventListener('click', () => {
        img.src = btn.dataset.fullSrc || '';
        img.alt = btn.dataset.title || 'Mapa ampliado';
        caption.textContent = btn.dataset.title || '';
        lightbox.hidden = false;
        img.onload = () => {
          destroyPanzoom();
          panzoom = Panzoom(img, { maxScale: 5, minScale: 1, contain: 'outside' });
        };
      }));
      zoomInBtn.addEventListener('click', () => panzoom && panzoom.zoomIn());
      zoomOutBtn.addEventListener('click', () => panzoom && panzoom.zoomOut());
      resetBtn.addEventListener('click', () => panzoom && panzoom.reset());
      lightbox.querySelector('.lightbox-backdrop').addEventListener('click', close);
      lightbox.querySelector('.lightbox-close').addEventListener('click', close);
      document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && !lightbox.hidden) close();
      });
      const wheelTarget = lightbox.querySelector('.lightbox-image');
      wheelTarget.parentElement.addEventListener('wheel', function (event) {
        if (!panzoom) return;
        event.preventDefault();
        panzoom.zoomWithWheel(event);
      });
    })();
  </script>
"""

for d in data['days']:
    ph = d.get('parkHours') or {}
    ll = d.get('lightningLane') or []
    park_map = d.get('parkMap')
    attractions = d.get('attractionsList') or []
    attraction_groups = d.get('attractionGroups') or {}

    detail_cards = [
        f'<div class="detail-card"><strong>Fecha</strong><span>{esc(d["displayDate"])}</span></div>',
        f'<div class="detail-card"><strong>Fase</strong><span>{esc(d["phase"])}</span></div>',
        f'<div class="detail-card"><strong>Tipo</strong><span>{esc(d["type"])}</span></div>',
        f'<div class="detail-card"><strong>Ubicación</strong><span>{esc(d["location"])}</span></div>',
        f'<div class="detail-card"><strong>Hotel</strong><span>{esc(d["hotel"])}</span></div>',
        f'<div class="detail-card"><strong>Transporte</strong><span>{esc(d["transport"])}</span></div>',
    ]
    if ph.get('earlyEntry'):
        detail_cards.append(f'<div class="detail-card"><strong>Early Entry</strong><span>{esc(ph.get("earlyEntry"))}</span></div>')
    if ph.get('parkHours'):
        detail_cards.append(f'<div class="detail-card"><strong>Horario Parque</strong><span>{esc(ph.get("parkHours"))}</span></div>')
    if ph.get('extendedEveningHours'):
        detail_cards.append(f'<div class="detail-card"><strong>Extended Evening</strong><span>{esc(ph.get("extendedEveningHours"))}</span></div>')

    park_map_html = ''
    if park_map:
        park_map_html = (
            f'<div class="timeline-block"><h3>Mapa del parque</h3>'
            f'<p class="muted">Mini mapa para ubicar secciones, atracciones y distancias relativas. Click para abrir visor con zoom.</p>'
            f'<button class="park-map-trigger" type="button" data-full-src="{esc(park_map["full"])}" data-title="Mapa de {esc(d["title"])}">'
            f'<img class="park-map-thumb" src="{esc(park_map["thumb"])}" alt="Mapa de {esc(d["title"])}" loading="lazy" /></button>'
            f'<p class="muted park-map-source">Fuente: {esc(park_map["source"])} </p></div>'
        )

    attractions_html = ''
    if attraction_groups:
        attractions_html = f'<details class="timeline-block collapsible-block attractions-details"><summary>Lista de atracciones del parque</summary>{grouped_items(attraction_groups)}</details>'
    elif attractions:
        attractions_html = f'<details class="timeline-block collapsible-block attractions-details"><summary>Lista de atracciones del parque</summary><ul class="clean attractions-list">{list_items(attractions)}</ul></details>'

    shows_html = f'<div class="timeline-block"><h3>Shows y Entretenimiento</h3><p>{esc(d.get("shows"))}</p></div>' if d.get('shows') else ''
    highlights_html = f'<div class="timeline-block"><h3>Prioridades del día</h3><ul class="clean">{list_items(d.get("highlights") or [])}</ul></div>' if d.get('highlights') else ''
    interesting_html = f'<div class="timeline-block"><h3>Otras atracciones o ideas interesantes</h3><ul class="clean">{list_items(d.get("interesting") or [])}</ul></div>' if d.get('interesting') else ''
    optional_html = f'<div class="timeline-block"><h3>Opcionales si sobra energía</h3><ul class="clean">{list_items(d.get("optional") or [])}</ul></div>' if d.get('optional') else ''
    notes_html = f'<div class="timeline-block"><h3>Notas completas</h3><p>{esc(d.get("notes", ""))}</p></div>'

    lightbox_html = """
  <div class="image-lightbox" id="imageLightbox" hidden>
    <button class="lightbox-backdrop" type="button" aria-label="Cerrar"></button>
    <div class="lightbox-dialog" role="dialog" aria-modal="true" aria-label="Mapa ampliado">
      <button class="lightbox-close" type="button" aria-label="Cerrar">×</button>
      <img class="lightbox-image" src="" alt="" />
      <p class="lightbox-caption"></p>
    </div>
  </div>
"""

    html_doc = f'''<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{esc(d['title'])} - Itinerario Orlando 2026</title>
  <meta name="description" content="Día {esc(d['displayDate'])} del itinerario Orlando 2026: {esc(d['title'])}" />
  <link rel="stylesheet" href="../assets/styles.v2.css" />
</head>
<body data-page="day-detail">
  <div class="topbar">
    <div class="container">
      <a href="../index.html" class="eyebrow">← Volver al itinerario completo</a>
      <div class="topnav">
        <a href="../../index.html">Inicio</a>
        <a href="../index.html">Itinerario</a>
      </div>
    </div>
  </div>

  <main>
    <section class="hero">
      <div class="container">
        <div class="hero-card">
          <span class="eyebrow">{esc(d['phase'])}</span>
          <h1>{esc(d['title'])}</h1>
          <p class="lead">{esc(d['displayDate'])} · {esc(d['location'])} · {esc(d['hotel'])}</p>
          <div class="badges">
            {badge(d['type'])}
            {badge(d['status'], 'status-' + esc((d.get('status','').split(' ')[0])))}
            {badge(d['ticket'])}
            {badge('Ritmo: ' + d['pace'])}
          </div>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="container panel">
        <div class="detail-grid">{''.join(detail_cards)}</div>
        {lightning_lane_html(ll) if ll else ''}
        {park_map_html}
        {attractions_html}
        {shows_html}
        {highlights_html}
        {interesting_html}
        {optional_html}
        {notes_html}
      </div>
    </section>
  </main>
{lightbox_html}
  <script src="../assets/panzoom.min.js"></script>
{LIGHTBOX_SCRIPT}
  <footer class="footer container">Basado en <code>docs/Itinerary.md</code> · versión estática para compartir</footer>
</body>
</html>
'''
    out = root / 'days' / f"day-{d['date'].replace('-', '')}.html"
    out.write_text(html_doc)

print(f'generated {len(data["days"])} clean day pages')
