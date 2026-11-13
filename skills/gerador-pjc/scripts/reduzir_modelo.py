"""Uso: python3 -I reduzir_modelo.py CALCULO_EXPORTADO.PJC MODELO_GERADOR_PJC.PJC"""
import sys, copy, hashlib
sys.path.insert(0, __file__.rsplit('/', 1)[0] if '/' in __file__ else '.')
import pjcio
r = pjcio.load(sys.argv[1])
for t in ('gprec', 'dadosEstruturados'):
    e = r.find(t)
    if e is not None: r.remove(e)
r.find('hashCodeLiquidacao').text = 'null'
for t in ('apuracoesDeJuros', 'historicosValidacao', 'historicosValidacaoAtualizacao'):
    for s in r.find(t): s.clear()
r.find('comentarios').text = 'null'
def trim(lst, keep=1):
    for c in list(lst)[keep:]: lst.remove(c)
need = {'AVISO PRÉVIO', 'FÉRIAS + 1/3', 'MULTA DO ARTIGO 477 DA CLT', 'SALDO DE SALÁRIO', '13º SALÁRIO', 'DEVOLUÇÃO DE DESCONTOS INDEVIDOS'}
vset = r.find('verbas/Set'); defs = {}
for e in r.iter():
    if e.tag in ('Calculada', 'Informada') and e.find('ativo') is not None:
        defs[(e.findtext('nome') or '').strip()] = e
keep = [copy.deepcopy(defs[n]) for n in sorted(need)]
for v in list(vset): vset.remove(v)
for v in keep:
    trim(v.find('ocorrencias/List')); vset.append(v)
for h in r.find('historicosSalariais/Set'): trim(h.find('ocorrencias/List'))
trim(r.find('fgts/Fgts/ocorrencias/Set'))
trim(r.find('inss/Inss/inssSobreSalariosDevidos/InssSobreSalariosDevidos/ocorrencias/Set'))
r.find('irpf/Irpf/ocorrencias/Set').clear()
r.find('fgts/Fgts/operacoesDeFgts/Set').clear()
P = r.find('processo/Processo')
for e in P.iter():
    if e.tag == 'nome' and e.text: e.text = 'MODELO'
    if e.tag in ('numeroDocumentoFiscal', 'numeroDocumento', 'numeroOAB', 'numeroDocumentoPrevidenciario') and e.text and e.text != 'null': e.text = '0'
    if e.tag in ('numero', 'valorDaCausa'): e.text = '0'
for h in r.find('honorarios/Set'):
    h.find('nomeCredor').text = 'MODELO'; h.find('numeroDocumentoFiscalCredor').text = '00000000000'
r.find('usuarioCriador').text = '0'
data = pjcio.save(r, sys.argv[2], 'MODELO_GERADOR_PJC.xml')
print('xml', len(data), 'sha256', hashlib.sha256(data).hexdigest())
