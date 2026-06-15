# Supervised vs Unsupervised Learning

## What it is

Supervised learning means you have labeled examples. Each input comes paired with a correct output. The model learns to map inputs to labels by minimizing its error on those pairs.

Unsupervised learning means you have inputs and no labels. The model finds structure in the data on its own, without being told what the "right answer" is.

Two related ideas worth knowing: self-supervised learning generates its own labels from the data structure (predict the next word, reconstruct a masked patch). Semi-supervised learning combines a small labeled set with a large unlabeled set. Both are out of scope here, but you will encounter them.

## Why it matters

The choice between supervised and unsupervised is not about which is more powerful. It is about what data you have and what biases that data carries.

Most production ML is supervised. You have a task. You have labels. You train a model to do the task. That is the default path.

But labels are not neutral. When a human labels data, they encode assumptions. If those assumptions are wrong or contested, a supervised model will learn and amplify the disagreement. Unsupervised learning sidesteps that by letting the data define its own structure.

## How it works (conceptually)

In supervised learning, you feed the model an input and it produces a prediction. You compare that prediction to the true label and compute a loss. The optimizer adjusts the model weights to reduce that loss. Repeat millions of times. The model gets better at predicting labels it has seen examples of.

In unsupervised learning, there is no label to compare against. Instead, the model tries to do something like compress the data into a smaller representation and then reconstruct it. The reconstruction error becomes the training signal. The model learns to preserve the most important structure in the data because it has to, in order to reconstruct accurately.

A beta-VAE does this by encoding inputs into a compact latent space (a vector of numbers), then decoding back to the original. The latent space dimensions end up capturing meaningful variation in the data, even though no one told the model what "meaningful" means.

## Real example

DinoTracker uses a beta-VAE to analyze dinosaur footprints. No labels. No human-defined categories.

The reason is deliberate. Footprint taxonomy in paleontology is contested. Experts disagree about which tracks belong to which species. If you train a supervised classifier on those labels, you bake taxonomic disputes into your model's weights and call it ground truth.

The beta-VAE learns a latent representation of footprint shapes without any labels. You can then compare footprints by their position in latent space, cluster them, and see what groupings the geometry itself suggests. Those clusters might align with expert taxonomy. They might not. Either way, you are not starting from the assumption that the labels were right.

SickNote is the opposite case. Each cough recording has a label: healthy or abnormal. The task is clear. The label is meaningful and verifiable. Supervised learning with a CNN is the right call.

## Key intuitions

- If labels exist and they are trustworthy, use supervised learning. It is more direct and usually more accurate on the specific task.
- If labels do not exist, are expensive to get, or are contested, unsupervised learning lets the data speak for itself.
- Unsupervised models find structure, but not necessarily the structure you want. A VAE might learn to separate footprints by size rather than species.
- The choice encodes a philosophical stance. Supervised says "I trust these labels." Unsupervised says "I want to discover structure without human priors."
- Semi-supervised is worth considering when you have a few hundred labeled examples and thousands of unlabeled ones. You can use the unlabeled data to improve the representation before fine-tuning on labels.

## Common mistakes

- Don't default to supervised learning when your labels are noisy, because the model will faithfully learn the noise and you will get a confident garbage predictor.
- Don't assume unsupervised learning will find the clusters you care about, because it finds whatever structure minimizes its reconstruction error, which may be color, size, or artifacts in your data collection process.
- Don't treat unsupervised output as ground truth. Latent space clusters need interpretation. They are hypotheses, not answers.
- Don't skip unsupervised learning just because you have labels. Sometimes running both and comparing is the most informative thing you can do.

## Links

- [Stanford CS229 Lecture Notes: Supervised Learning](https://cs229.stanford.edu/lectures-spring2022/main_notes.pdf)
- [Understanding VAEs (Lilian Weng)](https://lilianweng.github.io/posts/2018-08-12-vae/)
- [Scikit-learn: Clustering overview (unsupervised)](https://scikit-learn.org/stable/modules/clustering.html)
- [Semi-supervised learning overview (Van Engelen & Hoos, 2020)](https://link.springer.com/article/10.1007/s10994-019-05855-6)
