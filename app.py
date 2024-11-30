from flask import Flask, render_template, request, redirect, url_for, session
import os
import threading
from erp_combination import erp_combination

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/step1')
def step1():
    return render_template('step1.html')

@app.route('/step2')
def step2():
    return render_template('step2.html')

@app.route('/report')
def report():
    recommended_images = session.get('recommended_images', [])
    relative_paths = [os.path.relpath(path, 'static') for path in recommended_images]
    return render_template('report.html', recommended_images=relative_paths)

def run_erp_combination_async(*args, **kwargs):
    result = erp_combination(*args, **kwargs)
    if result and len(result) == 2:
        _, recommended_images = result
        session['recommended_images'] = recommended_images

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

if __name__ == '__main__':
    app.run(debug=True)
