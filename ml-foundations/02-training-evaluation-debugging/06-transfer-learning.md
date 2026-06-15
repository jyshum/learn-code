# Transfer Learning

## What it is

Transfer learning means starting with a model already trained on a large dataset, then adapting it to your specific task. Instead of training from random weights, you inherit weights that already encode useful structure. The most common version: take a CNN pretrained on ImageNet (1.2 million images, 1000 classes), swap out the final layer for your own classification head, and train on your data.

## Why it matters

Most ML projects do not have enough data to train a good model from scratch. If you have fewer than 100k labeled examples, training from scratch almost always underperforms a pretrained model. Transfer learning is not a shortcut. It is usually the correct choice. Starting from pretrained weights also trains faster and is more stable, so you get results in hours instead of days.

## How it works (conceptually)

A CNN learns features in layers. Early layers detect low-level patterns: edges, corners, color gradients, simple textures. These are not specific to any task. Middle layers combine those into shapes and regions. Late layers encode task-specific patterns like "this is a dog" or "this is a stop sign."

When you transfer a model, you keep the early and middle layers as-is. They already know how to find structure in images. You replace the final layer (the classification head) with one that matches your number of classes.

Then you have two strategies:

**Feature extraction.** Freeze all pretrained layers. Only train the new head. The pretrained layers act as a fixed feature extractor. This is fast and works well when your dataset is small or your domain is similar to the source.

**Fine-tuning.** Unfreeze some or all of the pretrained layers and train them along with the head. This lets the model adapt its features to your domain. You must use a small learning rate here, or you will destroy the pretrained weights.

A rough rule: small dataset means freeze more. Larger dataset means unfreeze more.

In PyTorch, freezing a layer looks like this:

```python
for param in model.layer1.parameters():
    param.requires_grad = False
```

## Real example

In SickNote, I used ResNet-18 pretrained on ImageNet. The input was mel spectrograms of cough sounds. On the surface, this makes no sense. ImageNet contains photos of cats, cars, and furniture. Cough spectrograms look nothing like that.

But the trick is that mel spectrograms are 2D images. They have frequency on one axis and time on the other. Patterns in those dimensions, such as frequency bands and temporal bursts, look structurally similar to textures and edges in natural images. The pretrained ResNet already knew how to find those kinds of patterns.

Fine-tuning from ImageNet weights reached 0.77 specificity in about half the epochs that training from scratch required. The model had a head start. It did not need to relearn what an edge or a texture was. It just needed to learn which spectral-temporal patterns correlated with abnormal coughs.

## Key intuitions

- Early CNN layers are universal. Edges and textures transfer across almost any image-like domain, including audio spectrograms, medical scans, and satellite imagery.
- The domain gap matters. ImageNet CNNs transfer well to medical images and audio spectrograms. They transfer less well to completely novel modalities with no visual analog.
- Always try transfer learning first. Training from scratch is rarely necessary with fewer than 100k examples.
- Feature extraction is a good baseline. If fine-tuning does not beat it, your dataset is probably too small to safely unfreeze layers.
- Learning rate is critical during fine-tuning. Use a rate 10x to 100x smaller than you would for training from scratch.

## Common mistakes

- Don't fine-tune with a learning rate that's too high, because it overwrites the pretrained weights in the first few batches and you end up no better than random initialization.
- Don't freeze all layers on a large dataset, because you leave signal on the table. With enough data, letting later layers adapt significantly improves performance.
- Don't skip adapting the input shape when your modality differs from the source. ResNet expects 3-channel RGB images. If your input is single-channel (grayscale spectrograms, CT slices), you need to either duplicate the channel or modify the first conv layer.
- Don't assume transfer learning is always safe across all layers. If your domain is very different from ImageNet, the later pretrained layers may actually hurt you. Start with more frozen layers and unfreeze gradually.

## Links

- [PyTorch Transfer Learning Tutorial](https://pytorch.org/tutorials/beginner/transfer_learning_tutorial.html)
- [CS231n: Transfer Learning](https://cs231n.github.io/transfer-learning/)
- [Pretrained Models in torchvision](https://pytorch.org/vision/stable/models.html)
- [Feature Visualization (Distill)](https://distill.pub/2017/feature-visualization/)
