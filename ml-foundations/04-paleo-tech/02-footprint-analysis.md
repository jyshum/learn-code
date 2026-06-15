# ML for Dinosaur Footprint Analysis

## What it is

Dinosaur footprint analysis uses ML to classify, compare, and cluster fossil footprints (ichnology). Traditional approaches measure footprints manually: length, width, digit ratios, step length. ML approaches range from CNNs trained on labeled footprint images to unsupervised models that learn shape representations without any labels at all.

## Why it matters

Footprint classification is contested. Different ichnologists use different criteria to define an ichnospecies. One expert's "Grallator" is another expert's "Anchisauripus." If you train a supervised model on one expert's labels, the model learns that expert's assumptions, not anything about the underlying biology. The model then fails to generalize to footprints from a different site or a different researcher's collection. This is not a data problem you can fix by collecting more labeled examples. The labels themselves are the problem.

## How it works (conceptually)

Two approaches dominate right now.

**Supervised CNN classification (Lallensack et al., 2022):** You collect labeled footprint images, train a CNN, and predict ichnospecies categories. This works well on the test set from the same collection. It fails when you apply it to footprints from a new site, because the model encoded the original labeling scheme. The accuracy numbers look good. The generalization does not.

**Unsupervised representation learning (DinoTracker, Hartmann et al., 2026):** You skip labels entirely. DinoTracker preprocesses each footprint image into a 2D silhouette outline, normalizes it to a canonical orientation, and feeds it into a beta-VAE. The beta-VAE learns a 16-dimensional latent representation of each footprint by compressing the outline and reconstructing it, without being told which footprints belong to the same category. UMAP then projects the 16-dimensional space down to 2D for visualization.

Because no labels are used during training, the latent space is not contaminated by expert disagreements. Footprints that are geometrically similar end up close together in latent space regardless of what anyone has called them. You can then do similarity search (find all footprints like this one), anomaly detection (which footprints don't fit any known cluster?), and cross-site comparison across time periods without needing a shared labeling scheme.

## Real example

In DinoTracker, the model was applied to a collection of Middle Jurassic footprints from China. Ichnologists had previously classified these into two separate ichnospecies based on morphological criteria. In the beta-VAE latent space, the two groups appeared adjacent, with substantial overlap in their cluster boundaries. A supervised model trained on the original labels would have maintained the separation, because that separation was baked into the training signal. The unsupervised model had no incentive to reproduce it. The proximity in latent space suggests the two "species" may represent the same trackmaker, different growth stages, or closely related animals. This does not settle the debate, but it surfaces a hypothesis that the supervised approach would have buried.

## Key intuitions

- Footprint shape is determined by the animal's foot anatomy, substrate consistency, gait, and body weight. ML can encode all of these at once. Manual measurements can only encode what the researcher decided to measure.
- When your labels are contested, supervised models do not learn biology. They learn sociology. The model absorbs whichever expert's taxonomy was used to create the training set.
- A beta-VAE's latent space is most useful as a similarity structure, not as a classification system. Two footprints close in latent space are geometrically similar. That is all you can claim without further validation.
- Validating an unsupervised model is genuinely hard. You have no ground truth. The best you can do is check whether the clusters align with independent evidence (stratigraphy, anatomy, trackway patterns) and whether domain experts find the groupings plausible.
- UMAP projections compress 16 dimensions into 2. Clusters that look separate in 2D may overlap in the full latent space. Always check distances in the original latent space before drawing conclusions from UMAP plots.

## Common mistakes

- Don't train a supervised model on one expert's footprint collection and then report test accuracy as evidence of generalization, because the test set is from the same collection with the same labeling biases. Generalization means applying to a different site with a different researcher's labels.
- Don't treat latent space proximity as taxonomic identity, because geometric similarity does not imply biological relatedness. Convergent evolution produces similar footprint shapes from unrelated animals.
- Don't skip silhouette normalization before feeding outlines to the VAE, because orientation and scale differences will dominate the latent representation and wash out genuine shape variation.
- Don't use the beta-VAE's reconstruction loss as your only quality check, because a model can achieve low reconstruction loss while encoding features that are biomechanically meaningless. Cross-validate against independent evidence before publishing cluster interpretations.

## Links

- Hartmann et al. (2026), PNAS: DinoTracker, beta-VAE on dinosaur footprint outlines. https://www.pnas.org/
- Lallensack et al. (2022): supervised CNN classification of dinosaur footprints. https://doi.org/10.7717/peerj.13476
- DinoTracker repository: https://github.com/dinotracker/dinotracker
- Falkingham et al. (2018), PLOS ONE: overview of quantitative methods in ichnology. https://doi.org/10.1371/journal.pone.0208026
