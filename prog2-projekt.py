import requests as req
import re
import pandas as pd


'''Tu dobimo podatke za najpopularnejse atrakcije'''
url = 'https://www.jenreviews.com/best-places-to-visit/'
regex = r'(\d{1,4}\.[\Wa-zA-Z\sáí’]+\s\([A-Z]?[a-zA-Z\s.,]+\))'

headers1 = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/111.0'}
r1 = req.get(url, headers=headers1)

'''Tu dobimo podatke za cene hotelov'''
headers = {
    'User Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.54'}
r2 = req.get(
    'https://www.theglobaleconomy.com/rankings/hotel_and_restaurant_prices_wb/', headers=headers)
tables = pd.read_html(r2.text)
tab = tables[0]

att = re.findall(regex, r1.text)  # Tabela atrakcij

# tabela hotelov
tab.set_index('Countries').T.to_dict()
tab.set_index('Hotel and restaurant prices, 2017').T.to_dict()

tst = []  # vsa števila
tc = []  # vse države
att2 = []  # atrakcije
for i in att:
    st = re.findall(r'\d+', i)
    tst.append(int(st[0]))  # tabelo števil polnemo
    c = re.findall(r'[a-zA-Z\s.,]+', i)  # razdelimo atrakcije in države
    a = re.findall(r'[a-zA-Z\s,]+', i)
    tc.append(c[1])
    att2.append(a[0])


rank_and_name = dict(zip(tst, att2))
rank_and_country = dict(zip(tst, tc))

# dodamo tiste,ki nimajo zraven države
rank_and_name[30] = "Serengeti National Park"
rank_and_name[76] = "Mozambique"
rank_and_name[85] = "Andorra"
rank_and_name[88] = "Costa Rica"

rank_and_country[30] = "Tanzania"
rank_and_country[76] = "Mozambique"
rank_and_country[85] = "Andorra"
rank_and_country[88] = "Costa Rica"


all_att = dict()
for rank, name in rank_and_name.items():  # za vsako državo bomo označili attrakcijo in njen rank
    if rank < 101:
        all_att[rank_and_country[rank]] = {"Rank": rank, "Attraction": name}

all_h = dict()
i = 0
for country in tab['Countries']:  # Uredimo in sestavimo lep slovar za cene hotelov
    all_h[country] = {'Hotel': tab['Hotel and restaurant prices, 2017'][i]}
    i += 1


dict_final = all_att.copy()

for key, val in all_h.items():  # Oba slovarja zdruzimo v en slovar dict_final
    if key not in all_att:
        dict_final[key] = val
    else:
        for key2, val2 in all_h[key].items():
            dict_final[key][key2] = val2

# print(dict_final)

#----------- UI -----------------------
check = True #Preverja, ali je prvi podatek uporbnik pravilno vnesu

if check:
    pod = input('Po katerem podatku želite iskati: \nDržava \nRank \nAtrakcija \nCena hotela\n').lower()
    #V tem inputu lahko uporabnik izbere po katerih podatkih želi brskat skozi podatke. Njegove opcije so država, rank, atrakcija in cena hotela.
    #Če narobe vpiše ta podatek, mu to sporoči in ga vrne na input

    if pod in 'drzavadržava': #Če išče po državi preveri če je vpisal pravilno državo in mu nato izpiše vse podatke o tej državi, ki so v slovarju
        check = False
        dr = input('Katera država vas zanima? ').lower()
        if dr.capitalize() in dict_final:
            for key, val in dict_final[dr.capitalize()].items():
                print(key+':',val)
        else:
            print('Podatki o tej državi niso na voljo')
    elif pod == 'rank': #Če išče po ranku mu izpiše katera država je na tem ranku in kaj je njena atrakcija
        check = False
        ran = input('Kateri rank države, po popularnosti atrakcije, vas zanima? ')
        for key in dict_final.keys():
            if 'Rank' in dict_final[key] and int(ran) == dict_final[key]['Rank']:
                print('Država, ki je na', ran + '. mestu na lestvici popularnih atrakcij je', key, 'z atrakcijo' + dict_final[key]['Attraction'][:-1] + '.')
                break
    elif pod == 'atrakcija': #Podobno kot pri ranku, le da uporabnik išče po atrakciji in program sporoči rank atrakcije in državo
        check = False
        atr = input('Vnseite ime atrakcije, ki vas zanima: ').lower()
        ph = False
        for key in dict_final.keys():
            if 'Attraction' in dict_final[key] and atr in dict_final[key]['Attraction'].lower():
                print('Država, v kateri se nahaja', atr.capitalize(), 'je', key,    'in ta atrakcija je po popularnosti na', str(dict_final[key]['Rank']) + '. mestu.')
                ph = True
                break
        if not ph:
            print('Podatki o tej atrakciji niso na voljo')
    elif pod == 'cena hotela': #Uporabnika vpraša po želenem indeksu cene in mu dovoli določeno odstopanje od indeksa. Izpiše mu vse države znotraj obsega 
        #uporabnikovega vnešenega indeksa in poa indeks cen hotelov teh držav
        check = False
        cena = int(input(
            'Vnesite okviren indeks hotelske sobe (Višja številka pomeni dražji hotel): '))
        delta = int(
            input('Vnesite kakšno odstopanje dopuščate (10 bi pomenilo +-10): '))
        ch = False
        for key in dict_final.keys():
            if 'Hotel' in dict_final[key] and cena-delta <= int(dict_final[key]['Hotel']) < cena+delta:
                print('Država, ki ustreza vašemu želenemu indeksu je', key, 'kjer je indeks povprečne cene hotela', str(dict_final[key]['Hotel']) + '.')
                ch = True
        if not ch:
            print('Vašemu podanemu indeksu ne ustreza nobena država')
    else: #To izpiše, če je na začetku narobe vpisal besedo
        print('Vnesli ste neznano besedo, prosim poskusite ponovno.')