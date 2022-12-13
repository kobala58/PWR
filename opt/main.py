import math
def main():
    grad = 2
    x,y = 4, 4
    step = 0.3
    stop = 0.01
    res = 1
    while res > stop:
        tmp = 0.3*x*grad
        xn = x - tmp
        yn = y - tmp
        res = math.sqrt(2) * tmp
        x,y = xn, yn
        print(xn)
    print(f"X: {xn},\n {2*(xn*xn)}")

def XDD():
    
    return 

if __name__ == "__main__":
    main()
