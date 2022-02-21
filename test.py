import cutils

def main():
    print(cutils.get_factors(1000000))
    print(cutils.even_split([1, 2, 3, 4, 5], 900))
    print(cutils.flatten([1, "a", [1, 2]]))

if __name__ == "__main__":
    main()