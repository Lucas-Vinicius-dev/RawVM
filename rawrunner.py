from rawvm import run
import sys

def main():
    if len(sys.argv) < 2:
        print("Use: raw <file.raw>")
        return

    filename = sys.argv[1]

    try:
        with open(filename, "r", encoding="utf-8") as f:
            code = f.read()
    except FileNotFoundError:
        print(f"FILE NOT FOUND ||: {filename}")
        return

    run(code)

if __name__ == "__main__":
    main()