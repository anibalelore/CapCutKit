import importlib.util, sys, json, copy, struct
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT/'capcut-kit'))
spec=importlib.util.spec_from_file_location('bridge',ROOT/'capcut-kit/capcut-bridge.py')
b=importlib.util.module_from_spec(spec);spec.loader.exec_module(b)
plan=json.loads((ROOT/'video-art/graphics-plan.json').read_text(encoding='utf-8'))
def kf(seg,prop,points):
    for typ in b.KF_TYPES[prop]:
        entry={'id':b.uid(),'material_id':'','property_type':typ,'keyframe_list':[]}
        for rel,val in points:
            entry['keyframe_list'].append({'id':b.uid(),'curveType':'Line','time_offset':seg['source_timerange']['start']+round(rel*1e6),'left_control':{'x':0.,'y':0.},'right_control':{'x':0.,'y':0.},'values':[val],'string_value':'','graphID':''})
        seg.setdefault('common_keyframes',[]).append(entry)
def mutate(d,folder):
    main=next(t for t in d['tracks'] if t['type']=='video' and t['flag']==0)
    assert len(main['segments'])==24
    assert not any('news-motion-master' in m.get('path','') for m in d['materials']['videos']), 'Already applied'
    fingerprint=[(s['source_timerange'].copy(),s['target_timerange'].copy()) for s in main['segments']]
    mats=d['materials'];track=b.overlay_track(d,1);track['name']='Apoyos animados · noticias IA'
    def media(file,photo=False):
        path=b.local_media(folder,ROOT/'video-art/assets'/file)
        if photo:
            w,h=struct.unpack('>II',path.read_bytes()[16:24]);dur=10800000000
        else:w,h,dur,has_audio=b.probe(path)
        mid=b.uid();m=b.video_material(mid,str(path).replace('\\','/'),w,h,dur,False)
        if photo:m['type']='photo'
        mats['videos'].append(m);return mid
    def overlay(mid,at,dur,src=0,fade=False):
        s=b.segment(mid,round(src*1e6),round(dur*1e6),round(at*1e6),b.segment_extras(mats))
        s['volume']=0.;s['track_render_index']=1;s['render_index']=1
        if fade:kf(s,'opacity',[(0,0.),(.25,1.),(dur-.25,1.),(dur,0.)])
        track['segments'].append(s);return s
    mid=media('news-motion-master.mov')
    for c in plan['overlays']:
        at=c['at'];dur=c['duration']
        if at==141.8:at=142.;dur=5.3
        overlay(mid,at,dur,c['source_start'])
    overlay(media('full-news.png',True),13.3,9.2,fade=True)
    overlay(media('split-top.png',True),31.8,27.5,fade=True)
    track['segments'].sort(key=lambda s:s['target_timerange']['start'])
    for i,s in enumerate(main['segments']):
        s['volume']=1.65;s['last_nonzero_volume']=1.65
        start=s['target_timerange']['start']/1e6;dur=s['target_timerange']['duration']/1e6;end=start+dur
        if end>31.5 and start<59.6:
            def ypos(t):
                if t<=31.5 or t>=59.6:return 0.
                if t<32.1:return -.42*(t-31.5)/.6
                if t<=59.:return -.42
                return -.42*(59.6-t)/.6
            times=sorted(set([start,end]+[t for t in [31.5,32.1,59.,59.6] if start<t<end]))
            kf(s,'y',[(t-start,ypos(t)) for t in times])
        elif i%3==1 and dur>5:
            kf(s,'scale',[(0,1.),(dur,1.045)])
    ref=json.loads((b.DRAFT_ROOT/'1009'/b.DRAFT_FILE).read_text(encoding='utf-8-sig'))
    audio=copy.deepcopy(ref['materials']['audios'][0]);oldid=audio['id'];audio['id']=b.uid()
    music=b.local_media(folder,ROOT/'video-art/assets/tech-news-original-112bpm.wav')
    audio.update(path=str(music).replace('\\','/'),name='Tech News · original · 112 BPM',duration=311300000,type='music',music_id='',app_id=0)
    mats['audios'].append(audio)
    template=next(s for t in ref['tracks'] if t['type']=='audio' for s in t['segments'] if s['material_id']==oldid)
    s=copy.deepcopy(template);s.update(id=b.uid(),material_id=audio['id'],source_timerange={'start':0,'duration':311300000},target_timerange={'start':0,'duration':311300000},common_keyframes=[],keyframe_refs=[],extra_material_refs=[],volume=.4,last_nonzero_volume=.4)
    for cat in ['speeds','placeholder_infos','sound_channel_mappings','vocal_separations']:
        for r in ref['materials'].get(cat,[]):
            if r['id'] in template['extra_material_refs']:
                r=copy.deepcopy(r);r['id']=b.uid();mats[cat].append(r);s['extra_material_refs'].append(r['id'])
    d['tracks'].append({'id':b.uid(),'type':'audio','flag':0,'attribute':0,'name':'Música noticias · original','is_default_name':False,'segments':[s]})
    assert fingerprint==[(s['source_timerange'],s['target_timerange']) for s in main['segments']]
    (ROOT/'video-art/preserved-cuts.json').write_text(json.dumps(fingerprint),encoding='utf-8')
b.edit_draft('1009 (1)',mutate,reopen=False)
print('Applied: 24 cuts preserved, 18 animated cards, 2 images, original ducked music.')
