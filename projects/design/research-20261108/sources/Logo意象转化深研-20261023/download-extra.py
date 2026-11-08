from pathlib import Path
import json, urllib.request, concurrent.futures, sys
ROOT=Path(__file__).resolve().parent
manifest=sys.argv[1] if len(sys.argv)>1 else 'extra-sources.json'
records=json.loads((ROOT/manifest).read_text(encoding='utf-8'))
def get(r):
    dest=ROOT/('论文' if r['kind']=='paper' else '原始参考')/r['file']
    try:
        req=urllib.request.Request(r['url'],headers={'User-Agent':'Mozilla/5.0'})
        with urllib.request.urlopen(req,timeout=30) as response:
            dest.write_bytes(response.read())
        return dict(r,status='downloaded',bytes=dest.stat().st_size)
    except Exception as e: return dict(r,status='failed',error=str(e))
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    result=list(pool.map(get,records))
(ROOT/(Path(manifest).stem+'-下载核验.json')).write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
for r in result: print(r['id'],r['status'],r.get('bytes',r.get('error')))
