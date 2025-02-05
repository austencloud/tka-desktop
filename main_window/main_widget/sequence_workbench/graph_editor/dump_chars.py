filename = r"C:\the-kinetic-constructor\main_window\main_widget\sequence_workbench\graph_editor\GE_pictograph_view.py"

with open(filename, "rb") as f:
    data = f.read()


# Print hex offset, hex data, and ASCII side by side
def print_hex_dump(data):
    for i in range(0, len(data), 16):
        chunk = data[i : i + 16]
        # Hex part
        hex_part = " ".join(f"{b:02x}" for b in chunk)
        # ASCII part (printable ASCII or '.')
        ascii_part = "".join(chr(b) if 32 <= b < 127 else "." for b in chunk)
        print(f"{i:08x}  {hex_part:<48}  |{ascii_part}|")


print_hex_dump(data)
