# PyQt-framework v7

**A lightweight, modular PyQt6 framework for building GUIs quickly and intuitively.**

PyQt-framework v7 simplifies GUI development by handling layouts, margins, padding, sizes, and alignments — so developers can focus on the app, not the boilerplate.

---

## Features

- **Intuitive API:** Users only provide values; the framework handles the rest.
- **Modular & Maintainable:**  
  - `Volumes` → margins & padding  
  - `Size` → widget size policies  
  - `Alignment` → alignment helpers  
- **Flexible Layouts:** Vertical, horizontal, and form layouts supported.  
- **Plug-and-Play Widgets:** Pages, stacked widgets, labels, buttons, entries, drop-downs, and more.  
- **Robust & Safe:** Built-in logging, validation, and sensible defaults.  
- **Production-Ready v7:** Optimized for rapid prototyping or full applications.

---

## Installation

Clone the repository:

```
git clone https://github.com/JoseRSolis3/PyQt-framework.git
cd PyQt-framework
```

Install dependencies (PyQt6):

```
pip install PyQt6
```

---

## Quick Start

```python
from framework import Widgets, Volumes, Size, Alignment

# Create an application window
app_window = Widgets.application(Widgets.label("Hello, PyQt!"), title="My App")

# Set margins and padding
layout = app_window.centralWidget().layout()
Volumes.margin_builder(layout, Volumes.top_margin(10))
Volumes.padding_builder(layout, Volumes.padding(5))

# Show the app
app_window.show()
```

---

## Widgets & Builders

- `Widgets.application()` → Create main windows  
- `Widgets.page()` → Create pages with child widgets  
- `Widgets.stacked()` → Stacked widget containers  
- `Widgets.label()`, `Widgets.entry()`, `Widgets.button()`, `Widgets.drop_down()` → Common widgets  

---

## Volumes

- `top_margin()`, `bottom_margin()`, `left_margin()`, `right_margin()` → Directional margins  
- `horizontal_margin()`, `vertical_margin()` → Axis-specific margins  
- `default_margin()` → All sides specified  
- `padding()` → Layout spacing  

---

## Size Policies

- `Size.auto`, `Size.fill`, `Size.fixed`, `Size.min`, `Size.max`, `Size.stretch`, `Size.default`  

---

## Alignment

- `Alignment.top`, `Alignment.bottom`, `Alignment.left`, `Alignment.right`, `Alignment.center`  
- Combinations: `top_left`, `top_right`, `bottom_left`, `bottom_right`  

---

## Contributing

Contributions are welcome! Feel free to submit pull requests for:  
- Additional widgets  
- New layout types  
- Feature improvements  
- Bug fixes  

---

## License

MIT License  

---

## Contact / More Info

[GitHub Repository](https://github.com/JoseRSolis3/PyQt-framework)

