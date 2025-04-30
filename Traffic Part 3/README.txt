Traffic Sign Classifier (CNN with TensorFlow)

This project trains a Convolutional Neural Network (CNN) to classify German traffic signs using the [GTSRB dataset](https://benchmark.ini.rub.de/gtsrb_news.html). It includes:

- Data preprocessing with OpenCV  
- CNN model building with TensorFlow  
- Training with early stopping  
- Model saving with automatic versioning  
- Training history visualization

---

📁 Project Structure

```
traffic_sign_classifier/
│
├── traffic.py           # Main training script
├── README.md            # This file
├── modelV1.h5           # Example of a saved model
├── ...
└── gtsrb/               # Dataset folder (0–42 subfolders)
```

---

Requirements

Install dependencies:

```
pip install tensorflow opencv-python numpy matplotlib scikit-learn
```

---

###  How to Run

1. **Download and Extract GTSRB Dataset**  
   Ensure the dataset is structured like:

   ```
   gtsrb/
     ├— 0/
     ├— 1/
     ├— ...
     └— 42/
   ```

2. **Run the Script**

```
python traffic.py gtsrb
```

> Each run automatically saves the model as `modelV1.h5`, `modelV2.h5`, etc.

---

### 📊 Output

- Accuracy and loss curves plotted
- Evaluation results printed after training
- Models saved automatically in the script directory

---

### 🧐 Model Summary

- 2 × Conv2D + MaxPooling layers  
- Dense(128) + Dropout(0.5)  
- Softmax output layer with 43 categories

---
