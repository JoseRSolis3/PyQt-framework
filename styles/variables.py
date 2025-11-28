# variables.py
# =======================
# CSS property suffixes / values for easy Python usage
# Supports: from variables import *
# =======================

# -----------------------
# Background properties
# -----------------------
color = "-color"
image = "-image"
repeat = "-repeat"
position = "-position"
attachment = "-attachment"
origin = "-origin"
clip = "-clip"
size = "-size"
blend_mode = "-blend-mode"

# Background values
noRepeat = "no-repeat"
repeat = "repeat"
repeatX = "repeat-x"
RepeatY = "repeat-y"
scroll = "scroll"
fixed = "fixed"
local = "local"

# -----------------------
# Border properties
# -----------------------
border = "-border"
border_color = "-border-color"
border_style = "-border-style"
border_width = "-border-width"
border_radius = "-border-radius"

# Border style values
dotted = "dotted"
dashed = "dashed"
solid = "solid"
double = "double"
groove = "groove"
ridge = "ridge"
inset = "inset"
outset = "outset"
none = "none"
hidden = "hidden"

# -----------------------
# Font properties
# -----------------------
font_family = "-font-family"
font_size = "-font-size"
font_weight = "-font-weight"
font_style = "-font-style"
font_variant = "-font-variant"
line_height = "-line-height"

# Font values
bold = "bold"
normal = "normal"
italic = "italic"
small_caps = "small-caps"

# -----------------------
# Text properties
# -----------------------
color_text = "color"
text_align = "-text-align"
text_decoration = "-text-decoration"
text_transform = "-text-transform"
text_overflow = "-text-overflow"
white_space = "-white-space"

# Text values
uppercase = "uppercase"
lowercase = "lowercase"
capitalize = "capitalize"
nowrap = "nowrap"
ellipsis = "ellipsis"

# -----------------------
# Display & Box
# -----------------------
display = "-display"
visibility = "-visibility"
overflow = "-overflow"
overflow_x = "-overflow-x"
overflow_y = "-overflow-y"
box_sizing = "-box-sizing"
width = "-width"
height = "-height"
min_width = "-min-width"
min_height = "-min-height"
max_width = "-max-width"
max_height = "-max-height"

# Display values
block = "block"
inline_block = "inline-block"
inline_ = "inline"
flex = "flex"
grid = "grid"
none_ = "none"

# -----------------------
# Positioning
# -----------------------
position_ = "-position"
top = "-top"
right = "-right"
bottom = "-bottom"
left = "-left"
z_index = "-z-index"

# Position values
relative = "relative"
absolute = "absolute"
fixed = "fixed"
sticky = "sticky"

# -----------------------
# Flexbox properties
# -----------------------
flex_direction = "-flex-direction"
flex_wrap = "-flex-wrap"
justify_content = "-justify-content"
align_items = "-align-items"
align_self = "-align-self"
align_content = "-align-content"
gap = "-gap"
row = "row"
row_reverse = "row-reverse"
column = "column"
column_reverse = "column-reverse"
wrap = "wrap"
nowrap_ = "nowrap"
space_between = "space-between"
space_around = "space-around"
space_evenly = "space-evenly"
center = "center"
flex_start = "flex-start"
flex_end = "flex-end"
stretch = "stretch"

# -----------------------
# Grid properties
# -----------------------
grid_template_columns = "-grid-template-columns"
grid_template_rows = "-grid-template-rows"
grid_column = "-grid-column"
grid_row = "-grid-row"
grid_area = "-grid-area"
grid_gap = "-grid-gap"

# -----------------------
# Units
# -----------------------
px = "px"
em = "em"
rem = "rem"
percent = "%"
vh = "vh"
vw = "vw"
vmin = "vmin"
vmax = "vmax"

# -----------------------
# Colors (common CSS colors)
# -----------------------
white = "white"
black = "black"
red = "red"
green = "green"
blue = "blue"
yellow = "yellow"
orange = "orange"
purple = "purple"
pink = "pink"
gray = "gray"
lightgray = "lightgray"
darkgray = "darkgray"
transparent = "transparent"
