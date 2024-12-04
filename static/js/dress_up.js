document.addEventListener('DOMContentLoaded', function() {
    const uploadContainer = document.getElementById('uploadContainer');
    const fileInput = document.getElementById('fileUpload');
    const imagePreviewBox = document.getElementById('imagePreviewBox');
    const imagePreview = document.getElementById('imagePreview');
    const fileNameDisplay = document.getElementById('fileName');
    const dressUpButton = document.getElementById('dressUpButton');
    const loadingOverlay = document.getElementById('loadingOverlay');

    function showLoading() {
        loadingOverlay.style.display = 'flex';
    }

    function hideLoading() {
        loadingOverlay.style.display = 'none';
    }

    function handleFiles(files) {
        const file = files[0];
        if (file && file.type.startsWith('image/')) {
            const reader = new FileReader();
            reader.onload = function(e) {
                const imgElement = document.createElement('img');
                imgElement.src = e.target.result;
                imgElement.style.maxWidth = '100%';
                imgElement.style.height = 'auto';
                imagePreview.innerHTML = ''; // 기존 미리보기 제거
                imagePreview.appendChild(imgElement);
                imagePreviewBox.style.display = 'block'; // 미리보기 박스 보이기
            };
            reader.readAsDataURL(file);
        }
    }

    uploadContainer.addEventListener('dragover', function(event) {
        event.preventDefault();
        uploadContainer.style.borderColor = '#CCCCCC'; // 드래그 중일 때 스타일을 더 밝은 회색으로 변경
    });

    uploadContainer.addEventListener('dragleave', function(event) {
        uploadContainer.style.borderColor = '#666666'; // 드래그가 끝났을 때 스타일을 검은색 계열로 복원
    });

    uploadContainer.addEventListener('drop', function(event) {
        event.preventDefault();
        uploadContainer.style.borderColor = '#666666'; // 드래그가 끝났을 때 스타일을 검은색 계열로 복원
        const files = event.dataTransfer.files;
        handleFiles(files);

        // 파일 입력 요소에 파일 설정
        if (files.length > 0) {
            fileInput.files = files;
            fileNameDisplay.textContent = files[0].name;
        }
    });

    fileInput.addEventListener('change', function(event) {
        handleFiles(event.target.files);
        if (fileInput.files.length > 0) {
            fileNameDisplay.textContent = fileInput.files[0].name;
        } else {
            fileNameDisplay.textContent = "No file selected";
        }
    });

    dressUpButton.addEventListener('click', function() {
        if (fileInput.files.length === 0) {
            alert('Please select a file to upload.');
            return;
        }

        showLoading(); // 로딩 시작

        const formData = new FormData();
        formData.append('model_image', fileInput.files[0]);

        fetch('/upload_and_execute_dress_up', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            // 서버 응답과 관계없이 100초 후에 로딩 종료
            setTimeout(() => {
                hideLoading();
                const existingMessage = document.querySelector('.upload-success-message');
                if (existingMessage) {
                    existingMessage.remove();
                }

                if (data.success) {
                    alert('Image uploaded successfully!');
                    const successMessage = document.createElement('div');
                    successMessage.textContent = 'Upload completed successfully!';
                    successMessage.style.color = 'green';
                    successMessage.style.marginTop = '10px';
                    successMessage.classList.add('upload-success-message');
                    uploadContainer.appendChild(successMessage);
                } else {
                    alert('Image upload failed.');
                }
            }, 100000); // 100,000 milliseconds = 100 seconds
        })
        .catch(error => {
            hideLoading(); // 로딩 종료
            console.error('Error:', error);
        });
    });
});