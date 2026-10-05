# -*- coding: utf-8 -*-
"""Shim: same API as the PDF base, but captures the story as HTML/JSON for the website."""
import json, os, re, html as _html

mm = 1.0
CONTENT_W = 174.0
A4 = (210.0, 297.0)
PAGE_W, PAGE_H = A4
MARG = 18.0

class _Colors:
    black = "#000000"; white = "#ffffff"
    def HexColor(self, s): return s
colors = _Colors()
AZUL = "#1F3A5F"; AZUL_CLARO = "#E8EEF6"; CINZA = "#555555"; CINZA_CLARO = "#F2F2F2"
VERMELHO = "#A8322D"; VERMELHO_CLARO = "#FBEAE9"; AMARELO = "#FFF4D6"; VERDE = "#2E6B3A"
VERDE_CLARO = "#E6F2E8"; LARANJA = "#C9781C"
S = {k: k for k in ["body", "small", "h1", "h2", "h3", "cell", "cellb", "cellw", "bullet", "alert", "title", "subtitle", "center"]}

REF_CLINICA = "Hospital Municipal Tabajara Ramos (Mogi Guaçu) — hemodinâmica, casos clínicos e demais"
REF_CIRURGICA = "Santa Casa de Mogi Guaçu — casos cirúrgicos, ginecológicos/obstétricos e pediatria"
REF_REGULACAO = "CROSS-SP / SAMU 192"

OUT_DIR = os.environ.get("PS_SITE_DATA", "/home/claude/site_data")
os.makedirs(OUT_DIR, exist_ok=True)

# ---------- markup conversion (reportlab para -> html) ----------
_FONT_RE = re.compile(r"<font\s+color=['\"]?([^'\" >]+)['\"]?\s*>", re.I)
def conv(txt):
    if not isinstance(txt, str):
        return str(txt)
    t = txt.replace("<br/>", "<br>").replace("<br />", "<br>")
    t = _FONT_RE.sub(lambda m: f'<span style="color:{m.group(1)}">', t)
    t = re.sub(r"</font>", "</span>", t, flags=re.I)
    return t

# ---------- node types ----------
class Node:
    def __init__(self, kind, **kw):
        self.kind = kind; self.__dict__.update(kw)
    def html(self):
        k = self.kind
        if k == "p":
            cls = {"small": "small", "center": "center"}.get(self.st, "")
            return f'<p class="{cls}">{conv(self.txt)}</p>' if cls else f"<p>{conv(self.txt)}</p>"
        if k == "h":
            return f"<h{self.level + 1}>{conv(self.txt)}</h{self.level + 1}>"
        if k == "ul":
            cls = ' class="small"' if self.st == "small" else ""
            return f"<ul{cls}>" + "".join(f"<li>{conv(i)}</li>" for i in self.items) + "</ul>"
        if k == "box":
            return f'<div class="box box-{self.boxkind}">{conv(self.txt)}</div>'
        if k == "table":
            out = ['<div class="tbl-wrap"><table>']
            for i, r in enumerate(self.rows):
                tag = "th" if (self.header and i == 0) else "td"
                cells = "".join(f"<{tag}>{_cell(c)}</{tag}>" for c in r)
                out.append(f"<tr>{cells}</tr>")
            out.append("</table></div>")
            return "".join(out)
        if k == "flow":
            return flow_svg(self.nodes, self.edges, self.ncols, self.nrows)
        if k == "legend":
            return ('<div class="legend"><span><i class="sw sw-start"></i>Entrada</span><span><i class="sw sw-decision"></i>Decisão</span>'
                    '<span><i class="sw sw-action"></i>Conduta</span><span><i class="sw sw-danger"></i>Risco / atenção</span>'
                    '<span><i class="sw sw-end"></i>Desfecho / transferência</span></div>')
        if k == "sig":
            return ('<div class="sig"><div class="sig-line"></div><b>Felipe Ribeiro Toledo — Médico — CRM-SP 216.986</b>'
                    '<div class="small">Responsável técnico pela elaboração</div></div>')
        if k == "group":
            return "".join(_h(x) for x in self.items)
        if k == "front":
            return ""  # rendered from metadata
        return ""

def _h(x):
    if isinstance(x, Node): return x.html()
    if isinstance(x, (list, tuple)): return "".join(_h(i) for i in x)
    if x is None: return ""
    return conv(str(x))

def _cell(c):
    if isinstance(c, str): return conv(c)
    return _h(c)

def P(txt, st="body"): return Node("p", txt=txt, st=st)
def H1(t): return Node("h", level=1, txt=t)
def H2(t): return Node("h", level=2, txt=t)
def H3(t): return Node("h", level=3, txt=t)
def bullets(items, st="bullet"): return Node("ul", items=list(items), st=st)
def box(txt, kind="alert"): return Node("box", txt=txt, boxkind=kind)
def table(rows, widths=None, header=True, zebra=True, fs=None): return Node("table", rows=rows, header=header)
def legend(): return Node("legend")
def signature_block(): return [Node("sig")]
def Spacer(*a, **k): return None
def PageBreak(*a, **k): return None
def KeepTogether(items): return Node("group", items=list(items))
class Paragraph(Node):
    def __init__(self, txt, st="body"): super().__init__("p", txt=txt, st=st if isinstance(st, str) else "body")
def Table(*a, **k): return None
def TableStyle(*a, **k): return None
class Flowable: pass
class HeaderBand(Flowable):
    def __init__(self, *a, **k): pass

class Flowchart(Node):
    def __init__(self, nodes, edges, ncols, nrows, width=None, row_h=None, node_h=None, fs=None):
        super().__init__("flow", nodes=nodes, edges=edges, ncols=ncols, nrows=nrows)

_META = {}
def front_block(title, subtitle, code, version="1.0 (minuta)", date="setembro/2026"):
    _META.update(dict(title=title, subtitle=subtitle, code=code, version=version, date=date))
    return [Node("front")]

class _Doc:
    def __init__(self, path, title, code):
        self.path, self.title, self.code = path, title, code
    def build(self, story, **kw):
        body = "".join(_h(x) for x in story)
        base = os.path.basename(self.path).replace(".pdf", "")
        data = dict(_META); data.update(file=base, pdf=os.path.basename(self.path), doc_title=self.title, code=self.code,
                    html=body)
        with open(os.path.join(OUT_DIR, base + ".json"), "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False)
        print("captured", base, len(body))

def make_doc(path, doc_title, doc_code):
    return _Doc(path, doc_title, doc_code), None

def qa(*a, **k): return []

# ---------- flowchart -> SVG ----------
def _esc(s): return _html.escape(s, quote=True)

def flow_svg(nodes, edges, ncols, nrows):
    W = 760.0
    col_w = W / ncols
    row_h = 88.0; node_h = 60.0
    H = nrows * row_h + 16
    def center(nid):
        col, row, _, _ = nodes[nid]
        return (col + 0.5) * col_w, 8 + (row + 0.5) * row_h
    fill = {"start": ("#1F3A5F", "#fff"), "decision": ("#FFF4D6", "#111"), "action": ("#E8EEF6", "#111"),
            "danger": ("#FBEAE9", "#111"), "end": ("#E6F2E8", "#111"), "info": ("#F2F2F2", "#111")}
    out = [f'<div class="flow-wrap"><svg class="flow" viewBox="0 0 {W:.0f} {H:.0f}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Fluxograma">',
           '<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
           '<path d="M0,0 L10,5 L0,10 z" fill="#666"/></marker></defs>']
    for e in edges:
        frm, to, label = e[0], e[1], (e[2] if len(e) > 2 else "")
        x1, y1 = center(frm); x2, y2 = center(to)
        st = 'stroke="#666" stroke-width="1.6" fill="none" marker-end="url(#ah)"'
        if abs(x1 - x2) < 1:
            out.append(f'<path d="M{x1:.1f},{y1 + node_h/2:.1f} L{x2:.1f},{y2 - node_h/2:.1f}" {st}/>')
            lx, ly = x1 + 14, (y1 + node_h/2 + y2 - node_h/2) / 2 + 4
            anchor = "start"
        elif abs(y1 - y2) < 1:
            sgn = 1 if x2 > x1 else -1
            out.append(f'<path d="M{x1 + sgn*col_w*0.45:.1f},{y1:.1f} L{x2 - sgn*col_w*0.45:.1f},{y2:.1f}" {st}/>')
            lx, ly = (x1 + x2) / 2, y1 - 6; anchor = "middle"
        else:
            ym = y2 - row_h / 2 if y2 > y1 else y1 + row_h / 2
            out.append(f'<path d="M{x1:.1f},{y1 + node_h/2:.1f} L{x1:.1f},{ym:.1f} L{x2:.1f},{ym:.1f} L{x2:.1f},{y2 - node_h/2:.1f}" {st}/>')
            lx, ly = (x1 + x2) / 2, ym - 5; anchor = "middle"
        if label:
            col = "#A8322D" if label.upper().startswith("N") else "#2E6B3A"
            out.append(f'<text x="{lx:.1f}" y="{ly:.1f}" text-anchor="{anchor}" font-size="11" font-weight="700" fill="{col}" class="flow-lbl">{_esc(label)}</text>')
    for nid, (col, row, txt, kind) in nodes.items():
        x, y = center(nid)
        bw = col_w * 0.92; bh = node_h
        f, tc = fill.get(kind, fill["info"])
        stroke = "#A8322D" if kind == "danger" else "#1F3A5F"
        rx = 22 if kind == "decision" else 6
        out.append(f'<rect x="{x - bw/2:.1f}" y="{y - bh/2:.1f}" width="{bw:.1f}" height="{bh:.1f}" rx="{rx}" fill="{f}" stroke="{stroke}" stroke-width="1.4"/>')
        lines = txt.split("\n")
        maxlen = max(len(l) for l in lines) if lines else 1
        fs = min(12.0, max(7.2, (bw - 10) / (maxlen * 0.56)))
        lh = fs * 1.22
        y0 = y - (len(lines) - 1) * lh / 2
        weight = "700" if kind in ("start", "decision") else "500"
        for i, ln in enumerate(lines):
            out.append(f'<text x="{x:.1f}" y="{y0 + i*lh:.1f}" text-anchor="middle" dominant-baseline="middle" font-size="{fs:.1f}" font-weight="{weight}" fill="{tc}">{_esc(ln)}</text>')
    out.append("</svg></div>")
    return "".join(out)
