from typing import List

from PIL import Image
import numpy as np
import pandas as pd
from pathlib import Path

def recommend_combination(
    avg_evoked_list: List[np.ndarray], 
    times_list: List[np.ndarray], 
    channels: List[str], 
    image_folder: str, 
    clothes_type: str,
    # result_dir: str,  # 추가: 결과를 저장할 폴더 경로
) -> None:
    result_dir = 'result'
    max_values_per_channel = []
    for channel_idx in range(len(channels)):
        max_values = []
        for num_images in range(len(times_list)):
            selected_indices = [
                index
                for index, value in enumerate(times_list[num_images])
                if 0.1 <= value <= 0.5
            ]
            start_index = selected_indices[0]
            end_index = selected_indices[-1]

            max_value = max(
                avg_evoked_list[num_images][channel_idx][start_index : end_index + 1]
            )
            max_values.append(max_value)
        max_values_per_channel.append(max_values)

    indices_of_largest_values_per_channel = []
    for channel in range(len(max_values_per_channel)):
        indices_of_largest_values = sorted(
            range(len(max_values_per_channel[channel])),
            key=lambda i: max_values_per_channel[channel][i],
            reverse=True,
        )[:3]
        largest_values = [
            max_values_per_channel[channel][i] for i in indices_of_largest_values
        ]
        top_values_and_indices = [
            (value, index)
            for value, index in zip(largest_values, indices_of_largest_values)
        ]
        indices_of_largest_values_per_channel.append(top_values_and_indices)

    top_values_and_indices = sum(indices_of_largest_values_per_channel, [])
    sorted_top_values_and_indices = sorted(
        top_values_and_indices, key=lambda i: i[0], reverse=True
    )
    top_recommendations = []
    seen_indices = set()
    for t in sorted_top_values_and_indices:
        if t[1] not in seen_indices and len(top_recommendations) < 3:
            top_recommendations.append(t)
            seen_indices.add(t[1])
    top_indices = [t[1] + 1 for t in top_recommendations]

    # 이미지 저장 경로 생성
    save_dir = Path(result_dir) / clothes_type
    save_dir.mkdir(parents=True, exist_ok=True)

    if clothes_type == "bottoms":
        for index in top_indices:
            print(f"당신이 끌리는 하의 조합은 {index}번 하의입니다.")
            image_filename = f"{image_folder}/B{index}.jpg"
            image = Image.open(image_filename)

            # 저장할 경로와 파일 이름 설정
            save_path = save_dir / f"bottoms_{index}.jpg"
            image.save(save_path)  # 이미지 저장
            image.show()  # 이미지 표시 (필요 없으면 제거 가능)

    elif clothes_type == "shoes":
        for index in top_indices:
            print(f"당신이 끌리는 신발의 조합은 {index}번 신발입니다.")
            image_filename = f"{image_folder}/S{index}.jpg"
            image = Image.open(image_filename)

            # 저장할 경로와 파일 이름 설정
            save_path = save_dir / f"shoes_{index}.jpg"
            image.save(save_path)  # 이미지 저장
            image.show()  # 이미지 표시 (필요 없으면 제거 가능)

    else:
        raise ValueError("Invalid clothes type")
