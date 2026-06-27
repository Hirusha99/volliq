# VolliQ 🏐

Volliq is a computer vision pipeline designed for athletic performance analysis in volleyball. It automatically synchronizes video feeds from a four-camera setup and utilizes the YOLOv8 model to detect, track, and analyze player movements across the court.

## 🚀 Key Features

* **Automated Multi-Camera Synchronization:** Aligns four distinct video feeds automatically (e.g., via audio signatures or frame timecodes) prior to processing.
* **YOLOv8 Player Tracking:** High-accuracy detection of players and the ball using fine-tuned YOLOv8 architectures.
* **Cross-Camera Re-identification:** Tracks distinct players seamlessly as they move across different camera fields of view.
* **Performance Analytics:** Extracts kinematic data, court positioning, and player trajectories to aid in sports performance analysis.

## 📁 Repository Structure

```text
├── Annotation_pipeline/
│   └── model/
│       ├── train24/             # Likely contains training run logs/weights
│       ├── best.pt              # Your fine-tuned YOLOv8 weights for volleyball/player detection
│       ├── app.py               # Main application script 
│       └── requirements.txt     
├── Traning_labelling/
│   ├── dataset/                 # Raw/processed images for training
│   ├── img/                     # Image storage
│   ├── data.yaml                # Dataset configuration file for YOLOv8 training
│   ├── labelling/
│   │   └── read.md              # Documentation specific to the labeling process
│   ├── runs/                    # YOLOv8 training output directories
│   ├── requirements.txt         # Dependencies specific to model training
│   └── train.ipynb              # Jupyter notebook for executing the YOLOv8 training loop
└── test-synconization/
    ├── requirements.txt         # Dependencies for the 4-camera synchronization tasks
    └── test_synco.ipynb         # Jupyter notebook dedicated to aligning the 4 video feeds

```
## 📊 Dataset

The model is trained and tested on the custom **VoLLIQ - Multiangle Volleyball Dataset**. This dataset contains annotated multi-camera footage specifically tailored for multi-player tracking in volleyball. 

* **Download the dataset here:** https://www.kaggle.com/datasets/nhwanigasingha/volliq-multiangle-volleyball-dataset/data

## Citation:
```
@misc{n_h__wanigasingha_m_k_a__ariyaratne_r_m__silva_2026,
	title={VoLLIQ - Multiangle Volleyball Dataset},
	url={https://www.kaggle.com/ds/10214908},
	DOI={10.34740/KAGGLE/DS/10214908},
	publisher={Kaggle},
	author={N.H. Wanigasingha and M.K.A. Ariyaratne and R.M. Silva},
	year={2026}
}
```
### License: CC BY-NC-SA 4.0

## 📊 Dataset Configuration & Setup

The **VoLLIQ - Multiangle Volleyball Dataset** is structured by Match  and Camera Angle (`AN01/`, `AN02/`...):

```text
VoLLIQ/
├── M1/
│   ├── AN01/
│   │   ├── frames/   # Contains frame_0000.jpg...
│   │   └── labels/   # Contains frame_0000.txt (YOLO format)
│   ├── AN02/
│   │   ├── frames/   # Contains frame_0000.jpg...
│   │   └── labels/   # Contains frame_0000.txt (YOLO format)
│   ├── AN03/
│   │   ├── frames/   # Contains frame_0000.jpg...
│   │   └── labels/   # Contains frame_0000.txt (YOLO format)
│   └── AN04/
│       ├── frames/   # Contains frame_0000.jpg...
│       └── labels/   # Contains frame_0000.txt (YOLO format)
```
### 📈 Dataset Statistics

The VoLLIQ dataset contains four object classes annotated in YOLO format.

* **Player_A** and **Player_B** dynamically classify on-court players into two distinct categories corresponding to the two opposing teams.
* **Judge** refers to the up judge (first referee).
* **Volleyball** denotes the match ball.

#### Dataset Summary Statistics

| Object Class | Total Bounding Boxes | Avg. Instances per Frame |
| ------------ | -------------------: | -----------------------: |
| Player_A     |              599,729 |                     6.01 |
| Player_B     |              559,286 |                     5.61 |
| Judge        |              100,134 |                     1.00 |
| Volleyball   |               10,550 |                     0.10 |

---


## 🚀 Project Architecture

The repository is modularized into three core components to manage synchronization, training, and deployment.

### 1. Training & Labeling (`Traning_labelling/`)

Contains:

* Dataset configuration (`data.yaml`)
* Annotation scripts
* Jupyter notebook (`train.ipynb`)

Used to fine-tune the YOLOv8 model on custom volleyball court data.

## 2. Synchronization (`test-synconization/`)

Contains:

* Experimental synchronization logic
* Notebook: `test_synco.ipynb`

Used to automatically align the four individual camera feeds into a synchronized timeline.

## 3. Inference & Annotation Pipeline (`Annotation_pipeline/`)

Contains:

* Fine-tuned model weights (`best.pt`)
* Main application script (`app.py`)

Used to perform player detection and tracking on synchronized volleyball footage.

---
## 💻 Usage Instructions

Follow these steps in order to process your multi-camera videos, train the tracking model, and deploy the inference application.


## 🛠️ Setup & Installation

It is recommended to use a virtual environment to manage project dependencies.

## 1. Clone the Repository

```bash
git clone https://github.com/Hirusha99/volliq.git
cd volliq
```

## 2. Create and Activate a Virtual Environment

### Using venv (Standard Python)

```bash
python -m venv venv
```

#### Linux / macOS

```bash
source venv/bin/activate
```

#### Windows

```bash
venv\Scripts\activate
```

## 3. Install Dependencies

Because the project is modular, install the dependencies required for the component you are using.

### Synchronization Module

```bash
pip install -r test-synconization/requirements.txt
```

### Training Module

```bash
pip install -r Traning_labelling/requirements.txt
```

### Inference Module

```bash
pip install -r Annotation_pipeline/model/requirements.txt
```

---

# 💻 Step-by-Step Usage Guide

Follow the workflow below to process raw volleyball footage and obtain player tracking results.

---

## Phase 1: Prepare and Synchronize Video Feeds

Before tracking can begin, the four camera feeds must be synchronized.

### Navigate to the Synchronization Module

```bash
cd test-synconization
```

### Launch the Notebook

```bash
jupyter notebook test_synco.ipynb
```

### Execute the Notebook

Run all notebook cells. The synchronization pipeline:

* Reads the raw video streams from camera angles AN01–AN04
* Computes temporal alignment parameters
* Synchronizes the video feeds
* Exports synchronized videos or aligned frame directories

### Verify Output

Ensure the synchronized videos or frame folders have been generated successfully before proceeding.

---

## Phase 2: Train the YOLOv8 Model (Optional)

> **Note:** If a trained `best.pt` model already exists, skip to Phase 3.

### Download and Extract the Dataset

Download the VoLLIQ dataset from Kaggle and extract it into:

```text
Traning_labelling/dataset/
```

### Navigate to the Training Module

```bash
cd ../Traning_labelling
```

### Verify Dataset Configuration

Open:

```text
img/data.yaml
```

Ensure that all dataset paths correctly point to the extracted directories.

### (Optional) Review or Modify Annotations

```bash
python labelling/labelling.py
```

### Launch Training

```bash
jupyter notebook train.ipynb
```

Run all cells to begin YOLOv8 training.

Training duration depends on the available hardware and GPU resources.

### Retrieve Trained Weights

After training completes, locate:

```text
runs/train/weights/best.pt
```

This file contains the best-performing model weights.

---

## Phase 3: Run the Tracking Application

Once the videos are synchronized and the model weights are ready, the tracking application can be executed.

### Navigate to the Deployment Module

```bash
cd ../Annotation_pipeline/model
```

### Place Model Weights

Copy your trained:

```text
best.pt
```

into:

```text
Annotation_pipeline/model/
```

Replace the existing model if necessary.

### Run the Application

```bash
python app.py
```
---
### View Results

The application will:

1. Load the YOLOv8 model.
2. Read the synchronized multi-camera video feeds.
3. Detect volleyball players and the ball.
4. Draw bounding boxes and tracking information.
5. Display or save the annotated output.

---
### 📌 Features

* Multi-camera volleyball video synchronization
* YOLOv8-based player and ball detection
* Custom VoLLIQ volleyball dataset
* End-to-end tracking pipeline
* Modular training, synchronization, and deployment framework
* Support for volleyball analytics and computer vision research




