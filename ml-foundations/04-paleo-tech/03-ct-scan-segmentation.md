# ML for Dinosaur CT Scan Segmentation

## What it is

CT scan segmentation is the task of labeling every voxel in a 3D CT image as either bone or not-bone. In paleontology, the goal is to digitally separate dinosaur bone from the surrounding rock matrix, so you can extract a clean 3D model of the fossil without physically destroying it.

A U-Net is the standard architecture for this. It takes 2D slices of the CT stack as input and outputs a binary mask. You run it slice by slice, then stack the masks into a 3D volume. See `01-models-and-representations/08-segmentation-architectures.md` for the architecture details and `02-training-evaluation-debugging/02-loss-functions.md` for Dice loss.

## Why it matters

Manual CT segmentation of a single fossil specimen can take hundreds of hours of expert time. A trained segmentologist clicks through thousands of slices, labeling bone by hand. That bottleneck limits how many specimens get analyzed and introduces inter-annotator inconsistency.

Automating even 80% of that work changes what questions paleontologists can ask. Zhao et al. (2025) used DL segmentation as the first step in a pipeline that ran finite element analysis (FEA) on the resulting 3D mesh. FEA simulates how mechanical stress distributes through a bone under loading, which connects directly to locomotion biomechanics and body mass estimation. Without fast, reproducible segmentation, that kind of pipeline is not practical at scale.

## How it works (conceptually)

CT scans produce 3D stacks of grayscale slices. Each voxel stores a density value in Hounsfield units (HU). Air is around -1000 HU. Soft tissue sits between -100 and 100 HU. Cortical bone in living animals is typically above 400 HU. Rock matrix varies widely, but often overlaps with bone in fossilized specimens.

That overlap is the core problem. In a modern bird or crocodile bone, thresholding by HU value is often enough to separate bone from soft tissue. In a fossilized bone, mineralization replaces original calcium with surrounding minerals, shifting the density of the bone toward the density of the matrix. Simple thresholding fails. You need a model that learns local spatial context, not just per-voxel density.

U-Net handles this by combining a contracting encoder (which captures what is in a region) with an expanding decoder (which recovers spatial precision). Skip connections let the decoder reuse fine-grained spatial detail from the encoder. The output is a per-pixel probability of being bone. You threshold that at 0.5 to get the binary mask.

Training uses Dice loss, which directly optimizes the overlap between predicted mask and ground truth. Cross-entropy treats every pixel equally, which is bad when bone pixels are a small fraction of the total (most of a CT slice is matrix or air). Dice loss is insensitive to class imbalance by construction.

Yu et al. (2022) was the first paper to apply this approach to dinosaur fossils. They segmented a sauropod specimen using a CNN-based pipeline and showed it was feasible. Knutsen and Konovalov (2024) pushed further by using few-shot adaptation: they pretrained a segmentation model and fine-tuned it on a small number of annotated fossil slices, which is more realistic because annotating fossil CT data is expensive and slow.

## Real example

In the paleo CT segmentation project, I started with a U-Net pretrained on bird bone CT scans. On bird validation data, it hit 85% Dice. On an initial test against a fossil specimen, it dropped to 62%.

The gap came from mineralization. The fossil bone HU distribution had shifted toward the matrix range, so the model kept labeling dense matrix patches as bone and missing low-density bone regions.

Fine-tuning with 5 annotated fossil slices (80 2D slices total, drawn from different depths in the specimen) brought Dice up to 78%. The remaining gap is taphonomic variation: preservation conditions differ across specimens, and the fine-tuning data only represents one preservation context. A model fine-tuned on one fossil does not transfer cleanly to another fossil from a different depositional environment without additional adaptation.

## Key intuitions

- Hounsfield unit ranges for bone and matrix overlap in fossils. Do not assume density thresholding will work as a baseline.
- Few-shot fine-tuning on fossil data is almost always necessary. A model trained purely on extant species (birds, crocodilians) will not hit acceptable Dice scores on fossils without adaptation.
- More annotated fossil slices help, but they have diminishing returns fast. Five to ten representative slices often gets you most of the way. The key is coverage across depth and preservation variation within the specimen.
- Dice loss is the right default. Cross-entropy will bias your model toward predicting matrix because matrix is the majority class.
- The segmentation output is a 3D mesh, and that mesh feeds downstream analyses like FEA. Errors in segmentation propagate into biomechanical estimates. A 78% Dice score sounds decent until you realize jagged mesh artifacts distort stress simulations.

## Common mistakes

- Don't train only on extant bone CT data and deploy directly on fossils, because the HU distributions are different enough that Dice will drop 20+ points and you won't know until you visually inspect the output.
- Don't use cross-entropy loss for segmentation when bone occupies a small fraction of the slice, because the model will converge to predicting mostly matrix and still get low loss while being useless.
- Don't fine-tune on slices all drawn from one depth in the specimen, because preservation varies through the rock and your fine-tuned model will overfit to one taphonomic context.
- Don't skip visual inspection of the 3D mesh before passing it to downstream analysis, because Dice score does not capture localized artifacts that matter for FEA.

## Links

- Yu et al. (2022): first deep learning segmentation of dinosaur CT scans. https://doi.org/10.7717/peerj.13595
- Zhao et al. (2025), Scientific Reports: DL segmentation plus FEA pipeline for biomechanical analysis. https://doi.org/10.1038/s41598-025-85689-0
- Knutsen & Konovalov (2024), Scientific Reports: few-shot CT segmentation on fossil bone. https://doi.org/10.1038/s41598-024-56013-5
