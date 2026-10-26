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

#13 пикселей в 1 см
kalibr = 13

vid = cv.VideoCapture("exp2.MOV")
point_size = 1
point_color = (150, 100, 150)
thickness = 4

f = open("coors.txt")
tm = open("time.txt")
time = []
for line in tm:
    time.append(float(line[:-1]))
a = []
for line in f:
    x, y1, likelyhood = line.split()
    x = strtofloat(x)
    y1 = strtofloat(y1)
    a.append([x, 1000-y1])

finalpoints = []
finalpointsx = []
finalpointsy = []

scale = 3

for i in range(len(a)):
    point = (a[i][0]/scale, a[i][1]/scale)
    finalpoints.append(point)
    finalpointsx.append((time[i], a[i][0]/scale))
    finalpointsy.append((time[i], a[i][1]/scale))

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
    #print(l, r)
    cv.imshow("catvid", cv.hconcat((frame, img)))
    if cv.waitKey(0) & 0xFF == ord('q'):
        break

vid.release()
cv.destroyAllWindows()

p = []
px = []
py = []

for i in range(l, r + 1):
    p.append(list(finalpoints[i]))
    p[-1][1] = p[-1][1] / kalibr * scale

    px.append(list(finalpointsx[i]))
    px[-1][1] = px[-1][1] / kalibr * scale

    py.append(list(finalpointsy[i]))
    py[-1][1] = py[-1][1] / kalibr * scale


point_size = 2

#---Х ОТ ВРЕМЕНИ---

k = 1
for i in range(1, 4):
    anss = polyfit(px, i)
    ans = anss[0]
    title = anss[1]
    title2 = anss[2]
    res = anss[3]
    points = []
    x = []
    yfit = []
    y = []
    for j in range(len(ans)):
        x.append(px[j][0])
        yfit.append(ans[j])
        y.append(px[j][1])
        points.append((px[j][0], ans[j]))

    print("степень " + str(k))
    print(title)

    plt.plot(x, y, label='data')
    plt.scatter(x, yfit, label='fit')
    plt.title('x(см) от времени(с)' + '\nстепень: ' + str(k) + '\nуравнение: ' + title2 + '\nошибка: ' + str(res[0])[:6])
    plt.legend()
    plt.grid(True)
    k += 1
    plt.show()
    if cv.waitKey(0) & 0xFF == ord('q'):
        cv.destroyAllWindows()


#---У ОТ ВРЕМЕНИ---

k = 1
for i in range(1, 4):
    anss = polyfit(py, i)
    ans = anss[0]
    title = anss[1]
    title2 = anss[2]
    res = anss[3]
    points = []
    x = []
    yfit = []
    y = []
    for j in range(len(ans)):
        x.append(py[j][0])
        yfit.append(ans[j])
        y.append(py[j][1])
        points.append((py[j][0], ans[j]))
    #print(points)

    print("степень " + str(k))
    print(title)

    plt.plot(x, y, label='data')
    plt.scatter(x, yfit, label='fit')
    plt.title('y(см) от времени(с)' + '\nстепень: ' + str(k) + '\nуравнение: ' + title2 + '\nошибка: ' + str(res[0])[:6])
    plt.legend()
    plt.grid(True)
    k += 1
    plt.show()
    if cv.waitKey(0) & 0xFF == ord('q'):
        cv.destroyAllWindows()
