from flask import Flask, request, jsonify, render_template, Response
from flask_cors import CORS
import numpy as np
import tensorflow as tf
import cv2
from PIL import Image, ImageDraw, ImageFont

app = Flask(__name__)
CORS(app)

#### templates 렌더링 ####
## 메인 페이지
@app.route('/main')
def main():
    return render_template('main.html')

## 제안 페이지
@app.route('/contact')
def contact():
    return render_template('contact.html')

## 자음 페이지
@app.route('/consonant')
def c_select():
   return render_template('cselect.html')

## 문제 페이지
@app.route('/consonant/quiz')
def c_quiz():
    images = [{'src': "../static/image/study/c00.jpg", 'alt': "ㄱ"},
              {'src': "../static/image/study/c01.jpg", 'alt': "ㄴ"},
              {'src': "../static/image/study/c02.jpg", 'alt': "ㄷ"},
              {'src': "../static/image/study/c03.jpg", 'alt': "ㄹ"},
              {'src': "../static/image/study/c04.jpg", 'alt': "ㅁ"},
              {'src': "../static/image/study/c05.jpg", 'alt': "ㅂ"},
              {'src': "../static/image/study/c06.jpg", 'alt': "ㅅ"},
              {'src': "../static/image/study/c07.jpg", 'alt': "ㅇ"},
              {'src': "../static/image/study/c08.jpg", 'alt': "ㅈ"},
              {'src': "../static/image/study/c09.jpg", 'alt': "ㅊ"},
              {'src': "../static/image/study/c10.jpg", 'alt': "ㅋ"},
              {'src': "../static/image/study/c11.jpg", 'alt': "ㅌ"},
              {'src': "../static/image/study/c12.jpg", 'alt': "ㅍ"},
              {'src': "../static/image/study/c13.jpg", 'alt': "ㅎ"}]
    return render_template('cquiz.html', images=images)

## 학습 페이지
@app.route('/consonant/learn')
def c_learn():
    return render_template('clearn.html')


## 모음 페이지
@app.route('/vowel')
def v_select():
   return render_template('vselect.html')

## 문제 페이지
@app.route('/vowel/quiz')
def v_quiz():
    images = [{'src': "../static/image/study/v00.jpg", 'alt': "ㅏ"},
              {'src': "../static/image/study/v01.jpg", 'alt': "ㅑ"},
              {'src': "../static/image/study/v02.jpg", 'alt': "ㅓ"},
              {'src': "../static/image/study/v03.jpg", 'alt': "ㅕ"},
              {'src': "../static/image/study/v04.jpg", 'alt': "ㅗ"},
              {'src': "../static/image/study/v05.jpg", 'alt': "ㅛ"},
              {'src': "../static/image/study/v06.jpg", 'alt': "ㅜ"},
              {'src': "../static/image/study/v07.jpg", 'alt': "ㅠ"},
              {'src': "../static/image/study/v08.jpg", 'alt': "ㅡ"},
              {'src': "../static/image/study/v09.jpg", 'alt': "ㅣ"},
              {'src': "../static/image/study/v10.jpg", 'alt': "ㅐ"},
              {'src': "../static/image/study/v11.jpg", 'alt': "ㅒ"},
              {'src': "../static/image/study/v12.jpg", 'alt': "ㅔ"},
              {'src': "../static/image/study/v13.jpg", 'alt': "ㅖ"},
              {'src': "../static/image/study/v14.jpg", 'alt': "ㅢ"},
              {'src': "../static/image/study/v15.jpg", 'alt': "ㅚ"},
              {'src': "../static/image/study/v16.jpg", 'alt': "ㅟ"}]
    return render_template('vquiz.html', images=images)

## 학습 페이지
@app.route('/vowel/learn')
def v_learn():
    return render_template('vlearn.html')

## 숫자 페이지
@app.route('/number')
def n_select():
   return render_template('nselect.html')

## 문제 페이지
@app.route('/number/quiz')
def n_quiz():
    images = [{'src': "../static/image/study/n00.jpg", 'alt': "0"},
              {'src': "../static/image/study/n01.jpg", 'alt': "1"},
              {'src': "../static/image/study/n02.jpg", 'alt': "2"},
              {'src': "../static/image/study/n03.jpg", 'alt': "3"},
              {'src': "../static/image/study/n04.jpg", 'alt': "4"},
              {'src': "../static/image/study/n05.jpg", 'alt': "5"},
              {'src': "../static/image/study/n06.jpg", 'alt': "6"},
              {'src': "../static/image/study/n07.jpg", 'alt': "7"},
              {'src': "../static/image/study/n08.jpg", 'alt': "8"},
              {'src': "../static/image/study/n09.jpg", 'alt': "9"}]
    return render_template('nquiz.html', images=images)

## 학습 페이지
@app.route('/number/learn')
def n_learn():
    return render_template('nlearn.html')


#### 문제 ####
# 자음
# 모델 불러오기
c_model = tf.keras.models.load_model('./model/c_model.h5')

# 자음 label 목록
c_label_list = {'ㄱ': 0, 'ㄴ': 1, 'ㄷ': 2, 'ㄹ': 3, 'ㅁ': 4, 'ㅂ': 5,
                'ㅅ': 6, 'ㅇ': 7, 'ㅈ': 8, 'ㅊ': 9, 'ㅋ': 10, 'ㅌ': 11, 'ㅍ': 12, 'ㅎ': 13}
c_labels = list(c_label_list.keys())

# 자음 문제
@app.route('/api/consonant/quiz', methods=['POST'])
def c_predict():
    if request.method == 'POST':
        # 이미지 파일 읽어오기
        file = request.files['image']

        # 이미지 로드
        img = cv2.imdecode(np.fromstring(
            file.read(), np.uint8), cv2.IMREAD_COLOR)

        # 이미지 256x256 크기로 변환
        img = cv2.resize(img, (256, 256))

        # 텐서로 변환
        img = np.expand_dims(
            tf.keras.applications.resnet_v2.preprocess_input(img), axis=0)

        # 예측
        pred = c_model.predict(img)

        # 가장 확률 높은 label
        label = c_labels[np.argmax(pred)]

        # 결과 반환
        result = {'label': label}
    return jsonify(result)


# 모음
# 모델 불러오기
v_model = tf.keras.models.load_model('./model/v_model.h5')

# 모음 label 목록
v_label_list = {'ㅏ': 0, 'ㅑ': 1, 'ㅓ': 2, 'ㅕ': 3, 'ㅗ': 4, 'ㅛ': 5, 'ㅜ': 6, 'ㅠ': 7, 'ㅡ': 8, 'ㅣ': 9,
                'ㅐ': 10, 'ㅒ': 11, 'ㅔ': 12, 'ㅖ': 13, 'ㅢ': 14, 'ㅚ': 15, 'ㅟ': 16}
v_labels = list(v_label_list.keys())

# 모음 문제
@app.route('/api/vowel/quiz', methods=['POST'])
def v_predict():
    if request.method == 'POST':
        # 이미지 파일 읽어오기
        file = request.files['image']

        # 이미지 로드
        img = cv2.imdecode(np.fromstring(
            file.read(), np.uint8), cv2.IMREAD_COLOR)

        # 이미지 256x256 크기로 변환
        img = cv2.resize(img, (256, 256))

        # 텐서로 변환
        img = np.expand_dims(
            tf.keras.applications.resnet_v2.preprocess_input(img), axis=0)

        # 예측
        pred = v_model.predict(img)

        # 가장 확률 높은 label
        label = v_labels[np.argmax(pred)]

        # 결과 반환
        result = {'label': label}
    return jsonify(result)


# 숫자
# 모델 불러오기
n_model = tf.keras.models.load_model('./model/n_model.h5')

# 숫자 label 목록
n_label_list = {'0': 0, '1': 1, '2': 2, '3': 3,
                '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9}
n_labels = list(n_label_list.keys())

# 숫자 문제
@app.route('/api/number/quiz', methods=['POST'])
def n_predict():
    if request.method == 'POST':
        # 이미지 파일 읽어오기
        file = request.files['image']

        # 이미지 로드
        img = cv2.imdecode(np.fromstring(
            file.read(), np.uint8), cv2.IMREAD_COLOR)

        # 이미지 256x256 크기로 변환
        img = cv2.resize(img, (256, 256))

        # 텐서로 변환
        img = np.expand_dims(
            tf.keras.applications.resnet_v2.preprocess_input(img), axis=0)

        # 예측
        pred = n_model.predict(img)

        # 가장 확률 높은 label
        label = n_labels[np.argmax(pred)]

        # 결과 반환
        result = {'label': label}
    return jsonify(result)


#### 학습 ####
def video(camera, model, labels):
    while camera.isOpened():
        ret, image = camera.read()
        if not ret:
            continue
        # 이미지 처리 및 예측
        img = cv2.resize(image, (256, 256))
        img = np.expand_dims(
            tf.keras.applications.resnet_v2.preprocess_input(img), axis=0)
        result = model.predict(img)
        # 결과 표시
        image_pil = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        draw = ImageDraw.Draw(image_pil)
        # org-텍스트 시작 위치 x,y
        org = (600, 50)
        # 모델 예측값
        text = labels[np.argmax(result)]
        # 글씨체, 크기
        font = ImageFont.truetype("fonts/NanumGothic.ttf", 150)
        # fill-텍스트 색 / stroke_width-외곽선 두께 / stroke_fill-외곽선 색상
        draw.text(org, text, font=font, fill=(0, 0, 0),
                  stroke_width=3, stroke_fill=(255, 255, 255))

        frame = cv2.cvtColor(np.array(image_pil), cv2.COLOR_RGB2BGR)
        ret, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n\r\n')


# 자음 학습
@app.route('/api/consonant/learn')
def c_video():
    camera = cv2.VideoCapture(0)
    return Response(video(camera, c_model, c_labels), mimetype='multipart/x-mixed-replace; boundary=frame')

# 모음 학습
@app.route('/api/vowel/learn')
def v_video():
    camera = cv2.VideoCapture(0)
    return Response(video(camera, v_model, v_labels), mimetype='multipart/x-mixed-replace; boundary=frame')

# 숫자 학습
@app.route('/api/number/learn')
def n_video():
    camera = cv2.VideoCapture(0)
    return Response(video(camera, n_model, n_labels), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(debug=True)
