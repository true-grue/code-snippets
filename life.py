# Conway's Game of Life

from random import randint
import tkinter as tk

GRID_W = 50
GRID_H = 50
SCREEN_W = GRID_W * 15
SCREEN_H = GRID_H * 15

States = [
  [[False for y in range(GRID_H)] for x in range(GRID_W)],
  [[False for y in range(GRID_H)] for x in range(GRID_W)]
]

root = tk.Tk()
C = tk.Canvas(root, width=SCREEN_W, height=SCREEN_H)
C.pack()

def make_grid():
  grid = [[] for x in range(GRID_W)]
  w, h = SCREEN_W / GRID_W, SCREEN_H / GRID_H
  for x in range(GRID_W):
    for y in range(GRID_H):   
      r = C.create_rectangle(x * w, y * h, x * w + w, y * h + h, fill="white")
      grid[x].append(r)
  return grid

Grid = make_grid()

def update_grid(grid, state):
  for x in range(GRID_W):
    for y in range(GRID_H):
      C.itemconfig(grid[x][y], fill="red" if state[x][y] else "white")

def get_neighbors(state, x, y):
  n = -int(state[x][y])
  for i in (-1, 0, 1):
    for j in (-1, 0, 1):
      x1, y1 = x + i, y + j
      if 0 <= x1 < GRID_W and 0 <= y1 < GRID_H:
        n += int(state[x1][y1])
  return n

def update_state(old_state, new_state):
  for x in range(GRID_W):
    for y in range(GRID_H):
      n = get_neighbors(old_state, x, y)
      if old_state[x][y] and n not in (2, 3):
        new_state[x][y] = False
      elif not old_state[x][y] and n == 3:
        new_state[x][y] = True
      else:
        new_state[x][y] = old_state[x][y]
    root.update()

def life():
  old_state, new_state = States
  update_grid(Grid, old_state)
  update_state(old_state, new_state)
  States[0] = new_state
  States[1] = old_state
  root.after(5, life)

def init_state(state, n):
  for i in range(n):
    x, y = randint(0, GRID_W - 1), randint(0, GRID_H - 1)
    state[x][y] = True

init_state(States[0], 500)
root.after(0, life)
tk.mainloop()
