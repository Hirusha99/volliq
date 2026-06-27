# LabelImg Setup Guide Using Python Virtual Environment

This guide explains how to install and run **LabelImg** using a Python virtual environment in VS Code.

## Requirements

- Python 3.9 installed
- Visual Studio Code
- VS Code Terminal

---

## Step 1: Check Python Version

Open the VS Code terminal and check the installed Python 3.9 version:

```bash
py -3.9 --version
```
---

## Step 2: Create a Virtual Environment

Create a virtual environment named label_venv:

```bash
py -3.9 -m venv label_venv
```
---

## Step 3: Activate Virtual Environment

```bash
.\label_venv\Scripts\activate
```
After activation, the environment name will appear in the terminal:

```
(label_venv)
```

---
## Step 4: Install LabelImg

```bash
pip install labelImg
```
---
## Step 5: Run LabelImg

```bash
labelImg
```
The LabelImg annotation interface will open, and you can start labeling your images.
---