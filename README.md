# patch_terraria_ultrawide.py

## About

This script will read `Terraria.exe` in your current working directory and find the byte pattern that controls the maximum screen width/height allowed before forced zoom is applied:

```text
00 00 F0 44 -- -- -- -- -- -- 00 00 96 44
```

The first 4 bytes control the maximum width, represented in little-endian (`44 F0 00 00` means 1920px).

The last 4 bytes control the maximum height, represented in little-endian (`44 96 00 00` means 1200px).

The middle 6 bytes are don't-cares.

When the script finds the matching pattern, it will update the `0x44` values to `0x55`, thereby allowing a massive screen resolution before forced zoom is applied.

A timestamped backup copy of the executable is made before it is opened or modified. This backup is not removed by the script.

## Install

1. Install the latest Python 3.

2. Copy `patch_terraria_ultrawide.py` to your computer.

3. _Optional: install [tqdm](https://github.com/tqdm/tqdm), e.g. `pip install tqdm`_

## Run

1. Open a Command Prompt and change directories to where the Terraria binary is (for Terraria installed through Steam, this is `C:\Program Files x86\Steam\steamapps\common\Terraria`)

2. Run the script:

   ```bash
   > python patch_terraria_ultrawide.py
   ```

3. If the script was successful, you should see the following output (position and bytes may differ slightly):

   ```text
   Found at position 0x3ea845:
   Old value: 0x00 0x00 0xF0 0x44 0x80 0x55 0x0C 0x00 0x04 0x22 0x00 0x00 0x96 0x44
   New value: 0x00 0x00 0xF0 0x55 0x80 0x55 0x0C 0x00 0x04 0x22 0x00 0x00 0x96 0x55
   ```

4. **Enjoy!** 😎
