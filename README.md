# CODDEG
#### Neuro Engineering Project

## A Service that EEG-based ERP analysis to recommend personalized fashion coordination and virtually apply the outfits to user images. 
This BCI project leverages EEG measurements to analyze ERP signals, identifying user preferences. </br>
Based on these insights, it recommends omnivore-inspired fashion coordination, combining tops and bottoms, and virtually applies the selected outfits to user images using advanced AI.

---
#### Requirements

To install the necessary packages, run:
```bash
# clone project
git clone https://github.com/jinseok19/CODEEG.git
cd codeeg

# [OPTIONAL] create conda environment
conda create -n myenv python=3.7
conda activate codeeg

# install requirements
pip install -r requirements.txt
```

#### Run

To start the application, execute:
```bash
python app.py
```

---
### Process

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
#### Non-Commercial use only!
This is the current best-in-class virtual try-on model, created by the Korea Advanced Institute of Science & Technology (KAIST). It’s capable of virtual try-on “in the wild” which has notoriously been difficult for generative models to tackle, until now!

IDM-VTON : Improving Diffusion Models for Authentic Virtual Try-on in the Wild
This is an official implementation of paper ‘Improving Diffusion Models for Authentic Virtual Try-on in the Wild’

![image](https://github.com/user-attachments/assets/49c32793-3ed3-46fb-bb45-16f772af79c9)

![teaser2](https://github.com/user-attachments/assets/80695dc8-fc54-4e90-a4e5-ff3b2533563b)

---

## **1. Core Features**

### **Web Application (`app.py`)**
- **Purpose:** The main Flask web application for the project.
- **Key Features:**
  - Handles routing (`/step1`, `/step2`, `/step3`).
  - Manages image uploads and user sessions.
  - Facilitates virtual try-on functionality by invoking `dress_up.py`.
  - Supports asynchronous task handling and result rendering.

---

### **Recommendation Workflow**
#### **Top and Bottom Recommendation (`task.py`)**
- **Objective:** Recommends the **Top 5** images for tops and bottoms based on EEG data.
- **Workflow:**
  1. **Image Preprocessing:** Resizes images for tops and bottoms.
  2. **ERP Analysis:** Uses `erp_combination.py` to extract P300 peaks from EEG data.
  3. **Recommendation:** Invokes `recommendation.py` to extract **Top 5** images based on P300 peaks.
  4. **Storage:** Saves recommended images in a specified directory.

#### **Top-Bottom Combination Recommendation (`task2.py`)**
- **Objective:** Recommends the **Top 3** top-bottom combinations based on EEG data.
- **Workflow:**
  1. Uses `task.py` to extract **Top 5** images for both tops and bottoms.
  2. **Combination Generation:** Creates 25 top-bottom combination images and resizes them.
  3. **ERP Analysis:** Uses `erp_combination2.py` to analyze EEG data for combination images.
  4. **Recommendation:** Invokes `recommendation2.py` to select the **Top 3** combinations based on P300 peaks.
  5. **Storage:** Saves the selected combinations, including their corresponding top and bottom images, in a specified directory.

---

### **EEG Data Processing**
#### **ERP Analysis**

![image](https://github.com/user-attachments/assets/23737f6c-4b88-4a1f-86df-0cfade3bae7d)

- `erp_combination.py` and `erp_combination2.py` analyze EEG data to detect P300 peaks, which indicate user preferences.

#### **Recommendation**

![image](https://github.com/user-attachments/assets/2a6b7eb1-745b-43d5-8753-a26095230533)

- `recommendation.py`: Recommends **Top 5** images for tops and bottoms.
- `recommendation2.py`: Recommends **Top 3** top-bottom combinations.

---

### **Image Processing**
#### **Image Resize & Combination**

![image](https://github.com/user-attachments/assets/e0d5c2f8-d150-4c6e-9363-539294df6979)

- `task.py`: Resizes top and bottom images.
- `task2.py`: Creates and resizes top-bottom combination images.

#### **Virtual Try-On**

![image](https://github.com/user-attachments/assets/68c09e79-6f46-4348-98e1-fa61cafd65b5)

- `dress_up.py`:
  - Generates virtual try-on images for tops and bottoms using the Replicate API.
  - Saves the results in specified directories.

---

## **2. Supporting Utilities**

### **Preprocessing (`preprocess.py`)**

![image](https://github.com/user-attachments/assets/44edb9f4-2690-4a2b-b4a4-c53bba2dcbe7)

- Processes EEG data:
  - Includes filtering, normalization, and epoch extraction.
- Handles image preprocessing:
  - Resizes and combines images within specified directories.

### **Signal Filtering (`iir.py`)**

![image](https://github.com/user-attachments/assets/912498c6-0d1c-4688-b8e3-a9d285368a15)

- Applies Butterworth filters (bandpass, lowpass, highpass) to EEG signals for noise reduction.


### **Data Analysis (`analysis.py`)**

![image](https://github.com/user-attachments/assets/922c8c16-e1da-45b7-89ca-3468996f30dc)

- Provides tools for ERP analysis.
- Supports data preprocessing and synchronization.

### **Visualization (`plot.py`)**

![image](https://github.com/user-attachments/assets/dceb1295-166b-4ccf-a396-6f60930f7599)

- Visualizes EEG data and frequency analysis results.
- Key Functions:
  - `PlotEEG`: Visualizes EEG channel data.

---

## **3. Directory Structure**

- **`static/uploads`**: Temporarily stores uploaded images.
- **`static/images/result`**: Stores processed results (tops, bottoms, combinations).
- **`templates`**: Contains HTML templates for the Flask web application.

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
│       └── result # recommended images results (top garments, bottom garments, combinations)
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

---

## **4. Key Modules**

### **Task Modules**
- `task.py`: Selects the top 5 recommended images for tops and bottoms.
- `task2.py`: Selects the top 3 recommended top-bottom combinations.

### **ERP-Based Recommendation**
- `erp_combination.py`: Analyzes user preferences for tops and bottoms.
- `erp_combination2.py`: Analyzes user preferences for top-bottom combinations.

### **Virtual Try-On**
- `dress_up.py`: Generates virtual try-on images.

---

## **5. Workflow Summary**

1. The user uploads their image.
2. EEG data and images are used to recommend tops and bottoms (`task.py`).
3. Top-bottom combination images are generated and final recommendations are made (`task2.py`).
4. Virtual try-on images are generated (`dress_up.py`).
5. Results are displayed via the web application.

---