# The Training Loop

## What it is

The training loop is the repeated cycle your model goes through to learn from data. Each cycle has four steps: forward pass, loss calculation, backward pass, and weight update. You run this cycle many times, over many batches, until the model improves.

That's it. Everything else in training is built around this core loop.

## Why it matters

Your model starts with random weights. The training loop is the only mechanism that moves those weights toward something useful. If your loop is broken, nothing else matters. A wrong loss function, a missing `zero_grad()`, or unshuffled data will silently degrade your results. Understanding this loop lets you debug training when it goes wrong, and it will go wrong.

## How it works (conceptually)

**Forward pass.** You feed a batch of inputs into the model. It produces predictions. No gradients are computed yet, just numbers flowing forward through layers.

**Loss calculation.** You compare the model's predictions to the true labels using your loss function. This produces a single scalar: how wrong the model was on this batch.

**Backward pass.** You call `loss.backward()`. PyTorch traces back through every operation and computes the gradient of the loss with respect to each weight. This tells you which direction to nudge each weight to reduce the loss.

**Optimizer step.** You call `optimizer.step()`. The optimizer uses those gradients to update the weights. How it uses them depends on the optimizer (SGD, Adam, etc.), but the goal is always the same: move the weights in the direction that reduces loss.

Then you repeat.

**Epochs, batches, and iterations.** An epoch is one complete pass through your entire training dataset. A batch is the subset of samples you process in a single forward pass. An iteration is one batch. If you have 1,000 samples and a batch size of 32, one epoch takes roughly 32 iterations.

**Why batch size matters.** Small batches give you noisy gradient estimates because you're only seeing a fraction of the data. But noisy gradients can actually help you escape local minima, and small batches update weights more frequently. Large batches give you stable, accurate gradient estimates but require more memory and update weights less often. Batch size of 32 is a common default. It's not magic, but it works well in many situations.

**Why `zero_grad()` matters.** PyTorch accumulates gradients by default. If you don't call `optimizer.zero_grad()` before each backward pass, the gradients from the previous iteration get added to the current ones. Your updates become wrong. This is one of the most common beginner mistakes.

## Real example

In SickNote, the training loop ran over mel spectrogram tensors from the COUGHVID dataset. Each epoch passed through all training samples, with a batch size of 32. One iteration looked like this:

```python
optimizer.zero_grad()
outputs = model(inputs)          # forward pass: spectrogram -> logit
loss = criterion(outputs, labels) # BCEWithLogitsLoss with pos_weight
loss.backward()                  # backward pass: compute gradients
optimizer.step()                 # update weights
```

Because 79.7% of recordings were abnormal, unshuffled data meant early batches could be almost entirely one class. Shuffling the dataset each epoch kept the class distribution roughly balanced across batches, which kept the gradient signal informative. Without shuffling, the model saw stretches of nearly identical labels and the loss barely moved in those phases.

## Key intuitions

- You are descending a loss landscape. Each batch gives you a slightly noisy estimate of which direction is downhill. Enough steps in roughly the right direction and you reach a good minimum.
- One batch is not one gradient descent step on the full dataset. It's a cheap approximation. The approximation is good enough, and it's much faster than computing the exact gradient over all your data.
- Gradients tell you direction, not distance. The learning rate controls how far you step in that direction. Too large a step and you overshoot. Too small and you barely move.
- The loop is where your model actually learns. Everything else, your architecture, your loss function, your data augmentation, only matters because of what happens inside this loop.
- Watching loss decrease per iteration (not just per epoch) tells you whether training is actually working. A loss that's flat for many iterations means something is wrong.

## Common mistakes

- Don't forget `optimizer.zero_grad()` because gradients accumulate across iterations and your weight updates become corrupted.
- Don't skip shuffling your dataset each epoch because the model will see the same ordering every time and may overfit to sequence patterns rather than learning general features.
- Don't log loss only at the end of each epoch because you lose visibility into whether training is progressing batch-to-batch, which makes it much harder to catch divergence early.
- Don't assume a decreasing loss means a good model because the loss measures performance on training data. Always track validation loss alongside training loss to catch overfitting.

## Links

- [PyTorch training loop tutorial](https://pytorch.org/tutorials/beginner/blitz/cifar10_tutorial.html)
- [PyTorch `zero_grad()` docs](https://pytorch.org/docs/stable/generated/torch.optim.Optimizer.zero_grad.html)
- [Andrej Karpathy: "A Recipe for Training Neural Networks"](http://karpathy.github.io/2019/04/25/recipe/)
- [PyTorch DataLoader docs (shuffling and batching)](https://pytorch.org/docs/stable/data.html#torch.utils.data.DataLoader)
