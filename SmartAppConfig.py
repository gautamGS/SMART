'''
BRAND_DICT = {
  1001 : 'PepsiCo',
  1002 : 'Doritos',
  1003 : 'Frito-Lay'
}
'''

BRAND_DICT = {
  1001 : 'Lays',
  1002 : 'Frito-Lay',
}


'''
PRODUCT_DICT = {
  1001 : [('Maxx', 2001), ('LaysAmericanStyle', 2002), ('Classic', 2003)],
  1002 : [('Kurkure', 2011), ('Crispz', 2012)],
}
'''

PRODUCT_DICT = {
  1001 : [('Nachos', 2001), ('KharaBoondi', 2002), ('Classic', 2003)],
  1002 : [('RibbonPakoda', 2011), ('CheeseNachos', 2012)],
}

AFFINITY_DICT = { 
   2001 : [(2002, 80), (2003, 90), (2011, 10), (2012, 50)],
   2002 : [(2001, 80), (2003, 70), (2011, 10), (2021, 5)],
   2003 : [(2001, 90), (2002, 95), (2011, 90), (2012, 5)],
   2011 : [(2001, 15), (2002, 15), (2003, 90), (2012, 90)],
   2012 : [(2001, 10), (2002, 80), (2003, 95), (2011, 80)],
}


COMPETITORS = [[1001, 1002]]

#Set PRD_ID_NOT_TO_MATCH to 0 to disable this option
PRD_ID_NOT_TO_MATCH=2003
USE_MATCHER_STUB = False
OP_DISP_WIDTH=300
OP_DISP_HEIGHT=500

PRD_MASTER_REPO = "./prd_repo"
OUTPUT_FOLDER = "./out_repo"