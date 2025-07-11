﻿# Artificial-Intelligence-Group-Project

## Experimentation Process and Results

### Accuracy and Learning Curves
- The model achieved a final accuracy of **91.5%** on the test dataset.
- Learning curves showed steady improvement in both training and validation accuracy, with minimal overfitting due to the use of dropout layers and early stopping.
- Loss curves indicated smooth convergence, with validation loss stabilizing after approximately 15 epochs.

### Confusion Matrix
The confusion matrix revealed:
- High precision and recall for most classes.
- Slight misclassification in visually similar categories, which could be attributed to dataset noise or insufficient samples for those classes.

---

## Architecture and Hyperparameters

### Model Architecture
- **Input Layer**: Image size normalized to 32x32 pixels.
- **Convolutional Layers**: 
  - 2 Conv2D layers with ReLU activation and 32/64 filters, followed by MaxPooling.
- **Fully Connected Layers**:
  - Dense layer with 128 neurons and ReLU activation.
  - Dropout layer with a rate of 0.5 to prevent overfitting.
- **Output Layer**: Softmax activation with 43 categories (for traffic sign classification).

### Hyperparameters
- **Optimizer**: Adam with a learning rate of 0.001.
- **Batch Size**: 64.
- **Epochs**: 18-20 (with early stopping based on validation loss).
- **Loss Function**: Categorical Crossentropy.

---

## What Worked and What Didn’t

### What Worked
- **Data Augmentation**: Techniques like rotation, zoom, and horizontal flipping improved generalization.
- **Early Stopping**: Prevented overfitting by halting training when validation loss stopped improving.
- **Dropout Layers**: Helped reduce overfitting and improved model robustness.

### What Didn’t Work
- **Higher Learning Rates**: Caused unstable training and poor convergence.
- **Deeper Architectures**: Adding more layers led to overfitting due to the limited size of the dataset.

---

## Final Model Structure

The final model structure is as follows:
1. **Conv2D**: 32 filters, kernel size (3,3), ReLU activation.
2. **MaxPooling2D**: Pool size (2,2).
3. **Conv2D**: 64 filters, kernel size (3,3), ReLU activation.
4. **MaxPooling2D**: Pool size (2,2).
5. **Flatten**: Converts 2D feature maps to 1D.
6. **Dense**: 128 neurons, ReLU activation.
7. **Dropout**: Rate 0.5.
8. **Dense**: 43 neurons, Softmax activation.

---

This project demonstrates the effectiveness of CNNs in traffic sign classification and highlights the importance of careful hyperparameter tuning and regularization techniques.
