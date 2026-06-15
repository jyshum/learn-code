# Convolutional Neural Networks (CNNs)

## What it is

A CNN is a neural network designed for grid-structured data. Images are grids of pixels. Mel spectrograms are grids of frequency vs. time. CNNs exploit that structure by learning small spatial patterns and detecting wherever those patterns appear in the input.

The core operation is convolution. A filter (also called a kernel) is a small grid of numbers. It slides across the input and computes a dot product at each position. The output is a feature map showing where that pattern was detected and how strongly.

## Why it matters

Standard fully connected networks treat every input value as independent. They have no concept of "these pixels are neighbors." CNNs share weights across positions, which means a filter that detects a horizontal edge works everywhere in the image, not just in the top-left corner.

This makes CNNs dramatically more efficient and more generalizable for grid data. And because mel spectrograms are grids too, CNNs transfer from image classification to audio classification with surprisingly little effort.

## How it works (conceptually)

Think of the forward pass as a chain of detectors:

```
input → [conv: detect edges] → [conv: detect shapes] → [pool: compress] → [conv: detect patterns] → [dense: classify]
```

Each conv layer applies a set of filters to the previous layer's output. Early layers detect low-level features like edges and textures. Middle layers combine those into shapes. Later layers detect task-specific patterns.

Pooling sits between conv layers. Max pooling takes a small region (say 2x2 pixels) and keeps only the maximum value. This compresses the feature maps and makes the network less sensitive to the exact position of a pattern. A cough with a particular frequency burst at time step 14 vs. time step 15 should still activate the same detector.

Popular architectures:

- ResNet: skip connections add the input of a block directly to its output. This lets gradients flow through very deep networks without vanishing. ResNet-18 and ResNet-50 are good defaults for fine-tuning.
- VGG: simple stack of conv layers with no skip connections. Interpretable and easy to debug.
- EfficientNet: scales depth, width, and resolution together. Best accuracy per parameter count if you need to be efficient.

Start with a pretrained ResNet before designing your own architecture. You get ImageNet features for free, and fine-tuning is much faster than training from scratch.

## Real example

In SickNote, I used ResNet-18 pretrained on ImageNet. The input was a 224x224 mel spectrogram image generated from each cough recording. The CNN's convolutional layers extracted frequency-temporal patterns. The final dense layer produced a single logit: healthy vs. abnormal.

The pretrained weights gave the model a head start on detecting local patterns even though ImageNet images have nothing to do with coughs. The convolutional layers learned to detect frequency bursts and spectral shapes that distinguish pathological coughs. The model reached 0.77 specificity after tuning with BCEWithLogitsLoss and pos_weight.

Grad-CAM was especially useful here because it highlights which regions of the spectrogram activated the network most. You can literally see the network attending to specific frequency bands in specific time windows.

## Key intuitions

- CNNs are the right default for any grid-structured input, including audio spectrograms. If your data has spatial or temporal structure, try a CNN before anything else.
- A pretrained ResNet trained on ImageNet transfers well to spectrograms even though cough sounds look nothing like dogs and cats. The low-level edge detectors are still useful.
- The filter learns the pattern. You do not hand-engineer what edges or frequency bursts look like. The network discovers them during training.
- Feature hierarchy is real. The first conv layer of a trained ResNet responds to oriented edges. The last conv layer responds to complex shapes or frequency patterns specific to your task.
- Pooling is not optional. Without it, small positional shifts produce completely different activations, and your network has to memorize every possible position of every pattern.

## Common mistakes

- Don't apply a CNN directly to a 1D audio waveform because the raw waveform has no spatial structure the CNN can exploit. Convert to a mel spectrogram first so you get a 2D frequency-time grid.
- Don't train from random weights when you have limited data because the network will overfit before it learns useful features. Start with ImageNet pretrained weights and fine-tune.
- Don't use too many conv layers for small inputs because the feature maps shrink with each layer, and by the time you reach the last conv block you may have a 1x1 feature map with no spatial information left.
- Don't skip Grad-CAM or similar visualization because without it you have no idea whether the network is attending to the right parts of the input, and debugging is guesswork.

## Links

- [CS231n: Convolutional Neural Networks for Visual Recognition](https://cs231n.github.io/convolutional-networks/)
- [PyTorch ResNet fine-tuning tutorial](https://pytorch.org/tutorials/beginner/finetuning_torchvision_models_tutorial.html)
- [Grad-CAM paper (Selvaraju et al., 2017)](https://arxiv.org/abs/1610.02391)
- [Audio classification with mel spectrograms (fast.ai)](https://www.fast.ai/posts/2019-04-10-recurrent-neural-networks.html)
