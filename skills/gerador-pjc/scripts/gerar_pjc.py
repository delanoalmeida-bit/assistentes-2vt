"""Gerador de arquivo .PJC (PJe-Calc 2.16) a partir de um modelo exportado + ficha JSON.

Uso: python3 gerar_pjc.py MODELO.PJC FICHA.json PROCESSO_SRC.PJC SAIDA.PJC

- MODELO: cálculo exportado que fornece os protótipos dos elementos (estrutura).
- FICHA: dados do caso (todos os valores vêm daqui).
- PROCESSO_SRC: PJC exportado do cálculo criado no PJe-Calc via "Obter do PJe"; dele só se
  copia o bloco <processo> (identificação do processo, partes e advogados).
"""
import sys, copy, json, datetime, calendar
from decimal import Decimal, ROUND_HALF_UP
import xml.etree.ElementTree as ET
sys.path.insert(0, __file__.rsplit('/', 1)[0] if '/' in __file__ else '.')
import pjcio
import calendario

# ---------------------------------------------------------------- utilidades
def ms(data):
    """'dd/mm/aaaa' -> milissegundos epoch à meia-noite de Brasília (UTC-3)."""
    if data is None: return 'null'
    d = datetime.datetime.strptime(data, '%d/%m/%Y').replace(tzinfo=datetime.timezone.utc)
    return str(int(d.timestamp() * 1000) + 3 * 3600 * 1000)

def ms_d(d): return ms(d.strftime('%d/%m/%Y'))
def dt(s): return datetime.datetime.strptime(s, '%d/%m/%Y').date()
def comp(s):  # 'mm/aaaa' -> date (1º dia)
    m, a = s.split('/'); return datetime.date(int(a), int(m), 1)
def meses(ini, fim):
    d = datetime.date(ini.year, ini.month, 1)
    while d <= fim:
        yield d
        d = datetime.date(d.year + (d.month == 12), d.month % 12 + 1, 1)
def ultimo_dia(d): return datetime.date(d.year, d.month, calendar.monthrange(d.year, d.month)[1])
def num(v):
    if v is None: return 'null'
    s = ('%.2f' % v).rstrip('0').rstrip('.')
    return s
def numq(v):  # quantidades: até 10 casas (o sistema grava as proporcionais com muitas casas)
    if v is None: return 'null'
    return ('%.10f' % v).rstrip('0').rstrip('.')
def data_ms(x):  # inverso de ms(): texto em ms -> date
    return (datetime.datetime(1970, 1, 1) + datetime.timedelta(milliseconds=int(x) - 3 * 3600 * 1000)).date()

def setf(e, tag, val):
    c = e.find(tag)
    if c is None: raise KeyError(f'{e.tag} sem campo {tag}')
    c.text = val

class Ids:
    """Alocador de ids novos, sem colisão com os existentes no modelo."""
    def __init__(self, root):
        mx = 0
        for e in root.iter('id'):
            if e.text and e.text.isdigit(): mx = max(mx, int(e.text))
        self.n = max(mx, 90_000_000) + 1000
    def __call__(self):
        self.n += 1; return str(self.n)

def ref(tag, rid):
    e = ET.Element(tag); r = ET.SubElement(e, 'internalRef'); r.text = rid; return e

# contribuição social: tabela mensal do PJe-Calc (gerada por extrair_tabela_inss.py; não editar à mão)
TABELA_INSS_INICIO = (2010, 1)
TABELA_INSS_FIM = (2026, 10)
# meses avulsos fora da tabela extraída (teto do segurado = teto do salário de contribuição × 11%; alíquota da 1ª faixa, recalculada pelo sistema)
TABELA_INSS_EXTRA = {(2004, 11): ('275.96', '7.65')}  # teto R$ 2.508,72 a partir de 05/2004 (caso Exemplo 13)
TABELA_INSS = [((2010, 1), '375.82', '8'), ((2010, 6), '381.41', '8'), ((2011, 1), '405.86', '8'), ((2011, 7), '406.09', '8'), ((2012, 1), '430.78', '8'), ((2013, 1), '457.49', '8'), ((2014, 1), '482.93', '8'), ((2015, 1), '513.01', '8'), ((2016, 1), '570.88', '8'), ((2017, 1), '608.44', '8'), ((2018, 1), '621.04', '8'), ((2019, 1), '642.34', '8'), ((2020, 1), '671.12', '8'), ((2020, 3), '713.1', '7.5'), ((2021, 1), '751.99', '7.5'), ((2022, 1), '828.39', '7.5'), ((2023, 1), '877.24', '7.5'), ((2023, 5), '876.98', '7.5'), ((2024, 1), '908.86', '7.5'), ((2025, 1), '951.63', '7.5'), ((2026, 1), '988.09', '7.5')]

# ---------------------------------------------------------------- gerador
LIMITE_NOME_VERBA = 45  # verbas não reflexas (nome também vai em `descricao`): 67 caracteres derrubou a importação
                        # (Exemplo 05, 03/11/2026); 44 e 45 importaram. Limite exato entre 46 e 66, não medido.
                        # Reflexos não gravam `descricao` e importaram com até 74 (Exemplo 03).

def _aniversarios_ok(a0, a1, adm, dem, fim_proj):
    """Período aquisitivo de férias aceito pelo sistema: começa num aniversário da admissão e termina
    na véspera do aniversário seguinte, na demissão ou no fim do aviso projetado (Exemplo 05, 03/11/2026)."""
    if (a0.day, a0.month) != (adm.day, adm.month) and a0 != adm:
        return False
    try: prox = a0.replace(year=a0.year + 1)
    except ValueError: prox = a0.replace(year=a0.year + 1, day=28)
    return a1 in (prox - datetime.timedelta(days=1), dem) or (fim_proj is not None and a1 == fim_proj)

def conferir_selic(CO, ajuiz):
    """ADC 58: a partir do ajuizamento, a SELIC engloba correção e juros. Combinações válidas no mesmo período:
    índice SELIC com SEM_JUROS, ou SEM_CORRECAO com juros SELIC. Recusa SELIC somada a outro índice ou a outros juros
    (Exemplo 05 e Exemplo 04: índice SELIC + juros SELIC; Exemplo 03: IPCA-E + juros SELIC). Devolve a mensagem ou None."""
    if not CO: return None
    ci = sorted(((dt(d), i) for i, d in CO.get('combinacoes_indice', [[CO.get('outro_indice'), CO.get('outro_a_partir')]]) if d),
                key=lambda x: x[0])
    cj = sorted(((dt(d), j) for j, d in CO.get('combinacoes_juros', []) if d), key=lambda x: x[0])
    def em(seq, base, d):
        v = base
        for d0, x in seq:
            if d0 <= d: v = x
        return v
    marcos = sorted({ajuiz} | {d for d, _ in ci + cj if d >= ajuiz})
    for m in marcos:
        d = m + datetime.timedelta(days=1)  # ignora o dia de diferença entre o índice (ajuizamento) e os juros (dia seguinte)
        i, j = em(ci, CO.get('indice'), d), em(cj, CO.get('juros'), d)
        if i == 'SELIC' and j not in (None, 'SEM_JUROS'):
            return (f'em {d:%d/%m/%Y} o índice é SELIC e os juros são {j}: o sistema soma as duas taxas. '
                    'Com o índice SELIC, os juros do período são SEM_JUROS (ADC 58).')
        if j in ('SELIC', 'SELIC_FAZENDA') and i not in (None, 'SEM_CORRECAO'):
            return (f'em {d:%d/%m/%Y} os juros são {j} e o índice é {i}: a SELIC já engloba a correção. '
                    'Com juros SELIC, o índice do período é SEM_CORRECAO (ADC 58).')
    return None

def validar_ficha(F):
    """Barra erros que o PJe-Calc só acusa na importação ou na liquidação (ver references/licoes_e_casos.md)."""
    C = F['contrato']; erros = []
    adm, dem = dt(C['admissao']), dt(C['demissao'])
    fim_proj = None
    if C.get('projetar_aviso') and C.get('aviso_dias'):
        fim_proj = dt(C['fim_projetado']) if C.get('fim_projetado') else dem + datetime.timedelta(days=C['aviso_dias'])
    for V in F['verbas']:
        nome = V.get('nome')
        if nome and V['tipo'] != 'REFLEXO' and len(nome) > LIMITE_NOME_VERBA:
            erros.append(f'nome de verba com {len(nome)} caracteres (máximo {LIMITE_NOME_VERBA}): {nome}')
        pers = []
        if V['tipo'] == 'FERIAS': pers = V['periodos_indenizados']
        elif V['tipo'] == 'REFLEXO' and V['reflexo'] == 'FERIAS': pers = V['periodos']
        for per in pers:
            if not _aniversarios_ok(dt(per[0]), dt(per[1]), adm, dem, fim_proj):
                erros.append(f'período aquisitivo {per[0]} a {per[1]} ({nome or V["tipo"]}) não é um dos que o sistema monta '
                             f'a partir da admissão; a liquidação recusa ("período aquisitivo ... diferente do gravado na página Férias")')
    CO = F.get('correcao') or {}
    erro_selic = conferir_selic(CO, dt(C['ajuizamento']))
    if erro_selic and not CO.get('permitir_selic_dupla'):
        erros.append(erro_selic + ' Só para reproduzir um cálculo de referência que tenha essa combinação: '
                     '"permitir_selic_dupla": true em correcao')
    if erros:
        raise ValueError('ficha recusada:\n- ' + '\n- '.join(erros))

def gerar(modelo, ficha, proc_src):
    root = pjcio.load(modelo)
    F = ficha; C = F['contrato']
    validar_ficha(F)
    ids = Ids(root)
    calc_id = root.findtext('id')

    # 1. remove resultados (testes E/F: o sistema recalcula)
    for t in ('gprec', 'dadosEstruturados'):
        e = root.find(t)
        if e is not None: root.remove(e)
    setf(root, 'hashCodeLiquidacao', 'null')
    for s in root.find('apuracoesDeJuros'): s.clear()
    # histórico de validação pertence ao cálculo-modelo, não ao novo cálculo
    for t in ('historicosValidacao', 'historicosValidacaoAtualizacao'):
        for s in root.find(t): s.clear()

    # 2. dados do cálculo
    setf(root, 'dataAdmissao', ms(C['admissao']))
    setf(root, 'dataDemissao', ms(C['demissao']))
    setf(root, 'dataAjuizamento', ms(C['ajuizamento']))
    setf(root, 'valorUltimaRemuneracao', num(C['ultima_remuneracao']))
    setf(root, 'valorMaiorRemuneracao', num(C['maior_remuneracao']))
    setf(root, 'dataInicioCalculo', 'null'); setf(root, 'dataTerminoCalculo', 'null')
    setf(root, 'valorCargaHorariaPadrao', num(C['carga_horaria']))
    setf(root, 'projetaAvisoIndenizado', 'true' if C['projetar_aviso'] else 'false')
    setf(root, 'prescricaoFgts', 'true' if C['prescricao_fgts'] else 'false')
    setf(root, 'prescricaoQuinquenal', 'true' if C['prescricao_quinquenal'] else 'false')
    # O PJe-Calc recusa a importação inteira se o comentário for longo demais (teste 01/11/2026:
    # 242 caracteres importou; 450 não). O limite exato não foi medido; 255 é o teto adotado.
    if C['comentarios'] and len(C['comentarios']) > 255:
        raise ValueError(f"comentário com {len(C['comentarios'])} caracteres; o máximo aceito é 255")
    setf(root, 'comentarios', C['comentarios'] or 'null')
    # datas de criação e de liquidação: da ficha ou do dia da geração (o modelo traz as dele)
    hoje = datetime.date.today().strftime('%d/%m/%Y')
    setf(root, 'dataCriacao', ms(hoje))
    setf(root, 'dataDeLiquidacao', ms(F.get('data_liquidacao') or hoje))

    # 3. processo (partes e advogados) do cálculo criado pelo "Obter do PJe"
    src = pjcio.load(proc_src)
    i = list(root).index(root.find('processo'))
    root.remove(root.find('processo'))
    root.insert(i, copy.deepcopy(src.find('processo')))
    if src.find('usuarioCriador') is not None:
        setf(root, 'usuarioCriador', src.findtext('usuarioCriador'))

    # 4. históricos salariais
    hset = root.find('historicosSalariais/Set')
    proto_h = [h for h in hset if h.findtext('nome') == 'ÚLTIMA REMUNERAÇÃO'][0]
    proto_ho = proto_h.find('ocorrencias/List')[0]
    for h in list(hset): hset.remove(h)
    hist_ids = {}

    def novo_hist(nome, fixa, fgts, inss, prop_fgts, prop_inss, valores):
        h = copy.deepcopy(proto_h); hid = ids(); hist_ids[nome] = hid
        setf(h, 'id', hid); setf(h, 'versao', '0'); setf(h, 'nome', nome)
        setf(h, 'tipoVariacaoParcela', 'FIXA' if fixa else 'VARIAVEL')
        setf(h, 'incidenciaFGTS', str(fgts).lower()); setf(h, 'aplicarProporcionalidadeFGTS', str(prop_fgts).lower())
        setf(h, 'incidenciaINSS', str(inss).lower()); setf(h, 'aplicarProporcionalidadeINSS', str(prop_inss).lower())
        L = h.find('ocorrencias/List'); L.clear()
        for d, v in valores:
            o = copy.deepcopy(proto_ho)
            setf(o, 'id', ids()); setf(o, 'versao', '0'); setf(o, 'dataOcorrencia', ms_d(d)); setf(o, 'valor', num(v))
            setf(o, 'recolhidoFGTS', 'false'); setf(o, 'recolhidoINSS', 'false')
            setf(o, 'incidenciaFGTS', str(fgts).lower()); setf(o, 'incidenciaINSS', str(inss).lower())
            o.find('historicoSalarial/HistoricoSalarial/internalRef').text = hid
            L.append(o)
        hset.append(h)

    HU = F['historicos'].get('ultima_remuneracao')  # opcional (o 121044 não tem)
    if HU:
        novo_hist('ÚLTIMA REMUNERAÇÃO', True, HU['fgts'], HU['inss'], False, False,
                  [(d, HU['valor']) for d in meses(comp(HU['inicio']), comp(HU['fim']))])
    fichas_extra = {k: v for k, v in F['historicos'].items() if k != 'ultima_remuneracao'}
    for nome, H in fichas_extra.items():
        vals = {}
        for a, b, v in H['faixas']:
            for d in meses(comp(a), comp(b)): vals[d] = v
        for ano, v13 in H.get('decimo_terceiro_nov_dez', {}).items():
            # adiantamento (novembro) arredonda para cima no meio centavo; dezembro leva o resto
            meio = float((Decimal(str(v13)) / 2).quantize(Decimal('0.01'), ROUND_HALF_UP))
            vals[datetime.date(int(ano), 11, 1)] = round(vals[datetime.date(int(ano), 11, 1)] + meio, 2)
            vals[datetime.date(int(ano), 12, 1)] = round(vals[datetime.date(int(ano), 12, 1)] + round(v13 - meio, 2), 2)
        novo_hist(nome, H.get('fixa', False), H['fgts'], H['inss'], H.get('proporcionalizar_fgts', False), H.get('proporcionalizar_inss', False), sorted(vals.items()))

    # 5. férias
    fset = root.find('listaDeFerias/Set'); proto_f = fset[0]
    for f in list(fset): fset.remove(f)
    for P in F['ferias']:
        f = copy.deepcopy(proto_f); a0, a1 = dt(P['aquisitivo'][0]), dt(P['aquisitivo'][1])
        c0 = a1 + datetime.timedelta(days=1)
        c1 = datetime.date(c0.year + 1, c0.month, c0.day) - datetime.timedelta(days=1)
        setf(f, 'id', ids()); setf(f, 'versao', '0'); setf(f, 'relativa', P['relativa'])
        setf(f, 'dataInicialDoPeriodoAquisitivo', ms_d(a0)); setf(f, 'dataFinalDoPeriodoAquisitivo', ms_d(a1))
        setf(f, 'dataInicialDoPeriodoConcessivo', ms_d(c0)); setf(f, 'dataFinalDoPeriodoConcessivo', ms_d(c1))
        setf(f, 'prazo', '30'); setf(f, 'situacao', P['situacao']); setf(f, 'dobraGeral', 'false')
        setf(f, 'abono', 'false'); setf(f, 'quantidadeDiasAbono', '10')
        g = P.get('gozo') or [None, None]
        setf(f, 'dataInicialDoPeriodoDeGozo1', ms(g[0])); setf(f, 'dataFinalDoPeriodoDeGozo1', ms(g[1]))
        setf(f, 'dobraDoPeriodoDeGozo1', 'false')
        for k in (2, 3):
            setf(f, f'dataInicialDoPeriodoDeGozo{k}', 'null'); setf(f, f'dataFinalDoPeriodoDeGozo{k}', 'null')
            setf(f, f'dobraDoPeriodoDeGozo{k}', 'false')
        fset.append(f)

    gozos = [(dt(P['gozo'][0]), dt(P['gozo'][1])) for P in F['ferias'] if P.get('gozo')]
    def dias_gozo(a, b):  # dias de [a, b] dentro de períodos de férias gozadas
        return sum(max(0, (min(b, g1) - max(a, g0)).days + 1) for g0, g1 in gozos)

    # 6. verbas
    vset = root.find('verbas/Set')
    defs = {}
    for e in root.iter():
        if e.tag in ('Calculada', 'Informada', 'Reflexo') and e.find('ativo') is not None:
            defs[(e.findtext('nome') or '').strip()] = e
    P_AVISO, P_FERIAS, P_477 = defs['AVISO PRÉVIO'], defs['FÉRIAS + 1/3'], defs['MULTA DO ARTIGO 477 DA CLT']
    P_SALDO, P_13 = defs['SALDO DE SALÁRIO'], defs['13º SALÁRIO']
    P_INF = defs.get('DEVOLUÇÃO DE DESCONTOS INDEVIDOS')
    proto_oc = P_SALDO.find('ocorrencias/List')[0]
    proto_hv = P_SALDO.find('historicosDaVerbaDoValorDevido/List')[0]
    for v in list(vset): vset.remove(v)

    dem = dt(C['demissao']); ini_presc = dt(C.get('marco_prescricional') or C['admissao'])
    ini_mes_dem = datetime.date(dem.year, dem.month, 1)

    def nova_verba(proto, periodo, ordem, **campos):
        v = copy.deepcopy(proto); vid = ids(); old = v.findtext('id')
        # o id da verba se repete na fórmula, no valor pago e nas autorreferências
        for e in v.iter():
            if e.tag in ('id', 'internalRef') and e.text == old: e.text = vid
        setf(v, 'versao', '0')
        dq = ids()
        for t in ('formula/FormulaCalculada/divisor/Divisor/id', 'formula/FormulaCalculada/quantidade/Quantidade/id',
                  'formula/FormulaReflexo/divisor/Divisor/id', 'formula/FormulaReflexo/quantidade/Quantidade/id'):
            if v.find(t) is not None: v.find(t).text = dq
        setf(v, 'periodoInicial', ms_d(periodo[0])); setf(v, 'periodoFinal', ms_d(periodo[1]))
        setf(v, 'ordem', str(ordem)); setf(v, 'ativo', 'true')
        v.find('calculo/Calculo/internalRef').text = calc_id
        for k, val in campos.items(): setf(v, k, val)
        v.find('ocorrencias/List').clear()
        return v, vid

    def ocorr(v, vid, d0, d1, div, mult, qtd, integ, carac, pag, aq=None, indeniz=False, pago=0, devido=None, ativo=True):
        o = copy.deepcopy(proto_oc)
        def fill(x, original):
            setf(x, 'id', ids()); setf(x, 'versao', '0')
            setf(x, 'dataInicial', ms_d(d0)); setf(x, 'dataFinal', ms_d(d1))
            setf(x, 'divisor', num(div)); setf(x, 'multiplicador', str(mult)); setf(x, 'quantidade', numq(qtd))
            setf(x, 'quantidadeIntegral', numq(integ)); setf(x, 'dobra', 'false')
            for t in ('devido', 'devidoIntegral', 'base', 'baseIntegral', 'indiceAcumulado'):
                if x.find(t) is not None: setf(x, t, 'null')
            setf(x, 'pago', num(pago)); setf(x, 'pagoIntegral', num(pago)); setf(x, 'ativo', str(ativo).lower())
            setf(x, 'valor', 'CALCULADO' if devido is None else 'INFORMADO'); setf(x, 'comporPrincipal', 'SIM')
            if devido is not None:
                setf(x, 'devido', num(devido)); setf(x, 'devidoIntegral', num(devido))
            setf(x, 'dataInicialPeriodoAquisitivo', ms_d(aq[0]) if aq else 'null')
            setf(x, 'dataFinalPeriodoAquisitivo', ms_d(aq[1]) if aq else 'null')
            setf(x, 'feriasIndenizadas', 'false' if original else str(indeniz).lower())
            setf(x, 'feriasComAbono', 'false')
            setf(x, 'caracteristica', carac); setf(x, 'ocorrenciaDePagamento', pag)
            vc = x.find('verbaDeCalculo')[0]; vc.tag = v.tag  # Calculada ou Informada, conforme a verba
            vc.find('internalRef').text = vid
        fill(o, False); fill(o.find('ocorrenciaOriginal/OcorrenciaDeVerba'), True)
        v.find('ocorrencias/List').append(o)

    def vinc_hist(v, vid, nome, prop):
        L = v.find('historicosDaVerbaDoValorDevido/List'); L.clear()
        h = copy.deepcopy(proto_hv); setf(h, 'id', ids()); setf(h, 'aplicarProporcionalidade', str(prop).lower())
        h.find('verbaDeCalculo/Calculada/internalRef').text = vid
        h.find('historicoSalarial/HistoricoSalarial/internalRef').text = hist_ids[nome]
        L.append(h)

    def base_hist(v, vid, V):
        # base = histórico salarial nomeado na ficha (ex.: comissões), em vez da maior remuneração
        b = V.get('base')
        if b in (None, 'MAIOR_REMUNERACAO'): return
        setf(v, 'formula/FormulaCalculada/baseTabelada/BaseTabelada/tipo', 'HISTORICO_SALARIAL')
        vinc_hist(v, vid, 'ÚLTIMA REMUNERAÇÃO' if b == 'ULTIMA_REMUNERACAO' else b, False)
        L = v.find('historicosDaVerbaDoValorDevido/List')
        if L[0].find('tipoVinculoHistorico') is not None: setf(L[0], 'tipoVinculoHistorico', 'BASE')

    periodo_geral = (ini_presc, dem)
    ordem = 0
    gerados = {}  # nome -> (verba, id, período): bases para os reflexos
    P_HE, P_VH = defs.get('PROTO HORAS EXTRAS'), defs.get('PROTO VERBA SOBRE HISTORICO')
    P_REF = {k: defs.get('PROTO REFLEXO ' + k.replace('MULTA_467', 'MULTA 467')) for k in ('RSR', 'AVISO', 'FERIAS', 'DECIMO', 'MULTA_467')}
    PREF = {'RSR': 'REPOUSO SEMANAL REMUNERADO E FERIADO', 'AVISO': 'AVISO PRÉVIO', 'FERIAS': 'FÉRIAS + 1/3',
            'DECIMO': '13º SALÁRIO', 'MULTA_467': 'MULTA DO ARTIGO 467 DA CLT'}
    est, mun = root.findtext('consideraFeriadoEstadual') == 'true', root.findtext('consideraFeriadoMunicipal') == 'true'
    def incid(V, padrao):
        return {k: str(V.get(c, padrao[c])).lower() for k, c in (('incidenciaFGTS', 'fgts'), ('incidenciaINSS', 'inss'), ('incidenciaIRPF', 'irpf'))}
    def mensal(p, cada):
        for d in meses(p[0], p[1]):
            a, b = max(d, p[0]), min(ultimo_dia(d), p[1])
            cada(a, b, (b - a).days + 1, a.day == 1 and b == ultimo_dia(d))
    for V in F['verbas']:
        t = V['tipo']
        if t == 'AVISO_PREVIO':
            v, vid = nova_verba(P_AVISO, (dt(V['periodo'][0]), dt(V['periodo'][1])) if V.get('periodo') else periodo_geral, ordem,
                                incidenciaFGTS=str(V.get('fgts', True)).lower(),
                                incidenciaINSS=str(V.get('inss', False)).lower(),
                                incidenciaIRPF=str(V.get('irpf', False)).lower())
            base_hist(v, vid, V)
            q = C['aviso_dias']; ocorr(v, vid, dem, dem, 30, 1, q, q * 30, 'AVISO_PREVIO', 'DESLIGAMENTO')
        elif t == 'FERIAS':
            v, vid = nova_verba(P_FERIAS, periodo_geral, ordem)
            setf(v, 'formula/FormulaCalculada/valorPago/ValorPago/quantidade', 'null')
            base_hist(v, vid, V)
            mf = str(V.get('multiplicador', '1.33333333'))  # o 121044 usa 1.3333
            setf(v, 'formula/FormulaCalculada/multiplicador/Multiplicador/outroValor', mf)
            for per in V['periodos_indenizados']:
                a0, a1, avos = per[:3]; pago = per[3] if len(per) > 3 else 0
                ocorr(v, vid, dem, dem, 12, mf, avos, avos * 30, 'FERIAS', 'PERIODO_AQUISITIVO',
                      aq=(dt(a0), dt(a1)), indeniz=True, pago=pago)
        elif t == 'MULTA_477':
            if V.get('periodo'):
                p = (dt(V['periodo'][0]), dt(V['periodo'][1])); v, vid = nova_verba(P_477, p, ordem)
                base_hist(v, vid, V)
                a = max(p[0], ini_mes_dem); ocorr(v, vid, a, dem, 1, 1, 1, round(30 / ((dem - a).days + 1), 4), 'COMUM', 'DESLIGAMENTO')
            else:
                v, vid = nova_verba(P_477, periodo_geral, ordem)
                ocorr(v, vid, ini_mes_dem, dem, 1, 1, 1, 3, 'COMUM', 'DESLIGAMENTO')
        elif t == 'SALDO_SALARIO':
            p = (dt(V['periodo'][0]), dt(V['periodo'][1]))
            v, vid = nova_verba(P_SALDO, p, ordem, incidenciaFGTS=str(V['fgts']).lower())
            setf(v, 'formula/FormulaCalculada/divisor/Divisor/outroValor', '1')
            setf(v, 'formula/FormulaCalculada/quantidade/Quantidade/valorInformado', '1')
            vinc_hist(v, vid, 'ÚLTIMA REMUNERAÇÃO', V.get('proporcionalizar', True))
            ocorr(v, vid, p[0], p[1], 1, 1, 1, 3, 'COMUM', 'DESLIGAMENTO')
        elif t == 'DECIMO_TERCEIRO':
            p = (dt(V['periodo'][0]), dt(V['periodo'][1]))
            v, vid = nova_verba(P_13, p, ordem, incidenciaFGTS=str(V['fgts']).lower(),
                                **{c: str(V[k]).lower() for k, c in (('inss', 'incidenciaINSS'), ('irpf', 'incidenciaIRPF')) if k in V})
            if V['base'] == 'MAIOR_REMUNERACAO':
                setf(v, 'formula/FormulaCalculada/baseTabelada/BaseTabelada/tipo', 'MAIOR_REMUNERACAO')
                v.find('historicosDaVerbaDoValorDevido/List').clear()
            else:
                base_hist(v, vid, V)
            # ocorrências: padrão uma só, na demissão; ou [[data, avos, ativa?], ...] (ex.: 20/12 de cada ano e a demissão)
            for oc in V.get('ocorrencias') or [[C['demissao'], V['avos']]]:
                a = oc[1]; ocorr(v, vid, dt(oc[0]), dt(oc[0]), 12, 1, a, a * 30, 'DECIMO_TERCEIRO_SALARIO', 'DEZEMBRO',
                                 ativo=oc[2] if len(oc) > 2 else True)
        elif t == 'SALARIO_RETIDO':
            p = (dt(V['periodo'][0]), dt(V['periodo'][1]))
            v, vid = nova_verba(P_SALDO, p, ordem, nome='SALÁRIO RETIDO', descricao='SALÁRIO RETIDO',
                                ocorrenciaDePagamento='MENSAL', incidenciaFGTS=str(V['fgts']).lower(),
                                aplicarProporcionalidade='true')
            v.find('assuntoCnj/AssuntoCnj/externalRef').text = '2452'
            setf(v, 'formula/FormulaCalculada/divisor/Divisor/outroValor', '1')
            setf(v, 'formula/FormulaCalculada/quantidade/Quantidade/valorInformado', '1')
            vinc_hist(v, vid, 'ÚLTIMA REMUNERAÇÃO', True)
            for d in meses(p[0], p[1]):
                ocorr(v, vid, max(d, p[0]), min(ultimo_dia(d), p[1]), 1, 1, 1, 1, 'COMUM', 'MENSAL')
        elif t == 'INFORMADA':
            # verba de valor informado por ocorrência (ex.: devolução de descontos, indenização de vale-transporte,
            # saldo de salário fixado em planilha). ocorrencias = [[data_inicial, data_final, valor], ...]
            if P_INF is None: raise ValueError('o modelo não tem a verba DEVOLUÇÃO DE DESCONTOS INDEVIDOS (protótipo de verba informada)')
            oc = V['ocorrencias']
            p = (dt(oc[0][0]), dt(oc[-1][1]))
            pagto = V.get('pagamento', 'MENSAL' if len(oc) > 1 else 'DESLIGAMENTO')
            v, vid = nova_verba(P_INF, p, ordem, nome=V['nome'], descricao=V['nome'], ocorrenciaDePagamento=pagto,
                                incidenciaFGTS=str(V.get('fgts', False)).lower(), incidenciaINSS=str(V.get('inss', False)).lower(),
                                incidenciaIRPF=str(V.get('irpf', False)).lower())
            if V.get('assunto_cnj'): v.find('assuntoCnj/AssuntoCnj/externalRef').text = str(V['assunto_cnj'])
            setf(v, 'formula/FormulaInformada/constante/Constante/valor', num(oc[0][2]) if len(oc) == 1 else '0')
            for a, b, val in oc:
                ocorr(v, vid, dt(a), dt(b), None, 'null', None, 0, 'COMUM', pagto, devido=val)
        elif t == 'HORAS_EXTRAS':
            # quantidade mensal fixa (ex.: 24 h semanais x 4,28 = 102,72), proporcional aos dias (base 30) nos meses incompletos
            if P_HE is None: raise ValueError('o modelo não tem o protótipo PROTO HORAS EXTRAS')
            p = (dt(V['periodo'][0]), dt(V['periodo'][1])); Q = V['quantidade_mensal']
            mult, div = V.get('multiplicador', 1.5), V.get('divisor', C['carga_horaria'])
            nome = V.get('nome', 'HORAS EXTRAS 50%')
            v, vid = nova_verba(P_HE, p, ordem, nome=nome, descricao=nome,
                                **incid(V, {'fgts': True, 'inss': True, 'irpf': False}))
            if V.get('assunto_cnj'): v.find('assuntoCnj/AssuntoCnj/externalRef').text = str(V['assunto_cnj'])
            if div == 'CARGA_HORARIA':  # divisor = carga horária do cálculo (adicional noturno, intervalo; cálculo 128483)
                setf(v, 'formula/FormulaCalculada/divisor/Divisor/tipo', 'CARGA_HORARIA')
                setf(v, 'formula/FormulaCalculada/divisor/Divisor/outroValor', 'null'); div = C['carga_horaria']
            else:
                setf(v, 'formula/FormulaCalculada/divisor/Divisor/outroValor', num(div))
            setf(v, 'formula/FormulaCalculada/multiplicador/Multiplicador/outroValor', str(mult))
            setf(v, 'formula/FormulaCalculada/quantidade/Quantidade/valorInformado', numq(Q))
            for chave, campo in (('excluir_faltas_justificadas', 'excluirFaltaJustificada'), ('excluir_faltas_nao_justificadas', 'excluirFaltaNaoJustificada'),
                                 ('excluir_ferias_gozadas', 'excluirFeriasGozadas')):
                if chave in V: setf(v, campo, str(V[chave]).lower())
            vinc_hist(v, vid, V.get('historico', 'ÚLTIMA REMUNERAÇÃO'), False)
            excl_he = v.findtext('excluirFeriasGozadas') == 'true'
            def oc_he(a, b, dias, cheio):
                g = dias_gozo(a, b) if excl_he else 0  # dias de férias gozadas saem da quantidade (128483)
                ocorr(v, vid, a, b, div, mult, Q if cheio and g == 0 else Q * (dias - g) / 30, Q, 'COMUM', 'MENSAL')
            mensal(p, oc_he)
        elif t == 'VERBA_HISTORICO':
            # verba mensal = histórico / divisor x multiplicador x quantidade (ex.: diferença salarial de 10%; horas extras
            # sobre comissões = comissão / 220 x 0,55 x 127,73; "repercussões" com coeficiente mensal)
            if P_VH is None: raise ValueError('o modelo não tem o protótipo PROTO VERBA SOBRE HISTORICO')
            p = (dt(V['periodo'][0]), dt(V['periodo'][1])); mult = V['multiplicador']
            div, Q = V.get('divisor', 1), V.get('quantidade', 1)
            pq, pb = V.get('proporcionalizar_quantidade', False), V.get('proporcionalizar_base', True)
            v, vid = nova_verba(P_VH, p, ordem, nome=V['nome'], descricao=V['nome'], aplicarProporcionalidade=str(pb).lower(),
                                **incid(V, {'fgts': True, 'inss': True, 'irpf': False}))
            if V.get('assunto_cnj'): v.find('assuntoCnj/AssuntoCnj/externalRef').text = str(V['assunto_cnj'])
            for chave, campo in (('excluir_faltas_justificadas', 'excluirFaltaJustificada'), ('excluir_faltas_nao_justificadas', 'excluirFaltaNaoJustificada'),
                                 ('excluir_ferias_gozadas', 'excluirFeriasGozadas')):
                if chave in V: setf(v, campo, str(V[chave]).lower())
            setf(v, 'formula/FormulaCalculada/divisor/Divisor/outroValor', num(div))
            setf(v, 'formula/FormulaCalculada/multiplicador/Multiplicador/outroValor', str(mult))
            setf(v, 'formula/FormulaCalculada/quantidade/Quantidade/valorInformado', numq(Q))
            setf(v, 'formula/FormulaCalculada/quantidade/Quantidade/aplicarProporcionalidade', str(pq).lower())
            if V.get('base_tabelada'):  # ex.: SALARIO_MINIMO (adicional de insalubridade, cálculo 123781)
                setf(v, 'formula/FormulaCalculada/baseTabelada/BaseTabelada/tipo', V['base_tabelada'])
                setf(v, 'formula/FormulaCalculada/baseTabelada/BaseTabelada/aplicarProporcionalidade', str(pb).lower())
                v.find('historicosDaVerbaDoValorDevido/List').clear()
            else:
                vinc_hist(v, vid, V['historico'], pb)
            excl_g = v.findtext('excluirFeriasGozadas') == 'true'
            def oc_vh(a, b, dias, cheio):
                g = dias_gozo(a, b) if excl_g else 0  # dias de férias gozadas saem da quantidade integral (123781)
                ef = dias - g; cheio = cheio and g == 0
                if ef <= 0: return  # mês inteiro de férias gozadas: sem ocorrência (validado no Exemplo 01, cálculo 128639)
                if pq: ocorr(v, vid, a, b, div, mult, Q if cheio else Q * ef / 30, Q, 'COMUM', 'MENSAL')
                else: ocorr(v, vid, a, b, div, mult, Q, Q if cheio else round(Q * min(30, ultimo_dia(a).day) / ef, 4), 'COMUM', 'MENSAL')
            mensal(p, oc_vh)
        elif t == 'REFLEXO':
            k = V['reflexo']; P = P_REF.get(k)
            if P is None: raise ValueError('o modelo não tem o protótipo de reflexo ' + k)
            bv, bvid, bp = gerados[V['base']]
            nome = V.get('nome', PREF[k] + ' SOBRE ' + V['base'])
            if k == 'FERIAS' and any(len(per) == 3 for per in V['periodos']) and bp[1] != ultimo_dia(bp[1]):
                # Exemplo 05: nas férias indenizadas o sistema toma como base o valor do último mês da verba-base, sem integralizar
                print(f"AVISO: '{nome}' tem férias indenizadas e a verba-base termina em mês incompleto ({bp[1]:%d/%m/%Y}); "
                      "o reflexo sairá sobre a fração do mês. Preferir VERBA_HISTORICO de data única.", file=sys.stderr)
            campos = {kk: vv for kk, vv in incid(V, {'fgts': None, 'inss': None, 'irpf': None}).items() if vv != 'none'}
            rp = (dt(V['periodo'][0]), dt(V['periodo'][1])) if V.get('periodo') else bp  # ex.: até a demissão (123781)
            v, vid = nova_verba(P, rp, ordem, nome=nome, **campos)
            it = v.find('formula/FormulaReflexo/baseVerba/BaseVerba/itens/List/ItemBaseVerba')
            setf(it, 'id', ids()); vc = it.find('verbaDeCalculo')[0]; vc.tag = bv.tag; vc.find('internalRef').text = bvid
            # média do reflexo: base variável (ex.: horas extras) usa os padrões do protótipo; base fixa (ex.: diferença
            # salarial) usa valor mensal, com a fração de mês integralizada e a base não integralizada (como no cálculo 108996)
            fixa = bv.findtext('tipoVariacaoParcela') == 'FIXA' and k != 'MULTA_467'
            padrao = {'comportamento': 'VALOR_MENSAL', 'periodo_media': 'PERIODO_AQUISITIVO', 'fracao': 'INTEGRALIZAR', 'integralizar': 'NAO'} if fixa else {}
            for chave, campo in (('comportamento', 'comportamentoDoReflexo'), ('periodo_media', 'periodoMediaReflexo'), ('fracao', 'tratamentoDaFracaoDeMesDoReflexo')):
                if chave in V or chave in padrao: setf(v, campo, V.get(chave, padrao.get(chave)))
            if 'integralizar' in V or 'integralizar' in padrao: setf(it, 'integralizar', V.get('integralizar', padrao.get('integralizar')))
            mref = V.get('multiplicador')  # Exemplo 01: multiplicador do reflexo (limitação ao teto do pedido; validado no Exemplo 01, cálculo 128639)
            if mref is not None: setf(v, 'formula/FormulaReflexo/multiplicador/Multiplicador/outroValor', str(mref))
            if k == 'RSR':
                def rsr(a, b, dias, cheio):
                    if not (TABELA_INSS_INICIO <= (a.year, a.month) and (b.year, b.month) <= TABELA_INSS_FIM):
                        raise ValueError('calendário de repousos validado só de %02d/%d a %02d/%d' % (TABELA_INSS_INICIO[1], TABELA_INSS_INICIO[0], TABELA_INSS_FIM[1], TABELA_INSS_FIM[0]))
                    u, r = calendario.uteis_repousos(a, b, estadual=est, municipal=mun)
                    ocorr(v, vid, a, b, u, 1, r, r if cheio else round(r * 30 / dias, 4), 'COMUM', 'MENSAL')
                for o in bv.find('ocorrencias/List'):
                    a, b = data_ms(o.findtext('dataInicial')), data_ms(o.findtext('dataFinal'))
                    rsr(a, b, (b - a).days + 1, a.day == 1 and b == ultimo_dia(a))
            elif k == 'AVISO':
                q = V.get('dias', C['aviso_dias']); ocorr(v, vid, dem, dem, 30, mref if mref is not None else 1, q, q * 30, 'AVISO_PREVIO', 'DESLIGAMENTO')
            elif k == 'FERIAS':
                # [início_aquisitivo, fim, avos] = indenizadas (na demissão); com [..., início_gozo, fim_gozo] = gozadas
                for per in V['periodos']:
                    a0, a1, avos = per[:3]
                    if len(per) > 3:
                        ocorr(v, vid, dt(per[3]), dt(per[4]), 12, str(mref) if mref is not None else '1.33333333', avos, avos, 'FERIAS', 'PERIODO_AQUISITIVO',
                              aq=(dt(a0), dt(a1)), indeniz=False)
                    else:
                        ocorr(v, vid, dem, dem, 12, str(mref) if mref is not None else '1.33333333', avos, avos * 30, 'FERIAS', 'PERIODO_AQUISITIVO',
                              aq=(dt(a0), dt(a1)), indeniz=True)
            elif k == 'DECIMO':
                for data, avos in V['ocorrencias']:
                    ocorr(v, vid, dt(data), dt(data), 12, mref if mref is not None else 1, avos, avos * 30, 'DECIMO_TERCEIRO_SALARIO', 'DEZEMBRO')
            elif k == 'MULTA_467':
                a = max(bp[0], ini_mes_dem); dias = (dem - a).days + 1
                ocorr(v, vid, a, dem, 1, '0.5', 1, round(30 / dias, 4), 'COMUM', 'DESLIGAMENTO')
            p = rp
        else:
            raise ValueError('tipo de verba não suportado: ' + t)
        if V.get('nome') and t not in ('INFORMADA', 'HORAS_EXTRAS', 'VERBA_HISTORICO', 'REFLEXO'):
            setf(v, 'nome', V['nome'])
        per = (data_ms(v.findtext('periodoInicial')), data_ms(v.findtext('periodoFinal')))
        gerados[v.findtext('nome').strip()] = (v, vid, per)
        vset.append(v); ordem += 1

    # data final do cálculo: obrigatória quando alguma ocorrência passa da demissão (ex.: dano moral com data posterior);
    # sem ela o PJe-Calc recusa a liquidação. Vem da ficha (contrato.termino_calculo) ou da última ocorrência.
    fim_oc = max([data_ms(o.findtext('dataFinal')) for v in vset for o in v.find('ocorrencias/List')] + [dem])
    termino = C.get('termino_calculo') or (fim_oc.strftime('%d/%m/%Y') if fim_oc > dem else None)
    if C.get('inicio_calculo'): setf(root, 'dataInicioCalculo', ms(C['inicio_calculo']))
    if termino: setf(root, 'dataTerminoCalculo', ms(termino))

    # 7. FGTS
    fg = root.find('fgts/Fgts'); FG = F['fgts']
    f0, f1 = dt(FG['inicio']), dt(FG['fim'])
    setf(fg, 'periodoInicial', ms_d(f0)); setf(fg, 'periodoFinal', ms_d(f1))
    setf(fg, 'destinoDoFgts', FG['destino']); setf(fg, 'multa', 'true' if FG.get('multa') else 'false')
    if FG.get('multa'): setf(fg, 'multaDoFgts', FG['multa'])
    setf(fg, 'tipoDoValorDaMulta', 'INFORMADA' if FG.get('multa_informada') is not None else 'CALCULADA')
    setf(fg, 'valorInformadoDaMulta', num(FG.get('multa_informada')))
    setf(fg, 'incidenciaDoFgts', FG['incidencia'])
    setf(fg, 'excluirAvisoDaMulta', str(FG['excluir_aviso_da_multa']).lower()); setf(fg, 'multaDoArtigo467', str(FG.get('multa_467', False)).lower())
    setf(fg, 'deduzirDoFGTS', 'false'); setf(fg, 'indiceMulta', 'null'); setf(fg, 'taxaDeJurosParaDataDemissao', 'null')
    fg.find('operacoesDeFgts/Set').clear()
    oset = fg.find('ocorrencias/Set'); proto_fo = oset[0]; oset.clear()
    hf = [h for h in hset if h.findtext('incidenciaFGTS') == 'true']
    base_f = {}
    for h in hf:
        prop = h.findtext('aplicarProporcionalidadeFGTS') == 'true'
        for o in h.find('ocorrencias/List'):
            k = int(o.findtext('dataOcorrencia')); val = float(o.findtext('valor'))
            if prop:  # histórico proporcional no FGTS: mês incompleto = valor x dias / 30 (como grava o sistema, cálculo 121044)
                m0 = data_ms(o.findtext('dataOcorrencia')); a_, b_ = max(m0, f0), min(ultimo_dia(m0), f1)
                g = dias_gozo(a_, b_)  # dias de férias gozadas também saem da base (128483)
                if g or not (a_.day == 1 and b_ == ultimo_dia(m0)): val = val * ((b_ - a_).days + 1 - g) / 30
            base_f[k] = base_f.get(k, 0) + val
    for d in meses(f0, f1):
        o = copy.deepcopy(proto_fo); data = max(d, f0)
        for x, orig in ((o, False), (o.find('ocorrenciaOriginal/OcorrenciaDeFgts'), True)):
            setf(x, 'id', ids()); setf(x, 'versao', '0'); setf(x, 'ocorrencia', ms_d(data))
            setf(x, 'baseHistorico', numq(round(base_f.get(int(ms_d(d)), 0), 6)))
            setf(x, 'tipoDeBaseDoFgts', 'CALCULADA'); setf(x, 'baseVerba', 'null'); setf(x, 'baseVerbaSemAvisoPrevio', 'null')
            dep = None if orig else FG.get('depositos', {}).get(d.strftime('%m/%Y'))  # FGTS já depositado, a deduzir
            setf(x, 'aliquotaDoFgtsEnum', 'OITO_POR_CENTO'); setf(x, 'depositado', num(dep) if dep is not None else '0')
            setf(x, 'tipoDeDepositadoDoFgts', 'INFORMADA' if dep is not None else 'CALCULADA')
            for t in ('indiceAcumulado', 'indiceAcumuladoDaMulta', 'taxaDeJuros'): setf(x, t, 'null')
        oset.append(o)

    # 8. contribuição social
    ins = root.find('inss/Inss'); I = F['inss']
    setf(ins, 'aliquotaEmpresaFixa', num(I['empresa'])); setf(ins, 'aliquotaRATFixa', num(I['sat']))
    if I.get('terceiros') is not None: setf(ins, 'aliquotaTerceirosFixa', num(I['terceiros']))  # caso Exemplo 13 (SAPT1: 5,8%)
    dev = ins.find('inssSobreSalariosDevidos/InssSobreSalariosDevidos')
    pag = ins.find('inssSobreSalariosPagos/InssSobreSalariosPagos')
    d0, d1 = dt(I['devidos'][0]), dt(I['devidos'][1])
    setf(dev, 'dataInicioPeriodo', ms_d(d0)); setf(dev, 'dataTerminoPeriodo', ms_d(d1))
    setf(pag, 'dataInicioPeriodo', ms(I['pagos'][0])); setf(pag, 'dataTerminoPeriodo', ms(I['pagos'][1]))
    for s in (pag.find('ocorrencias/Set'), pag.find('ocorrenciasAtualizacao/Set'), dev.find('ocorrenciasAtualizacao/Set')): s.clear()
    iset = dev.find('ocorrencias/Set'); proto_io = iset[0]; iset.clear()
    def tab_inss(d):
        # teto e alíquota do segurado que o próprio PJe-Calc grava em cada ocorrência mensal.
        # Extraídos do cálculo de referência 128449 (exportado em 01/11/2026) com extrair_tabela_inss.py.
        # Fora da cobertura o gerador para: exportar novo cálculo de referência e atualizar a tabela.
        if (d.year, d.month) in TABELA_INSS_EXTRA: return TABELA_INSS_EXTRA[(d.year, d.month)]
        if not (TABELA_INSS_INICIO <= (d.year, d.month) <= TABELA_INSS_FIM):
            raise ValueError('mês %02d/%d fora da tabela do INSS (%02d/%d a %02d/%d); atualizar com novo cálculo de referência'
                             % (d.month, d.year, TABELA_INSS_INICIO[1], TABELA_INSS_INICIO[0], TABELA_INSS_FIM[1], TABELA_INSS_FIM[0]))
        val = None
        for (y, m), t, a in TABELA_INSS:
            if (d.year, d.month) >= (y, m): val = (t, a)
        return val
    def inss_oc(dref, a, b, decimo):
        o = copy.deepcopy(proto_io)
        for x in (o, o.find('ocorrenciaOriginal/OcorrenciaDeInssSobreSalariosDevidos')):
            setf(x, 'id', ids()); setf(x, 'versao', '0')
            setf(x, 'dataOcorrenciaInss', ms_d(dref)); setf(x, 'dataInicioPeriodo', ms_d(a)); setf(x, 'dataTerminoPeriodo', ms_d(b))
            setf(x, 'valorBase', '0'); setf(x, 'tipoValorDaBase', 'CALCULADO')
            if x.find('valorBaseVerbas') is not None: setf(x, 'valorBaseVerbas', 'null')
            setf(x, 'ocorrenciaDecimoTerceiro', str(decimo and x is o).lower())
            setf(x, 'aliquotaEmpresa', num(I['empresa'])); setf(x, 'aliquotaSAT', num(I['sat']))
            if I.get('terceiros') is not None: setf(x, 'aliquotaTerceiros', num(I['terceiros']))  # lida da ocorrência, como empresa e SAT (Exemplo 13)
            t_, a_ = tab_inss(dref); setf(x, 'valorTetoSegurado', t_); setf(x, 'aliquotaSegurado', a_)
            setf(x, 'taxaDeJuros', 'null')
        iset.append(o)
    for d in meses(d0, d1):
        inss_oc(d, max(d, d0), min(ultimo_dia(d), d1), False)
        if d.month == 12 and datetime.date(d.year, 12, 20) <= dem:  # 13º de dezembro só durante o contrato
            inss_oc(d, datetime.date(d.year, 12, 20), datetime.date(d.year, 12, 20), True)
    inss_oc(ini_mes_dem, dem, dem, True)  # 13º rescisório

    # 9. multas / indenizações
    mset = root.find('multas/Set'); mset.clear()
    for M in F['multas']:
        m = ET.SubElement(mset, 'Multa')
        # RECLAMANTE_RECLAMADO: devida ao reclamante; RECLAMADO_RECLAMANTE: dedução (devida pelo reclamante)
        campos = [('id', ids()), ('versao', '0'), ('descricao', M['descricao']), ('tipoCredorDevedor', M.get('credor_devedor', 'RECLAMANTE_RECLAMADO')),
                  ('nomeTerceiro', 'null'), ('tipoValorDaMulta', 'INFORMADO'), ('valorMulta', num(M['valor'])),
                  ('valorJurosCalcExterno', 'null'), ('dataVencimentoMulta', ms(M['vencimento'])),
                  ('opcaoIndiceDeCorrecaoDaMulta', 'UTILIZAR_OUTRO_INDICE' if M.get('indice') else 'UTILIZAR_INDICE_TRABALHISTA'),
                  ('outroIndiceDeCorrecaoDaMulta', M.get('indice') or 'null'),
                  ('aplicarJurosSobreMulta', 'true' if M.get('juros_a_partir') else 'false'),
                  ('dataApartirDeAplicarJuros', ms(M.get('juros_a_partir'))), ('aliquotaMulta', 'null'), ('tipoBaseMulta', 'null'),
                  ('baseMulta', 'null'), ('indiceCorrecaoMulta', 'null'), ('taxaJurosMulta', 'null'), ('origemRegistro', 'CALCULO'),
                  ('tipoCobrancaReclamante', 'DESCONTAR_CREDITO'), ('dataEvento', 'null'), ('folhaDoEvento', 'null')]
        for k, val in campos: ET.SubElement(m, k).text = val
        cc = ET.SubElement(ET.SubElement(m, 'calculo'), 'Calculo')
        ET.SubElement(cc, 'internalRef').text = calc_id

    # 10. correção e juros
    pa = root.find('parametrosDeAtualizacao/ParametrosDeAtualizacao'); CO = F['correcao']
    setf(pa, 'indiceTrabalhista', CO['indice']); setf(pa, 'outroIndiceTrabalhista', CO['outro_indice'])
    setf(pa, 'combinarOutroIndice', 'true'); setf(pa, 'apartirDeOutroIndice', ms(CO['outro_a_partir']))
    setf(pa, 'aplicarJurosFasePreJudicial', str(CO['juros_pre_judicial']).lower())
    li = pa.find('listaDeCombinacaoDeIndices/Set'); proto_ci = li[0]; li.clear()
    for ind, apartir in CO.get('combinacoes_indice', [[CO['outro_indice'], CO['outro_a_partir']]]):
        ci = copy.deepcopy(proto_ci); setf(ci, 'id', ids()); setf(ci, 'outroIndiceTrabalhista', ind)
        setf(ci, 'apartirDeOutroIndice', ms(apartir)); li.append(ci)
    # juros: tabela base + combinações (ex.: SEM_JUROS até 29/08/2024 e TAXA_LEGAL a partir de 30/08/2024)
    setf(pa, 'juros', CO['juros'])
    lj = pa.find('listaDeCombinacaoDeJuros/Set'); proto_cj = lj[0]; lj.clear()
    setf(pa, 'combinarOutroJuros', 'true' if CO['combinacoes_juros'] else 'false')
    for tab, apartir in CO['combinacoes_juros']:
        cj = copy.deepcopy(proto_cj); setf(cj, 'id', ids()); setf(cj, 'outroJuros', tab)
        setf(cj, 'apartirDeOutroJuros', ms(apartir)); lj.append(cj)

    # 11. honorários
    hs = root.find('honorarios/Set'); proto_ho2 = hs[0]; hs.clear()
    for H in F['honorarios']:
        h = copy.deepcopy(proto_ho2); setf(h, 'id', ids())
        setf(h, 'nomeCredor', H['credor']); setf(h, 'numeroDocumentoFiscalCredor', H['doc'])
        setf(h, 'tipoHonorario', H.get('tipo', 'SUCUMBENCIAIS')); setf(h, 'descricao', H.get('descricao', 'HONORÁRIOS DE SUCUMBÊNCIA'))
        setf(h, 'tipoDeDevedor', H['devedor'])
        if H.get('valor') is not None:  # valor informado (ex.: honorários periciais fixados na sentença)
            setf(h, 'tipoValor', 'INFORMADO'); setf(h, 'aliquota', 'null'); setf(h, 'baseParaApuracao', 'null')
        else:
            setf(h, 'tipoValor', 'CALCULADO'); setf(h, 'aliquota', num(H['aliquota'])); setf(h, 'baseParaApuracao', H['base'])
        setf(h, 'tipoDocumentoFiscalCredor', 'CPF' if len(H['doc']) == 11 else 'CNPJ'); setf(h, 'apurarIRRF', 'false')
        for t in ('valor', 'baseHonorario', 'valorDescontoSimplificadoIrpf', 'valorImpostoRenda'):
            if h.find(t) is not None: setf(h, t, 'null')
        setf(h, 'dataVencimento', ms(H.get('vencimento') or F.get('data_liquidacao') or hoje))  # padrão: data da liquidação
        if H.get('valor') is not None: setf(h, 'valor', num(H['valor']))
        setf(h, 'tipoDeIndiceDeCorrecao', 'UTILIZAR_OUTRO_INDICE' if H.get('indice') else 'UTILIZAR_INDICE_TRABALHISTA')
        setf(h, 'outroIndiceDeCorrecao', H.get('indice') or 'null')
        setf(h, 'aplicarJuros', 'true' if H.get('juros_a_partir') else 'false'); setf(h, 'dataApartirDeAplicarJuros', ms(H.get('juros_a_partir')))
        hs.append(h)

    # 12. custas
    cu = root.find('custasJudiciais/CustasJudiciais')
    setf(cu, 'tipoDeCustasDeConhecimentoDoReclamado', F['custas']['reclamado_conhecimento'])
    setf(cu, 'baseParaCustasCalculadas', F['custas'].get('base', 'BRUTO_DEVIDO_AO_RECLAMANTE_MAIS_DEBITOS_RECLAMADO'))
    setf(cu, 'tipoDeCustasDeConhecimentoDoReclamante', 'NAO_SE_APLICA'); setf(cu, 'tipoDeCustasDeLiquidacao', 'NAO_SE_APLICA')
    if F['custas']['reclamado_conhecimento'] == 'INFORMADA' and F['custas'].get('valor') is not None:  # custas fixadas no título (caso Exemplo 13)
        setf(cu, 'dataVencimentoConhecimentoDoReclamado', ms(F['custas']['vencimento'])); setf(cu, 'valorConhecimentoDoReclamado', num(F['custas']['valor']))
    else:
        setf(cu, 'dataVencimentoConhecimentoDoReclamado', 'null'); setf(cu, 'valorConhecimentoDoReclamado', 'null')

    # 13. IR: período das verbas tributáveis; ocorrências são resultado
    ir = root.find('irpf/Irpf')
    trib = [int(o.findtext('dataInicial')) for v in vset if v.findtext('incidenciaIRPF') == 'true'
            for o in v.find('ocorrencias/List')]
    ano_rec = int((F.get('data_liquidacao') or hoje)[-4:])
    if trib:
        setf(ir, 'dataInicioAnosAnteriores', str(min(trib)))
        if dem.year >= ano_rec:  # como grava o sistema (128483): anos anteriores até 31/12; ano do recebimento até a demissão
            setf(ir, 'dataFimAnosAnteriores', ms('31/12/%d' % (ano_rec - 1))); setf(ir, 'dataFimAnoRecebimento', ms(C['demissao']))
        else:
            setf(ir, 'dataFimAnosAnteriores', ms(C['demissao']))
    else:  # sem verba tributável: não herdar as datas do modelo
        setf(ir, 'dataInicioAnosAnteriores', 'null'); setf(ir, 'dataFimAnosAnteriores', 'null')
    # ano do recebimento = ano da liquidação (separa RRA de anos anteriores do ano corrente)
    setf(ir, 'dataInicioAnoRecebimento', ms('01/01/' + (F.get('data_liquidacao') or hoje)[-4:]))
    for t in ('ocorrencias', 'ocorrenciasAtualizacao', 'ocorrenciasPagamento'): ir.find(t + '/Set').clear()

    # 14. seguro-desemprego
    if not F['seguro_desemprego']:
        sd = root.find('seguroDesemprego/SeguroDesemprego')
        for k, val in [('apurarSeguroDesemprego', 'false'), ('tipoSolicitacao', 'null'), ('numeroDeParcelas', '0'),
                       ('tipoSalarioPago', 'HISTORICO_SALARIAL'), ('remuneracaoMensal', '0'), ('limiteFaixa1', '0'),
                       ('valorPercentualFaixa1', '0'), ('valorPercentualFaixa2', '0'), ('somaFaixa2', '0'), ('valorPiso', '0'),
                       ('valorTeto', '0'), ('valorSeguroDesemprego', '0'), ('indiceDeCorrecao', '0'), ('taxaDeJuros', 'null')]:
            setf(sd, k, val)
    return root

if __name__ == '__main__':
    modelo, ficha, proc_src, saida = sys.argv[1:5]
    root = gerar(modelo, json.load(open(ficha, encoding='utf-8')), proc_src)
    entry = saida.rsplit('/', 1)[-1]
    data = pjcio.save(root, saida, entry)
    print('gerado', saida, len(data), 'bytes')
