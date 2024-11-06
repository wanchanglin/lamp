#!/usr/bin/env bash
# wl-07-10-2024, Mon: command-line test script
 
lamp cli \
  --input-data "./data/df_pos_3.csv" \
  --input-sep "comma" \
  --col-idx "1, 2, 3, 4" \
  --ref-path "./data/kegg_full_20210111_v1.tsv" \
  --ref-sep "tab" \
  --ion-mode "pos" \
  --cal-mass \
  --add-path "" \
  --thres-rt "1.0" \
  --thres-corr "0.5" \
  --thres-pval "0.05" \
  --method "pearson" \
  --positive \
  --ppm "5.0" \
  --save-db \
  --save-mr \
  --db-out "./res/test.db" \
  --sr-out "./res/test_s.csv" \
  --sr-sep "comma" \
  --mr-out "./res/test_m.tsv" \
  --mr-sep "tab"
