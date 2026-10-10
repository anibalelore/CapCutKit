import importlib.util,sys,copy,json
from pathlib import Path
r=Path(__file__).resolve().parent.parent;sys.path.insert(0,str(r/'capcut-kit'))
sp=importlib.util.spec_from_file_location('bridge',r/'capcut-kit/capcut-bridge.py');b=importlib.util.module_from_spec(sp);sp.loader.exec_module(b)
A=271900000;B=272633333;DELTA=B-A
def mutate(d,folder):
 assert d['duration']==311300000
 for t in d['tracks']:
  out=[]
  for s in t['segments']:
   start=s['target_timerange']['start'];dur=s['target_timerange']['duration'];end=start+dur
   if end<=A:out.append(s);continue
   if start>=B:s['target_timerange']['start']-=DELTA;out.append(s);continue
   for lo,hi in [(start,min(end,A)),(max(start,B),end)]:
    if hi<=lo:continue
    z=copy.deepcopy(s);z['id']=b.uid();z['target_timerange']={'start':lo if lo<A else lo-DELTA,'duration':hi-lo}
    z['source_timerange']={'start':s['source_timerange']['start']+lo-start,'duration':hi-lo}
    out.append(z)
  t['segments']=out
 json.dump({'removed':[A/1e6,B/1e6],'duration':DELTA/1e6},open(r/'video-art/eye-pause-trim.json','w'))
b.edit_draft('1009 (1)',mutate,reopen=False)
