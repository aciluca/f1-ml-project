# Formula 1 Session Analysis Tool

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)


This repository hosts a desktop application for analyzing official Formula 1 race data. The application, built in Python with a Tkinter GUI, allows users to visualize and compare driver performance through detailed analyses.

Currently in its early development stage, this tool provides a solid foundation for more complex F1 data analysis and a future pivot towards machine learning applications.
The project leverages the power of the [fastf1](https://github.com/theOehrly/Fast-F1) library for data access and standard data science libraries like Pandas, Matplotlib, and Seaborn for analysis and visualization.

---

## ⭐️ Project Status & Roadmap

### Current Version: v0.2 - Analysis Tool Alpha

This project is currently at **Version 0.2**. At this stage, the core architecture is complete, and the application serves as a robust tool for a specific type of visual analysis.

**What's included in v0.2:**
*   A functional, standalone **desktop application** with a clean Tkinter interface.
*   **Dynamic data loading** engine that fetches session data based on user selection.
*   A single, powerful **analysis module**: Lap Time Distribution Box Plot.
*   A professional, **modular code structure** that separates the GUI, configuration, and analysis logic, making the project easy to maintain and extend.

### Future Goals (The Roadmap)

The vision for this project extends beyond its current capabilities. Future versions will focus on:
*   **More Analysis Modules:** Integrating new plots, such as:
    *   Tire strategy visualization (Gantt chart).
    *   Head-to-head telemetry comparisons.
    *   Pace analysis over race stints.
*   **Data Export:** Adding functionality to save charts as images or export processed data to CSV files.
*   **Foundation for Machine Learning:** Building data preprocessing scripts to create clean datasets, which will be the first step towards achieving the original ML goals (e.g., lap time prediction).
*   **UI/UX Enhancements:** Improving the user interface with features like progress bars, themes, and more detailed status updates.

---

## ✨ Core Features (in v0.2)

*   **Desktop GUI:** An easy-to-use application built with Tkinter.
*   **Dynamic Session Selection:** Choose a year, and the event dropdown menu automatically updates with the correct race calendar.
*   **Lap Time Distribution Analysis:** Generates a grid of box plots to visualize the consistency and pace of each driver.
*   **Compound-Based Comparison:** Within each driver's plot, lap times are broken down by the tire compound used.
*   **Smart Outlier Filtering:** Unusually slow laps are filtered out on a per-compound basis to provide a more realistic view of true pace.

---

## 🛠️ Tech Stack

*   **GUI:** [`Tkinter`](https://docs.python.org/3/library/tkinter.html) (Python Standard Library)
*   **Data Access:** [`fastf1`](https://docs.fastf1.dev/)
*   **Data Manipulation:** [`Pandas`](https://pandas.pydata.org/), [`NumPy`](https://numpy.org/)
*   **Data Visualization:** [`Matplotlib`](https://matplotlib.org/), [`Seaborn`](https://seaborn.pydata.org/)

---

## 🚀 Getting Started

Follow these steps to set up and run the application locally.

### Prerequisites

*   [Python 3.9+](https://www.python.org/downloads/)
*   [Git](https://git-scm.com/)

### Installation

1.  **Clone the repository:**
    ```sh
    git clone https://github.com/aciluca/f1-ml-project.git
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

The project is organized as an installable Python package to ensure modularity and clean code.

```
f1-ml-project/
│
├── f1_analyzer/ # The main application source package
│ ├── init.py
│ ├── main.py # The application's entry point
│ ├── app.py # GUI logic (the "parent")
│ ├── config.py # Shared constants and configurations
│ └── modules/ # Specialized analysis modules (the "children")
│ ├── init.py
│ └── box_plot.py
│
├── cache/ # Cached data from fastf1 (ignored by Git)
├── venv/ # Virtual environment (ignored by Git)
├── .gitignore
├── README.md # This file
└── requirements.txt # List of Python dependencies
```

---

## 📈 Usage

To launch the application, make sure your virtual environment is active, navigate to the project's root directory (`f1-ml-project`), and run the following command:

```sh
python -m f1_analyzer
```

The -m flag tells Python to run the f1_analyzer package as an application, which automatically executes the __main__.py file.

Once the application is running:
1. Select the desired year, event, and session using the dropdown menus.
2. Click the "Generate Box Plot" button.
3. Wait for the data to load and the plot to be generated, which will appear directly in the main window.
---

## 📄 License

This project is released under the MIT License. See the `LICENSE` file for more details.



## ✍️ Author

**[Luca Acerbi]** - [aciluca](https://github.com/aciluca)


