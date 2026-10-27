from pathlib import Path
import csv, json

ROOT = Path(__file__).resolve().parents[1]
AGG = ROOT / 'work' / 'data' / 'aggregates'
OUT = ROOT / 'outputs' / 'LaDe-interactive-dashboard.html'

def load(name):
    with (AGG / name).open(encoding='utf-8-sig', newline='') as f:
        return list(csv.DictReader(f))

city_month = load('city_month.csv')
city_hour = load('city_accept_hour.csv')
region_month = load('city_region_month.csv')
for row in city_month + city_hour + region_month:
    for key, value in list(row.items()):
        if value == '':
            row[key] = None
        else:
            try:
                row[key] = float(value) if '.' in value else int(value)
            except ValueError:
                pass

payload = json.dumps({'cityMonth': city_month, 'cityHour': city_hour, 'regionMonth': region_month}, separators=(',', ':'))
html = r'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>LaDe-D | Delivery reliability and operations</title>
<style>
:root{--bg:#f4f6f8;--panel:#fff;--ink:#17243a;--muted:#607086;--line:#dce3eb;--blue:#1769aa;--teal:#0b887a;--orange:#dc7a22;--pale:#edf4fa;--shadow:0 8px 24px #1a33500c}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.5 "Segoe UI",Arial,sans-serif}.shell{max-width:1440px;margin:auto;padding:26px 30px 46px}.hero{background:#142b45;color:white;padding:26px 30px;border-radius:18px;display:flex;justify-content:space-between;gap:24px;align-items:center}.eyebrow{text-transform:uppercase;letter-spacing:.12em;font-size:11px;color:#aed9e5;font-weight:700}.hero h1{margin:7px 0 4px;font-size:clamp(25px,3vw,38px);line-height:1.1}.hero p{margin:0;color:#d5e2ed;max-width:800px}.tag{border:1px solid #ffffff46;border-radius:999px;padding:8px 13px;color:#eaf5ff;font-size:12px;white-space:nowrap}.notice{margin:16px 0;padding:13px 17px;background:#fff6e8;border:1px solid #f2d9a6;border-radius:12px;color:#694a17;font-size:13px}.controls{display:flex;align-items:end;flex-wrap:wrap;gap:12px;margin:18px 0}.control{background:var(--panel);padding:10px 13px;border:1px solid var(--line);border-radius:10px;box-shadow:var(--shadow);min-width:170px}.control label{display:block;color:var(--muted);font-size:11px;text-transform:uppercase;letter-spacing:.06em;margin-bottom:4px;font-weight:700}.control select{border:0;background:transparent;font-size:14px;color:var(--ink);min-width:145px;outline:0}.control.toggle{min-width:auto;display:flex;align-items:center;gap:9px;padding:14px}.toggle label{margin:0;text-transform:none;letter-spacing:0;font-size:13px;color:var(--ink)}.toggle input{accent-color:var(--blue)}.kpis{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:13px;margin-bottom:16px}.card,.panel{background:var(--panel);border:1px solid var(--line);border-radius:14px;box-shadow:var(--shadow)}.card{padding:16px 18px}.card .label{color:var(--muted);font-size:12px}.card .value{font-size:26px;font-weight:700;letter-spacing:-.03em;margin-top:4px}.card .sub{font-size:11px;color:var(--muted);margin-top:2px}.grid{display:grid;grid-template-columns:1.2fr .8fr;gap:15px}.panel{padding:18px 19px;min-width:0}.panel.wide{grid-column:1/-1}.panel-head{display:flex;justify-content:space-between;align-items:start;gap:15px;margin-bottom:7px}.panel h2{font-size:17px;margin:0}.panel .desc{font-size:12px;color:var(--muted);margin:2px 0 12px}.switch{display:flex;gap:5px;padding:3px;border-radius:8px;background:#edf2f7}.switch button{border:0;border-radius:6px;background:transparent;color:var(--muted);padding:6px 9px;cursor:pointer;font-size:12px}.switch button.active{background:#fff;color:var(--blue);box-shadow:0 1px 4px #20344c20;font-weight:700}svg{width:100%;height:auto;display:block;overflow:visible}.legend{display:flex;flex-wrap:wrap;gap:12px;margin-top:6px;font-size:11px;color:var(--muted)}.legend span{display:flex;align-items:center;gap:6px}.dot{width:9px;height:9px;border-radius:50%;display:inline-block}.foot{font-size:11px;color:var(--muted);margin-top:8px}.tablewrap{overflow:auto;max-height:430px;border:1px solid var(--line);border-radius:9px}table{width:100%;border-collapse:collapse;font-size:12px}th,td{padding:9px 10px;border-bottom:1px solid #e8edf2;text-align:right;white-space:nowrap}th{position:sticky;top:0;background:#f4f7fa;color:#53657b;font-weight:700}th:first-child,td:first-child{text-align:left}tr:last-child td{border-bottom:0}.empty{padding:35px;text-align:center;color:var(--muted)}.footer{margin-top:16px;border-top:1px solid var(--line);padding-top:12px;color:var(--muted);font-size:11px;display:flex;justify-content:space-between;gap:10px;flex-wrap:wrap}.small{font-size:11px}.outlier{color:#a1510a}.nowrap{white-space:nowrap}
@media(max-width:900px){.kpis{grid-template-columns:repeat(2,1fr)}.grid{grid-template-columns:1fr}.panel.wide{grid-column:auto}.hero{align-items:start;flex-direction:column}}@media(max-width:520px){.shell{padding:13px}.kpis{grid-template-columns:1fr 1fr}.card .value{font-size:21px}.control{flex:1}.hero{padding:21px}}
</style>
</head>
<body><main class="shell">
<header class="hero"><div><div class="eyebrow">Operations analytics · LaDe-D</div><h1>Delivery reliability, with data quality in view</h1><p>Explore acceptance-to-task-completion intervals across five Chinese cities and find where the source data needs careful interpretation.</p></div><div class="tag">Historical data · 2022</div></header>
<div class="notice"><strong>Read this before interpreting:</strong> This is historical data from China, not an India benchmark. The elapsed interval is descriptive, not an SLA or promised delivery measure. The timestamp year is provisionally set to 2022; timezone is undocumented. There are no customer reviews, so this does not measure satisfaction. Months outside May–October remain available for data-quality review.</div>
<section class="controls" aria-label="Dashboard filters"><div class="control"><label for="city">City</label><select id="city"></select></div><div class="control"><label for="detailMonth">Detail month</label><select id="detailMonth"></select></div><div class="control toggle"><input id="windowOnly" type="checkbox" checked><label for="windowOnly">Limit headline totals to May–October 2022</label></div></section>
<section class="kpis"><article class="card"><div class="label">Packages in headline scope</div><div class="value" id="kpiPackages">—</div><div class="sub" id="kpiScope">—</div></article><article class="card"><div class="label">Intervals over 24 hours</div><div class="value" id="kpiOver24">—</div><div class="sub">Package-weighted interval share; not an SLA miss rate</div></article><article class="card"><div class="label">Cross-calendar date flags</div><div class="value" id="kpiCrossDate">—</div><div class="sub">Source date differs from acceptance calendar date</div></article><article class="card"><div class="label">City-month groups</div><div class="value" id="kpiGroups">—</div><div class="sub">Percentiles below stay at their observed group grain</div></article></section>
<section class="grid">
<article class="panel wide"><div class="panel-head"><div><h2>Monthly delivery interval trend</h2><p class="desc">Each point is a precomputed city-month percentile. No monthly percentiles are averaged together.</p></div><div class="switch" id="monthlyMode"><button data-mode="median" class="active">Median</button><button data-mode="p90">P90</button></div></div><div id="monthlyChart"></div><div id="monthlyLegend" class="legend"></div><div class="foot">Acceptance month from the source clock. Month 12 has an observed record outside the documented May–October period; filter interpretation accordingly.</div></article>
<article class="panel"><div class="panel-head"><div><h2>Acceptance-hour pattern</h2><p class="desc" id="hourSubtitle">Choose one city and month or compare city lines.</p></div><div class="switch" id="hourMode"><button data-mode="median" class="active">Median</button><button data-mode="p90">P90</button></div></div><div id="hourChart"></div><div id="hourLegend" class="legend"></div><div class="foot">Source acceptance hour; do not assume local timezone. Each value is a city-month-hour group.</div></article>
<article class="panel"><div class="panel-head"><div><h2>Region-code view</h2></div></div><p class="desc">Highest P90 groups for the selected city and detail month. Region codes are source <code>region_id</code>, not named neighborhoods.</p><div class="tablewrap"><table><thead><tr><th>region_id</th><th>packages</th><th>median min</th><th>P90 min</th><th>&gt;24h</th></tr></thead><tbody id="regionRows"></tbody></table></div><div class="foot">Low-volume groups were screened upstream (fewer than 200 packages). This is a volume screen, not statistical proof.</div></article>
<article class="panel wide"><h2>Interpretation notes</h2><p class="desc">Use the dashboard to find questions for operations teams, not to claim causes.</p><ul class="small"><li>Do not compare an all-period city P90 by averaging monthly or hourly P90 values.</li><li>Long intervals do not by themselves prove a missed promise; the dataset has no promised delivery deadline or SLA field.</li><li>Timestamp parsing uses a provisional 2022 year and no timezone. Negative or out-of-window intervals require source clarification.</li><li>The source covers five cities in China and a historical period. Do not generalize the result to present-day Indian delivery operations.</li></ul></article>
</section><footer class="footer"><span>Source: Cainiao-AI LaDe-D, delivery event aggregates prepared locally in DuckDB.</span><span>Aggregate-only preview · raw package and courier rows are not embedded.</span></footer>
</main>
<script>
const DATA=__DATA__;
const COLORS=['#1769aa','#0b887a','#dc7a22','#7866b2','#cf5360'];
const cities=[...new Set(DATA.cityMonth.map(d=>d.city))].sort();
const months=[...new Set(DATA.cityMonth.map(d=>Number(d.accept_month)))].sort((a,b)=>a-b);
const monthLabel=m=>'2022-'+String(m).padStart(2,'0');
const fmt=n=>Number(n||0).toLocaleString('en-IN');
const minfmt=n=>Number(n).toLocaleString('en-IN',{maximumFractionDigits:1});
const citySelect=document.querySelector('#city'), monthSelect=document.querySelector('#detailMonth');
citySelect.innerHTML='<option value="All">All cities</option>'+cities.map(c=>`<option value="${c}">${c}</option>`).join('');
monthSelect.innerHTML=months.map(m=>`<option value="${m}" ${m===10?'selected':''}>${monthLabel(m)}${m<5||m>10?' · outside stated window':''}</option>`).join('');
let monthlyMode='median',hourMode='median';
for(const [id,setter] of [['monthlyMode',v=>monthlyMode=v],['hourMode',v=>hourMode=v]])document.querySelector('#'+id).addEventListener('click',e=>{if(e.target.dataset.mode){setter(e.target.dataset.mode);document.querySelectorAll('#'+id+' button').forEach(b=>b.classList.toggle('active',b===e.target));render()}});
for(const x of [citySelect,monthSelect,document.querySelector('#windowOnly')])x.addEventListener('change',render);
function scopeRows(){let rows=DATA.cityMonth.filter(r=>citySelect.value==='All'||r.city===citySelect.value);if(document.querySelector('#windowOnly').checked)rows=rows.filter(r=>r.accept_month>=5&&r.accept_month<=10);return rows}
function drawLines(host,legendHost,series,xs,{xLabel,yLabel,mode='median',xTick}){
 const W=830,H=300,L=56,R=24,T=18,B=45,innerW=W-L-R,innerH=H-T-B;
 if(!xs.length||!series.length){document.querySelector(host).innerHTML='<div class="empty">No data for the current selection.</div>';document.querySelector(legendHost).innerHTML='';return}
 const vals=series.flatMap(s=>s.points.map(p=>p.y)).filter(Number.isFinite);let max=Math.max(...vals,1);max=Math.ceil(max/50)*50;
 const sx=i=>L+(xs.length<2?innerW/2:i*innerW/(xs.length-1)),sy=y=>T+innerH-(y/max)*innerH;
 let svg=`<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="${yLabel} by ${xLabel}">`;
 for(let i=0;i<=4;i++){let y=max*i/4,py=sy(y);svg+=`<line x1="${L}" y1="${py}" x2="${W-R}" y2="${py}" stroke="#e7edf3"/><text x="${L-9}" y="${py+4}" text-anchor="end" font-size="10" fill="#718198">${Math.round(y)}</text>`}
 xs.forEach((x,i)=>{if(xs.length<14||i%2===0||i===xs.length-1)svg+=`<text x="${sx(i)}" y="${H-17}" text-anchor="middle" font-size="10" fill="#718198">${xTick(x)}</text>`});
 series.forEach(s=>{const p=s.points.filter(p=>Number.isFinite(p.y));if(p.length>1)svg+=`<polyline fill="none" stroke="${s.color}" stroke-width="2.5" points="${p.map(q=>`${sx(q.xi)},${sy(q.y)}`).join(' ')}"/>`;p.forEach(q=>svg+=`<circle cx="${sx(q.xi)}" cy="${sy(q.y)}" r="4" fill="${s.color}"><title>${s.name} · ${xLabel} ${xs[q.xi]} · ${yLabel} ${minfmt(q.y)} min · ${fmt(q.count)} packages</title></circle>`)});
 svg+=`<text transform="translate(15 ${T+innerH/2}) rotate(-90)" text-anchor="middle" font-size="10" fill="#607086">${yLabel} (minutes)</text></svg>`;document.querySelector(host).innerHTML=svg;
 document.querySelector(legendHost).innerHTML=series.map(s=>`<span><i class="dot" style="background:${s.color}"></i>${s.name}</span>`).join('');
}
function render(){
 const rows=scopeRows(),packages=rows.reduce((a,r)=>a+r.package_count,0),over=rows.reduce((a,r)=>a+r.over_24h_count,0),cross=rows.reduce((a,r)=>a+r.cross_calendar_date_count,0);
 document.querySelector('#kpiPackages').textContent=fmt(packages);document.querySelector('#kpiScope').textContent=`${citySelect.value==='All'?'All cities':citySelect.value} · ${document.querySelector('#windowOnly').checked?'May–October 2022':'all observed months'}`;
 document.querySelector('#kpiOver24').textContent=packages?`${(100*over/packages).toFixed(2)}%`:'—';document.querySelector('#kpiCrossDate').textContent=fmt(cross);document.querySelector('#kpiGroups').textContent=fmt(rows.length);
 const cityRows=rows.filter(r=>citySelect.value==='All'||r.city===citySelect.value),trendMonths=[...new Set(cityRows.map(r=>Number(r.accept_month)))].sort((a,b)=>a-b);
 let trendSeries=(citySelect.value==='All'?cities:[citySelect.value]).map((city,i)=>({name:city,color:COLORS[i%COLORS.length],points:trendMonths.map((m,xi)=>{const r=cityRows.find(d=>d.city===city&&Number(d.accept_month)===m);return {xi,y:r?Number(r[monthlyMode==='median'?'median_elapsed_min':'p90_elapsed_min']):NaN,count:r?Number(r.package_count):0}})}));
 drawLines('#monthlyChart','#monthlyLegend',trendSeries,trendMonths,{xLabel:'acceptance month',yLabel:monthlyMode==='median'?'Median':'P90',xTick:monthLabel});
 const m=Number(monthSelect.value),hourRows=DATA.cityHour.filter(r=>Number(r.accept_month)===m&&(citySelect.value==='All'||r.city===citySelect.value)),hours=[...new Set(hourRows.map(r=>Number(r.source_accept_hour)))].sort((a,b)=>a-b);
 document.querySelector('#hourSubtitle').textContent=`${monthLabel(m)} · ${citySelect.value==='All'?'All cities':citySelect.value}`;
 const hourSeries=(citySelect.value==='All'?cities:[citySelect.value]).map((city,i)=>({name:city,color:COLORS[i%COLORS.length],points:hours.map((h,xi)=>{const r=hourRows.find(d=>d.city===city&&Number(d.source_accept_hour)===h);return {xi,y:r?Number(r[hourMode==='median'?'median_elapsed_min':'p90_elapsed_min']):NaN,count:r?Number(r.package_count):0}})}));
 drawLines('#hourChart','#hourLegend',hourSeries,hours,{xLabel:'source acceptance hour',yLabel:hourMode==='median'?'Median':'P90',xTick:x=>String(x).padStart(2,'0')+':00'});
 const reg=DATA.regionMonth.filter(r=>Number(r.accept_month)===m&&(citySelect.value==='All'||r.city===citySelect.value)).sort((a,b)=>Number(b.p90_elapsed_min)-Number(a.p90_elapsed_min)).slice(0,15);
 document.querySelector('#regionRows').innerHTML=reg.length?reg.map(r=>`<tr><td>${r.city} · ${r.region_id}</td><td>${fmt(r.package_count)}</td><td>${minfmt(r.median_elapsed_min)}</td><td>${minfmt(r.p90_elapsed_min)}</td><td>${fmt(r.over_24h_count)}</td></tr>`).join(''):'<tr><td colspan="5" class="empty">No regions for this selection.</td></tr>';
}
render();
</script></body></html>'''.replace('__DATA__', payload)
OUT.write_text(html, encoding='utf-8')
print(f'Wrote {OUT} ({OUT.stat().st_size:,} bytes); embedded {len(city_month)} city-month, {len(city_hour)} city-hour, and {len(region_month)} region-month aggregates.')

