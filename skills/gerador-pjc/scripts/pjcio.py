import zipfile, xml.etree.ElementTree as ET
DECL=b'<?xml version="1.0" encoding="ISO-8859-1"?>'
def load(p):
    if zipfile.is_zipfile(p):
        with zipfile.ZipFile(p) as z: raw=z.read(z.namelist()[0])
    else: raw=open(p,'rb').read()
    return ET.fromstring(raw)
def dumps(r):
    body=ET.tostring(r,encoding='us-ascii',short_empty_elements=False)
    if body.startswith(b'<?xml'): body=body[body.index(b'?>')+2:].lstrip()
    body=body.replace(b"'",b'&apos;').replace(b'"',b'&quot;')
    return DECL+body
def save(r,out,entry,dt=(2026,10,31,12,0,0)):
    data=dumps(r)
    with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED) as z:
        zi=zipfile.ZipInfo(entry,date_time=dt); zi.compress_type=zipfile.ZIP_DEFLATED
        z.writestr(zi,data)
    return data
