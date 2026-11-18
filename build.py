# Buduje index.html z szablon.html + _dane (dane obiektow z bfmprojekt.pl) + oficjalny znak Wylinki
import json, html, re
E=lambda t: html.escape(str(t), quote=True)
ob=json.load(open('_dane/obiekty.json',encoding='utf-8'))
li=json.load(open('_dane/lista.json',encoding='utf-8'))
wy=json.load(open('_dane/wymiary.json',encoding='utf-8'))
POPR={'Budynk mieszkaniowy':'Budynek mieszkaniowy','Zespół budynków biurowych. mieszkaniowych i usługowych':'Zespół budynków biurowych, mieszkaniowych i usługowych','Biurowiec i Centrum Logistyczne':'Biurowiec i centrum logistyczne'}
ARCH={'ARTUR JASIŃSKI I WSPÓLNICY BIURO ARCHITEKTONICZNE SP. Z O.O':'Artur Jasiński i Wspólnicy Biuro Architektoniczne','KM rubaszkiewicz sp. z o.o':'KM Rubaszkiewicz','CAVU Architekci sp. z o.o':'CAVU Architekci','APA Zalewski Architekci sp. z o. o':'APA Zalewski Architekci','Bazukastudio Sp. z o.o. Sp. k':'Bazukastudio'}
TYP={'282':'Galeria handlowa'}
def m2(a): return re.sub(r'(\d)\.(\d{3})',r'\1 \2',a).replace(' ,',',').replace('P1- ','P1 - ')
cards=[];data=[]
for i,o in enumerate(ob):
    typ=POPR.get(o['type'],o['type']) or TYP.get(o['id'],'')
    ims=[[f"{o['id']}-{j}",*wy[f"{o['id']}-{j}"]] for j in range(1,o['n']+1)]
    data.append(dict(n=o['name'],c=o['city'],y=o['years'],t=typ,z=o['scope'],a=m2(o['area']),ar=ARCH.get(o['arch'],o['arch']),op=o['opened'],im=ims))
    k=o['id']
    cards.append(f'''   <li><button class="karta" type="button" data-i="{i}" aria-haspopup="dialog"><span class="foto"><img src="img/k/{k}-480.webp" srcset="img/k/{k}-320.webp 320w, img/k/{k}-480.webp 480w, img/k/{k}-800.webp 800w" sizes="(min-width:2400px) 15vw, (min-width:1800px) 18vw, (min-width:1200px) 22vw, (min-width:760px) 30vw, 46vw" width="800" height="600" loading="lazy" decoding="async" alt="{E(o['name'])}, {E(o['city'])}"></span><span class="tab"><span class="nz">{E(o['name'])}</span><span class="mt"><span>{E(o['city'])}</span><span>{E(o['years'] or '-')}</span></span></span></button></li>''')
lis=[]
for x in li:
    nm=x['nazwa']; typ=x.get('typ','')
    if 'commercial' in typ: typ='8 800 m²'
    m=re.match(r'(.*?)\s*\((.*)\)\s*$',nm)
    if m: nm,typ=m.group(1),m.group(2)
    r=x.get('reszta',[])
    zak=[l for l in r if l.lower().startswith('projekt')]
    otw=[l for l in r if l.lower().startswith(('obiekt','otwarcie'))]
    arch=[l.split(':',1)[1].strip() for l in r if l.lower().startswith(('architekt','architect'))]
    opis='; '.join(filter(None,[m2(typ), ', '.join(zak), ', '.join(o.replace('obiekt otwarty','otwarcie') for o in otw), ('architekt: '+arch[0]) if arch else '']))
    lis.append(f'    <li><b>{E(nm)}</b>{E(opis)}</li>')
s=open('szablon.html',encoding='utf-8').read()
s=s.replace('{{CARDS}}','\n'.join(cards)).replace('{{LISTA}}','\n'.join(lis)).replace('{{N}}',str(len(ob))).replace('{{NL}}',str(len(li)))
s=s.replace('{{DATA}}',json.dumps(data,ensure_ascii=False,separators=(',',':')).replace('</',r'<\/'))
s=s.replace('{{BADGE_STYLE}}',open('badge_style.part',encoding='utf-8').read().replace('<style>','').replace('</style>',''))
s=s.replace('{{BADGE_LINK}}',open('badge_link.part',encoding='utf-8').read().strip())
open('index.html','w',encoding='utf-8',newline='\n').write(s)
print('ok',len(ob),len(li),len(s))
