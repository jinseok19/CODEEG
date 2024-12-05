import os
import threading
from typing import List

from PIL import Image
import numpy as np
from pathlib import Path

def recommend_combination(
    avg_evoked_list: List[np.ndarray], 
    times_list: List[np.ndarray], 
    channels: List[str], 
    image_folder: str, 
    clothes_type: str,
    mode: str = "all"
) -> List[str]:
    
    result_dir = 'static/images/result'
    max_values_per_channel = []
    # 각 채널에 대해
    for channel_idx in range(len(channels)):
        max_values = []
        # 각 이미지에 대해
        for num_images in range(len(times_list)):
            # 0.1초~0.5초 사이의 시간 인덱스 추출
            selected_indices = [
                index for index, value in enumerate(times_list[num_images]) if 0.1 <= value <= 0.5
            ]
            start_index = selected_indices[0]
            end_index = selected_indices[-1]

            # 최대값 추출하여 리스트에 추가
            max_value = max(avg_evoked_list[num_images][channel_idx][start_index: end_index + 1])
            max_values.append(max_value)
        max_values_per_channel.append(max_values)

    # 각 채널의 최대값 상위 5개 인덱스 추출
    indices_of_largest_values_per_channel = []
    for channel in range(len(max_values_per_channel)):
        indices_of_largest_values = sorted(
            range(len(max_values_per_channel[channel])),
            key=lambda i: max_values_per_channel[channel][i],
            reverse=True,
        )[:5]
        largest_values = [max_values_per_channel[channel][i] for i in indices_of_largest_values]
        top_values_and_indices = [
            (value, index) for value, index in zip(largest_values, indices_of_largest_values)
        ]
        indices_of_largest_values_per_channel.append(top_values_and_indices)

    # 내림차순 정렬
    top_values_and_indices = sum(indices_of_largest_values_per_channel, [])
    sorted_top_values_and_indices = sorted(
        top_values_and_indices, key=lambda i: i[0], reverse=True
    )

    # 중복되지 않는 상위 5개 인덱스 결정
    seen_indices = set()
    top_indices = []
    for _, index in sorted_top_values_and_indices:
        if index not in seen_indices:
            top_indices.append(index)
            seen_indices.add(index)
        if len(top_indices) == 5:
            break

    save_dir = Path(result_dir) / clothes_type
    save_dir.mkdir(parents=True, exist_ok=True)

    # 폴더 비우기
    for file in save_dir.iterdir():
        if file.is_file():
            file.unlink()

    recommended_images = []

    # 옷 종류에 따라 이미지 출력
    if clothes_type == "bottoms":
        for index in top_indices:
            print(f"당신이 끌리는 하의 조합은 {index + 1}번 하의입니다.")
            image_filename = f"{image_folder}/B{index + 1}.jpg"
            bottom_image = Image.open(image_filename)
            save_path = save_dir / f"B{index+1}.jpg"
            try:
                # RGBA 모드를 RGB로 변환
                if bottom_image.mode == 'RGBA':
                    bottom_image = bottom_image.convert('RGB')
                # 이미지 저장
                bottom_image.save(save_path)
                print(f"조합 이미지 저장 완료: {save_path}")
                recommended_images.append(str(save_path))
            except Exception as e:
                print(f"Error: 조합 이미지를 생성하는 중 문제가 발생했습니다: {e}")
    
    elif clothes_type == "tops":
        for index in top_indices:
            print(f"당신이 끌리는 상의 조합은 {index + 1}번 상의입니다.")
            image_filename = f"{image_folder}/T{index + 1}.jpg"
            image = Image.open(image_filename)
            save_path = save_dir / f"T{index+1}.jpg"
            image.save(save_path)  # 이미지 저장
            recommended_images.append(str(save_path))  # 이미지 표시
    else:
        raise ValueError("Invalid clothes type")
    return recommended_images
