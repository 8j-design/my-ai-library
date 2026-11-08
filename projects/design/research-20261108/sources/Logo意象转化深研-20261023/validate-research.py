from pathlib import Path
import json,re,xml.etree.ElementTree as ET
from PIL import Image
from pypdf import PdfReader
ROOT=Path(__file__).resolve().parent
issues=[]; local_links=0
for p in ROOT.glob('*.md'):
    t=p.read_text(encoding='utf-8')
    if not t.strip():issues.append('Empty: '+p.name)
    for target in re.findall(r'\]\(([^)]+)\)',t):
        if re.match(r'^https?://|^#',target):continue
        link=Path(target) if re.match(r'^[A-Za-z]:[/\\]',target) else p.parent/target
        if not link.exists():issues.append('Missing link: '+p.name+' -> '+target)
        local_links+=1
figures=[]
for p in sorted((ROOT/'图解').glob('[0-9][0-9]-*.svg')):
    ET.parse(p)
    with Image.open(p.with_suffix('.png')) as im:
        im.verify()
    figures.append(p.name)
papers=[]
invalid=[]
for p in (ROOT/'论文').glob('*.pdf'):
    if not p.read_bytes().startswith(b'%PDF'):
        invalid.append(p.name);continue
    r=PdfReader(p);papers.append({'file':p.name,'pages':len(r.pages)})
images=[]
for p in (ROOT/'原始参考').iterdir():
    if p.suffix=='.svg':ET.parse(p);images.append({'file':p.name,'format':'SVG'});continue
    try:
        with Image.open(p) as im: images.append({'file':p.name,'format':im.format,'size':im.size})
    except Exception as e:issues.append('Unreadable image: '+p.name+' '+str(e))
cases=(ROOT/'02-二十组案例逐案拆解.md').read_text(encoding='utf-8')
case_count=len(re.findall(r'^## \d{2}｜',cases,re.M))
if case_count!=20:issues.append('Case count mismatch')
result={'date':'2026-10-23','local_links':local_links,'case_groups':case_count,'valid_papers':papers,'excluded_invalid_pdf_responses':invalid,'research_figures':figures,'downloaded_image_files':images,'issues':issues,'scope':'File/link/content-type validation only; visual QA performed separately; no audience study.'}
(ROOT/'交付核验.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'local_links':local_links,'case_groups':case_count,'valid_papers':len(papers),'excluded':invalid,'figures':len(figures),'image_files':len(images),'issues':issues},ensure_ascii=False,indent=2))
raise SystemExit(1 if issues else 0)
