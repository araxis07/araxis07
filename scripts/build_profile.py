#!/usr/bin/env python3
"""Build self-contained profile SVGs. Run from any directory with Python 3.

Layout inspired by https://github.com/Sharann-del/Sharann-del.
All artwork is drawn here; profile content and links belong to araxis07.
No network calls, generated statistics, external fonts or runtime dependencies.
"""
from pathlib import Path
from html import escape
import textwrap

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'assets' / 'index'

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

    for n,title,path in [(1,'WHOAMI','identity'),(2,'SYSTEM MAP','work'),(3,'PROJECTS','selected'),(4,'SIGNALS','scope'),(5,'THE ROUTE','journey'),(6,'STACK','tools')]:
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

    # A map of portfolio categories, not an architecture or runtime-data claim.
    body=t(left,25,'PROJECT ECOSYSTEM',12,'muted','letter-spacing="2"')
    body+=rule(41)
    if mobile:
        body+=f'<rect x="110" y="62" width="220" height="60" rx="2" fill="var(--soft)" stroke="var(--accent)"/>'
        body+=t(220,89,'ARAXIS07.SYS',16,'accent','text-anchor="middle"')+t(220,110,'selected work / 6 projects',12,'muted','text-anchor="middle"')
        nodes=[(22,166,'WEB PRODUCTS','Siam Luxe / AI Knowledge'),(22,258,'DATA INTERFACES','Finance Dashboard'),(22,350,'TRAVEL EXPERIENCES','Sakura Trails / Roam America'),(22,442,'TERMINAL SYSTEMS','Nexus Tech')]
        for x,y,title,sub in nodes:
            body+=f'<rect x="{x}" y="{y}" width="396" height="72" rx="2" fill="var(--bg)" stroke="var(--rule)"/>'
            body+=t(x+16,y+29,title,14,'cyan')+t(x+16,y+54,sub,13,'muted')
        body+='<path d="M110 92H37V166" fill="none" stroke="var(--accent)" class="flow"/>'
        for a,b in [(238,258),(330,350),(422,442)]:body+=line(37,a,37,b,'flow','accent')
        height=540
    else:
        for y in (122,300):body+=line(288,y,712,y,'flow','accent')
        body+=line(500,122,500,300,'flow','accent')
        for x,y,title,sub in [(48,87,'WEB PRODUCTS','Siam Luxe / AI Knowledge'),(672,87,'DATA INTERFACES','Finance Dashboard'),(48,265,'TRAVEL EXPERIENCES','Sakura Trails / Roam America'),(672,265,'TERMINAL SYSTEMS','Nexus Tech')]:
            body+=f'<rect x="{x}" y="{y}" width="280" height="76" rx="2" fill="var(--bg)" stroke="var(--rule)"/>'
            body+=t(x+17,y+30,title,14,'cyan')+t(x+17,y+56,sub,12,'muted')
        body+=f'<rect x="379" y="181" width="242" height="70" rx="2" fill="var(--soft)" stroke="var(--accent)"/>'
        body+=t(500,210,'ARAXIS07.SYS',17,'accent','text-anchor="middle"')+t(500,234,'selected work / 6 projects',12,'muted','text-anchor="middle"')
        height=379
    save('ecosystem',height,body,'Portfolio map: web products — Siam Luxe and AI Knowledge; data interfaces — Finance Dashboard; travel — Sakura Trails and Roam America; terminal simulation — Nexus Tech')

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
    entries=[('EDUCATION / 2025','Thai-Nichi Institute of Technology','B.Sc. Information Technology / Second-Class Honors.'),('EXPERIENCE / 4 MONTHS','IT Support Intern / Suvarnabhumi Airport','Computer-system troubleshooting, operational support and a data-visualization dashboard.'),('CURRENT CHAPTER / 2026','Tokyo, Japan','Studying Japanese while continuing to explore software, data and new experiences.')]
    for label,title,description in entries:
        body+=t(left,y,label,12,'accent','letter-spacing="1"');y+=27
        b,y=wrap(left,y,title,36 if mobile else 90,17,'ink',24);body+=b;y+=5
        b,y=wrap(left,y,description,42 if mobile else 96,15,'muted',23);body+=b;y+=4
        body+=rule(y);y+=27
    save('route',y-5,body,'Journey: TNI Information Technology graduate in 2025, four-month IT Support internship at Suvarnabhumi Airport, and Japanese study in Tokyo in 2026')

    groups=[('FRONTEND',['React / Next.js / TypeScript','JavaScript / Tailwind CSS / Material UI']),('BACKEND',['Node.js / NestJS / Express','REST APIs / Authentication']),('DATA',['PostgreSQL / MySQL / Supabase','SQLite / pgvector / Recharts']),('WORKFLOW',['Git / GitHub Actions / Docker','Playwright / Vite / Postman'])]
    body=''
    for i,(label,rows) in enumerate(groups):
        x=left if mobile else left+(i%2)*464;y=29+i*118 if mobile else 29+(i//2)*122
        body+=t(x,y,label,12,'accent','letter-spacing="2"')
        for j,row in enumerate(rows):body+=t(x,y+31+j*25,row,14,'ink' if j==0 else 'muted')
        body+=line(x,y+94,right if mobile else x+422,y+94)
    save('stack',500 if mobile else 257,body,'Technical stack includes React, Next.js, TypeScript, JavaScript, Tailwind CSS, Material UI, Node.js, NestJS, Express, REST APIs, authentication, PostgreSQL, MySQL, Supabase, SQLite, pgvector, Recharts, Git, GitHub Actions, Docker, Playwright, Vite and Postman')

    body=rule(20,'','accent')
    body+=t(left,51,'STAY CURIOUS. BUILD WITH INTENT.',14 if mobile else 17,'accent')
    body+=t(left,77,'Code / data / finance / Japanese / new experiences',11 if mobile else 14,'muted')
    body+=t(left,104,'ARAXIS07 / BUILDING BEYOND THE HORIZON',10 if mobile else 11,'muted','letter-spacing=".5"')
    save('footer',122,body,'Stay curious. Build with intent. Aon / araxis07 / building beyond the horizon')

def picture(name,alt):
    base=f'assets/index'
    return f'''<picture>
  <source media="(prefers-color-scheme: dark) and (max-width: 600px)" srcset="{base}/dark/mobile/{name}.svg" />
  <source media="(max-width: 600px)" srcset="{base}/light/mobile/{name}.svg" />
  <source media="(prefers-color-scheme: dark)" srcset="{base}/dark/desktop/{name}.svg" />
  <img src="{base}/light/desktop/{name}.svg" width="100%" alt="{escape(alt,quote=True)}" />
</picture>'''

def readme():
    parts=['<!-- ARAXIS07 / Developer Index. Generated by scripts/build_profile.py. -->','<div align="center">',picture('header','Pavornprat Mokarat — Aon / Full-Stack Developer / Thailand → Tokyo, Japan'),'<br />']
    buttons=[('PORTFOLIO','https://araxis07.github.io','7C3AED'),('REPOSITORIES','https://github.com/araxis07?tab=repositories','DB2777'),('RESUME','https://canva.link/j33ybwperioom0j','0891B2'),('EMAIL','mailto:pavornprat.aa@gmail.com','7C3AED')]
    badge_dir=ASSETS/'buttons'
    badge_dir.mkdir(parents=True,exist_ok=True)
    for label,url,color in buttons:
        (badge_dir/f'{label.lower()}.svg').write_text(f'''<svg xmlns="http://www.w3.org/2000/svg" width="138" height="34" viewBox="0 0 138 34" role="img" aria-label="{label.title()}"><title>{label.title()}</title><rect x=".5" y=".5" width="137" height="33" rx="3" fill="#141525" stroke="#{color}"/><path d="M1 7V27" stroke="#{color}" stroke-width="2"/><text x="69" y="21.5" fill="#f1efff" text-anchor="middle" font-family="Consolas,monospace" font-size="11" letter-spacing="1.1">{label}</text></svg>\n''')
    # Keep anchors in one HTML block so GitHub lays them out side by side.
    parts += ['\n'.join(f'<a href="{url}"><img src="assets/index/buttons/{label.lower()}.svg" width="138" height="34" alt="{label.title()}" /></a>' for label,url,color in buttons)]
    parts+=['</div>',picture('s01','01 / whoami'),picture('whoami','TNI Information Technology graduate with Second-Class Honors. Frontend, backend APIs and data interfaces. Learning Go, Rust and Japanese; JLPT N2 is a long-term goal.'),picture('s02','02 / system map'),picture('ecosystem','Six featured projects across web products, data interfaces, travel and terminal simulation.'),picture('s03','03 / projects')]
    for i,(name,repo,category,description,stack,status) in enumerate(PROJECTS,1):
        parts += [f'<a href="https://github.com/araxis07/{repo}">\n'+picture(f'project-{i:02}',f'{name} — {description} {status} Open repository.')+'\n</a>']
    parts+=['<p align="right"><a href="https://araxis07.github.io"><strong>View case studies on my portfolio →</strong></a></p>',
    '<details>\n<summary><strong>More projects from my previous profile</strong></summary>\n\n- [Japan Travel Guide](https://github.com/araxis07/Website-Japan)\n- [Sitcam Project](https://github.com/araxis07/Sitcam-Project)\n\n</details>',picture('s04','04 / signals'),picture('signals','Portfolio scope: six featured projects, two travel experiences and one terminal simulation. Not live GitHub statistics.'),picture('s05','05 / the route'),picture('route','TNI graduate in 2025. Four-month IT Support internship at Suvarnabhumi Airport. Studying Japanese in Tokyo in 2026.'),picture('s06','06 / stack'),picture('stack','React, Next.js, TypeScript, Node.js, NestJS, PostgreSQL, Supabase, Docker, GitHub Actions and more.')]
    parts+=['''<details>
<summary><strong>Additional technologies</strong></summary>
<br />

`Python` `Java` `C` `C++` `C#` `Ruby` `Vue` `Angular` `Flutter` `Redux` `Chart.js` `FastAPI` `Flask` `MongoDB` `NumPy` `TensorFlow` `AWS` `Linux` `Vercel` `Figma` `Arduino` `Unity`

Go and Rust are part of my ongoing learning.

</details>''',picture('footer','Stay curious. Build with intent. ARAXIS07 / building beyond the horizon'),'''<div align="center">
  <a href="mailto:pavornprat.aa@gmail.com">Start a conversation</a> ·
  <a href="https://canva.link/j33ybwperioom0j">View resume</a> ·
  <a href="https://araxis07.github.io">Visit portfolio</a> ·
  <a href="https://github.com/araxis07?tab=repositories">Explore code</a>
</div>''']
    return '\n\n'.join(parts)+'\n'

if __name__=='__main__':
    for theme in PALETTES:
        for mobile in (False,True):build(theme,mobile)
    (ROOT/'README.md').write_text(readme())
    print(f'Generated README and {len(list(ASSETS.rglob("*.svg")))} SVGs.')
