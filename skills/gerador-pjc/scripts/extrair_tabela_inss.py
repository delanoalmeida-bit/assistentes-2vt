"""Extrai de um PJC exportado do PJe-Calc a tabela mensal (teto e alíquota do segurado) que o sistema
grava nas ocorrências da contribuição social. Uso: python3 -I extrair_tabela_inss.py CALCULO.PJC"""
import sys, datetime
sys.path.insert(0, __file__.rsplit('/', 1)[0] if '/' in __file__ else '.')
import pjcio
r = pjcio.load(sys.argv[1])
ins = r.find('inss/Inss')
occ = list(ins.find('inssSobreSalariosPagos/InssSobreSalariosPagos/ocorrencias/Set')) + \
      list(ins.find('inssSobreSalariosDevidos/InssSobreSalariosDevidos/ocorrencias/Set'))
mes = {}
for o in occ:
    if o.findtext('ocorrenciaDecimoTerceiro') == 'true': continue
    dd = datetime.datetime.fromtimestamp(int(o.findtext('dataOcorrenciaInss')) / 1000, datetime.timezone(datetime.timedelta(hours=-3)))
    mes[(dd.year, dd.month)] = (o.findtext('valorTetoSegurado'), o.findtext('aliquotaSegurado'))
ks = sorted(mes); out = []; prev = None
for k in ks:
    if mes[k] != prev: out.append((k, *mes[k])); prev = mes[k]
print('TABELA_INSS_INICIO = (%d, %d)' % ks[0]); print('TABELA_INSS_FIM = (%d, %d)' % ks[-1])
print('TABELA_INSS = [' + ', '.join("((%d, %d), '%s', '%s')" % (y, m, t, a) for (y, m), t, a in out) + ']')
