import json
import numpy as np
import matplotlib.pyplot as plt
from random import uniform, randint, choice
from os.path import exists
from timeit import default_timer as timer
from math import sqrt, ceil


class Robot:
    def __init__(self, typ, price, range_, camera):
        self.type_ = typ
        self.price = price
        self.range_ = range_
        self.camera = camera


class Factory:
    def __init__(self):
        self.robo_lst = []

    def createRobo(self, cnt):
        self.robo_lst = [Robot(typ=choice(["AGV", "AFV", "ASV", "AUV"]),
                               price=round(uniform(0, 10000), 2),
                               range_=randint(0, 100),
                               camera=randint(0, 1))
                         for i in range(cnt)]

    def moveRobo(self):
        print(f"+{'-' * 5}+{'-' * 14}+{'-' * 8}+{'-' * 8}+")
        print(f"|{' ' * 1}TYP{' ' * 1}|"
              f"{' ' * 4}PRICE{' ' * 5}|"
              f"{' ' * 2}RANGE{' ' * 1}|"
              f"{' ' * 2}CAM{' ' * 3}|")
        for robot in self.robo_lst:
            x = len(f"{robot.price : 0.2f}")
            print(f"+{'-' * 5}+{'-' * 14}+{'-' * 8}+{'-' * 8}+")
            print(f"|{' ' * 1}{robot.type_}{' ' * 1}|"
                  f"{' ' * (10 - x)}{robot.price : 0.2f}{' ' * 1}zł{' ' * 1}|"
                  f"{' ' * (4 - len(str(robot.range_)))}{robot.range_}{' ' * 1}km{' ' * 1}|"
                  f"{' ' * 2}{'jest' if robot.camera == 0 else 'brak'}{' ' * 2}|")

    def saveRobo(self, location):
        payload = [{"typ": robot.type_, "price": robot.price, "range_": robot.range_,
                    "camera": robot.camera} for robot in self.robo_lst]
        with open(f"./{location}.json", "w") as f:
            json.dump(payload, f, indent=4)

    def readRobo(self, location):
        if not exists(f"./{location}.json"):
            raise FileNotFoundError
        else:
            with open(f"./{location}.json", "r") as f:
                dane = json.load(f)
            self.robo_lst = [Robot(robot["typ"], robot["price"], robot["range_"], robot["camera"])
                             for robot in dane]


# Heapsort with steps
def stepheapify(arr, n, i, steps):
    pivot = i
    l = 2 * i + 1
    r = 2 * i + 2
    steps.append([steps[-1][0] + 1,
                  f"Is left = {l} less than the length of the list = {n} and is the price of the pivot less than the "
                  f"price of the left?",
                  steps[-1][2].copy()])
    if l < n and arr[pivot].price < arr[l].price:
        pivot = l
        steps.append([steps[-1][0] + 1, "Yes, change the pivot to the number l", steps[-1][2].copy()])
    else:
        steps.append([steps[-1][0] + 1, "No, proceed further", steps[-1][2].copy()])

    steps.append([steps[-1][0] + 1,
                  f"Is right = {r} less than the length of the list = {n} and is the price of the pivot less than the "
                  f"price of the right?",
                  steps[-1][2].copy()])
    if r < n and arr[pivot].price < arr[r].price:
        pivot = r
        steps.append([steps[-1][0] + 1, "Yes, change the pivot to the number r", steps[-1][2].copy()])
    else:
        steps.append([steps[-1][0] + 1, "No, move over", steps[-1][2]].copy())

    steps.append([steps[-1][0] + 1, f"Did pivot change?", steps[-1][2]].copy())
    if pivot != i:
        arr[i], arr[pivot] = arr[pivot], arr[i]
        temp = steps[-1][2].copy()
        temp[i], temp[pivot] = temp[pivot], temp[i]
        steps.append([steps[-1][0] + 1, "Yes, swap them and repeat the heapification", temp])
        stepheapify(arr, n, pivot, steps)
    else:
        steps.append([steps[-1][0] + 1, "No, leave the heap", steps[-1][2].copy()])


def stepheapsort(arr, steps):
    n = len(arr)
    for i in range(n // 2 - 1, -1, -1):
        stepheapify(arr, n, i, steps)
    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        temp = steps[-1][2].copy()
        temp[0], temp[i] = temp[i], temp[0]
        steps.append([steps[-1][0] + 1, f"Swap the start and the i-th position = {i}", temp])
        stepheapify(arr, i, 0, steps)


def stepheap(arr):
    w = [a.price for a in arr]
    x = np.argsort(np.argsort(w))
    y = [[0, "Start", x]]
    stepheapsort(arr, y)
    for el in y:
        print(f"{el[0]}. {el[1]}")
        print(f"{el[2]}")


# Heapsort bez kroków
def heapify(arr, n, i):
    pivot = i
    l = 2 * i + 1
    r = 2 * i + 2

    if l < n and arr[pivot].price < arr[l].price:
        pivot = l

    if r < n and arr[pivot].price < arr[r].price:
        pivot = r

    if pivot != i:
        arr[i], arr[pivot] = arr[pivot], arr[i]
        heapify(arr, n, pivot)


def heapsort(arr):
    n = len(arr)
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)
    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        heapify(arr, i, 0)


# Quicksort z krokami

def steppartition(arr, l, r, steps):
    pivot = arr[r].price
    x = l - 1
    for y in range(l, r):
        steps.append(
            [steps[-1][0] + 1, f"Is walking through the loop {arr[y].price} less than or equal to the pivot = {pivot}?",
             steps[-1][2].copy()])
        if arr[y].price <= pivot:
            x += 1
            arr[x], arr[y] = arr[y], arr[x]
            temp = steps[-1][2].copy()
            temp[x], temp[y] = temp[y], temp[x]
            steps.append(
                [steps[-1][0] + 1,
                 f"Yes, increase the low index by one and swap its value with the value at the loop index", temp])
        else:
            steps.append(
                [steps[-1][0] + 1, f"No, move over", steps[-1][2].copy()])

    arr[x + 1], arr[r] = arr[r], arr[x + 1]
    temp = steps[-1][2].copy()
    temp[x + 1], temp[r] = temp[r], temp[x + 1]
    steps.append(
        [steps[-1][0] + 1, f"Swap the values at low index + 1 and high index, and return low index + 1", temp])
    return x + 1


def stepquicksort(arr, l, r, steps):
    steps.append([steps[-1][0] + 1, f"Is the low value = {l} less than the high value = {r}?", steps[-1][2].copy()])
    if l < r:
        steps.append(
            [steps[-1][0] + 1, f"Yes, we find the partition position.", steps[-1][2].copy()])
        p = steppartition(arr, l, r, steps)
        stepquicksort(arr, l, p - 1, steps)
        stepquicksort(arr, p + 1, r, steps)
    else:
        steps.append(
            [steps[-1][0] + 1, "No, leave this section untouched", steps[-1][2].copy()])


def stepquick(arr):
    w = [a.price for a in arr]
    x = np.argsort(np.argsort(w))
    y = [[0, "Start", x]]
    stepquicksort(arr, 0, len(arr) - 1, y)
    for el in y:
        print(f"{el[0]}. {el[1]}")
        print(f"{el[2]}")


# Quicksort without steps

def partition(arr, l, r):
    pivot = arr[r].price
    x = l - 1
    for y in range(l, r):
        if arr[y].price <= pivot:
            x += 1
            arr[x], arr[y] = arr[y], arr[x]
    arr[x + 1], arr[r] = arr[r], arr[x + 1]
    return x + 1


def quicksort(arr, l, r):
    if l < r:
        p = partition(arr, l, r)
        quicksort(arr, l, p - 1)
        quicksort(arr, p + 1, r)


# Countsort
def countsort(arr):
    count = [0 for _ in range(101)]
    for r in arr:
        count[r.range_] += 1
    for i in range(1, 101):
        count[i] += count[i - 1]

    out = [None] * len(arr)
    for i in range(len(arr) - 1, -1, -1):
        z = arr[i].range_
        count[z] -= 1
        pos = count[z]
        out[pos] = arr[i]
    return out


# Radixsort

def radixsort(matrix, col=0):
    if col >= len(matrix[0]):
        return matrix
    max_val = max(row[col] for row in matrix)
    exp = 1  #  10^(exp-1)

    while max_val // exp > 0:
        matrix = countingsort(matrix, col, exp)
        exp *= 10

    # Moving through columns if they are identical
    idx = 0
    while idx < len(matrix):
        end = idx + 1
        while end < len(matrix) and matrix[idx][0:col + 1] == matrix[end][0:col + 1]:
            # The above loop checks if there is a repeated value between the row with id and the row with end for
            # the first col columns. If so, it creates a new matrix containing those rows and passes it to radix,
            # shifting the current column one step to the right.
            end += 1
        group = matrix[idx:end]
        if len(group) > 1: # Check if the group consists of more than one row
            matrix[idx:end] = radixsort(group, col + 1)
        idx = end
    return matrix


def countingsort(matrix, col, exp):
    count = [0] * 10  # 10 digits
    out = [0] * len(matrix)

    for row in matrix:
        digit = (row[col] // exp) % 10
        count[digit] += 1

    for i in range(1, 10):
        count[i] += count[i - 1]

    for row in reversed(matrix):
        digit = (row[col] // exp) % 10
        count[digit] -= 1
        out[count[digit]] = row

    return out


def plot(f: Factory, n=1000):
    t_heap, t_quick, t_count, t_radix = [], [], [], []
    robot_arr = [_ for _ in range(10, n + 1, 10)]
    for i in robot_arr:
        print(i)
        f.createRobo(i)

        start = timer()
        heapsort(f.robo_lst.copy())
        t_heap.append(timer() - start)

        start = timer()
        quicksort(f.robo_lst.copy(), 0, len(f.robo_lst) - 1)
        t_quick.append(timer() - start)

        start = timer()
        countsort(f.robo_lst)
        t_count.append(timer() - start)

        ceilsqrt = ceil(sqrt(i))
        matrix = [[randint(0, ceilsqrt) for _ in range(i)] for __ in range(i)]
        start = timer()
        radixsort(matrix)
        t_radix.append(timer() - start)

    fig, ax = plt.subplots()
    ax.plot(robot_arr, t_heap, c="red", label="Heapsort")
    ax.plot(robot_arr, t_quick, c="green", label="Quicksort")
    ax.plot(robot_arr, t_count, c="blue", label="Countsort")
    ax.plot(robot_arr, t_radix, c="black", label="Radixsort")
    plt.legend()
    plt.show()


f = Factory()


def zad1():
    f.createRobo(10)
    stepheap(f.robo_lst)
    f.moveRobo()


def zad2():
    f.createRobo(10)
    stepquick(f.robo_lst)
    f.moveRobo()


def zad3():
    f.createRobo(10)
    f.robo_lst = countsort(f.robo_lst)
    f.moveRobo()


def zad4():
    tab = [
        [1, 2, 3, 4],
        [7, 8, 10, 10],
        [5, 2, 1, 3],
        [7, 6, 10, 12],
        [7, 8, 10, 13],
        [2, 1, 3, 7]
    ]
    tab = radixsort(tab)
    for row in tab:
        print(row)


def zad5():
    plot(f)


#zad1()
zad5()
