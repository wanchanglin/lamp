#!/usr/bin/env bash
# wl-07-10-2024, Mon: command-line test script
# --add-mass
 
lamp cli \
  --sep "tab" \
  --input-data "./data/df_pos_3.tsv" \
  --col-idx "1, 2, 3, 4" \
  --add-path "" \
  --ref-path "./data/lipidmaps_full_20201001_v1.xlsx" \
  --sheet-name "0" \
  --ion-mode "pos" \
  --cal-mass \
  --thres-rt "1.0" \
  --thres-corr "0.5" \
  --thres-pval "0.05" \
  --method "pearson" \
  --positive \
  --ppm "5.0" \
  --save-db \
  --save-mr \
  --db-out "./res/test.db" \
  --sr-out "./res/test_s.tsv" \
  --mr-out "./res/test_m.tsv"
