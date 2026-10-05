# Protocolos de Urgência — PS Natal Diegues (Estiva Gerbi/SP)

Site estático (HTML/CSS/JS puro, sem build) com os 36 protocolos institucionais do Pronto-Socorro Natal Diegues.

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
