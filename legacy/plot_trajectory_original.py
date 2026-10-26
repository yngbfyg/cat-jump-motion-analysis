#---ПОДКЛЮЧЕНИЕ БИБЛИОТЕК---
import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt

def nothing(x):
	pass

def strtofloat(x):
    for i in range(len(x)):
        if (x[i] == ','):
            x = x[:i] + '.' + x[i + 1:]
            break
    return float(x)

#---ФУНКЦИЯ ДЛЯ АППРОКСИМАЦИИ---
#на вход получает массив пар с координатами точек (по х и по у) и степень аппроксимации
#возвращает массив пар с координатами точек на аппроксимированной прямой (с теми же абсциссами)
def polyfit(points, k):
    x = []
    y = []
    for el in points:
        x.append(el[0])
        y.append(el[1])
    ans, res, _, _, _ = np.polyfit(x, y, k, full=True)
    titl = ""
    titl2 = ""
    kk = k
    for i in ans:
        i = float(i)
        i = float('{:.5f}'.format(i))
        titl += str(i)[:7] + ' '
        if (kk != 0):
            titl2 += str(i)[:7] + ' * x^' + str(kk) + ' + '
        else:
            titl2 += str(i)[:7]
        kk -= 1
    return [np.polyval(ans, x), titl, titl2, res]

#---ПОЛУЧЕННОЕ ЗНАЧЕНИЕ ДЛЯ МАСШАТБИРОВАНИЯ---
#13 пикселей в 1 см
kalibr = 13

#---ПУТЬ К ВАШЕМУ ИЗНАЧАЛЬНОМУ ВИДЕО---
vid = cv.VideoCapture("exp2.MOV")

#размер, цвет точек, толщина линии графика
point_size = 1
point_color = (150, 100, 150)
thickness = 4

#---ПУТЬ К ФАЙЛУ С КООРДИНАТАМИ---
f = open("coors.txt")
a = []
for line in f:
    x, y1, likelyhood = line.split()
    x = strtofloat(x)
    y1 = strtofloat(y1)
    a.append([x, 1000-y1])

finalpoints = []
scale = 3 #величина, которую можно изменять для комфортной работы с видео
for i in range(len(a)):
    point = (a[i][0]/scale, a[i][1]/scale)
    finalpoints.append(point)

cv.namedWindow('controls')
cv.createTrackbar('right', 'controls', 0, len(finalpoints) - 1, nothing)
cv.createTrackbar('left', 'controls', 0, len(finalpoints) - 1, nothing)

w = 1000/scale

while True:
    ret, frame = vid.read()
    frame = cv.resize(frame, (frame.shape[1]//scale, frame.shape[0]//scale))
    if not ret:
        break
    img = frame.copy()
    for point in finalpoints:
        cv.circle(frame, (int(point[0]), int(w - point[1])), point_size, point_color, thickness)

    r = cv.getTrackbarPos('right', 'controls')
    l = cv.getTrackbarPos('left', 'controls')

    for i in range(l, r + 1):
        cv.circle(img, (int(finalpoints[i][0]), int(w - finalpoints[i][1])), point_size, (255, 0, 0), thickness)
    cv.imshow("catvid", cv.hconcat((frame, img)))
    if cv.waitKey(0) & 0xFF == ord('q'):
        break

vid.release()
cv.destroyAllWindows()

p = []
for i in range(l, r + 1):
    p.append(list(finalpoints[i]))
    p[-1][0] = p[-1][0] / kalibr * scale
    p[-1][1] = p[-1][1] / kalibr * scale

point_size = 2 #размер точки на графике

k = 1
for i in range(1, 11):
    anss = polyfit(p, i)
    ans = anss[0]
    title = anss[1]
    title2 = anss[2]
    res = anss[3]
    points = []
    x = []
    yfit = []
    y = []
    for j in range(len(ans)):
        x.append(p[j][0])
        yfit.append(ans[j])
        y.append(p[j][1])
        points.append((p[j][0], ans[j]))

    print("степень " + str(k))
    print(title)

    plt.plot(x, y, label='data')
    plt.scatter(x, yfit, label='fit')
    plt.title('траектория (у от х)\n' + 'степень: ' + str(k) + '\nуравнение: ' + title2 + '\nошибка: ' + str(res[0])[:6])
    plt.legend()
    plt.grid(True)
    k += 1
    plt.show()
    if cv.waitKey(0) & 0xFF == ord('q'):
        cv.destroyAllWindows()
    if cv.waitKey(0) & 0xFF == ord('z'):
        cv.destroyAllWindows()
        break

'''
cv.namedWindow(window_capture_name)
cv.namedWindow(window_detection_name)
cv.createTrackbar(low_H_name, window_detection_name , low_H, max_value_H, on_low_H_thresh_trackbar)
'''