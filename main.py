from random import randint
import datetime
import math
from matplotlib import pyplot as plt

hull_points_result = []


def orientation(pb, pe, pc):
    # Mencari letak dari titik, apakah di atas atau di bawah garis yang dibentuk oleh dua titik
    # pb : titik awal garis
    # pe : titik akhir garis
    # pc : titik yang diujikan
    val = (pc[1]-pb[1]) * (pe[0]-pb[0]) - (pe[1]-pb[1]) * (pc[0]-pb[0])
    if val > 0:
        return 1
    elif val < 0:
        return -1
    else:
        return 0


def line_distance(pb, pe, pc):
    # Menghitung perkiraan jarak antara suatu titik dengan garis yang dibentuk oleh dua titik
    # pb : titik awal garis
    # pe : titik akhir garis
    # pc : titik yang diujikan
    return abs((pc[1] - pb[1]) * (pe[0] - pb[0]) - (pe[1] - pb[1]) * (pc[0] - pb[0]))


def generate_points(n):
    # Menghasilkan sejumlah titik ke dalam sebuah list of tuple
    points = []
    while len(points) < n:
        point = (randint(0, 100), randint(0, 100))
        points.append(point)
    return points


def main():
    # Bagian inti program. Program mulai dari sini
    n = int(input("Number of Points: "))  # Meminta input jumlah titik sampel
    if n < 3:
        print("The number of points must be equal or bigger than 3")
    else:
        sample_points = generate_points(n)
        print("Sample Points: " + str(sample_points))
        a = datetime.datetime.now()
        convexHull(sample_points)
        b = datetime.datetime.now()
        print("Hull points = " + str(hull_points_result))
        print("Time elapsed = " + str(b-a))
        draw(hull_points_result, sample_points)


def draw(hull, sample_points):
    # Menggambar hasil algoritna ke dalam suatu visualisasi
    # Titik diurutkan secara counter-clockwise sebelum digambar
    centroid = (sum(pt[0] for pt in hull) / len(hull), sum(pt[1] for pt in hull) / len(hull))
    hull.sort(key=lambda pt: math.atan2(pt[1] - centroid[1], pt[0] - centroid[0]))
    drawable_hull = hull
    drawable_hull.append(drawable_hull[0])
    plt.suptitle("Convex Hull")
    plt.scatter([pt[0] for pt in sample_points], [pt[1] for pt in sample_points], color='blue', s=10)
    plt.plot([pt[0] for pt in hull], [pt[1] for pt in hull], color='red')
    plt.axis([-10, 110, -10, 110])
    plt.grid()
    plt.show()


def quickHull(sample_points, pb, pe, side):
    # Algoritma pencarian titik titik terluar
    # Meliputi bagian DIVIDE, CONQUER dan COMBINE
    max_dist = 0
    hull_pt = (-1, -1)

    # Mencari titik terluar
    # Implentasi bagian CONQUER
    for point in sample_points:
        temp = line_distance(pb, pe, point)
        if orientation(pb, pe, point) == side and temp > max_dist:
            max_dist = temp
            hull_pt = point
        # endif
    # end_for

    if max_dist == 0:
        # Jika tidak ada titik lain yang paling luar, masukkan ke dalam solusi
        # Implementasi bagian COMBINE
        if not(pe in hull_points_result):
            hull_points_result.append(pe)
        # endif
        if not(pb in hull_points_result):
            hull_points_result.append(pb)
        # endif
        return
    # Memisahkan titik untuk quickhull selanjutnya
    # Implementasi bagian DIVIDE
    lower = []
    upper = []
    for point in sample_points:
        if orientation(pb, hull_pt, point) == -1 * orientation(hull_pt, pb, pe):  # bagian bawah vektor pb dan pe
            lower.append(point)
        elif orientation(pe, hull_pt, point) == -1 * orientation(hull_pt, pe, pb):  # bagian atas vektor pb dan pe
            upper.append(point)
        # endif
    # end_for
    quickHull(upper, hull_pt, pb, -1 * orientation(hull_pt, pb, pe))
    quickHull(lower, hull_pt, pe, -1 * orientation(hull_pt, pe, pb))


def convexHull(sample_points):
    # Algoritma pencarian titik terluar disertai dengan bagian DIVIDE
    mini = min(sample_points)
    maxi = max(sample_points)
    print("Max = "+str(maxi))
    print("Min = "+str(mini))
    upper = []
    lower = []
    # Mebagi titik sesuai orientasinya
    # Implementasi dari bagian DIVIDE
    for point in sample_points:
        if orientation(mini, maxi, point) == 1:
            upper.append(point)
        elif orientation(mini, maxi, point) == -1:
            lower.append(point)
        # endif
    # end for
    quickHull(upper, mini, maxi, 1)
    quickHull(lower, mini, maxi, -1)


if __name__ == "__main__":
    main()
