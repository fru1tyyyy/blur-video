# Computer Vision Projects using OpenCV and NumPy

This repository contains two computer vision implementations written in **Python** using **OpenCV** and **NumPy**. The projects demonstrate practical techniques in document image analysis and video processing, including segmentation, face anonymization, watermarking, and video compositing.

---

## Table of Contents
1. [Paragraph Extraction from Document Images](#1-paragraph-extraction-from-document-images)
2. [Video Processing with Face Blurring and Watermarking](#2-video-processing-with-face-blurring-and-watermarking)
3. [Project Structure](#project-structure)
4. [Requirements](#requirements)
5. [How to Run](#how-to-run)
6. [Applications](#applications)
7. [Notes](#notes)

---

## 1. Paragraph Extraction from Document Images

### Overview
This module automatically extracts paragraph regions from scanned document images using **projection profile analysis**. It is designed for documents with multiple columns and clearly separated paragraphs.

Each detected paragraph is cropped, refined, and saved as an individual image file.



### Key Features
- Grayscale image processing
- Binary image thresholding
- Column detection using **vertical projections**
- Paragraph detection using **horizontal projections**
- Whitespace trimming on all sides
- Noise and size filtering
- Batch processing of multiple images

### Input
- Images named `001.png` to `008.png` located in the `img/` directory.
- Assumes black text on a white background.

### Output
- Extracted paragraph images saved in: `extracted_paragraphs/`
- **Naming format:** `image_<image_number>para<paragraph_number>.png`

---

## 2. Video Processing with Face Blurring and Watermarking

### Overview
This module processes a traffic video by detecting ambient lighting conditions, enhancing visibility, anonymizing faces, and applying professional overlays and endscreens.



### Key Features
- **Automatic Day/Night Detection:** Analyzes frame brightness to determine scene type.
- **Brightness Enhancement:** Uses HSV color space manipulation for night-time footage.
- **Privacy Anonymization:** Face detection via Haar Cascades with Gaussian blur.
- **Compositing:** Picture-in-picture (PiP) video overlay and dynamic watermarking.
- **Video Concatenation:** Seamlessly appends an endscreen video to the processed output.

### Input Files
- `video/traffic.mp4` — Main video
- `video/talking.mp4` — Overlay video
- `video/endscreen.mp4` — Endscreen video
- `img/watermark1.png` — Active overlay watermark
- `img/watermark2.png` — Standard watermark
- `face_detector.xml` — Haar Cascade model

### Output
- Final processed video: `traffic.avi`

---

## 3. Project Structure

```text
├── img/
│   ├── 001.png ... 008.png
│   ├── watermark1.png
│   └── watermark2.png
├── video/
│   ├── traffic.mp4
│   ├── talking.mp4
│   └── endscreen.mp4
├── extracted_paragraphs/
├── face_detector.xml
├── paragraph_extraction.py
├── video_processing.py
└── README.md

```
## 4. Requirements
Ensure you have Python installed, then install the required libraries:
```Bash
pip install opencv-python numpy
```
---
## 5. How to Run
Document Analysis
To extract paragraphs from the images in the img/ folder:
```Bash
python paragraph_extraction.py
```
---
Video Analysis
To process the video with face blurring and overlays:
```Bash
python video_processing.py
```
---

## 6. Applications
Document Layout Analysis: Pre-processing for OCR (Optical Character Recognition).

Privacy-Preserving Analytics: Anonymizing individuals in public traffic or surveillance feeds.

Surveillance Enhancement: Improving visibility in night-time security monitoring.

Multimedia Content Production: Automating video overlays and watermarking.

---
## 7. Notes
Thresholds: The sensitivity of paragraph detection depends on the "gap" size between text. You may need to adjust the threshold variables in the script for different font sizes.

Paths: Ensure your video and image filenames match the scripts exactly or update the file paths within the code.

Resizing: The system resizes frames to a consistent resolution to ensure proper video concatenation.
