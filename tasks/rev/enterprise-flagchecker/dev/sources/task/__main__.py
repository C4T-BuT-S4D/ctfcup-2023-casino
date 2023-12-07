import zlib
import sys
import library.python.checker


def main():
    if library.python.checker.check(sys.argv[1]):
        print('Correct')
    else:
        print('Nope')


if __name__ == "__main__":
    main()
