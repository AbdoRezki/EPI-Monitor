# EPI Detection – YOLOv8 & Tkinter GUI

Real-time detection of Personal Protective Equipment (PPE) (helmet, mask, safety glasses, safety vest) from a camera stream using a YOLOv8 model and a **Tkinter/CustomTkinter** graphical interface.

## Features

- Real-time webcam detection of safety helmet, mask, safety glasses, and high-visibility safety vest.
- Graphical interface with dedicated buttons for each PPE type and live status display (red/green text) for each detection.
- Uses YOLOv8 models trained on a PPE dataset (including `nohelmet` / `helmet` classes) for robust detection on images and video frames.

## Project Structure

- `Epi-detection.ipynb`: Notebook for training the YOLOv8 model (data preparation, `config.yaml` creation, training, evaluation, and export of model weights).  
- `config.yaml`: YOLO configuration defining dataset paths and classes `nohelmet` and `helmet` for training and validation.
- `gui.py`: Tkinter/CustomTkinter application that loads YOLO weights, opens the webcam, performs real-time PPE detection, and displays results in the GUI. 

## Requirements

- Python 3.10+ recommended. 
- Main Python dependencies: `ultralytics` (YOLOv8), `opencv-python`, `customtkinter`, `tkinter`, `Pillow`, `numpy`, `pyyaml`, `json`.

Example installation:

```bash
pip install ultralytics opencv-python customtkinter pillow numpy pyyaml
```

## Training the Model (Optional)

- Use `Epi-detection.ipynb` to prepare the dataset (images and labels), configure `config.yaml`, and launch YOLOv8 training with the defined classes.
- After training, copy the generated weights (e.g. best.pt) from runs/detect/train/weights to the paths expected by gui.py for the PPE and glasses models.

## Running the GUI Application

- Update the model paths in `gui.py` so that the PPE model and glasses model point to your YOLOv8 weight files.
- Start the app:

```bash
python gui.py
```
- In the window, choose “Detect safety glasses”, “Detect safety helmet”, “Detect mask”, or “Detect safety vest”, click “Open camera”, and wait for detections to appear with bounding boxes and status text.

