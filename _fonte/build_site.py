# -*- coding: utf-8 -*-
"""Gera o site estático (GitHub Pages) a partir de site_data/*.json (completo) e site_sum/*.json (resumo)."""
import json, glob, os, re, html, shutil, unicodedata

ROOT = "/home/claude"
OUT = os.path.join(ROOT, "site")
DATA = os.path.join(ROOT, "site_data")
SUM = os.path.join(ROOT, "site_sum")
PDF_SRC = os.path.join(ROOT, "pkg")
UPL = "/root/.claude/uploads/54d70d1f-0e88-5a20-9611-84f2cee04f0f/"

CATS = {
    "cardio": ("Cardiovascular", ["01", "09", "15", "18", "19", "25", "30"]),
    "resp": ("Respiratório", ["07", "10", "16"]),
    "neuro": ("Neurológico", ["03", "14", "29", "32"]),
    "infec": ("Infecção", ["05", "06", "08", "10", "11", "26"]),
    "metab": ("Metabólico / endócrino", ["02", "13", "24"]),
    "abd": ("Abdome / digestivo", ["20", "21", "22"]),
    "trauma": ("Trauma / ambiente", ["27", "28", "29", "34"]),
    "tox": ("Alergia / toxicologia", ["12", "23"]),
    "mental": ("Saúde mental / violência", ["04", "31", "35"]),
    "dor": ("Dor / musculoesquelético", ["33", "36"]),
    "enf": ("Enfermagem / triagem", ["ENF"]),
}
TIME_DEP = ["30", "01", "03", "05", "12", "34"]  # faixa de acesso rápido

def slugify(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    s = re.sub(r"[^a-zA-Z0-9]+", "-", s).strip("-").lower()
    return s

def num_of(file):
    return file.split("_")[2]

def esc(s): return html.escape(s, quote=True)

def strip_tags(h):
    t = re.sub(r"<[^>]+>", " ", h)
    return re.sub(r"\s+", " ", html.unescape(t)).strip()

SUPPLY = re.compile(r"apresenta|estoque|disponib|REMUME|farm[aá]cia|preparo|glucagon|nitroglicerina|tiras|medidor|bal[aã]o|equipamento|CRIE|soro|tabela local|CCIH", re.I)
TIP_MED = "Verificar a apresentação e a posologia disponíveis no momento: lotes e fornecedores mudam. A dose total do protocolo permanece; o preparo deve ser conferido na ampola em uso."
TIP_GEN = "Item a conferir localmente antes da aprovação institucional. Para medicamentos, verificar sempre a apresentação e a posologia disponíveis no momento (podem mudar por lote)."
def mark_verif(h):
    def rep(m):
        inner = m.group(0)
        if SUPPLY.search(inner):
            return f'<mark class="verif verif-med" title="{TIP_MED}">⚠ verificar posologia/apresentação disponível no momento</mark>'
        return f'<mark class="verif" title="{TIP_GEN}">{inner}</mark>'
    return re.sub(r"\[(VERIFICAR|PACTUAR)[^\]]*\]", rep, h)

# ---------------- load ----------------
protos = []
for f in sorted(glob.glob(os.path.join(DATA, "*.json"))):
    d = json.load(open(f, encoding="utf-8"))
    s = json.load(open(os.path.join(SUM, d["file"] + ".json"), encoding="utf-8"))
    n = num_of(d["file"])
    cats = [k for k, (_, nums) in CATS.items() if n in nums]
    p = dict(d)
    p.update(s)
    p["num"] = n
    p["cats"] = cats
    p["slug"] = (n.lower() + "-" + slugify(s["short_title"]))
    p["href"] = f"protocolos/{p['slug']}.html"
    protos.append(p)
# ENF por último
protos.sort(key=lambda p: (p["num"] == "ENF", p["num"]))
by_num = {p["num"]: p for p in protos}

# ---------------- assets ----------------
for d in ["", "protocolos", "pdf", "assets"]:
    os.makedirs(os.path.join(OUT, d), exist_ok=True)
shutil.copy(UPL + "e3b0988d-image.png", os.path.join(OUT, "assets", "brasao.png"))
shutil.copy(UPL + "06d6573c-image.png", os.path.join(OUT, "assets", "prefeitura.png"))
for p in protos:
    shutil.copy(os.path.join(PDF_SRC, p["pdf"]), os.path.join(OUT, "pdf", p["pdf"]))
shutil.copy(os.path.join(PDF_SRC, "PS_NatalDiegues_00_INDICE_e_PENDENCIAS.pdf"), os.path.join(OUT, "pdf", "PS_NatalDiegues_00_INDICE_e_PENDENCIAS.pdf"))
open(os.path.join(OUT, ".nojekyll"), "w").close()

CSS = open(os.path.join(ROOT, "site_src", "style.css"), encoding="utf-8").read()
JS = open(os.path.join(ROOT, "site_src", "app.js"), encoding="utf-8").read()
open(os.path.join(OUT, "assets", "style.css"), "w", encoding="utf-8").write(CSS)
open(os.path.join(OUT, "assets", "app.js"), "w", encoding="utf-8").write(JS)

FAVICON = '<link rel="icon" href="{r}assets/brasao.png">'

def header(rel, compact=False):
    return f'''
<a class="skip" href="#main">Ir para o conteúdo</a>
<div class="govbar"><div class="wrap"><span>Prefeitura Municipal de Estiva Gerbi / SP</span><span class="sep">•</span><span>Secretaria Municipal de Saúde</span><span class="sep">•</span><span>Pronto-Socorro Natal Diegues</span></div></div>
<header class="site-head{' compact' if compact else ''}">
  <div class="wrap head-row">
    <a class="brand" href="{rel}index.html" aria-label="Página inicial — Protocolos PS Natal Diegues">
      <img src="{rel}assets/brasao.png" alt="Brasão de Estiva Gerbi — Luta e Conquista" width="56" height="56">
      <span class="brand-txt"><strong>Protocolos de Urgência e Emergência</strong><small>Pronto-Socorro Natal Diegues — Estiva Gerbi/SP</small></span>
    </a>
    <nav class="topnav" aria-label="Principal"><a href="{rel}index.html">Protocolos</a><a href="{rel}calculadora.html">Calculadora</a></nav>
    <img class="logo-pref" src="{rel}assets/prefeitura.png" alt="Prefeitura Municipal de Estiva Gerbi — Um governo humanizado" width="150">
  </div>
</header>'''

def footer(rel):
    return f'''
<footer class="site-foot">
  <div class="wrap foot-grid">
    <div>
      <strong>Série de protocolos institucionais — PS Natal Diegues</strong>
      <p>Elaboração: Felipe Ribeiro Toledo — Médico — CRM-SP 216.986. Versão 1.0 (minuta) — data-base setembro/2026. Documentos pendentes de aprovação pela Direção Clínica e Coordenação do PS; campos de vigência em branco até a assinatura.</p>
    </div>
    <div>
      <strong>Uso</strong>
      <p>Material de apoio à decisão para a equipe do PS. Não substitui o julgamento clínico à beira-leito nem a bula/diretriz vigente. Doses são expressas como dose total/taxa; <b>apresentações e diluições variam por lote</b> — conferir sempre a ampola em uso (ver <a href="{rel}calculadora.html">calculadora</a>).</p>
    </div>
    <div>
      <strong>Documentos</strong>
      <p><a href="{rel}pdf/PS_NatalDiegues_00_INDICE_e_PENDENCIAS.pdf">Índice geral e pendências (PDF)</a><br><a href="{rel}index.html#rede">Rede de referência pactuada</a></p>
    </div>
  </div>
  <div class="wrap foot-cred"><span><b>Desenvolvido por</b> Felipe Ribeiro Toledo — Médico — CRM-SP 216.986</span><span><b>Verificação e validação dos dados e protocolos</b> Edgar Aguiar</span></div>
  <div class="wrap foot-bottom">Prefeitura Municipal de Estiva Gerbi — Secretaria Municipal de Saúde • Site estático para consulta rápida.</div>
</footer>'''

def page(title, body, rel, extra_head="", compact=False, desc=""):
    return f'''<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc or title)}">
<meta name="theme-color" content="#1F3A5F">
{FAVICON.format(r=rel)}
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{rel}assets/style.css">
{extra_head}
</head>
<body>
{header(rel, compact)}
<main id="main" class="wrap">
{body}
</main>
{footer(rel)}
<script src="{rel}assets/app.js" defer></script>
</body>
</html>'''

# ---------------- index ----------------
def card(p):
    cat_lbl = " · ".join(CATS[c][0] for c in p["cats"]) if p["cats"] else ""
    badge = p["code"].replace("PS-ND-", "")
    return (f'<a class="card" href="{p["href"]}" data-cats="{" ".join(p["cats"])}" data-num="{p["num"]}">'
            f'<span class="card-num">{esc(badge)}</span>'
            f'<span class="card-title">{esc(p["short_title"])}</span>'
            f'<span class="card-sub">{esc(p["doc_title"])}</span>'
            f'<span class="card-cat">{esc(cat_lbl)}</span></a>')

search_index = []
for p in protos:
    txt = " ".join([p["short_title"], p["doc_title"], p["title"], p["subtitle"], " ".join(p["tags"]),
                    strip_tags(p["queixa"]), strip_tags(p["diagnostico_conduta"])[:1500], strip_tags(p["alarme"])])
    search_index.append(dict(n=p["num"], t=p["short_title"], f=p["doc_title"], h=p["href"], c=p["cats"], x=txt.lower()[:2600]))

quick = "".join(f'<a class="quick" href="{by_num[n]["href"]}"><span class="q-num">{by_num[n]["code"].replace("PS-ND-","")}</span>{esc(by_num[n]["short_title"])}</a>' for n in TIME_DEP)
chips = '<button class="chip is-on" data-cat="all" type="button">Todos</button>' + "".join(
    f'<button class="chip" data-cat="{k}" type="button">{esc(v[0])}</button>' for k, v in CATS.items())
cards = "".join(card(p) for p in protos)

index_body = f'''
<section class="hero">
  <h1>Consulta rápida de protocolos do PS</h1>
  <p class="lead">36 patologias + protocolo de enfermagem. Cada protocolo tem um <strong>modo resumido</strong> (queixa, diagnóstico e conduta, sinais de alarme, cuidados) e o <strong>documento completo</strong> com fluxograma, doses e referências.</p>
  <form class="search" role="search" onsubmit="return false">
    <label for="q" class="sr-only">Buscar protocolo</label>
    <svg class="s-ico" viewBox="0 0 24 24" aria-hidden="true"><circle cx="11" cy="11" r="7" fill="none" stroke="currentColor" stroke-width="2"/><path d="M20 20l-3.5-3.5" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>
    <input id="q" type="search" autocomplete="off" placeholder="Buscar por doença, sintoma ou medicamento — ex.: dor torácica, adrenalina, CIWA" aria-describedby="q-help">
    <kbd aria-hidden="true">/</kbd>
  </form>
  <p id="q-help" class="help"><span id="count">{len(protos)}</span> protocolos. Atalho: tecle <kbd>/</kbd> para buscar; <kbd>Esc</kbd> limpa.</p>
</section>

<section class="quick-strip" aria-label="Emergências tempo-dependentes">
  <span class="qs-lbl">Tempo-dependentes</span>
  {quick}
</section>

<section class="filters" aria-label="Filtrar por área">{chips}</section>

<section class="grid" id="grid">{cards}</section>
<p class="empty" id="empty" hidden>Nenhum protocolo corresponde à busca. Tente outro termo (sintoma, fármaco, sigla).</p>

<section class="rede" id="rede">
  <h2>Rede de referência pactuada <small>(04/09/2026)</small></h2>
  <div class="rede-grid">
    <div class="rede-item"><strong>Hospital Municipal Tabajara Ramos</strong><span>Mogi Guaçu</span><p>Hemodinâmica; casos clínicos e demais.</p></div>
    <div class="rede-item"><strong>Santa Casa de Mogi Guaçu</strong><span>Mogi Guaçu</span><p>Casos cirúrgicos, ginecológicos/obstétricos e pediatria.</p></div>
    <div class="rede-item"><strong>Regulação</strong><span>CROSS-SP • SAMU 192</span><p>Toda transferência passa pela regulação; comunicar médico a médico.</p></div>
  </div>
  <p class="small">Cenário fixo da série: PS sem hemodinâmica, sem UTI própria e sem neurologia — estabilizar e regular.</p>
</section>
<script>window.__INDEX__ = {json.dumps(search_index, ensure_ascii=False)};</script>
'''
open(os.path.join(OUT, "index.html"), "w", encoding="utf-8").write(
    page("Protocolos de Urgência — PS Natal Diegues — Estiva Gerbi", index_body, "./",
         desc="Protocolos institucionais de urgência e emergência do Pronto-Socorro Natal Diegues, Prefeitura de Estiva Gerbi/SP. Modo resumido e documento completo."))

# ---------------- protocol pages ----------------
def add_ids(h):
    toc = []
    def rep(m):
        txt = strip_tags(m.group(1))
        i = len(toc)
        toc.append((f"s{i}", txt))
        return f'<h2 id="s{i}">{m.group(1)}</h2>'
    h2 = re.sub(r"<h2>(.*?)</h2>", rep, h, flags=re.S)
    return h2, toc

def summary_block(p, flow_svg):
    sec = lambda cls, icon, ttl, body: f'''
<section class="sum sum-{cls}">
  <h2><span class="sum-ico" aria-hidden="true">{icon}</span>{ttl}</h2>
  <div class="sum-body">{mark_verif(body)}</div>
</section>'''
    out = [sec("queixa", "💬", "Queixa comum", p["queixa"]),
           sec("diag", "🩺", "Diagnóstico e conduta", p["diagnostico_conduta"]),
           sec("alarme", "⚠️", "Sinais de alarme", p["alarme"]),
           sec("cuidados", "🛡️", "Cuidados importantes", p["cuidados"])]
    if flow_svg:
        out.append(f'<details class="flow-details"><summary>Fluxograma de atendimento</summary>{flow_svg}<p class="small">Legenda: azul = entrada; amarelo = decisão; azul-claro = conduta; vermelho = risco/atenção; verde = desfecho/transferência.</p></details>')
    return "".join(out)

for i, p in enumerate(protos):
    rel = "../"
    full_html, toc = add_ids(mark_verif(p["html"]))
    m = re.search(r'<div class="flow-wrap">.*?</div>', p["html"], flags=re.S)
    flow_svg = m.group(0) if m else ""
    meta = f'''
<table class="meta"><tbody>
<tr><th>Código</th><td>{esc(p["code"])}</td><th>Versão</th><td>{esc(p["version"])}</td></tr>
<tr><th>Elaboração</th><td>Felipe Ribeiro Toledo — Médico — CRM-SP 216.986</td><th>Data-base</th><td>{esc(p["date"])}</td></tr>
<tr><th>Aprovação (Diretor Clínico)</th><td class="blank"></td><th>Vigência</th><td class="blank"></td></tr>
<tr><th>Aprovação (Coordenação PS)</th><td class="blank"></td><th>Revisão prevista</th><td class="blank"></td></tr>
</tbody></table>'''
    toc_html = "".join(f'<li><a href="#{a}">{esc(t)}</a></li>' for a, t in toc)
    prev_p = protos[i - 1] if i > 0 else None
    next_p = protos[i + 1] if i + 1 < len(protos) else None
    nav = '<nav class="pn" aria-label="Protocolos vizinhos">'
    nav += f'<a class="pn-prev" href="{prev_p["slug"]}.html"><small>Anterior</small>{esc(prev_p["short_title"])}</a>' if prev_p else "<span></span>"
    nav += f'<a class="pn-next" href="{next_p["slug"]}.html"><small>Próximo</small>{esc(next_p["short_title"])}</a>' if next_p else "<span></span>"
    nav += "</nav>"
    cat_lbl = " · ".join(CATS[c][0] for c in p["cats"])
    body = f'''
<nav class="crumbs" aria-label="Navegação"><a href="{rel}index.html">← Todos os protocolos</a><span>{esc(cat_lbl)}</span></nav>
<div class="proto-head">
  <span class="code">{esc(p["code"])}</span>
  <h1>{esc(p["title"])}</h1>
  <p class="subtitle">{esc(p["subtitle"])}</p>
  <div class="toolbar">
    <div class="seg" role="tablist" aria-label="Modo de leitura">
      <button role="tab" id="tab-resumo" aria-controls="resumo" aria-selected="true" data-mode="resumo" type="button">Resumo</button>
      <button role="tab" id="tab-completo" aria-controls="completo" aria-selected="false" data-mode="completo" type="button">Protocolo completo</button>
    </div>
    <a class="btn-pdf" href="{rel}pdf/{p["pdf"]}" download>Baixar PDF</a>
    <button class="btn-print" type="button" onclick="window.print()">Imprimir</button>
    <a class="btn-calc" href="{rel}calculadora.html">Calculadora de diluição</a>
  </div>
</div>

<section id="resumo" role="tabpanel" aria-labelledby="tab-resumo" class="mode-panel">
  <p class="mode-note">Síntese fiel ao protocolo completo, para consulta à beira-leito. Em dúvida, confira o documento completo.</p>
  <div class="box box-warn med-note"><b>Medicamentos:</b> as doses abaixo são doses totais/taxas do protocolo. Itens marcados <mark class="verif verif-med">⚠ verificar posologia/apresentação</mark> dependem do lote em uso — confira a ampola e calcule o preparo na <a href="{rel}calculadora.html">calculadora de diluição</a>.</div>
  {summary_block(p, flow_svg)}
</section>

<section id="completo" role="tabpanel" aria-labelledby="tab-completo" class="mode-panel" hidden>
  <div class="full-layout">
    <aside class="toc"><details class="toc-in" open><summary>Sumário</summary><ol>{toc_html}</ol></details></aside>
    <article class="doc">
      {meta}
      {full_html}
    </article>
  </div>
</section>
{nav}
'''
    open(os.path.join(OUT, "protocolos", p["slug"] + ".html"), "w", encoding="utf-8").write(
        page(f"{p['short_title']} — {p['code']} — PS Natal Diegues", body, rel, compact=True,
             desc=p["title"]))

# calculadora
calc_body = open(os.path.join(ROOT, "site_src", "calc_body.html"), encoding="utf-8").read()
open(os.path.join(OUT, "assets", "calc.js"), "w", encoding="utf-8").write(open(os.path.join(ROOT, "site_src", "calc.js"), encoding="utf-8").read())
open(os.path.join(OUT, "calculadora.html"), "w", encoding="utf-8").write(
    page("Calculadora de diluição e infusão — PS Natal Diegues", calc_body, "./",
         extra_head='<script src="./assets/calc.js" defer></script>', compact=True,
         desc="Calculadora de diluição, velocidade de infusão e doses por peso das drogas usadas nos protocolos do PS Natal Diegues."))

# README + 404
open(os.path.join(OUT, "README.md"), "w", encoding="utf-8").write(f"""# Protocolos de Urgência — PS Natal Diegues (Estiva Gerbi/SP)

Site estático (HTML/CSS/JS puro, sem build) com os {len(protos)} protocolos institucionais do Pronto-Socorro Natal Diegues.

## Publicar no GitHub Pages
1. Crie um repositório (ex.: `protocolos-ps-natal-diegues`) e envie **todo o conteúdo desta pasta** para a raiz do repositório (branch `main`).
2. Em *Settings → Pages*, escolha **Deploy from a branch**, branch `main`, pasta `/ (root)`. Salve.
3. Em 1–2 minutos o site estará em `https://<usuario>.github.io/<repositorio>/`.

O arquivo `.nojekyll` garante que o GitHub sirva os arquivos sem processamento.

## Estrutura
- `index.html` — página inicial com busca, filtros por área e cards.
- `protocolos/*.html` — uma página por protocolo (modo resumido + documento completo + fluxograma SVG).
- `pdf/` — PDFs originais (download em cada página).
- `assets/` — estilo, script e logos.

## Atualizar um protocolo
Os textos são gerados a partir dos scripts-fonte da série (ReportLab). Para mudar o conteúdo, altere o script `pNN_*.py`, regenere o PDF e o site (`build_site.py`) e substitua os arquivos.
""")
open(os.path.join(OUT, "404.html"), "w", encoding="utf-8").write(
    page("Página não encontrada", '<section class="hero"><h1>Página não encontrada</h1><p class="lead"><a href="index.html">Voltar aos protocolos</a></p></section>', "./"))
print("site gerado:", len(protos), "protocolos")
