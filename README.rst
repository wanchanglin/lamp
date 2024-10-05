LAMP - Liverpool Annotation of metabolites using Mass sPectrometry
==================================================================

Introduction
------------

The annotation or identification of metabolites detected in untargeted
metabolomics studies applying liquid chromatography-mass spectrometry can
apply full-scan (MS1), retention time (RT) and gas-phase fragmentation
(MS/MS) data. Full-scan MS1 data can be applied as a first pass to decrease
the number of possible annotations. However, electrospray ionisation is a
complex process which generates multiple features (m/z-RT pairs) for each
metabolite. The grouping of features and subsequent linkage to a single or
multiple molecular formula is required to maximise true positive annotations
and minimise false positive annotations.

LAMP is a Python package as an easy-to-use software for feature grouping
and metabolite annotation using MS1 data only. LAMPS groups features based
on RT similarity and positive correlations across multiple biological
samples. Genome-scale metabolic models are the source of metabolites applied
in reference files though any source of metabolites can be used (e.g. HMDB
or LIPID MAPS). The m/z differences related to in-source fragments, adducts,
isotopes, oligomers and charge states can be user-defined in the reference
file. 
