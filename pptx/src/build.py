"""Builds the UNAIR PowerPoint template (.potx) and sample deck (.pptx).

Layouts are written as raw OOXML so placeholders, inheritance and the master
sidebar behave like a hand-made PowerPoint template; python-pptx handles the
package bookkeeping and the sample slides. Run assets.js first.
"""
import re
import sys
from pathlib import Path

from pptx import Presentation
from pptx.opc.constants import CONTENT_TYPE as CT, RELATIONSHIP_TYPE as RT
from pptx.oxml import parse_xml
from pptx.oxml.ns import qn
from pptx.parts.slide import SlideLayoutPart
from pptx.util import Inches, Pt

HERE = Path(__file__).parent
A = HERE / "assets"
OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE.parent
OUT.mkdir(parents=True, exist_ok=True)

NS = ('xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
      'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
      'xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"')

# ── Brand ──────────────────────────────────────────────────────────────
BLUE, YELLOW, RED = "14497F", "FFCB05", "E6282B"
WHITE, TEXT, GREY_LIGHT, GREY_DARK = "FFFFFF", "333333", "F0F0F0", "666666"
FONT, FONT_LIGHT, FONT_SEMI = "Segoe UI", "Segoe UI Light", "Segoe UI Semibold"

# ── Geometry (inches, 16:9) ────────────────────────────────────────────
W, H = 13.333, 7.5
SB_W = 0.75                 # brand sidebar
SB_X = W - SB_W
ML = 0.6                    # left margin
CR = SB_X - 0.45            # content right edge (gap before sidebar)
CW = CR - ML
LOGO_RATIO = 8855 / 3334
STRIP_X, STRIP_W = W * 0.814, 1.26   # batik strip on title / closing
COVER_X = W * 0.08

E = lambda v: int(round(v * 914400))


# ── XML helpers ────────────────────────────────────────────────────────
def solid(c):
    return f'<a:solidFill><a:srgbClr val="{c}"/></a:solidFill>'


def rpr(tag="a:rPr", sz=None, b=None, i=None, color=None, font=None, cap=None, spc=None):
    at = ['lang="en-US"']
    if sz: at.append(f'sz="{int(sz * 100)}"')
    if b is not None: at.append(f'b="{int(bool(b))}"')
    if i is not None: at.append(f'i="{int(bool(i))}"')
    if cap: at.append(f'cap="{cap}"')
    if spc is not None: at.append(f'spc="{int(spc * 100)}"')
    inner = (solid(color) if color else "") + (f'<a:latin typeface="{font}"/>' if font else "")
    return f'<{tag} {" ".join(at)}>{inner}</{tag}>'


def ppr(tag="a:pPr", algn=None, lnspc=None, bullets=False, inner=""):
    at = [] if bullets else ['marL="0"', 'indent="0"']
    if algn: at.append(f'algn="{algn}"')
    kids = f'<a:lnSpc><a:spcPct val="{int(lnspc * 1000)}"/></a:lnSpc>' if lnspc else ""
    if not bullets: kids += "<a:buNone/>"
    return f'<{tag} {" ".join(at)}>{kids}{inner}</{tag}>'


def body_pr(anchor="t", ins=0.0, autofit=False, rot=None, wrap=True):
    i = E(ins)
    at = f'wrap="{"square" if wrap else "none"}" lIns="{i}" tIns="{i}" rIns="{i}" bIns="{i}" anchor="{anchor}" rtlCol="0"'
    return f'<a:bodyPr {at}>{"<a:normAutofit/>" if autofit else "<a:noAutofit/>"}</a:bodyPr>'


def xfrm(x, y, w, h, rot=None):
    r = f' rot="{rot}"' if rot else ""
    return f'<a:xfrm{r}><a:off x="{E(x)}" y="{E(y)}"/><a:ext cx="{E(w)}" cy="{E(h)}"/></a:xfrm>'


class Tree:
    """Collects shapes for one spTree and hands out unique shape ids."""

    def __init__(self):
        self.n, self.parts = 1, []

    def _id(self):
        self.n += 1
        return self.n

    def xml(self):
        return ('<p:spTree><p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>'
                '<p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/>'
                '<a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>' + "".join(self.parts) + "</p:spTree>")

    def rect(self, name, x, y, w, h, fill, geom="rect", adj=None):
        av = f'<a:gd name="adj" fmla="val {adj}"/>' if adj is not None else ""
        self.parts.append(
            f'<p:sp><p:nvSpPr><p:cNvPr id="{self._id()}" name="{name}"/><p:cNvSpPr/><p:nvPr userDrawn="1"/></p:nvSpPr>'
            f'<p:spPr>{xfrm(x, y, w, h)}<a:prstGeom prst="{geom}"><a:avLst>{av}</a:avLst></a:prstGeom>'
            f'{solid(fill)}<a:ln><a:noFill/></a:ln></p:spPr></p:sp>')

    def line(self, name, x, y, w, h, color, pt):
        self.parts.append(
            f'<p:cxnSp><p:nvCxnSpPr><p:cNvPr id="{self._id()}" name="{name}"/><p:cNvCxnSpPr/><p:nvPr userDrawn="1"/></p:nvCxnSpPr>'
            f'<p:spPr>{xfrm(x, y, w, h)}<a:prstGeom prst="line"><a:avLst/></a:prstGeom>'
            f'<a:ln w="{int(pt * 12700)}">{solid(color)}</a:ln></p:spPr></p:cxnSp>')

    def text(self, name, x, y, w, h, paras, anchor="t", rot=None, wrap=True):
        self.parts.append(
            f'<p:sp><p:nvSpPr><p:cNvPr id="{self._id()}" name="{name}"/><p:cNvSpPr txBox="1"/><p:nvPr userDrawn="1"/></p:nvSpPr>'
            f'<p:spPr>{xfrm(x, y, w, h, rot)}<a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:noFill/></p:spPr>'
            f'<p:txBody>{body_pr(anchor, wrap=wrap)}<a:lstStyle/>{paras}</p:txBody></p:sp>')

    def pic(self, name, rid, x, y, w, h, descr=None):
        d = f' descr="{descr}"' if descr else ""
        deco = "" if descr else ('<a:extLst><a:ext uri="{C183D7F6-B498-43B3-948B-1728B52AA6E4}">'
                                 '<adec:decorative xmlns:adec="http://schemas.microsoft.com/office/drawing/2017/decorative" val="1"/>'
                                 '</a:ext></a:extLst>')
        self.parts.append(
            f'<p:pic><p:nvPicPr><p:cNvPr id="{self._id()}" name="{name}"{d}>{deco}</p:cNvPr>'
            f'<p:cNvPicPr><a:picLocks noChangeAspect="1"/></p:cNvPicPr><p:nvPr userDrawn="1"/></p:nvPicPr>'
            f'<p:blipFill><a:blip r:embed="{rid}"/><a:stretch><a:fillRect/></a:stretch></p:blipFill>'
            f'<p:spPr>{xfrm(x, y, w, h)}<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></p:spPr></p:pic>')

    def ph(self, name, kind, idx, x, y, w, h, prompt, anchor="t", autofit=False, rot=None,
           algn=None, lnspc=None, bullets=False, **run):
        """kind: 'title', 'ctrTitle', 'subTitle', 'body', 'pic', or None (content object)."""
        t = f' type="{kind}"' if kind else ""
        i = f' idx="{idx}"' if idx is not None else ""
        lvl1 = ppr("a:lvl1pPr", algn, lnspc, bullets, rpr("a:defRPr", **run))
        self.parts.append(
            f'<p:sp><p:nvSpPr><p:cNvPr id="{self._id()}" name="{name}"/><p:cNvSpPr><a:spLocks noGrp="1"/></p:cNvSpPr>'
            f'<p:nvPr><p:ph{t}{i} hasCustomPrompt="1"/></p:nvPr></p:nvSpPr>'
            f'<p:spPr>{xfrm(x, y, w, h, rot)}<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></p:spPr>'
            f'<p:txBody>{body_pr(anchor, autofit=autofit)}<a:lstStyle>{lvl1}</a:lstStyle>'
            f'<a:p><a:r><a:rPr lang="en-US"/><a:t>{prompt}</a:t></a:r></a:p></p:txBody></p:sp>')


def para(text, algn=None, **run):
    p = f'<a:pPr algn="{algn}"/>' if algn else ""
    return f"<a:p>{p}<a:r>{rpr(**run)}<a:t>{text}</a:t></a:r></a:p>"


# ── Theme ──────────────────────────────────────────────────────────────
CLR_SCHEME = f"""<a:clrScheme name="Universitas Airlangga">
<a:dk1><a:srgbClr val="{TEXT}"/></a:dk1><a:lt1><a:srgbClr val="{WHITE}"/></a:lt1>
<a:dk2><a:srgbClr val="{BLUE}"/></a:dk2><a:lt2><a:srgbClr val="{GREY_LIGHT}"/></a:lt2>
<a:accent1><a:srgbClr val="{BLUE}"/></a:accent1><a:accent2><a:srgbClr val="{YELLOW}"/></a:accent2>
<a:accent3><a:srgbClr val="{RED}"/></a:accent3><a:accent4><a:srgbClr val="4F86C0"/></a:accent4>
<a:accent5><a:srgbClr val="{GREY_DARK}"/></a:accent5><a:accent6><a:srgbClr val="0B2E52"/></a:accent6>
<a:hlink><a:srgbClr val="{BLUE}"/></a:hlink><a:folHlink><a:srgbClr val="0B2E52"/></a:folHlink>
</a:clrScheme>"""


def fix_theme(prs):
    part = prs.slide_master.part.part_related_by(RT.THEME)
    xml = part.blob.decode("utf-8")
    xml = re.sub(r"<a:clrScheme .*?</a:clrScheme>", CLR_SCHEME, xml, flags=re.S)
    xml = re.sub(r'(<a:(?:major|minor)Font><a:latin typeface=")[^"]*"', rf'\g<1>{FONT}"', xml)
    xml = re.sub(r'<a:theme ([^>]*)name="[^"]*"', r'<a:theme \1name="Universitas Airlangga"', xml)
    xml = re.sub(r'<a:fontScheme name="[^"]*"', '<a:fontScheme name="Universitas Airlangga"', xml)
    part._blob = xml.encode("utf-8")


# ── Master ─────────────────────────────────────────────────────────────
def lvl(n, marL, indent, char, sz, color=TEXT):
    return (f'<a:lvl{n}pPr marL="{E(marL)}" indent="{-E(indent)}" algn="l" defTabSz="914400" rtl="0" eaLnBrk="1" latinLnBrk="0" hangingPunct="1">'
            f'<a:lnSpc><a:spcPct val="110000"/></a:lnSpc><a:spcBef><a:spcPts val="{600 if n == 1 else 300}"/></a:spcBef>'
            f'<a:buClr><a:srgbClr val="{BLUE}"/></a:buClr><a:buFont typeface="Arial"/><a:buChar char="{char}"/>'
            f'<a:defRPr sz="{sz * 100}" kern="1200">{solid(color)}<a:latin typeface="+mn-lt"/><a:ea typeface="+mn-ea"/><a:cs typeface="+mn-cs"/></a:defRPr></a:lvl{n}pPr>')


TITLE_STYLE = (f'<p:titleStyle {NS}><a:lvl1pPr algn="l" defTabSz="914400" rtl="0" eaLnBrk="1" latinLnBrk="0" hangingPunct="1">'
               f'<a:lnSpc><a:spcPct val="95000"/></a:lnSpc><a:spcBef><a:spcPct val="0"/></a:spcBef><a:buNone/>'
               f'<a:defRPr sz="3000" b="1" kern="1200">{solid(BLUE)}<a:latin typeface="+mj-lt"/><a:ea typeface="+mj-ea"/><a:cs typeface="+mj-cs"/></a:defRPr>'
               f'</a:lvl1pPr></p:titleStyle>')
BODY_STYLE = (f'<p:bodyStyle {NS}>' + lvl(1, 0.3, 0.3, "•", 18) + lvl(2, 0.65, 0.3, "–", 16) + lvl(3, 1.0, 0.25, "•", 14)
              + "".join(lvl(n, 1.0 + 0.35 * (n - 3), 0.25, "–" if n % 2 == 0 else "•", 14) for n in range(4, 10))
              + "</p:bodyStyle>")


def add_title_rule_logo(t, logo_rid):
    """Standard content-slide header: title, yellow rule, logo top-right."""
    lw = 2.0
    t.pic("Logo", logo_rid, CR - lw + 0.1, 0.28, lw, lw / LOGO_RATIO, descr="Universitas Airlangga logo")
    t.ph("Title", "title", None, ML, 0.3, 9.3, 0.92, "Click to edit title", anchor="b")
    t.line("Title rule", ML, 1.3, CW, 0, YELLOW, 2.25)


def build_master(prs, running_title):
    m = prs.slide_master
    el = m.part._element
    img = lambda p: m.part.get_or_add_image_part(str(p))[1]

    t = Tree()
    t.ph("Title Placeholder", "title", None, ML, 0.3, 9.3, 0.92, "Click to edit Master title style", anchor="b")
    t.ph("Text Placeholder", "body", 1, ML, 1.6, CW, 5.35, "Click to edit Master text styles", bullets=True)
    # Brand sidebar (right edge): key graphic, running title, slide number block.
    t.rect("Sidebar", SB_X, 0, SB_W, H, BLUE)
    t.pic("Sidebar key graphic", img(A / "keygraphic_white.png"), SB_X + (SB_W - 0.3) / 2, 0.45, 0.3, 0.3)
    label_len, label_bottom = 4.6, H - 0.9 - 0.4
    cx, cy = SB_X + SB_W / 2, label_bottom - label_len / 2
    t.text("Sidebar running title", cx - label_len / 2, cy - 0.15, label_len, 0.3,
           para(running_title, sz=8.5, b=True, color=WHITE, cap="all", spc=1.9), anchor="ctr", rot=16200000)
    t.rect("Sidebar number block", SB_X, H - 0.9, SB_W, 0.9, YELLOW)
    t.parts.append(
        f'<p:sp><p:nvSpPr><p:cNvPr id="{t._id()}" name="Sidebar slide number"/><p:cNvSpPr txBox="1"/><p:nvPr userDrawn="1"/></p:nvSpPr>'
        f'<p:spPr>{xfrm(SB_X, H - 0.9, SB_W, 0.9)}<a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:noFill/></p:spPr>'
        f'<p:txBody><a:bodyPr wrap="none" lIns="0" tIns="{E(0.22)}" rIns="0" bIns="0" anchor="t"><a:noAutofit/></a:bodyPr><a:lstStyle/>'
        f'<a:p><a:pPr algn="ctr"/><a:fld id="{{B6F15528-21DE-4FAA-801E-634DDDAF4B2B}}" type="slidenum">'
        f'{rpr(sz=12, b=True, color=BLUE)}<a:t>‹#›</a:t></a:fld></a:p></p:txBody></p:sp>')

    old = el.find(qn("p:cSld")).find(qn("p:spTree"))
    new = parse_xml(f'<p:wrap {NS}>{t.xml()}</p:wrap>')[0]
    old.getparent().replace(old, new)
    bg = el.find(qn("p:cSld")).find(qn("p:bg"))
    if bg is not None:
        bg.getparent().remove(bg)
    el.find(qn("p:cSld")).insert(0, parse_xml(
        f'<p:bg {NS}><p:bgPr>{solid(WHITE)}<a:effectLst/></p:bgPr></p:bg>'))

    styles = el.find(qn("p:txStyles"))
    for tag, xml in (("p:titleStyle", TITLE_STYLE), ("p:bodyStyle", BODY_STYLE)):
        styles.replace(styles.find(qn(tag)), parse_xml(xml))
    for hf in el.findall(qn("p:hf")):
        el.remove(hf)


# ── Layouts ────────────────────────────────────────────────────────────
_layout_id = [2147483700]


def add_layout(prs, name, build, sidebar=True, bg=None):
    master = prs.slide_master
    pkg = prs.part.package
    partname = pkg.next_partname("/ppt/slideLayouts/slideLayout%d.xml")
    stub = f'<p:sldLayout {NS}><p:cSld><p:spTree/></p:cSld></p:sldLayout>'.encode()
    part = SlideLayoutPart.load(partname, CT.PML_SLIDE_LAYOUT, pkg, stub)
    part.relate_to(master.part, RT.SLIDE_MASTER)
    rid = master.part.relate_to(part, RT.SLIDE_LAYOUT)
    _layout_id[0] += 1
    master._element.find(qn("p:sldLayoutIdLst")).append(
        parse_xml(f'<p:sldLayoutId {NS} id="{_layout_id[0]}" r:id="{rid}"/>'))

    t = Tree()
    build(t, lambda p: part.get_or_add_image_part(str(p))[1])
    bg_xml = f'<p:bg><p:bgPr>{solid(bg)}<a:effectLst/></p:bgPr></p:bg>' if bg else ""
    show = "" if sidebar else ' showMasterSp="0"'
    part._element = parse_xml(
        f'<p:sldLayout {NS} preserve="1" userDrawn="1"{show}><p:cSld name="{name}">{bg_xml}{t.xml()}</p:cSld>'
        f'<p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr></p:sldLayout>')


def L_title(t, img):
    lw = 2.9
    t.pic("Logo", img(A / "logo.png"), COVER_X - 0.14, 0.55, lw, lw / LOGO_RATIO, descr="Universitas Airlangga logo")
    t.pic("Batik strip", img(A / "strip_blue.png"), STRIP_X, 0, STRIP_W, H)
    w = STRIP_X - COVER_X - 0.8
    t.ph("Title", "ctrTitle", None, COVER_X, 2.3, w, 2.25, "Presentation title", anchor="b", sz=44, lnspc=95)
    t.ph("Subtitle", "subTitle", 1, COVER_X, 4.62, w, 0.65, "Subtitle", sz=22, color=BLUE, b=False)
    t.ph("Author", "body", 13, COVER_X, 5.42, w, 0.36, "Author name", sz=13, b=True, color=BLUE)
    t.ph("Affiliation", "body", 14, COVER_X, 5.76, w, 0.36, "Department, Universitas Airlangga", sz=13, color=BLUE)
    t.ph("Date", "body", 15, COVER_X, 6.62, 5, 0.3, "Date", sz=10.5, color=BLUE)


def L_section(t, img):
    lw = 1.95
    t.pic("Logo (white)", img(A / "logo_white.png"), 0.95 - 0.1, 2.15, lw, lw / LOGO_RATIO, descr="Universitas Airlangga logo")
    t.ph("Number", "body", 16, 7.8, 3.9, 5.0, 3.3, "01", anchor="b", algn="r", sz=180, b=True, color="356291", lnspc=80)
    t.ph("Title", "title", None, 0.95, 3.02, 10.2, 0.85, "Section title", autofit=True, sz=40, color=WHITE)
    t.ph("Subtitle", "body", 1, 0.95, 3.95, 9.5, 0.9, "Optional section description", sz=20, color=WHITE)


def L_content(t, img):
    add_title_rule_logo(t, img(A / "logo.png"))
    t.ph("Content", None, 1, ML, 1.6, CW, 5.35, "Click to add text", bullets=True, autofit=True)


def L_two(t, img):
    add_title_rule_logo(t, img(A / "logo.png"))
    cw = (CW - 0.5) / 2
    t.ph("Left content", None, 1, ML, 1.6, cw, 5.35, "Click to add text", bullets=True, autofit=True)
    t.ph("Right content", None, 2, ML + cw + 0.5, 1.6, cw, 5.35, "Click to add text", bullets=True, autofit=True)


def L_title_only(t, img):
    add_title_rule_logo(t, img(A / "logo.png"))


def L_agenda(t, img):
    t.line("Agenda rule", W * 0.09, 0.75, 0, 6.0, YELLOW, 2.25)
    t.ph("Title", "title", None, W * 0.045 - 1.6, H / 2 - 0.2, 3.2, 0.4, "Agenda", anchor="ctr", algn="ctr",
         rot=16200000, sz=14, cap="all", spc=4.5)
    x0, x1, y0, rh = W * 0.14, W * 0.92, 0.9, 1.14
    for i in range(5):
        y = y0 + i * rh
        t.text(f"Number {i + 1}", x0, y, 1.3, rh, para(f"{i + 1:02d}", sz=40, b=True, color=BLUE), anchor="ctr")
        t.ph(f"Item {i + 1}", "body", 20 + i, x0 + 1.35, y, x1 - x0 - 1.8, rh, f"Agenda item {i + 1}",
             anchor="ctr", sz=20, font=FONT_SEMI, color=TEXT)
        t.rect(f"Dot {i + 1}", x1 - 0.09, y + rh / 2 - 0.045, 0.09, 0.09, YELLOW, geom="ellipse")
        if i < 4:
            t.line(f"Separator {i + 1}", x0, y + rh, x1 - x0, 0, "E8E8E8", 0.75)


def L_text_image(t, img):
    x_img = SB_X * 0.55
    t.ph("Picture", "pic", 10, x_img, 0, SB_X - x_img, H, "Insert picture", anchor="ctr", algn="ctr", sz=14, color=GREY_DARK)
    t.ph("Title", "title", None, ML, 0.5, x_img - ML - 0.5, 1.05, "Click to edit title", anchor="b")
    t.ph("Text", "body", 1, ML, 1.85, x_img - ML - 0.5, 5.0, "Click to add text", bullets=True, autofit=True, sz=17)


def L_image_text(t, img):
    x_txt = 6.85
    t.ph("Picture", "pic", 10, 0, 0, 6.3, H, "Insert picture", anchor="ctr", algn="ctr", sz=14, color=GREY_DARK)
    t.ph("Title", "title", None, x_txt, 0.9, CR - x_txt, 1.0, "Click to edit title", anchor="b", sz=26)
    t.ph("Text", "body", 1, x_txt, 2.05, CR - x_txt, 4.7, "Click to add text", autofit=True, sz=17, lnspc=125)


def L_text_box(t, img):
    add_title_rule_logo(t, img(A / "logo.png"))
    t.ph("Lead", "body", 10, ML, 1.62, CW, 1.1, "Introductory sentence", sz=22, font=FONT_LIGHT, lnspc=115)
    t.rect("Box accent", ML, 2.95, CW, 3.85, YELLOW, geom="roundRect", adj=2500)
    t.rect("Box", ML + 0.08, 2.95, CW - 0.08, 3.85, GREY_LIGHT, geom="roundRect", adj=2500)
    t.ph("Box text", "body", 11, ML + 0.55, 3.35, CW - 1.1, 3.05, "Supporting detail", autofit=True, sz=17, lnspc=130)


def L_three(t, img):
    add_title_rule_logo(t, img(A / "logo.png"))
    t.ph("Lead", "body", 10, ML, 1.6, 8.2, 0.7, "Short introduction", sz=18, font=FONT_LIGHT)
    py, ph_ = 2.5, 4.4
    t.rect("Panel", ML, py, CW, ph_, GREY_LIGHT, geom="roundRect", adj=2500)
    pad, gap = 0.45, 0.45
    cw = (CW - 2 * pad - 2 * gap) / 3
    for i in range(3):
        x = ML + pad + i * (cw + gap)
        t.ph(f"Icon {i + 1}", "pic", 30 + i, x + (cw - 0.8) / 2, py + 0.45, 0.8, 0.8, "Icon", anchor="ctr", algn="ctr", sz=9, color=GREY_DARK)
        t.ph(f"Heading {i + 1}", "body", 40 + i, x, py + 1.4, cw, 0.5, "Heading", anchor="ctr", algn="ctr", sz=17, b=True, color=BLUE)
        t.ph(f"Text {i + 1}", "body", 50 + i, x, py + 1.95, cw, 2.1, "Short description", algn="ctr", autofit=True, sz=14, lnspc=120)


def L_overview(t, img):
    t.rect("Header band", 0, 0, SB_X, 1.15, BLUE)
    t.ph("Title", "title", None, ML, 0, SB_X - 2 * ML, 1.15, "Click to edit title", anchor="ctr", algn="ctr", sz=26, color=WHITE)
    gx, gap = ML, 0.4
    iw = (SB_X - 2 * ML - 2 * gap) / 3
    for i in range(3):
        x = gx + i * (iw + gap)
        t.ph(f"Picture {i + 1}", "pic", 10 + i, x, 1.95, iw, 2.75, "Insert picture", anchor="ctr", algn="ctr", sz=12, color=GREY_DARK)
        t.ph(f"Caption {i + 1}", "body", 20 + i, x, 4.9, iw, 0.9, "Caption", algn="ctr", sz=14)


def _quote(t, dark):
    bx = W * 0.18
    if dark:
        t.text("Quote mark", bx - 0.12, 0.95, 1.5, 1.6, para("“", sz=72, color="7D93AC", font=FONT), anchor="t")
    else:
        t.text("Quote mark", 0.35, -0.2, 4.5, 5.5, para("“", sz=280, color="EEF2F6", font=FONT), anchor="t")
    t.rect("Quote rule", bx, 2.05, 0.07, 3.4, YELLOW)
    t.ph("Quote", "body", 10, bx + 0.55, 2.05, W * 0.64 - 0.55, 2.65, "Quoted text", anchor="ctr", autofit=True,
         sz=26, i=True, lnspc=130, color=WHITE if dark else BLUE, font=FONT_LIGHT if dark else None)
    t.ph("Author", "body", 11, bx + 0.55, 4.85, W * 0.64 - 0.55, 0.6, "— Name, source (year)", anchor="b",
         sz=12, b=True, cap="all", spc=1.0, color="D9E2EC" if dark else GREY_DARK)


def L_quote(t, img):
    _quote(t, dark=False)


def L_quote_dark(t, img):
    t.pic("Scrim", img(A / "scrim.png"), 0, 0, W, H)
    _quote(t, dark=True)


def L_closing(t, img):
    lw = 2.9
    t.pic("Logo (white)", img(A / "logo_white.png"), COVER_X - 0.14, 0.55, lw, lw / LOGO_RATIO, descr="Universitas Airlangga logo")
    t.pic("Batik strip", img(A / "strip_yellow.png"), STRIP_X, 0, STRIP_W, H)
    w = STRIP_X - COVER_X - 0.8
    t.ph("Title", "title", None, COVER_X, 1.95, w, 1.7, "Thank you!", anchor="b", sz=44, color=WHITE)
    t.ph("Subtitle", "body", 1, COVER_X, 3.72, w, 0.62, "Questions?", sz=22, color=WHITE)
    t.ph("Contact", "body", 12, COVER_X, 4.55, w, 1.7, "Contact details", sz=13, color=WHITE, lnspc=130)
    t.ph("Note", "body", 13, COVER_X, 6.62, w, 0.3, "Small print, e.g. a URL", sz=10.5, color=WHITE)


LAYOUTS = [
    ("Title", L_title, False, WHITE),
    ("Section Divider", L_section, False, BLUE),
    ("Content", L_content, True, None),
    ("Two Content", L_two, True, None),
    ("Title Only", L_title_only, True, None),
    ("Agenda", L_agenda, False, WHITE),
    ("Text + Image", L_text_image, True, None),
    ("Image + Text", L_image_text, True, None),
    ("Text + Shaded Box", L_text_box, True, None),
    ("Three Columns", L_three, True, None),
    ("Overview Grid", L_overview, True, None),
    ("Quote", L_quote, False, WHITE),
    ("Quote (Dark / Photo)", L_quote_dark, False, BLUE),
    ("Closing", L_closing, False, BLUE),
]


def new_presentation(running_title):
    prs = Presentation()
    prs.slide_width, prs.slide_height = Inches(W), Inches(H)
    m = prs.slide_master
    for layout in list(m.slide_layouts):
        m.slide_layouts.remove(layout)
    fix_theme(prs)
    build_master(prs, running_title)
    for name, fn, sidebar, bg in LAYOUTS:
        add_layout(prs, name, fn, sidebar, bg)
    cp = prs.core_properties
    cp.title, cp.author = "Universitas Airlangga", "Rizqy Amelia Zein"
    return prs


# ── Sample deck ────────────────────────────────────────────────────────
def layout(prs, name):
    return next(l for l in prs.slide_layouts if l.name == name)


def fill(ph, items):
    """items: list of str | (str, level) | list-of-runs [(text, {'b':True})]."""
    tf = ph.text_frame
    for n, item in enumerate(items):
        p = tf.paragraphs[0] if n == 0 else tf.add_paragraph()
        level, runs = 0, item
        if isinstance(item, tuple) and isinstance(item[1], int):
            runs, level = item
        if isinstance(runs, str):
            runs = [(runs, {})]
        p.level = level
        for text, fmt in runs:
            r = p.add_run()
            r.text = text
            if fmt.get("b"): r.font.bold = True
            if fmt.get("color"): r.font.color.rgb = __import__("pptx").dml.color.RGBColor.from_string(fmt["color"])
            if fmt.get("buNone"):
                pPr = p._p.get_or_add_pPr()
                pPr.set("marL", "0"); pPr.set("indent", "0")
                pPr.insert(0, parse_xml(f'<a:buNone {NS}/>'))


def slide(prs, name, **by_idx):
    s = prs.slides.add_slide(layout(prs, name))
    phs = {p.placeholder_format.idx: p for p in s.placeholders}
    for key, val in by_idx.items():
        idx = 0 if key == "title" else int(key[1:])
        ph = phs[idx]
        if isinstance(val, Path):
            ph.insert_picture(str(val))
        else:
            fill(ph, val if isinstance(val, list) else [val])
    return s


def sample(prs):
    slide(prs, "Title", title="Universitas Airlangga Theme", p1="A Professional PowerPoint Template",
          p13="Rizqy Amelia Zein", p14="Department of Psychology, Universitas Airlangga", p15="13 September 2026")
    slide(prs, "Agenda", title="Agenda", p20="Background & Motivation", p21="Research Methodology",
          p22="Findings & Discussion", p23="Conclusions", p24="Q&A")
    slide(prs, "Content", title="Introduction", p1=[
        "This is a sample presentation using the Universitas Airlangga template.",
        "Clean, professional design", "Official UNAIR branding", "Easy to customize",
        ("Pick layouts from Home → Layout", 1)])
    bold_none = lambda t: [(t, {"b": True, "color": BLUE, "buNone": True})]
    slide(prs, "Two Content", title="Key Features",
          p1=[bold_none("Design Elements"), "UNAIR Blue primary color", "Yellow accent highlights", "Clean typography"],
          p2=[bold_none("Smart Features"), "Brand sidebar with slide number", "White logo on blue", "Section dividers"])
    slide(prs, "Section Divider", title="Field Study Results", p1="Opt-in, full-slide layouts for richer presentations", p16="01")

    s = slide(prs, "Title Only", title="Brand Colors")
    sw = [(BLUE, "UNAIR Blue", "#14497F · primary"), (YELLOW, "UNAIR Yellow", "#FFCB05 · accent"),
          (RED, "Red", "#E6282B · alerts"), (GREY_LIGHT, "Light Grey", "#F0F0F0 · panels")]
    cw = (CW - 3 * 0.4) / 4
    for i, (c, name, note) in enumerate(sw):
        x = ML + i * (cw + 0.4)
        shp = s.shapes.add_shape(5, Inches(x), Inches(1.9), Inches(cw), Inches(3.0))  # rounded rectangle
        shp.adjustments[0] = 0.04
        shp.fill.solid(); shp.fill.fore_color.rgb = __import__("pptx").dml.color.RGBColor.from_string(c)
        shp.line.fill.background(); shp.shadow.inherit = False
        tb = s.shapes.add_textbox(Inches(x), Inches(5.1), Inches(cw), Inches(1.0))
        tb.text_frame.margin_left = tb.text_frame.margin_right = 0
        fill(tb, [[(name, {"b": True, "color": BLUE})], [(note, {"color": GREY_DARK})]])
        tb.text_frame.paragraphs[0].runs[0].font.size = Pt(18)
        tb.text_frame.paragraphs[1].runs[0].font.size = Pt(14)

    s = slide(prs, "Title Only", title="Tables")
    rows = [("Variable", "Mean", "SD", "N"), ("Age", "25.3", "4.2", "150"), ("Score", "78.5", "12.1", "150"), ("Hours", "5.7", "1.8", "150")]
    tbl = s.shapes.add_table(4, 4, Inches(ML), Inches(1.8), Inches(CW), Inches(2.6)).table
    for r, row in enumerate(rows):
        for c, v in enumerate(row):
            cell = tbl.cell(r, c)
            cell.text = v
            cell.text_frame.paragraphs[0].runs[0].font.size = Pt(17)
    cap = s.shapes.add_textbox(Inches(ML), Inches(4.6), Inches(CW), Inches(0.4))
    cap.text_frame.margin_left = 0
    fill(cap, [[("Table 1. Sample data summary — tables pick up the brand colors from the theme.", {"color": GREY_DARK})]])
    cap.text_frame.paragraphs[0].runs[0].font.size = Pt(13)

    slide(prs, "Text + Image", title="Key Findings", p1=[
        "Effect sizes were consistent across cohorts", "Replication held under pre-registered analysis",
        "Results support the proposed mechanism"], p10=A / "art_blue.jpg")
    slide(prs, "Image + Text", p10=A / "art_yellow.jpg", title="Data Collection",
          p1="Field data were gathered across three sites using a standardized protocol, with inter-rater reliability checks throughout.")
    slide(prs, "Text + Shaded Box", title="Overview", p10="A quick summary before we dive into the details.",
          p11="This study examines how open science practices affect replication rates in psychological research, drawing on a pre-registered, multi-site design.")
    slide(prs, "Three Columns", title="Our Pillars", p10="Three principles guide this research program.",
          p30=A / "FaGraduationCap.png", p31=A / "FaHandshake.png", p32=A / "FaChartBar.png",
          p40="Rigor", p41="Collaboration", p42="Openness",
          p50="Pre-registered designs and transparent analysis pipelines.",
          p51="Multi-site partnerships across Indonesian universities.",
          p52="Data, code, and materials shared on publication.")
    slide(prs, "Overview Grid", title="Campus Highlights", p10=A / "art_a.jpg", p11=A / "art_b.jpg", p12=A / "art_c.jpg",
          p20="Main Campus, Surabaya", p21="Research Laboratory", p22="Student Life")
    slide(prs, "Quote", p10="Not everything that counts can be counted, and not everything that can be counted counts.",
          p11="— William Bruce Cameron, Informal Sociology (1963)")
    s = slide(prs, "Quote (Dark / Photo)",
              p10="The more any quantitative social indicator is used for social decision-making, the more subject it will be to corruption pressures.",
              p11="— Donald T. Campbell (1976)")
    rid = s.part.get_or_add_image_part(str(A / "art_photo.jpg"))[1]
    s._element.find(qn("p:cSld")).insert(0, parse_xml(
        f'<p:bg {NS}><p:bgPr><a:blipFill dpi="0" rotWithShape="1"><a:blip r:embed="{rid}"/><a:srcRect/>'
        f'<a:stretch><a:fillRect/></a:stretch></a:blipFill><a:effectLst/></p:bgPr></p:bg>'))
    slide(prs, "Closing", title="Thank you!", p1="Questions?",
          p12=["amelia.zein@psikologi.unair.ac.id", "rameliaz.github.io", "github.com/rameliaz"],
          p13="Template source: github.com/rameliaz/quarto-unair-theme")


if __name__ == "__main__":
    import io, zipfile
    tpl = new_presentation("Short presentation title")
    buf = io.BytesIO()
    tpl.save(buf)
    # A .potx is the same package with the template content type on presentation.xml.
    with zipfile.ZipFile(buf) as src, zipfile.ZipFile(OUT / "unair-template.potx", "w", zipfile.ZIP_DEFLATED) as dst:
        for item in src.infolist():
            data = src.read(item.filename)
            if item.filename == "[Content_Types].xml":
                data = data.replace(CT.PML_PRESENTATION_MAIN.encode(), CT.PML_TEMPLATE_MAIN.encode())
            dst.writestr(item, data)

    deck = new_presentation("UNAIR PowerPoint Template")
    sample(deck)
    deck.save(OUT / "unair-sample.pptx")
    print("wrote", OUT)
