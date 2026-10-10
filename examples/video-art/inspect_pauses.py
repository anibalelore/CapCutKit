import json,subprocess,re,sys
from pathlib import Path
from PIL import Image,ImageDraw
r=Path(__file__).resolve().parent.parent
cuts=json.load(open(r/'rough-cut/transcript/cuts.json',encoding='utf-8'))['segments']
out=subprocess.run([str(r/'capcut-kit/tools/bin/ffmpeg.exe'),'-hide_banner','-i',str(r/'rough-cut/analysis/first-cut.wav'),'-af','silencedetect=noise=-40dB:d=0.65','-f','null','NUL'],capture_output=True,text=True).stderr
pauses=list(zip([float(x) for x in re.findall(r'silence_start: ([\d.]+)',out)],[float(x) for x in re.findall(r'silence_end: ([\d.]+)',out)]))
times=[t for a,b in pauses for t in [a+.12,b-.12]]
if len(sys.argv)>1:times=[float(t) for t in sys.argv[1:]]
sheet=Image.new('RGB',(1000,760),'#111111');dr=ImageDraw.Draw(sheet)
for i,t in enumerate(times):
 cursor=0
 for c in cuts:
  dur=c['end']-c['start']
  if cursor<=t<cursor+dur:source=c['start']+t-cursor;break
  cursor+=dur
 p=r/f'video-art/assets/pause-{i}.jpg'
 subprocess.run([str(r/'capcut-kit/tools/bin/ffmpeg.exe'),'-y','-ss',str(source),'-i',str(r/'IMG_1579.MOV'),'-vf','scale=200:-2','-frames:v','1',str(p)],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,check=True)
 j=i%10
 im=Image.open(p);sheet.paste(im,(j%5*200,j//5*380));dr.text((j%5*200+5,j//5*380+355),str(round(t,2)),fill='white')
 if j==9 or i==len(times)-1:
  sheet.save(r/f'video-art/assets/pauses-contact-{i//10}.jpg');sheet=Image.new('RGB',(1000,760),'#111111');dr=ImageDraw.Draw(sheet)
