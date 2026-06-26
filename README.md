# 📩 AI Spam Detector

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python\&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.x-orange?logo=scikitlearn\&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-2.x-blue?logo=pandas\&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-1.x-blue?logo=numpy\&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-Web_App-red?logo=streamlit\&logoColor=white)
![Status](https://img.shields.io/badge/Status-Live-success)

## 🌐 Live Demo

👉 **Try the Application:**
https://spamadetect.streamlit.app/

---

## 📌 Project Overview

AI Spam Detector is a Machine Learning and Natural Language Processing (NLP) web application that classifies messages as **Spam** or **Ham (Legitimate Message)** in real time.

The project demonstrates the complete machine learning workflow, including data preprocessing, text vectorization, model training, evaluation, deployment, and user interaction through a modern Streamlit web interface.

---

## 🎯 Objectives

* Preprocess and clean text data
* Convert text into numerical features using NLP techniques
* Train machine learning classification models
* Compare model performance
* Save trained models for future predictions
* Deploy a user-friendly web application

---

## 🛠 Technologies Used

* Python
* Pandas
* NumPy
* Scikit-learn
* Streamlit
* Joblib
* Natural Language Processing (NLP)
* Git & GitHub

---

## 📂 Dataset

The dataset consists of SMS messages labeled as:

| Label | Description                        |
| ----- | ---------------------------------- |
| Ham   | Legitimate messages                |
| Spam  | Promotional or fraudulent messages |

Dataset Size: **5,572 Messages**

---

## ⚙️ Machine Learning Workflow

### 1. Data Preprocessing

* Removed unnecessary columns
* Encoded labels into numerical values
* Converted text to lowercase
* Removed punctuation and numbers
* Removed extra whitespace

### 2. Text Vectorization

Implemented:

* CountVectorizer
* TF-IDF Vectorizer

These techniques transformed raw text into machine-learning-ready numerical vectors.

### 3. Model Training

Developed and evaluated:

* Multinomial Naive Bayes
* Logistic Regression

### 4. Model Evaluation

Models were evaluated using:

* Accuracy
* Precision
* Recall
* F1 Score
* Confusion Matrix

### 5. Model Deployment

The best-performing model was deployed using Streamlit, allowing users to perform real-time spam detection through a web interface.

---

## 🚀 Features

✅ Spam/Ham Classification

✅ Real-Time Prediction

✅ Interactive Streamlit Dashboard

✅ Confidence Score Visualization

✅ Machine Learning Model Deployment

✅ Responsive User Interface

---

## 📊 Model Comparison

| Model                   | Vectorizer      |
| ----------------------- | --------------- |
| Multinomial Naive Bayes | TF-IDF          |
| Logistic Regression     | CountVectorizer |

**Selected Model for Deployment:** Logistic Regression + CountVectorizer
---

## 📈 Skills Demonstrated

* Machine Learning
* Natural Language Processing (NLP)
* Text Classification
* Feature Engineering
* Model Evaluation
* Data Cleaning
* Python Programming
* Streamlit Deployment
* GitHub Version Control

---

## 👩‍💻 Author

Amalki Fernando
