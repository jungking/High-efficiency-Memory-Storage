import cv2
import matplotlib.pyplot as plt

def show_image():
    faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    image = cv2.imread("image2.jpg")                #이미지 불러오기 해야함.
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(gray,
                                        scaleFactor= 1.1,      # 이미지 피라미드 스케일 factor
                                        minNeighbors=5         # 인접 객체 최소 거리 픽셀
                                        )        

    print ("Found {0} faces!".format(len(faces)))
    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
    cv2.imshow("Faces found", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    cv2.waitKey(1)

    return plt.imshow(image)

# 멀리 있는 얼굴 인식률 떨어짐 거의 20%..