# python_web

### html - python(flask) - mysql

### sign up, sign in -> upload picture, view picture


    upload.html        face.html  
이미지 업로드 -> 얼굴 인식 -> 인식된 얼굴에 이름 입력 -> 이미지 저장
html 이미지 위에 <area shape="rect" coords="1, 2, 3, 4 " alt = "face1" href = "computer.html">, 좌표로 사각형 만들기 가능 - O

내일은 db 할 것.

upload로 사진 등록 시, 얼굴 인식이 되고, 새로운 얼굴이라면 이름 입력,
이미 있는 얼굴이라면 혹시 이사람인가요? 라고 이름 선택 - X

이름 등록 후, picture로 가면 전체 사진 표에 id, date, content 에 추가로
이 사진에 찍힌 사람의 이름 (db에 저장된 것) 표시 - 데이터가 안넘어옹ㅁ

