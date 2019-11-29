############################################################################################

# This script recodes the indicators for Uruguay according to the SDG targets.
# A suggested allocation is provided for those indicators that were assigned to
# targets > 17.
# Information is based on dataset: test_sample.csv. 
# Authors: Daniele Guariso
# Last update: 29/11/2019

############################################################################################

import numpy as np
import pandas as pd

df_indicators = pd.read_csv('test_sample.csv')

df_indicators.iat[2,2] = 1.2
df_indicators.iat[4,2] = 1.2


# The national poverty line is always higher than the internationl one (1.9$) and is also, on average,
# higher than the two other thresholds (3.2$ and 5.5$), so the indicators stated in terms of these
# two other thresholds will be assigned to target 1.1.

df_indicators.iat[9,2] = 1.1
df_indicators.iat[11,2] = 1.1
df_indicators.iat[12,2] = 1.1

df_indicators.iat[15,2] = 1.2
df_indicators.iat[20,2] = 1.1
df_indicators.iat[21,2] = 1.1
df_indicators.iat[28,2] = 2.3

# 29 suggestion: 2.B
# 31 suggestion: 3.2
# 43 suggestion: 3.3
# 49 suggestion: 3.2
# 54 suggestion: 3.3
# 55 suggestion: 3.3
# 57 suggestion: 3.3
# 67 suggestion: 4.1
# 68 suggestion: 4.3
# 72 suggestion: 4.4
# 73 suggestion: 4.1
# 74 suggestion: 4.4 | 4.3
# 75 suggestion: 4.4 | 4.3
# 82 suggestion: 4.1
# 91 suggestion: 4.A
# 92 suggestion: 4.C
# 93 also 4.3
# 94 also 4.3
# 95 also 4.3
# 96 also 4.1
# 103 suggestion: 5.A | 5.5 |  8.5(?)
# 125 suggestion: 8.3
# 126 suggestion: 8.3

df_indicators.iat[127,2] = 8.2

# 128 suggestion: 8.2
# 129 suggestion: 8.3
# 130 suggestion: 8.3
# 131 suggestion: 8.3

df_indicators.iat[133,2] = 8.2
df_indicators.iat[134,2] = 8.2

# 135 suggestion: 8.2 | 8.3 | 17.10 | 17.12(?)
# 136 also 8.1(?) 
# 137 suggestion: 8.1(?) why 8.2?
# 138 suggestion: 8.8
# 140 suggestion: 8.3 | 17.10 | 17.12
# 142 also 8.1(?) 
# 143 suggestion: 17.11 | 8.2(?)
# 144 why SDG is 8? 
# 145 suggestion: 8.8 | 8.3(?)
# 146 suggestion: 8.3
# 147 suggestion: 8.3
# 148 why SDG is 8? (for target, also 8.2 (?))
# 149 suggestion: 17.11 | 8.2 (?)
# 153 why SDG is 8? also 9.5
# 154 suggestion: 16.6 (in case recode SDG)
# 155 suggestion: 8.3
# 156 suggestion: 8.2
# 157 suggestion: 8.8
# 158 suggestion: 8.2 | 17.11

df_indicators.iat[159,2] = 8.2

# 160 suggestion: 8.3 | 12.8(?)
# 161 suggestion: 17.3 | 8.3
# 162 suggestion: 8.3
# 166 suggestion: 8.3(?)
# 167 suggestion: also 8.3 | 9.5
# 168 suggestion: 8.5
# 169 suggestion: 8.2
# 170 suggestion: 8.1 | 17.13
# 171 why SDG is 8?
# 173 suggestion: 8.2
# 175 also 8.6
# 176 also 8.6
# 177 also 8.6
# 178 also 8.6
# 181 suggestion: 17.10 | 17.12 (in case recode SDG)
# 183 why SDG is 8?
# 184 suggestion: 8.3(?) | 17.1 
# 185 suggestion: 8.3
# 186 suggestion: 8.8
# 187 suggestion: 8.3 | 10.5
# 190 suggestion: 8.2
# 191 suggestion: 8.3
# 192 suggestion: 8.3
# 193 suggestion: 8.3
# 195 suggestion: 9.1
# 196 suggestion: 9.C | 17.8
# 200 suggestion: 9.1
# 201 suggestion: 9.1 | 7.1
# 202 suggestion: 9.1
# 204 suggestion: 9.1 | 11.2
# 205 suggestion: 9.5 
# 206 suggestion: 9.C | 17.8
# 211 suggestion: 10.5 | 8.10 (in case, recode SDG)
# 212 suggestion: 9.1
# 214 also 9.C
# 218 suggestion: 9.C | 17.8
# 219 suggestion: 9.5 | 9.B 
# 220 suggestion: 9.5
# 221 suggestion: 9.1
# 222 suggestion: 9.5 | 9.B | 17.8
# 223 why SDG 9?
# 225 suggestion: 9.5 
# 226 suggestion: 9.5 | 9.B | 17.8 | 8.3
# 227 suggestion: 9.C | 17.6 | 17.8
# 228 suggestion: 9.1 | 9.C | 17.8
# 229 suggestion: 9.5 | 9.B
# 230 suggestion 17.8 |  9.C
# 231 also 9.C 
# 232 suggestion: 9.1 | 17.6
# 234 suggestion: 9.3(?) | 8.3(?) 
# 235 suggestion: 9.B | 17.6
# 236 suggestion 9.3(?) | 8.3(?) 
# 237 suggestion: 9.5 | 9.B
# 238 why SDG is 10?

df_indicators.iat[239,2] = 10.2
df_indicators.iat[240,2] = 10.1
df_indicators.iat[241,2] = 10.1

# 242 suggestion: 10.3 | 8.10

df_indicators.iat[243,2] = 10.2
df_indicators.iat[244,2] = 10.2
df_indicators.iat[245,2] = 10.2
df_indicators.iat[246,2] = 10.2
df_indicators.iat[247,2] = 10.1

# 263 also 8.4
# 264 suggestion: 12.6(?)
# 265 also 8.4
# 266 suggestion: 12.6(?)

df_indicators.iat[269,2] = 13.2 #(?)

# 270 why SDG is 13?
# 271 why SDG is 13?
# 272 why SDG is 13?
# 273 why SDG is 13?

df_indicators.iat[276,2] = 2.4 # In case change SDG

# 284 also 15.A
# 285 suggestion: 10.5 (it measures borrowers and lenders' rights) (in case recode SDG)
# 286 why SDG is 16? 
# 287 why SDG is 16? 
# 288 suggestion: 16.A
# 289 suggestion: 16.3
# 290 suggestion: 16.6
# 291 why SDG is 16? (also 17.18)
# 292 suggestion: 16.3
# 293 suggestion: 16.6
# 294 suggestion: 16.7

df_indicators.iat[295,2] = 16.5 

# 296 suggestion 8.3 (it is about regulations that promote private sector development, in case change SDG)
# 297 suggestion: 16.3
# 298 suggestion: 16.3 | 9.B
# 299 suggestion: 16.4
# 300 suggestion: 16.6
# 301 suggestion: 16.6 | 16.5
# 302 suggestion: 16.3
# 303 suggestion: 16.3
# 304 suggestion: 16.5 
# 305 suggestion: 16.5
# 306 suggestion: 16.3
# 307 suggestion: 16.5
# 310 suggestion: 16.A | 16.1
# 311 suggestion: 16.A | 16.1

df_indicators.iat[315,2] = 8.9 # In case change SDG

# 316 suggestion: 17.12
# 317 suggestion: 17.12
# 318 suggestion: 17.13
# 319 suggestion: 17.13
# 320 suggestion: 17.13
