"""Render the KT1 Markdown source as a paginated PDF with embedded fonts."""
from pathlib import Path
from html import escape
import json
import re
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table, TableStyle,
    PageBreak, NextPageTemplate, Flowable, KeepTogether,
)
from reportlab.graphics import renderPDF
from svglib.svglib import svg2rlg

ROOT = Path(__file__).resolve().parents[2]
WIDTH, HEIGHT = A4
MARGIN = 48
CONTENT = WIDTH - 2*MARGIN
INK = colors.HexColor('#232230')
PURPLE = colors.HexColor('#6B469F')
MUTED = colors.HexColor('#676176')

def setup_fonts():
    font_dir = Path('C:/Windows/Fonts')
    for name, filename in [('Respawn','arial.ttf'),('Respawn-Bold','arialbd.ttf')]:
        path=font_dir/filename
        if not path.exists():raise RuntimeError(f'Font missing: {path}')
        pdfmetrics.registerFont(TTFont(name,str(path)))
    pdfmetrics.registerFontFamily('Respawn',normal='Respawn',bold='Respawn-Bold',italic='Respawn',boldItalic='Respawn-Bold')

def rich(value):
    value=escape(value)
    value = re.sub(r'\*\*(.+?)\*\*',r'<b>\1</b>',value)
    return re.sub(r'https?://[^\s<]+', lambda m: '<link href="'+m.group()+'" color="#6B469F">'+m.group()+'</link>', value)

class Cover(Flowable):
    width=CONTENT
    height=690
    def __init__(self,metadata):
        super().__init__();self.metadata=metadata;self.width=CONTENT;self.height=690
    def draw(self):
        c=self.canv
        c.setFillColor(colors.HexColor('#BDA4FF'));c.setFont('Respawn-Bold',10)
        c.drawString(0,652,'MOBILNE INFORMACIONE TEHNOLOGIJE')
        c.setFillColor(colors.white);c.setFont('Respawn-Bold',64);c.drawString(0,526,'respawn.')
        c.setFont('Respawn',22);c.drawString(0,482,'Mobilna prodavnica gaming opreme')
        c.setStrokeColor(colors.HexColor('#4A365F'));c.line(0,446,CONTENT,446)
        c.setFillColor(colors.HexColor('#BDA4FF'));c.setFont('Respawn-Bold',13)
        c.drawString(0,407,'KONTROLNA TAČKA 1')
        c.setFillColor(colors.HexColor('#D5CDDF'));c.setFont('Respawn',15)
        for i,line in enumerate(['Definisanje koncepta, tehnologija','i inicijalne strukture aplikacije']):c.drawString(0,374-i*24,line)
        # Vector motif: keyboard grid, consistent with the gaming domain.
        for row in range(3):
            for col in range(13):
                c.setFillColor(colors.HexColor(['#292333','#3A2E4C','#5C457B'][row]))
                c.roundRect(col*37,233-row*27,30,20,4,fill=1,stroke=0)
        c.setFillColor(colors.white);c.setFont('Respawn-Bold',17);c.drawString(0,118,self.metadata['student'])
        c.setFillColor(colors.HexColor('#B7B3C5'));c.setFont('Respawn',12);c.drawString(0,93,self.metadata['index'])
        c.setFillColor(colors.HexColor('#BDA4FF'));c.setFont('Respawn-Bold',9);c.drawString(0,33,'NACRT ZA PREGLED - FIGMA I ANDROID PROVERA NA ČEKANJU')

class DesignOverview(Flowable):
    width=CONTENT
    height=365
    def __init__(self):
        super().__init__();self.width=CONTENT;self.height=365
    def draw(self):
        c=self.canv
        choices=[('home','Katalog'),('detail','Detalji proizvoda'),('payment','Izbor plaćanja')]
        for i,(key,title) in enumerate(choices):
            drawing=svg2rlg(str(ROOT/'docs/design/screens'/f'{key}.svg'))
            scale=150/drawing.width
            c.saveState();c.translate(i*174,37);c.scale(scale,scale)
            renderPDF.draw(drawing,c,0,0);c.restoreState()
            c.setFont('Respawn-Bold',9);c.setFillColor(INK);c.drawString(i*174,17,title)

def cover_background(c,doc):
    c.setFillColor(colors.HexColor('#111116'));c.rect(0,0,WIDTH,HEIGHT,fill=1,stroke=0)

def body_background(c,doc):
    c.setFillColor(PURPLE);c.setFont('Respawn-Bold',9);c.drawString(MARGIN,HEIGHT-31,'RESPAWN / KT1')
    c.setFont('Respawn',8);c.setFillColor(MUTED);c.drawRightString(WIDTH-MARGIN,HEIGHT-31,'David Zejbeki · IT27/2024')
    c.setStrokeColor(colors.HexColor('#E4DDEB'));c.line(MARGIN,HEIGHT-40,WIDTH-MARGIN,HEIGHT-40)
    c.setFont('Respawn',8);c.drawString(MARGIN,27,'Koncept i inicijalna struktura aplikacije')
    c.drawRightString(WIDTH-MARGIN,27,str(doc.page))

def main():
    setup_fonts()
    metadata=json.loads((ROOT/'docs/project-metadata.json').read_text(encoding='utf-8'))
    source=(ROOT/'docs/KT1-IT27-2024.md').read_text(encoding='utf-8')
    validation=(ROOT/'docs/validation-summary.txt').read_text(encoding='utf-8') if (ROOT/'docs/validation-summary.txt').exists() else 'Provere su u toku. Dokument nije spreman za predaju.'
    replacements={
        '{{DOCUMENT_STATUS}}':'Nacrt za pregled; Figma objava i Android provera na čekanju.',
        '{{VALIDATION_SUMMARY}}':validation,
        '{{FIGMA_URL}}':metadata['figmaUrl'] or 'Nije objavljen - potreban je pristup Figma nalogu.',
        '{{GITHUB_URL}}':metadata['githubUrl'] or 'Nije objavljen - stvarni link treba dodati pre predaje.',
    }
    for key,value in replacements.items():source=source.replace(key,value)
    styles={
        'h1':ParagraphStyle('H1',fontName='Respawn-Bold',fontSize=19,leading=24,textColor=PURPLE,spaceAfter=17),
        'h2':ParagraphStyle('H2',fontName='Respawn-Bold',fontSize=12,leading=16,textColor=INK,spaceBefore=9,spaceAfter=8,keepWithNext=True),
        'body':ParagraphStyle('Body',fontName='Respawn',fontSize=10.2,leading=15.3,textColor=INK,spaceAfter=10),
        'bullet':ParagraphStyle('Bullet',fontName='Respawn',fontSize=10,leading=14.5,textColor=INK,leftIndent=12,firstLineIndent=-9,spaceAfter=6),
        'cell':ParagraphStyle('Cell',fontName='Respawn',fontSize=9,leading=12.5,textColor=INK),
        'th':ParagraphStyle('TH',fontName='Respawn-Bold',fontSize=9,leading=12.5,textColor=colors.white),
    }
    def para(text,kind='body'):return Paragraph(rich(text),styles[kind])
    def table(rows):
        count=len(rows[0])
        widths={2:[145,CONTENT-145],3:[160,160,CONTENT-320],5:[181,42,48,132,CONTENT-403]}.get(count,[CONTENT/count]*count)
        data=[[para(cell,'th' if i==0 else 'cell') for cell in row] for i,row in enumerate(rows)]
        result=Table(data,colWidths=widths,hAlign='LEFT',repeatRows=1)
        result.setStyle(TableStyle([
            ('BACKGROUND',(0,0),(-1,0),PURPLE),('VALIGN',(0,0),(-1,-1),'TOP'),
            ('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.HexColor('#F3F0F7'),colors.white]),
            ('LEFTPADDING',(0,0),(-1,-1),9),('RIGHTPADDING',(0,0),(-1,-1),9),
            ('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),8),
            ('LINEBELOW',(0,0),(-1,0),.5,PURPLE),
        ]));return result
    blocks=source.split('<!-- PAGE -->')[1:]
    story=[Cover(metadata),NextPageTemplate('body'),PageBreak()]
    for block_number,block in enumerate(blocks):
        source_lines=block.strip().splitlines();i=0
        while i<len(source_lines):
            line=source_lines[i].strip()
            if not line:i+=1;continue
            if line=='{{DESIGN_OVERVIEW}}':story.append(DesignOverview());i+=1;continue
            if line.startswith('|'):
                rows=[]
                while i<len(source_lines) and source_lines[i].strip().startswith('|'):
                    row=[c.strip() for c in source_lines[i].strip().strip('|').split('|')]
                    if not all(re.fullmatch(r'[:\- ]+',cell) for cell in row):rows.append(row)
                    i+=1
                story.extend([table(rows),Spacer(1,12)]);continue
            if line.startswith('# '):story.append(para(line[2:],'h1'))
            elif line.startswith('## '):story.append(para(line[3:],'h2'))
            elif line.startswith('- '):story.append(para('• '+line[2:],'bullet'))
            else:
                paragraph=[line]
                while i+1<len(source_lines) and source_lines[i+1].strip() and not source_lines[i+1].startswith(('#','|','- ','{{')):
                    i+=1;paragraph.append(source_lines[i].strip())
                story.append(para(' '.join(paragraph)))
            i+=1
        if block_number<len(blocks)-1:story.append(PageBreak())
    out=ROOT/'output/pdf'/metadata['documentName'];out.parent.mkdir(parents=True,exist_ok=True)
    doc=BaseDocTemplate(str(out),pagesize=A4,title='Respawn - Kontrolna tačka 1',author=metadata['student'],
                        subject='Mobilne informacione tehnologije - koncept i početni projekat')
    frame=Frame(MARGIN,48,CONTENT,HEIGHT-109,leftPadding=0,rightPadding=0,topPadding=0,bottomPadding=0)
    doc.addPageTemplates([PageTemplate(id='cover',frames=[frame],onPage=cover_background),
                          PageTemplate(id='body',frames=[frame],onPage=body_background)])
    doc.build(story)
    print(f'PDF created: {out}')

if __name__=='__main__':main()
