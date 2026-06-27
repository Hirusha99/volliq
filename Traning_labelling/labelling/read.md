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
---

# LabelImg Manual Annotation Guide

This guide explains how to install, open, and use **LabelImg** for creating manual image annotations.

The provided ZIP file contains a video tutorial explaining the complete process of creating manual annotations using LabelImg.

Link: https://drive.google.com/file/d/1o8bfTL4vGhkYxqjQEOOolm7DFoX7Neoq/view?usp=sharing
---