# ML Training Debugging Checklist

## What it is
A grouped checklist for diagnosing why ML training is broken. When training goes wrong, you need fast triage, not a research expedition. This checklist gives you a sequence of things to check before you start changing model architecture or hyperparameters.

## Why it matters
Most training failures have the same small set of root causes: wrong loss function, bad learning rate, data pipeline bug, or class imbalance. The symptoms look different but the fixes are quick once you know where to look. Debugging without a checklist means changing multiple things at once and never knowing what actually fixed it.

## How it works (conceptually)

Run through these groups in order. Stop when you find the problem.

---

### Sanity check first (do this before anything else)

- [ ] Overfit a single batch. Set `batch_size=4`, run 100+ steps on the same batch, check that loss goes to near-zero.
- [ ] If loss does NOT go near-zero on one batch, the model or loss function is broken. Fix this before doing anything else.
- [ ] If it does go near-zero, training mechanics are fine. Move on.

---

### Loss is NaN or exploding

- [ ] Learning rate is too high. Try dividing it by 10.
- [ ] Check for `log(0)` in your loss. Add a small epsilon: `log(pred + 1e-8)`.
- [ ] Check for NaN in your inputs. Run `torch.isnan(x).any()` on a batch before the forward pass.
- [ ] Reduce batch size. Instability sometimes comes from a bad batch containing extreme values.
- [ ] Add gradient clipping: `torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)`.

---

### Loss not decreasing at all

- [ ] Check that model parameters are actually updating. Run `requires_grad` on your parameters and confirm it's `True`.
- [ ] Check that your optimizer has the right parameters: `optimizer = torch.optim.Adam(model.parameters(), lr=...)`. Passing an empty list means nothing updates.
- [ ] Learning rate might be too low. Try multiplying it by 10.
- [ ] Run the one-batch overfit test. If the model can't memorize 4 samples, the model itself is too weak or the loss is wrong.

---

### Val loss plateaued but still high

- [ ] Lower the learning rate. Try a scheduler or manually reduce by 5-10x.
- [ ] Add more data augmentation to reduce overfitting to train patterns.
- [ ] Check if val distribution matches train. If they were split randomly, this should be fine. If you split by some other criteria, double-check.
- [ ] Train longer. Sometimes plateaus are temporary.

---

### Train loss low, val loss high (overfitting)

- [ ] Add dropout layers.
- [ ] Reduce model capacity (fewer layers or smaller hidden sizes).
- [ ] Add weight decay to the optimizer: `torch.optim.Adam(model.parameters(), lr=1e-3, weight_decay=1e-4)`.
- [ ] Use early stopping based on val loss.
- [ ] Get more training data or add augmentation.

---

### Metrics look wrong

- [ ] Check the classification threshold. Default 0.5 is often not optimal, especially with class imbalance.
- [ ] Check that the metric matches the task. Accuracy is misleading on imbalanced datasets. Use precision, recall, F1, or AUC instead.
- [ ] Confirm you are evaluating on the test set, not the val set you tuned on.
- [ ] Check that your metric function matches your loss function's output format. Logits vs probabilities vs class indices all behave differently.

---

### Model predicts the same class for everything

- [ ] Severe class imbalance. Check your class distribution: `torch.bincount(labels)`.
- [ ] Set `pos_weight` in `BCEWithLogitsLoss` to balance the loss signal.
- [ ] Check that your DataLoader samples both classes in every batch. Use `WeightedRandomSampler` if needed.
- [ ] Check the loss function itself. Using `CrossEntropyLoss` on a binary task with a single output node breaks things silently.

---

### Training is slow

- [ ] Check GPU utilization. Run `nvidia-smi` while training. If it's below 80%, the bottleneck is your data pipeline, not the model.
- [ ] Set `num_workers > 0` in your DataLoader. Start with `num_workers=4`.
- [ ] Increase batch size. Larger batches mean fewer CPU-GPU transfers per epoch.
- [ ] Move data preprocessing offline. If you are computing spectrograms or normalizing images inside `__getitem__`, precompute and cache them.
- [ ] Pin memory: `DataLoader(..., pin_memory=True)` if training on GPU.

---

## Real example
In SickNote, after swapping from `BCEWithLogitsLoss` to `CrossEntropyLoss` (a wrong choice for a binary single-output task), the model predicted only the majority class on every input. Accuracy was around 79%, which matched the "always predict abnormal" baseline exactly. The checklist item "model predicts same class for everything" pointed directly at the loss function mismatch. Switching back to `BCEWithLogitsLoss` with the original `pos_weight` restored normal training behavior within the first epoch.

## Key intuitions
- The one-batch overfit test is the single most important debugging step. Run it before every new training run on a new architecture.
- NaN loss almost always means learning rate is too high or there is a `log(0)` somewhere.
- If accuracy looks great but recall is terrible, you have a class imbalance problem, not a model problem.
- GPU utilization below 80% means the model is not the bottleneck. Fix the data pipeline first.
- Changing one thing at a time is not optional. If you change three things and training improves, you learned nothing.

## Common mistakes
- Don't debug with the full dataset because feedback is slow and you waste hours waiting for runs that fail for trivial reasons. Use a small subset until the run is stable.
- Don't change multiple hyperparameters at once because you lose the ability to isolate what fixed the problem.
- Don't assume slow training is a model problem without checking GPU utilization first because the bottleneck is usually the data pipeline.
- Don't skip the one-batch overfit test because you will spend hours tuning a model that is fundamentally broken in ways that would have been obvious in 5 minutes.

## Links
- [PyTorch Debugging Guide](https://pytorch.org/docs/stable/notes/faq.html)
- [Andrej Karpathy: A Recipe for Training Neural Networks](https://karpathy.github.io/2019/04/25/recipe/)
- [PyTorch DataLoader performance tuning](https://pytorch.org/docs/stable/data.html#single-and-multi-process-data-loading)
