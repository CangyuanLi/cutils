import cutils

def main():
    print(cutils.get_factors(1000000))
    print(cutils.even_split([1, 2, 3, 4, 5], 2))
    print(cutils.flatten([[1, 2, 3], [i for i in range(0, 100000)], [1], 23, [2, [2, 3, [[[[[[[[3]]]]]]]], [2, 4]], {1, 2, 3, 4}]]))

if __name__ == "__main__":
    main()