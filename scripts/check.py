"""Check generated navigation, document integrity, source coverage and public assets."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import hashlib,json,re,sys
ROOT=Path(__file__).resolve().parents[1]
class Page(HTMLParser):
 def __init__(self):super().__init__();self.ids=set();self.links=[];self.assets=[];self.navlinks=[];self.in_nav=0;self.text=[]
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if a.get('id'):self.ids.add(a['id'])
  if tag=='nav':self.in_nav+=1
  if tag=='a' and a.get('href'):
   self.links.append(a)
   if self.in_nav:self.navlinks.append(a['href'])
  if tag in ('img','script') and a.get('src'):self.assets.append(a['src'])
  if tag=='link' and a.get('rel') in ('stylesheet','icon'):self.assets.append(a.get('href',''))
 def handle_endtag(self,tag):
  if tag=='nav':self.in_nav=max(0,self.in_nav-1)
 def handle_data(self,data):self.text.append(data)
pages={p.name:Page() for p in ROOT.glob('*.html')}
for name,parser in pages.items():parser.feed((ROOT/name).read_text(encoding='utf8'))
routes=json.loads((ROOT/'content/routes.json').read_text(encoding='utf8'))
errors=[]
for name,page in pages.items():
 for a in page.links:
  href=a['href'];s=urlsplit(href)
  if s.scheme in ('http','https'):
   if a.get('target')!='_blank' or not {'noopener','noreferrer'}<=set(a.get('rel','').split()):errors.append(f'{name}: external rel/target {href}')
   continue
  if s.scheme:continue
  dest=unquote(s.path) or name
  if not (ROOT/dest).exists():errors.append(f'{name}: missing link {href}')
  if s.fragment and dest in pages and unquote(s.fragment) not in pages[dest].ids:errors.append(f'{name}: missing fragment {href}')
 for asset in page.assets:
  if not urlsplit(asset).scheme and not (ROOT/unquote(urlsplit(asset).path)).is_file():errors.append(f'{name}: missing asset {asset}')
 for p in routes:
  if p['id']+'.html' not in page.navlinks:errors.append(f'{name}: route absent from navigation: {p["id"]}')
 if 'noindex' not in (ROOT/name).read_text(encoding='utf8') and name=='404.html':errors.append('404 lacks noindex')
source=json.loads((ROOT/'content/source.json').read_text(encoding='utf8'))
all_text=' '.join(' '.join(p.text) for p in pages.values())
norm=lambda s:re.sub(r'\s+','',s)
for node in source['nodes']:
 if node['text'].strip() and norm(node['text']) not in norm(all_text):errors.append(f'Missing source text: {node.get("p",node.get("number"))}')
all_urls={a['href'] for p in pages.values() for a in p.links}
for url in source['links']:
 if url not in all_urls:errors.append('Missing original hyperlink '+url)
for doc in json.loads((ROOT/'content/documents.json').read_text(encoding='utf8')):
 if hashlib.sha256((ROOT/doc['file']).read_bytes()).hexdigest()!=doc['sha256']:errors.append('Original document hash mismatch')
artfile=ROOT/'content/artwork.json'
if artfile.exists():
 for art in json.loads(artfile.read_text(encoding='utf8'))['images']:
  p=ROOT/art['file']
  if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=art['sha256']:errors.append('Artwork mismatch: '+art['file'])
else:errors.append('Missing artwork provenance')
if errors:
 print('\n'.join(errors));sys.exit(1)
print(f'PASS: {len(pages)} HTML pages; {source["paragraph_count"]} original paragraphs, {source["table_count"]} tables and {len(source["links"])} exact URLs covered; navigation, fragments, assets, external links and hashes valid.')
