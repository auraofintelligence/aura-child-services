"""Build the public guide from its unchanged user-supplied DOCX and editorial metadata."""
from pathlib import Path
import hashlib, html, json, re, shutil, zipfile
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
BASE = 'https://auraofintelligence.github.io/aura-child-services/'
REPO = 'https://github.com/auraofintelligence/aura-child-services'
DOCNAME = 'Aura_Genesis_Children_and_Teens_Australian_Care.docx'
DOC = ROOT / 'documents' / DOCNAME
W = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
R = '{http://schemas.openxmlformats.org/officeDocument/2006/relationships}'
NS = {'w': W[1:-1]}
E = html.escape
OUT = ROOT
TODAY = '28 October 2026'

PAGES = [
 dict(id='index', nav='Welcome', title='Room to discover who you can become.', eyebrow='A FAIR GO IN THE AGE OF SUPERINTELLIGENCE', intro='Understand powerful AI, ask better questions and create something of your own. This proposal connects young people’s agency with ethical technology, trusted adults and real opportunities to grow.', start=1, end=9, image='creative-project-protopia-v3', image_alt='A fictional young person in purple directs a future-world game and explores AI choices with a trusted adult beside a colourful Aura display.'),
 dict(id='opportunity', nav='A wider opportunity', title='A future with more possibilities.', eyebrow='01 / OPPORTUNITY AND INTELLIGENCE', intro='The proposal connects everyday childhood opportunity with a wider question: how can young people share in the capabilities of increasingly powerful intelligence?', start=10,end=32),
 dict(id='personal-aura', nav='Aura and self understanding', title='Start with your own interests.', eyebrow='02 / PERSONAL AURA AND REFLECTION', intro='A supported computing station offers a place to make, learn and reflect. The young person brings the meaning; the record can change as their understanding grows.',start=33,end=55),
 dict(id='law-and-rights',nav='Understanding law',title='Understand the rules around you.',eyebrow='03 / LAW, HISTORY AND EVERYDAY CHOICES',intro='Follow a question to a readable source. Learn why a rule exists, whose decision it affects and what needs checking in the present setting.',start=56,end=78),
 dict(id='first-project',nav='A first project',title='Make something. Find your next step.',eyebrow='04 / FROM A FIRST ACTIVITY TO A GROWING INTEREST',intro='A small creative project can reveal what someone enjoys, what gets in the way and which person or resource would help them continue.',start=79,end=99),
 dict(id='family-and-identity',nav='Family, care and identity',title='Keep the relationships that matter.',eyebrow='05 / FAMILY, CARE, ADOPTION AND CULTURE',intro='A life can hold several important relationships. Chosen memories, useful information and cultural connections need room to retain their meaning through change.',start=100,end=111),
 dict(id='adult-opportunities',nav='Growing into adult life',title='A wider view of adult life.',eyebrow='06 / WORK, OWNERSHIP AND TIME',intro='Mentors, practical work experience, shared productive ownership and planned time for life offer different possibilities to investigate as young people grow into adulthood.',start=112,end=159,image='future-work-protopia-v3',image_alt='A fictional young adult and experienced mentor compare a robotic-gripper prototype with design records in a characterful advanced workshop.'),
 dict(id='community',nav='Contribution and wellbeing',title='Belong through shared everyday life.',eyebrow='07 / C-HOURS AND COMMUNITY',intro='A useful task, a shared meal or a welcoming invitation can connect people. Communities choose their recognition, while essential support remains independent of contribution.',start=160,end=183,image='community-mentorship-protopia-v3',image_alt='Fictional teenagers lead a robotics and digital community-model project with mentors, using purple, blue and gold technology details.'),
 dict(id='civic-futures',nav='2032 and civic futures',title='A local beginning. A long horizon.',eyebrow='08 / BRISBANE 2032 AND CIVIC STEWARDSHIP',intro='Local learning and a lasting volunteer network connect the Olympic horizon with young adults investigating the future of their communities, Earth and space.',start=184,end=220),
 dict(id='people-and-control',nav='People and personal control',title='Real people. Clear choices.',eyebrow='09 / RELATIONSHIPS, RIGHTS AND RESPONSIBILITY',intro='The young person can ask questions, correct a record and turn to accountable adults. Learning, recording, research and publication each need an understandable purpose and actual arrangements.',start=221,end=232),
 dict(id='development',nav='Developing the proposal',title='Begin where people can follow through.',eyebrow='10 / CARE SERVICES, FAMILIES AND SEPARATE SCHOOL PILOTS',intro='A useful pilot needs a willing host, time, support and something concrete to try. Young people help shape it, and what happens changes the next step.',start=233,end=252),
 dict(id='sources',nav='Sources and original document',title='Follow the proposal to its sources.',eyebrow='READING ROOM / EDITION AND EVIDENCE',intro='Read the unchanged original, follow every project and public-guidance reference, and distinguish the proposal from evidence about outcomes.',start=253,end=329),
 dict(id='connections',nav='Connected projects',title='Find the part you want to explore.',eyebrow='CONNECTIONS / DISTINCT PURPOSES',intro='Related projects offer background, tools and development directions. Each has its own scope and status; a link does not establish a service or partnership.'),
 dict(id='licence',nav='About and licence',title='Authorship, rights and this website.',eyebrow='PROJECT INFORMATION',intro='A public reading guide to Luke Nathan Hayes’s proposal, with the original document, exact source links and clearly identified concept artwork.'),
 dict(id='sitemap',nav='Sitemap',title='Choose your own route.',eyebrow='EVERY PAGE / ONE CONNECTED GUIDE',intro='Follow the chapters in sequence or begin with the question that matters to you.')
]

CONNECTIONS = [
 ('Verse Box','An assisted public introduction to personal Aura, learning and community participation.','https://auraofintelligence.github.io/aura-verse-box/'),
 ('Personal Aura','How an everyday Aura could develop with chosen records, practical control and continuity.','https://auraofintelligence.github.io/aura-verse-box/personal-aura.html'),
 ('Aura Genesis Protocol','The separate adult protocol and Geode development atlas. The children’s proposal uses Verse Box and excludes pressure treatment.','https://auraofintelligence.github.io/aura-genesis-geode-atlas/'),
 ('Adult teacher development','A sixty-day adult facilitator learning source. It is not a child participation requirement or a professional qualification.','https://auraofintelligence.github.io/aura-genesis-geode-atlas/teacher-training.html'),
 ('Community Hours','Verified voluntary human contribution and nonmonetary community recognition.','https://auraofintelligence.github.io/C-Hour-introduction/'),
 ('Mutual Futures: work and life','Proposed paid, supervised learning and planned periods away from work, dependent on actual arrangements.','https://auraofintelligence.github.io/mutual-futures/workforce.html'),
 ('Mutual Futures: succession','Willing business sellers, knowledge handover and possible shared ownership. No placement or ownership entitlement is promised.','https://auraofintelligence.github.io/mutual-futures/succession.html'),
 ('UNGA81: a fair go','Luke’s invitation to build Joyful Responsible Abundance during the intelligence transition.','https://auraofintelligence.github.io/UNGA81-Luke-Hayes/'),
 ('82 Claytons Road','A distinct Minjerribah land-gift and partnership proposal.','https://auraofintelligence.github.io/Anglican-Diocese-82-Claytons-Amity/'),
 ('P4A Xyz Cinema','A source-linked civic interface for places, decisions and questions to investigate.','https://auraofintelligence.github.io/p4a-xyz-cinema/'),
 ('Australian Law: Your Relevance','A learning method for tracing legal questions. Its historical legal collection does not establish current law.','https://auraofintelligence.github.io/australian-law-2012-lukes-relevance/pages/your-relevance.html'),
 ('Australian Legal Engine','The separate source parsing and retrieval project, including its stated limits.','https://github.com/auraofintelligence/australian-legal-engine')
]

def external(url, label):
    return f'<a href="{E(url,quote=True)}" target="_blank" rel="noopener noreferrer">{E(label)} <span aria-hidden="true">↗</span></a>'

def write(path, text):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(text,encoding='utf-8',newline='\n')

def extract():
    with zipfile.ZipFile(DOC) as z:
        relroot=ET.fromstring(z.read('word/_rels/document.xml.rels'))
        rels={r.attrib['Id']:r.attrib['Target'] for r in relroot if r.attrib.get('TargetMode')=='External'}
        body=ET.fromstring(z.read('word/document.xml')).find(W+'body')
    def inline(node):
        if node.tag==W+'t':return E(node.text or '')
        if node.tag in (W+'br',W+'cr'):return '<br>'
        if node.tag==W+'tab':return ' '
        if node.tag in (W+'instrText',W+'delText',W+'pPr',W+'rPr'):return ''
        inside=''.join(inline(n) for n in node)
        if node.tag==W+'hyperlink':
            target=rels.get(node.attrib.get(R+'id'))
            if target:return f'<a href="{E(target,quote=True)}" target="_blank" rel="noopener noreferrer">{inside}</a>'
        if node.tag==W+'r':
            rp=node.find(W+'rPr')
            if rp is not None and rp.find(W+'b') is not None:inside='<strong>'+inside+'</strong>'
            if rp is not None and rp.find(W+'i') is not None:inside='<em>'+inside+'</em>'
        return inside
    nodes=[];pnum=0;table=0
    for node in body:
        if node.tag==W+'p':
            pnum+=1
            style=node.find('./w:pPr/w:pStyle',NS)
            style=style.attrib.get(W+'val','body') if style is not None else 'body'
            text=''.join(node.itertext()) if False else ''.join(t.text or '' for t in node.iter(W+'t'))
            nodes.append(dict(kind='p',p=pnum,style=style,text=text,html=inline(node)))
        elif node.tag==W+'tbl':
            table+=1; rows=[]
            for ri,row in enumerate(node.findall(W+'tr')):
                cells=[]
                for cell in row.findall(W+'tc'):
                    tag='th' if ri==0 else 'td'
                    span=cell.find('./w:tcPr/w:gridSpan',NS)
                    attrs=f' colspan="{span.attrib.get(W+"val","1")}"' if span is not None else ''
                    if tag=='th':attrs+=' scope="col"'
                    cells.append(f'<{tag}{attrs}>'+''.join('<p>'+inline(p)+'</p>' for p in cell.findall(W+'p'))+f'</{tag}>')
                rows.append('<tr>'+''.join(cells)+'</tr>')
            text=' '.join(t.text or '' for t in node.iter(W+'t'))
            nodes.append(dict(kind='table',after=pnum,number=table,text=text,html=f'<div class="table-wrap" role="region" tabindex="0" aria-label="Source table {table}"><table>'+''.join(rows)+'</table></div>'))
    return nodes, sorted(set(rels.values()))

nodes, original_links=extract()
write(ROOT/'content/source.json',json.dumps({'document':DOCNAME,'paragraph_count':sum(n['kind']=='p' for n in nodes),'table_count':sum(n['kind']=='table' for n in nodes),'links':original_links,'nodes':nodes},ensure_ascii=False,indent=2)+'\n')
doc_hash=hashlib.sha256(DOC.read_bytes()).hexdigest()
write(ROOT/'content/documents.json',json.dumps([{'file':'documents/'+DOCNAME,'title':'Aura Genesis for Children and Young People in Australian Care','author':'Luke Nathan Hayes','source':'User-supplied original DOCX','sha256':doc_hash,'bytes':DOC.stat().st_size,'preservation':'Unchanged original; website chapter groupings are editorial.'}],indent=2)+'\n')
write(ROOT/'documents/SHA256SUMS',doc_hash+'  '+DOCNAME+'\n')

def route(p):return p['id']+'.html'
def nav(current):
    return '<a class="skip" href="#main">Skip to content</a><header class="site-header"><a class="brand" href="index.html"><span class="brand-mark" aria-hidden="true">a.</span><span>Aura <span class="brand-sub">Children & young people</span></span></a><nav class="primary" aria-label="Primary"><a href="first-project.html">A first project</a><a href="people-and-control.html">People & control</a><a href="sources.html">Sources</a></nav><details class="all-pages"><summary>All pages <span aria-hidden="true">＋</span></summary><nav class="menu-panel" aria-label="Every public page">'+''.join(f'<a href="{route(p)}"'+(' aria-current="page"' if current==p['id'] else '')+f'>{E(p["nav"])}</a>' for p in PAGES)+'</nav></details></header>'

def head(p,noindex=False):
    canon=BASE+('' if p['id']=='index' else route(p))
    og=BASE+'assets/images/'+p.get('image','creative-project-protopia-v3')+'.webp'
    return f'''<!doctype html><html lang="en-AU"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{E(p['nav'])} | Aura · Children &amp; young people</title><meta name="description" content="{E(p['intro'],quote=True)}"><meta name="theme-color" content="#613596">{('<base href="'+BASE+'"><meta name="robots" content="noindex">') if noindex else ''}<link rel="canonical" href="{canon}"><meta property="og:type" content="website"><meta property="og:locale" content="en_AU"><meta property="og:title" content="{E(p['title'],quote=True)}"><meta property="og:description" content="{E(p['intro'],quote=True)}"><meta property="og:url" content="{canon}"><meta property="og:image" content="{og}"><meta name="twitter:card" content="summary_large_image"><link rel="icon" type="image/png" href="assets/favicon.png"><link rel="stylesheet" href="assets/style.css"><script defer src="assets/app.js"></script><link rel="describedby" type="text/plain" href="llms.txt"></head><body id="top">'''

def masthead(p):
    result=f'<div class="masthead wrap"><p class="eyebrow">{E(p["eyebrow"])}</p><h1>{E(p["title"])}</h1><p class="intro">{E(p["intro"])}</p>'
    if p['id']=='index':result+='<div class="actions"><a class="button" href="first-project.html">Explore a first project <span aria-hidden="true">↗</span></a><a class="button secondary" href="people-and-control.html">People and choices</a></div>'
    result+='</div>'
    if p.get('image'):
        result+=f'<figure class="chapter-art wrap"><img src="assets/images/{p["image"]}.webp" alt="{E(p["image_alt"],quote=True)}" width="1536" height="1024" fetchpriority="high"><figcaption>AI-generated concept · Fictional people and proposed settings</figcaption></figure>'
    return result

def source_body(p):
    subset=[n for n in nodes if (n['kind']=='p' and p['start']<=n['p']<=p['end']) or (n['kind']=='table' and p['start']<=n['after']<=p['end'])]
    headings=[n for n in subset if n['kind']=='p' and n['style'].lower()=='heading1']
    toc='<aside class="chapter-index"><p class="eyebrow">IN THIS CHAPTER</p><nav aria-label="Chapter contents">'+''.join(f'<a href="#source-p-{n["p"]}">{E(n["text"])}</a>' for n in headings)+'<a href="#reading">Full reading</a></nav><a class="source-link" href="sources.html">Original and source register ↗</a></aside>'
    content=[]
    for n in subset:
        if n['kind']=='table':content.append(n['html']);continue
        if not n['text'].strip():continue
        style=n['style'].lower();pid=n['p']
        if style=='title':
            content.append(f'<h2 id="source-p-{pid}">{n["html"]}</h2>')
        elif style=='subtitle':content.append(f'<p class="lead" id="source-p-{pid}">{n["html"]}</p>')
        elif style.startswith('heading'):
            tag='h2' if style=='heading1' else 'h3'
            content.append(f'<{tag} id="source-p-{pid}">{n["html"]}</{tag}>')
        else:content.append(f'<p id="source-p-{pid}" data-source-paragraph="{pid}">{n["html"]}</p>')
    return '<div class="reading-layout wrap" id="reading">'+toc+'<article class="source-reading"><p class="reading-label">FROM THE ORIGINAL PROPOSAL</p>'+''.join(content)+'</article></div>'

def cards(pages):
    return '<div class="card-grid">'+''.join(f'<a class="route-card" href="{route(p)}"><span class="eyebrow">{E(p["eyebrow"].split(" / ")[0])}</span><h3>{E(p["nav"])}</h3><p>{E(p["intro"])}</p><span class="card-link">Read the chapter <span aria-hidden="true">↗</span></span></a>' for p in pages)+'</div>'

def home_extra():
    return '<section class="welcome-note wrap"><div><p class="eyebrow">A PROTOPIAN FUTURE / REAL OPPORTUNITIES</p><h2>Raise the bar.<br>Keep the choice yours.</h2></div><div><p>A fair go in the age of superintelligence means more than access to a screen. This proposal asks how children and young people can understand AI, investigate sources, make creative choices and develop capabilities that matter in their own lives.</p><p>Trusted adults, practical control over chosen records and actual routes to mentors, learning and future work give that ambition somewhere to begin. The young person’s interests and questions shape the next encounter.</p><p>Verse Box and everyday learning provide the setting here. The separate adult pressure programme and Truth Engine research tasks are outside the child and teen activities.</p><p class="status">Public proposal by Luke Nathan Hayes · Proposed activities and opportunities require real people, resources and agreed arrangements.</p></div></section><section class="purpose-panel wrap"><p class="eyebrow">ETHICAL TECHNOLOGY / HUMAN AGENCY</p><h2>A more capable future, shaped with you.</h2><p>The Protopian direction is ambitious: improve lives through practical steps that people can question, test and revise, while opening a wider future across communities, Earth and space.</p><div class="card-grid"><article class="note-card"><h3>Understand and question.</h3><p>Compare an AI response with its sources. Ask what is known, what is inferred and what still needs checking. A confident answer is a reason to investigate, not the end of the conversation.</p></article><article class="note-card"><h3>Create and choose.</h3><p>Make a game, tell a story or explore a practical design. Choose what information enters the activity, review the result and keep a real route to correction, help and a different next step.</p></article><article class="note-card"><h3>Share in the possibilities.</h3><p>Connect growing interests with mentors, community projects and later adult opportunities. The fair-go ambition includes access to skills, meaningful work, productive ownership and time for a worthwhile life.</p></article></div></section><section class="pathway wrap"><p class="eyebrow">FOLLOW A POSSIBLE PATH</p><h2>From curiosity to a wider world.</h2><ol class="journey"><li><span>01</span><strong>Choose an interest</strong><p>A game, film, robot, music project or a question you want to investigate.</p></li><li><span>02</span><strong>Reflect and understand</strong><p>Check a source, explore a right and decide which records belong in the activity.</p></li><li><span>03</span><strong>Meet a real person</strong><p>A trusted adult, mentor or community host helps the next activity happen.</p></li><li><span>04</span><strong>Grow your opportunities</strong><p>Learning, contribution and future work develop through actual arrangements.</p></li></ol></section><section class="chapters wrap"><div class="section-heading"><div><p class="eyebrow">EXPLORE THE GUIDE</p><h2>Begin where you are.</h2></div><a href="sitemap.html">Every page ↗</a></div>'+cards([PAGES[2],PAGES[4],PAGES[5],PAGES[6],PAGES[7],PAGES[9]])+'</section>'

def guidance_notes():
    notes=[
      ('OAIC: children and young people','Capacity for a privacy decision is assessed in the circumstances; the guidance does not give one universal decision age. Coverage also differs between settings.','https://www.oaic.gov.au/privacy/your-privacy-rights/more-privacy-rights/children-and-young-people'),
      ('Australian Human Rights Commission: child safe organisations','The National Principles place safety, participation, suitable adults, child-focused complaints and ongoing review within organisational practice.','https://humanrights.gov.au/resource-hub/resources-for-organisations-businesses/child-safe-organisations'),
      ('Queensland: charter of rights for a child in care','Queensland’s charter includes privacy, identity and cultural connection, participation in decisions and support for the transition from care.','https://www.families.qld.gov.au/our-work/child-safety/children-young-people-care/charter-rights')]
    return '<section class="guidance wrap"><p class="eyebrow">PRIMARY GUIDANCE REVIEWED · '+TODAY+'</p><h2>Three current source checks.</h2><p>These brief checks sit alongside the source document. The remaining reference register preserves the proposal’s source context; it is not a claim that every linked source has been reverified.</p><div class="card-grid">'+''.join('<article class="note-card"><h3>'+external(url,title)+'</h3><p>'+E(note)+'</p></article>' for title,note,url in notes)+'</div><p>Actual authority, duties and approval depend on the organisation, jurisdiction, role and activity.</p></section>'

def source_extra():
    return f'<section class="download wrap"><div><p class="eyebrow">UNCHANGED USER-SUPPLIED DOCUMENT</p><h2>The complete original.</h2><p>All substantive narrative, both tables and the original source-link labels are included in the chapter readings. The original DOCX keeps its own layout and bytes.</p><a class="button" href="documents/{DOCNAME}">Download the original DOCX ↓</a></div><div><p><strong>SHA-256</strong></p><p class="hash">{doc_hash}</p><p>{DOC.stat().st_size:,} bytes · 329 paragraphs · 2 tables</p><a href="content/documents.json">Document integrity register</a><p>The source’s “Open source” labels mean open the cited source. They do not relicense this work or the linked material.</p></div></section>'+guidance_notes()

def about():
    licence=(ROOT/'LICENCE.md').read_text(encoding='utf-8-sig')
    # Minimal Markdown conversion preserves every licence word and the attribution wording.
    output=[]; in_list=False
    for line in licence.splitlines():
        if line.startswith('- '):
            if not in_list:output.append('<ul>');in_list=True
            output.append('<li>'+E(line[2:])+'</li>');continue
        if in_list:output.append('</ul>');in_list=False
        if line.startswith('# '):output.append('<h2>'+E(line[2:])+'</h2>')
        elif line.startswith('## '):output.append('<h3>'+E(line[3:])+'</h3>')
        elif line.strip():output.append('<p>'+E(line)+'</p>')
    if in_list:output.append('</ul>')
    return '<section class="narrow wrap prose"><h2>A public guide to a developing proposal.</h2><p>Concept and source direction: Luke Nathan Hayes / Strange But True / Aura of Intelligence. Website implementation prepared with ChatGPT. Australian English and the source’s original meanings are preserved.</p><p>This website provides public reading, source links and generated editorial concepts. It collects no accounts, analytics, personal profiles, messages or submissions. External sites have their own arrangements. Optional search works on the text already on this page.</p><p>The original DOCX and third-party references retain their existing rights. Generated artwork depicts fictional people and possible settings, not actual participants, installed facilities or established outcomes.</p><p>'+external(REPO,'Source repository')+' · '+external(REPO+'/blob/main/RIGHTS.md','Rights and attribution')+' · <a href="content/artwork.json">Artwork provenance and prompts</a></p><h2>Strange But True licence.</h2><p>The exact licence text is reproduced below. It is also available in '+external(REPO+'/blob/main/LICENCE.md','LICENCE.md')+'.</p>'+''.join(output)+'</section>'

def connection_content():
    return '<section class="wrap connection-list">'+''.join('<article><h2>'+external(url,title)+'</h2><p>'+E(desc)+'</p></article>' for title,desc,url in CONNECTIONS)+'</section>'

def sitemap():
    return '<section class="wrap site-index"><label class="search-label" hidden data-search-control>Find a chapter<input type="search" data-search placeholder="Try family, work, rights or community" autocomplete="off"></label><p class="search-status" role="status" data-search-status hidden></p><div class="sitemap-grid">'+''.join(f'<a class="sitemap-card" data-search-item href="{route(p)}"><span>{str(i+1).zfill(2)}</span><div><h2>{E(p["nav"])}</h2><p>{E(p["intro"])}</p></div><span aria-hidden="true">↗</span></a>' for i,p in enumerate(PAGES))+'</div><p><a href="sitemap.xml">XML sitemap</a> · <a href="llms.txt">Machine-readable guide</a></p></section>'

def footer(p):
    i=PAGES.index(p);prev=PAGES[(i-1)%len(PAGES)];nxt=PAGES[(i+1)%len(PAGES)]
    return f'<nav class="chapter-route wrap" aria-label="Previous and next chapters"><a href="{route(prev)}"><span>← Previous</span><strong>{E(prev["nav"])}</strong></a><a href="{route(nxt)}"><span>Next →</span><strong>{E(nxt["nav"])}</strong></a></nav><footer class="site-footer"><div class="wrap footer-main"><div><a class="brand" href="index.html">Aura · Children & young people</a><p>Self understanding, human relationships<br>and opportunities to grow.</p></div><nav aria-label="Footer reading routes"><a href="index.html">Home</a><a href="first-project.html">A first project</a><a href="people-and-control.html">People and personal control</a><a href="sitemap.html">Every page</a></nav><nav aria-label="Project information"><a href="sources.html">Sources and original document</a><a href="connections.html">Connected projects</a><a href="licence.html">About and licence</a>{external(REPO,"GitHub repository")}</nav></div><div class="wrap footer-base"><span>© 2026 Luke Nathan Hayes / Aura of Intelligence</span><span>Public proposal · October 2026</span></div></footer><a class="to-top" href="#top" aria-label="Return to top">↑</a></body></html>'

for p in PAGES:
    body=masthead(p)
    if p['id']=='index':body+=home_extra()
    if p.get('start'):body+=source_body(p)
    if p['id']=='sources':body+=source_extra()
    if p['id']=='connections':body+=connection_content()
    if p['id']=='licence':body+=about()
    if p['id']=='sitemap':body+=sitemap()
    write(OUT/route(p),head(p)+nav(p['id'])+'<main id="main">'+body+'</main>'+footer(p))

missing=dict(id='404',nav='Page not found',title='Let’s find your way.',eyebrow='PAGE NOT FOUND',intro='This address does not match a page in the guide. The sitemap lists every public chapter.')
write(OUT/'404.html',head(missing,True)+nav('404')+'<main id="main">'+masthead(missing)+'<section class="wrap recovery"><a class="button" href="sitemap.html">Open the sitemap ↗</a></section></main>'+footer(PAGES[0]))
write(OUT/'sitemap.xml','<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join('<url><loc>'+BASE+('' if p['id']=='index' else route(p))+'</loc></url>' for p in PAGES)+'</urlset>\n')
write(OUT/'llms.txt','# Aura · Children and young people\n\n> A public proposal by Luke Nathan Hayes for supported learning, personal Aura, relationships, rights and opportunities for adulthood in Australian care.\n\nCanonical website: '+BASE+'\nSource repository: '+REPO+'\nLicence: '+REPO+'/blob/main/LICENCE.md\nRights: '+REPO+'/blob/main/RIGHTS.md\nOriginal document: '+BASE+'documents/'+DOCNAME+'\n\n## Public pages\n'+''.join('- ['+p['nav']+']('+BASE+('' if p['id']=='index' else route(p))+'): '+p['intro']+'\n' for p in PAGES)+'\nThe child and teen proposal uses Verse Box and everyday learning, not adult pressure treatment. Adult teacher training is facilitator context. C-Hours are nonmonetary voluntary contribution; essential support is independent. This is a public proposal, not an operating care service, recruitment platform or qualification. Discovery grants no additional reuse or AI-training rights.\n')
write(OUT/'robots.txt','# Informational project copy: crawler rules must be served at the origin root.\n# Merge .github/robots-root-snippet.txt into https://auraofintelligence.github.io/robots.txt\n# Preserve every other project policy. Discovery grants no additional reuse or AI-training rights.\nUser-agent: *\nAllow: /\nSitemap: '+BASE+'sitemap.xml\n')
write(ROOT/'content/routes.json',json.dumps([{k:p[k] for k in ['id','nav','title','intro']} for p in PAGES],ensure_ascii=False,indent=2)+'\n')
write(ROOT/'content/build-report.json',json.dumps({'pages':len(PAGES),'source_paragraphs':sum(n['kind']=='p' for n in nodes),'source_tables':sum(n['kind']=='table' for n in nodes),'original_hyperlinks':len(original_links),'source_sha256':doc_hash,'review_date':'2026-10-28'},indent=2)+'\n')
print(f'Built {len(PAGES)} public pages plus 404; preserved {len(nodes)} source blocks and {len(original_links)} exact source URLs.')
