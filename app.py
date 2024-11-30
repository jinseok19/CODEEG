from flask import Flask, render_template, request, redirect, url_for, session, flash
import os
import threading
from erp_combination import erp_combination
from src.task2 import combination_display_task
from erp_combination2 import erp_combination2

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
    recommended_combinations = session.get('recommended_combinations', [])
    tops = []
    bottoms = []
    for top_path, bottom_path in recommended_combinations:
        tops.append(os.path.relpath(top_path, 'static'))
        bottoms.append(os.path.relpath(bottom_path, 'static'))
    return render_template('report.html', tops=tops, bottoms=bottoms)

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
    try:
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
        
        if 'error' in session:
            flash(f'오류가 발생했습니다: {session["error"]}')
            session.pop('error', None)
            return redirect(url_for('step2'))
            
        return redirect(url_for('report'))
    except Exception as e:
        print(f"Error during combination display task: {e}")
        flash('테스트 중 오류가 발생했습니다.')
        return redirect(url_for('step2'))

if __name__ == '__main__':
    app.run(debug=True)
