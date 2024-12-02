import os
from typing import List, Optional, Tuple
from datetime import datetime

import pandas as pd

from task2_origin import combination_display_task
from src.analysis import AnalyzeEEG
from src.plot import PlotEEG
from src.recommendation2 import recommend_combination2


def erp_combination2(
    screen_width: int,
    screen_height: int,
    fs: int,
    channels: List[str],
    isi: int,
    event_save_path: str,
    result_dir: str,
    lowcut: float = 1.0,
    highcut: float = 30.0,
    tmin: float = -0.2,
    tmax: float = 1.0,
    mode: str = "all",
    event_file: str = "",
    data_file_path: str = "",
) -> Optional[Tuple[str, List[Tuple[str, str]]]]:
    if not mode=="analysis":
        today = str(datetime.now().date())
        if not os.path.exists(f"./data/{today}"):
            os.makedirs(f"./data/{today}")
        if not os.path.exists(f"./event/{today}"):
            os.makedirs(f"./event/{today}")

        event_file = combination_display_task(
            screen_width=screen_width,
            screen_height=screen_height,
            isi=isi,
            event_save_path=f"{event_save_path}/{today}",
        )

        rawdata_folders = os.listdir("C:/MAVE_RawData")

        text_file_name = f"C:/MAVE_RawData/{rawdata_folders[-1]}/Rawdata.txt"
        data_df = pd.read_csv(text_file_name, delimiter="\t")

        record_start_time = data_df.iloc[0, 0]
        hour = str(record_start_time).split(":")[0]
        min = str(record_start_time).split(":")[1]
        sec = str(record_start_time).split(":")[2].split(".")[0]

        data_df = data_df[channels]
        data_file_path = f"./data/{today}/Rawdata_{hour}.{min}.{sec}.csv"
        data_df.to_csv(data_file_path, index=False)

    if mode=="task":
        return event_file, []  # 빈 리스트 반환으로 수정

    # analysis 모드이거나 all 모드일 때 실행되는 부분
    if not os.path.exists(result_dir):
        os.makedirs(result_dir)

    analyze_eeg = AnalyzeEEG(channels=channels, fs=fs)
    eeg, eeg_times, avg_evoked_list, times_list = analyze_eeg.analyze_erp(
        eeg_filename=data_file_path if data_file_path else f"./data/{today}/Rawdata_{hour}.{min}.{sec}.csv",
        event_filename=event_file if event_file else f"{event_save_path}/{today}/combination_display_event_{hour}.{min}.{sec}.csv",
        result_dir=result_dir,
        num_types=9,  # 3x3 조합이므로 9개의 타입
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
        eeg_filename="eeg_raw_combination",
    )
    plot_eeg.plot_eeg()
    
    # 각 조합에 대한 전극 플롯 생성
    for i in range(9):  # 9개의 조합에 대해
        top_num = (i // 3) + 1  # 상의 번호 (1-3)
        bottom_num = (i % 3) + 1  # 하의 번호 (1-3)
        plot_eeg.plot_electrode(
            avg_evoked_list[i],
            times_list[i],
            filename=f"combination_T{top_num}_B{bottom_num}_electrode",
        )

    # recommendation2 함수를 사용하여 추천 조합 얻기
    recommended_combinations = recommend_combination2(
        avg_evoked_list=avg_evoked_list,
        times_list=times_list,
        channels=channels,
    )

    return event_file, recommended_combinations


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

    parser = argparse.ArgumentParser(
        description="Insert arguments for function of erp combination display"
    )
    parser.add_argument(
        "--screen_width",
        type=int,
        default=1920,
        help="Set screen width of combination display task",
    )
    parser.add_argument(
        "--screen_height",
        type=int,
        default=1080,
        help="Set screen height of combination display task",
    )
    parser.add_argument(
        "--fs", 
        type=int, 
        default=256, 
        help="Get resolution of EEG device"
    )
    parser.add_argument(
        "--channels",
        type=parse_list,
        default="['EEG_Fp1', 'EEG_Fp2']",
        help="Get channels of EEG device",
    )
    parser.add_argument(
        "--isi",
        type=int,
        default=1000,
        help="Set inter-stimulus interval of combination display task",
    )
    parser.add_argument(
        "--event_save_path",
        type=str,
        default="./event",
        help="Set a record of events file saving path",
    )
    parser.add_argument(
        "--result_dir",
        type=str,
        default="./plot",
        help="Set a EEG, ERP plots saving path",
    )
    parser.add_argument(
        "--result_dir_num",
        type=int,
        default=0,
        help="Set a EEG, ERP plots detailed saving path",
    )
    parser.add_argument(
        "--lowcut",
        type=float,
        default=1.0,
        help="Set butter filter lowcut to get ERP",
    )
    parser.add_argument(
        "--highcut",
        type=float,
        default=30.0,
        help="Set butter filter highcut to get ERP",
    )
    parser.add_argument(
        "--tmin",
        type=float,
        default=-0.2,
        help="Set epoch tmin to get ERP",
    )
    parser.add_argument(
        "--tmax",
        type=float,
        default=1.0,
        help="Set epoch tmax to get ERP",
    )
    parser.add_argument(
        "--mode",
        type=str,
        default="analysis",  # mode : analysis, all, task
        help="Set execution mode",
    )
    parser.add_argument(
        "--event_file",
        type=str,
        default="",
        help="Set event file path when mode is analysis",
    )
    parser.add_argument(
        "--data_file_path",
        type=str,
        default="",
        help="Set data file path when mode is analysis",
    )
    args = parser.parse_args()

    erp_combination2(
        screen_width=args.screen_width,
        screen_height=args.screen_height,
        fs=args.fs,
        channels=args.channels,
        isi=args.isi,
        event_save_path=args.event_save_path,
        result_dir=f"{args.result_dir}/combination/{args.result_dir_num}",
        lowcut=args.lowcut,
        highcut=args.highcut,
        tmin=args.tmin,
        tmax=args.tmax,
        mode=args.mode,
        event_file=args.event_file,
        data_file_path=args.data_file_path,
    ) 