import json,importlib.util,copy,sys
from pathlib import Path
kit=Path('capcut-kit').resolve();sys.path.insert(0,str(kit))
spec=importlib.util.spec_from_file_location('bridge',kit/'capcut-bridge.py')
b=importlib.util.module_from_spec(spec);spec.loader.exec_module(b)
plan=json.loads(Path('rough-cut/transcript/cuts.json').read_text(encoding='utf-8'))
def mutate(d,folder):
 tracks=[t for t in d['tracks'] if t['type']=='video']
 if len(tracks)!=1 or len(tracks[0]['segments'])!=1:
  raise SystemExit('Expected the untouched single-clip assembly; refusing to replace existing edits.')
 template=tracks[0]['segments'][0]
 material=next(m for m in d['materials']['videos'] if m['id']==template['material_id'])
 if Path(material['path']).name!='IMG_1579.MOV':
  raise SystemExit('Wrong source video; no edit applied.')
 out=[];cursor=0
 for cut in plan['segments']:
  seg=copy.deepcopy(template)
  start=round(cut['start']*1e6);duration=round((cut['end']-cut['start'])*1e6)
  seg['id']=b.uid();seg['source_timerange']={'start':start,'duration':duration}
  seg['target_timerange']={'start':cursor,'duration':duration}
  out.append(seg);cursor+=duration
 tracks[0]['segments']=out
 d['duration']=cursor
b.edit_draft('1009 (1)',mutate,reopen=False)
print('Applied',len(plan['segments']),'clips')
