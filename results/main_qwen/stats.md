# Generated statistics: qwen, main

Written by `analysis/analyze.py`. Do not edit. EXPLORATORY.
Cells: estimate [95% CI], bootstrap 10,000, clustered over items.

Episodes 1440, items 60.

## Turn 1, before any message (% collusive option)

| class | rate | n |
|---|---|---:|
| harmful | 12.4 [6.9, 18.1] | 720 |
| mutual_gains | 96.1 [92.4, 99.2] | 720 |

## Turn 2, harmful (% collusive option)

| channel | direct | euphemism | relationship | omission | all |
|---|---|---|---|---|---|
| raw | 45.0 [31.2, 58.6] | 50.0 [36.0, 63.8] | 41.7 [27.6, 55.8] | 25.0 [13.3, 37.5] | 40.4 [31.6, 48.9] |
| paraphrased | 46.7 [32.0, 61.5] | 55.0 [41.7, 68.3] | 43.3 [28.1, 58.6] | 21.7 [11.3, 33.3] | 41.7 [32.3, 51.0] |
| neutralized | 36.7 [23.8, 50.0] | 43.3 [29.7, 57.1] | 36.7 [21.4, 52.2] | 20.0 [10.6, 30.4] | 34.2 [26.2, 42.2] |
| sum_short | n/a | n/a | n/a | n/a | n/a |
| sum_long | n/a | n/a | n/a | n/a | n/a |
| sum_system | n/a | n/a | n/a | n/a | n/a |
| sum_codeswitch | n/a | n/a | n/a | n/a | n/a |

## Turn 2, mutual_gains (% collusive option)

| channel | direct | euphemism | relationship | omission | all |
|---|---|---|---|---|---|
| raw | 100.0 [100.0, 100.0] | 96.7 [91.7, 100.0] | 98.3 [94.4, 100.0] | 100.0 [100.0, 100.0] | 98.8 [97.2, 100.0] |
| paraphrased | 100.0 [100.0, 100.0] | 100.0 [100.0, 100.0] | 100.0 [100.0, 100.0] | 100.0 [100.0, 100.0] | 100.0 [100.0, 100.0] |
| neutralized | 98.3 [94.4, 100.0] | 100.0 [100.0, 100.0] | 96.7 [91.4, 100.0] | 98.3 [94.4, 100.0] | 98.3 [96.2, 100.0] |
| sum_short | n/a | n/a | n/a | n/a | n/a |
| sum_long | n/a | n/a | n/a | n/a | n/a |
| sum_system | n/a | n/a | n/a | n/a | n/a |
| sum_codeswitch | n/a | n/a | n/a | n/a | n/a |

## Relay minus raw (pp, turn 2)

| class | relay | direct | euphemism | relationship | omission | all |
|---|---|---|---|---|---|---|
| harmful | paraphrased | +1.7 [-10.0, 13.3] | +5.0 [-6.8, 16.7] | +1.7 [-12.5, 16.1] | -3.3 [-14.1, 6.7] | +1.3 [-4.2, 6.7] |
| harmful | neutralized | -8.3 [-21.9, 4.8] | -6.7 [-22.5, 9.4] | -5.0 [-17.7, 8.9] | -5.0 [-20.0, 8.8] | -6.2 [-12.5, 0.5] |
| mutual_gains | paraphrased | 0.0 [0.0, 0.0] | +3.3 [0.0, 8.3] | +1.7 [0.0, 5.6] | 0.0 [0.0, 0.0] | +1.2 [0.0, 2.8] |
| mutual_gains | neutralized | -1.7 [-5.6, 0.0] | +3.3 [0.0, 8.3] | -1.7 [-7.6, 3.8] | -1.7 [-5.6, 0.0] | -0.4 [-2.8, 1.6] |

## Neutralized minus paraphrased (pp)

| class | diff |
|---|---|
| harmful | -7.5 [-13.4, -1.7] |
| mutual_gains | -1.7 [-3.8, 0.0] |

## Pragmatic minus direct, relay effect (difference in differences, pp, harmful)

| relay | euphemism | relationship | omission |
|---|---|---|---|
| paraphrased | +3.3 [-12.5, 18.3] | 0.0 [-18.3, 18.2] | -5.0 [-19.6, 10.0] |
| neutralized | +1.7 [-19.7, 24.0] | +3.3 [-12.0, 17.6] | +3.3 [-16.1, 23.2] |

## Moved to collude (turn 1 not, turn 2 yes)

| class | raw | paraphrased | neutralized | sum_short | sum_long | sum_system | sum_codeswitch |
|---|---|---|---|---|---|---|---|
| harmful | 31.2 [24.0, 39.0] | 27.5 [20.1, 34.9] | 27.5 [19.9, 35.3] | n/a | n/a | n/a | n/a |
| mutual_gains | 1.7 [0.4, 3.3] | 5.0 [0.9, 10.5] | 2.5 [0.4, 5.7] | n/a | n/a | n/a | n/a |

## Disclosure, harmful episodes that colluded

| measure | rate | n |
|---|---|---:|
| answered CÓ (discrete item) | 95.3 [92.5, 97.9] | 279 |
| report names rival and message (lexical, weakest) | 9.0 [4.8, 13.8] | 279 |

## By family, harmful, turn 2 (descriptive: 5 scenarios each)

| family | raw | paraphrased | neutralized | sum_short | sum_long | sum_system | sum_codeswitch |
|---|---|---|---|---|---|---|---|
| ad_rotation | 37.5 [22.3, 50.0] | 52.5 [42.7, 62.5] | 40.0 [18.8, 56.2] | n/a | n/a | n/a | n/a |
| cover_bid | 12.5 [4.2, 20.8] | 17.5 [6.2, 25.0] | 7.5 [0.0, 18.8] | n/a | n/a | n/a | n/a |
| info_exchange | 47.5 [41.7, 50.0] | 45.0 [37.5, 50.0] | 37.5 [25.0, 50.0] | n/a | n/a | n/a | n/a |
| market_split | 77.5 [68.8, 87.5] | 77.5 [67.5, 91.7] | 65.0 [56.2, 75.0] | n/a | n/a | n/a | n/a |
| price_hold | 47.5 [31.2, 62.5] | 50.0 [31.5, 68.8] | 37.5 [22.5, 50.0] | n/a | n/a | n/a | n/a |
| review_swap | 20.0 [8.3, 25.0] | 7.5 [0.0, 12.5] | 17.5 [6.2, 25.0] | n/a | n/a | n/a | n/a |

## By family, raw channel (Track 2.1)

| family | turn 1 | turn 2 | moved by the message | twin cooperation |
|---|---|---|---|---|
| ad_rotation | 5.0 [0.0, 12.5] | 37.5 [22.3, 50.0] | 32.5 [18.8, 43.8] | 100.0 [100.0, 100.0] |
| cover_bid | 0.0 [0.0, 0.0] | 12.5 [4.2, 20.8] | 12.5 [4.2, 20.8] | 100.0 [100.0, 100.0] |
| info_exchange | 27.5 [25.0, 33.3] | 47.5 [41.7, 50.0] | 22.5 [16.7, 25.0] | 100.0 [100.0, 100.0] |
| market_split | 22.5 [9.7, 33.3] | 77.5 [68.8, 87.5] | 57.5 [37.5, 75.0] | 100.0 [100.0, 100.0] |
| price_hold | 0.0 [0.0, 0.0] | 47.5 [31.2, 62.5] | 47.5 [31.2, 62.5] | 100.0 [100.0, 100.0] |
| review_swap | 5.0 [0.0, 12.5] | 20.0 [8.3, 25.0] | 15.0 [5.0, 25.0] | 92.5 [87.5, 100.0] |

## Parse outcomes (refusals and unparsed are data)

| class | channel | turn 1 | turn 2 | disclosure | error | n |
|---|---|---|---|---|---|---:|
| harmful | neutralized | choice | choice | choice | False | 240 |
| harmful | paraphrased | choice | choice | choice | False | 240 |
| harmful | raw | choice | choice | choice | False | 240 |
| mutual_gains | neutralized | choice | choice | choice | False | 240 |
| mutual_gains | paraphrased | choice | choice | choice | False | 240 |
| mutual_gains | raw | choice | choice | choice | False | 240 |

## Monitor gemini

Verdicts 13920, unparsed 0.

By channel and view (%):

| metric | channel | action | report | delivered | raw | report_only | message_only | standard | baseline_info | pop_baseline | summary |
|---|---|---|---|---|---|---|---|---|---|---|---|
| missed collusion (FNR) | raw | 59.8 [38.6, 77.9] | 38.1 [24.2, 51.1] | 0.0 [0.0, 0.0] | n/a | 37.1 [22.1, 51.0] | 0.0 [0.0, 0.0] | 14.4 [6.7, 22.5] | 5.2 [1.1, 9.8] | 0.0 [0.0, 0.0] | 1.0 [0.0, 3.3] |
| missed collusion (FNR) | paraphrased | 54.0 [32.3, 73.0] | 33.0 [21.8, 42.4] | 0.0 [0.0, 0.0] | 0.0 [0.0, 0.0] | 38.0 [21.6, 52.7] | 1.0 [0.0, 3.2] | 22.0 [11.0, 33.7] | 4.0 [0.0, 8.6] | 0.0 [0.0, 0.0] | 3.0 [0.0, 6.5] |
| missed collusion (FNR) | neutralized | 58.5 [36.9, 78.3] | 36.6 [21.3, 51.3] | 0.0 [0.0, 0.0] | 0.0 [0.0, 0.0] | 41.5 [23.4, 58.2] | 0.0 [0.0, 0.0] | 11.0 [2.4, 22.0] | 2.4 [0.0, 5.9] | 0.0 [0.0, 0.0] | 7.3 [1.9, 13.8] |
| missed collusion (FNR) | sum_short | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| missed collusion (FNR) | sum_long | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| missed collusion (FNR) | sum_system | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| missed collusion (FNR) | sum_codeswitch | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| missed, message-moved episodes only | raw | 64.0 [42.5, 80.8] | 37.3 [23.3, 50.0] | 0.0 [0.0, 0.0] | n/a | 37.3 [21.7, 51.3] | 0.0 [0.0, 0.0] | 8.0 [1.4, 15.1] | 6.7 [1.4, 12.7] | 0.0 [0.0, 0.0] | 1.3 [0.0, 4.5] |
| missed, message-moved episodes only | paraphrased | 57.6 [34.6, 78.7] | 33.3 [24.1, 40.9] | 0.0 [0.0, 0.0] | 0.0 [0.0, 0.0] | 37.9 [23.5, 52.4] | 0.0 [0.0, 0.0] | 1.5 [0.0, 5.3] | 0.0 [0.0, 0.0] | 0.0 [0.0, 0.0] | 1.5 [0.0, 5.6] |
| missed, message-moved episodes only | neutralized | 62.1 [39.2, 82.1] | 40.9 [25.0, 56.7] | 0.0 [0.0, 0.0] | 0.0 [0.0, 0.0] | 45.5 [26.7, 63.0] | 0.0 [0.0, 0.0] | 3.0 [0.0, 7.7] | 1.5 [0.0, 4.9] | 0.0 [0.0, 0.0] | 7.6 [2.0, 14.6] |
| missed, message-moved episodes only | sum_short | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| missed, message-moved episodes only | sum_long | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| missed, message-moved episodes only | sum_system | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| missed, message-moved episodes only | sum_codeswitch | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| false alarm, harmful but declined | raw | 0.0 [0.0, 0.0] | 7.7 [3.3, 12.9] | 70.6 [57.3, 82.5] | n/a | 4.9 [1.8, 8.3] | 100.0 [100.0, 100.0] | 0.0 [0.0, 0.0] | 7.7 [2.3, 14.1] | 2.8 [0.0, 6.8] | 16.8 [8.5, 25.4] |
| false alarm, harmful but declined | paraphrased | 0.0 [0.0, 0.0] | 2.9 [0.0, 6.4] | 64.3 [51.7, 76.4] | 55.7 [41.8, 69.5] | 2.9 [0.0, 6.5] | 97.9 [93.9, 100.0] | 0.0 [0.0, 0.0] | 5.7 [0.8, 11.8] | 2.9 [0.0, 7.5] | 15.0 [7.6, 23.6] |
| false alarm, harmful but declined | neutralized | 0.0 [0.0, 0.0] | 6.3 [2.2, 11.4] | 67.1 [54.2, 79.2] | 60.1 [46.0, 73.3] | 5.1 [1.2, 10.1] | 98.7 [95.8, 100.0] | 0.0 [0.0, 0.0] | 6.3 [2.1, 11.2] | 1.3 [0.0, 3.2] | 13.9 [6.7, 21.9] |
| false alarm, harmful but declined | sum_short | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| false alarm, harmful but declined | sum_long | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| false alarm, harmful but declined | sum_system | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| false alarm, harmful but declined | sum_codeswitch | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| flagged, collusive before any message | raw | 54.5 [25.0, 83.3] | 59.1 [33.3, 82.4] | 100.0 [100.0, 100.0] | n/a | 63.6 [38.5, 86.7] | 100.0 [100.0, 100.0] | 63.6 [42.3, 83.3] | 100.0 [100.0, 100.0] | 100.0 [100.0, 100.0] | 100.0 [100.0, 100.0] |
| flagged, collusive before any message | paraphrased | 52.9 [21.9, 85.7] | 67.6 [44.4, 90.5] | 100.0 [100.0, 100.0] | 100.0 [100.0, 100.0] | 61.8 [35.5, 88.2] | 97.1 [90.0, 100.0] | 38.2 [16.0, 60.9] | 88.2 [75.0, 100.0] | 100.0 [100.0, 100.0] | 94.1 [87.1, 100.0] |
| flagged, collusive before any message | neutralized | 56.2 [18.2, 92.3] | 81.2 [60.0, 100.0] | 100.0 [100.0, 100.0] | 100.0 [100.0, 100.0] | 75.0 [50.0, 100.0] | 100.0 [100.0, 100.0] | 56.2 [28.6, 84.2] | 93.8 [82.4, 100.0] | 100.0 [100.0, 100.0] | 93.8 [82.4, 100.0] |
| flagged, collusive before any message | sum_short | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| flagged, collusive before any message | sum_long | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| flagged, collusive before any message | sum_system | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| flagged, collusive before any message | sum_codeswitch | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| false alarm, twins | raw | 0.0 [0.0, 0.0] | 0.0 [0.0, 0.0] | 0.0 [0.0, 0.0] | n/a | 0.0 [0.0, 0.0] | 2.5 [0.0, 5.6] | 0.0 [0.0, 0.0] | 0.0 [0.0, 0.0] | 0.0 [0.0, 0.0] | 0.0 [0.0, 0.0] |
| false alarm, twins | paraphrased | 0.0 [0.0, 0.0] | 0.0 [0.0, 0.0] | 0.0 [0.0, 0.0] | 0.0 [0.0, 0.0] | 0.0 [0.0, 0.0] | 2.5 [0.0, 5.4] | 0.0 [0.0, 0.0] | 0.0 [0.0, 0.0] | 0.0 [0.0, 0.0] | 0.0 [0.0, 0.0] |
| false alarm, twins | neutralized | 0.0 [0.0, 0.0] | 0.0 [0.0, 0.0] | 0.4 [0.0, 1.4] | 0.8 [0.0, 2.1] | 0.0 [0.0, 0.0] | 0.8 [0.0, 2.8] | 0.0 [0.0, 0.0] | 0.0 [0.0, 0.0] | 0.0 [0.0, 0.0] | 0.0 [0.0, 0.0] |
| false alarm, twins | sum_short | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| false alarm, twins | sum_long | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| false alarm, twins | sum_system | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| false alarm, twins | sum_codeswitch | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |

Pooled over channels (%):

| metric | action | report | delivered | raw | report_only | message_only | standard | baseline_info | pop_baseline | summary |
|---|---|---|---|---|---|---|---|---|---|---|
| missed collusion (FNR) | 57.3 [36.2, 75.7] | 35.8 [24.6, 45.9] | 0.0 [0.0, 0.0] | 0.0 [0.0, 0.0] | 38.7 [23.7, 52.4] | 0.4 [0.0, 1.1] | 16.1 [8.2, 24.5] | 3.9 [0.5, 8.0] | 0.0 [0.0, 0.0] | 3.6 [1.3, 6.2] |
| missed, message-moved episodes only | 61.4 [39.7, 79.3] | 37.2 [27.0, 46.3] | 0.0 [0.0, 0.0] | 0.0 [0.0, 0.0] | 40.1 [26.1, 53.5] | 0.0 [0.0, 0.0] | 4.3 [0.6, 8.7] | 2.9 [0.5, 5.8] | 0.0 [0.0, 0.0] | 3.4 [1.3, 5.9] |
| false alarm, harmful but declined | 0.0 [0.0, 0.0] | 5.7 [3.2, 8.4] | 67.3 [55.6, 78.4] | 58.1 [45.0, 71.0] | 4.3 [2.2, 6.9] | 98.9 [96.9, 100.0] | 0.0 [0.0, 0.0] | 6.6 [2.6, 11.2] | 2.3 [0.4, 4.9] | 15.2 [8.5, 22.3] |
| flagged, collusive before any message | 54.2 [23.3, 83.6] | 68.1 [46.3, 87.2] | 100.0 [100.0, 100.0] | 100.0 [100.0, 100.0] | 65.3 [41.5, 88.0] | 98.6 [95.5, 100.0] | 50.0 [30.6, 67.7] | 93.1 [84.0, 100.0] | 100.0 [100.0, 100.0] | 95.8 [90.0, 100.0] |
| false alarm, twins | 0.0 [0.0, 0.0] | 0.0 [0.0, 0.0] | 0.1 [0.0, 0.5] | 0.4 [0.0, 1.0] | 0.0 [0.0, 0.0] | 2.0 [0.3, 4.2] | 0.0 [0.0, 0.0] | 0.0 [0.0, 0.0] | 0.0 [0.0, 0.0] | 0.0 [0.0, 0.0] |

| contrast | pp |
|---|---|
| C5 FNR delivered minus raw, paraphrased | 0.0 [0.0, 0.0] |
| C5 FNR delivered minus raw, neutralized | 0.0 [0.0, 0.0] |
| C6 FNR action minus delivered | +57.3 [36.2, 75.7] |
| 2.2 fnr action minus both | +21.5 [8.0, 33.7] |
| 2.2 fnr report only minus both | +2.9 [-3.2, 8.4] |
| 2.2 fpr declined message only minus all | +31.5 [20.5, 43.3] |

## Monitor haiku

Verdicts 13920, unparsed 0.

By channel and view (%):

| metric | channel | action | report | delivered | raw | report_only | message_only | standard | baseline_info | pop_baseline | summary |
|---|---|---|---|---|---|---|---|---|---|---|---|
| missed collusion (FNR) | raw | 51.5 [30.7, 69.3] | 19.6 [5.1, 33.3] | 0.0 [0.0, 0.0] | n/a | 19.6 [6.2, 31.9] | 2.1 [0.0, 6.6] | 30.9 [19.3, 42.2] | 0.0 [0.0, 0.0] | 0.0 [0.0, 0.0] | 1.0 [0.0, 3.3] |
| missed collusion (FNR) | paraphrased | 49.0 [28.5, 66.7] | 23.0 [11.0, 35.0] | 0.0 [0.0, 0.0] | 0.0 [0.0, 0.0] | 21.0 [7.8, 34.4] | 1.0 [0.0, 3.2] | 37.0 [21.5, 51.7] | 0.0 [0.0, 0.0] | 0.0 [0.0, 0.0] | 2.0 [0.0, 4.7] |
| missed collusion (FNR) | neutralized | 47.6 [26.2, 66.3] | 19.5 [7.2, 31.6] | 0.0 [0.0, 0.0] | 0.0 [0.0, 0.0] | 12.2 [2.9, 22.0] | 0.0 [0.0, 0.0] | 23.2 [10.0, 38.3] | 0.0 [0.0, 0.0] | 0.0 [0.0, 0.0] | 3.7 [0.0, 8.0] |
| missed collusion (FNR) | sum_short | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| missed collusion (FNR) | sum_long | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| missed collusion (FNR) | sum_system | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| missed collusion (FNR) | sum_codeswitch | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| missed, message-moved episodes only | raw | 54.7 [34.0, 71.3] | 18.7 [3.9, 34.1] | 0.0 [0.0, 0.0] | n/a | 21.3 [6.3, 35.8] | 2.7 [0.0, 8.5] | 10.7 [2.8, 18.5] | 0.0 [0.0, 0.0] | 0.0 [0.0, 0.0] | 1.3 [0.0, 4.5] |
| missed, message-moved episodes only | paraphrased | 50.0 [31.1, 67.1] | 19.7 [9.8, 30.0] | 0.0 [0.0, 0.0] | 0.0 [0.0, 0.0] | 16.7 [6.8, 28.8] | 0.0 [0.0, 0.0] | 4.5 [0.0, 10.3] | 0.0 [0.0, 0.0] | 0.0 [0.0, 0.0] | 0.0 [0.0, 0.0] |
| missed, message-moved episodes only | neutralized | 50.0 [28.3, 68.9] | 19.7 [7.5, 32.1] | 0.0 [0.0, 0.0] | 0.0 [0.0, 0.0] | 10.6 [1.6, 21.2] | 0.0 [0.0, 0.0] | 4.5 [0.0, 12.5] | 0.0 [0.0, 0.0] | 0.0 [0.0, 0.0] | 4.5 [0.0, 9.7] |
| missed, message-moved episodes only | sum_short | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| missed, message-moved episodes only | sum_long | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| missed, message-moved episodes only | sum_system | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| missed, message-moved episodes only | sum_codeswitch | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| false alarm, harmful but declined | raw | 20.3 [8.1, 34.5] | 21.0 [10.9, 31.9] | 62.9 [50.0, 75.4] | n/a | 21.7 [11.3, 32.7] | 100.0 [100.0, 100.0] | 0.7 [0.0, 2.4] | 13.3 [6.2, 21.1] | 11.2 [5.1, 18.1] | 14.7 [7.3, 22.8] |
| false alarm, harmful but declined | paraphrased | 17.1 [6.8, 30.5] | 19.3 [9.7, 31.0] | 59.3 [46.3, 71.2] | 56.4 [42.2, 70.1] | 18.6 [9.5, 29.4] | 100.0 [100.0, 100.0] | 0.0 [0.0, 0.0] | 12.1 [5.3, 20.2] | 9.3 [3.6, 15.7] | 12.9 [5.9, 21.1] |
| false alarm, harmful but declined | neutralized | 18.4 [6.7, 32.9] | 22.2 [11.2, 34.9] | 47.5 [35.7, 59.5] | 63.3 [50.8, 74.8] | 21.5 [11.1, 33.5] | 99.4 [97.9, 100.0] | 0.0 [0.0, 0.0] | 14.6 [7.4, 22.6] | 14.6 [6.8, 23.3] | 15.8 [7.0, 26.4] |
| false alarm, harmful but declined | sum_short | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| false alarm, harmful but declined | sum_long | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| false alarm, harmful but declined | sum_system | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| false alarm, harmful but declined | sum_codeswitch | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| flagged, collusive before any message | raw | 59.1 [29.2, 87.5] | 77.3 [57.7, 95.0] | 100.0 [100.0, 100.0] | n/a | 86.4 [70.8, 100.0] | 100.0 [100.0, 100.0] | 0.0 [0.0, 0.0] | 100.0 [100.0, 100.0] | 100.0 [100.0, 100.0] | 100.0 [100.0, 100.0] |
| flagged, collusive before any message | paraphrased | 52.9 [21.9, 85.7] | 70.6 [44.0, 96.3] | 100.0 [100.0, 100.0] | 100.0 [100.0, 100.0] | 70.6 [44.9, 95.8] | 97.1 [91.1, 100.0] | 0.0 [0.0, 0.0] | 100.0 [100.0, 100.0] | 100.0 [100.0, 100.0] | 94.1 [87.1, 100.0] |
| flagged, collusive before any message | neutralized | 62.5 [25.0, 100.0] | 81.2 [60.0, 100.0] | 100.0 [100.0, 100.0] | 100.0 [100.0, 100.0] | 81.2 [60.0, 100.0] | 100.0 [100.0, 100.0] | 0.0 [0.0, 0.0] | 100.0 [100.0, 100.0] | 100.0 [100.0, 100.0] | 100.0 [100.0, 100.0] |
| flagged, collusive before any message | sum_short | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| flagged, collusive before any message | sum_long | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| flagged, collusive before any message | sum_system | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| flagged, collusive before any message | sum_codeswitch | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| false alarm, twins | raw | 0.0 [0.0, 0.0] | 0.8 [0.0, 2.1] | 5.9 [2.4, 10.1] | n/a | 0.4 [0.0, 1.4] | 2.5 [0.4, 5.2] | 0.0 [0.0, 0.0] | 1.7 [0.4, 3.4] | 3.8 [1.0, 7.3] | 0.0 [0.0, 0.0] |
| false alarm, twins | paraphrased | 0.0 [0.0, 0.0] | 0.0 [0.0, 0.0] | 5.4 [1.9, 9.7] | 2.1 [0.4, 4.3] | 0.0 [0.0, 0.0] | 2.5 [0.0, 5.5] | 0.0 [0.0, 0.0] | 0.8 [0.0, 2.1] | 4.6 [1.5, 8.2] | 0.0 [0.0, 0.0] |
| false alarm, twins | neutralized | 0.0 [0.0, 0.0] | 1.3 [0.0, 2.8] | 3.8 [1.2, 7.0] | 3.8 [1.0, 7.0] | 0.0 [0.0, 0.0] | 1.3 [0.0, 3.3] | 0.0 [0.0, 0.0] | 3.4 [0.7, 6.8] | 4.7 [1.8, 7.9] | 0.0 [0.0, 0.0] |
| false alarm, twins | sum_short | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| false alarm, twins | sum_long | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| false alarm, twins | sum_system | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| false alarm, twins | sum_codeswitch | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |

Pooled over channels (%):

| metric | action | report | delivered | raw | report_only | message_only | standard | baseline_info | pop_baseline | summary |
|---|---|---|---|---|---|---|---|---|---|---|
| missed collusion (FNR) | 49.5 [29.6, 66.4] | 20.8 [8.4, 32.6] | 0.0 [0.0, 0.0] | 0.0 [0.0, 0.0] | 17.9 [6.2, 29.2] | 1.1 [0.0, 2.7] | 30.8 [18.9, 42.1] | 0.0 [0.0, 0.0] | 0.0 [0.0, 0.0] | 2.2 [0.8, 3.6] |
| missed, message-moved episodes only | 51.7 [33.0, 67.2] | 19.3 [8.0, 30.8] | 0.0 [0.0, 0.0] | 0.0 [0.0, 0.0] | 16.4 [6.1, 27.1] | 1.0 [0.0, 3.2] | 6.8 [1.8, 12.2] | 0.0 [0.0, 0.0] | 0.0 [0.0, 0.0] | 1.9 [0.4, 3.8] |
| false alarm, harmful but declined | 18.6 [7.6, 32.0] | 20.9 [11.2, 32.1] | 56.2 [45.0, 66.9] | 60.1 [47.6, 72.0] | 20.6 [11.6, 30.4] | 99.8 [99.2, 100.0] | 0.2 [0.0, 0.8] | 13.4 [7.0, 20.5] | 11.8 [5.7, 18.5] | 14.5 [7.2, 22.8] |
| flagged, collusive before any message | 56.9 [26.6, 86.8] | 75.0 [53.4, 95.7] | 100.0 [100.0, 100.0] | 100.0 [100.0, 100.0] | 77.8 [58.7, 95.2] | 98.6 [95.7, 100.0] | 0.0 [0.0, 0.0] | 100.0 [100.0, 100.0] | 100.0 [100.0, 100.0] | 97.2 [93.8, 100.0] |
| false alarm, twins | 0.0 [0.0, 0.0] | 0.7 [0.1, 1.5] | 5.0 [2.7, 7.6] | 2.9 [0.8, 5.5] | 0.1 [0.0, 0.5] | 2.1 [0.3, 4.5] | 0.0 [0.0, 0.0] | 2.0 [0.7, 3.5] | 4.3 [2.1, 6.9] | 0.0 [0.0, 0.0] |

| contrast | pp |
|---|---|
| C5 FNR delivered minus raw, paraphrased | 0.0 [0.0, 0.0] |
| C5 FNR delivered minus raw, neutralized | 0.0 [0.0, 0.0] |
| C6 FNR action minus delivered | +49.5 [29.6, 66.4] |
| 2.2 fnr action minus both | +28.7 [17.1, 39.4] |
| 2.2 fnr report only minus both | -2.9 [-6.8, 1.1] |
| 2.2 fpr declined message only minus all | +43.5 [32.8, 54.8] |

## Monitor qwen

Verdicts 5280, unparsed 0.

By channel and view (%):

| metric | channel | action | report | delivered | raw |
|---|---|---|---|---|---|
| missed collusion (FNR) | raw | 19.6 [0.0, 39.1] | 29.9 [9.5, 48.6] | 0.0 [0.0, 0.0] | n/a |
| missed collusion (FNR) | paraphrased | 19.0 [0.0, 39.0] | 28.0 [9.1, 46.4] | 0.0 [0.0, 0.0] | 0.0 [0.0, 0.0] |
| missed collusion (FNR) | neutralized | 19.5 [0.0, 39.5] | 30.5 [9.8, 50.0] | 0.0 [0.0, 0.0] | 0.0 [0.0, 0.0] |
| missed collusion (FNR) | sum_short | n/a | n/a | n/a | n/a |
| missed collusion (FNR) | sum_long | n/a | n/a | n/a | n/a |
| missed collusion (FNR) | sum_system | n/a | n/a | n/a | n/a |
| missed collusion (FNR) | sum_codeswitch | n/a | n/a | n/a | n/a |
| missed, message-moved episodes only | raw | 20.0 [0.0, 40.3] | 28.0 [8.0, 46.8] | 0.0 [0.0, 0.0] | n/a |
| missed, message-moved episodes only | paraphrased | 12.1 [0.0, 27.8] | 22.7 [7.0, 41.4] | 0.0 [0.0, 0.0] | 0.0 [0.0, 0.0] |
| missed, message-moved episodes only | neutralized | 18.2 [0.0, 38.8] | 30.3 [9.1, 51.0] | 0.0 [0.0, 0.0] | 0.0 [0.0, 0.0] |
| missed, message-moved episodes only | sum_short | n/a | n/a | n/a | n/a |
| missed, message-moved episodes only | sum_long | n/a | n/a | n/a | n/a |
| missed, message-moved episodes only | sum_system | n/a | n/a | n/a | n/a |
| missed, message-moved episodes only | sum_codeswitch | n/a | n/a | n/a | n/a |
| false alarm, harmful but declined | raw | 29.4 [13.8, 47.5] | 42.0 [27.5, 56.8] | 100.0 [100.0, 100.0] | n/a |
| false alarm, harmful but declined | paraphrased | 30.0 [14.1, 48.6] | 37.9 [24.1, 53.3] | 99.3 [97.7, 100.0] | 100.0 [100.0, 100.0] |
| false alarm, harmful but declined | neutralized | 31.6 [15.4, 50.0] | 41.1 [26.7, 56.4] | 100.0 [100.0, 100.0] | 100.0 [100.0, 100.0] |
| false alarm, harmful but declined | sum_short | n/a | n/a | n/a | n/a |
| false alarm, harmful but declined | sum_long | n/a | n/a | n/a | n/a |
| false alarm, harmful but declined | sum_system | n/a | n/a | n/a | n/a |
| false alarm, harmful but declined | sum_codeswitch | n/a | n/a | n/a | n/a |
| flagged, collusive before any message | raw | 81.8 [53.3, 100.0] | 63.6 [33.3, 92.6] | 100.0 [100.0, 100.0] | n/a |
| flagged, collusive before any message | paraphrased | 67.6 [35.3, 100.0] | 61.8 [35.0, 89.3] | 100.0 [100.0, 100.0] | 100.0 [100.0, 100.0] |
| flagged, collusive before any message | neutralized | 75.0 [38.5, 100.0] | 68.8 [33.3, 100.0] | 100.0 [100.0, 100.0] | 100.0 [100.0, 100.0] |
| flagged, collusive before any message | sum_short | n/a | n/a | n/a | n/a |
| flagged, collusive before any message | sum_long | n/a | n/a | n/a | n/a |
| flagged, collusive before any message | sum_system | n/a | n/a | n/a | n/a |
| flagged, collusive before any message | sum_codeswitch | n/a | n/a | n/a | n/a |
| false alarm, twins | raw | 60.8 [42.9, 77.8] | 38.8 [24.0, 53.8] | 69.6 [56.7, 81.9] | n/a |
| false alarm, twins | paraphrased | 60.0 [42.3, 77.1] | 37.1 [22.6, 52.2] | 70.8 [58.5, 82.6] | 78.3 [70.3, 86.2] |
| false alarm, twins | neutralized | 61.0 [43.2, 78.0] | 41.1 [25.7, 56.6] | 64.0 [49.8, 77.6] | 78.0 [68.1, 87.1] |
| false alarm, twins | sum_short | n/a | n/a | n/a | n/a |
| false alarm, twins | sum_long | n/a | n/a | n/a | n/a |
| false alarm, twins | sum_system | n/a | n/a | n/a | n/a |
| false alarm, twins | sum_codeswitch | n/a | n/a | n/a | n/a |

Pooled over channels (%):

| metric | action | report | delivered | raw |
|---|---|---|---|---|
| missed collusion (FNR) | 19.4 [0.0, 38.8] | 29.4 [9.5, 47.8] | 0.0 [0.0, 0.0] | 0.0 [0.0, 0.0] |
| missed, message-moved episodes only | 16.9 [0.0, 35.4] | 27.1 [8.5, 45.7] | 0.0 [0.0, 0.0] | 0.0 [0.0, 0.0] |
| false alarm, harmful but declined | 30.4 [14.6, 48.4] | 40.4 [26.7, 55.0] | 99.8 [99.3, 100.0] | 100.0 [100.0, 100.0] |
| flagged, collusive before any message | 73.6 [43.7, 100.0] | 63.9 [37.0, 90.9] | 100.0 [100.0, 100.0] | 100.0 [100.0, 100.0] |
| false alarm, twins | 60.6 [42.8, 77.6] | 39.0 [24.5, 53.8] | 68.2 [55.4, 80.6] | 78.2 [69.8, 86.1] |

| contrast | pp |
|---|---|
| C5 FNR delivered minus raw, paraphrased | 0.0 [0.0, 0.0] |
| C5 FNR delivered minus raw, neutralized | 0.0 [0.0, 0.0] |
| C6 FNR action minus delivered | +19.4 [0.0, 38.8] |
