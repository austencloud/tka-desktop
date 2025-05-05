# Codex Pictograph Exporter

This package contains the code for exporting pictographs with turns for the Codex.

## Overview

The Codex Pictograph Exporter allows users to export pictographs with different turn combinations. It supports all Type 1 letters (A through V) and handles both hybrid and non-hybrid pictographs.

## Classes

### CodexDialog

The main dialog that users interact with. It allows users to select which pictograph types to export and configure the turns.

### CodexExporter

The main exporter class that handles the export process. It uses the other classes to create and export pictographs.

### PictographDataManager

Manages pictograph data, including retrieving data from the dataset and creating minimal data when needed.

### PictographFactory

Creates pictographs from data.

### PictographRenderer

Renders pictographs as images.

### TurnConfiguration

Manages turn configurations, including determining which letters are hybrid, getting turn combinations, and generating filenames.

### BaseCodexExporter

Base class for the exporter, providing common functionality.

## Usage

To use the exporter, create an instance of `CodexDialog` and show it:

```python
from main_window.main_widget.settings_dialog.ui.image_export.codex_exporter import CodexDialog

dialog = CodexDialog(image_export_tab)
dialog.exec()
```

## Directory Structure

The exporter creates a directory structure like this:

```
[User Selected Directory]/
├── red0_blue0/
│   ├── A.png
│   ├── B.png
│   ├── C.png  (only one version needed when turns are the same)
│   └── ...
├── red0_blue1/
│   ├── A.png
│   ├── B.png
│   ├── C_pro.png  (both versions needed when turns are different)
│   ├── C_anti.png
│   └── ...
└── ...
```

When exporting a single turn combination, the user will be taken directly to that specific turn folder. When exporting multiple turn combinations, the user will be taken to the main directory containing all the turn folders.

## Hybrid vs. Non-Hybrid Pictographs

- Non-hybrid pictographs (A, B, D, E, G, H, J, K, M, N, P, Q, S, T) have a single version.
- Hybrid pictographs (C, F, I, L, O, R, U, V) have two versions when the red and blue turns are different:

  1. Pro hand has turns, anti hand has 0 turns (filename: `letter_pro_turns.png`)
  2. Pro hand has 0 turns, anti hand has turns (filename: `letter_anti_turns.png`)

  When the turns are the same, only one version is needed.

This approach focuses on which motion type (pro or anti) gets the turns, rather than which color (red or blue). This ensures that we generate all relevant variations while keeping the structural base of the pictograph the same.
