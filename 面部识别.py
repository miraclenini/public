import cv2
import sys
import face_recognition


face_image = face_recognition.load_image_file(r'C:\Users\Administrator\Desktop\guazi\10.png')
#print(type(face_image)) # 多维数组
# 给定一张图像 返回图像每个面的128维的编码
face_encodings = face_recognition.face_encodings(face_image) #进行特征提取
#print(face_encodings)
# 给定图像 返回图像中每个人脸的面部特征位置
face_locations = face_recognition.face_locations(face_image) # 特征位置
#print(face_locations)

# 判断当前图像人脸个数
n = len(face_encodings)
if n > 2:
    print('超出2人个数')
    sys.exit()

try:
    face1 = face_encodings[0]
    face2 = face_encodings[1]

except:
    print('2')
    sys.exit()

# 两个人脸的特征进行对比
results = face_recognition.compare_faces([face1],face2,tolerance=0.5) #tolerance容错率
print(results)

# 框图
if results == [True]:
    print('1')
    name = 'PASS'

else:
    print('0')
    name = 'NO'

for i in range(len(face_encodings)):
    face_encoding = face_encodings[(i-1)]
    # print(face_encoding)
    face_location = face_locations[(i-1)]
    print(face_location)

    top,right,bottom,left = face_location   #位置参数

    # 画框          图像          框的位置               RGB颜色 框的粗细
    cv2.rectangle(face_image,(left,top),(right,bottom),(0,255,0),2)  # 传入图片
    #
    cv2.putText(face_image,name,(left-10,top-10),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),2)

# 颜色
face_image_rgb = cv2.cvtColor(face_image,cv2.COLOR_BGR2RGB)
#展示图像
cv2.imshow('output',face_image_rgb)


# 关闭
cv2.waitKey(0)

