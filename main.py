from random import randint
import math
from matplotlib import pyplot as plt
from termcolor import colored

hull = []
hull_lines = []


def main():
    n = int(input("Please enter the number of points: "))
    sample_points = generate_points(n)
    if 3 <= n <= 10000:
        sample_points.sort()
        print("Sample Points: " + str(sample_points))
        print("Running Hull Convex Algorithm...")
        convex_hull(sample_points)
        centroid = (sum(pt[0] for pt in hull)/len(hull), sum(pt[1] for pt in hull)/len(hull))
        hull.sort(key=lambda pt: math.atan2(pt[1]-centroid[1], pt[0]-centroid[0]))
        print("Hull Points: "+str(hull))
        print("Hull Lines: "+str(hull_lines))
        draw_hull(hull, sample_points)
    elif n < 2:
        print("Convex Hull must consist of 3 or more points")
    elif n > 10000:
        print("Too much points!")
    # endif


def draw_hull(hull_points, sample_points):
    drawable_hull = hull_points
    drawable_hull.append(drawable_hull[0])
    plt.suptitle("Hull Convex")
    plt.scatter([pt[0] for pt in sample_points], [pt[1] for pt in sample_points], color='blue')
    plt.plot([pt[0] for pt in hull], [pt[1] for pt in hull], color='red')
    plt.axis([-10, 110, -10, 110])
    plt.grid()
    plt.show()


def orientation(pb, pe, pc):
    val = (pc[1]-pb[1]) * (pe[0]-pb[0]) - (pe[1]-pb[1]) * (pc[0]-pb[0])
    if val > 0:
        return 1
    elif val < 0:
        return -1
    else:
        return 0


def line_distance(pb, pe, pc):
    return abs((pc[1] - pb[1]) * (pe[0] - pb[0]) - (pe[1] - pb[1]) * (pc[0] - pb[0]))


def generate_points(n):
    """Menghasilkan sejumlah titik ke dalam sebuah list of tuple"""
    points = []
    while len(points) < n:
        point = (randint(0, 100), randint(0, 100))
        if not(point in points):
            points.append(point)
    return points


def quick_hull(sample_points, pb, pe, side):
    idx = -1
    max_dist = 0

    for points in sample_points:
        temp = line_distance(pb, pe, points)
        if orientation(pb, pe, points) == side and temp > max_dist:
            idx = sample_points.index(points)
            max_dist = temp
        # endif
    # end_for

    if idx == -1:
        if not(pe in hull):
            hull.append(pe)
        # endif
        if not(pb in hull):
            hull.append(pb)
        # endif
        hull_lines.append((pb, pe))
        return
    # endif

    quick_hull(sample_points, sample_points[idx], pb, -1*orientation(sample_points[idx], pb, pe))
    quick_hull(sample_points, sample_points[idx], pe, -1*orientation(sample_points[idx], pe, pb))


def convex_hull(sample_points):
    if len(sample_points) < 3:
        return
    else:
        # Menentukan Nilai min dan max dari seluruh tuple sample_points
        mini = min(sample_points)
        maxi = max(sample_points)
        max_x = sample_points.index(maxi)
        min_x = sample_points.index(mini)
        quick_hull(sample_points, sample_points[min_x], sample_points[max_x], 1)
        quick_hull(sample_points, sample_points[min_x], sample_points[max_x], -1)
    # endif


if __name__ == "__main__":
    main()
# endif
