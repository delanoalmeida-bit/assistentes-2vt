"""Compara verbas ativas de dois PJC pelo nome: parâmetros e ocorrências (ignora ids e resultados)."""
import sys, datetime
sys.path.insert(0, __file__.rsplit('/', 1)[0] if '/' in __file__ else '.')
import pjcio
tz = datetime.timezone(datetime.timedelta(hours=-3))
def d(x):
    try: return datetime.datetime.fromtimestamp(int(x) / 1000, tz).strftime('%d/%m/%y')
    except: return x
RES = {'devido', 'devidoIntegral', 'base', 'baseIntegral', 'indiceAcumulado', 'id', 'versao', 'internalRef', 'ordem'}
def carregar(p):
    r = pjcio.load(p); byid = {}
    for e in r.iter():
        if e.tag in ('Calculada', 'Reflexo', 'Informada') and e.find('nome') is not None: byid[e.findtext('id')] = e
    hist = {h.findtext('id'): h.findtext('nome') for h in r.find('historicosSalariais/Set')}
    out = {}
    for e in byid.values():
        if e.findtext('ativo') != 'true': continue
        nome = e.findtext('nome').strip(); f = {}
        def walk(x, p):
            for c in x:
                if c.tag in ('ocorrencias', 'calculo'): continue
                if c.tag in ('Calculada', 'Reflexo', 'Informada') and p:
                    ref = c.findtext('internalRef') or c.findtext('id'); f[p + 'REF'] = byid[ref].findtext('nome').strip() if ref in byid else ref; continue
                if c.tag == 'HistoricoSalarial': f[p + 'HIST'] = hist.get(c.findtext('internalRef') or c.findtext('id')); continue
                if len(c): walk(c, p + c.tag + '/')
                elif c.tag not in RES: f[p + c.tag] = d(c.text) if c.tag.startswith(('periodo', 'data')) else c.text
        walk(e, '')
        oc = []
        for o in e.find('ocorrencias/List'):
            oc.append(tuple((k, d(o.findtext(k)) if k.startswith('data') else o.findtext(k)) for k in
                      ('dataInicial', 'dataFinal', 'divisor', 'multiplicador', 'quantidade', 'quantidadeIntegral', 'pago', 'valor', 'ativo',
                       'dataInicialPeriodoAquisitivo', 'dataFinalPeriodoAquisitivo', 'feriasIndenizadas', 'caracteristica', 'ocorrenciaDePagamento')))
        out[nome] = (e.tag, f, oc)
    return out
A, B = carregar(sys.argv[1]), carregar(sys.argv[2])
print('só no gerado:', sorted(set(A) - set(B))); print('só na referência:', sorted(set(B) - set(A)))
for n in sorted(set(A) & set(B)):
    ta, fa, oa = A[n]; tb, fb, ob = B[n]; dif = []
    if ta != tb: dif.append(('tag', ta, tb))
    for k in sorted(set(fa) | set(fb)):
        if fa.get(k) != fb.get(k): dif.append((k, fa.get(k), fb.get(k)))
    if oa != ob:
        if len(oa) != len(ob): dif.append(('n ocorrências', len(oa), len(ob)))
        for x, y in zip(oa, ob):
            if x != y: dif.append(('ocorrência', [kv for kv in x if kv not in y], [kv for kv in y if kv not in x]))
    print('==', n, 'OK' if not dif else '')
    for x in dif[:12]: print('    ', x)
