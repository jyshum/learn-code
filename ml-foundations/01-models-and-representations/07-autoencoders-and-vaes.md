# Autoencoders and VAEs

## What it is

An autoencoder is a model that learns to compress its input into a small representation and then reconstruct the original from that compressed form. The architecture is: input → [encoder] → bottleneck → [decoder] → reconstructed input.

The bottleneck is the key. It forces the model to keep only what matters. Everything that can't be squeezed through the bottleneck gets dropped.

A variational autoencoder (VAE) is a version of this where the bottleneck is not a single point but a probability distribution. Instead of encoding "this footprint = [0.3, -1.2, 0.8, ...]", a VAE encodes "this footprint = a distribution centered at [0.3, -1.2, 0.8, ...] with spread [0.1, 0.2, 0.05, ...]". You sample from that distribution to get the actual latent vector used for decoding.

A beta-VAE adds a stronger constraint on the latent space by weighting the KL term more heavily. Higher beta means the model is pushed harder to learn disentangled representations, where individual latent dimensions correspond to interpretable factors like size, elongation, or aspect ratio.

## Why it matters

Autoencoders don't need labels. The supervision signal is reconstruction quality. If the model can compress and reconstruct the input well, it has learned something real about the data's structure.

This matters when labels are scarce, contested, or biased. In paleontology, expert-assigned footprint categories carry decades of disagreement baked in. An autoencoder bypasses that entirely. It learns structure from the raw shapes themselves.

After training, the bottleneck representation (the latent vector) is a compact description of the input. You can use it for clustering, anomaly detection, or direct comparison between inputs, without ever defining a label.

## How it works (conceptually)

The encoder is a neural network that maps high-dimensional input down to a small vector. Think of it as answering: "what is the essential structure of this input, compressed into N numbers?"

The decoder is another neural network that maps that small vector back up to the original input size. It answers: "given this compression, what did the input look like?"

Training optimizes reconstruction loss: how different is the reconstructed output from the original input? For images, this is often mean squared error or binary cross-entropy over pixels.

For a VAE, training optimizes two terms simultaneously. Reconstruction loss ensures the decoded output looks like the input. KL divergence keeps the latent distribution close to a standard normal distribution. These two terms are in tension. The model must reconstruct well while keeping its latent encodings organized and compact.

```python
loss = reconstruction_loss + beta * kl_divergence
```

Higher beta pushes harder on KL. The latent space becomes smoother and more structured, but reconstruction quality may drop slightly. This tradeoff is the main dial you tune in a beta-VAE.

The smooth latent space is what makes VAEs useful for interpolation and generation. In a standard autoencoder, the space between two encoded points is undefined. In a VAE, it's continuous, so you can sample from it meaningfully.

## Real example

In DinoTracker, I trained a beta-VAE on 2D dinosaur footprint outlines. Each footprint was a contour shape, no labels attached.

After training, each footprint mapped to a 16-dimensional latent vector. Footprints with similar shapes clustered together in that latent space. The model grouped tridactyl prints, round prints, and elongated prints without being told those categories existed.

The most scientifically interesting footprints were the outliers: points far from any cluster in latent space. These were the specimens that didn't fit known categories. No labels needed to find them, just distance in latent space.

This sidesteps a real problem in paleo-research. Expert-labeled categories carry the assumptions of whoever labeled them. The beta-VAE learned from the shapes themselves.

## Key intuitions

- The bottleneck is the whole point. Make it too large and the model learns an identity mapping. It memorizes without compressing, and the latent space is meaningless.
- Latent distance is similarity. Points close together in latent space are structurally similar inputs. Points far apart are different. This gives you a similarity metric without any labels.
- VAE latent spaces are smooth. Standard autoencoders have gaps between encoded points that produce garbage when decoded. VAE spaces are continuous, so interpolation between two inputs produces meaningful intermediate representations.
- Beta controls the tradeoff. Higher beta = more disentangled and structured latent space, at the cost of slightly worse reconstruction. Start with beta=1 (standard VAE) and increase if you want interpretable dimensions.
- The decoder can be thrown away. Once trained, you often only use the encoder. The decoder was just a training tool to force good representations.

## Common mistakes

- Don't make the bottleneck too large, because the model has no reason to compress and learns to copy the input instead of understanding it. A latent space of 2-32 dimensions is a reasonable starting point depending on input complexity.
- Don't use a standard autoencoder when you need smooth interpolation or generation, because the latent space will have undefined regions that produce garbage outputs. Use a VAE instead.
- Don't skip visualizing the latent space, because you won't know if the model learned meaningful structure. Run UMAP or PCA on your latent vectors and plot them. Clusters should be visible if the model worked.
- Don't ignore the beta tuning in a beta-VAE, because the default beta=1 may not give you the disentanglement you need. If individual latent dimensions don't correspond to interpretable factors, increase beta and retrain.

## Links

- [Auto-Encoding Variational Bayes (Kingma & Welling, 2013)](https://arxiv.org/abs/1312.6114) - the original VAE paper
- [beta-VAE: Learning Basic Visual Concepts with a Constrained Variational Framework](https://openreview.net/forum?id=Sy2fchgr) - introduces the beta weighting
- [Understanding VAEs (Lilian Weng)](https://lilianweng.github.io/posts/2018-08-12-vae/) - clear walkthrough with visuals
- [UMAP for latent space visualization](https://umap-learn.readthedocs.io/en/latest/) - standard tool for visualizing high-dimensional latent vectors
