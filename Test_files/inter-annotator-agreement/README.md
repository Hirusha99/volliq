# Inter-Annotator Agreement Report Guide

This document explains the metrics generated in the `agreement_report.txt` file which compares annotations created by two different annotators (e.g., comparing the original annotations in `annotated/` vs. the adjusted ones in `transformed/`).

---

## Metric Breakdown & Interpretations

### 1. File Overview
- **Files in A & B / Common Files**: Lists how many files exist in each directory and how many are matched by name. Comparison is only run on common file names.

### 2. Symmetric F1-score (Presence Agreement)
- **What it means**: Measures how well both annotators agreed on the **existence** of objects.
- **Formula**: 
  $$F_1 = \frac{2 \times \text{Matched Boxes}}{\text{Total Boxes in A} + \text{Total Boxes in B}}$$
- **Interpretation**: 
  - Ranges from `0.0` (complete disagreement) to `1.0` (perfect agreement).
  - A high F1-score (e.g., `0.9556`) indicates that both annotators labeled almost the same physical objects.
  - A low F1-score indicates that one annotator frequently missed objects that the other labeled.

### 3. Average IoU of Matches (Localization Agreement)
- **What it means**: Measures how precisely the matched bounding boxes are aligned **spatially**.
- **Formula**: 
  - **Intersection over Union (IoU)** calculates the overlap area divided by the union area of two boxes:
    $$\text{IoU} = \frac{\text{Area of Intersection}}{\text{Area of Union}}$$
  - The report displays the average IoU across all matched bounding boxes.
- **Interpretation**: 
  - Ranges from the threshold (e.g., `0.5`) to `1.0`.
  - An average IoU of `0.7586` indicates high localization precision, though there are slight offsets in how boundaries/edges were drawn.
  - *Note on scale*: Very small objects (like `Ball`) are highly sensitive to small pixel offsets. A minor center shift of 0.003 units can lower IoU significantly, which is why a lower threshold (e.g. `0.1`) might match more objects.

### 4. Label Agreement Rate (Classification Agreement)
- **What it means**: Measures how consistently the annotators categorized the matched objects.
- **Formula**: 
  $$\text{Label Agreement} = \frac{\text{Matched Boxes with Same Class}}{\text{Total Matched Boxes}}$$
- **Interpretation**: 
  - A rate of `100.00%` means that whenever both annotators identified the same object, they assigned the exact same class label (e.g., both labeled it `Player_A`).
  - A lower rate indicates classification confusion (e.g., one labeling a person as `Player_A` and another labeling them as `Player_B`).

---

## Section Breakdowns

### Unmatched Annotations Breakdown
Lists the count of annotations that could not be matched under the given IoU threshold, broken down by class.
- **Unmatched in A**: Annotator A drew a box, but Annotator B either missed it entirely or drew a box with too low of an IoU to match.
- **Unmatched in B**: Annotator B drew a box that Annotator A missed or did not overlap with.

### Classification Label Mismatches
Lists any label conflicts for successfully matched bounding boxes (where spatial overlap was $\ge \text{threshold}$ but classification disagreed).
- *Example*: `A labeled 'Player_A' but B labeled 'Player_B'`
- Helpful for identifying ambiguous classes or systemic annotator bias.
