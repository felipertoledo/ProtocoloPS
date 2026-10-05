(function () {
  "use strict";
  // ------- Drogas em infusão contínua (doses conforme os protocolos da série) -------
  // ampUnit: unidade do conteúdo da ampola; unit: unidade da dose. perKg/perMin derivam da unit.
  var DRUGS = [
    { id: "nora", name: "Noradrenalina", ref: "Prot. 05 · 12 · 09", ampUnit: "mg", ampMg: 4, ampMl: 4, n: 4, vol: 250, unit: "mcg/kg/min", min: 0.05, max: 0.5, start: 0.05,
      nota: "Início 0,05–0,1 mcg/kg/min, titular até PAM ≥65. Ampola pode ser 4 mg/4 mL ou 8 mg/4 mL — conferir. Veia periférica calibrosa é aceitável no início; extravasamento → infiltrar fentolamina." },
    { id: "adre", name: "Adrenalina (infusão)", ref: "Prot. 12 · 30 · 18", ampUnit: "mg", ampMg: 1, ampMl: 1, n: 1, vol: 100, unit: "mcg/kg/min", min: 0.05, max: 0.5, start: 0.05,
      nota: "Anafilaxia refratária: 0,05–0,1 mcg/kg/min (adulto 1–10 mcg/min) após 2–3 doses IM + volume. Pós-PCR / bradicardia instável: 2–10 mcg/min. Sempre em bomba." },
    { id: "vaso", name: "Vasopressina", ref: "Prot. 05", ampUnit: "U", ampMg: 20, ampMl: 1, n: 1, vol: 100, unit: "U/min", min: 0.01, max: 0.04, start: 0.03,
      nota: "Dose fixa 0,03 U/min (0,01–0,04) quando noradrenalina em escalada; não titular como vasopressor de 1ª linha." },
    { id: "dobu", name: "Dobutamina", ref: "Prot. 09 · 05", ampUnit: "mg", ampMg: 250, ampMl: 20, n: 1, vol: 250, unit: "mcg/kg/min", min: 2.5, max: 20, start: 2.5,
      nota: "Perfil frio-úmido / disfunção miocárdica na sepse: iniciar 2,5–5 mcg/kg/min. Somar vasopressor se PAS <90." },
    { id: "dopa", name: "Dopamina", ref: "Prot. 18 · 30", ampUnit: "mg", ampMg: 50, ampMl: 10, n: 5, vol: 250, unit: "mcg/kg/min", min: 2, max: 20, start: 5,
      nota: "Bradicardia sintomática refratária à atropina: 5–20 mcg/kg/min (alternativa: adrenalina 2–10 mcg/min) enquanto se prepara o marca-passo." },
    { id: "ntg", name: "Nitroglicerina", ref: "Prot. 09 · 15 · 01", ampUnit: "mg", ampMg: 50, ampMl: 10, n: 1, vol: 250, unit: "mcg/min", min: 5, max: 200, start: 10,
      nota: "EAP hipertensivo / SCA com dor persistente: iniciar 10–20 mcg/min, dobrar a cada 3–5 min até 100–200 mcg/min. Contraindicada com PAS <90, IAM de VD e inibidor de PDE-5." },
    { id: "nps", name: "Nitroprussiato de sódio", ref: "Prot. 15 · 03", ampUnit: "mg", ampMg: 50, ampMl: 2, n: 1, vol: 250, unit: "mcg/kg/min", min: 0.25, max: 10, start: 0.25,
      nota: "Emergência hipertensiva: iniciar 0,25 mcg/kg/min, titular a cada 3–5 min; proteger da luz; na dissecção, betabloqueador IV antes. Evitar >2 mcg/kg/min por tempo prolongado (cianeto)." },
    { id: "amio", name: "Amiodarona (manutenção)", ref: "Prot. 18 · 30", ampUnit: "mg", ampMg: 150, ampMl: 3, n: 6, vol: 500, unit: "mg/min", min: 0.5, max: 1, start: 1,
      nota: "Ataque 150 mg IV em 10 min (TV/FA com pulso; repetir se recorrer) → 1 mg/min por 6 h → 0,5 mg/min por 18 h (máx. 2,2 g/24 h). PCR: 300 mg bólus → 150 mg. Diluir em SG 5%." },
    { id: "insu", name: "Insulina regular (bomba)", ref: "Prot. 02", ampUnit: "U", ampMg: 100, ampMl: 1, n: 1, vol: 100, unit: "U/kg/h", min: 0.05, max: 0.14, start: 0.1,
      nota: "CAD/EHH: 0,1 U/kg/h após K ≥3,3. Meta de queda 50–70 mg/dL/h; se <50 na 1ª h, dobrar; se >100/h, reduzir. Desprezar os primeiros 20 mL pelo equipo (adsorção)." },
    { id: "hnf", name: "Heparina não fracionada", ref: "Prot. 19 · 01", ampUnit: "U", ampMg: 5000, ampMl: 1, n: 5, vol: 250, unit: "U/kg/h", min: 12, max: 18, start: 18,
      nota: "TEP: bólus 80 U/kg → 18 U/kg/h, TTPa 1,5–2,5× (ver bólus abaixo). SCA: bólus 60 U/kg (máx. 4.000) → 12 U/kg/h (máx. 1.000 U/h)." },
    { id: "mida", name: "Midazolam (infusão)", ref: "Prot. 14 · 04 · 36", ampUnit: "mg", ampMg: 50, ampMl: 10, n: 1, vol: 50, unit: "mg/kg/h", min: 0.05, max: 2, start: 0.1,
      nota: "EME refratário: bólus 0,2 mg/kg → 0,05–2 mg/kg/h (exige via aérea protegida e monitorização). Sedação leve: 0,02–0,1 mg/kg/h." },
    { id: "fent", name: "Fentanil (infusão)", ref: "Prot. 36 · 34 · 14", ampUnit: "mcg", ampMg: 500, ampMl: 10, n: 1, vol: 50, unit: "mcg/kg/h", min: 0.5, max: 2, start: 1,
      nota: "Analgesia/sedação do paciente intubado: 0,5–2 mcg/kg/h. Bólus 1 mcg/kg IV (rápido, curto). Capnografia/oximetria contínuas." },
    { id: "keta", name: "Cetamina (infusão)", ref: "Prot. 14 · 36", ampUnit: "mg", ampMg: 500, ampMl: 10, n: 1, vol: 50, unit: "mg/kg/h", min: 0.5, max: 5, start: 1,
      nota: "EME refratário: bólus 1–2 mg/kg → 1–5 mg/kg/h (preserva PA). Analgesia subdissociativa: 0,1–0,3 mg/kg em 10–15 min (ver bólus)." },
    { id: "prop", name: "Propofol", ref: "Prot. 14", ampUnit: "mg", ampMg: 200, ampMl: 20, n: 1, vol: 20, unit: "mcg/kg/min", min: 20, max: 200, start: 30,
      nota: "EME refratário: bólus 1–2 mg/kg → 20–200 mcg/kg/min; hipotensão frequente; evitar >4 mg/kg/h por >48 h (síndrome da infusão). Usar puro (10 mg/mL) ou conforme padronização." },
    { id: "ibp", name: "Omeprazol/pantoprazol (infusão)", ref: "Prot. 22", ampUnit: "mg", ampMg: 40, ampMl: 10, n: 4, vol: 100, unit: "mg/h", min: 8, max: 8, start: 8,
      nota: "HDA não varicosa com estigma de alto risco: 80 mg IV bólus → 8 mg/h por 72 h (160 mg em 100–250 mL, trocar a cada 12–24 h conforme estabilidade da apresentação)." },
    { id: "octr", name: "Octreotida", ref: "Prot. 22", ampUnit: "mcg", ampMg: 100, ampMl: 1, n: 5, vol: 250, unit: "mcg/h", min: 25, max: 50, start: 50,
      nota: "HDA varicosa suspeita: bólus 50 mcg IV → 50 mcg/h por 2–5 dias (alternativa à terlipressina 2 mg IV 4/4 h)." }
  ];

  // ------- Bólus e volumes por peso -------
  // f(kg, idade, scq) -> {val, unit, extra}
  var BOLUS = [
    { g: "Reanimação e choque", items: [
      { n: "Adrenalina IM — anafilaxia (1 mg/mL)", ref: "12", f: function (k) { var d = Math.min(0.01 * k, k < 30 ? 0.3 : 0.5); return fmt(d, "mg") + " = " + fmt(d, "mL") + " IM (coxa). Repetir 5–15 min; adulto 0,3–0,5 mg"; } },
      { n: "Adrenalina IV/IO — PCR", ref: "30", f: function (k) { return k >= 40 ? "1 mg a cada 3–5 min (adulto)" : fmt(Math.min(0.01 * k, 1), "mg") + " (0,01 mg/kg, máx. 1 mg) a cada 3–5 min"; } },
      { n: "Amiodarona — PCR (FV/TVSP refratária)", ref: "30", f: function (k) { return k >= 40 ? "300 mg bólus → 150 mg em 3–5 min" : fmt(Math.min(5 * k, 300), "mg") + " (5 mg/kg, máx. 300) — repetir até 3×"; } },
      { n: "Lidocaína — PCR (alternativa)", ref: "30", f: function (k) { return fmt(1 * k, "mg") + "–" + fmt(1.5 * k, "mg") + " (1–1,5 mg/kg) → 0,5–0,75 mg/kg a cada 5–10 min (máx. 3 mg/kg)"; } },
      { n: "Cristaloide — sepse/choque séptico", ref: "05", f: function (k) { return fmt(30 * k, "mL") + " (30 mL/kg) na 1ª–3ª h se hipotensão/lactato ≥4; alíquotas de 500 mL (250 em cardiopata/DRC) com reavaliação"; } },
      { n: "Cristaloide — anafilaxia / dengue grupo D", ref: "12 · 11", f: function (k) { return fmt(20 * k, "mL") + " (20 mL/kg) rápido; repetir por PA/pulso"; } },
      { n: "Cristaloide — CAD 1ª hora", ref: "02", f: function (k) { return fmt(15 * k, "mL") + "–" + fmt(20 * k, "mL") + " (15–20 mL/kg) SF 0,9% na 1ª h; depois 250–500 mL/h"; } },
      { n: "Dengue grupo C — fase de expansão", ref: "11", f: function (k) { return fmt(10 * k, "mL") + "/h (10 mL/kg/h) por 1–2 h, reavaliar a cada hora"; } },
      { n: "Queimadura — fórmula de Parkland (ABA 2023)", ref: "28", f: function (k, a, s) { var t = 2 * k * s; return s ? fmt(t, "mL") + " em 24 h (2 mL/kg/% SCQ) → " + fmt(t / 2, "mL") + " nas 1ªs 8 h (≈ " + fmt(t / 16, "mL") + "/h); titular pela diurese 0,5 mL/kg/h = " + fmt(0.5 * k, "mL") + "/h" : "informe a % SCQ"; } }
    ] },
    { g: "Fibrinólise e anticoagulação", items: [
      { n: "Tenecteplase — IAMCSST", ref: "01", f: function (k, a) { var d = k < 60 ? 30 : k < 70 ? 35 : k < 80 ? 40 : k < 90 ? 45 : 50; var half = a >= 75; return (half ? fmt(d / 2, "mg") + " (metade da dose — idade ≥75 a; dose plena seria " + d + " mg)" : d + " mg") + " IV em bólus único de 5–10 s"; } },
      { n: "Alteplase — AVC isquêmico", ref: "03", f: function (k) { var d = Math.min(0.9 * k, 90); return fmt(d, "mg") + " (0,9 mg/kg, máx. 90): " + fmt(d * 0.1, "mg") + " em bólus 1 min + " + fmt(d * 0.9, "mg") + " em 60 min"; } },
      { n: "Enoxaparina — SCA (<75 a)", ref: "01", f: function (k, a) { return a >= 75 ? "sem bólus; " + fmt(0.75 * k, "mg") + " SC 12/12 h (0,75 mg/kg — ≥75 a)" : "30 mg IV bólus + " + fmt(1 * k, "mg") + " SC 12/12 h (1 mg/kg, máx. 100 mg/dose); ClCr <30: 1 mg/kg 1×/dia"; } },
      { n: "Enoxaparina — TEP/TVP", ref: "19", f: function (k) { return fmt(1 * k, "mg") + " SC 12/12 h (1 mg/kg) ou " + fmt(1.5 * k, "mg") + " 1×/dia; ClCr <30: 1 mg/kg 1×/dia"; } },
      { n: "Heparina NF — bólus TEP", ref: "19", f: function (k) { return fmt(80 * k, "U") + " IV (80 U/kg) → 18 U/kg/h = " + fmt(18 * k, "U") + "/h"; } },
      { n: "Heparina NF — bólus SCA", ref: "01", f: function (k) { return fmt(Math.min(60 * k, 4000), "U") + " IV (60 U/kg, máx. 4.000) → 12 U/kg/h = " + fmt(Math.min(12 * k, 1000), "U") + "/h (máx. 1.000)"; } }
    ] },
    { g: "Crise convulsiva / sedação / via aérea", items: [
      { n: "Diazepam IV", ref: "14", f: function (k) { return fmt(Math.min(0.15 * k, 10), "mg") + "–" + fmt(Math.min(0.2 * k, 10), "mg") + " (0,15–0,2 mg/kg, máx. 10 mg) a 2 mg/min; repetir 1× em 5 min"; } },
      { n: "Midazolam IM", ref: "14", f: function (k) { return k > 40 ? "10 mg IM (adulto >40 kg)" : fmt(Math.min(0.2 * k, 10), "mg") + " IM (0,2 mg/kg; 13–40 kg: 5 mg)"; } },
      { n: "Fenitoína — ataque", ref: "14", f: function (k) { var d = Math.min(20 * k, 1500); return fmt(d, "mg") + " (20 mg/kg, máx. 1,5 g) em SF 0,9%, ≤50 mg/min → infundir em ≥" + Math.ceil(d / 50) + " min; monitorizar"; } },
      { n: "Levetiracetam — ataque", ref: "14", f: function (k) { return fmt(Math.min(60 * k, 4500), "mg") + " (60 mg/kg, máx. 4,5 g) IV em 10–15 min"; } },
      { n: "Ácido valproico — ataque", ref: "14", f: function (k) { return fmt(Math.min(40 * k, 3000), "mg") + " (40 mg/kg, máx. 3 g) IV em 10 min"; } },
      { n: "Cetamina — indução", ref: "14 · 34", f: function (k) { return fmt(1 * k, "mg") + "–" + fmt(2 * k, "mg") + " IV (1–2 mg/kg)"; } },
      { n: "Etomidato — indução", ref: "34", f: function (k) { return fmt(0.3 * k, "mg") + " IV (0,3 mg/kg)"; } },
      { n: "Succinilcolina", ref: "34", f: function (k) { return fmt(1.5 * k, "mg") + " IV (1,5 mg/kg) — contraindicada em hipercalemia, queimadura >24–72 h, lesão medular/muscular"; } },
      { n: "Rocurônio", ref: "34 · 14", f: function (k) { return fmt(1.2 * k, "mg") + " IV (1,2 mg/kg)"; } },
      { n: "Cetamina — analgesia subdissociativa", ref: "36", f: function (k) { return fmt(0.1 * k, "mg") + "–" + fmt(0.3 * k, "mg") + " (0,1–0,3 mg/kg) em 10–15 min"; } },
      { n: "Fentanil — bólus analgésico", ref: "36", f: function (k) { return fmt(1 * k, "mcg") + " IV (1 mcg/kg) = " + fmt(k / 50, "mL") + " da ampola 50 mcg/mL"; } },
      { n: "Morfina — bólus", ref: "36", f: function (k) { return fmt(0.1 * k, "mg") + " IV (0,1 mg/kg; 2–4 mg por vez no adulto), repetir a cada 5–10 min"; } }
    ] },
    { g: "Metabólico / tóxico / pediatria", items: [
      { n: "Glicose — hipoglicemia", ref: "13", f: function (k) { return k >= 40 ? "Glicose 50%: 30–50 mL (15–25 g) IV; manter SG 10% 50–100 mL/h" : "Glicose 10%: " + fmt(2 * k, "mL") + "–" + fmt(5 * k, "mL") + " (2–5 mL/kg) IV em 5–10 min"; } },
      { n: "Bicarbonato 8,4% — intoxicação (tricíclico/QRS largo)", ref: "23 · 02", f: function (k) { return fmt(1 * k, "mEq") + "–" + fmt(2 * k, "mEq") + " (1–2 mEq/kg) IV em bólus = " + fmt(k, "mL") + "–" + fmt(2 * k, "mL") + " da solução 8,4% (1 mEq/mL)"; } },
      { n: "Naloxona", ref: "23", f: function (k) { return k >= 20 ? "0,04–0,4 mg IV, repetir a cada 2–3 min (até 2 mg; dependente: começar baixo)" : fmt(0.1 * k, "mg") + " (0,1 mg/kg) IV/IM/IN"; } },
      { n: "Gluconato de cálcio 10% — hipercalemia (criança)", ref: "24", f: function (k) { return k >= 40 ? "10–30 mL IV em 5–10 min (adulto), repetir em 5 min se ECG persistir" : fmt(0.5 * k, "mL") + "–" + fmt(1 * k, "mL") + " (0,5–1 mL/kg) IV lento"; } },
      { n: "Sulfato de magnésio — asma grave (criança)", ref: "07", f: function (k) { return k >= 40 ? "2 g IV em 20 min (adulto)" : fmt(Math.min(50 * k, 2000), "mg") + " (25–75 mg/kg, máx. 2 g) IV em 20 min"; } },
      { n: "Salbutamol spray com espaçador (criança)", ref: "07 · 12", f: function (k) { return Math.min(Math.round(k / 2), 10) + " jatos (1 jato/2 kg, máx. 10), 1 jato por vez"; } },
      { n: "SRO — Plano B", ref: "06", f: function (k) { return fmt(50 * k, "mL") + "–" + fmt(100 * k, "mL") + " (50–100 mL/kg) em 4 h, em pequenos goles"; } },
      { n: "Dipirona (criança)", ref: "36 · 06", f: function (k) { return fmt(10 * k, "mg") + "–" + fmt(15 * k, "mg") + " (10–15 mg/kg/dose) a cada 6 h"; } },
      { n: "Paracetamol (criança)", ref: "36 · 06", f: function (k) { return fmt(10 * k, "mg") + "–" + fmt(15 * k, "mg") + " (10–15 mg/kg/dose) a cada 6 h, máx. 75 mg/kg/dia"; } },
      { n: "Ibuprofeno (criança)", ref: "36", f: function (k) { return fmt(10 * k, "mg") + " (10 mg/kg/dose) a cada 8 h"; } }
    ] }
  ];

  function fmt(v, unit) {
    var s;
    if (v >= 100) s = Math.round(v).toLocaleString("pt-BR");
    else if (v >= 10) s = (Math.round(v * 10) / 10).toLocaleString("pt-BR");
    else s = (Math.round(v * 100) / 100).toLocaleString("pt-BR");
    return s + (unit ? " " + unit : "");
  }

  var $ = function (id) { return document.getElementById(id); };
  var sel = $("c-droga"); if (!sel) return;
  DRUGS.forEach(function (d, i) { var o = document.createElement("option"); o.value = i; o.textContent = d.name + "  —  " + d.ref; sel.appendChild(o); });

  var cur;
  function load() {
    cur = DRUGS[+sel.value];
    $("c-amp-lbl").textContent = cur.ampUnit;
    $("c-amp-mg").value = cur.ampMg; $("c-amp-ml").value = cur.ampMl; $("c-n").value = cur.n; $("c-vol").value = cur.vol;
    $("c-unit").textContent = cur.unit; $("c-dose").value = cur.start; $("c-rate-in").value = "";
    $("c-faixa").innerHTML = "<b>Faixa do protocolo:</b> " + fmt(cur.min) + "–" + fmt(cur.max) + " " + cur.unit + " · <b>Início sugerido:</b> " + fmt(cur.start) + " " + cur.unit;
    $("c-nota").textContent = cur.nota;
    calc();
  }
  // retorna concentração em "unidade da dose por mL" (mcg, mg ou U)
  function conc() {
    var amt = (+$("c-amp-mg").value || 0) * (+$("c-n").value || 0); // em ampUnit
    var vol = +$("c-vol").value || 0;
    if (!vol) return null;
    var doseMass = cur.unit.split("/")[0]; // mcg | mg | U
    var factor = 1;
    if (cur.ampUnit === "mg" && doseMass === "mcg") factor = 1000;
    if (cur.ampUnit === "mcg" && doseMass === "mg") factor = 0.001;
    return { perMl: amt * factor / vol, mass: doseMass, ampTotal: amt };
  }
  function rateFromDose(dose, kg, c) {
    var perKg = cur.unit.indexOf("/kg") >= 0, perMin = /min$/.test(cur.unit);
    var perH = dose * (perKg ? kg : 1) * (perMin ? 60 : 1); // massa por hora
    return perH / c.perMl;
  }
  function calc() {
    var kg = +$("c-peso").value || 0, c = conc();
    var doseMass = cur.unit.split("/")[0];
    if (!c || !kg) { $("c-conc").textContent = "—"; $("c-rate").textContent = "—"; return; }
    $("c-conc").textContent = fmt(c.perMl) + " " + doseMass + "/mL  (" + fmt(c.ampTotal) + " " + cur.ampUnit + " em " + $("c-vol").value + " mL)";
    var dose = +$("c-dose").value;
    if (dose > 0) {
      var r = rateFromDose(dose, kg, c);
      $("c-rate").textContent = fmt(r) + " mL/h";
      $("c-rate").className = (dose < cur.min || dose > cur.max) ? "warn" : "";
      $("c-rate").title = (dose < cur.min || dose > cur.max) ? "Fora da faixa do protocolo" : "";
    } else $("c-rate").textContent = "—";
    var rin = +$("c-rate-in").value;
    if (rin > 0) {
      var perKg = cur.unit.indexOf("/kg") >= 0, perMin = /min$/.test(cur.unit);
      var d = rin * c.perMl / (perKg ? kg : 1) / (perMin ? 60 : 1);
      $("c-dose-out").textContent = fmt(d) + " " + cur.unit + ((d < cur.min || d > cur.max) ? "  (fora da faixa)" : "");
    } else $("c-dose-out").textContent = "—";
    // tabela
    var steps = [], lo = cur.min, hi = cur.max, nS = 6;
    for (var i = 0; i <= nS; i++) steps.push(lo + (hi - lo) * i / nS);
    var h = "<tr><th>Dose (" + cur.unit + ")</th><th>mL/h</th></tr>";
    steps.forEach(function (s) { h += "<tr><td>" + fmt(s) + "</td><td><b>" + fmt(rateFromDose(s, kg, c)) + "</b></td></tr>"; });
    $("c-table").innerHTML = h;
    bolus();
  }
  function bolus() {
    var kg = +$("c-peso").value || 0, age = +($("b-idade") && $("b-idade").value) || 0, scq = +($("b-scq") && $("b-scq").value) || 0;
    var h = "";
    BOLUS.forEach(function (g) {
      h += '<tr><th colspan="3">' + g.g + "</th></tr>";
      g.items.forEach(function (it) {
        var v; try { v = kg ? it.f(kg, age, scq) : "—"; } catch (e) { v = "—"; }
        h += "<tr><td>" + it.n + "</td><td><b>" + v + "</b></td><td class=\"small\">Prot. " + it.ref + "</td></tr>";
      });
    });
    $("b-table").innerHTML = h;
  }
  ["c-peso", "c-amp-mg", "c-amp-ml", "c-n", "c-vol", "c-dose", "c-rate-in", "b-idade", "b-scq"].forEach(function (id) { var el = $(id); if (el) el.addEventListener("input", calc); });
  sel.addEventListener("change", load);
  // droga por hash (#nora)
  var hid = (location.hash || "").replace("#", "");
  DRUGS.forEach(function (d, i) { if (d.id === hid) sel.value = i; });
  load();
})();
