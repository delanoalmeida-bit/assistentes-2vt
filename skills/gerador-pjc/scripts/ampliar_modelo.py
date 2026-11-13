"""Acrescenta ao modelo reduzido os protótipos de horas extras, verba sobre histórico e reflexos,
tirados de um cálculo exportado (ex.: 108996). Uso: python3 -I ampliar_modelo.py MODELO.PJC REF.PJC SAIDA.PJC"""
import sys, copy, hashlib
sys.path.insert(0, __file__.rsplit('/', 1)[0] if '/' in __file__ else '.')
import pjcio
m = pjcio.load(sys.argv[1]); ref = pjcio.load(sys.argv[2])
QUER = {'HORAS EXTRAS 50%': 'PROTO HORAS EXTRAS', 'DIFERENÇA SALARIAL': 'PROTO VERBA SOBRE HISTORICO',
        'REPOUSO SEMANAL REMUNERADO E FERIADO SOBRE HORAS EXTRAS 50%': 'PROTO REFLEXO RSR',
        'AVISO PRÉVIO SOBRE HORAS EXTRAS 50%': 'PROTO REFLEXO AVISO',
        'FÉRIAS + 1/3 SOBRE HORAS EXTRAS 50%': 'PROTO REFLEXO FERIAS',
        '13º SALÁRIO SOBRE HORAS EXTRAS 50%': 'PROTO REFLEXO DECIMO',
        'MULTA DO ARTIGO 467 DA CLT SOBRE AVISO PRÉVIO': 'PROTO REFLEXO MULTA 467'}
achados = {}
for e in ref.iter():
    n = (e.findtext('nome') or '').strip()
    if e.tag in ('Calculada', 'Reflexo') and n in QUER and e.find('ativo') is not None and n not in achados:
        achados[n] = copy.deepcopy(e)
assert len(achados) == len(QUER), set(QUER) - set(achados)
vset = m.find('verbas/Set')
for n, v in achados.items():
    L = v.find('ocorrencias/List')
    for c in list(L)[1:]: L.remove(c)
    # base de reflexo: só referência (a definição completa da base fica fora)
    for it in v.iter('ItemBaseVerba'):
        vc = it.find('verbaDeCalculo'); b = vc[0]; rid = b.findtext('id') or b.findtext('internalRef')
        vc.remove(b); nb = type(b)(b.tag); r = type(b)('internalRef'); r.text = rid; nb.append(r); vc.append(nb)
    for h in v.iter('HistoricoSalarialDaVerba'):
        hs = h.find('historicoSalarial'); b = hs[0]; rid = b.findtext('id') or b.findtext('internalRef')
        hs.remove(b); nb = type(b)(b.tag); r = type(b)('internalRef'); r.text = rid; nb.append(r); hs.append(nb)
    v.find('nome').text = QUER[n]
    vset.append(v)
data = pjcio.save(m, sys.argv[3], 'MODELO_GERADOR_PJC.xml')
print('xml', len(data), 'sha256', hashlib.sha256(data).hexdigest())
