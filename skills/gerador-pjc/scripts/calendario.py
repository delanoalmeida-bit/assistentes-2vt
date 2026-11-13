"""Calendário de repousos do PJe-Calc para São Luís-MA: domingos + feriados nacionais, estaduais (MA)
e municipais (São Luís) + pontos facultativos. Validado contra os 202 meses do cálculo 128456 (01/2010 a 10/2026)."""
import datetime
def pascoa(y):
    a=y%19;b=y//100;c=y%100;d=b//4;e=b%4;f=(b+8)//25;g=(b-f+1)//3;h=(19*a+b-d-g+15)%30
    i=c//4;k=c%4;l=(32+2*e+2*i-h-k)%7;m=(a+11*h+22*l)//451;mes=(h+l-7*m+114)//31;dia=((h+l-7*m+114)%31)+1
    return datetime.date(y,mes,dia)
def feriados(y, estadual=True, municipal=True, facultativos=('CARNAVAL','SEXTA-FEIRA SANTA','CORPUS CHRISTI')):
    f={datetime.date(y,1,1),datetime.date(y,4,21),datetime.date(y,5,1),datetime.date(y,9,7),datetime.date(y,10,12),
       datetime.date(y,11,2),datetime.date(y,11,15),datetime.date(y,12,25)}
    if y>=2024: f.add(datetime.date(y,11,20))
    p=pascoa(y)
    if 'CARNAVAL' in facultativos: f.add(p-datetime.timedelta(days=47))
    if 'SEXTA-FEIRA SANTA' in facultativos: f.add(p-datetime.timedelta(days=2))
    if 'CORPUS CHRISTI' in facultativos: f.add(p+datetime.timedelta(days=60))
    if estadual: f.add(datetime.date(y,7,28))
    if municipal: f|={datetime.date(y,6,29),datetime.date(y,9,8)}
    return f
def uteis_repousos(a,b,**kw):
    fs=set(); 
    for y in range(a.year,b.year+1): fs|=feriados(y,**kw)
    rep=ut=0; d=a
    while d<=b:
        if d.weekday()==6 or d in fs: rep+=1
        else: ut+=1
        d+=datetime.timedelta(days=1)
    return ut,rep
