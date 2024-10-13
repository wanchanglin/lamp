# Quick Start

In this vignette we will demonstrate how to use `lamp` python package. The 
input data and reference files are located in 
https://github.com/wanchanglin/lamp/tree/master/examples/data.

## Setup

To use `lamp`, the first step is to import some python libraries including 
`lamp`.


```python
import pandas as pd
from lamp import anno, stats, utils
```

## Data loading

`lamp` supports text files separated by comma (`,`) or tab (`\t`).
The Microsoft's XLSX is also supported, presuming that data are in the 
first sheet.

Here we use a small example data set with TSV format. Load it into python and
have a look of data format:



```python
# data set
d_data = "./data/df_pos_2.tsv"
data = pd.read_table(d_data, header=0, sep="\t")
data
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>name</th>
      <th>namecustom</th>
      <th>mz</th>
      <th>mzmin</th>
      <th>mzmax</th>
      <th>rt</th>
      <th>rtmin</th>
      <th>rtmax</th>
      <th>npeaks</th>
      <th>.</th>
      <th>...</th>
      <th>X210</th>
      <th>X209</th>
      <th>X208</th>
      <th>X207</th>
      <th>X206</th>
      <th>X205</th>
      <th>X204</th>
      <th>X203</th>
      <th>X202</th>
      <th>X201</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>M151T34</td>
      <td>M150.8867T34</td>
      <td>150.886715</td>
      <td>150.886592</td>
      <td>150.886863</td>
      <td>34.152700</td>
      <td>33.637595</td>
      <td>35.465548</td>
      <td>97</td>
      <td>97</td>
      <td>...</td>
      <td>4.224942e+06</td>
      <td>3.946599e+06</td>
      <td>3.668948e+06</td>
      <td>3.754321e+06</td>
      <td>3.853724e+06</td>
      <td>3.787350e+06</td>
      <td>3.584464e+06</td>
      <td>3.499711e+06</td>
      <td>3.623205e+06</td>
      <td>4.145770e+06</td>
    </tr>
    <tr>
      <th>1</th>
      <td>M151T40</td>
      <td>M151.0402T40</td>
      <td>151.040235</td>
      <td>151.040092</td>
      <td>151.040350</td>
      <td>39.838172</td>
      <td>37.556072</td>
      <td>40.532315</td>
      <td>95</td>
      <td>95</td>
      <td>...</td>
      <td>1.419062e+06</td>
      <td>1.251606e+06</td>
      <td>1.214826e+06</td>
      <td>8.143028e+05</td>
      <td>5.331963e+05</td>
      <td>1.930928e+06</td>
      <td>1.479001e+06</td>
      <td>1.076354e+06</td>
      <td>9.293218e+05</td>
      <td>5.298062e+05</td>
    </tr>
    <tr>
      <th>2</th>
      <td>M152T40</td>
      <td>M152.0436T40</td>
      <td>152.043607</td>
      <td>152.043451</td>
      <td>152.043737</td>
      <td>40.303700</td>
      <td>38.092678</td>
      <td>40.909428</td>
      <td>81</td>
      <td>81</td>
      <td>...</td>
      <td>1.203919e+05</td>
      <td>9.970442e+04</td>
      <td>9.384000e+04</td>
      <td>4.186335e+04</td>
      <td>NaN</td>
      <td>2.115447e+05</td>
      <td>1.285713e+05</td>
      <td>9.389346e+04</td>
      <td>7.163655e+04</td>
      <td>4.916483e+04</td>
    </tr>
    <tr>
      <th>3</th>
      <td>M153T34</td>
      <td>M152.8838T34</td>
      <td>152.883824</td>
      <td>152.883678</td>
      <td>152.883959</td>
      <td>34.174647</td>
      <td>33.637595</td>
      <td>35.465548</td>
      <td>98</td>
      <td>98</td>
      <td>...</td>
      <td>5.592065e+06</td>
      <td>5.761380e+06</td>
      <td>5.845419e+06</td>
      <td>5.576013e+06</td>
      <td>5.552878e+06</td>
      <td>6.132789e+06</td>
      <td>5.891378e+06</td>
      <td>5.418082e+06</td>
      <td>5.036840e+06</td>
      <td>5.733794e+06</td>
    </tr>
    <tr>
      <th>4</th>
      <td>M153T36</td>
      <td>M153.0195T36</td>
      <td>153.019474</td>
      <td>153.019331</td>
      <td>153.019633</td>
      <td>35.785847</td>
      <td>34.130244</td>
      <td>36.287354</td>
      <td>98</td>
      <td>98</td>
      <td>...</td>
      <td>7.284938e+06</td>
      <td>1.083289e+07</td>
      <td>1.140072e+07</td>
      <td>8.220552e+06</td>
      <td>9.255154e+06</td>
      <td>7.648211e+06</td>
      <td>7.723814e+06</td>
      <td>5.571163e+06</td>
      <td>5.362560e+06</td>
      <td>9.259675e+06</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>395</th>
      <td>M283T339</td>
      <td>M283.2646T339</td>
      <td>283.264583</td>
      <td>283.264341</td>
      <td>283.264809</td>
      <td>338.763489</td>
      <td>338.398380</td>
      <td>339.165948</td>
      <td>94</td>
      <td>94</td>
      <td>...</td>
      <td>3.509767e+05</td>
      <td>4.117633e+05</td>
      <td>3.948000e+05</td>
      <td>4.338804e+05</td>
      <td>5.335221e+05</td>
      <td>6.224684e+05</td>
      <td>7.009340e+05</td>
      <td>3.005173e+05</td>
      <td>3.133173e+05</td>
      <td>8.204783e+05</td>
    </tr>
    <tr>
      <th>396</th>
      <td>M284T60</td>
      <td>M284.1953T60</td>
      <td>284.195294</td>
      <td>284.194939</td>
      <td>284.195536</td>
      <td>59.593561</td>
      <td>58.844217</td>
      <td>60.107058</td>
      <td>59</td>
      <td>59</td>
      <td>...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>2.558004e+04</td>
      <td>4.020517e+04</td>
      <td>NaN</td>
      <td>3.162670e+04</td>
      <td>5.446684e+04</td>
    </tr>
    <tr>
      <th>397</th>
      <td>M284T108</td>
      <td>M284.2235T108</td>
      <td>284.223499</td>
      <td>284.223156</td>
      <td>284.223692</td>
      <td>108.406389</td>
      <td>107.880510</td>
      <td>108.971046</td>
      <td>72</td>
      <td>72</td>
      <td>...</td>
      <td>7.477652e+04</td>
      <td>7.482219e+04</td>
      <td>3.399667e+04</td>
      <td>7.233564e+04</td>
      <td>1.043879e+05</td>
      <td>2.506785e+04</td>
      <td>2.753769e+04</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>398</th>
      <td>M284T339</td>
      <td>M284.268T339</td>
      <td>284.267962</td>
      <td>284.267634</td>
      <td>284.268204</td>
      <td>338.725056</td>
      <td>338.268300</td>
      <td>339.370098</td>
      <td>84</td>
      <td>84</td>
      <td>...</td>
      <td>3.697604e+04</td>
      <td>5.398264e+04</td>
      <td>5.340109e+04</td>
      <td>6.557698e+04</td>
      <td>7.656575e+04</td>
      <td>1.040606e+05</td>
      <td>1.063727e+05</td>
      <td>NaN</td>
      <td>3.059370e+04</td>
      <td>1.358056e+05</td>
    </tr>
    <tr>
      <th>399</th>
      <td>M285T34</td>
      <td>M284.775T34</td>
      <td>284.775031</td>
      <td>284.774635</td>
      <td>284.775287</td>
      <td>34.079641</td>
      <td>33.667172</td>
      <td>35.198181</td>
      <td>97</td>
      <td>97</td>
      <td>...</td>
      <td>3.439330e+06</td>
      <td>3.359842e+06</td>
      <td>3.375577e+06</td>
      <td>3.789056e+06</td>
      <td>3.478506e+06</td>
      <td>3.391588e+06</td>
      <td>5.067802e+06</td>
      <td>3.497546e+06</td>
      <td>3.316025e+06</td>
      <td>3.906000e+06</td>
    </tr>
  </tbody>
</table>
<p>400 rows × 110 columns</p>
</div>



This data set includes peak list and intensity data matrix. `lamp` will use
peak list's name, m/z value and retention time. Hence you needs to 
indicates the locations of peak name, m/z value, retention time and starting 
points of data matrix from input data. Here they are 1, 3, 6 and 11,
respectively. 


```python
cols = [1, 3, 6, 11]
# get the input data set for `lamp` 
df = anno.read_peak(d_data, cols, sep='\t')
df
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>name</th>
      <th>mz</th>
      <th>rt</th>
      <th>QC9</th>
      <th>QC5</th>
      <th>QC4</th>
      <th>QC3</th>
      <th>QC26</th>
      <th>QC25</th>
      <th>QC24</th>
      <th>...</th>
      <th>X210</th>
      <th>X209</th>
      <th>X208</th>
      <th>X207</th>
      <th>X206</th>
      <th>X205</th>
      <th>X204</th>
      <th>X203</th>
      <th>X202</th>
      <th>X201</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>M151T34</td>
      <td>150.886715</td>
      <td>34.152700</td>
      <td>3.664879e+06</td>
      <td>3.735147e+06</td>
      <td>5.190263e+06</td>
      <td>2.742966e+06</td>
      <td>3.824723e+06</td>
      <td>3.722932e+06</td>
      <td>3.804188e+06</td>
      <td>...</td>
      <td>4.224942e+06</td>
      <td>3.946599e+06</td>
      <td>3.668948e+06</td>
      <td>3.754321e+06</td>
      <td>3.853724e+06</td>
      <td>3.787350e+06</td>
      <td>3.584464e+06</td>
      <td>3.499711e+06</td>
      <td>3.623205e+06</td>
      <td>4.145770e+06</td>
    </tr>
    <tr>
      <th>1</th>
      <td>M151T40</td>
      <td>151.040235</td>
      <td>39.838172</td>
      <td>7.406381e+05</td>
      <td>7.524075e+05</td>
      <td>NaN</td>
      <td>6.429245e+05</td>
      <td>1.167016e+06</td>
      <td>1.175981e+06</td>
      <td>1.122533e+06</td>
      <td>...</td>
      <td>1.419062e+06</td>
      <td>1.251606e+06</td>
      <td>1.214826e+06</td>
      <td>8.143028e+05</td>
      <td>5.331963e+05</td>
      <td>1.930928e+06</td>
      <td>1.479001e+06</td>
      <td>1.076354e+06</td>
      <td>9.293218e+05</td>
      <td>5.298062e+05</td>
    </tr>
    <tr>
      <th>2</th>
      <td>M152T40</td>
      <td>152.043607</td>
      <td>40.303700</td>
      <td>6.105241e+04</td>
      <td>5.335546e+04</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>6.875157e+04</td>
      <td>7.807399e+04</td>
      <td>8.943068e+04</td>
      <td>...</td>
      <td>1.203919e+05</td>
      <td>9.970442e+04</td>
      <td>9.384000e+04</td>
      <td>4.186335e+04</td>
      <td>NaN</td>
      <td>2.115447e+05</td>
      <td>1.285713e+05</td>
      <td>9.389346e+04</td>
      <td>7.163655e+04</td>
      <td>4.916483e+04</td>
    </tr>
    <tr>
      <th>3</th>
      <td>M153T34</td>
      <td>152.883824</td>
      <td>34.174647</td>
      <td>5.141479e+06</td>
      <td>5.496344e+06</td>
      <td>8.335846e+06</td>
      <td>3.860588e+06</td>
      <td>5.316874e+06</td>
      <td>5.988232e+06</td>
      <td>5.844917e+06</td>
      <td>...</td>
      <td>5.592065e+06</td>
      <td>5.761380e+06</td>
      <td>5.845419e+06</td>
      <td>5.576013e+06</td>
      <td>5.552878e+06</td>
      <td>6.132789e+06</td>
      <td>5.891378e+06</td>
      <td>5.418082e+06</td>
      <td>5.036840e+06</td>
      <td>5.733794e+06</td>
    </tr>
    <tr>
      <th>4</th>
      <td>M153T36</td>
      <td>153.019474</td>
      <td>35.785847</td>
      <td>5.336758e+06</td>
      <td>5.558265e+06</td>
      <td>1.118557e+07</td>
      <td>6.876715e+06</td>
      <td>9.967314e+06</td>
      <td>9.073822e+06</td>
      <td>9.328573e+06</td>
      <td>...</td>
      <td>7.284938e+06</td>
      <td>1.083289e+07</td>
      <td>1.140072e+07</td>
      <td>8.220552e+06</td>
      <td>9.255154e+06</td>
      <td>7.648211e+06</td>
      <td>7.723814e+06</td>
      <td>5.571163e+06</td>
      <td>5.362560e+06</td>
      <td>9.259675e+06</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>395</th>
      <td>M283T339</td>
      <td>283.264583</td>
      <td>338.763489</td>
      <td>7.330602e+05</td>
      <td>8.243956e+05</td>
      <td>NaN</td>
      <td>1.159506e+06</td>
      <td>4.294760e+05</td>
      <td>4.641813e+05</td>
      <td>4.570657e+05</td>
      <td>...</td>
      <td>3.509767e+05</td>
      <td>4.117633e+05</td>
      <td>3.948000e+05</td>
      <td>4.338804e+05</td>
      <td>5.335221e+05</td>
      <td>6.224684e+05</td>
      <td>7.009340e+05</td>
      <td>3.005173e+05</td>
      <td>3.133173e+05</td>
      <td>8.204783e+05</td>
    </tr>
    <tr>
      <th>396</th>
      <td>M284T60</td>
      <td>284.195294</td>
      <td>59.593561</td>
      <td>2.310932e+04</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>1.759336e+04</td>
      <td>2.645392e+04</td>
      <td>2.727266e+04</td>
      <td>...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>2.558004e+04</td>
      <td>4.020517e+04</td>
      <td>NaN</td>
      <td>3.162670e+04</td>
      <td>5.446684e+04</td>
    </tr>
    <tr>
      <th>397</th>
      <td>M284T108</td>
      <td>284.223499</td>
      <td>108.406389</td>
      <td>3.748444e+04</td>
      <td>2.993283e+04</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>3.175596e+04</td>
      <td>3.879604e+04</td>
      <td>4.299529e+04</td>
      <td>...</td>
      <td>7.477652e+04</td>
      <td>7.482219e+04</td>
      <td>3.399667e+04</td>
      <td>7.233564e+04</td>
      <td>1.043879e+05</td>
      <td>2.506785e+04</td>
      <td>2.753769e+04</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>398</th>
      <td>M284T339</td>
      <td>284.267962</td>
      <td>338.725056</td>
      <td>1.161886e+05</td>
      <td>1.476514e+05</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>6.753490e+04</td>
      <td>5.436219e+04</td>
      <td>...</td>
      <td>3.697604e+04</td>
      <td>5.398264e+04</td>
      <td>5.340109e+04</td>
      <td>6.557698e+04</td>
      <td>7.656575e+04</td>
      <td>1.040606e+05</td>
      <td>1.063727e+05</td>
      <td>NaN</td>
      <td>3.059370e+04</td>
      <td>1.358056e+05</td>
    </tr>
    <tr>
      <th>399</th>
      <td>M285T34</td>
      <td>284.775031</td>
      <td>34.079641</td>
      <td>4.063268e+06</td>
      <td>3.807148e+06</td>
      <td>4.645099e+06</td>
      <td>2.232221e+06</td>
      <td>4.576754e+06</td>
      <td>4.533339e+06</td>
      <td>4.559356e+06</td>
      <td>...</td>
      <td>3.439330e+06</td>
      <td>3.359842e+06</td>
      <td>3.375577e+06</td>
      <td>3.789056e+06</td>
      <td>3.478506e+06</td>
      <td>3.391588e+06</td>
      <td>5.067802e+06</td>
      <td>3.497546e+06</td>
      <td>3.316025e+06</td>
      <td>3.906000e+06</td>
    </tr>
  </tbody>
</table>
<p>400 rows × 103 columns</p>
</div>



Data frame `df` now includes only `name`, `mz`, `rt` and intensity data
matrix. 

## Metabolite annotation

To performance metabolite annotation, users should provide their own 
reference file. Otherwise, `lamp` will use its default reference file for 
annotation.


```python
ref_path = ""    # if empty, use default reference file for matching

# load reference library
cal_mass = False
ref = anno.read_ref(ref_path, calc=cal_mass)
ref
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>compound_id</th>
      <th>molecular_formula</th>
      <th>compound_name</th>
      <th>exact_mass</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1638</td>
      <td>C10Cl10O</td>
      <td>Chlordecone</td>
      <td>485.683441</td>
    </tr>
    <tr>
      <th>1</th>
      <td>38485</td>
      <td>C10H10Br2O2</td>
      <td>Dibromothymoquinone</td>
      <td>319.904755</td>
    </tr>
    <tr>
      <th>2</th>
      <td>32427</td>
      <td>C10H10BrNO2</td>
      <td>Brofoxine (USAN/INN)</td>
      <td>254.989491</td>
    </tr>
    <tr>
      <th>3</th>
      <td>39834</td>
      <td>C10H10Cl2N2O</td>
      <td>Fenmetozole (USAN)</td>
      <td>244.017018</td>
    </tr>
    <tr>
      <th>4</th>
      <td>10156</td>
      <td>C10H10Cl2O3</td>
      <td>4-(2,4-Dichlorophenoxy)butyric acid</td>
      <td>248.000700</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>31639</th>
      <td>80256</td>
      <td>H5O10P3</td>
      <td>PPPi</td>
      <td>257.909557</td>
    </tr>
    <tr>
      <th>31640</th>
      <td>37374</td>
      <td>H6NO9P3</td>
      <td>(Diphosphono)Aminophosphonic Acid</td>
      <td>256.925542</td>
    </tr>
    <tr>
      <th>31641</th>
      <td>32626</td>
      <td>H9N2O4P</td>
      <td>Ammonium phosphate (NF)</td>
      <td>132.029994</td>
    </tr>
    <tr>
      <th>31642</th>
      <td>735</td>
      <td>HNO3</td>
      <td>Nitrate</td>
      <td>62.995643</td>
    </tr>
    <tr>
      <th>31643</th>
      <td>40762</td>
      <td>HNO3</td>
      <td>Peroxynitrite</td>
      <td>62.995643</td>
    </tr>
  </tbody>
</table>
<p>31644 rows × 4 columns</p>
</div>



The reference file must have two columns: `molecular_formula` and
`compound_name` (or `name`). The `exact_mass` is optional. if absent, `lamp`
will calculates it based on NIST database. If your reference file has
`exact_mass` and want to calculate it using NIST database, set `calc` as
True.  The `exact_mass` is used to match against a range of `mz`, controlled
by `ppm` in data frame `df`.

Now we have a look another reference file:


```python
ref_path = "./data/hmdb_urine_v4_0_20200910_v1.tsv"

# load reference library
cal_mass = True    # there is no exact mass in reference file, so calculate
ref = anno.read_ref(ref_path, calc=cal_mass)
ref
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>id</th>
      <th>molecular_formula</th>
      <th>molecular_name</th>
      <th>inchi</th>
      <th>inchi_key</th>
      <th>exact_mass</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>HMDB0000001</td>
      <td>C7H11N3O2</td>
      <td>1-Methylhistidine</td>
      <td>InChI=1S/C7H11N3O2/c1-10-3-5(9-4-10)2-6(8)7(11...</td>
      <td>BRMWTNUJHUMWMS-LURJTMIESA-N</td>
      <td>169.085127</td>
    </tr>
    <tr>
      <th>1</th>
      <td>HMDB0000002</td>
      <td>C3H10N2</td>
      <td>1,3-Diaminopropane</td>
      <td>InChI=1S/C3H10N2/c4-2-1-3-5/h1-5H2</td>
      <td>XFNJVJPLKCPIBV-UHFFFAOYSA-N</td>
      <td>74.084398</td>
    </tr>
    <tr>
      <th>2</th>
      <td>HMDB0000005</td>
      <td>C4H6O3</td>
      <td>2-Ketobutyric acid</td>
      <td>InChI=1S/C4H6O3/c1-2-3(5)4(6)7/h2H2,1H3,(H,6,7)</td>
      <td>TYEYBOSBBBHJIV-UHFFFAOYSA-N</td>
      <td>102.031694</td>
    </tr>
    <tr>
      <th>3</th>
      <td>HMDB0000008</td>
      <td>C4H8O3</td>
      <td>2-Hydroxybutyric acid</td>
      <td>InChI=1S/C4H8O3/c1-2-3(5)4(6)7/h3,5H,2H2,1H3,(...</td>
      <td>AFENDNXGAFYKQO-VKHMYHEASA-N</td>
      <td>104.047344</td>
    </tr>
    <tr>
      <th>4</th>
      <td>HMDB0000010</td>
      <td>C19H24O3</td>
      <td>2-Methoxyestrone</td>
      <td>InChI=1S/C19H24O3/c1-19-8-7-12-13(15(19)5-6-18...</td>
      <td>WHEUWNKSCXYKBU-QPWUGHHJSA-N</td>
      <td>300.172545</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>1606</th>
      <td>HMDB0012308</td>
      <td>C8H8O3</td>
      <td>Vanillin</td>
      <td>InChI=1S/C8H8O3/c1-11-8-4-6(5-9)2-3-7(8)10/h2-...</td>
      <td>MWOOGOJBHIARFG-UHFFFAOYSA-N</td>
      <td>152.047344</td>
    </tr>
    <tr>
      <th>1607</th>
      <td>HMDB0012322</td>
      <td>C10H8O</td>
      <td>2-Naphthol</td>
      <td>InChI=1S/C10H8O/c11-10-6-5-8-3-1-2-4-9(8)7-10/...</td>
      <td>JWAZRIHNYRIHIV-UHFFFAOYSA-N</td>
      <td>144.057515</td>
    </tr>
    <tr>
      <th>1608</th>
      <td>HMDB0012325</td>
      <td>C5H10O5</td>
      <td>Arabinofuranose</td>
      <td>InChI=1S/C5H10O5/c6-1-2-3(7)4(8)5(9)10-2/h2-9H...</td>
      <td>HMFHBZSHGGEWLO-HWQSCIPKSA-N</td>
      <td>150.052823</td>
    </tr>
    <tr>
      <th>1609</th>
      <td>HMDB0012451</td>
      <td>C20H28O3</td>
      <td>all-trans-5,6-Epoxyretinoic acid</td>
      <td>InChI=1S/C20H28O3/c1-15(8-6-9-16(2)14-17(21)22...</td>
      <td>KEEHJLBAOLGBJZ-WEDZBJJJSA-N</td>
      <td>316.203845</td>
    </tr>
    <tr>
      <th>1610</th>
      <td>HMDB0012467</td>
      <td>C15H13O9S</td>
      <td>(-)-Epicatechin sulfate</td>
      <td>InChI=1S/C15H14O9S/c16-9-3-8-5-13(24-25(20,21)...</td>
      <td>WTXWEAXATVSZQX-AFYYWNPRSA-M</td>
      <td>369.028028</td>
    </tr>
  </tbody>
</table>
<p>1611 rows × 6 columns</p>
</div>



Next we use HMDB reference file for compounds match. Here function argument
`ppm` is used to control the m/z value matching tolerance or range.


```python
ppm = 5.0
match = anno.comp_match_mass(df, ppm, ref)
match
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>id</th>
      <th>mz</th>
      <th>molecular_formula</th>
      <th>molecular_name</th>
      <th>inchi</th>
      <th>inchi_key</th>
      <th>exact_mass</th>
      <th>ppm_error</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>M154T37</td>
      <td>154.062402</td>
      <td>C8H10O3</td>
      <td>Hydroxytyrosol</td>
      <td>InChI=1S/C8H10O3/c9-4-3-6-1-2-7(10)8(11)5-6/h1...</td>
      <td>JUUBCHWRXWPFFH-UHFFFAOYSA-N</td>
      <td>154.06</td>
      <td>-3.84</td>
    </tr>
    <tr>
      <th>1</th>
      <td>M164T119</td>
      <td>164.046774</td>
      <td>C9H8O3</td>
      <td>Phenylpyruvic acid</td>
      <td>InChI=1S/C9H8O3/c10-8(9(11)12)6-7-4-2-1-3-5-7/...</td>
      <td>BTNMPGBKDVTSJY-UHFFFAOYSA-N</td>
      <td>164.05</td>
      <td>-3.47</td>
    </tr>
    <tr>
      <th>2</th>
      <td>M164T119</td>
      <td>164.046774</td>
      <td>C9H8O3</td>
      <td>m-Coumaric acid</td>
      <td>InChI=1S/C9H8O3/c10-8-3-1-2-7(6-8)4-5-9(11)12/...</td>
      <td>KKSDGJDHHZEWEP-SNAWJCMRSA-N</td>
      <td>164.05</td>
      <td>-3.47</td>
    </tr>
    <tr>
      <th>3</th>
      <td>M164T119</td>
      <td>164.046774</td>
      <td>C9H8O3</td>
      <td>4-Hydroxycinnamic acid</td>
      <td>InChI=1S/C9H8O3/c10-8-4-1-7(2-5-8)3-6-9(11)12/...</td>
      <td>NGSWKAQJJWESNS-ZZXKWVIFSA-N</td>
      <td>164.05</td>
      <td>-3.47</td>
    </tr>
    <tr>
      <th>4</th>
      <td>M164T119</td>
      <td>164.046774</td>
      <td>C9H8O3</td>
      <td>2-Hydroxycinnamic acid</td>
      <td>InChI=1S/C9H8O3/c10-8-4-2-1-3-7(8)5-6-9(11)12/...</td>
      <td>PMOWTIHVNWZYFI-AATRIKPKSA-N</td>
      <td>164.05</td>
      <td>-3.47</td>
    </tr>
    <tr>
      <th>5</th>
      <td>M164T233</td>
      <td>164.046832</td>
      <td>C9H8O3</td>
      <td>Phenylpyruvic acid</td>
      <td>InChI=1S/C9H8O3/c10-8(9(11)12)6-7-4-2-1-3-5-7/...</td>
      <td>BTNMPGBKDVTSJY-UHFFFAOYSA-N</td>
      <td>164.05</td>
      <td>-3.12</td>
    </tr>
    <tr>
      <th>6</th>
      <td>M164T233</td>
      <td>164.046832</td>
      <td>C9H8O3</td>
      <td>m-Coumaric acid</td>
      <td>InChI=1S/C9H8O3/c10-8-3-1-2-7(6-8)4-5-9(11)12/...</td>
      <td>KKSDGJDHHZEWEP-SNAWJCMRSA-N</td>
      <td>164.05</td>
      <td>-3.12</td>
    </tr>
    <tr>
      <th>7</th>
      <td>M164T233</td>
      <td>164.046832</td>
      <td>C9H8O3</td>
      <td>4-Hydroxycinnamic acid</td>
      <td>InChI=1S/C9H8O3/c10-8-4-1-7(2-5-8)3-6-9(11)12/...</td>
      <td>NGSWKAQJJWESNS-ZZXKWVIFSA-N</td>
      <td>164.05</td>
      <td>-3.12</td>
    </tr>
    <tr>
      <th>8</th>
      <td>M164T233</td>
      <td>164.046832</td>
      <td>C9H8O3</td>
      <td>2-Hydroxycinnamic acid</td>
      <td>InChI=1S/C9H8O3/c10-8-4-2-1-3-7(8)5-6-9(11)12/...</td>
      <td>PMOWTIHVNWZYFI-AATRIKPKSA-N</td>
      <td>164.05</td>
      <td>-3.12</td>
    </tr>
    <tr>
      <th>9</th>
      <td>M164T53</td>
      <td>164.046825</td>
      <td>C9H8O3</td>
      <td>Phenylpyruvic acid</td>
      <td>InChI=1S/C9H8O3/c10-8(9(11)12)6-7-4-2-1-3-5-7/...</td>
      <td>BTNMPGBKDVTSJY-UHFFFAOYSA-N</td>
      <td>164.05</td>
      <td>-3.16</td>
    </tr>
    <tr>
      <th>10</th>
      <td>M164T53</td>
      <td>164.046825</td>
      <td>C9H8O3</td>
      <td>m-Coumaric acid</td>
      <td>InChI=1S/C9H8O3/c10-8-3-1-2-7(6-8)4-5-9(11)12/...</td>
      <td>KKSDGJDHHZEWEP-SNAWJCMRSA-N</td>
      <td>164.05</td>
      <td>-3.16</td>
    </tr>
    <tr>
      <th>11</th>
      <td>M164T53</td>
      <td>164.046825</td>
      <td>C9H8O3</td>
      <td>4-Hydroxycinnamic acid</td>
      <td>InChI=1S/C9H8O3/c10-8-4-1-7(2-5-8)3-6-9(11)12/...</td>
      <td>NGSWKAQJJWESNS-ZZXKWVIFSA-N</td>
      <td>164.05</td>
      <td>-3.16</td>
    </tr>
    <tr>
      <th>12</th>
      <td>M164T53</td>
      <td>164.046825</td>
      <td>C9H8O3</td>
      <td>2-Hydroxycinnamic acid</td>
      <td>InChI=1S/C9H8O3/c10-8-4-2-1-3-7(8)5-6-9(11)12/...</td>
      <td>PMOWTIHVNWZYFI-AATRIKPKSA-N</td>
      <td>164.05</td>
      <td>-3.16</td>
    </tr>
    <tr>
      <th>13</th>
      <td>M167T35</td>
      <td>167.021095</td>
      <td>C7H5NO4</td>
      <td>Quinolinic acid</td>
      <td>InChI=1S/C7H5NO4/c9-6(10)4-2-1-3-8-5(4)7(11)12...</td>
      <td>GJAWHXHKYYXBSV-UHFFFAOYSA-N</td>
      <td>167.02</td>
      <td>-4.57</td>
    </tr>
    <tr>
      <th>14</th>
      <td>M173T36_3</td>
      <td>173.104423</td>
      <td>C8H15NO3</td>
      <td>Hexanoylglycine</td>
      <td>InChI=1S/C8H15NO3/c1-2-3-4-5-7(10)9-6-8(11)12/...</td>
      <td>UPCKIPHSXMXJOX-UHFFFAOYSA-N</td>
      <td>173.11</td>
      <td>-4.45</td>
    </tr>
    <tr>
      <th>15</th>
      <td>M174T35</td>
      <td>174.088395</td>
      <td>C8H14O4</td>
      <td>Suberic acid</td>
      <td>InChI=1S/C8H14O4/c9-7(10)5-3-1-2-4-6-8(11)12/h...</td>
      <td>TYFQFVWCELRYAO-UHFFFAOYSA-N</td>
      <td>174.09</td>
      <td>-4.67</td>
    </tr>
    <tr>
      <th>16</th>
      <td>M181T36</td>
      <td>181.060407</td>
      <td>C6H7N5O2</td>
      <td>8-Hydroxy-7-methylguanine</td>
      <td>InChI=1S/C6H7N5O2/c1-11-2-3(9-6(11)13)8-5(7)10...</td>
      <td>VHPXSVXJBWZORQ-UHFFFAOYSA-N</td>
      <td>181.06</td>
      <td>2.39</td>
    </tr>
    <tr>
      <th>17</th>
      <td>M212T39</td>
      <td>212.067866</td>
      <td>C10H12O5</td>
      <td>Vanillactic acid</td>
      <td>InChI=1S/C10H12O5/c1-15-9-5-6(2-3-7(9)11)4-8(1...</td>
      <td>SVYIZYRTOYHQRE-UHFFFAOYSA-N</td>
      <td>212.07</td>
      <td>-2.86</td>
    </tr>
    <tr>
      <th>18</th>
      <td>M276T36</td>
      <td>276.077397</td>
      <td>C10H16N2O5S</td>
      <td>Biotin sulfone</td>
      <td>InChI=1S/C10H16N2O5S/c13-8(14)4-2-1-3-7-9-6(5-...</td>
      <td>QPFQYMONYBAUCY-ZKWXMUAHSA-N</td>
      <td>276.08</td>
      <td>-2.16</td>
    </tr>
  </tbody>
</table>
</div>



`match` gives the compound matching results. `lamp` also provides a mass
adjust option by adduct library. You can provide your own adducts library
otherwise `lamp` uses its default adducts library. 

The adducts library looks like:


```python
add_path = './data/adducts_short.tsv'
lib_df = pd.read_csv(add_path, sep="\t")
lib_df
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>label</th>
      <th>exact_mass</th>
      <th>charge</th>
      <th>ion_mode</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>[M+H]+</td>
      <td>1.007276</td>
      <td>1</td>
      <td>pos</td>
    </tr>
    <tr>
      <th>1</th>
      <td>[M+NH4]+</td>
      <td>18.033826</td>
      <td>1</td>
      <td>pos</td>
    </tr>
    <tr>
      <th>2</th>
      <td>[M+Na]+</td>
      <td>22.989221</td>
      <td>1</td>
      <td>pos</td>
    </tr>
    <tr>
      <th>3</th>
      <td>[M+Mg]+</td>
      <td>23.984493</td>
      <td>1</td>
      <td>pos</td>
    </tr>
    <tr>
      <th>4</th>
      <td>[M+K]+</td>
      <td>38.963158</td>
      <td>1</td>
      <td>pos</td>
    </tr>
    <tr>
      <th>5</th>
      <td>[M+Fe]+</td>
      <td>55.934388</td>
      <td>1</td>
      <td>pos</td>
    </tr>
    <tr>
      <th>6</th>
      <td>[M+Cu]+</td>
      <td>62.929049</td>
      <td>1</td>
      <td>pos</td>
    </tr>
    <tr>
      <th>7</th>
      <td>[M+2H]+</td>
      <td>2.015101</td>
      <td>1</td>
      <td>pos</td>
    </tr>
    <tr>
      <th>8</th>
      <td>[M+3H]+</td>
      <td>3.022926</td>
      <td>1</td>
      <td>pos</td>
    </tr>
    <tr>
      <th>9</th>
      <td>[M-H]-</td>
      <td>-1.007276</td>
      <td>1</td>
      <td>neg</td>
    </tr>
    <tr>
      <th>10</th>
      <td>[M+35Cl]-</td>
      <td>34.969401</td>
      <td>1</td>
      <td>neg</td>
    </tr>
    <tr>
      <th>11</th>
      <td>[M+Formate]-</td>
      <td>44.998203</td>
      <td>1</td>
      <td>neg</td>
    </tr>
    <tr>
      <th>12</th>
      <td>[M+Acetate]-</td>
      <td>59.013853</td>
      <td>1</td>
      <td>neg</td>
    </tr>
  </tbody>
</table>
</div>



We use this addcuts file to adjust mass:


```python
ion_mode = "pos"
# if empty, use default adducts library
add_path = "./data/adducts_short.tsv"

lib_add = anno.read_lib(add_path, ion_mode)
lib_add
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>label</th>
      <th>exact_mass</th>
      <th>charge</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>[M+H]+</td>
      <td>1.007276</td>
      <td>1</td>
    </tr>
    <tr>
      <th>1</th>
      <td>[M+NH4]+</td>
      <td>18.033826</td>
      <td>1</td>
    </tr>
    <tr>
      <th>2</th>
      <td>[M+Na]+</td>
      <td>22.989221</td>
      <td>1</td>
    </tr>
    <tr>
      <th>3</th>
      <td>[M+Mg]+</td>
      <td>23.984493</td>
      <td>1</td>
    </tr>
    <tr>
      <th>4</th>
      <td>[M+K]+</td>
      <td>38.963158</td>
      <td>1</td>
    </tr>
    <tr>
      <th>5</th>
      <td>[M+Fe]+</td>
      <td>55.934388</td>
      <td>1</td>
    </tr>
    <tr>
      <th>6</th>
      <td>[M+Cu]+</td>
      <td>62.929049</td>
      <td>1</td>
    </tr>
    <tr>
      <th>7</th>
      <td>[M+2H]+</td>
      <td>2.015101</td>
      <td>1</td>
    </tr>
    <tr>
      <th>8</th>
      <td>[M+3H]+</td>
      <td>3.022926</td>
      <td>1</td>
    </tr>
  </tbody>
</table>
</div>



Now use this function to match compounds:


```python
match_1 = anno.comp_match_mass_add(df, ppm, ref, lib_add)
match_1
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>id</th>
      <th>mz</th>
      <th>molecular_formula</th>
      <th>molecular_name</th>
      <th>inchi</th>
      <th>inchi_key</th>
      <th>exact_mass</th>
      <th>adduct</th>
      <th>ppm_error</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>M152T40</td>
      <td>152.043607</td>
      <td>C5H8N2O2</td>
      <td>Dihydrothymine</td>
      <td>InChI=1S/C5H8N2O2/c1-3-2-6-5(9)7-4(3)8/h3H,2H2...</td>
      <td>NBAKTGXDIBVZOO-VKHMYHEASA-N</td>
      <td>152.04</td>
      <td>[M+Mg]+</td>
      <td>3.52</td>
    </tr>
    <tr>
      <th>1</th>
      <td>M154T37</td>
      <td>154.062402</td>
      <td>C8H8O3</td>
      <td>p-Hydroxyphenylacetic acid</td>
      <td>InChI=1S/C8H8O3/c9-7-3-1-6(2-4-7)5-8(10)11/h1-...</td>
      <td>XQXPVVBIMDBYFF-UHFFFAOYSA-N</td>
      <td>154.06</td>
      <td>[M+2H]+</td>
      <td>-0.28</td>
    </tr>
    <tr>
      <th>2</th>
      <td>M154T37</td>
      <td>154.062402</td>
      <td>C8H8O3</td>
      <td>3-Hydroxyphenylacetic acid</td>
      <td>InChI=1S/C8H8O3/c9-7-3-1-2-6(4-7)5-8(10)11/h1-...</td>
      <td>FVMDYYGIDFPZAX-UHFFFAOYSA-N</td>
      <td>154.06</td>
      <td>[M+2H]+</td>
      <td>-0.28</td>
    </tr>
    <tr>
      <th>3</th>
      <td>M154T37</td>
      <td>154.062402</td>
      <td>C8H8O3</td>
      <td>ortho-Hydroxyphenylacetic acid</td>
      <td>InChI=1S/C8H8O3/c9-7-4-2-1-3-6(7)5-8(10)11/h1-...</td>
      <td>CCVYRRGZDBSHFU-UHFFFAOYSA-N</td>
      <td>154.06</td>
      <td>[M+2H]+</td>
      <td>-0.28</td>
    </tr>
    <tr>
      <th>4</th>
      <td>M154T37</td>
      <td>154.062402</td>
      <td>C8H8O3</td>
      <td>Mandelic acid</td>
      <td>InChI=1S/C8H8O3/c9-7(8(10)11)6-4-2-1-3-5-6/h1-...</td>
      <td>IWYDHOAUDWTVEP-ZETCQYMHSA-N</td>
      <td>154.06</td>
      <td>[M+2H]+</td>
      <td>-0.28</td>
    </tr>
    <tr>
      <th>5</th>
      <td>M154T37</td>
      <td>154.062402</td>
      <td>C8H8O3</td>
      <td>3-Cresotinic acid</td>
      <td>InChI=1S/C8H8O3/c1-5-3-2-4-6(7(5)9)8(10)11/h2-...</td>
      <td>WHSXTWFYRGOBGO-UHFFFAOYSA-N</td>
      <td>154.06</td>
      <td>[M+2H]+</td>
      <td>-0.28</td>
    </tr>
    <tr>
      <th>6</th>
      <td>M154T37</td>
      <td>154.062402</td>
      <td>C8H8O3</td>
      <td>4-Hydroxy-3-methylbenzoic acid</td>
      <td>InChI=1S/C8H8O3/c1-5-4-6(8(10)11)2-3-7(5)9/h2-...</td>
      <td>LTFHNKUKQYVHDX-UHFFFAOYSA-N</td>
      <td>154.06</td>
      <td>[M+2H]+</td>
      <td>-0.28</td>
    </tr>
    <tr>
      <th>7</th>
      <td>M154T37</td>
      <td>154.062402</td>
      <td>C8H8O3</td>
      <td>Vanillin</td>
      <td>InChI=1S/C8H8O3/c1-11-8-4-6(5-9)2-3-7(8)10/h2-...</td>
      <td>MWOOGOJBHIARFG-UHFFFAOYSA-N</td>
      <td>154.06</td>
      <td>[M+2H]+</td>
      <td>-0.28</td>
    </tr>
    <tr>
      <th>8</th>
      <td>M157T35</td>
      <td>157.036819</td>
      <td>C4H10N2O2</td>
      <td>2,4-Diaminobutyric acid</td>
      <td>InChI=1S/C4H10N2O2/c5-2-1-3(6)4(7)8/h3H,1-2,5-...</td>
      <td>OGNSCSPNOLGXSM-UHFFFAOYSA-N</td>
      <td>157.04</td>
      <td>[M+K]+</td>
      <td>-3.61</td>
    </tr>
    <tr>
      <th>9</th>
      <td>M157T35</td>
      <td>157.036819</td>
      <td>C4H10N2O2</td>
      <td>L-2,4-diaminobutyric acid</td>
      <td>InChI=1S/C4H10N2O2/c5-2-1-3(6)4(7)8/h3H,1-2,5-...</td>
      <td>OGNSCSPNOLGXSM-VKHMYHEASA-N</td>
      <td>157.04</td>
      <td>[M+K]+</td>
      <td>-3.61</td>
    </tr>
    <tr>
      <th>10</th>
      <td>M167T35</td>
      <td>167.021095</td>
      <td>C5H8N2O2</td>
      <td>Dihydrothymine</td>
      <td>InChI=1S/C5H8N2O2/c1-3-2-6-5(9)7-4(3)8/h3H,2H2...</td>
      <td>NBAKTGXDIBVZOO-VKHMYHEASA-N</td>
      <td>167.02</td>
      <td>[M+K]+</td>
      <td>-3.83</td>
    </tr>
    <tr>
      <th>11</th>
      <td>M174T35</td>
      <td>174.088395</td>
      <td>C9H13NO</td>
      <td>Phenylpropanolamine</td>
      <td>InChI=1S/C9H13NO/c1-7(10)9(11)8-5-3-2-4-6-8/h2...</td>
      <td>DLNKOYKMWOXYQA-VXNVDRBHSA-N</td>
      <td>174.09</td>
      <td>[M+Na]+</td>
      <td>-3.10</td>
    </tr>
    <tr>
      <th>12</th>
      <td>M174T35</td>
      <td>174.088395</td>
      <td>C10H14O</td>
      <td>Thymol</td>
      <td>InChI=1S/C10H14O/c1-7(2)9-5-4-8(3)6-10(9)11/h4...</td>
      <td>MGSRCZKZVOBKFT-UHFFFAOYSA-N</td>
      <td>174.09</td>
      <td>[M+Mg]+</td>
      <td>-3.23</td>
    </tr>
    <tr>
      <th>13</th>
      <td>M174T35</td>
      <td>174.088395</td>
      <td>C10H14O</td>
      <td>(S)-Carvone</td>
      <td>InChI=1S/C10H14O/c1-7(2)9-5-4-8(3)10(11)6-9/h4...</td>
      <td>ULDHMXUKGWMISQ-VIFPVBQESA-N</td>
      <td>174.09</td>
      <td>[M+Mg]+</td>
      <td>-3.23</td>
    </tr>
    <tr>
      <th>14</th>
      <td>M174T35</td>
      <td>174.088395</td>
      <td>C8H12O4</td>
      <td>2-Octenedioic acid</td>
      <td>InChI=1S/C8H12O4/c9-7(10)5-3-1-2-4-6-8(11)12/h...</td>
      <td>BNTPVRGYUHJFHN-HWKANZROSA-N</td>
      <td>174.09</td>
      <td>[M+2H]+</td>
      <td>-1.52</td>
    </tr>
    <tr>
      <th>15</th>
      <td>M174T35</td>
      <td>174.088395</td>
      <td>C8H12O4</td>
      <td>cis-4-Octenedioic acid</td>
      <td>InChI=1S/C8H12O4/c9-7(10)5-3-1-2-4-6-8(11)12/h...</td>
      <td>LQVYKEXVMZXOAH-UPHRSURJSA-N</td>
      <td>174.09</td>
      <td>[M+2H]+</td>
      <td>-1.52</td>
    </tr>
    <tr>
      <th>16</th>
      <td>M181T36</td>
      <td>181.060407</td>
      <td>C8H8N2O3</td>
      <td>Nicotinuric acid</td>
      <td>InChI=1S/C8H8N2O3/c11-7(12)5-10-8(13)6-2-1-3-9...</td>
      <td>ZBSGKPYXQINNGF-UHFFFAOYSA-N</td>
      <td>181.06</td>
      <td>[M+H]+</td>
      <td>-1.99</td>
    </tr>
    <tr>
      <th>17</th>
      <td>M184T38</td>
      <td>184.097942</td>
      <td>C10H13N2</td>
      <td>Nicotine imine</td>
      <td>InChI=1S/C10H13N2/c1-12-7-3-5-10(12)9-4-2-6-11...</td>
      <td>GTQXYYYOJZZJHL-UHFFFAOYSA-N</td>
      <td>184.10</td>
      <td>[M+Na]+</td>
      <td>4.61</td>
    </tr>
    <tr>
      <th>18</th>
      <td>M185T39_2</td>
      <td>185.082034</td>
      <td>C5H15NO4P</td>
      <td>Phosphorylcholine</td>
      <td>InChI=1S/C5H14NO4P/c1-6(2,3)4-5-10-11(7,8)9/h4...</td>
      <td>YHHSONZFOIEMCP-UHFFFAOYSA-O</td>
      <td>185.08</td>
      <td>[M+H]+</td>
      <td>4.80</td>
    </tr>
    <tr>
      <th>19</th>
      <td>M186T36</td>
      <td>186.045606</td>
      <td>C6H14N2O</td>
      <td>N-Acetylputrescine</td>
      <td>InChI=1S/C6H14N2O/c1-6(9)8-5-3-2-4-7/h2-5,7H2,...</td>
      <td>KLZGKIDSEJWEDW-UHFFFAOYSA-N</td>
      <td>186.05</td>
      <td>[M+Fe]+</td>
      <td>3.25</td>
    </tr>
    <tr>
      <th>20</th>
      <td>M187T38</td>
      <td>187.097642</td>
      <td>C5H15NO4P</td>
      <td>Phosphorylcholine</td>
      <td>InChI=1S/C5H14NO4P/c1-6(2,3)4-5-10-11(7,8)9/h4...</td>
      <td>YHHSONZFOIEMCP-UHFFFAOYSA-O</td>
      <td>187.10</td>
      <td>[M+3H]+</td>
      <td>4.52</td>
    </tr>
    <tr>
      <th>21</th>
      <td>M193T40</td>
      <td>193.050761</td>
      <td>C5H14N4</td>
      <td>Agmatine</td>
      <td>InChI=1S/C5H14N4/c6-3-1-2-4-9-5(7)8/h1-4,6H2,(...</td>
      <td>QYPPJABKJHAVHS-UHFFFAOYSA-N</td>
      <td>193.05</td>
      <td>[M+Cu]+</td>
      <td>-0.69</td>
    </tr>
    <tr>
      <th>22</th>
      <td>M200T36</td>
      <td>200.061328</td>
      <td>C7H16N2O</td>
      <td>N-Acetylcadaverine</td>
      <td>InChI=1S/C7H16N2O/c1-7(10)9-6-4-2-3-5-8/h2-6,8...</td>
      <td>RMOIHHAKNOFHOE-UHFFFAOYSA-N</td>
      <td>200.06</td>
      <td>[M+Fe]+</td>
      <td>3.39</td>
    </tr>
    <tr>
      <th>23</th>
      <td>M201T39_1</td>
      <td>201.051849</td>
      <td>C10H10O3</td>
      <td>4-Methoxycinnamic acid</td>
      <td>InChI=1S/C10H10O3/c1-13-9-5-2-8(3-6-9)4-7-10(1...</td>
      <td>AFDXODALSZRGIH-QPJJXVBHSA-N</td>
      <td>201.05</td>
      <td>[M+Na]+</td>
      <td>-1.82</td>
    </tr>
    <tr>
      <th>24</th>
      <td>M203T36_1</td>
      <td>203.002108</td>
      <td>C9H9NO</td>
      <td>Indole-3-carbinol</td>
      <td>InChI=1S/C9H9NO/c11-6-7-5-10-9-4-2-1-3-8(7)9/h...</td>
      <td>IVYPNXXAYMYVSP-UHFFFAOYSA-N</td>
      <td>203.00</td>
      <td>[M+Fe]+</td>
      <td>-3.42</td>
    </tr>
    <tr>
      <th>25</th>
      <td>M212T39</td>
      <td>212.067866</td>
      <td>C8H15NO3</td>
      <td>Hexanoylglycine</td>
      <td>InChI=1S/C8H15NO3/c1-2-3-4-5-7(10)9-6-8(11)12/...</td>
      <td>UPCKIPHSXMXJOX-UHFFFAOYSA-N</td>
      <td>212.07</td>
      <td>[M+K]+</td>
      <td>-2.29</td>
    </tr>
    <tr>
      <th>26</th>
      <td>M212T39</td>
      <td>212.067866</td>
      <td>C10H10O5</td>
      <td>Vanilpyruvic acid</td>
      <td>InChI=1S/C10H10O5/c1-15-9-5-6(2-3-7(9)11)4-8(1...</td>
      <td>YGQHQTMRZPHIBB-UHFFFAOYSA-N</td>
      <td>212.07</td>
      <td>[M+2H]+</td>
      <td>-0.28</td>
    </tr>
    <tr>
      <th>27</th>
      <td>M217T37_1</td>
      <td>217.018279</td>
      <td>C10H11NO</td>
      <td>Tryptophol</td>
      <td>InChI=1S/C10H11NO/c12-6-5-8-7-11-10-4-2-1-3-9(...</td>
      <td>MBBOMCVGYCRMEA-UHFFFAOYSA-N</td>
      <td>217.02</td>
      <td>[M+Fe]+</td>
      <td>-0.79</td>
    </tr>
    <tr>
      <th>28</th>
      <td>M221T37</td>
      <td>221.012328</td>
      <td>C9H11NO2</td>
      <td>L-Phenylalanine</td>
      <td>InChI=1S/C9H11NO2/c10-8(9(11)12)6-7-4-2-1-3-5-...</td>
      <td>COLNVLDHVKWLRT-QMMMGPOBSA-N</td>
      <td>221.01</td>
      <td>[M+Fe]+</td>
      <td>-4.70</td>
    </tr>
    <tr>
      <th>29</th>
      <td>M223T38</td>
      <td>223.008162</td>
      <td>C4H10NO6P</td>
      <td>O-Phosphothreonine</td>
      <td>InChI=1S/C4H10NO6P/c1-2(3(5)4(6)7)11-12(8,9)10...</td>
      <td>USRGIUJOYOXOQJ-GBXIJSLDSA-N</td>
      <td>223.01</td>
      <td>[M+Mg]+</td>
      <td>-4.06</td>
    </tr>
    <tr>
      <th>30</th>
      <td>M223T40</td>
      <td>223.096863</td>
      <td>C12H14O4</td>
      <td>Monoisobutyl phthalic acid</td>
      <td>InChI=1S/C12H14O4/c1-8(2)7-16-12(15)10-6-4-3-5...</td>
      <td>RZJSUWQGFCHNFS-UHFFFAOYSA-N</td>
      <td>223.10</td>
      <td>[M+H]+</td>
      <td>1.69</td>
    </tr>
    <tr>
      <th>31</th>
      <td>M226T44</td>
      <td>226.128007</td>
      <td>C8H18N4O2</td>
      <td>Asymmetric dimethylarginine</td>
      <td>InChI=1S/C8H18N4O2/c1-12(2)8(10)11-5-3-4-6(9)7...</td>
      <td>YDGMGEXADBMOMJ-LURJTMIESA-N</td>
      <td>226.13</td>
      <td>[M+Mg]+</td>
      <td>2.38</td>
    </tr>
    <tr>
      <th>32</th>
      <td>M226T44</td>
      <td>226.128007</td>
      <td>C8H18N4O2</td>
      <td>Symmetric dimethylarginine</td>
      <td>InChI=1S/C8H18N4O2/c1-10-8(11-2)12-5-3-4-6(9)7...</td>
      <td>HVPFXCBJHIIJGS-LURJTMIESA-N</td>
      <td>226.13</td>
      <td>[M+Mg]+</td>
      <td>2.38</td>
    </tr>
    <tr>
      <th>33</th>
      <td>M227T36</td>
      <td>227.066175</td>
      <td>C9H10N2O5</td>
      <td>3-Nitrotyrosine</td>
      <td>InChI=1S/C9H10N2O5/c10-6(9(13)14)3-5-1-2-8(12)...</td>
      <td>FBTSQILOGYXGMD-LURJTMIESA-N</td>
      <td>227.07</td>
      <td>[M+H]+</td>
      <td>-0.32</td>
    </tr>
    <tr>
      <th>34</th>
      <td>M229T38</td>
      <td>229.069418</td>
      <td>C4H10N3O5P</td>
      <td>Phosphocreatine</td>
      <td>InChI=1S/C4H10N3O5P/c1-7(2-3(8)9)4(5)6-13(10,1...</td>
      <td>DRBBFCLWYRJSJZ-UHFFFAOYSA-N</td>
      <td>229.07</td>
      <td>[M+NH4]+</td>
      <td>-0.94</td>
    </tr>
    <tr>
      <th>35</th>
      <td>M233T38</td>
      <td>233.043479</td>
      <td>C8H10N4O2</td>
      <td>Caffeine</td>
      <td>InChI=1S/C8H10N4O2/c1-10-4-9-6-5(10)7(13)12(3)...</td>
      <td>RYYVLZVUVIJVGH-UHFFFAOYSA-N</td>
      <td>233.04</td>
      <td>[M+K]+</td>
      <td>-0.23</td>
    </tr>
    <tr>
      <th>36</th>
      <td>M245T44</td>
      <td>245.045772</td>
      <td>C7H15N3O3</td>
      <td>Homocitrulline</td>
      <td>InChI=1S/C7H15N3O3/c8-5(6(11)12)3-1-2-4-10-7(9...</td>
      <td>XIGSAGMEBXLVJJ-YFKPBYRVSA-N</td>
      <td>245.05</td>
      <td>[M+Fe]+</td>
      <td>0.17</td>
    </tr>
    <tr>
      <th>37</th>
      <td>M245T37_2</td>
      <td>245.093315</td>
      <td>C13H18O2</td>
      <td>Ibuprofen</td>
      <td>InChI=1S/C13H18O2/c1-9(2)8-11-4-6-12(7-5-11)10...</td>
      <td>HEFNNWSXXWATRW-UHFFFAOYSA-N</td>
      <td>245.09</td>
      <td>[M+K]+</td>
      <td>-2.13</td>
    </tr>
    <tr>
      <th>38</th>
      <td>M249T38</td>
      <td>249.038309</td>
      <td>C8H10N4O3</td>
      <td>1,3,7-Trimethyluric acid</td>
      <td>InChI=1S/C8H10N4O3/c1-10-4-5(9-7(10)14)11(2)8(...</td>
      <td>BYXCFUMGEBZDDI-UHFFFAOYSA-N</td>
      <td>249.04</td>
      <td>[M+K]+</td>
      <td>-0.56</td>
    </tr>
    <tr>
      <th>39</th>
      <td>M261T43</td>
      <td>260.972975</td>
      <td>C10H7NO4</td>
      <td>Xanthurenic acid</td>
      <td>InChI=1S/C10H7NO4/c12-7-3-1-2-5-8(13)4-6(10(14...</td>
      <td>FBZONXHGGPHHIY-UHFFFAOYSA-N</td>
      <td>260.97</td>
      <td>[M+Fe]+</td>
      <td>4.13</td>
    </tr>
    <tr>
      <th>40</th>
      <td>M269T37_2</td>
      <td>269.088048</td>
      <td>C10H12N4O5</td>
      <td>Inosine</td>
      <td>InChI=1S/C10H12N4O5/c15-1-4-6(16)7(17)10(19-4)...</td>
      <td>UGQMRVRMYYASKQ-KQYNXXCUSA-N</td>
      <td>269.09</td>
      <td>[M+H]+</td>
      <td>0.01</td>
    </tr>
    <tr>
      <th>41</th>
      <td>M275T168</td>
      <td>275.201932</td>
      <td>C18H24O2</td>
      <td>Estradiol</td>
      <td>InChI=1S/C18H24O2/c1-18-9-8-14-13-5-3-12(19)10...</td>
      <td>VOXZDWNPVJITMN-ZBRFXRBCSA-N</td>
      <td>275.20</td>
      <td>[M+3H]+</td>
      <td>5.00</td>
    </tr>
    <tr>
      <th>42</th>
      <td>M275T168</td>
      <td>275.201932</td>
      <td>C18H24O2</td>
      <td>17a-Estradiol</td>
      <td>InChI=1S/C18H24O2/c1-18-9-8-14-13-5-3-12(19)10...</td>
      <td>VOXZDWNPVJITMN-SFFUCWETSA-N</td>
      <td>275.20</td>
      <td>[M+3H]+</td>
      <td>5.00</td>
    </tr>
    <tr>
      <th>43</th>
      <td>M277T181</td>
      <td>277.217564</td>
      <td>C18H28O2</td>
      <td>19-Norandrosterone</td>
      <td>InChI=1S/C18H28O2/c1-18-9-8-14-13-5-3-12(19)10...</td>
      <td>UOUIARGWRPHDBX-CQZDKXCPSA-N</td>
      <td>277.22</td>
      <td>[M+H]+</td>
      <td>4.90</td>
    </tr>
    <tr>
      <th>44</th>
      <td>M277T181</td>
      <td>277.217564</td>
      <td>C18H28O2</td>
      <td>19-Noretiocholanolone</td>
      <td>InChI=1S/C18H28O2/c1-18-9-8-14-13-5-3-12(19)10...</td>
      <td>UOUIARGWRPHDBX-DHMVHTBWSA-N</td>
      <td>277.22</td>
      <td>[M+H]+</td>
      <td>4.90</td>
    </tr>
    <tr>
      <th>45</th>
      <td>M278T71</td>
      <td>278.148195</td>
      <td>C11H20N2O6</td>
      <td>Saccharopine</td>
      <td>InChI=1S/C11H20N2O6/c12-7(10(16)17)3-1-2-6-13-...</td>
      <td>ZDGJAHTZVHVLOT-YUMQZZPRSA-N</td>
      <td>278.15</td>
      <td>[M+2H]+</td>
      <td>3.44</td>
    </tr>
    <tr>
      <th>46</th>
      <td>M279T233</td>
      <td>279.233232</td>
      <td>C18H30O2</td>
      <td>alpha-Linolenic acid</td>
      <td>InChI=1S/C18H30O2/c1-2-3-4-5-6-7-8-9-10-11-12-...</td>
      <td>DTOSIQBPPRVQHS-PDBXOOCHSA-N</td>
      <td>279.23</td>
      <td>[M+H]+</td>
      <td>4.93</td>
    </tr>
    <tr>
      <th>47</th>
      <td>M279T233</td>
      <td>279.233232</td>
      <td>C18H28O2</td>
      <td>19-Norandrosterone</td>
      <td>InChI=1S/C18H28O2/c1-18-9-8-14-13-5-3-12(19)10...</td>
      <td>UOUIARGWRPHDBX-CQZDKXCPSA-N</td>
      <td>279.23</td>
      <td>[M+3H]+</td>
      <td>4.93</td>
    </tr>
    <tr>
      <th>48</th>
      <td>M279T233</td>
      <td>279.233232</td>
      <td>C18H28O2</td>
      <td>19-Noretiocholanolone</td>
      <td>InChI=1S/C18H28O2/c1-18-9-8-14-13-5-3-12(19)10...</td>
      <td>UOUIARGWRPHDBX-DHMVHTBWSA-N</td>
      <td>279.23</td>
      <td>[M+3H]+</td>
      <td>4.93</td>
    </tr>
    <tr>
      <th>49</th>
      <td>M281T287</td>
      <td>281.248903</td>
      <td>C18H32O2</td>
      <td>Linoleic acid</td>
      <td>InChI=1S/C18H32O2/c1-2-3-4-5-6-7-8-9-10-11-12-...</td>
      <td>OYHQOLUKZRVURQ-HZJYTTRNSA-N</td>
      <td>281.25</td>
      <td>[M+H]+</td>
      <td>4.97</td>
    </tr>
    <tr>
      <th>50</th>
      <td>M281T287</td>
      <td>281.248903</td>
      <td>C18H30O2</td>
      <td>alpha-Linolenic acid</td>
      <td>InChI=1S/C18H30O2/c1-2-3-4-5-6-7-8-9-10-11-12-...</td>
      <td>DTOSIQBPPRVQHS-PDBXOOCHSA-N</td>
      <td>281.25</td>
      <td>[M+3H]+</td>
      <td>4.97</td>
    </tr>
    <tr>
      <th>51</th>
      <td>M282T61</td>
      <td>282.070271</td>
      <td>C10H14N2O6</td>
      <td>Ribothymidine</td>
      <td>InChI=1S/C10H14N2O6/c1-4-2-12(10(17)11-8(4)16)...</td>
      <td>DWRXFEITVBNRMK-JXOAFFINSA-N</td>
      <td>282.07</td>
      <td>[M+Mg]+</td>
      <td>2.10</td>
    </tr>
    <tr>
      <th>52</th>
      <td>M282T61</td>
      <td>282.070271</td>
      <td>C10H14N2O6</td>
      <td>3-Methyluridine</td>
      <td>InChI=1S/C10H14N2O6/c1-11-6(14)2-3-12(10(11)17...</td>
      <td>UTQUILVPBZEHTK-UHFFFAOYSA-N</td>
      <td>282.07</td>
      <td>[M+Mg]+</td>
      <td>2.10</td>
    </tr>
    <tr>
      <th>53</th>
      <td>M283T37</td>
      <td>283.103695</td>
      <td>C11H14N4O5</td>
      <td>1-Methylinosine</td>
      <td>InChI=1S/C11H14N4O5/c1-14-3-13-9-6(10(14)19)12...</td>
      <td>WJNGQIYEQLPJMN-IOSLPCCCSA-N</td>
      <td>283.10</td>
      <td>[M+H]+</td>
      <td>-0.01</td>
    </tr>
  </tbody>
</table>
</div>



## Correlation analysis

Next step is correlation analysis, based on intensity data matrix along all
peaks. All results are filtered by the correlation coefficient, p-values
and retention time difference. That is: keep correlation results in an
retention time differences/windows(such as 1 seconds) with correlation
coefficient larger than a threshold(such as 0.5) and their correlation
p-values less than a threshold (such as 0.05).

`lamp` uses one of correlation methods, either `pearson` or `spearman`. Also
parameter `positive` allows user to select only positive correlation results.

Two functions, `_tic` and `_toc`, record the correlation computation time in
seconds. 


```python
thres_rt = 1.0
thres_corr = 0.5
thres_pval = 0.05
method = "spearman"   # "pearson"
positive = True

utils._tic()
corr = stats.comp_corr_rt(df, thres_rt, thres_corr, thres_pval, method,
                          positive)
utils._toc()
corr
```

    Elapsed time: 4.283773899078369 seconds.
    




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>name_a</th>
      <th>name_b</th>
      <th>r_value</th>
      <th>p_value</th>
      <th>rt_diff</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>M151T34</td>
      <td>M153T34</td>
      <td>0.80</td>
      <td>1.267076e-23</td>
      <td>0.02</td>
    </tr>
    <tr>
      <th>1</th>
      <td>M151T34</td>
      <td>M155T34</td>
      <td>0.71</td>
      <td>1.752854e-16</td>
      <td>0.20</td>
    </tr>
    <tr>
      <th>2</th>
      <td>M151T34</td>
      <td>M161T34</td>
      <td>0.78</td>
      <td>1.869949e-21</td>
      <td>0.14</td>
    </tr>
    <tr>
      <th>3</th>
      <td>M151T34</td>
      <td>M163T34</td>
      <td>0.69</td>
      <td>3.239594e-15</td>
      <td>0.20</td>
    </tr>
    <tr>
      <th>4</th>
      <td>M151T34</td>
      <td>M167T35</td>
      <td>0.51</td>
      <td>5.776482e-08</td>
      <td>0.73</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>1783</th>
      <td>M283T34_1</td>
      <td>M283T34_2</td>
      <td>0.62</td>
      <td>4.214876e-12</td>
      <td>0.29</td>
    </tr>
    <tr>
      <th>1784</th>
      <td>M283T34_1</td>
      <td>M285T34</td>
      <td>0.82</td>
      <td>5.937139e-26</td>
      <td>0.08</td>
    </tr>
    <tr>
      <th>1785</th>
      <td>M283T34_2</td>
      <td>M285T34</td>
      <td>0.66</td>
      <td>7.898957e-14</td>
      <td>0.37</td>
    </tr>
    <tr>
      <th>1786</th>
      <td>M283T60</td>
      <td>M284T60</td>
      <td>0.86</td>
      <td>1.033010e-29</td>
      <td>0.15</td>
    </tr>
    <tr>
      <th>1787</th>
      <td>M283T339</td>
      <td>M284T339</td>
      <td>0.91</td>
      <td>4.031333e-39</td>
      <td>0.04</td>
    </tr>
  </tbody>
</table>
<p>1788 rows × 5 columns</p>
</div>



Based on the correlation analysis, we can extract the groups and their size by:


```python
# get correlation group and size
corr_df = stats.corr_grp_size(corr)
corr_df
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>name</th>
      <th>cor_grp_size</th>
      <th>cor_grp</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>M219T35</td>
      <td>52</td>
      <td>M221T34::M223T34::M225T35::M226T35::M229T34::M...</td>
    </tr>
    <tr>
      <th>1</th>
      <td>M216T35</td>
      <td>52</td>
      <td>M217T35::M218T35::M219T34::M219T35::M221T34::M...</td>
    </tr>
    <tr>
      <th>2</th>
      <td>M217T35</td>
      <td>52</td>
      <td>M218T35::M219T34::M219T35::M221T34::M223T34::M...</td>
    </tr>
    <tr>
      <th>3</th>
      <td>M215T35</td>
      <td>52</td>
      <td>M216T35::M217T35::M218T35::M219T34::M219T35::M...</td>
    </tr>
    <tr>
      <th>4</th>
      <td>M218T35</td>
      <td>51</td>
      <td>M219T34::M219T35::M221T34::M223T34::M225T35::M...</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>335</th>
      <td>M173T119</td>
      <td>1</td>
      <td>M171T119</td>
    </tr>
    <tr>
      <th>336</th>
      <td>M277T71</td>
      <td>1</td>
      <td>M278T71</td>
    </tr>
    <tr>
      <th>337</th>
      <td>M259T233</td>
      <td>1</td>
      <td>M191T233</td>
    </tr>
    <tr>
      <th>338</th>
      <td>M284T60</td>
      <td>1</td>
      <td>M283T60</td>
    </tr>
    <tr>
      <th>339</th>
      <td>M266T66</td>
      <td>1</td>
      <td>M265T66</td>
    </tr>
  </tbody>
</table>
<p>340 rows × 3 columns</p>
</div>



## Summarize results

The final step gets the summary table in different format and save for the 
further analysis.


```python
# get summary of metabolite annotation
sr, mr = anno.comp_summ(df, match)
```

This function combines peak table with compound matching results and returns 
two results in different formats. `sr` is single row results for each peak id
in peak table `df`:


```python
sr
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>name</th>
      <th>mz</th>
      <th>rt</th>
      <th>exact_mass</th>
      <th>ppm_error</th>
      <th>molecular_formula</th>
      <th>molecular_name</th>
      <th>inchi</th>
      <th>inchi_key</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>M151T34</td>
      <td>150.886715</td>
      <td>34.152700</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>1</th>
      <td>M151T40</td>
      <td>151.040235</td>
      <td>39.838172</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2</th>
      <td>M152T40</td>
      <td>152.043607</td>
      <td>40.303700</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>3</th>
      <td>M153T34</td>
      <td>152.883824</td>
      <td>34.174647</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>4</th>
      <td>M153T36</td>
      <td>153.019474</td>
      <td>35.785847</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>395</th>
      <td>M283T61</td>
      <td>283.068474</td>
      <td>60.739869</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>396</th>
      <td>M284T108</td>
      <td>284.223499</td>
      <td>108.406389</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>397</th>
      <td>M284T339</td>
      <td>284.267962</td>
      <td>338.725056</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>398</th>
      <td>M284T60</td>
      <td>284.195294</td>
      <td>59.593561</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>399</th>
      <td>M285T34</td>
      <td>284.775031</td>
      <td>34.079641</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
  </tbody>
</table>
<p>400 rows × 9 columns</p>
</div>



`mr` is multiple rows format if the match more than once from the reference
file:


```python
mr
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>name</th>
      <th>mz</th>
      <th>rt</th>
      <th>molecular_formula</th>
      <th>molecular_name</th>
      <th>inchi</th>
      <th>inchi_key</th>
      <th>exact_mass</th>
      <th>ppm_error</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>M151T34</td>
      <td>150.886715</td>
      <td>34.152700</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>1</th>
      <td>M151T40</td>
      <td>151.040235</td>
      <td>39.838172</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2</th>
      <td>M152T40</td>
      <td>152.043607</td>
      <td>40.303700</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>3</th>
      <td>M153T34</td>
      <td>152.883824</td>
      <td>34.174647</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>4</th>
      <td>M153T36</td>
      <td>153.019474</td>
      <td>35.785847</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>404</th>
      <td>M283T61</td>
      <td>283.068474</td>
      <td>60.739869</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>405</th>
      <td>M284T108</td>
      <td>284.223499</td>
      <td>108.406389</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>406</th>
      <td>M284T339</td>
      <td>284.267962</td>
      <td>338.725056</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>407</th>
      <td>M284T60</td>
      <td>284.195294</td>
      <td>59.593561</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>408</th>
      <td>M285T34</td>
      <td>284.775031</td>
      <td>34.079641</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
  </tbody>
</table>
<p>409 rows × 9 columns</p>
</div>




Now we merges single format results with correlation results:


```python
# merge summery table with correlation analysis
res = anno.comp_summ_corr(sr, corr_df)
res
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>name</th>
      <th>mz</th>
      <th>rt</th>
      <th>exact_mass</th>
      <th>ppm_error</th>
      <th>molecular_formula</th>
      <th>molecular_name</th>
      <th>inchi</th>
      <th>inchi_key</th>
      <th>cor_grp_size</th>
      <th>cor_grp</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>M167T35</td>
      <td>167.021095</td>
      <td>34.882147</td>
      <td>167.02</td>
      <td>-4.57</td>
      <td>C7H5NO4</td>
      <td>Quinolinic acid</td>
      <td>InChI=1S/C7H5NO4/c9-6(10)4-2-1-3-8-5(4)7(11)12...</td>
      <td>GJAWHXHKYYXBSV-UHFFFAOYSA-N</td>
      <td>25.0</td>
      <td>M171T34::M197T36::M209T34::M211T34::M213T34::M...</td>
    </tr>
    <tr>
      <th>1</th>
      <td>M276T36</td>
      <td>276.077397</td>
      <td>36.385373</td>
      <td>276.08</td>
      <td>-2.16</td>
      <td>C10H16N2O5S</td>
      <td>Biotin sulfone</td>
      <td>InChI=1S/C10H16N2O5S/c13-8(14)4-2-1-3-7-9-6(5-...</td>
      <td>QPFQYMONYBAUCY-ZKWXMUAHSA-N</td>
      <td>13.0</td>
      <td>M277T36_2::M278T36::M173T36_2::M186T36::M187T3...</td>
    </tr>
    <tr>
      <th>2</th>
      <td>M154T37</td>
      <td>154.062402</td>
      <td>37.183625</td>
      <td>154.06</td>
      <td>-3.84</td>
      <td>C8H10O3</td>
      <td>Hydroxytyrosol</td>
      <td>InChI=1S/C8H10O3/c9-4-3-6-1-2-7(10)8(11)5-6/h1...</td>
      <td>JUUBCHWRXWPFFH-UHFFFAOYSA-N</td>
      <td>12.0</td>
      <td>M155T38::M158T37_2::M164T36::M171T37_2::M173T3...</td>
    </tr>
    <tr>
      <th>3</th>
      <td>M174T35</td>
      <td>174.088395</td>
      <td>35.001130</td>
      <td>174.09</td>
      <td>-4.67</td>
      <td>C8H14O4</td>
      <td>Suberic acid</td>
      <td>InChI=1S/C8H14O4/c9-7(10)5-3-1-2-4-6-8(11)12/h...</td>
      <td>TYFQFVWCELRYAO-UHFFFAOYSA-N</td>
      <td>9.0</td>
      <td>M211T34::M213T34::M219T34::M221T34::M229T35::M...</td>
    </tr>
    <tr>
      <th>4</th>
      <td>M181T36</td>
      <td>181.060407</td>
      <td>35.734801</td>
      <td>181.06</td>
      <td>2.39</td>
      <td>C6H7N5O2</td>
      <td>8-Hydroxy-7-methylguanine</td>
      <td>InChI=1S/C6H7N5O2/c1-11-2-3(9-6(11)13)8-5(7)10...</td>
      <td>VHPXSVXJBWZORQ-UHFFFAOYSA-N</td>
      <td>9.0</td>
      <td>M224T36::M225T35::M226T35::M227T36::M269T37_2:...</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>395</th>
      <td>M279T50</td>
      <td>279.159930</td>
      <td>50.055451</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>396</th>
      <td>M279T79</td>
      <td>279.163910</td>
      <td>78.758079</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>397</th>
      <td>M282T85</td>
      <td>282.207859</td>
      <td>84.719202</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>398</th>
      <td>M283T47</td>
      <td>283.110871</td>
      <td>46.822069</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>399</th>
      <td>M284T108</td>
      <td>284.223499</td>
      <td>108.406389</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
  </tbody>
</table>
<p>400 rows × 11 columns</p>
</div>



The result data frame `res` is re-arranged as four parts from top to bottom:
 
 - 1st part: identified metabolites, satisfied with correlation analysis
 - 2nd part: identified metabolites, not satisfied with correlation
 - 3rd part: no identified metabolites, satisfied with correlation
 - 4th part: no identified metabolites, not satisfied with correlation

The users should focus on the first part and perform their further analysis. 

You can save all results in different forms, such as text format TSV or CSV.
You can also save all results `sqlite3` database and use 
[DB Browser for SQLite](https://sqlitebrowser.org/) to view: 


```python
import sqlite3

f_save = False   # here we do NOT save results
db_out = "test.db"
sr_out = "test_s.tsv"

if f_save:
    # save all results into a sqlite3 database
    conn = sqlite3.connect(db_out)
    df[["name", "mz", "rt"]].to_sql("peaklist", conn,
                                    if_exists="replace", index=False)
    corr_df.to_sql("corr_grp", conn, if_exists="replace", index=False)
    corr.to_sql("corr_pval_rt", conn, if_exists="replace", index=False)
    match.to_sql("match", conn, if_exists="replace", index=False)
    mr.to_sql("anno_mr", conn, if_exists="replace", index=False)
    res.to_sql("anno_sr", conn, if_exists="replace", index=False)

    conn.commit()
    conn.close()

    # save final results
    res.to_csv(sr_out, sep="\t", index=False)

```

## End user usages

For end users, `lamp` has two options: command line interface or graphical
user interface.

To use GUI,  open a terminal and type in:

```bash
$ lamp gui
```

To use CLI, open a terminal and type in something like:

```bash
$ lamp cli \
  --sep "tab" \
  --input-data "./data/df_pos_3.tsv" \
  --col-idx "1, 2, 3, 4" \
  --add-path "" \
  --ref-path "" \
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
```

Or you can create a bash script `lamp_cli.sh` (Linux and MacOS) or
Windows script `lamp_cli.bat`  to contain these CLI arguments and run:

- For Linux and MacOS terminal:

  ```bash
  $ chmod +x lamp_cli.sh   
  $ ./lamp_cli.sh
  ```

- For Windows terminal:

  ```bash
  $ lamp_cli.bat
  ```


