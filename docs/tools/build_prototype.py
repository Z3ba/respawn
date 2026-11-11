"""Build a local clickable concept and editable SVG screens. No live shop data."""
from pathlib import Path
from html import escape
import json

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'docs/design'
BG, CARD, ACCENT, TEXT, MUTED = '#111116', '#1D1D25', '#BDA4FF', '#F4F1FA', '#B7B3C5'
SCREENS = [
    ('home', 'Katalog'), ('search', 'Pretraga'), ('detail', 'Detalji proizvoda'),
    ('login', 'Prijava'), ('register', 'Registracija'), ('favorites', 'Omiljeno'),
    ('cart', 'Korpa'), ('delivery', 'Dostava'), ('payment', 'Plaćanje'),
    ('success', 'Potvrda porudžbine'), ('payment-error', 'Neuspešno plaćanje'),
    ('profile', 'Profil'), ('orders', 'Porudžbine'), ('admin', 'Administracija'),
]

def rect(x, y, w, h, fill=CARD, radius=16, stroke=None):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="{fill}"' + (f' stroke="{stroke}"' if stroke else '') + '/>'

def text(x, y, value, size=14, fill=TEXT, weight=400, anchor='start'):
    return f'<text x="{x}" y="{y}" fill="{fill}" font-family="Arial, sans-serif" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}">{escape(value)}</text>'

def lines(x, y, values, size=14, fill=MUTED, gap=23, weight=400, anchor='start'):
    return ''.join(text(x, y + gap*i, value, size, fill, weight, anchor) for i, value in enumerate(values))

def link(content, target, label):
    return f'<a href="#{target}" data-go="{target}" aria-label="{escape(label)}">{content}</a>'

def button(y, label, target, primary=True, x=24, width=342):
    return link(rect(x, y, width, 52, ACCENT if primary else CARD, 14) +
                text(x + width/2, y+32, label, 15, BG if primary else TEXT, 700, 'middle'), target, label)

def field(y, label, value='', x=24, width=342):
    return text(x, y, label, 12, MUTED, 700) + rect(x, y+12, width, 52) + text(x+16, y+44, value or label, 14, TEXT if value else MUTED)

def tag(x, y, label, width=90, active=False, target='search'):
    return link(rect(x,y,width,36, '#3C2D59' if active else CARD,18) + text(x+width/2,y+23,label,12,ACCENT if active else MUTED,600,'middle'),target,label)

def keyboard(x,y,scale=1):
    parts=[f'<g transform="translate({x} {y}) scale({scale})">',
           rect(0,0,280,114,'#252330',14,'#777087'), rect(8,8,264,98,'#17151E',9)]
    for row in range(4):
        for col in range(12):
            parts.append(rect(15+col*21,15+row*19,17,14, ['#63517D','#8E6FC2','#AE8BEA'][row%3],3))
    parts += [rect(57,92,119,8,'#A98AD8',3),'</g>']
    return ''.join(parts)

def mouse(x,y,scale=1):
    return f'<g transform="translate({x} {y}) scale({scale})"><path d="M50 4C15 4 6 34 6 73C6 112 22 132 50 132C78 132 94 112 94 73C94 34 85 4 50 4Z" fill="#373240" stroke="#AC8AE8" stroke-width="2"/><path d="M50 5V59M7 57H93" fill="none" stroke="#BDA4FF" stroke-width="2"/>{rect(45,22,10,24,ACCENT,5)}</g>'

def product_card(x,y,name,price,kind='keyboard'):
    art=keyboard(x+9,y+19,.48) if kind=='keyboard' else mouse(x+53,y+7,.65)
    return link(rect(x,y,164,204)+art+text(x+12,y+126,'RESPAWN ORIGINALS',8,MUTED,700)+text(x+12,y+151,name,14,TEXT,700)+text(x+12,y+181,price,15,ACCENT,700),'detail',f'Detalji: {name}')

def item(y=171):
    return rect(24,y,342,130)+rect(36,y+14,92,94,'#2B2537',12)+keyboard(40,y+44,.30)+text(143,y+32,'Nova TKL',17,TEXT,700)+text(143,y+55,'Mehanička · ljubičasta',12,MUTED)+text(143,y+83,'12.990 RSD',17,ACCENT,700)+text(143,y+108,'Količina: 1',12,MUTED)

def nav(active='home'):
    p=[rect(0,760,390,84,CARD,0)]
    for i,(key,label) in enumerate([('home','Početna'),('search','Pretraga'),('cart','Korpa'),('profile','Profil')]):
        x=49+i*97
        color=ACCENT if key==active else MUTED
        paths={
            'home':'M-10 0L0-9L10 0V10H3V3H-3V10H-10Z',
            'search':'M6 6L12 12M9-2A9 9 0 1 1-9-2A9 9 0 1 1 9-2',
            'cart':'M-9-5H9V11H-9ZM-4-5V-8A4 4 0 0 1 4-8V-5',
            'profile':'M-10 11C-10 0 10 0 10 11ZM4-6A4 4 0 1 1-4-6A4 4 0 1 1 4-6',
        }
        icon=f'<g transform="translate({x} 790)" fill="none" stroke="{color}" stroke-width="1.7" stroke-linejoin="round" stroke-linecap="round"><path d="{paths[key]}"/></g>'
        p.append(link(icon+text(x,820,label,10,color,600,'middle'),key,label))
    return ''.join(p)

def shell(key,title,body):
    header=text(24,32,'9:41',12,TEXT,700)+text(365,32,'LTE  ▰',11,MUTED,400,'end')
    header+=link(text(24,80,'respawn.',29,TEXT,900),'home','Početna')
    header+=link(rect(326,52,40,40,CARD,20)+text(346,78,'○',25,ACCENT,400,'middle'),'profile','Profil')
    active=key if key in ['home','search','cart','profile'] else 'home'
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="390" height="844" viewBox="0 0 390 844" role="group" aria-label="{escape(title)}" data-screen="{key}"><title>{escape(title)} - Respawn UI koncept</title>{rect(0,0,390,844,BG,0)}{header}{body}{nav(active)}</svg>'

def build(key):
    title=dict(SCREENS)[key]
    if key=='home':
        body=rect(24,112,342,215,'#39264F',24)+text(44,145,'LEVEL UP YOUR SETUP',10,ACCENT,700)
        body+=lines(44,188,['Tvoj sledeći','upgrade.'],34,TEXT,38,800)
        body+=text(44,253,'Gaming oprema za tvoj način igre.',12,'#DED5F0')
        body+=button(273,'Istraži ponudu  →','search',True,44,225)
        body+=text(24,370,'Pronađi svoju opremu',20,TEXT,700)
        body+=tag(24,389,'Tastature',100,True)+tag(132,389,'Miševi',74)+tag(214,389,'Slušalice',87)+tag(309,389,'Sve',57)
        body+=text(24,467,'Izdvojeno za tvoj setup',20,TEXT,700)
        body+=product_card(24,487,'Nova TKL','12.990 RSD')+product_card(202,487,'Pulse Wireless','7.490 RSD','mouse')
        body+=text(24,731,'Oprema koja prati tvoj stil igre.',12,MUTED)
    elif key=='search':
        body=text(24,137,'Pronađi svoj upgrade',26,TEXT,700)+field(173,'PRETRAGA','tastatura')
        body+=tag(24,258,'Tastature',106,True)+tag(138,258,'Cena',72)+tag(218,258,'Brend',72)
        body+=text(24,331,'Rezultati pretrage',18,TEXT,700)+product_card(24,354,'Nova TKL','12.990 RSD')
        body+=text(24,600,'Primer filtriranog kataloga.',13,MUTED)
    elif key=='detail':
        body=text(24,126,'TASTATURE / RESPAWN',10,ACCENT,700)+rect(24,147,342,191)
        body+=keyboard(51,189,1)+text(24,380,'Nova TKL',30,TEXT,800)+text(24,409,'Mehanička tastatura · bežična',14,MUTED)
        body+=text(24,455,'12.990 RSD',28,ACCENT,700)+tag(24,479,'Na stanju',100,True,'detail')
        body+=lines(24,554,['Kompaktan TKL format, tihi prekidači','i RGB osvetljenje za tvoj setup.'],14)
        body+=text(24,621,'Povezivanje: USB-C / Bluetooth',13,MUTED)
        body+=button(649,'Dodaj u korpu','cart')+button(704,'Sačuvaj u omiljeno','favorites',False)
    elif key in ('login','register'):
        register=key=='register'
        body=text(24,148,'Kreiraj svoj nalog' if register else 'Dobro došao nazad.',27,TEXT,800)
        body+=text(24,179,'Tvoja oprema. Tvoje porudžbine.',14,MUTED)
        y=225
        if register:body+=field(y,'IME I PREZIME','Tvoje ime');y+=94
        body+=field(y,'E-MAIL','ime@primer.rs')+field(y+94,'LOZINKA','••••••••••')
        body+=button(y+190,'Registruj se' if register else 'Prijavi se','profile')
        body+=button(y+254,'Već imaš nalog? Prijava' if register else 'Nemaš nalog? Registracija','login' if register else 'register',False)
        body+=lines(24,705,['Vizuelni prikaz forme.','Prototip ne čuva podatke.'],12)
    elif key=='favorites':
        body=text(24,141,'Omiljena oprema',28,TEXT,800)+text(24,169,'Sačuvaj ideje za sledeći upgrade.',13,MUTED)
        body+=product_card(24,204,'Nova TKL','12.990 RSD')+button(456,'Nastavi istraživanje','home',False)
    elif key=='cart':
        body=text(24,141,'Tvoja korpa',28,TEXT,800)+text(24,165,'1 proizvod za tvoj setup',13,MUTED)+item(188)
        body+=rect(24,359,342,176)+text(44,394,'Pregled porudžbine',17,TEXT,700)
        body+=text(44,432,'Proizvodi',14,MUTED)+text(346,432,'12.990 RSD',14,TEXT,600,'end')
        body+=text(44,465,'Dostava',14,MUTED)+text(346,465,'Besplatna',14,TEXT,600,'end')
        body+=text(44,506,'Ukupno',17,TEXT,700)+text(346,506,'12.990 RSD',20,ACCENT,700,'end')
        body+=button(573,'Nastavi na dostavu','delivery')+button(638,'Nastavi kupovinu','home',False)
    elif key=='delivery':
        body=text(24,139,'Gde šaljemo opremu?',26,TEXT,800)+text(24,171,'01 DOSTAVA   /   02 PLAĆANJE',10,ACCENT,700)
        body+=field(212,'IME I PREZIME','Ime primaoca')+field(306,'TELEFON','Kontakt telefon')+field(400,'ADRESA','Ulica i broj')
        body+=field(494,'GRAD','Grad',24,190)+field(494,'POŠTANSKI BROJ','Broj',226,140)
        body+=button(614,'Nastavi na plaćanje','payment')+button(680,'Nazad na korpu','cart',False)
    elif key=='payment':
        body=text(24,141,'Kako želiš da platiš?',26,TEXT,800)+text(24,174,'01 DOSTAVA   /   02 PLAĆANJE',10,ACCENT,700)
        body+=link(rect(24,210,342,90,'#30243F',16,ACCENT)+text(44,244,'Kartica · Stripe',18,TEXT,700)+text(44,274,'Test režim · bez stvarne naplate',12,MUTED),'success','Simuliraj uspešno Stripe test plaćanje')
        body+=link(rect(24,316,342,82)+text(44,350,'Plaćanje pouzećem',18,TEXT,700)+text(44,376,'Plaćanje pri preuzimanju',12,MUTED),'success','Simuliraj poručivanje pouzećem')
        body+=text(24,450,'Ukupno',16,MUTED)+text(366,450,'12.990 RSD',24,ACCENT,700,'end')
        body+=lines(24,503,['Za karticu se otvara Stripe PaymentSheet.','Ovaj prototip samo prikazuje korisnički tok.'],12)
        body+=button(583,'Simuliraj uspešno plaćanje','success')+button(649,'Prikaži neuspešno plaćanje','payment-error',False)
    elif key in ('success','payment-error'):
        success=key=='success'
        body=rect(143,204,104,104,'#30243F',52)+text(195,273,'✓' if success else '!',57,ACCENT,700,'middle')
        body+=text(195,371,'Oprema je na putu.' if success else 'Plaćanje nije uspelo.',27,TEXT,800,'middle')
        body+=lines(195,414,['Porudžbina je primljena.','Status prati u svojim porudžbinama.'] if success else ['Naplata nije potvrđena.','Pokušaj ponovo ili izaberi pouzeće.'],14,anchor='middle')
        # Center supporting copy without changing generic text helper.
        body+=button(508,'Moje porudžbine' if success else 'Pokušaj ponovo','orders' if success else 'payment')
        body+=button(574,'Nazad na početnu' if success else 'Izaberi drugi način plaćanja','home' if success else 'payment',False)
        body+=text(195,692,'SIMULIRANI ISHOD · UI KONCEPT',10,MUTED,700,'middle')
    elif key=='profile':
        body=text(24,140,'Tvoj profil',28,TEXT,800)+rect(24,171,342,93)+text(44,210,'Hej, igraču.',21,TEXT,700)+text(44,238,'Tvoja oprema na jednom mestu.',13,MUTED)
        for i,(label,target) in enumerate([('Moje porudžbine','orders'),('Omiljena oprema','favorites'),('Administracija · admin uloga','admin'),('Prijava / promena naloga','login')]):
            body+=button(296+i*71,label+'  →',target,False)
        body+=lines(24,649,['Administracija je u konačnoj aplikaciji','dostupna samo potvrđenom administratoru.'],12)
    elif key=='orders':
        body=text(24,141,'Moje porudžbine',28,TEXT,800)+rect(24,181,342,210)
        body+=text(44,218,'Porudžbina #R-001',18,TEXT,700)+text(44,246,'Primer · Nova TKL × 1',13,MUTED)
        body+=tag(44,270,'U obradi',102,True,'orders')+text(44,348,'12.990 RSD',23,ACCENT,700)
        body+=button(439,'Nazad na profil','profile',False)
    else:
        body=text(24,140,'Administracija',28,TEXT,800)+text(24,172,'PREGLED PRODAVNICE',10,ACCENT,700)
        body+=rect(24,200,164,95)+rect(202,200,164,95)+text(44,237,'Porudžbine',13,MUTED)+text(44,275,'01',30,TEXT,800)+text(222,237,'Proizvodi',13,MUTED)+text(222,275,'02',30,TEXT,800)
        body+=text(24,343,'Upravljanje',20,TEXT,700)
        for i,label in enumerate(['Proizvodi i kategorije','Korisnički nalozi','Porudžbine i statusi']):body+=button(369+i*75,label+'  →','admin',False)
        body+=lines(24,650,['Koncept administratorskog pregleda.','CRUD forme se razvijaju u narednoj fazi.'],12)
    return shell(key,title,body)

def main():
    (OUT/'screens').mkdir(parents=True,exist_ok=True)
    svgs={key:build(key) for key,_ in SCREENS}
    for key,svg in svgs.items():(OUT/'screens'/f'{key}.svg').write_text(svg,encoding='utf-8')
    links=''.join(f'<a href="#{key}" data-go="{key}"><span>{i:02}</span>{escape(title)}</a>' for i,(key,title) in enumerate(SCREENS,1))
    sections=''.join(f'<section class="screen" id="screen-{key}" aria-label="{escape(title)}" hidden>{svgs[key]}</section>' for key,title in SCREENS)
    html='''<!doctype html><html lang="sr-Latn"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Respawn · KT1 UI/UX prototip</title><style>
    *{box-sizing:border-box}body{margin:0;background:#0c0c10;color:#f4f1fa;font-family:Arial,sans-serif}a{color:inherit}header{padding:25px 4vw;border-bottom:1px solid #2b2736;display:flex;gap:24px;align-items:center;flex-wrap:wrap}header b{font-size:26px;letter-spacing:-1px}header small{color:#bda4ff;letter-spacing:2px;font-size:10px}header p{margin:0;color:#aaa5ba;font-size:12px}.layout{max-width:1260px;margin:35px auto;display:grid;grid-template-columns:240px 390px 250px;gap:50px;justify-content:center;padding:0 22px}.sidebar h1{font-size:16px;margin:0 0 19px}.sidebar nav{display:grid;gap:5px}.sidebar a{display:flex;gap:13px;padding:11px 12px;text-decoration:none;border-radius:9px;color:#aaa5ba;font-size:13px}.sidebar a.active{background:#30243f;color:#d6c5ff}.sidebar span{font-size:10px;opacity:.6}.device{border:1px solid #3b344a;border-radius:30px;overflow:hidden;box-shadow:0 26px 95px #0008;width:390px;height:844px;max-width:100%}.screen svg{display:block;width:100%;height:auto}.notes{padding-top:50px;color:#b7b3c5;font-size:13px;line-height:1.8}.notes h2{color:#f4f1fa;font-size:20px;line-height:1.3}.notes .pill{display:inline-block;background:#30243f;color:#d6c5ff;border-radius:30px;padding:4px 12px;font-size:10px;letter-spacing:1px}.notes ol{padding-left:18px}.notes strong{color:#f4f1fa}.notes .swatches{display:flex;gap:9px;margin-top:20px}.swatches i{width:32px;height:32px;border-radius:9px;border:1px solid #4d435e}svg a{cursor:pointer}svg a:hover{filter:brightness(1.13)}svg a:focus{outline:2px solid #bda4ff}footer{text-align:center;color:#827b92;font-size:11px;padding:10px 20px 32px}@media(max-width:1050px){.layout{grid-template-columns:190px 390px;gap:25px}.notes{display:none}}@media(max-width:650px){header{padding:18px 24px}header p{line-height:1.5}.layout{display:block;margin:20px auto;padding:0 12px}.sidebar{margin-bottom:18px}.sidebar h1{display:none}.sidebar nav{display:flex;overflow-x:auto;gap:6px}.sidebar a{white-space:nowrap}.sidebar span{display:none}.device{margin:auto;height:auto;border-radius:22px;width:390px}.screen{width:100%}}
    </style></head><body><header><b>respawn.</b><small>KT1 / UI CONCEPT</small><p>Planirani interfejs · izmišljeni primeri proizvoda · bez stvarne kupovine</p></header><main class="layout"><aside class="sidebar"><h1>Istraži prototip</h1><nav aria-label="Ekrani prototipa">'''+links+'''</nav></aside><div class="device">'''+sections+'''</div><aside class="notes"><span class="pill">MOBILE / ANDROID</span><h2>Oprema za tvoj<br>sledeći nivo.</h2><p>Jedna prodavnica gaming opreme, sa jasnim putanjama od istraživanja do poručivanja.</p><strong>Glavni tok kupovine</strong><ol><li>Katalog i detalji</li><li>Korpa i dostava</li><li>Stripe test ili pouzeće</li><li>Potvrda i porudžbine</li></ol><p>Prijava, kartica i porudžbina su vizuelna simulacija. U prototip se ne unose privatni podaci.</p><p>HTML i SVG su lokalni materijali. Figma objava i povezivanje zahtevaju pristup nalogu.</p><div class="swatches"><i style="background:#111116"></i><i style="background:#1d1d25"></i><i style="background:#bda4ff"></i><i style="background:#f4f1fa"></i></div></aside></main><footer>David Zejbeki · IT27/2024 · Respawn / Kontrolna tačka 1</footer><script>
    const screens=new Set('''+json.dumps([k for k,_ in SCREENS])+''');
    function show(){let key=location.hash.slice(1)||'home';if(!screens.has(key))key='home';document.querySelectorAll('.screen').forEach(s=>s.hidden=s.id!=='screen-'+key);document.querySelectorAll('.sidebar a').forEach(a=>a.classList.toggle('active',a.dataset.go===key));document.title='Respawn · '+key+' · UI koncept';}
    window.addEventListener('hashchange',show);show();
    </script></body></html>'''
    (OUT/'index.html').write_text(html,encoding='utf-8')
    (OUT/'tokens.json').write_text(json.dumps({'colors':{'background':BG,'surface':CARD,'accent':ACCENT,'text':TEXT,'muted':MUTED},'spacingUnit':8,'screen':{'width':390,'height':844},'screens':dict(SCREENS)},ensure_ascii=False,indent=2),encoding='utf-8')
    (OUT/'README.md').write_text('''# Respawn UI/UX koncept

Otvori index.html u pregledaču. Svaki ekran dostupan je iz bočnog menija; dugmad povezuju glavni tok i ishod neuspešnog plaćanja. Prototip ne izvršava kupovinu i ne prikuplja podatke.

SVG fajlovi u screens/ su uređivi vizuelni materijal za uvoz u Figma Design. Posle uvoza povezati ekrane u Prototype režimu: home -> detail -> cart -> delivery -> payment -> success -> orders; payment -> payment-error -> payment. Za prijavu koristiti login -> profile i register -> profile. Zasebno povezati favorites i admin prikaze. SVG import ne prenosi HTML interakcije.

Status: Figma dokument još nije objavljen. Za konačan Figma prototip potrebno je pristupiti nalogu, uvesti/organizovati ekrane, napraviti zajedničke komponente, povezati interakcije i proveriti prezentaciju. Ne predstavljati ove lokalne fajlove kao već završenu Figma objavu.
''',encoding='utf-8')
    print(f'Built {len(svgs)} SVG screens and local interactive prototype: {OUT}')

if __name__=='__main__':main()
