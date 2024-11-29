from flask import Flask, render_template, request, redirect, url_for
import os
import threading
from erp_combination import erp_combination

app = Flask(__name__)

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
    return render_template('report.html')



def run_erp_combination_async(*args, **kwargs):
    threading.Thread(target=erp_combination, args=args, kwargs=kwargs, daemon=True).start()



@app.route('/run_erp_combination_top', methods=['POST'])
def run_erp_combination_top():
    # 비동기적으로 ERP 조합 실행
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
    # 비동기적으로 ERP 조합 실행
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


from flask import Flask, request
import threading

@app.route('/run_erp_combination', methods=['POST'])
def run_erp_combination():
    threading.Thread(
        target=erp_combination,
        kwargs={
            "screen_width": 1920,
            "screen_height": 1080,
            "fs": 256,
            "channels": ['EEG_Fp1', 'EEG_Fp2'],
            "isi": 1000,
            "image_folder": "./images",  # 수정
            "clothes_type": "tops",  # 수정
            "num_trials": 10,
            "num_images": 5,
            "event_save_path": "./event",
            "result_dir": "./result",
            "lowcut": 1.0,
            "highcut": 30.0,
            "tmin": -0.2,
            "tmax": 1.0,
            "mode": "all",
        }
    ).start()
    return "ERP Combination Task Started!", 200


if __name__ == '__main__':
    app.run(debug=True)
