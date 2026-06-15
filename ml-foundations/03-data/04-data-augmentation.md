# Data Augmentation

## What it is

Data augmentation is the practice of artificially expanding your training set by applying transformations to existing examples. Instead of collecting more data, you create new versions of what you already have. The model sees each example in multiple slightly different forms during training, which forces it to learn the underlying pattern rather than memorize the exact input.

## Why it matters

Most real ML projects are data-constrained. You have hundreds of examples, not millions. Augmentation can effectively double or triple your usable training data without any new collection effort. It also acts as a regularizer: if the model cannot rely on exact pixel positions or exact frequency content, it has to learn what actually matters about the input.

On small datasets, augmentation is often the highest-leverage thing you can do before touching architecture or hyperparameters.

## How it works (conceptually)

You define a set of transformations that preserve the label. Then, during each training epoch, you randomly apply some of these transformations to each example before it reaches the model. The model never sees the exact same input twice.

For images, common transformations include random crop, horizontal flip, rotation, brightness and contrast adjustment, and color jitter. These are applied randomly at training time only, not at inference.

For audio and spectrograms, the go-to technique is SpecAugment: you randomly mask out horizontal bands (frequency masking) and vertical bands (time masking) on the mel spectrogram. This forces the model to recognize patterns even when parts of the signal are missing. You can also apply time stretching, pitch shifting, and additive noise.

Test-time augmentation (TTA) is a related trick: at inference, you run the model on several augmented versions of the same input and average the predictions. This improves accuracy without any retraining.

## Real example

In SickNote, I applied SpecAugment to the mel spectrograms during training. Each training batch masked random frequency bands and random time steps before the CNN saw them. The goal was to stop the model from latching onto recording artifacts, like a narrow frequency band caused by a specific microphone, rather than actual clinical signal in the cough.

Without augmentation, val AUC was around 0.04 lower. With SpecAugment, the model was forced to use distributed features across time and frequency, which is closer to what a clinician actually listens for. The augmentation did not change the architecture or the loss function. It just changed what the model was allowed to memorize.

## Key intuitions

- Augmentation almost always helps on small datasets. If you have hundreds of examples, try it before anything else.
- The transformation must preserve the label. A flipped cough is still a cough. A pitch-shifted cough is still a cough. But a time-reversed cough might not sound like a real cough at all, so you need to check.
- Augmentation only applies to training. Your validation and test sets must stay untouched so your metrics reflect real-world performance.
- More aggressive is not always better. If you stretch and distort your examples so much that they no longer resemble real inputs, you are training on a different distribution than you are testing on.
- Domain context determines what is valid. Horizontal flip is safe for natural images. It is wrong for medical scans where left-right anatomy matters. Pitch shifting is safe for cough classification. It is wrong for speaker identification where pitch is the signal.

## Common mistakes

- Don't apply augmentation to your validation or test sets, because your metrics will no longer reflect how the model performs on real data.
- Don't use transformations that change the label, because the model learns the wrong thing. Flipping a road sign that says "Turn Left" produces a sign that means "Turn Right."
- Don't use augmentations that are too aggressive, because examples that look nothing like real inputs push the model toward a distribution it will never see at inference.
- Don't skip augmentation just because you have a decent dataset size, because it also acts as regularization and can reduce overfitting even when data is not the bottleneck.

## Links

- [SpecAugment paper (Park et al., 2019)](https://arxiv.org/abs/1904.08779)
- [Torchvision transforms documentation](https://pytorch.org/vision/stable/transforms.html)
- [torchaudio transforms documentation](https://pytorch.org/audio/stable/transforms.html)
- [Test-time augmentation overview (fast.ai)](https://docs.fast.ai/learner.html#tta)
