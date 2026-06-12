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
│   │   ├── labelling.py         # Script used to generate or manage bounding box annotations
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

* **Download the dataset here:** (https://www.kaggle.com/datasets/nhwanigasingha/volliq-multiangle-volleyball-dataset/data)

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