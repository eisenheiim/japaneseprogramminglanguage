from pathlib import Path
import difflib

def compare_folders(dir1, dir2):
    dir1 = Path(dir1)
    dir2 = Path(dir2)

    files1 = {f.name: f for f in dir1.iterdir() if f.is_file()}
    files2 = {f.name: f for f in dir2.iterdir() if f.is_file()}

    all_names = sorted(set(files1) | set(files2))

    for name in all_names:
        f1 = files1.get(name)
        f2 = files2.get(name)

        

        if f1 is None:
            print(f"\n=== {name} ===")
            print(f"❌ Only in {dir2}")
            continue

        if f2 is None:
            print(f"\n=== {name} ===")
            print(f"❌ Only in {dir1}")
            continue

        lines1 = f1.read_text(encoding="utf-8", errors="ignore").splitlines()
        lines2 = f2.read_text(encoding="utf-8", errors="ignore").splitlines()

        if lines1 == lines2:
            pass
        else:
            print(f"\n=== {name} ===")
            print("⚠️ Files differ")
            diff = difflib.unified_diff(
                lines1,
                lines2,
                fromfile=str(f1),
                tofile=str(f2),
                lineterm=""
            )
            for line in diff:
                print(line)

if __name__ == "__main__":
    compare_folders("out2", "outputs")

