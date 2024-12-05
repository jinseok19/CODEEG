# CODDEG
#### Neuro Engineering

## project start

#### Installation

To install the necessary packages, run:
```bash
pip install flask
pip install replicate
```

#### Run the Application

To start the application, execute:
```bash
python app.py
```
This format uses Markdown to clearly separate sections and provides code blocks for easy copying.

---
### Project Structure

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

![image](https://github.com/user-attachments/assets/f6e7cf17-b79d-45d1-9811-93d1ff4a9daf)

Wearing the MAVE EEG device, we test top and bottom images. Using P300 signals, we select the top and bottom images to create combination images. These results are then processed using the Replicate API with the IDM-VTON model to virtually dress the user image.

#### Steps to Use

##### Step 1: Initial Testing
1. Test the top clothing items.
2. Test the bottom clothing items.

##### Step 2: Combination and Dressing
1. Test the clothing combinations.
2. Proceed with the virtual dressing:
   - 2.1 Upload your full-body image.
   - 2.2 Click the 'Dress Up' button.

##### Step 3: Viewing Results
1. Click the 'View Report' button to see the results.
---

### IDM-VTON
Non-Commercial use only!
This is the current best-in-class virtual try-on model, created by the Korea Advanced Institute of Science & Technology (KAIST). It’s capable of virtual try-on “in the wild” which has notoriously been difficult for generative models to tackle, until now!

IDM-VTON : Improving Diffusion Models for Authentic Virtual Try-on in the Wild
This is an official implementation of paper ‘Improving Diffusion Models for Authentic Virtual Try-on in the Wild’

![image](https://github.com/user-attachments/assets/49c32793-3ed3-46fb-bb45-16f772af79c9)

![teaser2](https://github.com/user-attachments/assets/80695dc8-fc54-4e90-a4e5-ff3b2533563b)

---
# abstract
## Software Module Descriptions

### `app.py`
This module serves as the main entry point for the Flask web application. It handles routing, rendering HTML templates, and managing user sessions. Key functionalities include:
- Initializing the Flask app and setting up configurations.
- Defining routes for different steps of the application (`/step1`, `/step2`, `/step3`).
- Handling image uploads and executing the `dress_up.py` script.
- Rendering reports and managing image processing tasks asynchronously.

### `src/task2.py`
This module is responsible for managing the combination task for images. It includes:
- Functions to combine and resize images.
- A `combination_task2` function that uses Pygame to display images and record user responses.
- Ensures directories for image storage are created and managed properly.

### `src/recommendation2.py`
This module provides functionality for recommending clothing combinations based on EEG data. It includes:
- The `recommend_combination2` function, which processes EEG data to select top clothing combinations.
- Methods to manage and store recommended images in a structured directory format.
- Utilizes image processing to ensure the best combinations are selected and saved.

### `erp_combination.py` and `erp_combination2.py`
These modules (not fully detailed here) are likely responsible for processing EEG data to determine clothing preferences. They are used in conjunction with the main application to provide personalized recommendations.

### `dress_up.py`
This script is executed to apply virtual clothing to user images using the Replicate API. It processes top and bottom clothing images and saves the results in specified directories.

### `static/uploads`
This directory is used to store uploaded images temporarily during the processing phase.

### `static/images/result`
This directory structure is used to store the results of image processing tasks, including top, bottom, and combination images.

### `templates`
Contains HTML templates used by the Flask application to render web pages for different steps and reports.

---

These modules work together to provide a seamless experience for users, from uploading images to receiving personalized clothing recommendations based on EEG data.

--- 
## Detail

### dress_up.py

![image](https://github.com/user-attachments/assets/68c09e79-6f46-4348-98e1-fa61cafd65b5)


The script processes images by using a Replicate client to apply a virtual try-on model to top and bottom clothing images, saving the results in specified output folders. It iterates over predefined directory combinations, finding images by prefix and logging the process.

---

### erp_combination.py

![image](https://github.com/user-attachments/assets/23737f6c-4b88-4a1f-86df-0cfade3bae7d)


This script processes EEG data to analyze and visualize ERP responses, recommending clothing combinations based on the analysis. It supports command-line arguments for flexible configuration and execution.

---
### task.py

![image](https://github.com/user-attachments/assets/e0d5c2f8-d150-4c6e-9363-539294df6979)

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

![image](https://github.com/user-attachments/assets/2a6b7eb1-745b-43d5-8753-a26095230533)

The recommend_combination function analyzes EEG data to recommend clothing combinations by identifying the top evoked responses within a specified time window and saves the corresponding images. It supports both "tops" and "bottoms" clothing types, ensuring the recommended images are stored in a designated directory.

--- 

### preprocess.py

![image](https://github.com/user-attachments/assets/44edb9f4-2690-4a2b-b4a4-c53bba2dcbe7)

PreprocessEEG class processes EEG data through methods for reading, filtering, normalizing, and extracting epochs, while resize_images_in_folder and combine_images functions handle image resizing and combination tasks.

---

### iir.py

![image](https://github.com/user-attachments/assets/912498c6-0d1c-4688-b8e3-a9d285368a15)

The FilterSignal class provides methods to apply bandpass, lowpass, and highpass Butterworth filters to signals, using specified sampling frequency and filter order. It processes input data arrays and returns filtered signals.
