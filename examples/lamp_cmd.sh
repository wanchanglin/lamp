#!/usr/bin/env bash

# wl-07-10-2024, Mon: command-line test script

# '--cal-mass',
# '--add-mass',
 
lamp cmd \
  --sep 'tab' \
  --input-data './data/df_pos_2.tsv' \
  --col-idx '1, 3, 6, 11' \
  --add-path '' \
  --ref-path './ref/ref_all_v7_pos.tsv' \
  --ion-mode 'pos' \
  --thres-rt '1.0' \
  --thres-corr '0.5' \
  --thres-pval '0.05' \
  --method "pearson" \
  --positive \
  --ppm '5.0' \
  --save-db \
  --save-mr \
  --db-out './res/test.db' \
  --sr-out './res/test_s.tsv' \
  --mr-out './res/test_m.tsv'
