Introduction to LAMP
====================

Untargeted metabolomics studies routinely apply liquid chromatography-mass
spectrometry to acquire data for hundreds or low thousands of metabolites
and exposome-related (bio)chemicals. The annotation or higher-confidence
identification of metabolites and biochemicals can apply multiple different
data types (1) chromatographic retention time, (2) the mass-to-charge
(*m/z*) ratio of ions formed during electrospray ionisation for the
structurally intact metabolite or (bio)chemical and (3) fragmentation mass
spectra derived from MS/MS or MS\ :sup:`n` experiments.

Commonly, the mass-to-charge (*m/z*) ratio of ions formed during
electrospray ionisation for the structurally intact metabolite are applied
as a first step in the annotation process. Importantly, a single metabolite
can be detected as multiple different ion types (adducts, isotopes,
in-source fragments, oligomers) and grouping together of features
representing the same metabolite or biochemical can decrease the number of
false positive annotations. The Liverpool Annotation of metabolites using
Mass sPectrometry (LAMP) is a Python package and an easy-to-use software for
feature grouping and metabolite annotation using MS1 data only. LAMP groups
features based on chromatographic retention time similarity and positive
response-based correlations across multiple biological samples. Genome-scale
metabolic models are the source of metabolites applied in the standard
reference files though any source of metabolites can be used (e.g. HMDB or
LIPIDMAPS). The *m/z* differences related to in-source fragments, adducts,
isotopes, oligomers and charge states can be user-defined in the reference
file.
