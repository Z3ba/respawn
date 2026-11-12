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
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.lib.utils import ImageReader
from reportlab.graphics import renderPDF
from svglib.svglib import svg2rlg

ROOT = Path(__file__).resolve().parents[2]
WIDTH, HEIGHT = A4
MARGIN = 72
CONTENT = WIDTH - 2*MARGIN
INK = colors.HexColor('#000000')
PURPLE = colors.HexColor('#000000')
MUTED = colors.HexColor('#000000')

def setup_fonts():
    font_dir = Path('C:/Windows/Fonts')
    for name, filename in [('Respawn','times.ttf'),('Respawn-Bold','timesbd.ttf')]:
        path=font_dir/filename
        if not path.exists():raise RuntimeError(f'Font missing: {path}')
        pdfmetrics.registerFont(TTFont(name,str(path)))
    pdfmetrics.registerFontFamily('Respawn',normal='Respawn',bold='Respawn-Bold',italic='Respawn',boldItalic='Respawn-Bold')

def rich(value):
    value=escape(value)
    value = re.sub(r'\*\*(.+?)\*\*',r'<b>\1</b>',value)
    return re.sub(r'https?://[^\s<]+', lambda m: '<link href="'+m.group()+'" color="#000000">'+m.group()+'</link>', value)

class Cover(Flowable):
    width=CONTENT
    height=690
    def __init__(self,metadata):
        super().__init__();self.metadata=metadata;self.width=CONTENT;self.height=690
    def draw(self):
        c=self.canv;c.setFillColor(colors.black)
        c.setFont('Respawn',14)
        for i,line in enumerate(['Fakultet tehničkih nauka, Novi Sad','Mobilne informacione tehnologije','Inženjerstvo informacionih sistema']):
            c.drawString(-28,690-i*19,line)
        c.setFont('Respawn-Bold',22)
        c.drawCentredString(CONTENT/2,466,'PROJEKTNA DOKUMENTACIJA')
        c.drawCentredString(CONTENT/2,434,'MOBILNE APLIKACIJE “RESPAWN”')
        c.setFont('Respawn',14)
        c.drawString(0,140,'Student:')
        c.drawString(0,114,self.metadata['student']+' '+self.metadata['index'])

class DesignOverview(Flowable):
    width=CONTENT
    height=320
    def __init__(self):
        super().__init__();self.width=CONTENT;self.height=320
    def draw(self):
        c=self.canv
        choices=[('home','Katalog'),('detail','Detalji proizvoda'),('cart','Korpa')]
        for i,(key,title) in enumerate(choices):
            drawing=svg2rlg(str(ROOT/'docs/design/screens'/f'{key}.svg'))
            scale=130/drawing.width
            c.saveState();c.translate(i*158,37);c.scale(scale,scale)
            renderPDF.draw(drawing,c,0,0);c.restoreState()
            c.setFont('Respawn-Bold',9);c.setFillColor(INK);c.drawString(i*158,17,title)

class Figure(Flowable):
    def __init__(self,kind):
        super().__init__();self.kind=kind;self.width=CONTENT
        self.height={'structure':310,'app':405,'payment':365}[kind]
    def draw(self):
        c=self.canv
        if self.kind=='structure':
            c.drawImage(ImageReader(str(ROOT/'docs/images/project-structure.png')),0,0,width=CONTENT,height=CONTENT*1050/1550)
        elif self.kind=='app':
            for i,key in enumerate(['initial-home','initial-profile']):
                c.drawImage(ImageReader(str(ROOT/'docs/images'/f'{key}.png')),30+i*220,10,width=175,height=175*844/390)
        else:
            drawing=svg2rlg(str(ROOT/'docs/design/screens/payment.svg'))
            scale=160/drawing.width;c.saveState();c.translate((CONTENT-160)/2,5);c.scale(scale,scale);renderPDF.draw(drawing,c,0,0);c.restoreState()

class AcademicDocument(BaseDocTemplate):
    def beforeDocument(self):
        self.seen=set()
    def afterFlowable(self,flowable):
        if isinstance(flowable,Paragraph) and flowable.style.name in ['H1','H2']:
            heading=flowable.getPlainText()
            if heading not in self.seen:
                self.seen.add(heading)
                self.notify('TOCEntry',(0 if flowable.style.name=='H1' else 1,heading,self.page-2))

def cover_background(c,doc):
    pass

def body_background(c,doc):
    c.setFillColor(colors.black);c.setFont('Respawn',12)
    c.drawRightString(WIDTH-MARGIN,27,str(doc.page-2))

def main():
    setup_fonts()
    metadata=json.loads((ROOT/'docs/project-metadata.json').read_text(encoding='utf-8'))
    source=(ROOT/'docs/KT1-IT27-2024.md').read_text(encoding='utf-8')
    validation=(ROOT/'docs/validation-summary.txt').read_text(encoding='utf-8') if (ROOT/'docs/validation-summary.txt').exists() else 'Provere su u toku. Dokument nije spreman za predaju.'
    replacements={
        '{{DOCUMENT_STATUS}}':'KT1 - inicijalni projekat; Android APK izgrađen, pokretanje na uređaju preostaje.' if metadata.get('androidBuildPassed') else 'Nacrt za pregled; Android build je u toku.',
        '{{VALIDATION_SUMMARY}}':validation,
        '{{FIGMA_URL}}':metadata['figmaUrl'] or 'Planiran za kasniju fazu; KT1 koristi lokalni prototip.',
        '{{GITHUB_URL}}':metadata['githubUrl'] or 'Nije objavljen - stvarni link treba dodati pre predaje.',
    }
    for key,value in replacements.items():source=source.replace(key,value)
    styles={
        'h1':ParagraphStyle('H1',fontName='Respawn-Bold',fontSize=20,leading=24,textColor=PURPLE,spaceAfter=17),
        'h2':ParagraphStyle('H2',fontName='Respawn-Bold',fontSize=14,leading=18,textColor=INK,spaceBefore=9,spaceAfter=8,keepWithNext=True),
        'body':ParagraphStyle('Body',fontName='Respawn',fontSize=12,leading=15,textColor=INK,spaceAfter=10,alignment=4),
        'bullet':ParagraphStyle('Bullet',fontName='Respawn',fontSize=12,leading=15,textColor=INK,leftIndent=12,firstLineIndent=-9,spaceAfter=6),
        'cell':ParagraphStyle('Cell',fontName='Respawn',fontSize=10,leading=12.5,textColor=INK),
        'th':ParagraphStyle('TH',fontName='Respawn-Bold',fontSize=10,leading=12.5,textColor=colors.black),
    }
    def para(text,kind='body'):return Paragraph(rich(text),styles[kind])
    def table(rows):
        count=len(rows[0])
        widths={2:[CONTENT*.30,CONTENT*.70],3:[CONTENT/3]*3,5:[CONTENT*.34,CONTENT*.10,CONTENT*.12,CONTENT*.24,CONTENT*.20]}.get(count,[CONTENT/count]*count)
        data=[[para(cell,'th' if i==0 else 'cell') for cell in row] for i,row in enumerate(rows)]
        result=Table(data,colWidths=widths,hAlign='LEFT',repeatRows=1)
        result.setStyle(TableStyle([
            ('BACKGROUND',(0,0),(-1,0),colors.white),('VALIGN',(0,0),(-1,-1),'TOP'),
            ('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,colors.white]),
            ('LEFTPADDING',(0,0),(-1,-1),9),('RIGHTPADDING',(0,0),(-1,-1),9),
            ('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),8),
            ('GRID',(0,0),(-1,-1),.5,colors.black),
        ]));return result
    blocks=source.split('<!-- PAGE -->')[1:]
    toc=TableOfContents()
    toc.levelStyles=[ParagraphStyle('TOC0',fontName='Respawn',fontSize=12,leading=18,spaceBefore=8),ParagraphStyle('TOC1',fontName='Respawn',fontSize=11,leading=15,leftIndent=16)]
    story=[Cover(metadata),NextPageTemplate('toc'),PageBreak(),Paragraph('Sadržaj',ParagraphStyle('ContentsTitle',fontName='Respawn-Bold',fontSize=20,leading=26,spaceAfter=20)),toc,NextPageTemplate('body'),PageBreak()]
    for block_number,block in enumerate(blocks):
        source_lines=block.strip().splitlines();i=0
        while i<len(source_lines):
            line=source_lines[i].strip()
            if not line:i+=1;continue
            if line in ['{{PROJECT_STRUCTURE}}','{{INITIAL_APP}}','{{PAYMENT_OVERVIEW}}']:
                story.append(Figure({'{{PROJECT_STRUCTURE}}':'structure','{{INITIAL_APP}}':'app','{{PAYMENT_OVERVIEW}}':'payment'}[line]));i+=1;continue
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
    out=ROOT/'output/kt1'/metadata['documentName'];out.parent.mkdir(parents=True,exist_ok=True)
    doc=AcademicDocument(str(out),pagesize=A4,title='Respawn - Kontrolna tačka 1',author=metadata['student'],
                        subject='Mobilne informacione tehnologije - koncept i početni projekat')
    frame=Frame(MARGIN,48,CONTENT,HEIGHT-109,leftPadding=0,rightPadding=0,topPadding=0,bottomPadding=0)
    doc.addPageTemplates([PageTemplate(id='cover',frames=[frame],onPage=cover_background),
                          PageTemplate(id='toc',frames=[frame],onPage=cover_background),
                          PageTemplate(id='body',frames=[frame],onPage=body_background)])
    doc.multiBuild(story)
    print(f'PDF created: {out}')

if __name__=='__main__':main()
