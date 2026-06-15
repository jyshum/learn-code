# Optimizers and Learning Rate

## What it is

An optimizer is the algorithm that takes the gradients computed during backprop and uses them to update your model's weights. After every batch, the loss is computed, gradients flow backward, and the optimizer steps: it decides how much to move each weight and in which direction.

The learning rate is the scalar that controls the size of those steps. It is the single most important hyperparameter you will tune.

## Why it matters

The optimizer and learning rate determine whether training actually works. A bad loss function means you optimize for the wrong thing. A bad optimizer or learning rate means you fail to optimize at all. You can have a perfect architecture with a perfect dataset and still get nowhere if the learning rate is off by one order of magnitude.

## How it works (conceptually)

After backprop, each weight has a gradient: the direction that increases the loss. The optimizer moves weights in the opposite direction, by an amount scaled by the learning rate.

**SGD** does exactly this. Each step is: move the weight by learning rate times gradient. Simple, predictable, and still competitive when you tune momentum carefully. Momentum in SGD accumulates a velocity across steps, which helps the optimizer push through flat regions.

**Adam** adapts the learning rate per parameter. It tracks two running averages: the gradient itself and the squared gradient. Parameters that get large gradients often get a smaller effective step. Parameters with small or sparse gradients get a relatively larger step. This makes Adam much faster to get going. You rarely need to tune beyond the initial learning rate.

**Which to use:** Start with Adam at 1e-3. It will converge faster in almost every case. If you are squeezing out final performance and have time to tune, SGD with momentum and a schedule can sometimes generalize slightly better. For most projects, Adam wins on time budget.

**Learning rate schedules** change the LR during training rather than holding it fixed.

- `ReduceLROnPlateau` watches a metric (usually validation loss) and halves the LR when it stops improving. Set a patience of 3-5 epochs and a factor of 0.5.
- `CosineAnnealingLR` decays the LR smoothly along a cosine curve, which tends to prevent the LR from dropping too fast early and too slow late.
- Warmup starts the LR very low, ramps it up over the first few epochs, then decays. This helps when the model weights are random and large early gradients would destabilize training.

**Weight decay** is L2 regularization baked into the optimizer. It adds a small penalty proportional to the magnitude of each weight. This discourages weights from growing too large, which prevents overfitting. In PyTorch you pass it as `weight_decay=1e-4` directly to the optimizer. No separate code needed.

**The learning rate finder** is a diagnostic sweep. You run a short training loop where the LR increases from 1e-7 to 1e-1 over many mini-batches and you plot loss vs. LR. The loss will drop as LR rises, then sharply increase once the LR is too large. Your target LR is one order of magnitude below where the loss starts rising. This takes 1-2 minutes and saves hours of guessing.

## Real example

In SickNote, I used Adam with an initial LR of 1e-4 and `ReduceLROnPlateau` watching validation loss. Early in training the loss dropped steadily. Around epoch 12, val loss flattened and the scheduler triggered, halving the LR to 5e-5 automatically. Training recovered and val loss dropped again for another 3-4 epochs before stabilizing. Without the scheduler, training would have stalled at a worse local minimum. The final model reached 0.77 specificity, which would not have been achievable with a fixed LR.

## Key intuitions

- The learning rate is the dial you touch most. Everything else is secondary until you have the LR right.
- Start Adam at 1e-3. If loss oscillates or explodes, drop to 1e-4. If training is crawling, try 3e-3.
- A loss curve that bounces wildly means your LR is too high. A loss curve that barely moves means it is too low or you have a bug.
- Always use a scheduler. Fixed LR rarely gives you the best final result because what works early in training is too large late in training.
- Weight decay at 1e-4 or 1e-5 is almost always free performance. Turn it on by default.

## Common mistakes

- Don't set LR too high because loss will oscillate and never converge. The model takes huge steps, overshoots the minimum, and bounces around it.
- Don't use a fixed LR for the full training run because training stalls. The model needs smaller steps as it approaches a good solution.
- Don't use SGD with default settings (no momentum, no schedule) because it is dramatically slower than Adam out of the box. If you use SGD, set momentum to 0.9 and use a schedule.
- Don't ignore weight decay because large weights overfit, especially on small datasets. It costs you nothing to add it.

## Links

- [PyTorch Optimizer docs](https://pytorch.org/docs/stable/optim.html)
- [fast.ai learning rate finder explanation](https://fastai1.fast.ai/callbacks.lr_finder.html)
- [ReduceLROnPlateau docs](https://pytorch.org/docs/stable/generated/torch.optim.lr_scheduler.ReduceLROnPlateau.html)
- [Andrej Karpathy: A Recipe for Training Neural Networks](http://karpathy.github.io/2019/04/25/recipe/)
