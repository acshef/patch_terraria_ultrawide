import datetime, io, os, pathlib, shutil, typing as t


if t.TYPE_CHECKING:
    from _typeshed import FileDescriptorOrPath


try:
    from tqdm import tqdm
except ImportError:

    class DummyTQDM:
        def __init__(self, *args, **kwargs):
            return

        def __enter__(self, *args, **kwargs):
            return self

        def __exit__(self, *args, **kwargs):
            return

        def update(self, *args, **kwargs):
            return

    tqdm = DummyTQDM


__version__ = "1.0.0"


T = t.TypeVar("T")


EXE_NAME = "Terraria.exe"


PATTERN = (
    0x00,  # Max width before zoom is capped, little endian (44 F0 00 00 is 1920)
    0x00,
    0xF0,
    0x44,
    None,  # Don't cares
    None,
    None,
    None,
    None,
    None,
    0x00,  # Max height before zoom is capped, little endian (44 96 00 00 is 1200)
    0x00,
    0x96,
    0x44,
)


REPLACEMENT = b"\x00\x00\x00\x55\x00\x00\x00\x00\x00\x00\x00\x00\x00\x55"  # Raise the rightmost byte of both dimensions


def main(path: "FileDescriptorOrPath"):
    path = pathlib.Path(path)
    backup = path.with_name(
        path.name + "_backup_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    )
    shutil.copyfile(path, backup)
    byte_count = path.stat().st_size
    pattern_len = len(PATTERN)
    success = False
    with open(path, "rb+", buffering=io.DEFAULT_BUFFER_SIZE) as f:
        with tqdm(total=byte_count - pattern_len + 1) as pbar:
            while b := f.peek(pattern_len)[:pattern_len]:
                if len(b) < pattern_len:
                    # Reached the end of the bytes, now we're just getting the tail
                    break

                if match(b, PATTERN, ignore=[None]):
                    success = True
                    new_value = bytes(x | y for x, y in zip(b, REPLACEMENT))
                    pbar.close()
                    print(f"Found at position {hex(f.tell())}:")
                    print("Old value: " + " ".join(f"0x{x:02X}" for x in b))
                    print("New value: " + " ".join(f"0x{x:02X}" for x in new_value))
                    f.write(new_value)
                    break

                f.seek(1, os.SEEK_CUR)
                pbar.update()

    if not success:
        print("Pattern not found!")
        return 13  # WinError.h ERROR_INVALID_DATA


def match(
    a: t.Iterable[bytes], b: t.Iterable[bytes], /, *, ignore: t.Iterable[bytes] = None
) -> bool:
    maxlen = max(len(a), len(b))
    if ignore is None:
        ignore = []
    for i in range(maxlen):
        if i >= len(a) or i >= len(b):
            return False
        if a[i] in ignore or b[i] in ignore:
            continue
        if a[i] != b[i]:
            return False
    return True


if __name__ == "__main__":
    try:
        path = pathlib.Path(".", EXE_NAME).resolve(True)
        exit(main(path))
    except FileNotFoundError:
        print(f"Could not find {EXE_NAME} in your current working directory!")
        exit(2)  # WinError.h ERROR_FILE_NOT_FOUND
    except KeyboardInterrupt:
        print("Aborted!")
        exit(1067)  # WinError.h ERROR_PROCESS_ABORTED
