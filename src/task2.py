import datetime
import time
import csv
import pygame
import os
import atexit
from pathlib import Path


def combination_display_task(
    screen_width: int,
    screen_height: int,
    isi: int,
    event_save_path: str,
) -> str:
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

    tops_dir = result_dir / 'tops'
    bottoms_dir = result_dir / 'bottoms'

    # 이미지 로드
    top_images = []
    bottom_images = []
    
    # 상의 이미지 로드 (최대 5개)
    for top_file in sorted(tops_dir.glob('T*.jpg'))[:5]:
        top_images.append(pygame.image.load(str(top_file)))
    
    # 하의 이미지 로드 (최대 5개)
    for bottom_file in sorted(bottoms_dir.glob('B*.jpg'))[:5]:
        bottom_images.append(pygame.image.load(str(bottom_file)))

    # 모든 조합의 반응 데이터를 저장할 리스트
    response_data = []

    # 모든 조합에 대해 실험 진행 (5x5 = 25 조합)
    for top_idx, top_image in enumerate(top_images):
        for bottom_idx, bottom_image in enumerate(bottom_images):
            # 화면 초기화
            screen.fill((255, 255, 255))  # 흰색 배경

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
            response_data.append([rt, response, top_idx + 1, bottom_idx + 1])

    # CSV 파일에 반응 데이터 저장
    with open(filename, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["RT", "Response", "Top_Number", "Bottom_Number"])
        writer.writerows(response_data)

    # 상위 5개의 조합 선택 (반응 시간 기준)
    sorted_data = sorted(response_data, key=lambda x: x[0])[:5]

    # 선택된 조합 이미지를 저장
    for idx, (rt, response, top_num, bottom_num) in enumerate(sorted_data):
        top_image = top_images[top_num - 1]
        bottom_image = bottom_images[bottom_num - 1]

        combined_image = pygame.Surface((screen_width // 2, screen_height // 2))
        scaled_top = pygame.transform.scale(top_image, (screen_width // 2, screen_height // 4))
        scaled_bottom = pygame.transform.scale(bottom_image, (screen_width // 2, screen_height // 4))
        combined_image.blit(scaled_top, (0, 0))
        combined_image.blit(scaled_bottom, (0, screen_height // 4))

        combined_image_path = combination_dir / f"combination_T{top_num}_B{bottom_num}.jpg"
        pygame.image.save(combined_image, str(combined_image_path))
        print(f"저장된 상위하위 조합 이미지: {combined_image_path}")

    # Pygame 종료
    pygame.quit()
    return filename

