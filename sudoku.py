import csv
import sys
from collections import Counter 
from itertools import chain
from PyQt6.QtWidgets import QMainWindow, QApplication, QWidget, QTextEdit, QPushButton
from PyQt6 import uic


def update_value(x, y):
  grid[x]["value"] = y


# a = row, b = column, c = value, d = box
def update_value_refresh(a, b, c, d = None):
  grid[f'{str(a)}{str(b)}']["value"] = c
  grid[f'{str(a)}{str(b)}']["possible_values"].clear()
  remove_possible_values_from_row(a, c)
  remove_possible_values_from_column(b, c)
  remove_possible_values_from_box(d, c)


def update_possible_values(x, y):
  grid[x]["possible_values"] = y


def check_row_for_value(x, y):
  check_list = []
  for n in range(1, 10):
    check_list.append(grid[f'{str(x)}{str(n)}']["value"])
  if y in check_list:
    return True
  else:
    return False


def check_column_for_value(x, y):
  check_list = []
  for n in range(1, 10):
    check_list.append(grid[f'{str(n)}{str(x)}']["value"])
  if y in check_list:
    return True
  else:
    return False


def check_box_for_value(x, y):
  check_list = []
  for n in grid:
    if grid[n]["box"] != x:
      pass
    else:
      check_list.append(grid[n]["value"])
  if y in check_list:
    return True
  else:
    return False


def check_puzzle():
  values_list = set()
  for box in grid:
    values_list.add(grid[box]["value"])
  if None in values_list:
    return False
  else:
    return True


def get_possible_values():
  for square in grid:
    if grid[square]["value"] is None:
      row = grid[square]["row"]
      column = grid[square]["column"]
      box = grid[square]["box"]
      for n in range(1, 10):
        if check_box_for_value(box, n) is False:
          if check_row_for_value(row, n) is False:
            if check_column_for_value(column, n) is False:
              grid[square]["possible_values"].add(n)
            else:
              pass
          else:
            pass
        else:
          pass
    else:
      pass


def remove_possible_values_from_row(x, y):
  for n in range(1, 10):
    if y in grid[f'{str(x)}{str(n)}']["possible_values"]:
      grid[f'{str(x)}{str(n)}']["possible_values"].remove(y)


def remove_possible_values_from_column(x, y):
  for n in range(1, 10):
    if y in grid[f'{str(n)}{str(x)}']["possible_values"]:
      grid[f'{str(n)}{str(x)}']["possible_values"].remove(y)


def remove_possible_values_from_box(x, y):
  for n in grid:
    if grid[n]["box"] != x:
      pass
    else:
      if y in grid[n]["possible_values"]:
        grid[n]["possible_values"].remove(y)


def check_singles():
  for square in grid:
    if len(grid[square]["possible_values"]) == 1:
      row = grid[square]["row"]
      column = grid[square]["column"]
      box = grid[square]["box"]
      value = grid[square]["possible_values"].pop()
      grid[square]["value"] = value
      remove_possible_values_from_row(row, value)
      remove_possible_values_from_column(column, value)
      remove_possible_values_from_box(box, value)


def check_multiples_in_row():
  for x in range(1, 10):
    possible_values_set_list = []
    for n in range(1, 10):
      possible_values_set_list.append(grid[f'{str(x)}{str(n)}']["possible_values"])
    freq = Counter(chain.from_iterable(possible_values_set_list))
    res = {idx for idx in freq if freq[idx] == 1}
    while len(res) > 0:
      value = res.pop()
      for p in range(1,10):
        if value in grid[f'{str(x)}{str(p)}']["possible_values"]:
          box = grid[f'{str(x)}{str(p)}']["box"]
          update_value_refresh(x, p, value, box)



def check_multiples_in_column():
  for x in range(1, 10):
    possible_values_set_list = []
    for n in range(1, 10):
      possible_values_set_list.append(grid[f'{str(n)}{str(x)}']["possible_values"])
    freq = Counter(chain.from_iterable(possible_values_set_list))
    res = {idx for idx in freq if freq[idx] == 1}
    while len(res) > 0:
      value = res.pop()
      for p in range(1,10):
        if value in grid[f'{str(p)}{str(x)}']["possible_values"]:
          box = grid[f'{str(p)}{str(x)}']["box"]
          update_value_refresh(p, x, value, box)


def check_multiples_in_box():
  for n in range(1, 10):
    possible_values_set_list = []
    for square in grid:
      if grid[square]["box"] == n:
        possible_values_set_list.append(grid[square]["possible_values"])
        freq = Counter(chain.from_iterable(possible_values_set_list))
        res = {idx for idx in freq if freq[idx] == 1}
      else:
        pass
    while len(res) > 0:
      value = res.pop()
      for square in grid:
        if grid[square]["box"] == n:
          if value in grid[square]["possible_values"]:
            update_value_refresh(square[0], square[1], value, n)
          else:
            pass
        else:
          pass


def create_grid():
    grid = {}
    square_list = []
    for n in range(1, 10):
        for p in range(1, 10):
            square_list.append([n, p])
    for squares in square_list:
        name = f'{str(squares[0])}{str(squares[1])}'
        new_dict = {name : {'name': name, 'row' : squares[0], 'column' : squares[1], 'value' : None, 'possible_values': set(), 'box' : None}}
        grid.update(new_dict)
    #Update box key for all dictionaries
    for q in grid:
        if grid[q]["row"] <= 3 and grid[q]["column"] <= 3:
            grid[q]["box"] = 1
        elif grid[q]["row"] <= 3 and grid[q]["column"] > 3 and grid[q]["column"] <= 6:
            grid[q]["box"] = 2
        elif grid[q]["row"] <= 3 and grid[q]["column"] > 6 and grid[q]["column"] <= 9:
            grid[q]["box"] = 3
        elif grid[q]["row"] > 3 and grid[q]["row"] <= 6 and grid[q]["column"] <= 3:
            grid[q]["box"] = 4
        elif grid[q]["row"] > 3 and grid[q]["row"] <= 6 and grid[q]["column"] > 3 and grid[q]["column"] <= 6:
            grid[q]["box"] = 5
        elif grid[q]["row"] > 3 and grid[q]["row"] <= 6 and grid[q]["column"] > 6 and grid[q]["column"] <= 9:
            grid[q]["box"] = 6
        elif grid[q]["row"] > 6 and grid[q]["row"] <= 9 and grid[q]["column"] <= 3:
            grid[q]["box"] = 7
        elif grid[q]["row"] > 6 and grid[q]["row"] <= 9 and grid[q]["column"] > 3 and grid[q]["column"] <= 6:
            grid[q]["box"] = 8
        elif grid[q]["row"] > 6 and grid[q]["row"] <= 9 and grid[q]["column"] > 6 and grid[q]["column"] <= 9:
            grid[q]["box"] = 9
    return grid


class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()
        uic.loadUi("sudoku.ui", self)
        self.show()
        self.save_button.clicked.connect(self.save_button_clicked)
        self.solve_button.clicked.connect(self.solve_button_clicked)
        self.left_html = """<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd">\n<html><head><meta name="qrichtext" content="1" /><style type="text/css">\np, li { white-space: pre-wrap; }\n</style></head><body style=" font-family:'MS Shell Dlg 2'; font-size:36pt; font-weight:400; font-style:normal;">\n<p align="center" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;">"""
        self.right_html = '</p></body></html>'

    def save_button_clicked(self):
        for widget in QApplication.allWidgets():
            if isinstance(widget, QTextEdit):
                widget.setReadOnly(True)
        self.save_button.setEnabled(False)
        for widget in QApplication.allWidgets():
            if isinstance(widget, QTextEdit):
                if widget.toPlainText() == '':
                    pass
                else:
                    name = widget.objectName()[1:]
                    value = widget.toPlainText()
                    update_value(name, int(value))
        get_possible_values()

    def solve_button_clicked(self):
        while check_puzzle() is False:
          check_singles()
          check_multiples_in_row()
          check_multiples_in_column()
          check_multiples_in_box()
        for square in grid:
            self.name = f'b{grid[square]["name"]}'
            self.value = grid[square]["value"]
            for widget in QApplication.allWidgets():
                if isinstance(widget, QTextEdit):
                    if widget.objectName() == self.name:
                        widget.setText(f'{self.left_html}{self.value}{self.right_html}')


grid = create_grid()
app = QApplication(sys.argv)
window = UI()
app.exec()