# Distribution Shift

## What it is

Distribution shift happens when the data your model sees at inference time comes from a different distribution than the data it trained on. The model's learned assumptions no longer hold. Performance degrades, often silently.

There are three main flavors:

**Covariate shift** means the input distribution changes (P(X) differs) but the relationship between inputs and labels stays the same. You trained on recordings from hospital A. You deploy at hospital B with different microphones. The signal looks different even though coughs are still coughs.

**Label shift** means the label distribution changes (P(Y) differs) but the input-given-label relationship is the same. Your model trained on a 50/50 healthy-to-sick split. The deployment population is 90% healthy. The model's prior is miscalibrated.

**Dataset shift** is a mix of both. Usually this is what you actually have in practice.

## Why it matters

A model trained on one distribution is implicitly fitting to that distribution's quirks. If those quirks don't exist in production, you're extrapolating. The model has no way to know it's extrapolating. It will still produce confident-looking outputs. You just won't know whether to trust them.

This is not a niche problem. It is the default condition of deploying any real model.

## How it works (conceptually)

Think of your training data as defining a region in feature space. The model learns patterns within that region. When a new input lands inside that region, the model interpolates. When it lands outside, the model extrapolates in ways it was never trained for.

Covariate shift moves the test inputs into different parts of feature space. Label shift skews which outputs the model is expected to produce. Either way, the learned mapping is being asked to generalize beyond its evidence.

To detect shift, you compare the feature distributions between training and deployment data. KL divergence and the Population Stability Index (PSI) are common tools. A simpler signal: monitor model confidence over time. A sustained drop in average confidence often means the inputs are moving away from the training distribution.

To handle shift, you have a few options. Domain adaptation trains on source data plus a small amount of labeled or unlabeled target data. Feature normalization can reduce domain-specific variation before it reaches the model. Careful feature selection helps too: choose features that are stable across domains, not features that are proxies for domain identity.

## Real example

In the paleo CT segmentation project, a U-Net trained on modern bird bone CT scans scored 85% Dice on the bird validation set. When I ran the same model on an initial fossil test slice, Dice dropped to 62%.

The cause was clear once I looked at the data. Geological mineralization changes bone CT density over millions of years. The contrast between bone and rock matrix in a fossil scan looks different from the contrast between bone and soft tissue in a modern scan. The model had never seen that texture pattern during training.

Fine-tuning with 5 annotated fossil slices brought Dice back up to 78%. That is distribution shift mitigation in practice: identify the gap, collect a small amount of target-domain labeled data, and adapt.

The body mass estimation work has the same problem at an even deeper level. Allometric regression models trained on living mammals are then asked to predict dinosaur body mass. No dinosaurs are in the training set. The size range, bone geometry, and physiology of sauropods violate the model's assumptions in ways that are hard to even quantify. Brassey (2017) reviews why volumetric approaches reduce this problem: they rely on geometry rather than species-specific scaling constants, so they're less sensitive to the taxonomic gap.

## Key intuitions

- Always ask "is my test distribution the same as my training distribution?" before trusting a model's output. If the answer is no, quantify the gap before you deploy.
- Good held-out test performance does not mean good deployment performance. If your test set was sampled from the same distribution as training, you won't see the shift until production.
- Confidence scores are a weak early-warning system. A well-calibrated model becomes less confident when inputs drift out of distribution.
- Some features are more stable across domains than others. Features close to the raw signal (pixel intensity, raw audio) shift more. Features representing shape or structure often shift less.
- The more extreme the domain gap, the more labeled target-domain data you need. Five fossil slices helped. Zero would not have.

## Common mistakes

- Don't assume your held-out test set catches shift, because if you sampled it from the same source as training, it has the same biases. You need data from the actual deployment domain.
- Don't deploy and walk away, because shift accumulates over time and you won't notice until something breaks visibly. Set up confidence monitoring or periodic spot-checks.
- Don't ignore domain-specific reasons your training data is biased, because those biases are exactly what shift will exploit. In paleo-ML, the entire training distribution is extant species. That is a bias with no fix inside the training data itself.
- Don't treat a post-shift Dice score as a model failure without first checking whether the input distribution changed, because a drop in metric almost always has a cause and sometimes the fix is data, not architecture.

## Links

- Brassey (2017), "Body mass estimation in paleontology": https://www.palass.org/publications/palaeontology-journal/archive/60/4/article_pp491-511
- Knutsen & Konovalov (2024), CT segmentation applied to fossil specimens: reference for the paleo CT segmentation project context
- Dataset Shift in Machine Learning, Quinonero-Candela et al. (2009): https://mitpress.mit.edu/9780262170055/dataset-shift-in-machine-learning/
- Population Stability Index explainer (practical monitoring): https://www.listendata.com/2015/05/population-stability-index.html
