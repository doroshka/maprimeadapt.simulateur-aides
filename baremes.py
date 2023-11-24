import time
import json
import requests
import math
from re import sub
from bs4 import BeautifulSoup

json_str = '''
{
	"MPA":{
		"Île-de-France": {
			"1":[
				{"min" : 0,     "max": 22461, "value": 70},
				{"min" : 22461, "max": 27343, "value": 50}
			],
			"2":[
				{"min" : 0,     "max": 32967, "value": 70},
				{"min" : 32967, "max": 40130, "value": 50}
			],
			"3":[
				{"min" : 0,     "max": 39591, "value": 70},
				{"min" : 39591, "max": 48197, "value": 50}
			],
			"4":[
				{"min" : 0,     "max": 46226, "value": 70},
				{"min" : 46226, "max": 56277, "value": 50}
			],
			"5":[
				{"min" : 0,     "max": 52886, "value": 70},
				{"min" : 52886, "max": 64380, "value": 50}
			]
		},
		"Province": {
			"1":[
				{"min" : 0,     "max": 16229, "value": 70},
				{"min" : 16229, "max": 20805, "value": 50}
			],
			"2":[
				{"min" : 0,     "max": 23734, "value": 70},
				{"min" : 23734, "max": 30427, "value": 50}
			],
			"3":[
				{"min" : 0,     "max": 28545, "value": 70},
				{"min" : 28545, "max": 36591, "value": 50}
			],
			"4":[
				{"min" : 0,     "max": 33346, "value": 70},
				{"min" : 33346, "max": 42748, "value": 50}
			],
			"5":[
				{"min" : 0,     "max": 38168, "value": 70},
				{"min" : 38168, "max": 48930, "value": 50}
			]
		}
	},
	"ANAH":{
		"Île-de-France": {
			"1":[
				{"min" : 0,     "max": 22461, "value": 50},
				{"min" : 22461, "max": 27343, "value": 35}
			],
			"2":[
				{"min" : 0,     "max": 32967, "value": 50},
				{"min" : 32967, "max": 40130, "value": 35}
			],
			"3":[
				{"min" : 0,     "max": 39591, "value": 50},
				{"min" : 39591, "max": 48197, "value": 35}
			],
			"4":[
				{"min" : 0,     "max": 46226, "value": 50},
				{"min" : 46226, "max": 56277, "value": 35}
			],
			"5":[
				{"min" : 0,     "max": 52886, "value": 50},
				{"min" : 52886, "max": 64380, "value": 35}
			]
		},
		"Province": {
			"1":[
				{"min" : 0,     "max": 16229, "value": 50},
				{"min" : 16229, "max": 20805, "value": 35}
			],
			"2":[
				{"min" : 0,     "max": 23734, "value": 50},
				{"min" : 23734, "max": 30427, "value": 35}
			],
			"3":[
				{"min" : 0,     "max": 28545, "value": 50},
				{"min" : 28545, "max": 36591, "value": 35}
			],
			"4":[
				{"min" : 0,     "max": 33346, "value": 50},
				{"min" : 33346, "max": 42748, "value": 35}
			],
			"5":[
				{"min" : 0,     "max": 38168, "value": 50},
				{"min" : 38168, "max": 48930, "value": 35}
			]
		}
	},
	"CNAV":{
		"Île-de-France": {
			"1":[
				{"min" : 0,     "max": 906,   "value": 65},
				{"min" : 906,   "max": 970,   "value": 59},
				{"min" : 970,   "max": 1094,  "value": 55},
				{"min" : 1094,  "max": 1181,  "value": 50},
				{"min" : 1181,  "max": 1236,  "value": 43},
				{"min" : 1236,  "max": 1364,  "value": 37},
				{"min" : 1364,  "max": 2279,  "value": 30}
			],
			"2":[
				{"min" : 0,     "max": 1572,  "value": 65},
				{"min" : 1572,  "max": 1678,  "value": 59},
				{"min" : 1678,  "max": 1839,  "value": 55},
				{"min" : 1839,  "max": 1902,  "value": 50},
				{"min" : 1902,  "max": 1971,  "value": 43},
				{"min" : 1971,  "max": 2082,  "value": 37},
				{"min" : 2082,  "max": 3344,  "value": 30}
			]
		},
		"Province": {
			"1":[
				{"min" : 0,     "max": 906,   "value": 65},
				{"min" : 906,   "max": 970,   "value": 59},
				{"min" : 970,   "max": 1094,  "value": 55},
				{"min" : 1094,  "max": 1181,  "value": 50},
				{"min" : 1181,  "max": 1236,  "value": 43},
				{"min" : 1236,  "max": 1364,  "value": 37},
				{"min" : 1364,  "max": 1542,  "value": 30}
			],
			"2":[
				{"min" : 0,     "max": 1572,  "value": 65},
				{"min" : 1572,  "max": 1678,  "value": 59},
				{"min" : 1678,  "max": 1839,  "value": 55},
				{"min" : 1839,  "max": 1902,  "value": 50},
				{"min" : 1902,  "max": 1971,  "value": 43},
				{"min" : 1971,  "max": 2082,  "value": 37},
				{"min" : 2082,  "max": 2312,  "value": 30}
			]
		}
	}
}
'''

baremes = json.loads(json_str)

def checkEligibility(p, n1, n2, n3):
    r = dict()
    r['is_ok'] = 1
    r['MPA'] = "Non Eligible"
    #r['ANAH'] = "Non Eligible"
    #r['CNAV'] = "Non Eligible"
    r['province'] = p

    r['var'] = {}
    r['var']['nom_de_part_int'] = n1
    r['var']['revenue_fiscal'] = n2
    #r['var']['revenue_global'] = n3/12

    r['var']['nom_de_part_MPA'] = str(r['var']['nom_de_part_int'])
    #r['var']['nom_de_part_ANAH'] = str(r['var']['nom_de_part_int'])
    #r['var']['nom_de_part_CNAV'] = str(r['var']['nom_de_part_int'])
    if r['var']['nom_de_part_int'] > 5:
        r['var']['nom_de_part_MPA'] = "5"
        #r['var']['nom_de_part_ANAH'] = "5"
    if r['var']['nom_de_part_int'] > 2:
        r['var']['nom_de_part_CNAV'] = "2"

    r['var']['MPA'] = 0
    #r['var']['ANAH'] = 0
    #r['var']['CNAV'] = 0

    #for val in baremes['ANAH'][p][r['var']['nom_de_part_ANAH']]:
    #   if r['var']['revenue_fiscal'] >= val['min'] and r['var']['revenue_fiscal'] < val['max']:
    #       r['var']['ANAH'] = val['value']
    #       r['ANAH'] = str(r['var']['ANAH'])+"%"
    #       break

    for val in baremes['MPA'][p][r['var']['nom_de_part_MPA']]:
       if r['var']['revenue_fiscal'] >= val['min'] and r['var']['revenue_fiscal'] < val['max']:
           r['var']['MPA'] = val['value']
           r['MPA'] = str(r['var']['MPA'])+"%"
           break

    #for val in baremes['CNAV'][p][r['var']['nom_de_part_CNAV']]:
    #   if r['var']['revenue_global'] >= val['min'] and r['var']['revenue_global'] < val['max']:
    #       r['var']['CNAV'] = val['value']
    #       r['CNAV'] = str(r['var']['CNAV'])+"%"
    #       break

    return r
