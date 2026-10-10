import importlib.util,sys,json,copy
from pathlib import Path
r=Path(__file__).resolve().parent.parent;sys.path.insert(0,str(r/'capcut-kit'))
sp=importlib.util.spec_from_file_location('bridge',r/'capcut-kit/capcut-bridge.py');b=importlib.util.module_from_spec(sp);sp.loader.exec_module(b)
def mutate(d,folder):
 mats=d['materials'];main=next(t for t in d['tracks'] if t['type']=='video' and t['flag']==0)
 assert not any('chatgpt-quote-' in m.get('path','') for m in mats['videos'])
 for t in d['tracks']:
  if t['type']=='video' and t['flag']==2:
   t['segments']=[s for s in t['segments'] if not 168000000<=s['target_timerange']['start']<215000000]
 tr=b.overlay_track(d,2);tr['name']='Cita literal · Respuesta de ChatGPT'
 for p in json.load(open(r/'video-art/quote-plan.json',encoding='utf-8')):
  path=b.local_media(folder,r/'video-art/assets'/p['file']);mid=b.uid();m=b.video_material(mid,str(path).replace('\\','/'),1080,1920,10800000000,False);m['type']='photo';mats['videos'].append(m)
  s=b.segment(mid,0,round(p['duration']*1e6),round(p['at']*1e6),b.segment_extras(mats));s.update(volume=0.,track_render_index=2,render_index=2);tr['segments'].append(s)
 music=next(t for t in d['tracks'] if t['type']=='audio');template=music['segments'][0]
 old=next(m for m in mats['audios'] if m['id']==template['material_id']);m=copy.deepcopy(old);m['id']=b.uid();m['path']=str(b.local_media(folder,r/'video-art/assets/graphics-sound-effects.wav')).replace('\\','/');m['name']='Efectos suaves · gráficos';mats['audios'].append(m)
 s=copy.deepcopy(template);s.update(id=b.uid(),material_id=m['id'],volume=1.,last_nonzero_volume=1.)
 d['tracks'].append({'id':b.uid(),'type':'audio','flag':0,'attribute':0,'name':'Efectos · entradas GC','is_default_name':False,'segments':[s]})
b.edit_draft('1009 (1)',mutate,reopen=False)
