"""Resumo estrutural de um PJC para montar a ficha. Uso: python3 -I dump_calc.py CALC.PJC"""
import sys, datetime
sys.path.insert(0, __file__.rsplit('/', 1)[0] if '/' in __file__ else '.')
import pjcio
tz = datetime.timezone(datetime.timedelta(hours=-3))
def d(x):
    try: return datetime.datetime.fromtimestamp(int(x)/1000, tz).strftime('%d/%m/%Y')
    except: return x
r = pjcio.load(sys.argv[1])
print('RAIZ:', {k: (d(r.findtext(k)) if k.startswith('data') else r.findtext(k)) for k in ('dataAdmissao','dataDemissao','dataAjuizamento','dataInicioCalculo','dataTerminoCalculo','dataDeLiquidacao','valorUltimaRemuneracao','valorMaiorRemuneracao','valorCargaHorariaPadrao','projetaAvisoIndenizado','prescricaoQuinquenal','prescricaoFgts','consideraFeriadoEstadual','consideraFeriadoMunicipal','comentarios')})
hist = {}
for h in r.find('historicosSalariais/Set'):
    hist[h.findtext('id')] = h.findtext('nome')
    oc = h.find('ocorrencias/List')
    vals = sorted({o.findtext('valor') for o in oc})
    print('HIST', h.findtext('nome'), h.findtext('tipoVariacaoParcela'), 'fgts', h.findtext('incidenciaFGTS'), h.findtext('aplicarProporcionalidadeFGTS'), 'inss', h.findtext('incidenciaINSS'), len(oc), 'oc', d(oc[0].findtext('dataOcorrencia')), d(oc[-1].findtext('dataOcorrencia')), vals[:5])
for f in r.find('listaDeFerias/Set'):
    print('FERIAS', f.findtext('relativa'), f.findtext('situacao'), f.findtext('prazo'))
byid = {}
for e in r.iter():
    if e.tag in ('Calculada','Informada','Reflexo') and e.find('ativo') is not None: byid[e.findtext('id')] = e
listed = [v for v in r.find('verbas/Set') if v.tag != 'internalRef']
nomes = {v.findtext('nome') for v in listed}
extra = [e for e in byid.values() if e.findtext('nome') not in nomes]
print('VERBAS SO ANINHADAS:', [e.findtext('nome') for e in extra], 'refs vazias no Set:', sum(1 for v in r.find('verbas/Set') if v.tag == 'internalRef' and not v.text))
for v in listed + extra:
    print('\n== VERBA', v.tag, repr(v.findtext('nome')), 'ativo', v.findtext('ativo'), d(v.findtext('periodoInicial')), d(v.findtext('periodoFinal')))
    print('   inc FGTS/INSS/IR', v.findtext('incidenciaFGTS'), v.findtext('incidenciaINSS'), v.findtext('incidenciaIRPF'), 'pag', v.findtext('ocorrenciaDePagamento'), 'carac', v.findtext('caracteristica'), 'var', v.findtext('tipoVariacaoParcela'), 'prop', v.findtext('aplicarProporcionalidade'), 'cnj', v.findtext('assuntoCnj/AssuntoCnj/externalRef'))
    fc = v.find('formula')[0] if v.find('formula') is not None and len(v.find('formula')) else None
    if fc is not None:
        info = {}
        for t in ('divisor/Divisor/tipo','divisor/Divisor/outroValor','multiplicador/Multiplicador/outroValor','quantidade/Quantidade/tipo','quantidade/Quantidade/valorInformado','quantidade/Quantidade/aplicarProporcionalidade','baseTabelada/BaseTabelada/tipo'):
            if fc.find(t) is not None: info[t.split('/')[-1] if 'Divisor' not in t else 'div.'+t.split('/')[-1]] = fc.findtext(t)
        print('  ', fc.tag, info)
        for it in fc.iter('ItemBaseVerba'):
            b = it.find('verbaDeCalculo')[0]; rid = b.findtext('internalRef') or b.findtext('id')
            print('   base verba:', byid[rid].findtext('nome') if rid in byid else rid, 'integralizar', it.findtext('integralizar'))
    for hv in v.iter('HistoricoSalarialDaVerba'):
        b = hv.find('historicoSalarial')[0]; rid = b.findtext('internalRef') or b.findtext('id')
        print('   hist:', hist.get(rid, rid), 'prop', hv.findtext('aplicarProporcionalidade'))
    if v.tag == 'Reflexo':
        print('   reflexo:', v.findtext('comportamentoDoReflexo'), v.findtext('periodoMediaReflexo'), v.findtext('tratamentoDaFracaoDeMesDoReflexo'))
    oc = list(v.find('ocorrencias/List'))
    print('   ocorrencias', len(oc))
    for o in oc[:3] + (oc[-2:] if len(oc) > 5 else oc[3:]):
        print('    ', d(o.findtext('dataInicial')), d(o.findtext('dataFinal')), 'div', o.findtext('divisor'), 'mult', o.findtext('multiplicador'), 'q', o.findtext('quantidade'), 'qi', o.findtext('quantidadeIntegral'), o.findtext('valor'), 'dev', o.findtext('devido'), 'pago', o.findtext('pago'), o.findtext('caracteristica'), o.findtext('ocorrenciaDePagamento'), d(o.findtext('dataInicialPeriodoAquisitivo')), d(o.findtext('dataFinalPeriodoAquisitivo')), o.findtext('ativo'))
fg = r.find('fgts/Fgts')
print('\nFGTS', {c.tag: (d(c.text) if c.tag.startswith(('periodo','data')) else c.text) for c in fg if not len(c)})
print('FGTS oc', len(fg.find('ocorrencias/Set')))
ins = r.find('inss/Inss')
print('INSS', {c.tag: c.text for c in ins if not len(c)})
for t in ('inssSobreSalariosDevidos/InssSobreSalariosDevidos','inssSobreSalariosPagos/InssSobreSalariosPagos'):
    x = ins.find(t); print(t.split('/')[0], d(x.findtext('dataInicioPeriodo')), d(x.findtext('dataTerminoPeriodo')), len(x.find('ocorrencias/Set')))
for m in r.find('multas/Set'): print('MULTA', {c.tag: (d(c.text) if 'data' in c.tag.lower() else c.text) for c in m if not len(c)})
for h in r.find('honorarios/Set'): print('HON', {c.tag: c.text for c in h if not len(c)})
cu = r.find('custasJudiciais/CustasJudiciais'); print('CUSTAS', {c.tag: c.text for c in cu if not len(c)})
pa = r.find('parametrosDeAtualizacao/ParametrosDeAtualizacao'); print('ATUAL', {c.tag: (d(c.text) if 'apartir' in c.tag.lower() else c.text) for c in pa if not len(c)})
for c in pa.find('listaDeCombinacaoDeIndices/Set'): print('  ind', c.findtext('outroIndiceTrabalhista'), d(c.findtext('apartirDeOutroIndice')))
for c in pa.find('listaDeCombinacaoDeJuros/Set'): print('  jur', c.findtext('outroJuros'), d(c.findtext('apartirDeOutroJuros')))
ir = r.find('irpf/Irpf'); print('IR', {c.tag: (d(c.text) if c.tag.startswith('data') else c.text) for c in ir if not len(c)})
sd = r.find('seguroDesemprego/SeguroDesemprego'); print('SD', sd.findtext('apurarSeguroDesemprego'))
