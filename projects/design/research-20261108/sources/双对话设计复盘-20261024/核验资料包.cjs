const fs=require('fs');
const path=require('path');
const root=__dirname;
const documents=fs.readdirSync(root).filter(n=>n.endsWith('.md'));
const broken=[],checks=[];
for(const name of documents){const text=fs.readFileSync(path.join(root,name),'utf8');let count=0;for(const match of text.matchAll(/!?\[[^\]]*\]\(([^\n)]+)\)/g)){let target=match[1].trim().replace(/^<|>$/g,'');if(/^(https?:|codex:|#)/.test(target))continue;target=target.split('#')[0];if(!target)continue;const p=path.resolve(root,decodeURIComponent(target));count++;if(!fs.existsSync(p))broken.push({document:name,target,path:p});}checks.push({document:name,localLinks:count,characters:text.length});}
const histories=[];for(const title of ['羊年','汉字重构']){const data=JSON.parse(fs.readFileSync(path.join(root,'证据',title+'-取回记录.json'),'utf8'));histories.push({title,turns:data.turns.length,uniqueTurnIds:new Set(data.turns.map(t=>t.turnId)).size,hasMore:data.retrieval.hasMore,firstRef:data.turns[0].ref,lastRef:data.turns.at(-1).ref,emptyMessageTurns:data.turns.filter(t=>!t.messages.length).length});}
const result={checkedAt:new Date().toISOString(),documents:checks,brokenLinks:broken,histories};
fs.writeFileSync(path.join(root,'证据','资料包链接与轮次核验.json'),JSON.stringify(result,null,2));
console.log(JSON.stringify(result,null,2));
