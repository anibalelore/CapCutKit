import json
from pathlib import Path
# Decode with the already installed FFmpeg instead of the unavailable PyAV DLL.
import sys, types, wave
import numpy as np
adapter=types.ModuleType('faster_whisper.audio')
def decode_audio(path,sampling_rate=16000,split_stereo=False):
    with wave.open(str(path),'rb') as f:
        assert f.getframerate()==sampling_rate and f.getnchannels()==1
        return np.frombuffer(f.readframes(f.getnframes()),dtype=np.int16).astype(np.float32)/32768

def pad_or_trim(array,length=3000,axis=-1):
    if array.shape[axis]>length:
        array=array.take(indices=range(length),axis=axis)
    if array.shape[axis]<length:
        widths=[(0,0)]*array.ndim
        widths[axis]=(0,length-array.shape[axis])
        array=np.pad(array,widths)
    return array
adapter.decode_audio=decode_audio
adapter.pad_or_trim=pad_or_trim
sys.modules['faster_whisper.audio']=adapter
from faster_whisper import WhisperModel
model=WhisperModel('small',device='cpu',compute_type='int8',cpu_threads=6)
segments, info=model.transcribe('rough-cut/analysis/first-cut.wav',language='es',word_timestamps=True,vad_filter=True,beam_size=3)
rows=[]
for s in segments:
 row={'start':s.start,'end':s.end,'text':s.text,'words':[{'start':w.start,'end':w.end,'word':w.word} for w in s.words]}
 rows.append(row)
 print(f'{s.start:.2f}-{s.end:.2f} {s.text}',flush=True)
 Path('rough-cut/analysis/first-cut-transcript.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
