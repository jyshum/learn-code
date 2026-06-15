# Explainability (Grad-CAM and Related)

## What it is

Explainability tools show WHERE in the input your model is paying attention when it makes a prediction. They do not explain WHY the model works internally. They can reveal whether the model is using the right features or cheating off something irrelevant.

The two most common tools are Grad-CAM and SHAP. Grad-CAM works on CNNs and produces a heatmap over an image. SHAP works on tabular models and tells you how much each feature pushed a prediction up or down.

## Why it matters

A model can hit 90% accuracy for the wrong reasons. It might be keying off a background artifact, a watermark, or a recording artifact rather than the actual signal. Your metrics will look fine. Your model will fail in production when that artifact disappears.

Explainability is how you catch that before deployment. It is also how you build credibility with domain experts who need to trust the model before acting on its outputs.

## How it works (conceptually)

Grad-CAM stands for Gradient-weighted Class Activation Mapping. During a forward pass, your CNN produces activation maps at each convolutional layer. Grad-CAM looks at the gradients flowing back into the last convolutional layer when you predict a specific class. Those gradients tell you which channels in that layer were most important for the prediction. Grad-CAM weights each activation map by its corresponding gradient and averages them together. The result is a single spatial map the same size as the feature map. You upsample it back to the input size and overlay it as a heatmap.

In code, you hook into the last conv layer like this:

```python
gradients = []
activations = []

def save_gradient(module, grad_input, grad_output):
    gradients.append(grad_output[0])

def save_activation(module, input, output):
    activations.append(output)
```

Then after a forward-backward pass, you pool the gradients over spatial dimensions and weight the activation maps. High values in the resulting map correspond to regions the model attended to.

SHAP works differently. For a tabular model, it assigns each feature a value representing its contribution to pushing the prediction above or below the baseline. Positive SHAP values push the prediction higher. Negative values push it lower. It is grounded in game theory and is consistent across model types.

## Real example

In SickNote, I applied Grad-CAM to mel spectrogram inputs after training the CNN to classify coughs as healthy or abnormal. The heatmaps on abnormal predictions consistently lit up in the 0-1 kHz frequency band. That matched known clinical patterns: wet coughs and productive coughs carry more low-frequency energy than dry coughs.

That alignment mattered. With a 79.7% abnormal class imbalance, there were plenty of ways the model could have found shortcuts. The heatmaps showing the right frequency band gave confidence that the model was picking up real acoustic signal, not a dataset artifact like recording quality differences between healthy and sick participants.

## Key intuitions

- Run explainability on your failures, not just your successes. The cases where the heatmap looks wrong are the most informative.
- A heatmap on the right region does not mean the model understands the concept. It means the model is correlating with that region. Correlation is a start, not a finish.
- If the heatmap highlights background or padding, you have a data problem, not a model problem.
- Domain experts can interpret heatmaps in ways you cannot. Show them the visualizations early.
- Explainability is most useful when you have a prior about what the model should attend to. Without that prior, you are just looking at a colorful picture.

## Common mistakes

- Don't trust a good-looking heatmap without checking it against domain knowledge, because the model could be correlating with a confound that happens to be spatially co-located with the real signal.
- Don't apply Grad-CAM to fully connected layers, because Grad-CAM requires spatial structure to produce a meaningful map. It only works on convolutional layers.
- Don't interpret heatmap intensity as model certainty, because a bright heatmap just means high activation weighted by gradient. A confidently wrong model produces bright heatmaps too.
- Don't run explainability only at the end of training, because catching the wrong attention patterns early lets you fix the data pipeline before you sink more compute into it.

## Links

- [Grad-CAM paper (Selvaraju et al., 2017)](https://arxiv.org/abs/1610.02391)
- [pytorch-grad-cam library](https://github.com/jacobgil/pytorch-grad-cam)
- [SHAP documentation](https://shap.readthedocs.io/en/latest/)
- [Distill: Feature Visualization](https://distill.pub/2017/feature-visualization/)
