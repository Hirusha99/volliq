import os
import sys

def compute_iou(box1, box2):
    """
    Computes Intersection over Union (IoU) between two bounding boxes.
    Each box format: (xmin, ymin, xmax, ymax)
    """
    x1_1, y1_1, x2_1, y2_1 = box1
    x1_2, y1_2, x2_2, y2_2 = box2
    
    # Intersection coordinates
    xi1 = max(x1_1, x1_2)
    yi1 = max(y1_1, y1_2)
    xi2 = min(x2_1, x2_2)
    yi2 = min(y2_1, y2_2)
    
    inter_width = max(0.0, xi2 - xi1)
    inter_height = max(0.0, yi2 - yi1)
    inter_area = inter_width * inter_height
    
    # Area of each box
    area1 = (x2_1 - x1_1) * (y2_1 - y1_1)
    area2 = (x2_2 - x1_2) * (y2_2 - y1_2)
    
    # Union area
    union_area = area1 + area2 - inter_area
    
    if union_area <= 0.0:
        return 0.0
    return inter_area / union_area

def parse_annotation_file(file_path):
    """
    Parses YOLO format file and converts coordinates to (xmin, ymin, xmax, ymax).
    Returns list of tuples: (class_id, (xmin, ymin, xmax, ymax))
    """
    boxes = []
    if not os.path.exists(file_path):
        return boxes
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split()
            if len(parts) != 5:
                continue
            try:
                class_id = int(parts[0])
                x_center = float(parts[1])
                y_center = float(parts[2])
                width = float(parts[3])
                height = float(parts[4])
                
                # Convert to corner format
                xmin = x_center - width / 2.0
                ymin = y_center - height / 2.0
                xmax = x_center + width / 2.0
                ymax = y_center + height / 2.0
                
                boxes.append((class_id, (xmin, ymin, xmax, ymax)))
            except ValueError:
                continue
    return boxes

def match_boxes(boxes1, boxes2, iou_threshold=0.5):
    """
    Greedily matches two lists of boxes based on their IoU coordinates.
    
    Returns:
        matched_pairs: list of ((class_id1, box1), (class_id2, box2), iou)
        unmatched1: list of unmatched (class_id, box) from boxes1
        unmatched2: list of unmatched (class_id, box) from boxes2
    """
    pairs = []
    for i, b1 in enumerate(boxes1):
        for j, b2 in enumerate(boxes2):
            iou = compute_iou(b1[1], b2[1])
            if iou >= iou_threshold:
                pairs.append((iou, i, j))
                
    # Sort pairs by highest IoU descending
    pairs.sort(key=lambda x: x[0], reverse=True)
    
    matched1_indices = set()
    matched2_indices = set()
    matched_pairs = []
    
    for iou, idx1, idx2 in pairs:
        if idx1 not in matched1_indices and idx2 not in matched2_indices:
            matched1_indices.add(idx1)
            matched2_indices.add(idx2)
            matched_pairs.append((boxes1[idx1], boxes2[idx2], iou))
            
    unmatched1 = [boxes1[i] for i in range(len(boxes1)) if i not in matched1_indices]
    unmatched2 = [boxes2[j] for j in range(len(boxes2)) if j not in matched2_indices]
    
    return matched_pairs, unmatched1, unmatched2

def load_class_names(classes_path):
    """Loads classes map from classes.txt if present."""
    if not os.path.exists(classes_path):
        return {}
    with open(classes_path, 'r', encoding='utf-8') as f:
        names = [line.strip() for line in f if line.strip()]
    return {i: name for i, name in enumerate(names)}

def compare_directories(dir_a, dir_b, iou_threshold=0.5, output_file=None):
    # Load class maps
    classes_a = load_class_names(os.path.join(dir_a, 'classes.txt'))
    classes_b = load_class_names(os.path.join(dir_b, 'classes.txt'))
    # Use union or fallback to index strings
    class_map = {}
    all_class_ids = set(classes_a.keys()).union(classes_b.keys())
    for cid in all_class_ids:
        name_a = classes_a.get(cid)
        name_b = classes_b.get(cid)
        class_map[cid] = name_a or name_b or f"Class_{cid}"

    # Get txt files (excluding classes.txt)
    files_a = set(f for f in os.listdir(dir_a) if f.endswith('.txt') and f != 'classes.txt')
    files_b = set(f for f in os.listdir(dir_b) if f.endswith('.txt') and f != 'classes.txt')
    
    common_files = sorted(list(files_a.intersection(files_b)))
    only_a = sorted(list(files_a - files_b))
    only_b = sorted(list(files_b - files_a))
    
    # Aggregated metrics
    total_boxes_a = 0
    total_boxes_b = 0
    total_matches = 0
    total_class_matches = 0
    sum_iou_matches = 0.0
    
    # Class mapping mismatch count: { (class_a, class_b): count }
    mismatches = {}
    
    # Unmatched counts by class ID
    unmatched_a_counts = {}
    unmatched_b_counts = {}
    
    for filename in common_files:
        path_a = os.path.join(dir_a, filename)
        path_b = os.path.join(dir_b, filename)
        
        boxes_a = parse_annotation_file(path_a)
        boxes_b = parse_annotation_file(path_b)
        
        total_boxes_a += len(boxes_a)
        total_boxes_b += len(boxes_b)
        
        matches, un_a, un_b = match_boxes(boxes_a, boxes_b, iou_threshold)
        
        total_matches += len(matches)
        for b1, b2, iou in matches:
            sum_iou_matches += iou
            c1, c2 = b1[0], b2[0]
            if c1 == c2:
                total_class_matches += 1
            else:
                mismatches[(c1, c2)] = mismatches.get((c1, c2), 0) + 1
                
        for b in un_a:
            cid = b[0]
            unmatched_a_counts[cid] = unmatched_a_counts.get(cid, 0) + 1
            
        for b in un_b:
            cid = b[0]
            unmatched_b_counts[cid] = unmatched_b_counts.get(cid, 0) + 1

    # Build Report
    report = []
    report.append("=" * 60)
    report.append(" INTER-ANNOTATOR AGREEMENT REPORT")
    report.append("=" * 60)
    report.append(f"Comparing Directories:\n  A: {dir_a}\n  B: {dir_b}\n")
    report.append(f"File Overview:")
    report.append(f"  Files in A:         {len(files_a)}")
    report.append(f"  Files in B:         {len(files_b)}")
    report.append(f"  Common files:       {len(common_files)}")
    if only_a:
        report.append(f"  Only in A:          {len(only_a)} files (e.g. {only_a[:3]})")
    if only_b:
        report.append(f"  Only in B:          {len(only_b)} files (e.g. {only_b[:3]})")
    report.append("-" * 60)
    
    report.append(f"Annotation Metrics (IoU Threshold: {iou_threshold}):")
    report.append(f"  Total annotations in A: {total_boxes_a}")
    report.append(f"  Total annotations in B: {total_boxes_b}")
    report.append(f"  Total matched boxes:    {total_matches}")
    
    if total_boxes_a + total_boxes_b > 0:
        f1_score = 2.0 * total_matches / (total_boxes_a + total_boxes_b)
        report.append(f"  Symmetric F1-score:     {f1_score:.4f} (Agreement on object presence)")
    else:
        report.append("  Symmetric F1-score:     N/A (No boxes)")
        
    if total_matches > 0:
        avg_iou = sum_iou_matches / total_matches
        class_accuracy = total_class_matches / total_matches
        report.append(f"  Average IoU of matches: {avg_iou:.4f} (Localization agreement)")
        report.append(f"  Label Agreement Rate:   {class_accuracy:.2%} (Classification agreement on matches)")
    else:
        report.append("  Average IoU of matches: N/A")
        report.append("  Label Agreement Rate:   N/A")
    report.append("-" * 60)

    # Class-level unmatched breakdown
    has_unmatched = False
    report.append("Unmatched Annotations Breakdown:")
    for cid in sorted(all_class_ids):
        count_a = unmatched_a_counts.get(cid, 0)
        count_b = unmatched_b_counts.get(cid, 0)
        if count_a > 0 or count_b > 0:
            has_unmatched = True
            cname = class_map.get(cid, f"Class {cid}")
            report.append(f"  {cname:<15} -> Unmatched in A: {count_a:<5} | Unmatched in B: {count_b:<5}")
    if not has_unmatched:
        report.append("  None. All objects matched between annotators.")
    report.append("-" * 60)

    # Classification conflicts breakdown
    report.append("Classification Label Mismatches:")
    if mismatches:
        for (c1, c2), count in sorted(mismatches.items(), key=lambda x: x[1], reverse=True):
            name1 = class_map.get(c1, f"Class {c1}")
            name2 = class_map.get(c2, f"Class {c2}")
            report.append(f"  A labeled '{name1}' but B labeled '{name2}': {count} times")
    else:
        report.append("  None. No labeling conflicts among matched objects.")
    report.append("=" * 60)

    report_text = "\n".join(report)
    print(report_text)
    
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(report_text)
            f.write('\n')
        print(f"\nReport saved to: {output_file}")

if __name__ == '__main__':
    # Default directories
    script_dir = os.path.dirname(os.path.abspath(__file__))
    dir_a = os.path.join(script_dir, 'annotated-rusiru')
    dir_b = os.path.join(script_dir, 'annotated-hirusha')
    
    # Allow overriding directories via arguments
    if len(sys.argv) >= 3:
        dir_a = sys.argv[1]
        dir_b = sys.argv[2]
        
    iou_thresh = 0.5
    if len(sys.argv) >= 4:
        try:
            iou_thresh = float(sys.argv[3])
        except ValueError:
            pass
            
    out_file = os.path.join(script_dir, 'agreement_report-rusiru-hirusha.txt')
    if len(sys.argv) >= 5:
        out_file = sys.argv[4]
            
    compare_directories(dir_a, dir_b, iou_threshold=iou_thresh, output_file=out_file)
