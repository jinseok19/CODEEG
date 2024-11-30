import os
from typing import List, Optional, Tuple
from datetime import datetime
import csv
import pandas as pd

from src.analysis import AnalyzeEEG
from src.plot import PlotEEG
from src.recommendation import recommend_combination


def erp_combination(
    screen_width: int,
    screen_height: int,
    isi: int,
    fs: int,
    channels: List[str],  # channels 추가
    top_image_folder: str,
    bottom_image_folder: str,
    num_tops: int,  # 추가된 부분
    num_bottoms: int,
    event_save_path: str,
    result_dir: str,
    lowcut: float = 1.0,
    highcut: float = 30.0,
    tmin: float = -0.2,
    tmax: float = 1.0,
    mode: str = "all",
) -> Optional[str]:
    """
    ERP Combination Function: Dynamically load and process images from folders.
    """
     # Debugging: print num_tops and num_bottoms values
    print(f"Number of tops: {num_tops}, Number of bottoms: {num_bottoms}")
   
    top_images = sorted([
        os.path.normpath(os.path.join(top_image_folder, file))
        for file in os.listdir(top_image_folder)
        if file.lower().endswith(('.jpg', '.png'))
    ])
    bottom_images = sorted([
        os.path.normpath(os.path.join(bottom_image_folder, file))
        for file in os.listdir(bottom_image_folder)
        if file.lower().endswith(('.jpg', '.png'))
    ])
        
    # Ensure images are found
    if not top_images:
        raise FileNotFoundError(f"No top images found in folder: {top_image_folder}")
    if not bottom_images:
        raise FileNotFoundError(f"No bottom images found in folder: {bottom_image_folder}")

    # Debugging: Print loaded images
    print(f"Top images: {top_images}")
    print(f"Bottom images: {bottom_images}")

    # Prepare event log
    today = datetime.now().strftime('%Y-%m-%d')
    event_save_dir = os.path.join(event_save_path, today)
    os.makedirs(event_save_dir, exist_ok=True)
    event_file = os.path.join(event_save_dir, f"combination_event_{datetime.now().strftime('%H-%M-%S')}.csv")

    # Write the event log
    with open(event_file, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Top Image", "Bottom Image", "ISI", "Reaction_Time", "Response"])

        # Start combination process
        for top_idx, top_image in enumerate(top_images):
            for bottom_idx, bottom_image in enumerate(bottom_images):
                # Simulate displaying images (replace with actual rendering logic)
                print(f"Displaying Top: {top_image}, Bottom: {bottom_image}")

                # Example reaction time and response (replace with actual logic)
                reaction_time = 1000  # Example reaction time
                response = "HIT"     # Example response

                # Log the event
                writer.writerow([os.path.basename(top_image), os.path.basename(bottom_image), isi, reaction_time, response])

    print(f"Event log saved to: {event_file}")
    return event_file


def combination_task(
    screen_width: int,
    screen_height: int,
    isi: int,
    top_image_path: str,
    bottom_image_path: str,
    result_dir: str,
) -> Tuple[float, str]:
    """
    Displays a combination of top and bottom images in a Pygame screen.
    Records reaction time and response.
    """
    import pygame
    # Initialize Pygame
    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("ERP Combination Task")

    # Load images
    top_image = pygame.image.load(top_image_path)
    bottom_image = pygame.image.load(bottom_image_path)

    # Display top image
    screen.fill((0, 0, 0))
    screen.blit(top_image, (screen_width // 2 - top_image.get_width() // 2, 100))
    pygame.display.flip()
    time.sleep(isi / 1000.0)

    # Display bottom image and record reaction
    start_time = pygame.time.get_ticks()
    screen.blit(bottom_image, (screen_width // 2 - bottom_image.get_width() // 2, 400))
    pygame.display.flip()

    reaction_time, response = 0, "MISS"
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                reaction_time = pygame.time.get_ticks() - start_time
                response = "HIT"
                running = False
            elif event.type == pygame.QUIT:
                running = False

    pygame.quit()
    return reaction_time, response


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
        description="Insert arguments for function of erp combination"
    )
    parser.add_argument(
        "--screen_width",
        type=int,
        default=1920,
        help="Set screen width of combination task",
    )
    parser.add_argument(
        "--screen_height",
        type=int,
        default=1080,
        help="Set screen height of combination task",
    )
    parser.add_argument(
        "--fs", type=int, default=256, help="Get resolution of EEG device"
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
        help="Set inter-stimulus interval of combination task",
    )
    parser.add_argument(
        "--top_image_folder",
        type=str,
        default="./images/tops",
        help="Set path to top images",
    )
    parser.add_argument(
        "--bottom_image_folder",
        type=str,
        default="./images/bottoms",
        help="Set path to bottom images",
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
        "--num_tops",
        type=int,
        default=3,
        help="Number of top images to use",
    )
    parser.add_argument(
        "--num_bottoms",
        type=int,
        default=3,
        help="Number of bottom images to use",
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

    erp_combination(
        screen_width=args.screen_width,
        screen_height=args.screen_height,
        fs=args.fs,
        channels=args.channels,
        isi=args.isi,
        top_image_folder=args.top_image_folder,
        bottom_image_folder=args.bottom_image_folder,
        event_save_path=args.event_save_path,
        result_dir=args.result_dir,
        num_tops=args.num_tops,
        num_bottoms=args.num_bottoms,
        lowcut=args.lowcut,
        highcut=args.highcut,
        tmin=args.tmin,
        tmax=args.tmax,
        mode=args.mode,
        event_file=args.event_file,
        data_file_path=args.data_file_path,
    )
