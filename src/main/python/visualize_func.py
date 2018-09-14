import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
from io import BytesIO
import sys
import base64


th_props = [
  ('font-size', '15px'),
  ('text-align', 'center'),
  ('font-weight', 'bold'),
  ('color', '#000'),
  ('font-family','Verdana'),
  ('background-color', '#f7f7f7'),
  ('padding', '12px'),
  ('border-top', '1px solid #636363'),
  ('border-bottom', '1px solid #636363'),
  ('border-left', '1px solid #636363'),
  ('border-right', '1px solid #636363')
]

# Set CSS properties for td elements in dataframe
td_props = [
  ('font-size', '14px'),
  ('color', '#2d2d2d'),
  ('font-family','Verdana'),
  ('background-color', '#fff'),
  ('padding', '10px'),
  ('border-top', '1px solid #636363'),
  ('border-bottom', '1px solid #636363'),
  ('border-left', '1px solid #636363'),
  ('border-right', '1px solid #636363')
]

# Set table styles
styles = [
  dict(selector="th", props=th_props),
  dict(selector="td", props=td_props),
  dict(selector=".row_heading", props=[('display', 'none')]),
  dict(selector=".blank.level0", props=[('display', 'none')]),
  dict(selector="th:first-child ", props=[('display', 'none')])
]


def make_cmap(colors, position=None, bit=False):
    bit_rgb = np.linspace(0,1,256)
    if position is None:
        position = np.linspace(0,1,len(colors))
    else:
        if len(position) != len(colors):
            sys.exit("position length must be the same as colors")
        elif position[0] != 0 or position[-1] != 1:
            sys.exit("position must start with 0 and end with 1")
    if bit:
        for i in range(len(colors)):
            colors[i] = (bit_rgb[colors[i][0]],
                         bit_rgb[colors[i][1]],
                         bit_rgb[colors[i][2]])
    cdict = {'red': [], 'green': [], 'blue': []}
    for pos, color in zip(position, colors):
        cdict['red'].append((pos, color[0], color[0]))
        cdict['green'].append((pos, color[1], color[1]))
        cdict['blue'].append((pos, color[2], color[2]))

    cmap = mpl.colors.LinearSegmentedColormap('my_colormap', cdict, 256)
    return cmap


def gbar(ax, x, y, cmap, width=0.5, bottom=5):
    X = [[.6, .6], [.7, .7]]
    for left, top in zip(x, y):
        right = left + width
        ax.imshow(X, interpolation='bicubic', cmap=cmap,
                  extent=(left, right, bottom, top), alpha=1)
