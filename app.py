from flask import Flask, render_template, request, redirect, url_for, session, flash
import os
import threading
from erp_combination import erp_combination
from src.task2 import combination_display_task
from erp_combination2 import erp_combination2
from PIL import Image
import hashlib

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Add a custom filter for zip
@app.template_filter('zip')
def zip_filter(a, b, c):
    return zip(a, b, c)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/step1')
def step1():
    return render_template('step1.html')

@app.route('/step2')
def step2():
    return render_template('step2.html')

@app.route('/step3')
def step3():
    return render_template('step3.html')

@app.route('/report')
def report():
    all_images = {
        f'best_{i}': {'top': [], 'bottom': [], 'combination': []}
        for i in range(1, 6)
    }

    # Dictionary to store image hashes to prevent duplicates
    image_hashes = {'top': {}, 'bottom': {}}
    unique_images = {'top': [], 'bottom': []}

    def get_image_hash(image_path):
        try:
            full_path = os.path.join('static', image_path)
            with Image.open(full_path) as img:
                # Convert image to grayscale and resize to small size for comparison
                img = img.convert('L').resize((8, 8), Image.Resampling.LANCZOS)
                pixels = list(img.getdata())
                avg = sum(pixels) / len(pixels)
                # Create binary hash
                bits = ''.join(['1' if pixel > avg else '0' for pixel in pixels])
                return hashlib.md5(bits.encode()).hexdigest()
        except Exception as e:
            print(f"Error processing image {image_path}: {e}")
            return None

    base_folder = os.path.join('static', 'images', 'result', 'combination')

    # Process each best folder (best_1 to best_5)
    for i in range(1, 6):
        best_folder = os.path.join(base_folder, f'best_{i}')
        
        if os.path.exists(best_folder):
            for filename in sorted(os.listdir(best_folder)):
                relative_path = f'images/result/combination/best_{i}/{filename}'
                
                if filename.startswith('T') and filename.endswith('.jpg'):
                    all_images[f'best_{i}']['top'].append(relative_path)
                    # Check for duplicates using image hash
                    img_hash = get_image_hash(relative_path)
                    if img_hash and img_hash not in image_hashes['top']:
                        image_hashes['top'][img_hash] = relative_path
                        unique_images['top'].append(relative_path)
                        
                elif filename.startswith('B') and filename.endswith('.jpg'):
                    all_images[f'best_{i}']['bottom'].append(relative_path)
                    # Check for duplicates using image hash
                    img_hash = get_image_hash(relative_path)
                    if img_hash and img_hash not in image_hashes['bottom']:
                        image_hashes['bottom'][img_hash] = relative_path
                        unique_images['bottom'].append(relative_path)
                        
                elif filename.startswith('combination_') and filename.endswith('.jpg'):
                    all_images[f'best_{i}']['combination'].append(relative_path)

    # 선택된 옷 이미지 정보 생성 (실제 중복 제거된 이미지만 포함)
    selected_clothes = []
    
    # 중복 제거된 상의 이미지 추가
    for top_img in unique_images['top']:
        selected_clothes.append({
            'path': top_img,
            'description': 'Top'
        })
    
    # 중복 제거된 하의 이미지 추가
    for bottom_img in unique_images['bottom']:
        selected_clothes.append({
            'path': bottom_img,
            'description': 'Bottom'
        })

    return render_template('report.html', all_images=all_images, selected_clothes=selected_clothes)

def run_erp_combination_async(*args, **kwargs):
    result = erp_combination(*args, **kwargs)
    if result and len(result) == 2:
        _, recommended_images = result
        session['recommended_images'] = recommended_images

def ensure_directory_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Created directory: {directory}")

def run_erp_combination2_async(*args, **kwargs):
    try:
        result = erp_combination2(**kwargs)
        if result and len(result) == 2:
            _, recommended_combinations = result
            session['recommended_combinations'] = recommended_combinations
    except Exception as e:
        print(f"Error in ERP combination 2: {e}")
        session['error'] = str(e)

@app.route('/run_erp_combination_top', methods=['POST'])
def run_erp_combination_top():
    run_erp_combination_async(
        screen_width=1920,
        screen_height=1080,
        fs=256,
        channels=['EEG_Fp1', 'EEG_Fp2'],
        isi=1000,
        top_image_path='./images/backgrounds/B0.jpg',
        clothes_type='tops',
        image_folder='./images/tops',
        num_trials=1,
        num_images=30,
        event_save_path='./event',
        result_dir='./plot/tops/0',
        lowcut=1.0,
        highcut=30.0,
        tmin=-0.2,
        tmax=1.0,
        mode='all'
    )
    return redirect(url_for('step1'))

@app.route('/run_erp_combination_bottom', methods=['POST'])
def run_erp_combination_bottom():
    run_erp_combination_async(
        screen_width=1920,
        screen_height=1080,
        fs=256,
        channels=['EEG_Fp1', 'EEG_Fp2'],
        isi=1000,
        top_image_path='./images/backgrounds/B0.jpg',
        clothes_type='bottoms',
        image_folder='./images/bottoms',
        num_trials=1,
        num_images=30,
        event_save_path='./event',
        result_dir='./plot/bottoms/0',
        lowcut=1.0,
        highcut=30.0,
        tmin=-0.2,
        tmax=1.0,
        mode='all'
    )
    return redirect(url_for('step1'))

@app.route('/run_erp_combination', methods=['POST'])
def run_erp_combination():
    run_erp_combination_async(
        screen_width=1920,
        screen_height=1080,
        fs=256,
        channels=['EEG_Fp1', 'EEG_Fp2'],
        isi=1000,
        top_image_path='./result/bottoms',
        clothes_type='tops',
        image_folder='./result/tops',
        num_trials=1,
        num_images=30,
        event_save_path='./event',
        result_dir='./plot/tops/0',
        lowcut=1.0,
        highcut=30.0,
        tmin=-0.2,
        tmax=1.0,
        mode='all'
    )
    return redirect(url_for('step2'))

@app.route('/run_combination_display', methods=['POST'])
def run_combination_display():
    run_erp_combination2_async(
        screen_width=1920,
        screen_height=1080,
        fs=256,
        channels=['EEG_Fp1', 'EEG_Fp2'],
        isi=1000,
        event_save_path='./event',
        result_dir='./plot/combination/0',
        lowcut=1.0,
        highcut=30.0,
        tmin=-0.2,
        tmax=1.0,
        mode='all'
    )
    return redirect(url_for('step3'))

if __name__ == '__main__':
    app.run(debug=True)
