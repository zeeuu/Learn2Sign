const video = document.getElementById("videoElement");
const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');

      
// 현재 이미지 인덱스
let currentIndex = -1;

// 이미지를 랜덤하게 섞은 리스트
let shuffledImages = shuffleArray(images);

const imageElement = document.getElementById("imageElement");
const nextButton = document.getElementById("nextButton");
const correctModal = document.getElementById("correctModal");
const wrongModal = document.getElementById("wrongModal");
const correctButton = document.getElementById("correctButton");
const wrongButton = document.getElementById("wrongButton");

// 이미지 보여주기
function showImage() {
    const image = shuffledImages[currentIndex];
    imageElement.src = image.src;
    imageElement.alt = image.alt;
}

// 다음 이미지로 이동
function nextImage() {
    currentIndex++;
    if (currentIndex >= shuffledImages.length) {
        currentIndex = 0; // 이미지 목록의 끝에 도달하면 처음 이미지로 이동
    }
    showImage();
}

// 배열을 랜덤하게 섞는 함수
function shuffleArray(array) {
    const shuffled = array.slice(); // 배열 복사
    for (let i = shuffled.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]]; // 요소 위치 교환
    }
    return shuffled;
}

// 정답 모달 열기
function openCorrectModal() {
    correctModal.style.display = "block";
}
// 오답 모달 열기
function openWrongModal() {
    wrongModal.style.display = "block";
}
// 정답 모달 닫기
function closeCorrectModal() {
    correctModal.style.display = "none";
    nextImage();
}
// 오답 모달 닫기
function closeWrongModal() {
    wrongModal.style.display = "none";
}

// 정답 확인 버튼 클릭 시 이벤트 핸들러
correctButton.addEventListener("click", closeCorrectModal);
// 오답 확인 버튼 클릭 시 이벤트 핸들러
wrongButton.addEventListener("click", closeWrongModal);
// 초기 이미지 보여주기
nextImage();

// 웹캠
navigator.mediaDevices
.getUserMedia({ video: true })
.then((stream) => {
    video.srcObject = stream;
})
.catch((error) => {
    console.error(error);
});

// 캡쳐한 이미지 canvas에 그리기
function takePicture() {
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
}

// 스페이스 키 입력시 발생 이벤트(api 호출)
document.addEventListener('keydown', (event) => {
    if (event.code === 'Space') {
        takePicture();
        canvas.toBlob(blob => {
            const formData = new FormData();
            formData.append("image", blob);
            fetch("/api/vowel/quiz", {
                method: "POST",
                headers: {},
                body: formData,
            })
            .then((response) => response.json())
            .then(result => {
                // 응답 받은 데이터의 label 값과 해당 이미지 label(alt 속성값) 비교
                if (result.label === imageElement.alt) {
                  openCorrectModal();
                } else {
                  openWrongModal();
                }
            })
            .catch((error) => console.error(error));
        });
    }
});
