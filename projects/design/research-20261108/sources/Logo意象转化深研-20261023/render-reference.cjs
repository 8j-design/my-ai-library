const fs=require('fs');
const path=require('path');
const sharp=require('C:/Users/scvfv/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/sharp');
const root=__dirname;
(async()=>{
  const svg=fs.readFileSync(path.join(root,'原始参考','Aquarium-标志.svg'));
  await sharp(svg,{density:200}).flatten({background:'#163d59'}).trim().resize({width:1050}).png().toFile(path.join(root,'图解','Aquarium-原矢量可见化.png'));
  await sharp(fs.readFileSync(path.join(root,'原始参考','Unilever-官方.svg')),{density:96}).flatten({background:'#ffffff'}).resize({width:950}).png().toFile(path.join(root,'图解','Unilever-原矢量预览.png'));
  console.log('Rendered 2 source SVGs. Aquarium uses a dark backdrop so its original white paths are visible.');
})();
