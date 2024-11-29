import os
import threading
from datetime import datetime
from typing import List, Optional, Tuple

import pandas as pd
from src.task import combination_task
from src.analysis import AnalyzeEEG
from src.plot import PlotEEG
from src.recommendation import recommend_combination


def erp_combination(
    screen_width: int,
    screen_height: int,
    fs: int,
    channels: List[str],
    isi: int,
    image_folder: str,
    clothes_type: str,
    num_trials: int,
    num_images: int,
    event_save_path: str,
    result_dir: str,
    lowcut: float = 1.0,
    highcut: float = 30.0,
    tmin: float = -0.2,
    tmax: float = 1.0,
    mode: str = "all",
    event_file: str = "",
    data_file_path: str = "",
) -> Optional[Tuple[str, str]]:
    if mode != "analysis":
        today = str(datetime.now().date())
        if not os.path.exists(f"./data/{today}"):
            os.makedirs(f"./data/{today}")
        if not os.path.exists(f"./event/{today}"):
            os.makedirs(f"./event/{today}")

        event_file = combination_task(
            screen_width=1920,
            screen_height=1080,
            isi=1000,
            tops_path=f"{result_dir}/tops",      # 상의 이미지 경로
            bottoms_path=f"{result_dir}/bottoms", # 하의 이미지 경로
            event_save_path="./event",           # 이벤트 저장 경로
        )



        rawdata_folders = os.listdir("C:/MAVE_RawData")
        text_file_name = f"C:/MAVE_RawData/{rawdata_folders[-1]}/Rawdata.txt"
        data_df = pd.read_csv(text_file_name, delimiter="\t")

        record_start_time = data_df.iloc[0, 0]
        hour = str(record_start_time).split(":")[0]
        minute = str(record_start_time).split(":")[1]
        sec = str(record_start_time).split(":")[2].split(".")[0]

        data_df = data_df[channels]
        data_file_path = f"./data/{today}/Rawdata_{hour}.{minute}.{sec}.csv"
        data_df.to_csv(data_file_path, index=False)

    if mode == "task":
        return event_file, data_file_path

    analyze_eeg = AnalyzeEEG(channels=channels, fs=fs)
    eeg, eeg_times, avg_evoked_list, times_list = analyze_eeg.analyze_erp(
        eeg_filename=data_file_path,
        event_filename=event_file,
        result_dir=result_dir,
        num_types=num_images,
        lowcut=lowcut,
        highcut=highcut,
        tmin=tmin,
        tmax=tmax,
    )

    plot_eeg = PlotEEG(
        channels=channels,
        result_dir=result_dir,
        is_show=False,
        is_save=True,
        eeg=eeg,
        eeg_times=eeg_times,
        eeg_filename="eeg_raw",
    )
    plot_eeg.plot_eeg()

    for i in range(num_images):
        plot_eeg.plot_electrode(
            avg_evoked_list[i], times_list[i], filename=f"{clothes_type}_{i+1}_electrode"
        )

    recommend_combination(
        avg_evoked_list=avg_evoked_list,
        times_list=times_list,
        channels=channels,
        image_folder=image_folder,
        clothes_type=clothes_type,
    )


if __name__ == "__main__":
    import argparse
    import ast

    def parse_list(string: str):
        try:
            parsed_list = ast.literal_eval(string)
            if isinstance(parsed_list, list):
                return parsed_list
            else:
                raise argparse.ArgumentTypeError("Invalid list format")
        except (ValueError, SyntaxError):
            raise argparse.ArgumentTypeError("Invalid list format")

    parser = argparse.ArgumentParser(description="Insert arguments for ERP combination function")
    parser.add_argument("--screen_width", type=int, default=1920)
    parser.add_argument("--screen_height", type=int, default=1080)
    parser.add_argument("--fs", type=int, default=256)
    parser.add_argument("--channels", type=parse_list, default="['EEG_Fp1', 'EEG_Fp2']")
    parser.add_argument("--isi", type=int, default=1000)
    parser.add_argument("--image_path", type=str, default="./images")
    parser.add_argument("--clothes_type", type=str, default="tops")
    parser.add_argument("--num_trials", type=int, default=10)
    parser.add_argument("--num_images", type=int, default=5)
    parser.add_argument("--event_save_path", type=str, default="./event")
    parser.add_argument("--result_dir", type=str, default="./result")
    parser.add_argument("--lowcut", type=float, default=1.0)
    parser.add_argument("--highcut", type=float, default=30.0)
    parser.add_argument("--tmin", type=float, default=-0.2)
    parser.add_argument("--tmax", type=float, default=1.0)
    parser.add_argument("--mode", type=str, default="all")
    args = parser.parse_args()

    # 수정된 호출 예시
    erp_combination(
        screen_width=args.screen_width,
        screen_height=args.screen_height,
        fs=args.fs,
        channels=args.channels,
        isi=args.isi,
        image_folder=args.image_path,  # image_path가 image_folder로 전달
        clothes_type=args.clothes_type,
        num_trials=args.num_trials,
        num_images=args.num_images,
        event_save_path=args.event_save_path,
        result_dir=args.result_dir,
        lowcut=args.lowcut,
        highcut=args.highcut,
        tmin=args.tmin,
        tmax=args.tmax,
        mode=args.mode,
    )

