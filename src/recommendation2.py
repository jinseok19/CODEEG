import threading
from typing import List, Tuple
import numpy as np
from pathlib import Path
import shutil
from PIL import Image

def clear_directory(directory: Path):
    if directory.exists() and directory.is_dir():
        shutil.rmtree(directory)
    directory.mkdir(parents=True, exist_ok=True)

def recommend_combination2(
    avg_evoked_list: List[np.ndarray], 
    times_list: List[np.ndarray], 
    channels: List[str],
    image_folder: str,
    mode: str = "all"
) -> List[str]:
    print("recommend_combination2 함수 시작")
    
    result_dir = './static/images/result/combination'
    clear_directory(result_dir)
    max_values_per_channel = []

    # 각 채널에 대해
    for channel_idx in range(len(channels)):
        print(f"채널 {channels[channel_idx]} 처리 중...")
        max_values = []
        # 각 조합에 대해 (25개의 조합)
        for num_combination in range(len(times_list)):
            # 0.1초~0.5초 사이의 시간 인덱스 추출
            selected_indices = [
                index for index, value in enumerate(times_list[num_combination]) 
                if 0.1 <= value <= 0.5
            ]
            if not selected_indices:
                print(f"Warning: 시간 범위 0.1~0.5초에 해당하는 데이터가 없습니다. 조합 {num_combination} 건너뜁니다.")
                continue
            
            start_index = selected_indices[0]
            end_index = selected_indices[-1]

            max_value = max(avg_evoked_list[num_combination][channel_idx][start_index:end_index + 1])
            max_values.append(max_value)
        max_values_per_channel.append(max_values)

    print("최대값 계산 완료")
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
    combination_dir = Path(result_dir)
    
    print(f"결과 디렉토리 경로 설정: {combination_dir}")
    combination_dir.mkdir(parents=True, exist_ok=True)
    print(f"결과 디렉토리 생성됨: {combination_dir}")

    '''# 폴더 비우기
    if mode == "all":
        for file in combination_dir.iterdir():
            if file.is_file():
                file.unlink()  # 파일 삭제'''

    for idx in top_indices:
        image_filename = f"combination_{idx}.jpg"
        image = Image.open(image_filename)
        combination_path = str(combination_dir / f"best_{idx}/combination_{idx}.jpg")
        image.save(combination_path)
        print(f"조합 이미지 저장 완료: {combination_path}")
        top_recommendations.append(combination_path)
    
    return top_recommendations

'''
# 각 채널의 최대값 상위 3개 인덱스 추출
indices_of_largest_values_per_channel = []
for channel in range(len(max_values_per_channel)):
    indices_of_largest_values = sorted(
        range(len(max_values_per_channel[channel])),
        key=lambda i: max_values_per_channel[channel][i],
        reverse=True,
    )[:3]
    indices_of_largest_values_per_channel.append(indices_of_largest_values)

print("상위 인덱스 추출 완료")

# 결과 디렉토리 생성
combination_dir = Path(result_dir)
print(f"결과 디렉토리 경로 설정: {combination_dir}")
combination_dir.mkdir(parents=True, exist_ok=True)
print(f"결과 디렉토리 생성됨: {combination_dir}")

recommended_combinations = []

for idx, index in enumerate(indices_of_largest_values_per_channel[0]):
    top_num = (index // 3) + 1
    bottom_num = (index % 3) + 1

    original_top_path = f"static/images/tops/T{top_num}.jpg"
    original_bottom_path = f"static/images/bottoms/B{bottom_num}.jpg"
    combination_path = str(combination_dir / f"combination_{idx + 1}.jpg")

    try:
        if not Path(original_top_path).exists():
            print(f"Error: 상의 이미지 {original_top_path}가 존재하지 않습니다.")
            continue
        if not Path(original_bottom_path).exists():
            print(f"Error: 하의 이미지 {original_bottom_path}가 존재하지 않습니다.")
            continue

        top_image = Image.open(original_top_path)
        bottom_image = Image.open(original_bottom_path)
        combined_image = Image.new(
            "RGB",
            (max(top_image.width, bottom_image.width), top_image.height + bottom_image.height),
        )
        combined_image.paste(top_image, (0, 0))
        combined_image.paste(bottom_image, (0, top_image.height))

        combined_image.save(combination_path)
        print(f"조합 이미지 저장 완료: {combination_path}")
        recommended_combinations.append(combination_path)
    except Exception as e:
        print(f"Error: 조합 이미지를 생성하는 중 문제가 발생했습니다: {e}")

print("추천 조합 완료")
return recommended_combinations
'''
