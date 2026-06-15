# Open Problems in Paleo-ML

## What it is

Paleo-ML is a field where every interesting problem is still open. The ML methods exist. The gap is between what the methods assume and what paleontological data can actually provide. No ground truth. Tiny datasets. Irreducible distribution shift. Fossils that are compressed, cracked, and chemically altered. Experts from two different disciplines who don't share vocabulary. These are not engineering problems you solve with a better optimizer.

## Why it matters

If you use ML on fossil data without understanding these constraints, you will produce results that look credible but aren't. Accuracy numbers on a held-out validation set mean something when the test distribution matches the training distribution. In paleo-ML, it almost never does. The open problems are not niche edge cases. They are the central challenge of applying any model to deep-time biological data.

## How it works (conceptually)

Here is the structure of why these problems are hard.

**No ground truth.** For living species, you can measure body mass directly. For dinosaurs, you cannot. Every model you train on extant animals and apply to extinct ones is making claims about a world no one can verify. The field lacks shared protocols for what counts as sufficient validation when you cannot check the answer.

**Small data.** Paleo-ML datasets typically have tens to low hundreds of labeled specimens. This is structural. Fossils are rare. Digitized, cleaned, and labeled fossils are rarer. Data augmentation helps at the margins. Few-shot learning reduces the sample requirement. But the constraint does not go away, and models that need thousands of examples will fail.

**Irreducible distribution shift.** Every paleo-ML model trains on extant species and predicts on extinct ones. That shift cannot be closed by collecting more data. The question becomes: how much should you trust a prediction at a given degree of extrapolation? The further the extinct taxon is from your training distribution, the less you should trust the output. There is no clean answer for how to quantify this.

**Taphonomic variation.** Fossils are physically altered after death and before discovery. Bones compress under sediment. Minerals replace original material. Specimens are partially destroyed. A model trained on clean, well-preserved museum specimens will not handle a flattened, partially reconstructed footprint the same way. This is not the same as standard domain shift. The deformation is physically unpredictable specimen by specimen.

**Latent space interpretability.** A beta-VAE encodes footprint shapes as vectors in a latent space. Clusters emerge. Outliers appear. But which latent dimensions correspond to which biological features, whether that is body size, gait, species, or substrate type, is not known from the model alone. Linking latent dimensions to biomechanical meaning requires expert annotation of the space after the fact, and that work is largely undone.

**Fragmentary reconstruction.** Most fossil specimens are incomplete. Estimating total body volume from partial remains requires assumptions about what the missing parts looked like. Those assumptions add uncertainty that propagates into every downstream prediction. There is no standard method for representing or propagating that uncertainty through a volumetric mass estimate.

**Interdisciplinary communication.** ML practitioners and paleontologists have different training and different standards for evidence. A paleontologist who cannot inspect a model's reasoning will not trust it. An ML practitioner who does not understand taphonomy will make invalid assumptions about what training data is comparable. Building tools that work across this gap is a design problem, not a modeling problem.

## Real example

DinoTracker trains a beta-VAE on footprint shape data without labels. The model finds structure in the latent space: clusters of morphologically similar tracks, outliers that don't fit existing clusters. That structure is genuinely interesting.

The open problem is validation. When two footprints are close in latent space, it could mean they came from the same species, or from animals of similar size, or from animals moving at similar speeds, or it could mean they were preserved under similar sediment conditions that deformed them the same way. The model cannot distinguish biological similarity from preservational artifact. Without ground truth labels and without expert review of the latent clusters, you cannot know which story is true. This is where paleontologist collaboration becomes the bottleneck, not the ML.

## Key intuitions

- The hardest problems in paleo-ML are domain problems, not ML problems. Better architectures do not fix absent ground truth.
- Small dataset size is a ceiling on model complexity. A model with more parameters than you have training examples is memorizing, not learning.
- Distribution shift in paleo-ML is directional and irreducible. You always extrapolate from living to extinct, never the other way.
- Latent space structure is a hypothesis, not a finding. Clusters need biological interpretation by domain experts before they mean anything.
- Uncertainty should be a first-class output. A point estimate of body mass without a credible interval is not a scientific result.

## Common mistakes

- Don't present paleo-ML predictions as definitive because the absence of ground truth means your uncertainty interval is almost certainly larger than your model reports.
- Don't skip domain expert review of results because a model can produce plausible-looking clusters that reflect preservational artifacts rather than biology, and you cannot tell the difference from the numbers alone.
- Don't optimize for held-out accuracy as the primary metric because when your test set is drawn from the same narrow distribution as your training set, good accuracy tells you nothing about how the model will perform on the extinct taxa you actually care about.
- Don't treat taphonomic deformation as standard noise because it is systematically different from variation in modern specimens, and augmentation strategies designed for the latter will not cover the former.

## Links

- [Brassey (2017): Body-mass estimation in paleontology](https://doi.org/10.1017/pal.2016.64)
- [Knutsen & Konovalov (2024): Deep learning segmentation of fossil CT data](https://doi.org/10.7717/peerj.17577)
- [Sellers et al. (2012): Minimum convex hull mass estimation of dinosaurs](https://doi.org/10.1371/journal.pone.0051393)
- [Yu et al. (2022): Automated segmentation of fossil specimens from CT scans](https://doi.org/10.3389/fevo.2022.842199)
