# Edge-Case Detection Failures in Autonomous Driving: A Comparative Visual Taxonomy

[![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/downloads/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.0%2B-EE4C2C.svg)](https://pytorch.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Companion code for our IEEE Transactions on Intelligent Vehicles (T-IV) paper. This repository provides a reproducible pipeline that evaluates **seven object detection architectures** on curated edge-case images and produces **comparative tapestry** visualisations that expose failure modes critical to autonomous driving safety.

---

## Overview

The pipeline runs every input image through seven COCO-pretrained detectors under identical conditions (uniform confidence threshold τ = 0.50, no fine-tuning, no test-time augmentation) and renders a **2×4 grid** — the *comparative tapestry* — where each cell shows one model's detections with colour-coded bounding boxes:

| Cell | Model | Colour | Paradigm |
|------|-------|--------|----------|
| (1,1) | **Original** | White | — |
| (1,2) | **DETR** | Dodger Blue | Transformer-based |
| (1,3) | **SSD** | Orange | One-stage, anchor-based |
| (1,4) | **FCOS** | Lime Green | One-stage, anchor-free |
| (2,1) | **Faster R-CNN** | Crimson | Two-stage |
| (2,2) | **RetinaNet** | Magenta | One-stage, anchor-based |
| (2,3) | **Mask R-CNN** | Purple | Two-stage |
| (2,4) | **YOLOv11** | Hot Pink | One-stage, anchor-free |

## Taxonomy of Failure Categories

The edge-case images are organised into three principal failure categories:

**1. Anthropomorphic Mimicry** — Mannequins, life-size cardboard cutouts, printed faces on posters, celebrity T-shirts, and portrait paintings that fool detectors into false "person" classifications.

**2. Optical-Geometric Distortions** — Rearview mirrors, shop-window reflections, and wet-road specular surfaces that create phantom object duplicates.

**3. Environmental Degradation** — Fog, heavy rain, wet tunnels, and low-light conditions where atmospheric scattering and occlusion cause missed detections.

---

## Repository Structure

```
.
├── run_detectors.py      # Main detection pipeline
├── requirements.txt      # Python dependencies
├── IMAGE_SOURCES.md      # Links to all edge-case images (categorised)
├── LICENSE               # MIT License
├── README.md             # This file
├── images/               # Place downloaded images here (not tracked by git)
└── results/              # Output tapestries appear here (not tracked by git)
```

---

## Getting Started

### Prerequisites

- Python 3.9 or later
- ~4 GB disk space for model weights (downloaded automatically on first run)
- No GPU required — all inference runs on CPU for maximum compatibility

### 1. Clone the Repository

```bash
git clone https://github.com/<your-username>/edge-case-detection-taxonomy.git
cd edge-case-detection-taxonomy
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Download the Edge-Case Images

We do not redistribute the images due to copyright. Instead, [`IMAGE_SOURCES.md`](IMAGE_SOURCES.md) provides the original source URL for every image used in the paper, organised by failure category.

1. Open `IMAGE_SOURCES.md` and visit each link.
2. Download the images and place them in the `images/` directory.
3. Any filename is fine — the pipeline processes all supported formats (`.jpg`, `.jpeg`, `.png`, `.webp`, `.avif`, `.bmp`, `.tiff`).

### 4. Run the Pipeline

```bash
python run_detectors.py --input ./images --output ./results
```

On first execution, the following model weights are downloaded automatically:

| Model | Source | Size (approx.) |
|-------|--------|----------------|
| DETR (ResNet-50) | HuggingFace `facebook/detr-resnet-50` | ~160 MB |
| SSD300 (VGG-16) | torchvision | ~100 MB |
| FCOS (ResNet-50-FPN) | torchvision | ~130 MB |
| Faster R-CNN (ResNet-50-FPN) | torchvision | ~160 MB |
| RetinaNet (ResNet-50-FPN) | torchvision | ~130 MB |
| Mask R-CNN (ResNet-50-FPN) | torchvision | ~170 MB |
| YOLOv11 Nano | Ultralytics `yolo11n.pt` | ~5 MB |

### Command-Line Options

| Flag | Default | Description |
|------|---------|-------------|
| `--input` | `./images` | Path to folder containing input images |
| `--output` | `./results` | Path to output folder for comparative tapestries |
| `--width` | `1600` | Total pixel width of the output tapestry grid |
| `--threshold` | `0.50` | Confidence threshold τ applied uniformly to all models |

### Example

```bash
# Run with a lower threshold and wider output
python run_detectors.py --input ./images --output ./results --threshold 0.30 --width 2400
```

---

## Output

Each input image produces a single PNG file in the output directory, named `res_<original_stem>.png`. The tapestry arranges all seven model outputs in a 2×4 grid with colour-coded bounding boxes, dark title bars, and class labels with confidence scores.

---

## Models and Pretrained Weights

All models use **COCO-pretrained** weights with **no domain-specific fine-tuning**. This is a deliberate methodological choice: general-purpose weights expose the baseline architectural vulnerabilities that fine-tuning would mask, reflecting the out-of-the-box behaviour encountered in rapid prototyping pipelines.

| Model | Framework | Weight Source | Pretrained Data |
|-------|-----------|---------------|-----------------|
| DETR | HuggingFace Transformers | `facebook/detr-resnet-50` (no_timm) | MS COCO |
| SSD | torchvision | `ssd300_vgg16(pretrained=True)` | MS COCO |
| FCOS | torchvision | `fcos_resnet50_fpn(pretrained=True)` | MS COCO |
| Faster R-CNN | torchvision | `fasterrcnn_resnet50_fpn(pretrained=True)` | MS COCO |
| RetinaNet | torchvision | `retinanet_resnet50_fpn(pretrained=True)` | MS COCO |
| Mask R-CNN | torchvision | `maskrcnn_resnet50_fpn(pretrained=True)` | MS COCO |
| YOLOv11 | Ultralytics | `yolo11n.pt` | MS COCO |

---

## Citation

If you use this code or methodology in your research, please cite:

```bibtex
@article{mittal2025edgecase,
  title     = {Edge-Case Detection Failures in Autonomous Driving:
               A Comparative Visual Taxonomy},
  author    = {Mittal, Devansh},
  journal   = {IEEE Transactions on Intelligent Vehicles},
  year      = {2025},
  note      = {Under review}
}
```

---

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

The edge-case images used in the study are **not** included in this repository and remain the property of their respective copyright holders. See [`IMAGE_SOURCES.md`](IMAGE_SOURCES.md) for original source links.
