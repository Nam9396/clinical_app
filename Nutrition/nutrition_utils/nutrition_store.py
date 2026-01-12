## protein 

vaminolact_6_5 = {
    "name": "Vaminolact 6.5%", 
    "vol": "100ml", 
    "con_per_ml": 0.065
}

aminoplasmal_5 = {
    "name": "Aminoplasmal 5%", 
    "vol": "250ml / 500ml", 
    "con_per_ml": 0.05
}

aminoplasmal_10 = {
    "name": "Aminoplasmal 10%", 
    "vol": "250ml / 500ml", 
    "con_per_ml": 0.1
}

protein_ls = [
   vaminolact_6_5, 
   aminoplasmal_5, 
   aminoplasmal_10 
]

## lipid

smoflipid = {
    "name": "Smoflipid 20%", 
    "vol": "100ml / 250ml / 500ml", 
    "con_per_ml": 0.2
}

lipid_ls = [
    smoflipid
]

## đường 

glucose_10 = {
    "name": "Glucose 10%", 
    "vol": "250ml / 500ml", 
    "con_per_ml": 0.1
}

glucose_30 = {
    "name": "Glucose 30%", 
    "vol": "250ml / 500ml", 
    "con_per_ml": 0.3
}

glucose_ls = [
    glucose_10, 
    glucose_30
]

## điện giải

nacl_0_9 = {
    "name": "Natri chloride 0.9%", 
    "vol": "100ml / 250ml / 500ml", 
    "con_per_ml": 0.154
}

nacl_3 = {
    "name": "Natri chloride 3%", 
    "vol": "100ml / 250ml / 500ml", 
    "con_per_ml": 0.513
}

nacl_10 = {
    "name": "Natri chloride 10%", 
    "vol": "100ml / 250ml / 500ml", 
    "con_per_ml": 1.71
}

na_ls = [
    nacl_10,
    nacl_0_9, 
    nacl_3
]

kcl_10 = {
    "name": "Kali clorid 10%", 
    "vol": "5ml / 10ml", 
    "con_per_ml": 1.34
}

k_ls = [
    kcl_10
]

calci_gluconat_10 = {
    "name": "Growpone (Calci gluconate) 10%", 
    "vol": "10ml", 
    "con_per_ml": 0.45
}

cacl_10 = {
    "name": "Calci clorid 10%", 
    "vol": "5ml / 10ml", 
    "con_per_ml": 1.36
}

ca_ls = [
    calci_gluconat_10, 
    cacl_10
]

mg_so4 = {
    "name": "Magnesi sulfat kabi 15%", 
    "vol": "10ml", 
    "con_per_ml": 1.22
}

mg_ls = [
    mg_so4
]

electrolyte_ls = [
    nacl_0_9,
    nacl_3,
    nacl_10,
    kcl_10,
    calci_gluconat_10,
    cacl_10,
    mg_so4
]

## dinh dưỡng đường miệng 

sua_me = {
    "name": "Sữa mẹ", 
    "kcal_ml": 0.67, 
    "desc": ""
}

s1 = {
    "name": "S1", 
    "kcal_ml": 0.675, 
    "desc": "Sữa công thức 1 cho trẻ < 6 tháng"
}

s2 = {
    "name": "S2", 
    "kcal_ml": 0.672, 
    "desc": "Sữa công thức 1 cho trẻ 6 - 12 tháng"
}

non_thang = {
    "name": "Non tháng", 
    "kcal_ml": 0.714, 
    "desc": "Sữa công thức cao năng lượng cho trẻ non tháng"
}

f75 = {
    "name": "F‐75", 
    "kcal_ml": 0.75, 
    "desc": "Sữa cao năng lượng (SNLC1 - F75)"
}

pediasure = {
    "name": "Pediasure", 
    "kcal_ml": 1, 
    "desc": "Sữa cao năng lượng (SNLC2 - F100)"
}

po_nutrition_ls = [
    sua_me, 
    s1, 
    s2, 
    non_thang, 
    f75, 
    pediasure, 
    
]