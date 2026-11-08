const fs=require('fs');
const path=require('path');
const crypto=require('crypto');
const root=path.resolve(__dirname,'..');
const out=__dirname;
const skip=new Set(['.git','node_modules','工具依赖','Skill校验依赖','.agents','.codex',path.basename(out)]);
const files=[],errors=[];
function walk(dir){let entries;try{entries=fs.readdirSync(dir,{withFileTypes:true});}catch(e){errors.push({path:dir,error:e.code});return;}for(const entry of entries){const p=path.join(dir,entry.name);if(entry.isSymbolicLink())continue;if(entry.isDirectory()){if(!skip.has(entry.name))walk(p);}else if(entry.isFile()){const st=fs.statSync(p);files.push({relative:path.relative(root,p).replaceAll('\\','/'),path:p,size:st.size,extension:path.extname(p).toLowerCase(),modifiedAt:st.mtime.toISOString()});}}}
walk(root);
files.sort((a,b)=>a.relative.localeCompare(b.relative,'zh-CN'));
const origins=new Map();
for(const title of ['羊年','汉字重构']){const data=JSON.parse(fs.readFileSync(path.join(out,'证据',title+'-取回记录.json'),'utf8'));for(const turn of data.turns){const refs=[];for(const m of turn.messages)if(m.type==='userMessage')for(const c of m.content||[])if(c.type==='localImage')refs.push({path:c.path,role:'用户附件'});for(const g of turn.imageGenerations)refs.push({path:g.savedPath,role:'生成原图'});for(const p of turn.viewedImages)refs.push({path:p,role:'查看图像'});for(const f of turn.changedFiles)refs.push({path:f.path,role:'变更文件'});for(const r of refs){if(typeof r.path!=='string'||!path.isAbsolute(r.path))continue;const key=path.normalize(r.path);if(!origins.has(key))origins.set(key,{path:key,exists:fs.existsSync(key),evidence:[]});const record=origins.get(key);if(!record.evidence.some(x=>x.ref===turn.ref&&x.role===r.role))record.evidence.push({thread:title,ref:turn.ref,turnId:turn.turnId,role:r.role});}}}
const csvCell=v=>'"'+String(v??'').replaceAll('"','""')+'"';
fs.writeFileSync(path.join(out,'证据','项目文件清单.csv'),'\uFEFF'+[['相对路径','字节数','类型','修改时间UTC','聊天证据编号'],...files.map(f=>[f.relative,f.size,f.extension,f.modifiedAt,(origins.get(path.normalize(f.path))?.evidence||[]).map(e=>e.ref).filter((v,i,a)=>a.indexOf(v)===i).join(' ')])].map(r=>r.map(csvCell).join(',')).join('\r\n'));
fs.writeFileSync(path.join(out,'证据','聊天文件定位.json'),JSON.stringify([...origins.values()],null,2));
const groups={};for(const f of files){const group=f.relative.includes('/')?f.relative.split('/')[0]:'项目根目录';groups[group]??={count:0,bytes:0,md:0,images:0,svg:0};const g=groups[group];g.count++;g.bytes+=f.size;if(f.extension==='.md')g.md++;if(['.png','.jpg','.jpeg','.webp'].includes(f.extension))g.images++;if(f.extension==='.svg')g.svg++;}
const selected=[['01-长江题-被否定的几何稿.png','汉字创意再研究-20261021/视觉核对/对照-被否定的几何重构.png'],['02-早期羊年-获认可的辅助字调整.png','瑞羊启新春-京彩中国年-2027/05-用户选定图-辅助字统一版.png'],['03-竖版v5-阅读分组问题.png','选定羊姿态融合与收紧-20261024/参考羊融合-紧凑竖版-v5.png'],['04-横版-用户认可的小羊基准.png','竖式移植已认可小羊-20261024/横版-用户认可基准.png'],['05-竖版-最新移植样稿.png','竖式移植已认可小羊-20261024/竖式-移植横版双羊.png']];
fs.mkdirSync(path.join(out,'关键图版'),{recursive:true});const copies=[];for(const [name,rel]of selected){const src=path.join(root,rel),dst=path.join(out,'关键图版',name);fs.copyFileSync(src,dst);const sha=p=>crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex');copies.push({source:rel,copy:'关键图版/'+name,sha256:sha(src),identical:sha(src)===sha(dst)});}
const allRefs=[...origins.values()];const stats={projectFileCount:files.length,projectMarkdownCount:files.filter(f=>f.extension==='.md').length,projectBytes:files.reduce((n,f)=>n+f.size,0),groups,scanErrors:errors,skippedDirectories:[...skip],referencePathCount:allRefs.length,existingReferenceCount:allRefs.filter(r=>r.exists).length,missingReferences:allRefs.filter(r=>!r.exists),keyCopies:copies};
fs.writeFileSync(path.join(out,'证据','整理核验.json'),JSON.stringify(stats,null,2));
let md='# 项目文件定位索引\n\n扫描范围：设计项目普通文件；排除 Git 内部、工具依赖、校验依赖与本次输出目录。索引覆盖研究正文、原图、参考、提示词、脚本、SVG和历史资料库副本，不表示本轮逐张看过所有图片。原文件保持原位。修改时间不当作设计发生顺序，时间线以聊天为准。\n\n完整逐文件表见[项目文件清单.csv](项目文件清单.csv)，聊天位置与存在性见[聊天文件定位.json](聊天文件定位.json)。\n\n|目录|文件|研究/提示词MD|图像|SVG|\n|---|---:|---:|---:|---:|\n';for(const [name,g]of Object.entries(groups))md+='|'+name+'|'+g.count+'|'+g.md+'|'+g.images+'|'+g.svg+'|\n';
md+='\n共 '+files.length+' 个普通文件，'+stats.projectMarkdownCount+' 份 Markdown。聊天直接记录的 '+allRefs.length+' 个唯一文件路径中，'+stats.existingReferenceCount+' 个当前可定位，'+stats.missingReferences.length+' 个未找到；未找到的路径保存在整理核验JSON，不能据此声称原始附件已全部恢复。\n';
fs.writeFileSync(path.join(out,'证据','项目文件定位索引.md'),md);
console.log(JSON.stringify({fileCount:files.length,mdCount:stats.projectMarkdownCount,groups:Object.keys(groups).length,referencePaths:allRefs.length,missing:stats.missingReferences.map(r=>r.path),scanErrors:errors,keyCopies:copies.map(c=>({copy:c.copy,identical:c.identical}))},null,2));
