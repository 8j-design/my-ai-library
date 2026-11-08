from pathlib import Path
import re
ROOT=Path(__file__).resolve().parent
OUT=ROOT/'图解'
OUT.mkdir(exist_ok=True)

def text(x,y,s,size=22,color='#222',weight=400):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" font-weight="{weight}" font-family="Microsoft YaHei, sans-serif">{s}</text>'
def svg(name,w,h,content):
    (OUT/name).write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}"><rect width="{w}" height="{h}" fill="#f5f4f0"/>{content}</svg>',encoding='utf-8')
def panel(x,y,w,h,title):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="white"/>'+text(x+20,y+34,title,21)
def spoon(x,y,s=1,fill='white',length=112):
    return f'<g transform="translate({x},{y}) scale({s})"><path d="M0 -62 C-37 -62 -44 -13 -25 8 C-17 16 -7 18 -6 34 L-5 {length} L5 {length} L6 34 C7 18 17 16 25 8 C44 -13 37 -62 0 -62Z" fill="{fill}"/></g>'
def nib(x,y):
    return f'<path d="M{x-76} {y-105} L{x+76} {y-105} L{x+103} {y+93} Q{x+39} {y+113} {x+23} {y+176} L{x-23} {y+176} Q{x-39} {y+113} {x-103} {y+93}Z" fill="#202425"/>'
c=text(24,40,'研究图 1｜同样两个意象，结构关系可以不同',28)
for i,title in enumerate(['并置：两件物体','嵌入：一个轮廓装另一个','共构：留白承担两项任务']):
    x=24+i*430;c+=panel(x,66,408,400,title)
    if i==0:
        c+=f'<g transform="translate({x+111},230) scale(.7)">'+nib(0,0)+'</g>'+spoon(x+298,245,.8,'#202425')
    else:
        c+=f'<g transform="translate({x+203},235) scale(.9)">'+nib(0,0)+spoon(0,-5,.63 if i==1 else .98,length=190 if i==2 else 112)+'</g>'
    desc=['两者各自完整，靠位置建立联系','勺柄止于内部，主要是图中藏图','勺柄通向外部，同时成为笔尖中缝'][i]
    c+=text(x+20,435,desc,18)
c+=text(24,506,'分析性重构示意；不是 GFW 原稿，也不是其真实草图过程。三种关系没有脱离任务的统一优劣。',18)
svg('01-并置嵌入共构.svg',1330,535,c)

raw=(ROOT/'原始参考'/'Aquarium-标志.svg').read_text()
paths=re.findall(r'<path[^>]+/>',raw)
base=''.join(paths[:4]);eyes=''.join(paths[4:])
c=text(24,40,'研究图 2｜一组边界，如何在波浪与鱼群之间组织观看',28)
for i,title in enumerate(['原矢量：轮廓与眼点共同作用','干预：只移除眼点']):
    x=24+i*630;c+=panel(x,66,606,585,title)
    c+=f'<rect x="{x+20}" y="125" width="566" height="480" fill="#163d59"/>'
    c+=f'<g transform="translate({x+61},140) scale(1.55) translate(-390,0)" fill="white">{base}{eyes if i==0 else ""}</g>'
c+=text(24,690,'原图：Chermayeff &amp; Geismar &amp; Haviv，National Aquarium。右图为研究用矢量删减。',18)
c+=text(24,722,'观察问题：保留相同边界后，类别线索与第一眼读法会如何变化？未做受众实验，不能由此宣称识别率。',18)
svg('02-鱼群波浪与眼点.svg',1310,755,c)

c=text(24,40,'研究图 3｜物体没变，位置关系已经改变',28)
for i,title in enumerate(['横条在下方且接近','横条移到上方','横条向一侧偏移','横条仍在下方但远离']):
    x=24+i*310;c+=panel(x,66,288,340,title)
    cx=x+144;cy=220
    c+=f'<circle cx="{cx}" cy="{cy}" r="61" fill="none" stroke="#17618c" stroke-width="21"/>'
    bx,by=(cx-60,310) if i==0 else (cx-60,111) if i==1 else (cx+20,310) if i==2 else (cx-60,366)
    c+=f'<rect x="{bx}" y="{by}" width="120" height="20" fill="#47834d"/>'
c+=text(24,448,'自制基础形示意，受 Conservation International 案例启发；不是该品牌的规范或改稿建议。',18)
c+=text(24,480,'研究问题：承托、遮盖、失衡、分离等读法中，哪些来自位置，哪些需要语境？',18)
svg('03-关系位置对照.svg',1270,510,c)

c=text(24,40,'研究图 4｜十二张迁移草图：检验结构，不以数量代表质量',28)
names=['书与门：独立并置','门在书内：形象容纳','开口共用：让出中缝','开口加宽：页形被削弱','两株植物：独立并置','靠近根部：仍各自独立','共用主干：左右展开','主干过密：关系挤压','包围闭合：保护或封闭','小开口：保护或可进入','大开口：开放或泄漏','偏移圆心：接触或失衡']
for i,title in enumerate(names):
    col=i%4;row=i//4;x=24+col*314;y=70+row*280
    c+=panel(x,y,294,258,title)
    cx=x+147;cy=y+140
    if i<4:
        if i==0:
            c+=f'<path d="M{cx-110} {cy-40} L{cx-62} {cy-20} L{cx-62} {cy+57} L{cx-110} {cy+37}Z M{cx-58} {cy-20} L{cx-10} {cy-40} L{cx-10} {cy+37} L{cx-58} {cy+57}Z" fill="#202425"/>'
            c+=f'<path d="M{cx+28} {cy+56} V{cy-50} H{cx+104} V{cy+56}" stroke="#202425" stroke-width="12" fill="none"/>'
        else:
            gap=[0,10,22,51][i]
            c+=f'<path d="M{cx-100} {cy-60} Q{cx-48} {cy-64} {cx-gap} {cy-34} L{cx-gap} {cy+82} Q{cx-45} {cy+48} {cx-100} {cy+53}Z M{cx+100} {cy-60} Q{cx+48} {cy-64} {cx+gap} {cy-34} L{cx+gap} {cy+82} Q{cx+45} {cy+48} {cx+100} {cy+53}Z" fill="#202425"/>'
            if i==1:c+=f'<path d="M{cx-38} {cy+65} V{cy-15} H{cx+38} V{cy+65}" stroke="white" stroke-width="11" fill="none"/>'
    elif i<8:
        a=i-4
        stems=[(-55,55),(-34,34),(0,0),(-10,10)][a]
        for j,dx in enumerate(stems):
            topdx=(-65 if j==0 else 65)
            c+=f'<path d="M{cx+dx} {cy+85} Q{cx+dx} {cy+10} {cx+topdx} {cy-32}" stroke="#202425" stroke-width="{12 if a!=3 else 25}" fill="none"/>'
            c+=f'<path d="M{cx+topdx} {cy-30} Q{cx+topdx-40} {cy-87} {cx+topdx-57} {cy-56} Q{cx+topdx-35} {cy-25} {cx+topdx} {cy-30}Z" fill="#202425"/>'
        c+=f'<path d="M{cx-95} {cy+87} H{cx+95}" stroke="#202425" stroke-width="8"/>'
    else:
        a=i-8
        r=86;cut=[0,18,60,22][a]
        c+=f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#202425" stroke-width="24"/>'
        if cut:c+=f'<rect x="{cx+59}" y="{cy-cut}" width="50" height="{cut*2}" fill="white"/>'
        c+=f'<circle cx="{cx+(55 if a==3 else 0)}" cy="{cy}" r="22" fill="#202425"/>'
c+=text(24,960,'以上为本轮自制方法练习；未做品牌匹配、陌生受众测试或最终造型修正。',18)
svg('04-十二张结构迁移草图.svg',1300,995,c)

c=text(24,40,'研究图 5｜大形识别与内部内容，是两个观察尺度',28)
for i,title in enumerate(['单元排列形成大形','相同单元散开','大形缩小后观察']):
    x=24+i*420;c+=panel(x,66,398,390,title)
    coords=[]
    for row in range(7):
        for col in range(7):
            if col in [0,1,5,6] or row>=5:coords.append((col,row))
    for j,(col,row) in enumerate(coords):
        if i==1:col,row=(j*3%8),(j*5%9)
        scale=.44 if i==2 else 1
        px=x+68+(col*36)*scale;py=145+(row*36)*scale
        if i==2:px+=70;py+=70
        c+=f'<circle cx="{px}" cy="{py}" r="{12*scale}" fill="#2852a0"/>'
c+=text(24,502,'基础圆点自制示意，受 Unilever 的整体与局部层级启发；不是 Unilever 的元素排布或缩小测试。',18)
svg('05-整体与局部层级.svg',1300,535,c)
print('Created 5 vector research figures, including 12 transfer sketches.')
