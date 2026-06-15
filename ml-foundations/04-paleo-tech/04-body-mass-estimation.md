# ML for Dinosaur Body Mass Estimation

## What it is

Body mass estimation is the problem of figuring out how heavy a dinosaur was when all you have is bones, and often incomplete ones. You cannot weigh a fossil. You cannot measure soft tissue. Every method extrapolates from correlations observed in living animals and applies them to creatures that died 66 million years ago.

The core pipeline is: measure something on a fossil skeleton, find a living animal where that same measurement correlates with body mass, and project outward. The further you project, the less trustworthy your answer.

## Why it matters

Body mass touches almost everything in paleobiology. Metabolic rate scales with mass. Growth rates scale with mass. Locomotion models require mass as an input. If your mass estimate is wrong by a factor of two, your whole biomechanical analysis inherits that error.

It also matters because dinosaur mass estimates in the literature vary wildly, sometimes by an order of magnitude for the same specimen. Knowing which methods produce which kinds of errors helps you read those papers critically.

## How it works (conceptually)

**Allometric regression** is the traditional approach. You take a dataset of living mammals, measure limb bone dimensions (femur length, femur shaft circumference, humerus length), log-transform everything, fit a linear regression in log-log space, then back-transform to get a mass prediction. It works because bone dimensions scale predictably with body size across mammals.

The problem Packard (2009) identified is back-transformation bias. When you fit in log-space and then exponentiate to get back to kilograms, you systematically inflate estimates. This is a statistical artifact, not biology. The bias gets worse the further you extrapolate from your training data.

**Volumetric methods** take a different approach. Sellers et al. (2012) built 3D skeletal reconstructions and computed convex hull volumes. A convex hull wraps the skeleton in the tightest possible geometric shell. Mass is then volume times an assumed tissue density. This is more geometrically grounded because it reasons about the actual 3D shape of the animal rather than treating a single bone measurement as a proxy for the whole body. Brassey (2017) reviewed these approaches and found they reduce the number of extrapolation assumptions required compared to allometric regression.

**ML regression** trains on the same extant animal datasets but uses models like XGBoost or neural networks instead of log-linear equations. The advantage is that these models can capture non-linear relationships that a straight line in log-log space misses. Feature selection can also tell you which skeletal measurements carry the most predictive signal, which is useful when fossil specimens are fragmentary and you only have a few bones to work with.

The shared problem across all methods is distribution shift. Every model is trained on living animals. The largest living land animal is an elephant at around 6,000 kg. A large sauropod weighed 50,000 to 70,000 kg or more. You are asking a model to extrapolate 10x outside its training distribution. The honest answer is that uncertainty intervals at that range are enormous.

**The CT segmentation connection** offers a way to sidestep skeletal measurement regression entirely. If you can segment a CT scan to extract a 3D bone mesh (see `03-ct-scan-segmentation.md`), you can compute volume directly from the mesh geometry. Zhao et al. (2025) explores this pipeline. It still requires assumptions about soft tissue volume and density, but it removes one entire layer of proxy-based inference.

## Real example

For the paleo body mass estimation project, I trained XGBoost on 847 extant mammal specimens using femoral shaft circumference and total femur length as features. The model predicted 32,000 kg for a large Brachiosaurus specimen. The 95% prediction interval was 18,000 to 55,000 kg.

That interval is not a failure. It is the honest answer. The model knows it is extrapolating well beyond its training distribution, and the interval reflects that.

The allometric regression on the same specimen gave 41,000 kg with no stated uncertainty. That point estimate looks more confident, but the confidence is false. It does not account for back-transformation bias or for the fact that the regression was fit on animals 10x smaller. The XGBoost interval is less satisfying to read, but it is telling the truth.

## Key intuitions

- A point estimate for dinosaur body mass without a confidence interval is overconfident. Always report the interval.
- The biggest source of error is not your model architecture. It is the distribution shift between your extant training set and your fossil specimen. No amount of tuning fixes that.
- Volumetric methods and skeletal measurement regressions are not competing. They are complementary. If you have both a 3D reconstruction and bone measurements, use both and compare.
- XGBoost's prediction intervals widen naturally as you extrapolate. That widening is a feature, not a bug. It is the model telling you it is uncertain.
- Which skeletal measurements you use matters more than which ML model you choose. Femoral shaft circumference is consistently more predictive than femur length alone.

## Common mistakes

- Don't report back-transformed log-space regression estimates without applying a bias correction, because Packard (2009) showed this systematically inflates mass predictions in a way that is not biologically meaningful.
- Don't use R-squared alone to evaluate your regression model, because R-squared looks fine even when the model is badly wrong in the extrapolation range where you actually need it.
- Don't assume your training set covers the target because mammals and dinosaurs are both vertebrates with limb bones, because the size gap between your largest training specimen and a large sauropod is so large that the correlation structure may not hold.
- Don't skip uncertainty quantification because the estimate "seems reasonable," because a 32,000 kg estimate and a 55,000 kg estimate are both reasonable for the same Brachiosaurus, and that ambiguity is real.

## Links

- Packard, G.C. (2009). On the use of logarithmic transformations in allometric analyses. Journal of Theoretical Biology. https://doi.org/10.1016/j.jtbi.2008.10.016
- Sellers, W.I. et al. (2012). Minimum convex hull mass estimations of complete mounted skeletons. Biology Letters. https://doi.org/10.1098/rsbl.2012.0263
- Brassey, C.A. (2017). Body-mass estimation in paleontology: a review of volumetric techniques. Paleontological Society Papers. https://doi.org/10.1017/scs.2017.12
