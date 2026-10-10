"""Original 112 BPM electronic news bed, deterministic synthesis and voice ducking."""
import wave,json
from pathlib import Path
import numpy as np
from scipy.signal import butter,sosfilt

root=Path(__file__).resolve().parent.parent
sr=44100;duration=311.3;bpm=112;beat=60/bpm
mix=np.zeros((round(sr*duration),2),dtype=np.float32)
rng=np.random.default_rng(901)
def add(signal,at,level=1,pan=0):
    pos=round(at*sr);n=min(len(signal),len(mix)-pos)
    if n<=0:return
    signal=signal[:n]*level
    mix[pos:pos+n,0]+=signal*np.sqrt((1-pan)/2)
    mix[pos:pos+n,1]+=signal*np.sqrt((1+pan)/2)
def osc(freq,length,kind='sine'):
    t=np.arange(round(length*sr),dtype=np.float32)/sr
    s=np.sin(2*np.pi*freq*t)
    if kind=='pluck':s+=.3*np.sin(2*np.pi*freq*2*t)+.14*np.sin(2*np.pi*freq*3*t)
    env=(1-np.exp(-t/.008))*np.exp(-t/(length*.28))
    return s*env
def midi(n):return 440*2**((n-69)/12)
roots=[45,41,48,43]
for bar in range(int(np.ceil(duration/(beat*4)))):
    at=bar*beat*4;rootnote=roots[(bar//4)%4]
    phase=(bar//16)%3
    # Bass pattern, varied every sixteen bars.
    for off,note in [(0,rootnote),(1.5,rootnote+12),(2,rootnote),(3.5,rootnote+7)]:
        add(osc(midi(note),beat*.7,'pluck'),at+off*beat,.17)
    # Crisp kick, restrained snare and hi-hats.
    for off in (0,2):
        t=np.arange(round(sr*.24))/sr
        kick=np.sin(2*np.pi*(48*t+70*.018*(1-np.exp(-t/.018))))*np.exp(-t/.055)
        add(kick,at+off*beat,.22)
    for off in (1,3):
        t=np.arange(round(sr*.14))/sr
        noise=rng.standard_normal(len(t)).astype(np.float32)
        snap=sosfilt(butter(2,[900,6500],btype='bandpass',fs=sr,output='sos'),noise)*np.exp(-t/.028)
        add(snap,at+off*beat,.085)
    for off in np.arange(.5,4,.5):
        t=np.arange(round(sr*.05))/sr
        hat=sosfilt(butter(2,7000,btype='highpass',fs=sr,output='sos'),rng.standard_normal(len(t)))*np.exp(-t/.009)
        add(hat,at+off*beat,.033,pan=(-.4 if off%1 else .4))
    # A clear but sparse arpeggio rather than an incessant melody.
    notes=[rootnote+24,rootnote+31,rootnote+36,rootnote+34]
    for j in range(8):
        if phase==1 and j%2:continue
        add(osc(midi(notes[(j+bar)%4]),beat*.8,'pluck'),at+j*beat/2,.034,pan=.45*(-1)**j)
    # Soft chord bed and occasional riser to mark sections.
    if bar%2==0:
        chord=sum(osc(midi(n),beat*7) for n in [rootnote+12,rootnote+15,rootnote+19])
        add(chord,at,.025)
    if bar%16==15:
        t=np.arange(round(sr*beat*2))/sr
        sw=rng.standard_normal(len(t)).astype(np.float32)*(t/(beat*2))**2
        sw=sosfilt(butter(2,[1700,5000],btype='bandpass',fs=sr,output='sos'),sw)
        add(sw,at+2*beat,.028)
# Light stereo delay, deterministic.
delay=round(sr*beat*.75)
mix[delay:,0]+=mix[:-delay,1]*.12
mix[delay:,1]+=mix[:-delay,0]*.12
rms=np.sqrt(np.mean(mix**2));mix*=10**(-23/20)/max(rms,1e-7)
with wave.open(str(root/'rough-cut/analysis/first-cut.wav'),'rb') as f:
    voice=np.frombuffer(f.readframes(f.getnframes()),dtype=np.int16).astype(np.float32)/32768
window=1600
levels=np.sqrt(np.array([np.mean(voice[i:i+window]**2) for i in range(0,len(voice),window)]))
activity=np.clip((levels-.004)/.025,0,1)
times=np.arange(len(mix))/sr
duck=np.interp(times,np.arange(len(activity))*.1,1-.5*activity)
duck=sosfilt(butter(1,3,fs=sr,output='sos'),duck).astype(np.float32)
fade=np.minimum(1,times/1.2)*np.minimum(1,(duration-times)/2.4)
mix*= (duck*fade)[:,None]
mix=np.tanh(mix)
path=root/'video-art/assets/tech-news-original-112bpm.wav'
with wave.open(str(path),'wb') as f:
    f.setnchannels(2);f.setsampwidth(2);f.setframerate(sr)
    f.writeframes((np.clip(mix,-1,1)*32767).astype(np.int16).tobytes())
(root/'video-art/music-notes.json').write_text(json.dumps({'title':'Tech News / 112','composition':'Original procedural electronic news bed','bpm':bpm,'duration':duration,'voice_ducking':'up to 6 dB, driven by the preserved first cut','capcut_volume':.4},indent=2),encoding='utf-8')
print(path,'RMS dB',20*np.log10(np.sqrt(np.mean(mix**2))),'peak',float(np.max(abs(mix))))
