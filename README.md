# CODDEG
Neuro Engineering

# Project Structure

```
CODEEG/
├── __pycache__/                 # Compiled Python bytecode cache
├── data/                        # Directory for storing EEG data
├── event/                       # Directory for storing event data
├── images/                      # Repository for original images
├── plot/                        # Directory for storing ERP analysis plots
│   ├── bottoms/                 # Plots related to bottoms
│   ├── combination/             # Plots related to combinations
│   └── tops/                    # Plots related to tops
├── run/                         # Scripts for execution
├── src/                         # Source code directory
│   ├── __pycache__/            # Python cache
│   ├── analysis.py             # EEG analysis module
│   ├── iir.py                  # Signal filtering module
│   ├── plot.py                 # Data visualization module
│   ├── preprocess.py           # Data preprocessing module
│   ├── recommendation.py       # Clothing recommendation algorithm
│   ├── recommendation2.py      # Improved clothing recommendation algorithm
│   ├── task.py                 # Basic experiment task
│   └── task2.py                # Improved experiment task
├── static/                      # Web static files
│   ├── css/                    # Stylesheets
│   ├── data/                   # Data files for web
│   ├── images/                 # Images for web
│   ├── js/                     # JavaScript files
│   └── uploads/                # User-uploaded files
├── templates/                   # HTML templates
│   ├── dress_up.html           # Virtual fitting page
│   ├── index.html              # Main page
│   ├── report.html             # Result report page
│   ├── start_page.html         # Start page
│   ├── step1.html              # Step 1 experiment page
│   ├── step2.html              # Step 2 experiment page
│   └── step3.html              # Step 3 experiment page
├── app.py                       # Flask web application
├── dress_up.py                 # Virtual fitting logic
├── erp_combination.py          # ERP-based clothing combination analysis
├── erp_combination2.py         # Improved clothing combination analysis
└── README.md                   # Project documentation
```
### Project Process

![image](https://github.com/user-attachments/assets/5396f46e-4f08-458b-a27d-1595b3fa6402)


### IDM-VTOM


---

### erp_combination.py

![image](https://github.com/user-attachments/assets/23737f6c-4b88-4a1f-86df-0cfade3bae7d)


This script processes EEG data to analyze and visualize ERP responses, recommending clothing combinations based on the analysis. It supports command-line arguments for flexible configuration and execution.

---
### task.py


This script initializes a Pygame environment to conduct a visual stimulus experiment, resizing images and logging response times to a CSV file. It supports customizable screen dimensions, inter-stimulus intervals, and trial configurations.

--- 
### analysis.py

![image](https://github.com/user-attachments/assets/922c8c16-e1da-45b7-89ca-3468996f30dc)


This module provides EEG analysis tools, including ERP, ERDS, and SSVEP analysis, with preprocessing capabilities such as filtering, normalization, and time synchronization. It supports various scaling methods for frequency domain analysis results.

--- 
### plot.py

![image](https://github.com/user-attachments/assets/dceb1295-166b-4ccf-a396-6f60930f7599)

This code provides functionality to visualize and save EEG data, plotting various EEG channels and average FFT values for selected frequencies. The PlotEEG class generates plots for EEG data, while the plot_ssvep function visualizes average FFT values per frequency from a given DataFrame.

--- 

### recommendation.py

The recommend_combination function analyzes EEG data to recommend clothing combinations by identifying the top evoked responses within a specified time window and saves the corresponding images. It supports both "tops" and "bottoms" clothing types, ensuring the recommended images are stored in a designated directory.

--- 
