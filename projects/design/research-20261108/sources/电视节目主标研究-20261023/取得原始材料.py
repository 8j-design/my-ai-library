import urllib.request, urllib.parse, re, pathlib, concurrent.futures, json
root=pathlib.Path(__file__).parent/'资料'
sources={
 '央视2025':'https://news.cctv.com/2024/11/29/ARTIKgahTAP3XsuREaqLyZXZ241129.shtml',
 '北京2026':'https://news.bjd.com.cn/2025/12/26/11486975.shtml',
 '河南2025':'https://dzb-jinbw.hntv.tv/html/2025-01/08/content_932002.htm?div=1',
 '山东2025':'https://news.iqilu.com/shandong/shandonggedi/20250103/5763968.shtml',
 '奥斯卡标识':'https://images.ctfassets.net/mqgaq446dh9d/1hRNcghUHboflQc5dN5lhO/f331d2533a40ce9f53d25eecf77adaf4/oscars_logo_white_mode.jpg?fm=jpg&q=80&w=3840',
 'Eurovision2026':'https://www.ebu.ch/files/live/sites/ebu/files/News/2025/08/ESC_70_Heart_Social_1280x720.png',
}
def fetch(name,url):
 try:
  req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'})
  with urllib.request.urlopen(req,timeout=25) as r: data=r.read();typ=r.headers.get('Content-Type','')
  if 'image' in typ:
   ext='.png' if 'png' in typ else '.jpg'; p=root/(name+ext);p.write_bytes(data)
   return {'name':name,'url':url,'file':str(p),'type':typ}
  text=data.decode('utf-8',errors='replace');(root/(name+'.html')).write_text(text,encoding='utf-8')
  urls=[]
  for m in re.findall(r'(?:src|data-src)=[\"\x27]([^\"\x27]+)',text,re.I):
   u=urllib.parse.urljoin(url,m)
   if re.search(r'\.(?:jpg|jpeg|png)(?:[?]|$)',u,re.I) and u not in urls: urls.append(u)
  return {'name':name,'url':url,'images':urls[:20],'count':len(urls)}
 except Exception as e:return {'name':name,'error':str(e)}
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as ex: results=list(ex.map(lambda x:fetch(*x),sources.items()))
(root/'来源.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
for r in results:print(json.dumps(r,ensure_ascii=False))
