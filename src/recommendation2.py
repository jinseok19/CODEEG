import threading
from typing import List, Tuple
import numpy as np
from pathlib import Path
import shutil
from PIL import Image

def recommend_combination2(
    avg_evoked_list: List[np.ndarray], 
    times_list: List[np.ndarray], 
    channels: List[str], 
) -> List[Tuple[str, str]]:
    
    result_dir = 'static/images/result'
    max_values_per_channel = []
    
    # 각 채널에 대해
    for channel_idx in range(len(channels)):
        max_values = []
        # 각 조합에 대해 (9개의 조합)
        for num_combination in range(len(times_list)):
            # 0.1초~0.5초 사이의 시간 인덱스 추출
            selected_indices = [
                index for index, value in enumerate(times_list[num_combination]) 
                if 0.1 <= value <= 0.5
            ]
            start_index = selected_indices[0]
            end_index = selected_indices[-1]

            # 최대값 추출하여 리스트에 추가
            max_value = max(avg_evoked_list[num_combination][channel_idx][start_index:end_index + 1])
            max_values.append(max_value)
        max_values_per_channel.append(max_values)

    # 각 채널의 최대값 상위 3개 인덱스 추출
    indices_of_largest_values_per_channel = []
    for channel in range(len(max_values_per_channel)):
        indices_of_largest_values = sorted(
            range(len(max_values_per_channel[channel])),
            key=lambda i: max_values_per_channel[channel][i],
            reverse=True,
        )[:3]
        largest_values = [max_values_per_channel[channel][i] for i in indices_of_largest_values]
        top_values_and_indices = [
            (value, index) for value, index in zip(largest_values, indices_of_largest_values)
        ]
        indices_of_largest_values_per_channel.append(top_values_and_indices)

    # 상위 3개 값을 기준으로 최종 인덱스 결정
    top_values_and_indices = sum(indices_of_largest_values_per_channel, [])
    sorted_top_values_and_indices = sorted(
        top_values_and_indices, key=lambda i: i[0], reverse=True
    )

    # 중복되지 않는 상위 3개 인덱스 결정
    seen_indices = set()
    top_indices = []
    for _, index in sorted_top_values_and_indices:
        if index not in seen_indices:
            top_indices.append(index)
            seen_indices.add(index)
        if len(top_indices) == 3:
            break

    # 결과 디렉토리 생성
    tops_dir = Path(result_dir) / 'tops'
    bottoms_dir = Path(result_dir) / 'bottoms'
    tops_dir.mkdir(parents=True, exist_ok=True)
    bottoms_dir.mkdir(parents=True, exist_ok=True)

    recommended_combinations = []
    for index in top_indices:
        # 인덱스를 상의와 하의 번호로 변환
        top_num = (index // 3) + 1
        bottom_num = (index % 3) + 1
        
        # 원본 이미지 경로
        original_top_path = f"static/images/tops/T{top_num}.jpg"
        original_bottom_path = f"static/images/bottoms/B{bottom_num}.jpg"
        
        # 결과 이미지 경로
        result_top_path = str(tops_dir / f"T{top_num}.jpg")
        result_bottom_path = str(bottoms_dir / f"B{bottom_num}.jpg")
        
        # 이미지 복사
        shutil.copy2(original_top_path, result_top_path)
        shutil.copy2(original_bottom_path, result_bottom_path)
        
        recommended_combinations.append((result_top_path, result_bottom_path))
        print(f"추천하는 조합은 {top_num}번 상의와 {bottom_num}번 하의입니다.")
        print(f"상의 이미지가 {result_top_path}에 저장되었습니다.")
        print(f"하의 이미지가 {result_bottom_path}에 저장되었습니다.")

    # 상의/하의 경로 쌍의 리스트를 반환
    return recommended_combinations 