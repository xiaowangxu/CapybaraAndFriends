"""Rebuild the blog's standalone research figures from its checked-in data.

Usage: python scripts/build-working-register-figures.py
Requires matplotlib. Optional --source points to register_research_20260908
to refresh the curated data from the original experiment JSON files.
Chart contract: independent-shard paired deltas (4 pairs), development
ablation deltas (4 variants), optimizer throughput (4 configurations).
All bars start at zero; exact labels and captions identify differing budgets.
Static SVG + PNG are the publication surface; Markdown tables provide values.
Palette: institutional neutral ink + teal; open/hatched marks identify controls.
"""
from pathlib import Path
import argparse
import hashlib
import json
import math
from html import escape

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'docs/public/assets/working-registers'
OUT.mkdir(parents=True, exist_ok=True)
parser = argparse.ArgumentParser()
parser.add_argument('--source', type=Path)
args = parser.parse_args()
data_path = OUT / 'evidence.json'
if args.source:
    def read(name):
        return json.loads((args.source / name).read_text(encoding='utf-8'))
    final = read('final_shard_evaluation.json')
    aggregate = read('aggregate.json')
    pairs = [(42,384,'attnres_reserve64_d384_s42'),(43,384,'selected64_d384_s43'),
             (44,384,'selected64_d384_s44'),(42,512,'reserve64_d512_s42')]
    by_run = {r['run']:r for r in final['results']}
    result = {'date':'2026-09-08', 'scope':'Local matched-backbone experiments; not a paper-scale replication.',
              'final_shard':{'name':'002_00000.parquet','target_tokens':262144,
                             'cache_sha256':final['cache_sha256'],'cross_shard_deduplication':False},
              'pairs':[], 'development_runs':aggregate, 'throughput':[],
              'training_windows':read('paired_seed_statistics.json')['pairs'], 'source_sha256':{}}
    for seed,d,wr in pairs:
        base = f'attnres_d{d}_s{seed}'
        b,w = by_run[base],by_run[wr]
        delta = w['normal']['mean_ce']-b['normal']['mean_ce']
        result['pairs'].append({'seed':seed,'d_model':d,'baseline_run':base,'reserve_run':wr,
            'steps':w['step'],'train_tokens':16777216 if d==384 else 33554432,
            'baseline_ce':b['normal']['mean_ce'],'reserve_ce':w['normal']['mean_ce'],
            'delta_ce':delta,'ppl_change_percent':100*math.expm1(delta)})
    for name in ['batching_attnres_reserve_r64.json','batching_attnres_block4_r0.json']:
        source=read(name)
        for row in source['results']:
            result['throughput'].append({'variant':source['variant'], **row})
    for name in ['final_shard_evaluation.json','aggregate.json','paired_seed_statistics.json',
                 'batching_attnres_reserve_r64.json','batching_attnres_block4_r0.json']:
        result['source_sha256'][name]=hashlib.sha256((args.source/name).read_bytes()).hexdigest()
    data_path.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

data=json.loads(data_path.read_text(encoding='utf-8'))
font=Path('C:/Windows/Fonts/msyh.ttc')
if font.exists():
    font_manager.fontManager.addfont(str(font))
    plt.rcParams['font.family']=font_manager.FontProperties(fname=str(font)).get_name()
plt.rcParams.update({'font.size':12,'axes.unicode_minus':False,'svg.fonttype':'path',
                     'text.color':'#263a38','axes.labelcolor':'#263a38','xtick.color':'#596965',
                     'ytick.color':'#263a38','axes.spines.top':False,'axes.spines.right':False})
INK='#263a38'; TEAL='#267c6d'; LIGHT='#dae9e4'

def canvas(title, subtitle, height=5.6):
    fig,ax=plt.subplots(figsize=(11.5,height))
    fig.subplots_adjust(left=.32,right=.85,top=.72,bottom=.20)
    fig.text(.045,.925,title,fontsize=21,weight='bold')
    fig.text(.045,.84,subtitle,fontsize=11,color='#596965')
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_color('#a7b4af')
    ax.tick_params(axis='y',length=0,pad=12)
    ax.set_axisbelow(True)
    ax.grid(axis='x',color='#e7eeea')
    return fig,ax

def save(fig,name,note):
    fig.text(.045,.06,note,fontsize=10,color='#596965')
    fig.savefig(OUT/f'{name}.svg',facecolor='white')
    fig.savefig(OUT/f'{name}.png',dpi=160,facecolor='white')
    plt.close(fig)

fig,ax=canvas('相同 AttnRes 底座上，四组配对都出现改善',
    '独立 FineWeb 分片 · 262,144 target tokens · 每行是一个配对实验，不是置信区间')
rows=data['pairs']
values=[-r['delta_ce'] for r in rows]
labels=[f"{'15.85M' if r['d_model']==384 else '34.38M'} / seed {r['seed']}" for r in rows]
bars=ax.barh(labels,values,color=[TEAL]*3+[LIGHT],edgecolor=INK,height=.55)
bars[-1].set_hatch('///')
ax.invert_yaxis();ax.set_xlim(0,.068);ax.set_xlabel('CE 降低量（baseline − WR；越大越好）')
for i,r in enumerate(rows):
    ax.text(values[i]+.0015,i,f"{values[i]:.6f}\nPPL {r['ppl_change_percent']:.2f}%",va='center',fontsize=10)
save(fig,'quality','来源：final_shard_evaluation.json · 小模型训练 16.78M tokens；较大模型 33.55M tokens。')

dev={r['run']:r['mean_dev_ce'] for r in data['development_runs']}
base=dev['attnres_d384_s42']
names=['attnres_reserve64_d384_s42','attnres_overwrite64_d384_s42',
       'attnres_reservegate64_d384_s42','attnres_d384_s42']
fig,ax=canvas('完整读取与跨层保留，在本轮消融中更有效',
    '15.85M 附近 · seed 42 · 16.78M training tokens · 两个开发切片平均 CE')
vals=[base-dev[n] for n in names]
bars=ax.barh(['完整 WR-Reserve','去掉 carry：仅 g × c','只读入 gate 分支','纯 Block AttnRes'],vals,
             color=[TEAL,LIGHT,LIGHT,'white'],edgecolor=INK,height=.55)
bars[1].set_hatch('///');bars[2].set_hatch('...')
ax.invert_yaxis();ax.set_xlim(0,.055);ax.set_xlabel('相对纯 AttnRes 的 CE 降低量（越大越好）')
for i,n in enumerate(names):ax.text(vals[i]+.001,i,f'{vals[i]:.6f}\nCE {dev[n]:.6f}',va='center',fontsize=10)
save(fig,'ablation','来源：aggregate.json · 开发集用于选型；消融为从头训练的模型，未作为独立测试结果。')

speed=[r for r in data['throughput'] if r['variant']=='attnres_reserve']
base_speed=next(r for r in data['throughput'] if r['variant']=='attnres_block4' and r['batch']==32)
fig,ax=canvas('100M：矩阵预算相同，实测吞吐仍需单独比较',
    'RTX 5070 Ti · FP32 + TF32 · SDPA + compile · 有效 batch 64 · 2 步预热后测 8 步')
rows=speed+[base_speed]
vals=[r['tokens_per_second']/1000 for r in rows]
labels=[f"WR：{r['batch']} × {r['accumulation']}" for r in speed]+['AttnRes：32 × 2']
bars=ax.barh(labels,vals,color=[LIGHT,LIGHT,TEAL,'white'],edgecolor=INK,height=.55)
bars[-1].set_hatch('///')
ax.invert_yaxis();ax.set_xlim(0,48);ax.set_xlabel('千 tokens / 秒（越大越好；横轴从零开始）')
for i,r in enumerate(rows):ax.text(vals[i]+.7,i,f"{vals[i]:.2f}k\n{r['peak_allocated_bytes']/2**30:.2f} GiB",va='center',fontsize=10)
save(fig,'throughput','来源：batching_*.json · 显存为 PyTorch 峰值已分配；不含数据加载、冷编译、评估与保存。')

# Code-native engineering diagrams: fixed geometry, selectable text, no raster generation.
def start(title,subtitle,w=1100,h=720):
    return [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img"><title>{escape(title)}</title><desc>{escape(subtitle)}</desc>',
    '<defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0 0L8 4L0 8" fill="#596965"/></marker></defs>',
    '<rect width="100%" height="100%" fill="#fff"/>',
    '<style>text{font-family:"Microsoft YaHei","Noto Sans CJK SC",sans-serif;fill:#263a38}.title{font-size:29px;font-weight:700}.sub{font-size:17px;fill:#596965}.label{font-size:20px}.small{font-size:17px}</style>',
    f'<text x="40" y="54" class="title">{escape(title)}</text><text x="40" y="90" class="sub">{escape(subtitle)}</text>']
def box(parts,x,y,w,h,lines,private=False):
    parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{"#e8f2ee" if private else "#f5f7f6"}" stroke="{"#267c6d" if private else "#9aaca5"}"/>')
    for i,line in enumerate(lines):parts.append(f'<text x="{x+w/2}" y="{y+h/2+(i-(len(lines)-1)/2)*27+7}" text-anchor="middle" class="label">{escape(line)}</text>')
def arrow(parts,path):parts.append(f'<path d="{path}" fill="none" stroke="#596965" stroke-width="2" marker-end="url(#arrow)"/>')
def finish(parts,name): (OUT/f'{name}.svg').write_text('\n'.join(parts+['</svg>']),encoding='utf-8')

p=start('从即时输出，到公开 / 私有两种计算去向','左：纯 Block AttnRes   右：相同底座 + WR-Reserve（展开一个非末层 FFN）',h=825)
box(p,45,125,335,72,['公开历史 → DepthRead'])
box(p,45,230,335,65,['RMSNorm'])
box(p,45,330,335,80,['Gate / Up：各 m 通道'])
box(p,45,450,335,80,['全部 m 通道执行 SwiGLU'])
box(p,45,570,335,72,['Down：m → d'])
box(p,45,680,335,75,['公开输出 → partial sum'])
for a,b in [(197,230),(295,330),(410,450),(530,570),(642,680)]:arrow(p,f'M212 {a} V{b-3}')
box(p,450,125,315,72,['相同公开历史 → DepthRead'])
box(p,830,125,225,72,['旧状态 wₗ → Rₗ'],True)
box(p,500,230,480,65,['公开读取 + 工作读取 → RMSNorm'])
arrow(p,'M607 197 V213 H675 V227');arrow(p,'M942 197 V213 H840 V227')
box(p,500,330,480,80,['相同 Gate / Up：各 m 通道'])
arrow(p,'M740 295 V327')
box(p,445,450,285,80,['公开：m − r 通道','SwiGLU'],False)
box(p,775,450,285,80,['私有：r 通道','sigmoid 门 / tanh 候选'],True)
arrow(p,'M660 410 V430 H587 V447');arrow(p,'M820 410 V430 H918 V447')
box(p,445,570,285,72,['Down：m − r → d'])
box(p,775,570,285,72,['wₗ₊₁ = (1−g)wₗ + gc'],True)
arrow(p,'M587 530 V567');arrow(p,'M918 530 V567')
arrow(p,'M1055 161 H1080 V606 H1063')
box(p,445,680,285,75,['公开输出 → partial sum'])
box(p,775,680,285,75,['下一层 FFN 再读取'],True)
arrow(p,'M587 642 V677');arrow(p,'M918 642 V677')
p.append('<text x="40" y="795" class="small">私有指本层没有直接公开投影；新状态不直接进入下一层 Attention，也不直接送入 LM head。</text>')
finish(p,'architecture')

p=start('工作寄存器沿深度传递；各 token 的读写可以并行','每次 forward 从零开始；横向为网络深度，纵向为 token 位置。此图省略公开 Attention 路径。',h=505)
for i,x in enumerate([235,510,785]):
    p.append(f'<text x="{x+105}" y="151" class="label" text-anchor="middle">第 {i+1} 个 FFN</text>')
for t,y in enumerate([190,285,380]):
    p.append(f'<text x="40" y="{y+38}" class="label">token {t+1}：w₀ = 0</text>')
    for i,x in enumerate([235,510,785]):
        box(p,x,y,210,60,[f'读取 / 计算 / 更新'],True)
        if i<2:arrow(p,f'M{x+210} {y+30} H{x+270}')
    arrow(p,f'M185 {y+30} H232')
p.append('<text x="40" y="481" class="small">图中的工作状态没有 token 间的直接连边；跨 token 交互仍由公开的因果 Attention 完成。</text>')
finish(p,'depth-axis')

p=start('省下公开 Down，支付下一层 Read','FFN 矩阵参数与投影 MAC 对齐；逐元素更新、状态存储和内核效率另计。',h=515)
box(p,40,130,490,100,['基线：每层 3dm','Gate / Up  2dm  +  Down  dm'])
box(p,570,130,490,100,['内部层：仍为 3dm','2dm  +  d(m−r)  +  dr'],True)
box(p,40,285,305,100,['首层：只写不读','相对基线 −dr'])
box(p,395,285,310,100,['中间层：读旧、写新','相对基线 0'],True)
box(p,755,285,305,100,['末层：只读不写','相对基线 +dr'])
p.append('<text x="550" y="448" text-anchor="middle" class="title">全网络：3Ldm  +  (L−1)r 个门偏置</text>')
p.append('<text x="550" y="487" text-anchor="middle" class="small">100M 配置：L=10、d=896、m=2400、r=64 → 仅增加 576 个参数</text>')
finish(p,'budget')
print('Wrote evidence.json, 3 scientific charts (SVG + PNG), and 3 architecture diagrams.')
