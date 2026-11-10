#!/usr/bin/env python3
"""Build self-contained profile SVGs. Run from any directory with Python 3.

Layout inspired by https://github.com/Sharann-del/Sharann-del.
All artwork is drawn here; profile content and links belong to araxis07.
No network calls, external fonts or runtime dependencies. Quantitative artwork
uses the reviewed public GitHub snapshot in data/github-stats.json.
"""
from pathlib import Path
from html import escape
import textwrap
import json
import math
from collections import Counter
from system_map import render_system_map

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'assets' / 'index'
STATS = json.loads((ROOT / 'data' / 'github-stats.json').read_text())
HIGHLIGHTS = json.loads((ROOT / 'data' / 'portfolio-highlights.json').read_text())
SYSTEM_MAP = json.loads((ROOT / 'data' / 'system-map.json').read_text())

PROJECTS = [
    ('Siam Luxe', 'Siam-Luxe', 'FULL-STACK COMMERCE',
     'Multilingual Thai dining platform with ordering, reservations, member accounts and admin workflows.',
     'Next.js / TypeScript / Supabase / PostgreSQL',
     'Product foundation; live provider setup and deployment remain.'),
    ('AI Knowledge Base', 'AI-Knowledge', 'DOCUMENT INTELLIGENCE',
     'Private document workspaces, hybrid search and grounded AI answers with visible source citations.',
     'Next.js / Supabase / pgvector / Playwright',
     'Live AI flows require provider configuration.'),
    ('Nexus Tech', 'Nexus-Tech', 'TERMINAL SIMULATION',
     'Offline business simulation with deterministic systems, company strategy, campaigns and SQLite saves.',
     'Python / Rich / Typer / SQLite',
     'Stable Alpha; human playtesting and pacing validation remain.'),
    ('Finance Dashboard', 'finance-dashboard', 'FINTECH FRONTEND',
     'Income, expense and transaction views with category charts, file upload UI and local persistence.',
     'Next.js / Tailwind CSS / Zustand / Recharts',
     'Frontend MVP; parsing is mocked and data stays local.'),
    ('Sakura Trails', 'Japan-sakura-trails', 'JAPAN TRAVEL',
     'Japan travel guide with 93 destinations, four languages, a seasonal 3D landscape and local trip planning.',
     'React / TypeScript / Three.js / Leaflet',
     'Local-first guide and planner; no booking service.'),
    ('Roam America', 'usa-travel-planner', 'USA TRAVEL',
     'Explore all 50 U.S. states in five languages with daily itineraries, offline guides and local trip planning.',
     'React / TypeScript / Vite / optional Supabase',
     'Local planning needs no account; cloud services are optional.'),
]

PALETTES = {
    'dark': dict(bg='#0b0d17', ink='#eff1ff', muted='#a7b0cb', rule='#30364f',
                 accent='#b6a0ff', cyan='#65d9ed', pink='#ee9bc8', soft='#151729'),
    'light': dict(bg='#faf9ff', ink='#232339', muted='#565e77', rule='#d2d3e4',
                  accent='#6743b4', cyan='#086d85', pink='#a93072', soft='#eeeaf8'),
}

def t(x, y, value, size=16, color='ink', extra=''):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="var(--{color})" {extra}>{escape(value)}</text>'

def line(x1, y1, x2, y2, cls='', color='rule'):
    return f'<path d="M{x1} {y1}H{x2}" stroke="var(--{color})" class="{cls}"/>' if y1 == y2 else f'<path d="M{x1} {y1}L{x2} {y2}" stroke="var(--{color})" class="{cls}"/>'

def wrap(x, y, value, width, size=16, color='ink', leading=25):
    lines = textwrap.wrap(value, width)
    return ''.join(t(x, y+i*leading, s, size, color) for i, s in enumerate(lines)), y+len(lines)*leading

def svg(name, width, height, body, theme, mobile, label):
    p=PALETTES[theme]
    css=':root{'+''.join(f'--{k}:{v};' for k,v in p.items())+'}'
    css+='''text{font-family:"SFMono-Regular",Consolas,"Liberation Mono",monospace}
    .flow{stroke-dasharray:3 10;animation:flow 3s linear infinite}
    .cursor{animation:cursor 1.5s steps(1) infinite}
    .breathe{animation:breathe 4s ease-in-out infinite}
    @keyframes flow{to{stroke-dashoffset:-26}}
    @keyframes cursor{50%{opacity:.18}}
    @keyframes breathe{50%{opacity:.45}}
    @media(prefers-reduced-motion:reduce){.flow,.cursor,.breathe{animation:none}}
    '''
    doc=f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}" role="img" aria-label="{escape(label,quote=True)}">
    <title>{escape(label)}</title><style>{css}</style>
    <rect width="{width}" height="{height}" fill="var(--bg)"/>{body}</svg>\n'''
    # Explicit colors also render in image proxies and non-browser SVG readers.
    for key,value in p.items():doc=doc.replace(f'var(--{key})',value)
    target=ASSETS/theme/('mobile' if mobile else 'desktop')/f'{name}.svg'
    target.parent.mkdir(parents=True,exist_ok=True)
    target.write_text(doc)

def build(theme, mobile):
    w=440 if mobile else 1000
    left=22 if mobile else 48
    right=w-left
    def save(name,height,body,label): svg(name,w,height,body,theme,mobile,label)
    def rule(y, cls='', color='rule'):return line(left,y,right,y,cls,color)
    body=t(left,30,'ARAXIS07 / DEVELOPER INDEX',11,'muted', 'letter-spacing="1.5"')+rule(44)
    if mobile:
        body+=t(left,84,'Pavornprat',28)+t(left,119,'Mokarat',28)
        body+=t(left,150,'AON / FULL-STACK DEVELOPER',13,'accent')
        body+=t(left,176,'THAILAND → TOKYO, JAPAN',12,'muted')
        body+=rule(195)
        body+=t(left,222,'Interfaces. APIs. Data. Ideas.',14)
        body+=t(left,245,'Built with curiosity and intent.',13,'muted')
        body+=f'<rect x="{right-9}" y="232" width="7" height="14" fill="var(--cyan)" class="cursor"/>'
        height=264
    else:
        body+=t(right,30,'THAILAND → TOKYO, JAPAN',11,'muted','text-anchor="end" letter-spacing="1.2"')
        body+=t(left,103,'Pavornprat Mokarat',42,extra='letter-spacing="-1"')
        body+=t(left,135,'AON / FULL-STACK DEVELOPER',16,'accent','letter-spacing=".8"')
        body+=t(left,175,'Interfaces. APIs. Data. Ideas.',15)
        body+=t(left,201,'Building thoughtful digital products with curiosity and intent.',14,'muted')
        body+=rule(225)
        body+=t(left,251,'WEB SYSTEMS',11,'accent','letter-spacing="1.6"')
        body+=t(300,251,'DATA & VISUALIZATION',11,'cyan','letter-spacing="1.6"')
        body+=t(644,251,'CREATIVE ENGINEERING',11,'pink','letter-spacing="1.6"')
        body+=f'<rect x="{right-9}" y="238" width="7" height="15" fill="var(--cyan)" class="cursor"/>'
        height=270
    save('header',height,body,'Pavornprat Mokarat / Aon / Full-Stack Developer from Thailand, based in Tokyo, Japan')

    for n,title,path in [(1,'WHOAMI','identity'),(2,'SYSTEM MAP','work'),(3,'PROJECTS','selected'),(4,'TELEMETRY','activity'),(5,'THE ROUTE','journey'),(6,'STACK','tools')]:
        b=rule(13)+t(left,47,f'{n:02}',24,'accent')
        b+=t(left+50,44,title,14,extra='letter-spacing="1.7"')
        if not mobile:b+=t(right,44,'~/'+path,11,'muted','text-anchor="end"')
        save(f's{n:02}',64,b,f'{n:02} / {title}')

    width=42 if mobile else 96
    body=''; y=27
    for text,color in [
        ('Hello, I’m Aon — a developer who enjoys turning complex ideas into practical digital products.','ink'),
        ('B.Sc. Information Technology, Thai-Nichi Institute of Technology. Second-Class Honors.','ink'),
        ('My work spans frontend interfaces, backend APIs, dashboards and data-rich experiences.','muted'),
    ]:
        s,y=wrap(left,y,text,width,15,color,23);body+=s;y+=10
    body+=rule(y);y+=28
    s,y=wrap(left,y,'LEARNING / Go, Rust and Japanese.',width,14,'accent',23);body+=s;y+=8
    s,y=wrap(left,y,'LONG-TERM LANGUAGE GOAL / JLPT N2.',width,14,'muted',23);body+=s
    save('whoami',y+12,body,'About Aon: TNI Information Technology graduate with Second-Class Honors; building web products, learning Go, Rust and Japanese, with JLPT N2 as a long-term goal')

    # A rooted portfolio-category tree with six independent project leaves.
    target = ASSETS/theme/('mobile' if mobile else 'desktop')/'ecosystem.svg'
    target.parent.mkdir(parents=True,exist_ok=True)
    target.write_text(render_system_map(SYSTEM_MAP, theme, mobile))

    for i,(name,repo,category,description,stack,status) in enumerate(PROJECTS,1):
        body=t(left,22,f'{i:02} / {category}',11,'accent','letter-spacing="1"')
        body+=t(left,50,name,19 if mobile else 20)
        if not mobile:body+=t(right,50,'↗',18,'cyan','text-anchor="end"')
        b,y=wrap(left,78,description,42 if mobile else 96,15,'ink',23);body+=b;y+=7
        b,y=wrap(left,y,stack,43 if mobile else 100,13,'cyan',21);body+=b;y+=6
        b,y=wrap(left,y,status,45 if mobile else 110,12,'muted',20);body+=b
        body+=rule(y+1)
        save(f'project-{i:02}',y+12,body,f'{name}. {description} Stack: {stack}. Status: {status}')

    # Counts describe the six cards above; no invented velocity, scores or activity.
    stats=[('06','FEATURED PROJECTS','Documented in this profile.'),('02','TRAVEL EXPERIENCES','Japan and the United States.'),('01','TERMINAL SIMULATION','Nexus Tech / Stable Alpha.')]
    body=t(left,25,'PORTFOLIO AT A GLANCE',12,'muted','letter-spacing="2"')+rule(43)
    for i,(value,label,caption) in enumerate(stats):
        x=left if mobile else left+i*312;y=75+i*90 if mobile else 84
        body+=t(x,y+18,value,28,'accent')+t(x+68,y+1,label,12)
        if mobile:body+=t(x+68,y+24,caption,11,'muted')
        else:body+=t(x,y+50,caption,12,'muted')
    height=345 if mobile else 177
    body+=rule(height-33)+t(left,height-12,'SCOPE COUNTS / NOT LIVE GITHUB STATISTICS',9 if mobile else 11,'muted','letter-spacing=".4"')
    save('signals',height,body,'Portfolio scope: six featured projects, two travel experiences and one terminal simulation. These are scope counts, not live GitHub activity statistics.')

    body='';y=31
    for entry in HIGHLIGHTS['route']:
        label,title,description = (entry[key] for key in ('label','title','description'))
        body+=t(left,y,label,12,'accent','letter-spacing="1"');y+=27
        b,y=wrap(left,y,title,36 if mobile else 90,17,'ink',24);body+=b;y+=5
        b,y=wrap(left,y,description,42 if mobile else 96,15,'muted',23);body+=b;y+=4
        body+=rule(y);y+=27
    save('route',y-5,body,'Journey: TNI Information Technology 2021–2025, GPAX 3.45 and Second-Class Honors; Teaching Assistant June 2021–October 2024; four-month Suvarnabhumi Airport IT Support internship December 2024–March 2025; Akamonkai Japanese Language School, Tokyo, January–December 2026. JLPT N2 is a learning goal.')

    groups=[
        ('LANGUAGES',['TypeScript / JavaScript / Python','Go / Rust / Ruby / SQL']),
        ('FRONTEND',['Next.js / React / Tailwind CSS','Material UI / HTML / CSS']),
        ('BACKEND',['Node.js / NestJS / Express','REST APIs / Authentication']),
        ('DATA & STORAGE',['PostgreSQL / Supabase / MySQL','SQLite / pgvector / Recharts']),
        ('TESTING & QUALITY',['Playwright / Postman','E2E testing / API testing']),
        ('DELIVERY & TOOLS',['Git / GitHub / GitHub Actions','CI/CD pipelines / Docker / Vite']),
    ]
    body=''
    for i,(label,rows) in enumerate(groups):
        x=left if mobile else left+(i%2)*464;y=29+i*118 if mobile else 29+(i//2)*122
        body+=t(x,y,label,12,'accent','letter-spacing="2"')
        for j,row in enumerate(rows):body+=t(x,y+31+j*25,row,14,'ink' if j==0 else 'muted')
        body+=line(x,y+94,right if mobile else x+422,y+94)
    save('stack',736 if mobile else 379,body,'Technical stack: ' + '; '.join(label + ': ' + ', '.join(rows) for label,rows in groups))

    body=rule(20,'','accent')
    body+=t(left,51,'STAY CURIOUS. BUILD WITH INTENT.',14 if mobile else 17,'accent')
    body+=t(left,77,'Code / data / finance / Japanese / new experiences',11 if mobile else 14,'muted')
    body+=t(left,104,'ARAXIS07 / BUILDING BEYOND THE HORIZON',10 if mobile else 11,'muted','letter-spacing=".5"')
    save('footer',122,body,'Stay curious. Build with intent. Aon / araxis07 / building beyond the horizon')

def build_telemetry(theme):
    repos=STATS['repositories']
    assert repos and all(not r['private'] for r in repos)
    assert len({r['full_name'] for r in repos}) == len(repos)
    langs=Counter(r['language'] or 'Unclassified' for r in repos)
    years=Counter(r['created_at'][:4] for r in repos)
    n=len(repos)
    date=STATS['snapshot_date']
    ordered=sorted(langs.items(), key=lambda x:(-x[1],x[0]))
    # Quantitative bar lengths start at zero; direct labels carry count/share.
    body=t(48,27,'PUBLIC GITHUB TELEMETRY',12,'accent','letter-spacing="1.6"')
    body+=t(952,27,'SNAPSHOT / '+date,11,'muted','text-anchor="end"')+line(48,43,952,43)
    body+=t(48,76,'PRIMARY LANGUAGES',13)+t(48,99,f'Repository count / share of {n} public repos',11,'muted')
    maxlang=max(langs.values())
    start=130;step=28
    for i,(lang,count) in enumerate(ordered):
        y=start+i*step
        body+=t(48,y,lang,13)
        body+=f'<rect x="165" y="{y-9}" width="220" height="8" fill="var(--soft)"/>'
        body+=f'<rect x="165" y="{y-9}" width="{220*count/maxlang:.3f}" height="8" fill="var(--accent)"/>'
        body+=t(480,y,f'{count} / {100*count/n:.1f}%',12,'muted','text-anchor="end"')
    axis_y=start+(len(ordered)-1)*step+24
    body+=line(165,axis_y,385,axis_y)+t(165,axis_y+18,'0',11,'muted')
    body+=t(385,axis_y+18,str(maxlang)+' repos',11,'muted','text-anchor="end"')

    body+=line(516,66,516,axis_y+20)
    body+=t(548,76,'REPOSITORIES CREATED',13)+t(548,99,'Current public set / grouped by creation year',11,'muted')
    year_rows=sorted(years.items())
    chart_left,chart_right,baseline,chart_h=580,936,381,240
    tick_step=max(5,math.ceil(max(years.values())/15)*5)
    ceiling=tick_step*3
    for i in range(4):
        value=tick_step*i;y=baseline-chart_h*value/ceiling
        body+=line(chart_left,y,chart_right,y)
        body+=t(565,y+4,str(value),11,'muted','text-anchor="end"')
    band=(chart_right-chart_left)/len(year_rows)
    bar_width=min(48,band*.6)
    for i,(year,count) in enumerate(year_rows):
        x=chart_left+band*(i+.5);height=chart_h*count/ceiling
        body+=f'<rect x="{x-bar_width/2:.2f}" y="{baseline-height:.2f}" width="{bar_width:.2f}" height="{height:.2f}" fill="var(--cyan)"/>'
        body+=t(x,baseline-height-11,str(count),14,'ink','text-anchor="middle"')
        body+=t(x,baseline+26,year,12,'muted','text-anchor="middle"')
    bottom=max(axis_y+55,466)
    body+=line(48,bottom,952,bottom)
    body+=t(48,bottom+25,'One primary language per repository. Percentages describe repository shares.',11,'muted')
    body+=t(48,bottom+46,'Creation year is taken from the current public repository set. Public-data snapshot.',11,'muted')
    label='Public GitHub snapshot '+date+'. Primary languages: '+', '.join(f'{k}: {v} repositories ({100*v/n:.1f} percent)' for k,v in ordered)+'. Repositories by creation year: '+', '.join(f'{y}: {v}' for y,v in year_rows)+'.'
    svg('telemetry',1000,bottom+65,body,theme,False,label)

    body=t(48,28,'GITHUB STATS',13,'accent','letter-spacing="1.6"')
    body+=t(952,28,'PUBLIC DATA / '+date,11,'muted','text-anchor="end"')+line(48,45,952,45)
    metrics=[
        (n,'PUBLIC REPOSITORIES','Owned by araxis07'),
        (len([k for k in langs if k!='Unclassified']),'PRIMARY LANGUAGES','GitHub repository labels'),
        (len(PROJECTS),'FEATURED PROJECTS','Documented in this profile'),
        (sum(r['stars'] for r in repos),'REPOSITORY STARS','Across owned public repos'),
        (STATS['authored_public_pull_requests'],'PUBLIC PRs AUTHORED','Across public GitHub repos'),
        (STATS['authored_public_issues'],'PUBLIC ISSUES AUTHORED','Across public GitHub repos'),
    ]
    for i,(value,label,caption) in enumerate(metrics):
        x=48+(i%3)*312;y=93+(i//3)*89
        body+=t(x,y,str(value),28,'accent')+t(x+65,y-11,label,11)
        body+=t(x+65,y+11,caption,10,'muted')
    body+=line(48,218,952,218)+t(48,242,'Snapshot values / source data and counting definitions are linked below.',11,'muted')
    svg('github-stats',1000,262,body,theme,False,'Public GitHub stats as of '+date+': '+', '.join(f'{v} {label.lower()}' for v,label,_ in metrics)+'.')

def picture(name,alt):
    base=f'assets/index'
    # GitHub's themed README rendering must select only between equal canvases.
    # A narrow-layout source can be promoted by its theme and then stretched
    # across the profile overview. Keep both theme sources at viewBox 1000.
    return f'''<picture>
  <source media="(prefers-color-scheme: dark)" srcset="{base}/dark/desktop/{name}.svg" />
  <img src="{base}/light/desktop/{name}.svg" width="100%" alt="{escape(alt,quote=True)}" />
</picture>'''

def project_details(project):
    parts = [
        '<details>',
        '<summary><strong>'+escape(project['name'])+' · role, engineering &amp; evidence</strong></summary>',
        '',
        '**My role**', '', project['role'], '',
        '**Engineering**', '', project['approach'], '',
        '**Scope**', '',
        ' · '.join(metric['label']+': '+metric['value'] for metric in project['metrics']), '',
        '**Delivered**', '',
        '\n'.join('- '+item for item in project['delivered']), '',
        '**Current status**', '', project['status'], '',
    ]
    if project['screenshots']:
        parts += ['**Interface screenshots**', '']
        for shot in project['screenshots']:
            parts += [
                '<p><img src="'+escape(shot['src'],quote=True)+'" width="460" alt="'+escape(shot['alt'],quote=True)+'" /><br /><sub>'+escape(shot['caption'])+'</sub></p>', ''
            ]
    dialog_id = next(p['case_study'] for branch in SYSTEM_MAP['branches'] for p in branch['projects'] if project['repository'].rstrip('/').endswith('/'+p['repo']))
    parts += ['[View source code]('+project['repository']+') · [Read this case study](https://araxis07.github.io/#'+dialog_id+')', '', '</details>']
    return '\n'.join(parts)

def credentials_and_languages():
    parts = ['<details>', '<summary><strong>Selected credentials, competitions &amp; languages</strong></summary>', '', '**Credentials & competitions**', '']
    parts += ['- '+item['year']+' — '+item['name'] for item in HIGHLIGHTS['credentials']]
    parts += ['', '**Languages**', '']
    parts += ['- **'+item['name']+':** '+item['level'] for item in HIGHLIGHTS['languages']]
    parts += ['', '</details>']
    return '\n'.join(parts)

def project_branches():
    parts = ['<details>', '<summary><strong>Explore the project branches</strong></summary>', '']
    for branch in SYSTEM_MAP['branches']:
        links = ' · '.join('['+p['name']+'](https://github.com/araxis07/'+p['repo']+')' for p in branch['projects'])
        parts += ['- **'+branch['label'].title()+':** '+links]
    parts += ['', '</details>']
    return '\n'.join(parts)

def readme():
    parts=['<!-- ARAXIS07 / Developer Index. Generated by scripts/build_profile.py. -->','<div align="center">',picture('header','Pavornprat Mokarat — Aon / Full-Stack Developer / Thailand → Tokyo, Japan'),'<br />']
    buttons=[('PORTFOLIO','https://araxis07.github.io','7C3AED'),('REPOSITORIES','https://github.com/araxis07?tab=repositories','DB2777'),('RESUME','https://canva.link/j33ybwperioom0j','0891B2'),('LINKEDIN','https://www.linkedin.com/in/pavornprat/','0A66C2'),('EMAIL','mailto:pavornprat.aa@gmail.com','7C3AED')]
    badge_dir=ASSETS/'buttons'
    badge_dir.mkdir(parents=True,exist_ok=True)
    for label,url,color in buttons:
        (badge_dir/f'{label.lower()}.svg').write_text(f'''<svg xmlns="http://www.w3.org/2000/svg" width="138" height="34" viewBox="0 0 138 34" role="img" aria-label="{label.title()}"><title>{label.title()}</title><rect x=".5" y=".5" width="137" height="33" rx="3" fill="#141525" stroke="#{color}"/><path d="M1 7V27" stroke="#{color}" stroke-width="2"/><text x="69" y="21.5" fill="#f1efff" text-anchor="middle" font-family="Consolas,monospace" font-size="11" letter-spacing="1.1">{label}</text></svg>\n''')
    # Keep anchors in one HTML block so GitHub lays them out side by side.
    parts += ['\n'.join(f'<a href="{url}"><img src="assets/index/buttons/{label.lower()}.svg" width="138" height="34" alt="{label.title()}" /></a>' for label,url,color in buttons)]
    parts+=['</div>', '''**Pavornprat Mokarat (Aon) · Full-Stack Developer**

I build web products, backend workflows, and data-rich interfaces with Next.js, React, TypeScript, Node.js, PostgreSQL, and Supabase. B.Sc. Information Technology, Thai-Nichi Institute of Technology · Second-Class Honors · GPAX 3.45.

**Start with a case study:** [Siam Luxe — full-stack workflows](https://araxis07.github.io/#case-study-siam) · [AI Knowledge Base — document retrieval](https://araxis07.github.io/#case-study-ai) · [Roam America — travel planning](https://araxis07.github.io/#case-study-usa)

[Contact me](mailto:pavornprat.aa@gmail.com) · [LinkedIn](https://www.linkedin.com/in/pavornprat/)
''',picture('s01','01 / whoami'),picture('whoami','TNI Information Technology graduate with Second-Class Honors. Frontend, backend APIs and data interfaces. Learning Go, Rust and Japanese; JLPT N2 is a long-term goal.'),picture('s02','02 / system map'),picture('ecosystem','System Map: web products — Siam Luxe and AI Knowledge Base; data interfaces — Finance Dashboard; travel experiences — Sakura Trails and Roam America; terminal systems — Nexus Tech.'),project_branches(),picture('s03','03 / projects')]
    for i,(name,repo,category,description,stack,status) in enumerate(PROJECTS,1):
        parts += [f'<a href="https://github.com/araxis07/{repo}">\n'+picture(f'project-{i:02}',f'{name} — {description} {status} Open repository.')+'\n</a>']
        parts += [project_details(HIGHLIGHTS['projects'][i-1])]
    parts+=['<p align="right"><a href="https://araxis07.github.io"><strong>View case studies on my portfolio →</strong></a></p>',
    '<details>\n<summary><strong>More projects from my previous profile</strong></summary>\n\n- [Japan Travel Guide](https://github.com/araxis07/Website-Japan)\n- [Sitcam Project](https://github.com/araxis07/Sitcam-Project)\n\n</details>',
    picture('s04','04 / telemetry'),
    picture('telemetry','Public GitHub snapshot '+STATS['snapshot_date']+': primary language distribution by repository count and public repositories grouped by creation year.'),
    picture('github-stats','Public GitHub statistics: repository count, primary languages, featured projects, repository stars, authored public pull requests and authored public issues.'),
    '''<details>
<summary><strong>Data sources and counting definitions</strong></summary>

- [Public GitHub snapshot and source URLs](data/github-stats.json)
- Language shares count each current public repository once, using GitHub's primary-language label.
- Creation-year bars group the current public repositories by their creation date.
- Stars cover owned public repositories; authored PR and issue totals cover public GitHub repositories.
- [How to refresh the snapshot](docs/telemetry.md)

</details>''',
    picture('s05','05 / the route'),picture('route','TNI B.Sc. Information Technology 2021–2025, GPAX 3.45, Second-Class Honors. Teaching Assistant June 2021–October 2024. Four-month IT Support internship at Suvarnabhumi Airport December 2024–March 2025. Akamonkai Japanese Language School, Tokyo, January–December 2026; JLPT N2 is a learning goal.'),credentials_and_languages(),picture('s06','06 / stack'),picture('stack','Languages: TypeScript, JavaScript, Python, Go, Rust, Ruby, SQL. Frontend: Next.js, React, Tailwind CSS and Material UI. Backend: Node.js, NestJS and Express. Data: PostgreSQL, Supabase, MySQL, SQLite and pgvector. Testing: Playwright and Postman. Delivery: Git, GitHub, GitHub Actions, CI/CD pipelines, Docker and Vite.')]
    parts+=['''**Core:** Next.js · React · TypeScript · JavaScript · Node.js · Tailwind CSS · PostgreSQL · Supabase

**Supporting tools & languages:** Python · Ruby · SQL · Git / GitHub · Playwright · Postman · GitHub Actions · CI/CD pipelines

**Ongoing learning:** Go · Rust. The project details above show the technologies used in each build.

<details>
<summary><strong>Additional technologies</strong></summary>
<br />

`Python` `Java` `C` `C++` `C#` `Ruby` `Vue` `Angular` `Flutter` `Redux` `Chart.js` `FastAPI` `Flask` `MongoDB` `NumPy` `TensorFlow` `AWS` `Linux` `Vercel` `Figma` `Arduino` `Unity`

Go and Rust are part of my ongoing learning.

</details>''',picture('footer','Stay curious. Build with intent. ARAXIS07 / building beyond the horizon'),'''<div align="center">
  <a href="mailto:pavornprat.aa@gmail.com">Start a conversation</a> ·
  <a href="https://canva.link/j33ybwperioom0j">View resume</a> ·
  <a href="https://araxis07.github.io">Visit portfolio</a> ·
  <a href="https://github.com/araxis07?tab=repositories">Explore code</a> ·
  <a href="https://www.linkedin.com/in/pavornprat/">LinkedIn</a>
</div>''']
    return '\n\n'.join(parts)+'\n'

if __name__=='__main__':
    for theme in PALETTES:
        for mobile in (False,True):build(theme,mobile)
        build_telemetry(theme)
    (ROOT/'README.md').write_text(readme())
    print(f'Generated README and {len(list(ASSETS.rglob("*.svg")))} SVGs.')
