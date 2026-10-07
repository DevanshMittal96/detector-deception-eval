#!/usr/bin/env python3
"""
Object Detection Comparison Pipeline
=====================================
Runs 7 detection models on input images and produces 2x4 comparison tapestries.
Optionally writes every raw detection (box, label, score) to a JSON file.

Models: DETR, SSD, FCOS, Faster R-CNN, RetinaNet, Mask R-CNN, YOLOv11

Usage:
    python run_detectors.py --input /path/to/images --output /path/to/results

Example:
    python run_detectors.py --input ./images --output ./results --width 1600 --threshold 0.50
    python run_detectors.py --input ./images --output ./results --save-json ./results/detections.json

Setup:
    pip install -r requirements.txt
"""

import argparse
import json
import os
import sys
import warnings
from pathlib import Path

import torch
import torchvision
from torchvision import transforms as T
from torchvision.utils import draw_bounding_boxes
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from tqdm import tqdm

try:  # AVIF support for Pillow builds without native libavif
    import pillow_avif  # noqa: F401
except ImportError:
    pass

warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────
# Configuration
# ─────────────────────────────────────────────

CONFIDENCE_THRESHOLD = 0.50

# Each model gets a unique, visually distinct color (RGB)
MODEL_COLORS = {
    "DETR":         (30, 144, 255),   # Dodger blue
    "SSD":          (255, 165, 0),    # Orange
    "FCOS":         (50, 205, 50),    # Lime green
    "Faster R-CNN": (220, 20, 60),    # Crimson red
    "RetinaNet":    (255, 0, 255),    # Magenta
    "Mask R-CNN":   (148, 103, 189),  # Purple
    "YOLO v11":     (255, 105, 180),  # Hot pink
}

# COCO class labels (used by torchvision models)
COCO_LABELS = [
    "__background__", "person", "bicycle", "car", "motorcycle", "airplane",
    "bus", "train", "truck", "boat", "traffic light", "fire hydrant",
    "N/A", "stop sign", "parking meter", "bench", "bird", "cat", "dog",
    "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe",
    "N/A", "backpack", "umbrella", "N/A", "N/A", "handbag", "tie",
    "suitcase", "frisbee", "skis", "snowboard", "sports ball", "kite",
    "baseball bat", "baseball glove", "skateboard", "surfboard",
    "tennis racket", "bottle", "N/A", "wine glass", "cup", "fork",
    "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange",
    "broccoli", "carrot", "hot dog", "pizza", "donut", "cake", "chair",
    "couch", "potted plant", "bed", "N/A", "dining table", "N/A", "N/A",
    "toilet", "N/A", "tv", "laptop", "mouse", "remote", "keyboard",
    "cell phone", "microwave", "oven", "toaster", "sink", "refrigerator",
    "N/A", "book", "clock", "vase", "scissors", "teddy bear",
    "hair drier", "toothbrush",
]

# Supported image extensions
SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".avif", ".bmp", ".tiff"}


# ─────────────────────────────────────────────
# Model Loading
# ─────────────────────────────────────────────

def get_device():
    """Detect the best available device for Apple Silicon / CPU."""
    if torch.backends.mps.is_available():
        print("  [INFO] Using Apple Silicon GPU (MPS)")
        return torch.device("mps")
    else:
        print("  [INFO] Using CPU")
        return torch.device("cpu")


def load_torchvision_model(model_fn, device):
    """Load a torchvision detection model with COCO-pretrained weights."""
    # torchvision >= 0.13 uses weights=; "DEFAULT" is the same COCO checkpoint
    # that pretrained=True loaded. Older versions only accept pretrained=True.
    try:
        model = model_fn(weights="DEFAULT")
    except TypeError:
        model = model_fn(pretrained=True)
    model.eval()
    # MPS has issues with some detection ops; fall back to CPU for inference
    # torchvision detection models work most reliably on CPU
    model.to("cpu")
    return model


def load_all_models(device):
    """
    Load all 7 models. Returns a dict of {name: (model, inference_fn)}.
    Each inference_fn takes a PIL image and returns (boxes, labels, scores).
    """
    models = {}

    print("\n[1/7] Loading DETR...")
    try:
        from transformers import DetrImageProcessor, DetrForObjectDetection, DetrConfig

        detr_processor = DetrImageProcessor.from_pretrained(
            "facebook/detr-resnet-50", revision="no_timm"
        )

        # Strategy: create a minimal config with dilation explicitly set,
        # then load pretrained weights into it
        try:
            from huggingface_hub import hf_hub_download
            config_path = hf_hub_download(
                "facebook/detr-resnet-50", "config.json", revision="no_timm"
            )
            with open(config_path, "r") as f:
                config_dict = json.load(f)
            # Patch the problematic field
            config_dict["dilation"] = False
            # Remove any keys DetrConfig doesn't recognize to avoid warnings
            detr_config = DetrConfig.from_dict(config_dict)
        except Exception:
            # Ultimate fallback: create default config with dilation=False
            detr_config = DetrConfig(dilation=False)

        detr_model = DetrForObjectDetection.from_pretrained(
            "facebook/detr-resnet-50",
            revision="no_timm",
            config=detr_config,
            ignore_mismatched_sizes=True,
        )
        detr_model.eval().to("cpu")

        def detr_infer(img):
            inputs = detr_processor(images=img, return_tensors="pt")
            with torch.no_grad():
                outputs = detr_model(**inputs)
            target_sizes = torch.tensor([img.size[::-1]])
            results = detr_processor.post_process_object_detection(
                outputs, target_sizes=target_sizes, threshold=CONFIDENCE_THRESHOLD
            )[0]
            boxes = results["boxes"].cpu()
            scores = results["scores"].cpu()
            labels = [
                detr_model.config.id2label.get(l.item(), f"class_{l.item()}")
                for l in results["labels"]
            ]
            return boxes, labels, scores

        models["DETR"] = detr_infer
        print("  [OK] DETR loaded")
    except Exception as e:
        print(f"  [SKIP] DETR failed to load: {e}")

    print("[2/7] Loading SSD...")
    try:
        ssd = load_torchvision_model(torchvision.models.detection.ssd300_vgg16, device)

        def ssd_infer(img):
            tensor = T.ToTensor()(img).unsqueeze(0)
            with torch.no_grad():
                preds = ssd(tensor)[0]
            mask = preds["scores"] >= CONFIDENCE_THRESHOLD
            boxes = preds["boxes"][mask].cpu()
            scores = preds["scores"][mask].cpu()
            labels = [COCO_LABELS[l] for l in preds["labels"][mask].tolist()]
            return boxes, labels, scores

        models["SSD"] = ssd_infer
        print("  [OK] SSD loaded")
    except Exception as e:
        print(f"  [SKIP] SSD failed to load: {e}")

    print("[3/7] Loading FCOS...")
    try:
        fcos = load_torchvision_model(torchvision.models.detection.fcos_resnet50_fpn, device)

        def fcos_infer(img):
            tensor = T.ToTensor()(img).unsqueeze(0)
            with torch.no_grad():
                preds = fcos(tensor)[0]
            mask = preds["scores"] >= CONFIDENCE_THRESHOLD
            boxes = preds["boxes"][mask].cpu()
            scores = preds["scores"][mask].cpu()
            labels = [COCO_LABELS[l] for l in preds["labels"][mask].tolist()]
            return boxes, labels, scores

        models["FCOS"] = fcos_infer
        print("  [OK] FCOS loaded")
    except Exception as e:
        print(f"  [SKIP] FCOS failed to load: {e}")

    print("[4/7] Loading Faster R-CNN...")
    try:
        frcnn = load_torchvision_model(
            torchvision.models.detection.fasterrcnn_resnet50_fpn, device
        )

        def frcnn_infer(img):
            tensor = T.ToTensor()(img).unsqueeze(0)
            with torch.no_grad():
                preds = frcnn(tensor)[0]
            mask = preds["scores"] >= CONFIDENCE_THRESHOLD
            boxes = preds["boxes"][mask].cpu()
            scores = preds["scores"][mask].cpu()
            labels = [COCO_LABELS[l] for l in preds["labels"][mask].tolist()]
            return boxes, labels, scores

        models["Faster R-CNN"] = frcnn_infer
        print("  [OK] Faster R-CNN loaded")
    except Exception as e:
        print(f"  [SKIP] Faster R-CNN failed to load: {e}")

    print("[5/7] Loading RetinaNet...")
    try:
        retina = load_torchvision_model(
            torchvision.models.detection.retinanet_resnet50_fpn, device
        )

        def retina_infer(img):
            tensor = T.ToTensor()(img).unsqueeze(0)
            with torch.no_grad():
                preds = retina(tensor)[0]
            mask = preds["scores"] >= CONFIDENCE_THRESHOLD
            boxes = preds["boxes"][mask].cpu()
            scores = preds["scores"][mask].cpu()
            labels = [COCO_LABELS[l] for l in preds["labels"][mask].tolist()]
            return boxes, labels, scores

        models["RetinaNet"] = retina_infer
        print("  [OK] RetinaNet loaded")
    except Exception as e:
        print(f"  [SKIP] RetinaNet failed to load: {e}")

    print("[6/7] Loading Mask R-CNN...")
    try:
        mrcnn = load_torchvision_model(
            torchvision.models.detection.maskrcnn_resnet50_fpn, device
        )

        def mrcnn_infer(img):
            tensor = T.ToTensor()(img).unsqueeze(0)
            with torch.no_grad():
                preds = mrcnn(tensor)[0]
            mask = preds["scores"] >= CONFIDENCE_THRESHOLD
            boxes = preds["boxes"][mask].cpu()
            scores = preds["scores"][mask].cpu()
            labels = [COCO_LABELS[l] for l in preds["labels"][mask].tolist()]
            return boxes, labels, scores

        models["Mask R-CNN"] = mrcnn_infer
        print("  [OK] Mask R-CNN loaded")
    except Exception as e:
        print(f"  [SKIP] Mask R-CNN failed to load: {e}")

    print("[7/7] Loading YOLO v11...")
    try:
        from ultralytics import YOLO
        yolo = YOLO("yolo11n.pt")  # Downloads automatically on first run

        def yolo_infer(img):
            results = yolo(img, verbose=False, conf=CONFIDENCE_THRESHOLD)[0]
            if results.boxes is None or len(results.boxes) == 0:
                return torch.zeros((0, 4)), [], torch.zeros(0)
            boxes = results.boxes.xyxy.cpu()
            scores = results.boxes.conf.cpu()
            labels = [results.names[int(c)] for c in results.boxes.cls.tolist()]
            return boxes, labels, scores

        models["YOLO v11"] = yolo_infer
        print("  [OK] YOLO v11 loaded")
    except Exception as e:
        print(f"  [SKIP] YOLO v11 failed to load: {e}")

    return models


# ─────────────────────────────────────────────
# Drawing & Tapestry Assembly
# ─────────────────────────────────────────────

def get_font(size=16):
    """Try to load a clean sans-serif font; fall back to default."""
    font_paths = [
        "/System/Library/Fonts/Helvetica.ttc",
        "/System/Library/Fonts/SFNSText.ttf",
        "/System/Library/Fonts/SFNSDisplay.ttf",
        "/Library/Fonts/Arial.ttf",
        "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "C:/Windows/Fonts/arial.ttf",
    ]
    for fp in font_paths:
        if os.path.exists(fp):
            try:
                return ImageFont.truetype(fp, size)
            except Exception:
                continue
    return ImageFont.load_default()


def draw_detections(pil_img, boxes, labels, scores, color_rgb):
    """
    Draw bounding boxes with labels and confidence scores on a PIL image.
    Returns a new PIL image with annotations.
    """
    img = pil_img.copy()
    draw = ImageDraw.Draw(img)
    font = get_font(size=max(14, int(min(img.size) * 0.025)))
    font_small = get_font(size=max(12, int(min(img.size) * 0.020)))

    for i in range(len(boxes)):
        box = boxes[i].tolist()
        x1, y1, x2, y2 = box
        label = labels[i]
        score = scores[i].item()

        # Draw box
        outline_width = max(2, int(min(img.size) * 0.004))
        draw.rectangle([x1, y1, x2, y2], outline=color_rgb, width=outline_width)

        # Compose label text
        text = f"{label}: {score:.2f}"

        # Measure text for background rectangle
        try:
            bbox = draw.textbbox((0, 0), text, font=font_small)
            tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
        except AttributeError:
            tw, th = draw.textsize(text, font=font_small)

        # Draw label background
        label_y = max(0, y1 - th - 6)
        draw.rectangle(
            [x1, label_y, x1 + tw + 8, label_y + th + 6],
            fill=color_rgb,
        )
        # Draw label text (white on colored background)
        draw.text((x1 + 4, label_y + 2), text, fill=(255, 255, 255), font=font_small)

    return img


def create_model_title_bar(text, width, color_rgb, bar_height=50):
    """Create a colored title bar with the model name centered."""
    bar = Image.new("RGB", (width, bar_height), color=(30, 30, 30))
    draw = ImageDraw.Draw(bar)
    font = get_font(size=max(20, int(bar_height * 0.5)))

    try:
        bbox = draw.textbbox((0, 0), text, font=font)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    except AttributeError:
        tw, th = draw.textsize(text, font=font)

    x = (width - tw) // 2
    y = (bar_height - th) // 2
    draw.text((x, y), text, fill=color_rgb, font=font)
    return bar


def build_tapestry(original_img, model_results, target_width=800):
    """
    Build a 2-row x 4-column grid image:
      Row 1: Original, DETR, SSD, FCOS
      Row 2: Faster R-CNN, RetinaNet, Mask R-CNN, YOLO v11
    Each cell has a title bar on top and the annotated image below.
    Annotations are drawn AFTER resizing so text stays crisp.
    target_width controls the TOTAL width of the grid.
    """
    cols = 4
    bar_height = 40
    padding = 4  # pixels between cells

    # Width of each cell
    cell_w = (target_width - padding * (cols - 1)) // cols

    # Resize original to cell width, preserving aspect ratio
    scale_x = cell_w / original_img.width
    cell_h = int(original_img.height * scale_x)
    scale_y = cell_h / original_img.height

    # Pre-resize the original once (all cells share this base)
    base_resized = original_img.resize((cell_w, cell_h), Image.LANCZOS)

    # Build ordered list: Original + all models
    ordered_names = ["Original"] + [
        name for name in MODEL_COLORS if name in model_results
    ]

    # Create each cell (title bar + image)
    cells = []
    for name in ordered_names:
        if name == "Original":
            color = (255, 255, 255)
            img_cell = base_resized.copy()
        else:
            color = MODEL_COLORS[name]
            boxes, labels, scores = model_results[name]

            # Scale bounding boxes to the resized cell dimensions
            if torch.is_tensor(boxes) and len(boxes) > 0:
                scaled_boxes = boxes.clone()
                scaled_boxes[:, 0] *= scale_x  # x1
                scaled_boxes[:, 1] *= scale_y  # y1
                scaled_boxes[:, 2] *= scale_x  # x2
                scaled_boxes[:, 3] *= scale_y  # y2
            else:
                scaled_boxes = boxes

            # Draw on the already-resized image so text is crisp
            img_cell = draw_detections(base_resized.copy(), scaled_boxes, labels, scores, color)

        title_bar = create_model_title_bar(name, cell_w, color, bar_height)

        # Combine title + image into one cell
        cell = Image.new("RGB", (cell_w, bar_height + cell_h), color=(30, 30, 30))
        cell.paste(title_bar, (0, 0))
        cell.paste(img_cell, (0, bar_height))
        cells.append(cell)

    # Arrange into 2 rows of 4
    rows = 2
    cell_total_h = bar_height + cell_h
    grid_w = cols * cell_w + padding * (cols - 1)
    grid_h = rows * cell_total_h + padding * (rows - 1)

    tapestry = Image.new("RGB", (grid_w, grid_h), color=(30, 30, 30))

    for idx, cell in enumerate(cells):
        row = idx // cols
        col = idx % cols
        x = col * (cell_w + padding)
        y = row * (cell_total_h + padding)
        tapestry.paste(cell, (x, y))

    return tapestry


# ─────────────────────────────────────────────
# Image Loading (handles all formats)
# ─────────────────────────────────────────────

def load_image(path):
    """Load any supported image format and convert to RGB PIL Image."""
    try:
        img = Image.open(path)
        img = img.convert("RGB")
        return img
    except Exception as e:
        print(f"  [WARN] Could not load {path}: {e}")
        return None


# ─────────────────────────────────────────────
# Main Pipeline
# ─────────────────────────────────────────────

def main():
    global CONFIDENCE_THRESHOLD

    print("[Script version: v6 — crisp labels fix]")

    parser = argparse.ArgumentParser(
        description="Run 7 object detection models and produce comparison tapestries."
    )
    parser.add_argument(
        "--input",
        type=str,
        default="./images",
        help="Path to folder containing input images",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="./results",
        help="Path to output folder for comparison tapestries",
    )
    parser.add_argument(
        "--width",
        type=int,
        default=1600,
        help="Total width of the output grid (default: 1600)",
    )
    parser.add_argument(
        "--threshold",
        type=float,
        default=0.50,
        help="Confidence threshold for detections (default: 0.50)",
    )
    parser.add_argument(
        "--save-json",
        type=str,
        default=None,
        help="Optional path of a JSON file to write all raw detections to",
    )
    args = parser.parse_args()

    CONFIDENCE_THRESHOLD = args.threshold

    input_dir = Path(args.input)
    output_dir = Path(args.output)

    if not input_dir.exists():
        print(f"[ERROR] Input directory does not exist: {input_dir}")
        sys.exit(1)

    output_dir.mkdir(parents=True, exist_ok=True)

    # Gather image files
    image_files = sorted([
        f for f in input_dir.iterdir()
        if f.suffix.lower() in SUPPORTED_EXTENSIONS
    ])

    if not image_files:
        print(f"[ERROR] No supported images found in {input_dir}")
        sys.exit(1)

    print(f"\n{'='*60}")
    print(f"  Object Detection Comparison Pipeline")
    print(f"{'='*60}")
    print(f"  Input:      {input_dir}")
    print(f"  Output:     {output_dir}")
    print(f"  Images:     {len(image_files)}")
    print(f"  Threshold:  {CONFIDENCE_THRESHOLD}")
    print(f"  Width:      {args.width}px")
    print(f"{'='*60}")

    # Load all models
    device = get_device()
    models = load_all_models(device)

    if not models:
        print("\n[ERROR] No models loaded successfully. Check your installations.")
        sys.exit(1)

    print(f"\n  Successfully loaded {len(models)}/{len(MODEL_COLORS)} models")
    print(f"{'='*60}\n")

    all_detections = {}

    # Process each image
    for img_path in tqdm(image_files, desc="Processing images"):
        tqdm.write(f"\n  Processing: {img_path.name}")

        img = load_image(img_path)
        if img is None:
            continue

        # Run all models
        model_results = {}
        for model_name, infer_fn in models.items():
            try:
                boxes, labels, scores = infer_fn(img)
                n_det = len(boxes) if torch.is_tensor(boxes) else 0
                tqdm.write(f"    {model_name:>15s}: {n_det} detections")
                model_results[model_name] = (boxes, labels, scores)
                all_detections.setdefault(img_path.name, {})[model_name] = [
                    {
                        "label": labels[i],
                        "score": round(float(scores[i]), 4),
                        "box_xyxy": [round(float(v), 1) for v in boxes[i].tolist()],
                    }
                    for i in range(n_det)
                ]
            except Exception as e:
                tqdm.write(f"    {model_name:>15s}: [ERROR] {e}")

        # Build tapestry
        tapestry = build_tapestry(img, model_results, target_width=args.width)

        # Save result
        out_name = f"res_{img_path.stem}.png"
        out_path = output_dir / out_name
        tapestry.save(out_path, quality=95)
        tqdm.write(f"    -> Saved: {out_path.name}")

    if args.save_json:
        Path(args.save_json).parent.mkdir(parents=True, exist_ok=True)
        with open(args.save_json, "w") as f:
            json.dump(
                {"threshold": CONFIDENCE_THRESHOLD, "detections": all_detections},
                f, indent=1,
            )
        print(f"  Raw detections written to: {args.save_json}")

    print(f"\n{'='*60}")
    print(f"  DONE! Results saved to: {output_dir}")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
