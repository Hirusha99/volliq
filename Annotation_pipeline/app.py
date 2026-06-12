import os
import cv2
import argparse
import zipfile
import tempfile
from ultralytics import YOLO
import gradio as gr
import imageio_ffmpeg

def process_video(video_path, skip_frames):
    if not video_path:
        raise gr.Error("Error: Please upload a video first!")

    model_path = r"E:\Hiru\data_set_final\data_set_final\model\best.pt"
    if not os.path.exists(model_path):
        raise gr.Error(f"Error: Model not found at {model_path}")
        
    try:
        model = YOLO(model_path)
    except Exception as e:
        raise gr.Error(f"Error loading YOLO model: {e}")

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise gr.Error("Error opening video.")

    fps = int(cap.get(cv2.CAP_PROP_FPS))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    # We will create a temp directory in the current drive to store frames and labels
    # Default Windows temp drive is full (OSError: [Errno 28] No space left on device)
    base_temp_dir = r"e:\Hirusha\data_set_final\temp"
    os.makedirs(base_temp_dir, exist_ok=True)
    temp_dir = tempfile.mkdtemp(dir=base_temp_dir)
    frames_dir = os.path.join(temp_dir, "frames")
    labels_dir = os.path.join(temp_dir, "labels")
    os.makedirs(frames_dir, exist_ok=True)
    os.makedirs(labels_dir, exist_ok=True)

    # We will also create an output video with annotations drawn
    out_video_path = os.path.join(temp_dir, "annotated_video.avi")
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    # Use standard fps so the browser doesn't choke on a 1 FPS video
    out = cv2.VideoWriter(out_video_path, fourcc, fps, (width, height))

    frame_idx = 0
    saved_idx = 0
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
            
        if frame_idx % skip_frames == 0:
            # 1. Run inference
            results = model(frame, verbose=False)
            result = results[0]
            boxes = result.boxes
            
            # 2. Save image and label
            frame_name = f"frame_{saved_idx:04d}.jpg"
            label_name = f"frame_{saved_idx:04d}.txt"
            
            cv2.imwrite(os.path.join(frames_dir, frame_name), frame)
            
            with open(os.path.join(labels_dir, label_name), 'w') as f:
                if boxes:
                    for box in boxes:
                        cls = int(box.cls[0])
                        x, y, w, h = box.xywhn[0].tolist() 
                        f.write(f"{cls} {x:.6f} {y:.6f} {w:.6f} {h:.6f}\n")
            
            # 3. Draw annotations on frame and write to video
            annotated_frame = result.plot()
            out.write(annotated_frame)
            
            saved_idx += 1
            
        frame_idx += 1
        
    cap.release()
    out.release()
    
    # Gradio/Browsers require H264 encoding to play MP4 files, but cv2's 'mp4v' doesn't always work.
    # We will use ffmpeg to quickly re-encode the video.
    h264_out_path = os.path.join(temp_dir, "annotated_video_h264.mp4")
    ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
    
    import subprocess
    try:
        subprocess.run([
            ffmpeg_exe, "-y", "-i", out_video_path, "-vcodec", "libx264", h264_out_path
        ], check=True, capture_output=True)
    except subprocess.CalledProcessError as e:
        print(f"FFmpeg error: {e.stderr.decode()}")
        # Fallback to the original video if encoding fails
        h264_out_path = out_video_path
    
    # Create a zip of frames and labels
    zip_path = os.path.join(temp_dir, "dataset.zip")
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for root, _, files in os.walk(frames_dir):
            for file in files:
                zipf.write(os.path.join(root, file), os.path.join("frames", file))
        for root, _, files in os.walk(labels_dir):
            for file in files:
                zipf.write(os.path.join(root, file), os.path.join("labels", file))
                
    return h264_out_path, h264_out_path, zip_path

def gradio_interface():
    with gr.Blocks(title="Auto-Annotation Tool") as app:
        gr.Markdown("# Video Auto-Annotation Tool")
        gr.Markdown("Upload a video. The tool will automatically extract frames, annotate them using the default model, and provide a downloadable dataset (images + YOLO labels) as well as the annotated video.")
        
        with gr.Row():
            with gr.Column():
                video_input = gr.File(label="Upload Video File (Any Format)")
                skip_frames_input = gr.Slider(minimum=1, maximum=120, value=30, step=1, label="Extract Every Nth Frame")
                process_btn = gr.Button("Process Video", variant="primary")
                
            with gr.Column():
                video_output = gr.Video(label="Annotated Video")
                video_download = gr.File(label="Download Annotated Video")
                zip_output = gr.File(label="Download Dataset (Frames + Labels ZIP)")
                
        process_btn.click(
            fn=process_video,
            inputs=[video_input, skip_frames_input],
            outputs=[video_output, video_download, zip_output]
        )
        
    # app.launch(server_name="127.0.0.1", server_port=7860, share=False)
    app.launch(server_name="127.0.0.1", server_port=None, share=False)

if __name__ == "__main__":
    gradio_interface()
