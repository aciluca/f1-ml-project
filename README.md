# Formula 1 Machine Learning Project

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This repository hosts a data analysis and machine learning project applied to official Formula 1 race data. The goal is to use telemetry, lap times, and weather data to build predictive models and uncover hidden patterns in driver and team performance.

The project leverages the power of the [fastf1](https://github.com/theOehrly/Fast-F1) library for data access and standard data science libraries like Pandas, Scikit-learn, and (optionally) TensorFlow/PyTorch for modeling.

---

## 🎯 Project Goals

*   **Exploratory Data Analysis (EDA):** Visualize and understand race dynamics (tire degradation, strategies, lap performance).
*   **Feature Engineering:** Create meaningful features from raw telemetry and timing data.
*   **Predictive Modeling:** Develop machine learning models to predict outcomes such as:
    *   Lap Time.
    *   Tire compound degradation.
    *   A driver's unique driving style.

---

## 🛠️ Tech Stack

*   **Data Access:** [`fastf1`](https://docs.fastf1.dev/)
*   **Data Manipulation:** [`Pandas`](https://pandas.pydata.org/), [`NumPy`](https://numpy.org/)
*   **Data Visualization:** [`Matplotlib`](https://matplotlib.org/), [`Seaborn`](https://seaborn.pydata.org/)
*   **Machine Learning:** [`Scikit-learn`](https://scikit-learn.org/)
*   **Notebooks:** [`Jupyter Lab`](https://jupyter.org/)

---

## 🚀 Getting Started

Follow these steps to set up the development environment locally.

### Prerequisites

*   [Python 3.9+](https://www.python.org/downloads/)
*   [Git](https://git-scm.com/)

### Installation

1.  **Clone the repository:**
    ```sh
    git clone https://github.com/YOUR_USERNAME/f1-ml-project.git
    cd f1-ml-project
    ```

2.  **Create and activate a virtual environment:**
    ```sh
    # Create the venv
    python -m venv venv

    # Activate it (Windows PowerShell)
    .\venv\Scripts\activate

    # Activate it (macOS/Linux)
    # source venv/bin/activate
    ```

3.  **Install the dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

---

## 📂 Project Structure

The project is organized to separate logic, analysis, and data.

```
├── data/               # Raw and processed datasets
│   ├── raw/
│   └── processed/
├── models/             # Trained and saved models
├── notebooks/          # Jupyter notebooks for analysis, prototyping, and visualization
├── src/                # Python scripts with reusable logic
│   ├── data_loader.py
│   ├── preprocessing.py
│   ├── train.py
│   └── ...
├── .gitignore          # Files to be ignored by Git
├── README.md           # This file
└── requirements.txt    # List of Python dependencies
```

---

## 📈 Usage

1.  **Data Exploration:** Open the `notebooks/` directory to find examples of how to download and visualize data with `fastf1`. Start with `01_data_exploration.ipynb`.
2.  **Model Training:** Run scripts from the `src/` directory to process data and launch a full training pipeline.
    ```sh
    python src/train.py
    ```

---

## 📄 License

This project is released under the MIT License. See the `LICENSE` file for more details.

---

## ✍️ Author

*   **[Luca Acerbi]** - [aciluca](https://github.com/aciluca)

---
