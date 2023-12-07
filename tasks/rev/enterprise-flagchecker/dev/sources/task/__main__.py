import zlib
import sys
import library.python.checker


def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} [flag]")
        sys.exit(1)

    try:
        if library.python.checker.check(sys.argv[1]):
            print('Correct')
        else:
            print('Nope')
    except:
        sys.exit(1)


if __name__ == "__main__":
    main()
