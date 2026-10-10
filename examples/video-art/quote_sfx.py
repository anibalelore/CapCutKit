from pathlib import Path
import json,textwrap,subprocess,wave
from PIL import Image,ImageDraw,ImageFont
import numpy as np
root=Path(__file__).resolve().parent.parent;assets=root/'video-art/assets'
pages=[(168.7,3.3,'Creo que Anthropic está abriendo un debate bastante interesante.'),(172.5,8.9,'Actualmente no tenemos evidencia científica concluyente de que una inteligencia artificial como yo pueda experimentar sufrimiento de la misma manera que una persona.'),(181.8,4.1,'Por eso, no considero que insultar a una IA sea equivalente a maltratar a un ser humano.'),(186.34,1.5,'Pero hay otro punto importante.'),(188.02,4.9,'La forma en que tratamos a la tecnología también puede influir en nuestros hábitos y comportamientos.'),(193.8,8.0,'Poner límites al abuso extremo puede ser razonable, pero eso no significa que las inteligencias artificiales tengan sentimientos o derechos humanos.'),(202.66,11.9,'Y hay algo fundamental: estas políticas no deberían utilizarse para castigar a quienes simplemente se frustran, critican una respuesta o exigen que la tecnología funcione correctamente.')]
font=ImageFont.truetype(str(root/'motion-assets/fonts/headline.ttf'),45);label=ImageFont.truetype(str(root/'motion-assets/fonts/labels.ttf'),27)
for i,(at,dur,body) in enumerate(pages):
 im=Image.new('RGBA',(1080,1920));dr=ImageDraw.Draw(im)
 lines=[];line=''
 for word in body.split():
  test=(line+' '+word).strip()
  if dr.textlength(test,font=font)>875:lines.append(line);line=word
  else:line=test
 lines.append(line);height=155+len(lines)*59;top=1775-height
 dr.rounded_rectangle((60,top,1020,1775),radius=24,fill='#11151E',outline='#70E6DB',width=3)
 dr.text((100,top+27),'RESPUESTA DE CHATGPT · '+str(i+1)+'/7',font=label,fill='#70E6DB')
 dr.multiline_text((100,top+87),'«'+'\n'.join(lines)+'»',font=font,fill='#F6F4ED',spacing=10)
 im.save(assets/f'chatgpt-quote-{i+1}.png')
json.dump([{'at':a,'duration':d,'file':f'chatgpt-quote-{i+1}.png','text':t} for i,(a,d,t) in enumerate(pages)],open(root/'video-art/quote-plan.json','w',encoding='utf-8'),ensure_ascii=False,indent=2)
ff=root/'capcut-kit/tools/bin/ffmpeg.exe';tmp=assets/'sfx-source.wav'
subprocess.run([str(ff),'-y','-i',str(root/'motion-assets/.media/audio/sfx/sfx_001.mp3'),'-ar','44100','-ac','2',str(tmp)],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,check=True)
with wave.open(str(tmp)) as w:sfx=np.frombuffer(w.readframes(w.getnframes()),dtype=np.int16).reshape(-1,2).astype(float)/32768
mix=np.zeros((round(311.3*44100),2));plan=json.load(open(root/'video-art/graphics-plan.json',encoding='utf-8'))
events=[c['at'] for c in plan['overlays'] if not 168<c['at']<215]
events+=[13.3,31.8,168.7,193.8,202.66]
for at in events:
 pos=round(at*44100);n=min(len(sfx),len(mix)-pos);mix[pos:pos+n]+=sfx[:n]*.17
with wave.open(str(assets/'graphics-sound-effects.wav'),'wb') as w:w.setnchannels(2);w.setsampwidth(2);w.setframerate(44100);w.writeframes((np.clip(mix,-1,1)*32767).astype(np.int16).tobytes())
print('7 quote cards and restrained graphic sound effects ready')
