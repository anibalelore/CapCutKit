import json
from pathlib import Path
from html import escape

root=Path(__file__).resolve().parent.parent
cards=[
 (0.1,5.2,'DEBATE IA','¿TE PUEDEN BLOQUEAR?','Por insultar a una inteligencia artificial','question'),
 (23.0,6.0,'EL MATIZ','LA CLAVE ES EL CONTEXTO','Hay detalles que cambian la lectura','text'),
 (66.0,5.5,'LA PREGUNTA','¿UN INSULTO = UN BANEO?','Antes de sacar conclusiones…','question'),
 (81.5,7.0,'EL LÍMITE','ABUSO EXTREMO','Repetitivo · sin finalidad justificable','text'),
 (89.9,5.3,'OJO CON ESTO','CRITICAR ≠ ABUSAR','Frustración · crítica · pruebas de seguridad','contrast'),
 (98.5,8.0,'LA CONVERSACIÓN','CONVERSACIÓN FINALIZADA','El modelo puede dejar de responder','chat'),
 (118.0,5.6,'TRANSPARENCIA','VAMOS A LOS DATOS','Las cifras mencionadas en el vídeo','text'),
 (129.0,6.0,'CUENTAS BLOQUEADAS','11,4 MILLONES','Cifra citada en la narración','stat'),
 (136.4,5.5,'APELACIONES','398 MIL','Cifra citada en la narración','stat'),
 (141.8,5.5,'DECISIONES REVERTIDAS','42 MIL','Cifra citada en la narración','stat'),
 (159.0,6.0,'OTRA PERSPECTIVA','LE PREGUNTÉ A CHATGPT','¿Qué opina una IA sobre el debate?','chat'),
 (172.4,8.0,'LA RESPUESTA','¿PUEDE SUFRIR UNA IA?','Una pregunta distinta a la conducta humana','question'),
 (193.8,7.0,'DOS PLANOS','LÍMITES AL ABUSO','≠ derechos humanos para una IA','contrast'),
 (205.0,8.0,'EL ESPACIO PARA CRITICAR','FRUSTRARSE · CRITICAR','Exigir que la tecnología funcione','text'),
 (221.6,7.0,'EL FOCO DEL DEBATE','CÓMO NOS COMPORTAMOS','Cuando interactuamos con la tecnología','text'),
 (234.2,7.0,'FUERA DE LA PANTALLA','DE LA IA A LA VIDA REAL','Familia · hijos · colegas','network'),
 (255.8,7.5,'TU CRITERIO','¿SANCIÓN O EXCESO?','¿Dónde pondrías tú el límite?','question'),
 (306.3,5.0,'ABRAMOS EL DEBATE','TE LEO EN COMENTARIOS','¿Qué opinas tú?','chat'),
]
cursor=0; scenes=[];tweens=[];manifest=[]
for i,(at,dur,kicker,title,sub,kind) in enumerate(cards):
 sid=f'card{i}';scene=f'scene{i}';bar=''.join(f'<i class="meter m{j}"></i>' for j in range(9))
 scenes.append(f'''<section id="{scene}" class="clip scene" data-start="{cursor}" data-duration="{dur}" data-track-index="{i}">
 <div class="scene-content"><article id="{sid}" class="panel {kind}">
 <div class="top"><span class="status"></span><span class="kicker">{escape(kicker)}</span><span class="edition">IA / 26</span></div>
 <h1>{escape(title)}</h1><p>{escape(sub)}</p><div class="bottom"><div class="meters">{bar}</div><span class="brand">anibaelore</span></div>
 <div class="rule"></div></article></div></section>''')
 tweens+= [f'''tl.from("#{sid}",{{y:42,opacity:0,duration:.4,ease:"power3.out"}},{cursor+.12});
 tl.from("#{sid} h1",{{x:-22,opacity:0,duration:.43,ease:"expo.out"}},{cursor+.25});
 tl.from("#{sid} p",{{y:14,opacity:0,duration:.4,ease:"sine.out"}},{cursor+.4});
 tl.from("#{sid} .rule",{{scaleX:0,transformOrigin:"left",duration:.6,ease:"power2.out"}},{cursor+.22});
 tl.from("#{sid} .meter",{{scaleY:.15,transformOrigin:"bottom",duration:.5,stagger:.06,ease:"back.out(1.2)"}},{cursor+.55});
 tl.to("#{sid}",{{opacity:0,y:12,duration:.25,ease:"power2.in"}},{cursor+dur-.25});''']
 manifest.append({'at':at,'duration':dur,'source_start':cursor,'title':title,'kind':kind})
 cursor+=dur
html='''<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=1080,height=1920">
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script><style>
@font-face{font-family:News;src:url(fonts/headline.ttf);font-weight:100 900}
@font-face{font-family:Data;src:url(fonts/labels.ttf);font-weight:400}
*{box-sizing:border-box;margin:0;padding:0}html,body{width:1080px;height:1920px;background:transparent;overflow:hidden}
#root{width:100%;height:100%;background:transparent}.scene{position:absolute;inset:0;width:100%;height:100%}
.scene-content{width:100%;height:100%;padding:1280px 70px 180px;display:flex;flex-direction:column;justify-content:center;gap:20px}
.panel{position:relative;width:100%;padding:32px 38px 25px;background:#11151E;border-radius:22px;border:2px solid #FFB957;box-shadow:0 18px 36px #11151E60}
.top{display:flex;align-items:center;gap:14px;color:#FFB957}.status{width:12px;height:12px;background:#FFB957;border-radius:50%;flex-shrink:0}
.kicker{font:28px Data,monospace;letter-spacing:1px}.edition{margin-left:auto;font:23px Data,monospace;color:#BB96ED}
h1{font:900 82px/1.04 News,sans-serif;letter-spacing:-2px;color:#F6F4ED;margin:24px 0 18px;max-width:864px}
p{font:400 34px/1.25 News,sans-serif;color:#F6F4ED;max-width:855px}.stat h1{font-size:106px;color:#FFB957}.contrast h1,.question h1{color:#70E6DB}
.bottom{display:flex;justify-content:space-between;align-items:center;margin-top:28px}.brand{font:28px Data,monospace;color:#BB96ED}.meters{display:flex;gap:7px;height:32px;align-items:flex-end}
.meter{display:block;width:10px;background:#70E6DB;border-radius:3px;height:22px}.m1,.m4,.m7{height:32px}.m2,.m5,.m8{height:15px}
.rule{height:3px;position:absolute;left:38px;right:38px;bottom:0;background:#FFB957}
</style></head><body><div id="root" data-composition-id="news-overlays" data-start="0" data-duration="DURATION" data-width="1080" data-height="1920">SCENES</div>
<script>window.__timelines=window.__timelines||{};const tl=gsap.timeline({paused:true});TWEENS window.__timelines['news-overlays']=tl;</script></body></html>'''
html=html.replace('DURATION',str(cursor)).replace('SCENES',''.join(scenes)).replace('TWEENS','\n'.join(tweens))
(root/'motion-assets/index.html').write_text(html,encoding='utf-8')
(root/'video-art/graphics-plan.json').write_text(json.dumps({'master_duration':cursor,'overlays':manifest,'images':[{'at':13.3,'duration':9.2,'file':'Anthropic’s Claude Policy Alert.png','layout':'full'},{'at':31.8,'duration':27.5,'file':'ChatGPT Image Oct 9, 2026, 09_14_05 PM.png','layout':'top-image-bottom-speaker'}]},ensure_ascii=False,indent=2),encoding='utf-8')
print('Authored',len(cards),'overlays;',cursor,'seconds of motion assets')
