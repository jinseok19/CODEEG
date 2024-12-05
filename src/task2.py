import datetime
import time
import csv
import pygame
import os
import atexit
from pathlib import Path

import random

from src.preprocess import resize_images_in_folder, combine_images

# Relative paths for images
tops_chosen_path = './static/images/result/tops'
bottoms_chosen_path = './static/images/result/bottoms'
combination_path = './images/chosen_combinations_init'
combination_resized_path = './images/chosen_combinations'

# Create directories if they don't exist
for path in [tops_chosen_path, bottoms_chosen_path, combination_path, combination_resized_path]:
    if not os.path.exists(path):
        os.makedirs(path)

def combination_task2(
    screen_width: int,
    screen_height: int,
    isi: int,
    event_save_path: str,
    background_path: str,
    image_folder: str,
    num_trials: int,
    num_images: int
) -> str:
    
    combine_images(tops_chosen_path, bottoms_chosen_path, combination_path)
    resize_images_in_folder(combination_path, combination_resized_path)

    # Pygame 초기화 및 종료 보장
    pygame.init()
    atexit.register(pygame.quit)

    # 화면 설정
    screen = pygame.display.set_mode((screen_width, screen_height))

    # 현재 시간으로 파일 이름 생성
    current_time = datetime.datetime.now()
    hour = str(current_time).split(" ")[1].split(":")[0]
    min = str(current_time).split(" ")[1].split(":")[1]
    sec = str(current_time).split(" ")[1].split(":")[2]
    filename = os.path.join(event_save_path, f"combination_display_event_{hour}.{min}.{sec}.csv")

# CSV 파일 생성 및 헤더 작성
    with open(filename, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["ISI", "RT", "Response", "Stimulus"])

        # 이미지 미리 로드
        top_image = pygame.image.load(background_path)
        task_images = []
        '''
        for num_image in range(num_images):
            image_path = os.path.join(
                image_folder,
                f"combination_{num_image}.jpg"
            )
            task_images.append(pygame.image.load(image_path))
        '''
        valid_extensions = ('.jpg', '.jpeg', '.png', '.bmp')

        # 폴더 내 모든 파일을 순차적으로 확인
        for image_name in os.listdir(combination_resized_path):
            # 이미지 파일인지 확인
            if image_name.lower().endswith(valid_extensions):
                image_path = os.path.join(combination_resized_path, image_name)
                task_images.append(pygame.image.load(image_path))

        # 실험 시작
        for _ in range(num_trials):
            for num_image, task_image in enumerate(task_images):
                # 화면에 상단 이미지 표시
                screen.fill((0, 0, 0))  # 배경색 초기화
                screen.blit(
                    top_image,
                    (
                        screen_width // 2 - top_image.get_width() // 2,
                        screen_height // 2 - top_image.get_height() // 2,
                    ),
                )
                pygame.display.flip()
                time.sleep(isi / 1000.0)  # ISI 대기

                # 반응 시간 측정 시작
                start_time = pygame.time.get_ticks()

                # 화면에 작업 이미지 표시
                screen.fill((0, 0, 0))
                screen.blit(
                    task_image,
                    (
                        screen_width // 2 - task_image.get_width() // 2,
                        screen_height // 2 - task_image.get_height() // 2,
                    ),
                )
                pygame.display.flip()

                # 반응 기록
                response = "CR"
                running = True
                while running:
                    for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_RETURN:
                                response = "HIT"
                                running = False
                        elif event.type == pygame.QUIT:
                            pygame.quit()
                            exit()

                    # 반응 시간을 제한 (예: 1초)
                    if pygame.time.get_ticks() - start_time > 1000:
                        running = False

                end_time = pygame.time.get_ticks()
                rt = end_time - start_time if response == "HIT" else 1000

                # 결과를 CSV에 기록
                writer.writerow([isi, rt, response, num_image + 1])

    # 실험 종료 대기 및 Pygame 종료
    time.sleep(10)
    pygame.quit()
    return filename
'''
    # 선택된 조합 이미지를 저장
    for idx, (rt, response, top_num, bottom_num, top_idx, bottom_idx) in enumerate(sorted_data):
        top_image = top_images[top_idx]
        bottom_image = bottom_images[bottom_idx]

        # 상의 및 하의 원본 경로
        top_path = top_image_paths[top_idx]
        bottom_path = bottom_image_paths[bottom_idx]

        # 조합된 이미지 생성
        combined_image = pygame.Surface((screen_width // 2, screen_height // 2))
        scaled_top = pygame.transform.scale(top_image, (screen_width // 2, screen_height // 4))
        scaled_bottom = pygame.transform.scale(bottom_image, (screen_width // 2, screen_height // 4))
        combined_image.blit(scaled_top, (0, 0))
        combined_image.blit(scaled_bottom, (0, screen_height // 4))

        # Create a directory for each best combination
        best_dir = combination_dir / f"best_{idx + 1}"
        best_dir.mkdir(parents=True, exist_ok=True)

        # Save combined image
        combined_image_path = best_dir / f"combination_{top_num}_{bottom_num}.jpg"
        pygame.image.save(combined_image, str(combined_image_path))

        # Copy individual top and bottom images
        top_image_path = best_dir / f"{top_num}.jpg"
        pygame.image.save(top_image, str(top_image_path))
        bottom_image_path = best_dir / f"{bottom_num}.jpg"
        pygame.image.save(bottom_image, str(bottom_image_path))

        print(f"저장된 상하의 조합 이미지: {combined_image_path}")
        print(f"저장된 상의 이미지: {top_image_path}")
        print(f"저장된 하의 이미지: {bottom_image_path}")

    # Pygame 종료
    pygame.quit()
    return filename
'''

'''
def combination_task2(
    screen_width: int,
    screen_height: int,
    isi: int,
    event_save_path: str,
) -> str:
    
    combine_images(tops_chosen_path, bottoms_chosen_path, combination_path)
    resize_images_in_folder(combination_path, combination_resized_path)

    # Pygame 초기화 및 종료 보장
    pygame.init()
    atexit.register(pygame.quit)

    # 화면 설정
    screen = pygame.display.set_mode((screen_width, screen_height))

    # 현재 시간으로 파일 이름 생성
    current_time = datetime.datetime.now()
    timestamp = current_time.strftime("%H.%M.%S")
    filename = os.path.join(event_save_path, f"combination_display_event_{timestamp}.csv")

    # 결과 이미지 경로 설정
    result_dir = Path('static/images/result')
    combination_dir = result_dir / 'combination'
    combination_dir.mkdir(parents=True, exist_ok=True)  # 디렉토리 생성

    # 상의와 하의 이미지 디렉토리 경로 설정
    tops_dir = result_dir / 'tops'
    bottoms_dir = result_dir / 'bottoms'

    # 이미지 로드
    top_images = []
    bottom_images = []
    top_image_paths = []
    bottom_image_paths = []

    # 상의 이미지 로드 (최대 5개)
    for top_file in sorted(tops_dir.glob('T*.jpg'))[:5]:
        top_images.append(pygame.image.load(str(top_file)))
        top_image_paths.append(top_file)  # 원본 경로 저장

    # 하의 이미지 로드 (최대 5개)
    for bottom_file in sorted(bottoms_dir.glob('B*.jpg'))[:5]:
        bottom_images.append(pygame.image.load(str(bottom_file)))
        bottom_image_paths.append(bottom_file)  # 원본 경로 저장

    # 모든 상하의 조합 생성
    combinations = [(t_idx, b_idx) for t_idx in range(len(top_images)) for b_idx in range(len(bottom_images))]

    # 조합 순서를 무작위로 섞기
#    

    # 모든 조합의 반응 데이터를 저장할 리스트
    response_data = []

    # 모든 조합에 대해 실험 진행
    for top_idx, bottom_idx in combinations:
        top_image = top_images[top_idx]
        bottom_image = bottom_images[bottom_idx]

        # 화면 초기화
        screen.fill((0, 0, 0))  # 흰색 배경

        # 이미지 크기 조정 (화면의 1/4 크기로)
        scaled_top = pygame.transform.scale(
            top_image,
            (screen_width // 2, screen_height // 4)
        )
        scaled_bottom = pygame.transform.scale(
            bottom_image,
            (screen_width // 2, screen_height // 4)
        )

        # 이미지 위치 계산 (상의는 위쪽, 하의는 아래쪽)
        top_position = (
            screen_width // 4,
            screen_height // 8
        )
        bottom_position = (
            screen_width // 4,
            screen_height // 2
        )

        # 이미지 표시
        screen.blit(scaled_top, top_position)
        screen.blit(scaled_bottom, bottom_position)
        pygame.display.flip()

        # 반응 시간 측정 시작
        start_time = pygame.time.get_ticks()

        # 반응 기록
        response = "CR"
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        response = "HIT"
                        running = False
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            # 반응 시간을 제한 (예: 1초)
            if pygame.time.get_ticks() - start_time > 1000:
                running = False

        end_time = pygame.time.get_ticks()
        rt = end_time - start_time if response == "HIT" else 1000

        # ISI 대기
        screen.fill((0, 0, 0))  # 검은색 화면
        pygame.display.flip()
        time.sleep(isi / 1000.0)

        # 반응 데이터를 저장
        response_data.append([rt, response, f"T{top_idx + 1}", f"B{bottom_idx + 1}", top_idx, bottom_idx])

    # CSV 파일에 반응 데이터 저장
    with open(filename, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["RT", "Response", "Top_Number", "Bottom_Number", "Top_Index", "Bottom_Index"])
        writer.writerows(response_data)

    # 상위 3개의 조합 선택 (반응 시간 기준)
    sorted_data = sorted(response_data, key=lambda x: x[0])[:5]

    # 선택된 조합 이미지를 저장
    for idx, (rt, response, top_num, bottom_num, top_idx, bottom_idx) in enumerate(sorted_data):
        top_image = top_images[top_idx]
        bottom_image = bottom_images[bottom_idx]

        # 상의 및 하의 원본 경로
        top_path = top_image_paths[top_idx]
        bottom_path = bottom_image_paths[bottom_idx]

        # 조합된 이미지 생성
        combined_image = pygame.Surface((screen_width // 2, screen_height // 2))
        scaled_top = pygame.transform.scale(top_image, (screen_width // 2, screen_height // 4))
        scaled_bottom = pygame.transform.scale(bottom_image, (screen_width // 2, screen_height // 4))
        combined_image.blit(scaled_top, (0, 0))
        combined_image.blit(scaled_bottom, (0, screen_height // 4))

        # Create a directory for each best combination
        best_dir = combination_dir / f"best_{idx + 1}"
        best_dir.mkdir(parents=True, exist_ok=True)

        # Save combined image
        combined_image_path = best_dir / f"combination_{top_num}_{bottom_num}.jpg"
        pygame.image.save(combined_image, str(combined_image_path))

        # Copy individual top and bottom images
        top_image_path = best_dir / f"{top_num}.jpg"
        pygame.image.save(top_image, str(top_image_path))
        bottom_image_path = best_dir / f"{bottom_num}.jpg"
        pygame.image.save(bottom_image, str(bottom_image_path))

        print(f"저장된 상하의 조합 이미지: {combined_image_path}")
        print(f"저장된 상의 이미지: {top_image_path}")
        print(f"저장된 하의 이미지: {bottom_image_path}")

    # Pygame 종료
    pygame.quit()
    return filename
'''