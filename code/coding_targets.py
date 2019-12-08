############################################################################################

# This script recodes the indicators for Uruguay according to the SDG targets.
# A suggested allocation is provided for those indicators that were assigned to
# targets > 17.
# If multiple targets are suggested, the indicator is assigned to only one of them.
# The script also creates two additional dataset with the new allocation (test_sample_recoded.xlsx,
# test_sample_3_recoded.xlsx)
# Information is based on dataset: test_sample.xlsx, test_sample_3.xlsx.
# Authors: Daniele Guariso
# Last update: 08/12/2019

############################################################################################

import numpy as np
import pandas as pd
import os

home =  os.getcwd()[0:-4]

df_indicators = pd.read_excel(home+'data\\test_sample.xlsx')
# df_indicators = pd.read_excel(home+'data/test_sample.xlsx')

df_indicators.iat[2,2] = '1.2'
df_indicators.iat[4,2] = '1.2'


# The national poverty line is always higher than the internationl one (1.9$) and is also, on average,
# higher than the two other thresholds (3.2$ and 5.5$), so the indicators stated in terms of these
# two other thresholds will be assigned to target 1.1.

df_indicators.iat[9,2] = '1.1'
df_indicators.iat[11,2] = '1.1'
df_indicators.iat[12,2] = '1.1'

df_indicators.iat[15,2] = '1.2'
df_indicators.iat[20,2] = '1.1'
df_indicators.iat[21,2] = '1.1'
df_indicators.iat[28,2] = '2.1'

# 29 suggestion: 2.B
df_indicators.iat[29,2] = '2.b'

# 31 suggestion: 3.2
df_indicators.iat[31,2] = '3.2'

# 43 suggestion: 3.3
df_indicators.iat[43,2] = '3.3'

# 49 suggestion: 3.2
df_indicators.iat[49,2] = '3.2'

# 54 suggestion: 3.3
df_indicators.iat[54,2] = '3.3'

# 55 suggestion: 3.3
df_indicators.iat[55,2] = '3.3'

# 57 suggestion: 3.3
df_indicators.iat[57,2] = '3.3'

# 67 suggestion: 4.1
df_indicators.iat[67,2] = '4.1'

# 68 suggestion: 4.3
df_indicators.iat[68,2] = '4.3'

# 72 suggestion: 4.4
df_indicators.iat[72,2] = '4.4'

# 73 suggestion: 4.1
df_indicators.iat[73,2] = '4.1'

# 74 suggestion: 4.4 | 4.3
df_indicators.iat[74,2] = '4.4'

# 75 suggestion: 4.4 | 4.3
df_indicators.iat[75,2] = '4.4'

# 82 suggestion: 4.1
df_indicators.iat[82,2] = '4.1'

# 91 suggestion: 4.A
df_indicators.iat[91,2] = '4.a'

# 92 suggestion: 4.C
df_indicators.iat[92,2] = '4.c'

# 93 also 4.3
# 94 also 4.3
# 95 also 4.3
# 96 also 4.1

# 103 suggestion: 5.A | 5.5 |  8.5
df_indicators.iat[103,2] = '5.5'

# 125 suggestion: 8.3
df_indicators.iat[125,2] = '8.3'

# 126 suggestion: 8.3
df_indicators.iat[126,2] = '8.3'

df_indicators.iat[127,2] = '8.2'

# 128 suggestion: 8.2
df_indicators.iat[128,2] = '8.2'

# 129 suggestion: 8.3
df_indicators.iat[129,2] = '8.3'

# 130 suggestion: 8.3
df_indicators.iat[130,2] = '8.3'

# 131 suggestion: 8.3
df_indicators.iat[131,2] = '8.3'

df_indicators.iat[133,2] = '8.2'
df_indicators.iat[134,2] = '8.2'

# 135 suggestion: 8.2 | 8.3 | 17.10 | 17.12 | 17.13
# Recode SDG for 135
df_indicators.iat[135,1] = '17'
df_indicators.iat[135,2] = '17.13'

# Recode SDG for 136
df_indicators.iat[136,1] = '17'

# 137 suggestion: 8.1
df_indicators.iat[137,2] = '8.1'

# 138 suggestion: 8.8
df_indicators.iat[138,2] = '8.8'

# 140 suggestion: 8.3 | 17.10 | 17.12
df_indicators.iat[140,2] = '8.3'

# Recode SDG for 142
df_indicators.iat[142,1] = '17'
 
# 143 suggestion: 17.11 | 8.2
 # Recode SDG for 143
df_indicators.iat[143,1] = '17'
df_indicators.iat[143,2] = '17.11'

# Recode SDG for 144  
df_indicators.iat[144,1] = '17'

# 145 suggestion: 8.8 | 8.3
df_indicators.iat[145,2] = '8.3'

# 146 suggestion: 8.3
df_indicators.iat[146,2] = '8.3'

# 147 suggestion: 8.3
df_indicators.iat[147,2] = '8.3'

# Recode SDG for 148
df_indicators.iat[148,1] = '17'

# 149 suggestion: 17.11 | 8.2 
# Recode SDG for 149
df_indicators.iat[149,1] = '17'
df_indicators.iat[149,2] = '17.11'

# Recode SDG for 153 
df_indicators.iat[153,1] = '17'

# 154 suggestion: 16.6 (in case recode SDG)
df_indicators.iat[154,1] = '16'
df_indicators.iat[154,2] = '16.6'

# 155 suggestion: 8.3
df_indicators.iat[155,2] = '8.3'

# 156 suggestion: 17.13
# Recode SDG for 156
df_indicators.iat[156,2] = '17.13'
df_indicators.iat[156,1] = '17'

# 157 suggestion: 8.8
df_indicators.iat[157,2] = '8.8'

# 158 suggestion: 8.2 | 17.11
# Recode SDG for 158
df_indicators.iat[158,2] = '17.11'
df_indicators.iat[158,1] = '17'

df_indicators.iat[159,2] = '8.2'

# 160 suggestion: 8.2
df_indicators.iat[160,2] = '8.2'

# 161 suggestion: 17.3 | 8.3
df_indicators.iat[161,2] = '8.3'

# 162 suggestion: 8.3
df_indicators.iat[162,2] = '8.3'

# 166 suggestion: 8.3
df_indicators.iat[166,2] = '8.3'

# 167 also 8.3 | 9.5
# Recode SDG for 167
df_indicators.iat[167,1] = '17'

# 168 suggestion: 8.5
df_indicators.iat[168,2] = '8.5'

# 169 suggestion: 8.2
df_indicators.iat[169,2] = '8.2'

# 170 suggestion: 8.1 | 17.13
# Recode SDG for 170
df_indicators.iat[170,1] = '17'
df_indicators.iat[170,2] = '17.13'

# Recode SDG for 171
df_indicators.iat[171,1] = '17'

# 173 suggestion: 8.2
df_indicators.iat[173,2] = '8.2'

# 175 also 8.6
# 176 also 8.6
# 177 also 8.6
# 178 also 8.6

# 181 suggestion: 17.10 | 17.12 
# Recode SDG for 181
df_indicators.iat[181,1] = '17'
df_indicators.iat[181,2] = '17.12'

# Recode SDG for 183 
df_indicators.iat[183,1] = '17'

# 184 suggestion: 8.3 | 17.1 
df_indicators.iat[184,2] = '8.3'

# 185 suggestion: 8.3
df_indicators.iat[185,2] = '8.3'

# 186 suggestion: 8.8
df_indicators.iat[186,2] = '8.8'

# 187 suggestion: 8.3 | 10.5
# Recode SDG for 187
df_indicators.iat[187,2] = '10.5'
df_indicators.iat[187,1] = '10'

# 190 suggestion: 8.2
df_indicators.iat[190,2] = '8.2'

# 191 suggestion: 8.3
df_indicators.iat[191,2] = '8.3'

# 192 suggestion: 8.3
df_indicators.iat[192,2] = '8.3'

# 193 suggestion: 8.3
df_indicators.iat[193,2] = '8.3'

# 195 suggestion: 9.1
df_indicators.iat[195,2] = '9.1'

# 196 suggestion: 9.C | 17.8
df_indicators.iat[196,2] = '9.c'

# Recode SDG for 197
df_indicators.iat[197,1] = '17'

# 200 suggestion: 9.1
df_indicators.iat[200,2] = '9.1'

# 201 suggestion: 9.1 | 7.1
# Recode SDG for 201
df_indicators.iat[201,1] = '7'
df_indicators.iat[201,2] = '7.1'

# 202 suggestion: 9.1
df_indicators.iat[202,2] = '9.1'

# 204 suggestion: 9.1 | 11.2
df_indicators.iat[204,2] = '9.1'

# 205 suggestion: 9.5 
df_indicators.iat[205,2] = '9.5'

# 206 suggestion: 9.C | 17.8
df_indicators.iat[206,2] = '9.c'

# 211 suggestion: 10.5 | 8.10 (in case, recode SDG)
# Recode SDG for 211 
df_indicators.iat[211,2] = '10.5'
df_indicators.iat[211,1] = '10'

# 212 suggestion: 9.1
df_indicators.iat[212,2] = '9.1'

# 214 also 9.C
# Recode SDG for 214
df_indicators.iat[214,1] = '17'

# 218 suggestion: 9.C | 17.8
df_indicators.iat[218,2] = '9.c'

# 219 suggestion: 9.5 | 9.B 
df_indicators.iat[219,2] = '9.5'

# 220 suggestion: 9.5
df_indicators.iat[220,2] = '9.5'

# 221 suggestion: 9.1
df_indicators.iat[221,2] = '9.1'

# 222 suggestion: 9.5 | 9.B | 17.8
df_indicators.iat[222,2] = '9.5' 

# Recode SDG for 223 
df_indicators.iat[223,1] = '8'

# 225 suggestion: 9.5
df_indicators.iat[225,2] = '9.5' 

# 226 suggestion: 9.5 | 9.B | 17.8 | 8.3
df_indicators.iat[226,2] = '9.5' 

# 227 suggestion: 9.C | 17.6 | 17.8
# Recode SDG for 227
df_indicators.iat[227,2] = '17.6'
df_indicators.iat[227,1] = '17'

# 228 suggestion: 9.1 | 9.C | 17.8
df_indicators.iat[228,2] = '9.c'

# 229 suggestion: 9.5 | 9.B
df_indicators.iat[229,2] = '9.b'

# 230 suggestion 17.8 |  9.C
# Recode SDG for 230
df_indicators.iat[230,2] = '17.8'
df_indicators.iat[230,1] = '17'

# 231 also 9.C 
# Recode SDG for 231
df_indicators.iat[231,1] = '17'

# 232 suggestion: 9.1 | 17.6
# Recode SDG for 232
df_indicators.iat[232,2] = '17.6'
df_indicators.iat[232,1] = '17'

# 234 suggestion: 9.3| 8.3
# Recode SDG for 234
df_indicators.iat[234,2] = '8.3'
df_indicators.iat[234,1] = '8'

# 235 suggestion: 9.B | 17.6
# Recode SDG for 235
df_indicators.iat[235,2] = '17.6'
df_indicators.iat[235,1] = '17'

# 236 suggestion 9.3| 8.3
df_indicators.iat[236,2] = '9.3'

# 237 suggestion: 9.5 | 9.B
df_indicators.iat[237,2] = '9.5'

# Recode SDG for 238
df_indicators.iat[238,1] = '17'

df_indicators.iat[239,2] = '10.2'
df_indicators.iat[240,2] = '10.1'
df_indicators.iat[241,2] = '10.1'

# 242 suggestion: 10.3 | 8.10 | 9.3
# Recode SDG for 242
df_indicators.iat[242,2] = '9.3'
df_indicators.iat[242,1] = '9'

df_indicators.iat[243,2] = '10.2'
df_indicators.iat[244,2] = '10.2'
df_indicators.iat[245,2] = '10.2'
df_indicators.iat[246,2] = '10.2'
df_indicators.iat[247,2] = '10.1'

# 263 also 8.4
# 264 suggestion: 12.6
df_indicators.iat[264,2] = '12.6'

# 265 also 8.4
# 266 suggestion: 12.6
df_indicators.iat[266,2] = '12.6'

df_indicators.iat[269,2] = '13.2' 

# Recode SDG for 270
df_indicators.iat[270,1] = '9'

# Recode SDG for 271
df_indicators.iat[271,1] = '9'

# Recode SDG for 272
df_indicators.iat[272,1] = '9'

# Recode SDG for 273
df_indicators.iat[273,1] = '9'

# 276 suggestion: 2.4
# Recode SDG for 276
df_indicators.iat[276,2] = '2.4'
df_indicators.iat[276,1] = '2'

# 284 also 15.A

# 285 suggestion: 10.5 (it measures borrowers and lenders' rights)
# Recode SDG for 285
df_indicators.iat[285,2] = '10.5'
df_indicators.iat[285,1] = '10'

# Recode SDG for 286
df_indicators.iat[286,1] = '17'

# Recode SDG for 287
df_indicators.iat[287,1] = '17'

# 288 suggestion: 16.A
df_indicators.iat[288,2] = '16.a'

# 289 suggestion: 16.3
df_indicators.iat[289,2] = '16.3'

# 290 suggestion: 16.6
df_indicators.iat[290,2] = '16.6'

# Recode SDG for 291 (also 17.18)
df_indicators.iat[291,1] = '17'

# 292 suggestion: 16.3
df_indicators.iat[292,2] = '16.3'

# 293 suggestion: 16.6
df_indicators.iat[293,2] = '16.6'

# 294 suggestion: 16.7
df_indicators.iat[294,2] = '16.7'

df_indicators.iat[295,2] = '16.5' 

# 296 suggestion 8.3 (it is about regulations that promote private sector development, in case change SDG)
# Recode SDG for 296
df_indicators.iat[296,2] = '8.3'
df_indicators.iat[296,1] = '8'

# 297 suggestion: 16.3
df_indicators.iat[297,2] = '16.3'

# 298 suggestion: 16.3 | 9.B
df_indicators.iat[298,2] = '16.3'

# 299 suggestion: 16.4
df_indicators.iat[299,2] = '16.4'

# 300 suggestion: 16.6
df_indicators.iat[300,2] = '16.6'

# 301 suggestion: 16.6 | 16.5
df_indicators.iat[301,2] = '16.6'

# 302 suggestion: 16.3
df_indicators.iat[302,2] = '16.3'

# 303 suggestion: 16.3
df_indicators.iat[303,2] = '16.3'

# 304 suggestion: 16.5 
df_indicators.iat[304,2] = '16.5'

# 305 suggestion: 16.5
df_indicators.iat[305,2] = '16.5'

# 306 suggestion: 16.3
df_indicators.iat[306,2] = '16.3'

# 307 suggestion: 16.5
df_indicators.iat[307,2] = '16.5'

# 310 suggestion: 16.A | 16.1
df_indicators.iat[310,2] = '16.1'

# 311 suggestion: 16.A | 16.1
df_indicators.iat[311,2] = '16.1'

# 315 suggestion: 8.9
# Recode SDG for 315
df_indicators.iat[315,2] = '8.9' 
df_indicators.iat[315,1] = '8' 

# 316 suggestion: 17.12
df_indicators.iat[316,2] = '17.12'

# 317 suggestion: 17.10
df_indicators.iat[317,2] = '17.10'

# 318 suggestion: 17.13
df_indicators.iat[318,2] = '17.13'

# 319 suggestion: 17.13
df_indicators.iat[319,2] = '17.13'

# 320 suggestion: 17.13
df_indicators.iat[320,2] = '17.13'

df_indicators.to_excel(home+"data\\test_sample_recoded.xlsx", index=False, encoding='utf-16')

# Recoding the new set of indicators

df_indicators2 = pd.read_excel(home+'data\\test_sample_3.xlsx')
# df_indicators2 = pd.read_excel(home+'data/test_sample_3.xlsx')

# Recode SDG for 0 
df_indicators2.iat[0,2] = '4'

# Recode SDG for 1
df_indicators2.iat[1,2] = '4'

# Recode SDG for 2
df_indicators2.iat[2,2] = '4'

# Recode SDG for 3
df_indicators2.iat[3,2] = '4'

# Recode SDG for 4
df_indicators2.iat[4,2] = '4'

# 24 suggestion: 3.3
df_indicators2.iat[24,3] = '3.3'

# Recode SDG for 49
df_indicators2.iat[49,2] = '4'

# Recode SDG for 50
df_indicators2.iat[50,2] = '4'

# Recode SDG for 51
df_indicators2.iat[51,2] = '4'

# Recode SDG for 52
df_indicators2.iat[52,2] = '4'

df_indicators2.to_excel(home+"data\\test_sample_3_recoded.xlsx", index=False, encoding='utf-16')
