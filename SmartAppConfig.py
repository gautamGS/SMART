BRAND_DICT = {
  1001 : 'PepsiCo',
  1002 : 'Doritos',
  1003 : 'Frito-Lay'
}

PRODUCT_DICT = {
  1001 : [('LaysCrisp', 2001), ('LaysAmericanStyle', 2002), ('PepsiDrink', 2003)],
  1002 : [('LaysMax', 2011), ('CheeseDip', 2012)],
  1003 : [('Kurkure', 2021)]
}

AFFINITY_DICT = { 
   2001 : [(2002, 80), (2003, 90), (2011, 10), (2012, 50), (2021, 80)],
   2002 : [(2001, 80), (2003, 90), (2011, 10), (2021, 5)],
   2003 : [(2001, 90), (2002, 95), (2011, 90), (2012, 5), (2021, 90)],
   2011 : [(2001, 15), (2002, 15), (2003, 90), (2012, 90), (2021, 10)],
   2012 : [(2001, 10), (2002, 80), (2003, 95), (2011, 80), (2021, 10)],
   2021 : [(2001, 10), (2002, 15), (2003, 98), (2011, 10), (2012, 30)]
}

PRD_IN_CONSIDERATION = 2002

COMPETITORS = [[1001, 1002]]

#Set PRD_ID_NOT_TO_MATCH to 0 to disable this option
PRD_ID_NOT_TO_MATCH=2003

OP_DISP_WIDTH=300
OP_DISP_HEIGHT=500
OUTPUT_FOLDER = "./out_repo"