# Path Interpolator v1.0

A Python-based GUI utility for processing geometric paths. This tool takes a series of coordinates, applies a spatial offset (buffer), and interpolates points at fixed intervals along the resulting path.

## Features
* **Path Offsetting**: Expand or contract paths using a numerical offset via Shapely buffers.
* **Smart Interpolation**: Generate points at a specific distance ($r$) along the path length.
* **Live Preview**: Interactive plot powered by `pyqtgraph` to visualize the original vs. interpolated results.
* **Drag & Drop**: Drop `.txt`, `.tpl`, or `.dat` files directly onto the interface.
* **Custom Styling**: Integrated with the "Adaptic" QSS theme for a modern dark look.

## Setup and Execution

This project uses `uv` for extremely fast, reliable dependency management.

1.  **Clone & Enter**:
    ```bash
    git clone <your-repo-url>
    cd path-interpolator
    ```
2.  **Initialize & Sync**:
    Set up the virtual environment and install all packages defined in the `pyproject.toml` automatically:
    ```bash
    uv sync
    ```
3.  **Run the application**:
    ```bash
    uv run main.py
    ```

---

## How to Use
1.  **Input File**: Browse or Drag & Drop a text file containing coordinates. The file should be formatted with space-separated $X$ and $Y$ values:
    ```text
    0.0000 0.0000
    10.0000 0.0000
    10.0000 10.0000
    ```
2.  **Parameters**:
    * **r**: The desired distance between each interpolated point.
    * **Offset**: The distance to "push" the path outwards (positive) or inwards (negative).
3.  **Generate**: Click **Generate**. The app will create a new file with the `_interpolated` suffix and display the results on the plot.

---

## For End Users (.exe)
If you are using the standalone executable version:
1.  Launch `path-interpolator-v1.0.exe`.
2.  No Python installation or environment setup is required.
3.  *Note: You may need to click "More Info" -> "Run anyway" if prompted by Windows SmartScreen.*