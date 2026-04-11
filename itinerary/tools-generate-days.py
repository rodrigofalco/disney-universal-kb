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

for d in data['days']:
    ph = d.get('parkHours') or {}
    ll = d.get('lightningLane') or []
    park_map = d.get('parkMap')
    attractions = d.get('attractionsList') or []
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
        <div class="detail-grid">
          <div class="detail-card"><strong>Fecha</strong><span>{esc(d['displayDate'])}</span></div>
          <div class="detail-card"><strong>Fase</strong><span>{esc(d['phase'])}</span></div>
          <div class="detail-card"><strong>Tipo</strong><span>{esc(d['type'])}</span></div>
          <div class="detail-card"><strong>Ubicación</strong><span>{esc(d['location'])}</span></div>
          <div class="detail-card"><strong>Hotel</strong><span>{esc(d['hotel'])}</span></div>
          <div class="detail-card"><strong>Transporte</strong><span>{esc(d['transport'])}</span></div>
          {f'<div class="detail-card"><strong>Early Entry</strong><span>{esc(ph.get("earlyEntry"))}</span></div>' if ph.get('earlyEntry') else ''}
          {f'<div class="detail-card"><strong>Horario Parque</strong><span>{esc(ph.get("parkHours"))}</span></div>' if ph.get('parkHours') else ''}
          {f'<div class="detail-card"><strong>Extended Evening</strong><span>{esc(ph.get("extendedEveningHours"))}</span></div>' if ph.get('extendedEveningHours') else ''}
        </div>

        {f'<div class="timeline-block"><h3>Lightning Lane Reservadas</h3><div class="card-grid">' + ''.join([f'<div class="mini-card"><div class="badges"><span class="badge {'status-confirmado' if x.get('type') == 'Individual' else 'status-aprobado'}">{'Individual' if x.get('type') == 'Individual' else 'Multi Pass'}</span><span class="badge">{esc(x.get("timeWindow"))}</span></div><h4>{esc(x.get("attraction"))}</h4></div>' for x in ll]) + '</div></div>' if ll else ''}

        {f'<div class="timeline-block"><h3>Mapa del parque</h3><p class="muted">Mini mapa para ubicar secciones, atracciones y distancias relativas. Click para ampliar.</p><a class="park-map-link" href="{esc(park_map["full"])}" target="_blank" rel="noopener noreferrer"><img class="park-map-thumb" src="{esc(park_map["thumb"])}" alt="Mapa de {esc(d["title"])}" loading="lazy" /></a><p class="muted park-map-source">Fuente: {esc(park_map["source"])} </p></div>' if park_map else ''}

        {f'<details class="timeline-block collapsible-block attractions-details"><summary>Lista de atracciones del parque</summary><ul class="clean attractions-list">{list_items(attractions)}</ul></details>' if attractions else ''}

        {f'<div class="timeline-block"><h3>Shows y Entretenimiento</h3><p>{esc(d.get("shows"))}</p></div>' if d.get('shows') else ''}

        {f'<div class="timeline-block"><h3>Prioridades del día</h3><ul class="clean">{list_items(d.get("highlights") or [])}</ul></div>' if d.get('highlights') else ''}
        {f'<div class="timeline-block"><h3>Otras atracciones o ideas interesantes</h3><ul class="clean">{list_items(d.get("interesting") or [])}</ul></div>' if d.get('interesting') else ''}
        {f'<div class="timeline-block"><h3>Opcionales si sobra energía</h3><ul class="clean">{list_items(d.get("optional") or [])}</ul></div>' if d.get('optional') else ''}

        <div class="timeline-block">
          <h3>Notas completas</h3>
          <p>{esc(d.get('notes',''))}</p>
        </div>
      </div>
    </section>
  </main>

  <footer class="footer container">Basado en <code>docs/Itinerary.md</code> · versión estática para compartir</footer>
</body>
</html>
'''
    out = root / 'days' / f"day-{d['date'].replace('-', '')}.html"
    out.write_text(html_doc)
print(f'generated {len(data["days"])} clean day pages')
