import orodja
import csv
import re
import os


        
  
    
            


def pocisti_goro(gora):
    podatki = gora.groupdict()
    podatki['id'] = int(podatki['id'])
    podatki['priljubljenost'] = int(podatki['priljubljenost'])
    podatki['st_ogledov'] = int(podatki['st_ogledov'])
    podatki['st_poti'] = int(podatki['st_poti'])
    podatki['st_GPS_sledi'] = int(podatki['st_GPS_sledi'])
    podatki['višina'] = int(podatki['višina'])
    podatki['ime'] = podatki['ime'].strip()
    podatki['država'] = podatki['država'].strip()
    podatki['gorovje'] = podatki['gorovje'].strip()
    podatki['vrsta'] = podatki['vrsta'].strip()
    podatki['nakljucna_pot'] = podatki['nakljucna_pot'].strip()
    cas_h_min = podatki['cas_hoje'].replace('&nbsp;h',' ').replace('&nbsp;min','').replace('&nbsp;', '').split()
    
    if 'h' in podatki['cas_hoje']:
        if len(cas_h_min)==2:
            podatki['cas_hoje'] = int(cas_h_min[0])*60 + int(cas_h_min[1])
        else:
            podatki['cas_hoje'] = int(cas_h_min[0])*60
    else:
        podatki['cas_hoje'] = int(cas_h_min[0])
       
    podatki['zahtevnost_poti'] = podatki['zahtevnost_poti'].strip()
    
            
        
    
    return podatki


def izloci_podatke_gora(imenik):
   
    regex_gore = re.compile(
    r'<td class="naslov1"><b>&nbsp;&nbsp;<h1>(?P<ime>.*?)</h1></b></td>.*?'
    r'<tr><td><b>Država:</b> <a class=moder href=/gore/.+?/\d>(?P<država>.*?)</a></td></tr>.*?'
    r'<tr><td><b>Gorovje:</b> <a class="moder" href="/gorovje/.*?/\d{1,3}">(?P<gorovje>.*?)</a></td></tr>.*?'
    r'<tr><td><b>Višina:</b> (?P<višina>\d+?)&nbsp;m</td></tr>.*?'
    r'<tr><td><b>Širina/Dolžina:</b>&nbsp;<a class="moder" href="/zemljevid\.asp\?goraid=(?P<id>\d*?)">.*?'
    r'<tr><td><b>Vrsta:</b> (?P<vrsta>.*?)</td></tr>.*?'
    r'<tr><td><b>Ogledov:</b> (?P<st_ogledov>\d*?)</td></tr>.*?'
    r'<tr><td><b>Priljubljenost:</b> \d+% \((?P<priljubljenost>\d+). mesto\)</td></tr>.*?'
    r'<tr><td><b>Število poti:</b> <a class="moder" href="#poti">(?P<st_poti>\d*?)</a></td></tr>.*?'
    r'<tr><td><b>Število GPS sledi:</b> <a class="moder" href="/gps.asp">(?P<st_GPS_sledi>\d+)</a></td></tr>.*?'
    r"href='/izlet/.*?'>(?P<nakljucna_pot>.*?)&nbsp;.*?</a></td><td><a.*?"
    r"href='/izlet/.*?>(?P<cas_hoje>.*?)</a></td><td><a.*?"
    r"href='/izlet/.*?'>(?P<zahtevnost_poti>.*?)</a></td><td>.*?"
    ,
    flags=re.DOTALL)
    
    gore = []
    for html_datoteka in orodja.datoteke(imenik):
        for gora in re.finditer(regex_gore, orodja.vsebina_datoteke(html_datoteka)):
            gore.append(pocisti_goro(gora))
            
    print(gore)


    orodja.zapisi_tabelo(gore,['ime', 'država', 'gorovje', 'višina', 'id', 'vrsta', 'st_ogledov', 'priljubljenost', 'st_poti', 'st_GPS_sledi', 'nakljucna_pot', 'cas_hoje', 'zahtevnost_poti'], 'gore.csv')

izloci_podatke_gora('Hribi/')
