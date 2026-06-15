# Key Research Groups and Papers in Paleo-ML

## What it is
A field guide to the core literature in ML-applied paleontology, organized by subfield.

---

## Footprint Analysis

**Lallensack et al. (2022)**
Journal of Vertebrate Paleontology.
Trained a supervised deep convolutional neural network to classify dinosaur footprints by ichnotaxon.
This establishes the supervised baseline for the field, but the labels encode contested taxonomic interpretations, so the classifier inherits those disputes and generalizes poorly across collections with different naming conventions.

**Hartmann et al. (2026)**
PNAS.
Trained a beta-VAE on dinosaur footprint images without any labels, learning a continuous latent space of footprint shapes (DinoTracker).
Because no labels are used, the model sidesteps taxonomic bias entirely and enables similarity search, clustering, and anomaly detection across footprint collections, regardless of what experts have called them.

---

## CT Segmentation

**Yu et al. (2022)**
First published deep learning segmentation of dinosaur CT scans, using a CNN to separate bone voxels from surrounding rock matrix.
This is the proof of concept that the task is tractable at all. The main limitation is that training data was scarce and the evaluation was on a single specimen.

**Knutsen & Konovalov (2024)**
Scientific Reports.
Applied few-shot CT segmentation to fossil bone, using a small amount of annotated fossil data on top of a model pre-trained on modern anatomy.
This is the most methodologically relevant prior work for any project facing distribution shift between extant training data and fossil test data. It shows that even a handful of annotated fossil slices can meaningfully adapt the model.

**Zhao et al. (2025)**
Scientific Reports.
Combined deep learning CT segmentation with finite element analysis (FEA) to simulate biomechanical loading on a segmented fossil bone.
This demonstrates the full downstream pipeline: from raw CT scan, through DL segmentation, to mechanical simulation. It closes the loop between morphology and function.

---

## Body Mass and Biomechanics

**Packard (2009)**
Journal of Zoology.
A statistical critique of allometric regression methods used to estimate dinosaur body mass from skeletal measurements.
Read this before applying any regression-based mass estimate. It documents the systematic biases in log-log regression and explains why prediction intervals for large dinosaurs are far wider than most papers report.

**Sellers et al. (2012)**
PLOS ONE.
Estimated dinosaur body mass using 3D convex hulls fitted to skeletal reconstructions rather than regression on bone dimensions.
This is the geometric alternative to regression. It avoids the extrapolation problem entirely by working in volume space, though it depends on the quality of the skeletal reconstruction.

**Brassey (2017)**
PeerJ.
Reviewed the full range of volumetric mass estimation methods, comparing regression, convex hulls, and 3D surface methods across a range of taxa.
Start here before committing to any single method. It maps the tradeoffs between approaches and tells you where each one breaks down.

---

## Broader Surveys

**Yu et al. (2024)**
Earth-Science Reviews.
A comprehensive survey of AI applications across paleontology, covering footprint analysis, CT segmentation, phylogenetic inference, stratigraphy, and specimen identification.
This is the single best overview of where the field is. Read it before starting any paleo-ML project.

---

## Real example

When starting the paleo CT segmentation project, I read Yu et al. (2024) first. It gave a complete map of what had been tried across the field and where gaps still existed. From that survey, Knutsen & Konovalov (2024) stood out as the most methodologically relevant prior work for our specific challenge of training on modern bird and crocodilian bones and predicting on fossil specimens. That directly shaped the decision to pursue few-shot fine-tuning with a small set of annotated fossil CT slices rather than training from scratch.

---

## Key intuitions

- Read Yu et al. (2024) before starting any paleo-ML project. It maps the territory and saves weeks of literature search.
- Supervised footprint classifiers (Lallensack et al.) and unsupervised latent space approaches (Hartmann et al.) answer different questions. Choose based on whether you trust the existing labels.
- Distribution shift is the central challenge in paleo-ML. Modern training data and fossil test data come from different distributions. Knutsen & Konovalov (2024) is the best template for handling it.
- For body mass estimation, Packard (2009) is a prerequisite, not optional background. Skipping it leads to overconfident predictions.

---

## Common mistakes

- Don't apply a supervised footprint classifier trained on one collection to another without checking label consistency, because taxonomic naming conventions differ between research groups and the model will silently misclassify.
- Don't skip Packard (2009) before running allometric regression, because the confidence intervals on mass estimates for large dinosaurs are far wider than the point estimates suggest.
- Don't treat CT segmentation models trained on modern bone as ready-to-deploy on fossils, because matrix fill, mineralization, and scan artifacts create a distribution shift that degrades performance significantly.

---

## Links

- Yu et al. (2024) Earth-Science Reviews survey: https://doi.org/10.1016/j.earscirev.2024.104770
- Knutsen & Konovalov (2024) Scientific Reports: https://doi.org/10.1038/s41598-024-51197-2
- Sellers et al. (2012) PLOS ONE convex hull mass estimation: https://doi.org/10.1371/journal.pone.0033731
- Brassey (2017) PeerJ volumetric methods review: https://doi.org/10.7717/peerj.3302
