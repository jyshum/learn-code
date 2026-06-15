# Segmentation Architectures (U-Net and Related)

## What it is

Segmentation is the task of classifying every pixel in an image. Instead of outputting one label per image (classification), you output a mask the same size as the input, where each pixel gets a class label. If you are separating bone from rock in a CT scan, the output is a full-resolution image where each pixel is either "bone" or "not bone."

U-Net is the dominant architecture for this task, especially in medical and scientific imaging. It was designed specifically for settings where labeled data is scarce and spatial precision matters.

## Why it matters

Most image problems people reach for CNNs to solve are actually segmentation problems in disguise. You do not just want to know "is there bone in this scan?" You want to know exactly which pixels are bone. Classification cannot give you that. Segmentation can.

U-Net also punches above its weight on small datasets. It was built for medical imaging, where you might have dozens of labeled scans instead of millions of images. Skip connections are the main reason it works in this regime.

## How it works (conceptually)

U-Net has a U shape: a downsampling path on the left and an upsampling path on the right.

The encoder (left side) is a stack of convolution layers followed by pooling. Each stage halves the spatial dimensions and doubles the number of feature channels. The encoder learns to detect features at increasing levels of abstraction. Early layers detect edges and textures. Deeper layers detect higher-level structures like "this looks like cortical bone."

The bottleneck is the narrowest point. The feature map is small spatially but rich in abstract information.

The decoder (right side) is a stack of upsampling operations followed by convolutions. Each stage doubles the spatial dimensions and reduces channels, expanding back toward the original resolution. The decoder learns to place the detected features at the correct pixel locations.

Skip connections are what make U-Net work. At each resolution in the encoder, the feature map is copied and concatenated with the corresponding decoder feature map at the same resolution. This gives the decoder two things at once: high-level abstract information from the bottleneck, and low-level spatial detail from the encoder. Without skip connections, fine-grained boundaries are lost during downsampling and never recovered.

A concrete way to think about it:

```
encoder → [compress, detect bone features] → bottleneck → decoder → [expand, locate bone pixels]
            ^                                                                  |
            |________________ skip connections ________________________________|
```

The loss function for segmentation matters. When your target class is small relative to the background, pixel-wise cross-entropy fails because the model learns to predict background everywhere and still gets high accuracy. Dice loss directly optimizes for the overlap between predicted and true masks. Use it when your target region is a small fraction of the image. See `02-training-evaluation-debugging/02-loss-functions.md` for details.

## Real example

In the paleo CT segmentation project, I trained a U-Net to separate bone from rock matrix in dinosaur CT scans. The input is a 2D CT slice. The output is a binary mask indicating bone pixels.

The skip connections were essential. Bone boundaries are fine-grained, high-frequency details. The encoder compresses them away to build abstract bone-vs-rock features, and the skip connections are what let the decoder recover the exact pixel-level boundaries afterward. Without them, the predictions were blurry and missed thin cortical walls entirely.

Training was done on modern bird and crocodilian specimens, where clean labels exist. The network then had to generalize to fossil specimens, which is a real distribution shift: fossil bone looks different from modern bone due to mineralization and matrix infill. The model transferred reasonably well before fine-tuning on a small set of manually labeled fossil slices. This mirrors the approach in Knutsen and Konovalov (2024) and Zhao et al. (2025).

## Key intuitions

- U-Net is your first choice for any scientific image segmentation task. Do not design a custom architecture before trying it.
- Skip connections are not optional. They are the mechanism that lets the decoder recover spatial detail lost during downsampling.
- The encoder asks "what is here?" and the decoder asks "where exactly is it?" Skip connections are how the decoder gets the answer to the second question.
- Small foreground objects require Dice loss, not cross-entropy. The math on pixel-wise accuracy is misleading when 95% of pixels are background.
- U-Net transfers well to small datasets when pre-trained on related domains, even when the domain shift is significant.

## Common mistakes

- Don't evaluate segmentation using only pixel-wise accuracy, because if your target region is 5% of the image, a model that predicts all-background scores 95% accuracy and is completely useless.
- Don't skip the skip connections when building a custom U-Net variant, because the decoder loses all access to fine-grained spatial detail and your masks will be blurry and imprecise.
- Don't use pixel-wise cross-entropy as your only loss when bone or target tissue is a small fraction of the image, because the loss signal is dominated by correct background predictions and the model ignores the foreground.
- Don't jump to a custom architecture before baseline U-Net, because U-Net has been validated across hundreds of medical and scientific segmentation tasks and is hard to beat without a specific reason.

## Links

- [U-Net: Convolutional Networks for Biomedical Image Segmentation (Ronneberger et al., 2015)](https://arxiv.org/abs/1505.04597) -- the original paper, short and readable
- [segmentation-models-pytorch](https://github.com/qubvel/segmentation_models.pytorch) -- drop-in U-Net and variants with pretrained encoders, fastest way to get started
- [Knutsen and Konovalov (2024) on CT segmentation of fossil material](https://peerj.com/articles/17407/) -- directly relevant to the paleo CT project
- [Dice Loss explanation (Towards Data Science)](https://towardsdatascience.com/metrics-to-evaluate-your-semantic-segmentation-model-6bcb99639aa2) -- practical guide to segmentation metrics and why accuracy is not one of them
