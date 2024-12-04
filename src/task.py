import datetime
import time
import csv
import pygame
import os
import atexit
from src.preprocess import resize_images_in_folder

# Relative paths for images
tops_init_path = './images/tops_init'
tops_resized_path = './images/tops'
bottoms_init_path = './images/bottoms_init'
bottoms_resized_path = './images/bottoms'

# Create directories if they don't exist
for path in [tops_init_path, tops_resized_path, bottoms_init_path, bottoms_resized_path]:
    if not os.path.exists(path):
        os.makedirs(path)


def combination_task(
    screen_width: int,
    screen_height: int,
    isi: int,
    top_image_path: str,
    image_folder: str,
    num_trials: int,
    num_images: int,
    event_save_path: str,
    clothes_type: str,
) -> str:
    
    resize_images_in_folder(tops_init_path, tops_resized_path)
    resize_images_in_folder(bottoms_init_path, bottoms_resized_path)
    
    # Pygame 초기화 및 종료 보장
    pygame.init()
    atexit.register(pygame.quit)
    
    print(screen_height)
    print(screen_width)
    
    # 화면 설정
    screen = pygame.display.set_mode((screen_width, screen_height))
    current_time = datetime.datetime.now()
    hour = str(current_time).split(" ")[1].split(":")[0]
    min = str(current_time).split(" ")[1].split(":")[1]
    sec = str(current_time).split(" ")[1].split(":")[2]

    filename = f"{event_save_path}/combination_event_{hour}.{min}.{sec}.csv"
    
    # CSV 파일 생성 및 헤더 작성
    with open(filename, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["ISI", "RT", "Response", "Stimulus"])

        # 이미지 미리 로드
        top_image = pygame.image.load(top_image_path)
        task_images = []
        for num_image in range(num_images):
            image_path = os.path.join(
                image_folder,
                f"{clothes_type[0].upper()}{num_image + 1}.jpg",  # B, S, T로 시작
            )
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