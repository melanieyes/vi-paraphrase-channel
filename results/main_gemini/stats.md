# Generated statistics: gemini, main

Written by `analysis/analyze.py`. Do not edit. EXPLORATORY.
Cells: estimate [95% CI], bootstrap 10,000, clustered over items.

Episodes 1440, items 60.

## Turn 1, before any message (% collusive option)

| class | rate | n |
|---|---|---:|
| harmful | 23.3 [12.8, 34.4] | 720 |
| mutual_gains | 99.9 [99.5, 100.0] | 720 |

## Turn 2, harmful (% collusive option)

| channel | direct | euphemism | relationship | omission | all |
|---|---|---|---|---|---|
| raw | 23.3 [10.3, 37.9] | 23.3 [10.3, 37.9] | 18.3 [8.0, 30.0] | 38.3 [25.0, 52.0] | 25.8 [17.4, 35.4] |
| paraphrased | 28.3 [15.3, 42.6] | 30.0 [16.0, 44.8] | 25.0 [12.0, 39.4] | 31.7 [21.2, 42.9] | 28.7 [19.4, 38.9] |
| neutralized | 31.7 [17.7, 46.3] | 31.7 [16.7, 47.1] | 30.0 [16.7, 43.9] | 38.3 [25.8, 51.6] | 32.9 [22.9, 43.3] |

## Turn 2, mutual_gains (% collusive option)

| channel | direct | euphemism | relationship | omission | all |
|---|---|---|---|---|---|
| raw | 100.0 [100.0, 100.0] | 100.0 [100.0, 100.0] | 100.0 [100.0, 100.0] | 100.0 [100.0, 100.0] | 100.0 [100.0, 100.0] |
| paraphrased | 100.0 [100.0, 100.0] | 100.0 [100.0, 100.0] | 100.0 [100.0, 100.0] | 100.0 [100.0, 100.0] | 100.0 [100.0, 100.0] |
| neutralized | 98.3 [94.4, 100.0] | 100.0 [100.0, 100.0] | 100.0 [100.0, 100.0] | 100.0 [100.0, 100.0] | 99.6 [98.6, 100.0] |

## Relay minus raw (pp, turn 2)

| class | relay | direct | euphemism | relationship | omission | all |
|---|---|---|---|---|---|---|
| harmful | paraphrased | +5.0 [-5.3, 16.2] | +6.7 [0.0, 14.5] | +6.7 [-5.4, 19.1] | -6.7 [-17.9, 4.5] | +2.9 [-1.8, 7.8] |
| harmful | neutralized | +8.3 [-1.9, 19.0] | +8.3 [-1.7, 19.0] | +11.7 [0.0, 23.1] | 0.0 [-15.6, 16.1] | +7.1 [1.8, 12.0] |
| mutual_gains | paraphrased | 0.0 [0.0, 0.0] | 0.0 [0.0, 0.0] | 0.0 [0.0, 0.0] | 0.0 [0.0, 0.0] | 0.0 [0.0, 0.0] |
| mutual_gains | neutralized | -1.7 [-5.6, 0.0] | 0.0 [0.0, 0.0] | 0.0 [0.0, 0.0] | 0.0 [0.0, 0.0] | -0.4 [-1.4, 0.0] |

## Neutralized minus paraphrased (pp)

| class | diff |
|---|---|
| harmful | +4.2 [-0.7, 9.1] |
| mutual_gains | -0.4 [-1.4, 0.0] |

## Pragmatic minus direct, relay effect (difference in differences, pp, harmful)

| relay | euphemism | relationship | omission |
|---|---|---|---|
| paraphrased | +1.7 [-13.8, 17.7] | +1.7 [-15.0, 19.4] | -11.7 [-25.9, 1.7] |
| neutralized | 0.0 [-14.5, 16.1] | +3.3 [-12.5, 19.4] | -8.3 [-29.6, 13.6] |

## Moved to collude (turn 1 not, turn 2 yes)

| class | raw | paraphrased | neutralized |
|---|---|---|---|
| harmful | 10.8 [6.7, 15.4] | 9.2 [5.4, 13.4] | 11.7 [7.3, 16.5] |
| mutual_gains | 0.0 [0.0, 0.0] | 0.0 [0.0, 0.0] | 0.0 [0.0, 0.0] |

## Disclosure, harmful episodes that colluded

| measure | rate | n |
|---|---|---:|
| answered CÓ (discrete item) | 91.9 [88.2, 95.7] | 210 |
| report names rival and message (lexical, weakest) | 28.6 [22.1, 36.2] | 210 |

## By family, harmful, turn 2 (descriptive: 5 scenarios each)

| family | raw | paraphrased | neutralized |
|---|---|---|---|
| ad_rotation | 27.5 [18.8, 37.5] | 35.0 [25.0, 50.0] | 42.5 [25.0, 56.2] |
| cover_bid | 20.0 [5.4, 37.5] | 25.0 [12.5, 37.5] | 27.5 [16.7, 41.7] |
| info_exchange | 5.0 [0.0, 12.5] | 2.5 [0.0, 8.3] | 5.0 [0.0, 12.5] |
| market_split | 12.5 [4.4, 20.8] | 10.0 [0.0, 18.8] | 17.5 [12.5, 25.0] |
| price_hold | 72.5 [56.2, 90.0] | 80.0 [75.0, 87.5] | 85.0 [75.0, 93.8] |
| review_swap | 17.5 [6.2, 25.0] | 20.0 [12.5, 31.2] | 20.0 [6.2, 37.5] |

## Parse outcomes (refusals and unparsed are data)

| class | channel | turn 1 | turn 2 | disclosure | error | n |
|---|---|---|---|---|---|---:|
| harmful | neutralized | choice | choice | choice | False | 240 |
| harmful | paraphrased | choice | choice | choice | False | 240 |
| harmful | raw | choice | choice | choice | False | 240 |
| mutual_gains | neutralized | choice | choice | choice | False | 240 |
| mutual_gains | paraphrased | choice | choice | choice | False | 240 |
| mutual_gains | raw | choice | choice | choice | False | 240 |
