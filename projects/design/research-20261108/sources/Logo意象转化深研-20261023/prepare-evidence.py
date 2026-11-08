from pathlib import Path
import json, re, subprocess
from PIL import Image, ImageOps, ImageDraw, ImageFont
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parent
OLD = ROOT.parent / 'Logo图形意象化研究-20261023' / '阅读证据'
OUT = ROOT / '图解'
OUT.mkdir(exist_ok=True)
FONT = ImageFont.truetype('C:/Windows/Fonts/msyh.ttc', 23)
SMALL = ImageFont.truetype('C:/Windows/Fonts/msyh.ttc', 18)

def sheet(files, name, columns=3, cell=(570,440)):
    w,h=cell
    canvas=Image.new('RGB',(columns*w,((len(files)+columns-1)//columns)*h),'#f2f1ed')
    d=ImageDraw.Draw(canvas)
    for i,p in enumerate(files):
        try:
            im=Image.open(p).convert('RGBA')
            white=Image.new('RGBA',im.size,'white'); white.alpha_composite(im)
            im=ImageOps.contain(white.convert('RGB'),(w-32,h-72))
            x=(i%columns)*w; y=(i//columns)*h
            canvas.paste(im,(x+(w-im.width)//2,y+12+(h-72-im.height)//2))
            d.text((x+16,y+h-47),p.stem[:29],font=FONT,fill='#202020')
        except Exception as e: print('image-error',p.name,str(e))
    canvas.save(OUT/name)

images=[p for p in (ROOT/'原始参考').iterdir() if p.suffix.lower() in ['.jpg','.png','.gif','.jpeg']]
sheet(images[:6],'原图对照-01.jpg')
sheet(images[6:],'原图对照-02.jpg')
sheet([OLD/'GFW-钢笔与勺子-机构档案.jpeg',OLD/'CI-作者项目首图.jpg',OLD/'NBC-作者项目首图.jpg'],'原图对照-03.jpg')

keywords={
 'Gentner1983.pdf':['systematicity','relations between','CONCLUS'],
 'Gentner2003.pdf':['Experiment 2','General Discussion','Participants'],
 'Dunlosky2013.pdf':['general assessment','General Assessment','distributed practice'],
 'SchwartzBransford1998.pdf':['neither the contrasting','Participants.','GENERAL DISCUSSION'],
 'Schon1992.pdf':['Seeing/Drawing/Seeing','unexpected','2 Seeing'],
}
index=[]
for p in sorted((ROOT/'论文').glob('*.pdf')):
    if not p.read_bytes().startswith(b'%PDF'):
        print('Not a PDF; excluded:',p.name)
        continue
    reader=PdfReader(p)
    texts=[page.extract_text() or '' for page in reader.pages]
    relevant=[]
    for i,t in enumerate(texts):
        matches=[k for k in keywords.get(p.name,[]) if k.lower() in t.lower()]
        if matches: relevant.append({'pdf_page':i+1,'keywords':matches})
    index.append({'file':p.name,'pages':len(texts),'relevant':relevant})
    (ROOT/'论文'/f'{p.stem}-全文提取.txt').write_text('\n\n'.join(f'=== PDF PAGE {i+1} ===\n{t}' for i,t in enumerate(texts)),encoding='utf-8')
    print(p.name,'pages=',len(texts),'relevant=',relevant)
(ROOT/'论文'/'阅读页索引.json').write_text(json.dumps(index,ensure_ascii=False,indent=2),encoding='utf-8')
