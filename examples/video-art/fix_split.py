import importlib.util,sys,uuid
from pathlib import Path
root=Path(__file__).resolve().parent.parent;sys.path.insert(0,str(root/'capcut-kit'))
sp=importlib.util.spec_from_file_location('bridge',root/'capcut-kit/capcut-bridge.py');b=importlib.util.module_from_spec(sp);sp.loader.exec_module(b)
def mutate(d,folder):
    for t in d['tracks']:
        if t['type']=='video' and t['flag']==0:
            for s in t['segments']:
                for k in s.get('common_keyframes',[]):
                    if k['property_type']=='KFTypePositionY':
                        for p in k['keyframe_list']:p['values'][0]*=.72/.64
                        for typ in ['KFTypeScaleX','KFTypeScaleY']:
                            z=__import__('copy').deepcopy(k);z['id']=str(uuid.uuid4());z['property_type']=typ
                            for p in z['keyframe_list']:
                                p['id']=str(uuid.uuid4());p['values'][0]=1.+p['values'][0]*.28/.72
                            s['common_keyframes'].append(z)
b.edit_draft('1009 (1)',mutate,reopen=False)
