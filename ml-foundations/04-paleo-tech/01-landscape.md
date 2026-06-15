# ML in Paleontology: Landscape Overview

## What it is

ML in paleontology is the application of machine learning to problems that have traditionally required expert manual analysis of physical specimens. The active subfields are: footprint classification and representation learning, CT segmentation to separate bone from rock matrix, body mass estimation from skeletal measurements, phylogenetic classification from morphometric data, and locomotion analysis from trackways.

These problems look like standard computer vision or regression tasks on the surface. They are not. The structural constraints of the domain change which methods are viable and which are not.

## Why it matters

Paleontology has always been data-starved. Fossils are rare. They are fragmentary. They are expensive to excavate, prepare, and analyze. A single expert spending months on a specimen is the current norm for many analyses.

ML can do two things here. First, it can extract more signal from existing data, finding patterns in CT scans or skeletal proportions that human experts miss or cannot process at scale. Second, it can scale analysis. A trained model can classify thousands of footprint images in minutes. A human expert cannot.

The field is also bottlenecked by expert availability. There are very few people in the world with the taxonomic knowledge to label a dinosaur trackway confidently. ML lets you do more with those people's time.

## How it works (conceptually)

The core pipeline looks familiar: collect images or measurements, preprocess them, train a model, evaluate predictions. But the domain constraints reshape every step.

**Training data comes from extant species. Predictions are about extinct ones.** For body mass estimation, you train on living mammals with known masses and known skeletal measurements. You then predict on dinosaurs. The distribution shift is not a bug to fix. It is a permanent feature of the problem. Dinosaurs are not in your training set. They never will be.

**Labels are contested.** Paleontologists disagree on species boundaries, on whether a footprint belongs to a theropod or an ornithopod, on whether two specimens are the same taxon. When you encode expert labels as ground truth, you are encoding one school of thought. Your model learns that disagreement as fact.

**Datasets are small.** Tens to hundreds of labeled specimens is common. Thousands is exceptional. This rules out methods that need large labeled datasets to generalize.

Given these constraints, the methods getting traction are:

- CNNs for image classification of footprints and specimens, trained on small datasets with heavy augmentation
- U-Net variants for CT segmentation, separating bone voxels from rock matrix
- Regression models (allometric, XGBoost, random forest) for body mass estimation from skeletal measurements
- Unsupervised representation learning (beta-VAE) to sidestep contested labels entirely

Yu et al. (2024) in Earth-Science Reviews is the most comprehensive survey of the field. Most published work is proof-of-concept, not production systems.

## Real example

DinoTracker uses a beta-VAE for unsupervised footprint analysis. The earlier approach in the literature (Lallensack et al. 2022) used supervised DCNN classification. That approach requires labeled training data, which means encoding contested taxonomy as model ground truth. If experts disagree about whether a track belongs to species A or species B, a supervised model learns one answer as correct.

DinoTracker's beta-VAE learns latent representations of footprint shapes without supervision. It compares footprints in latent space rather than predicting labeled categories. This means you can ask "which footprints are morphologically similar" without committing to a taxonomic classification. The Hartmann et al. (2026) approach reflects where the field is going: away from supervised classification that bakes in contested labels, toward representation learning that lets the morphology speak for itself.

The CT segmentation work in the paleo-tech project follows a similar logic. Training on modern bird and crocodilian bones, then predicting on fossil specimens, is a deliberate choice to work with the distribution shift rather than pretend it does not exist.

## Key intuitions

- Small datasets and contested labels are structural features of paleontology ML. They are not problems that better data collection will eventually solve. Method choices must account for them from day one.
- Distribution shift between extant training data and extinct test cases is permanent. Models that perform well on held-out extant specimens may still generalize poorly to fossils.
- Unsupervised methods are often more honest than supervised ones here, because they do not require you to assert ground truth you do not have.
- Domain expert input is not optional. Knowing which morphological comparisons are meaningful requires paleontological knowledge that is not in the data.
- Proof-of-concept accuracy on a small benchmark does not mean the method is ready for research use. The validation standards in this field are still being established.

## Common mistakes

- Don't treat this like a standard computer vision problem where more data will fix things. The data ceiling in paleontology is set by the fossil record, not by how hard you try.
- Don't use accuracy as your primary success metric when ground truth is uncertain. If expert labels are contested, a model that achieves 90% accuracy may just be agreeing with one school of thought.
- Don't skip the domain expert. Training a CNN on footprint images without paleontologist input on which features matter produces a model that may be classifying image artifacts or matrix texture rather than morphology.
- Don't assume that good performance on extant holdout sets transfers to fossil specimens. The distribution shift between living and extinct taxa is real and often large.

## Links

- Yu et al. (2024), "Machine learning in palaeontology," Earth-Science Reviews: https://doi.org/10.1016/j.earscirev.2024.104765
- Lallensack et al. (2022), supervised DCNN footprint classification: https://doi.org/10.1111/pala.12599
- Knutsen & Konovalov (2024), CT segmentation of marine reptile fossils: https://doi.org/10.7717/peerj.17407
- Brassey (2017), body mass estimation review: https://doi.org/10.1098/rsbl.2016.0868
