import urllib.request,urllib.parse,pathlib,re,concurrent.futures,json
root=pathlib.Path(__file__).parent/'资料'
sources={
 '北京2026-标识':'https://img1.bjd.com.cn/2025/12/26/21fc2a179266d55b33362d6bd0f6058e9b1c5af6.jpg',
 '北京2026-主视觉':'https://img1.bjd.com.cn/2025/12/26/2708a913bea96feed9cede5924e625a6a5078a05.jpg',
 '山东2025-官宣缩略':'https://img12.iqilu.com/10395/sucaiku/compress/202501/03/11b906ef1b93432389fe235dad12b7b2.png',
 '央视2025-实际页':'https://www.cctv.com/2024/11/29/ARTIKgahTAP3XsuREaqLyZXZ241129.shtml',
 '央视2026-官宣':'https://1118.cctv.com/2025/12/17/ARTIekgannVjVvLWjGpEEQp9251217.shtml',
}
def fetch(item):
 name,url=item
 try:
  with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=20) as r:data=r.read();typ=r.headers.get('Content-Type','')
  if 'image' in typ:
   p=root/(name+('.png' if 'png' in typ else '.jpg'));p.write_bytes(data);return {'name':name,'url':url,'file':str(p)}
  text=data.decode('utf-8',errors='replace');(root/(name+'.html')).write_text(text,encoding='utf-8')
  urls=[]
  for m in re.findall(r'(?:src|data-src)=[\"\x27]([^\"\x27]+)',text,re.I):
   u=urllib.parse.urljoin(url,m)
   if re.search(r'\.(?:jpg|jpeg|png)(?:[?]|$)',u,re.I) and u not in urls:urls.append(u)
  return {'name':name,'url':url,'images':urls[:16],'count':len(urls)}
 except Exception as e:return {'name':name,'error':str(e)}
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as ex: results=list(ex.map(fetch,sources.items()))
(root/'图像来源.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
for r in results: print(json.dumps(r,ensure_ascii=True))
