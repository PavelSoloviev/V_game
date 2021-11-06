from random import shuffle
from tkinter import *

Field_SIZE = 3  # Размер игрового поля
Block_SIZE = 100  # Размер одного блока
Empty_block_SQUARE = Field_SIZE ** 2  # Значение пустого блока

root = Tk()     # Создание окна приложения
#root.iconbitmap('E:/Game/Game_for_Isu/logo.ico')
root.title("Игра в 8")
# Создание области для рисования
c = Canvas(root, width=Field_SIZE * Block_SIZE,
           height=Field_SIZE * Block_SIZE, bg='#FFFFFF')
c.pack()


def get_inv_count():    # Функция, которая считает количество перемещений

    inv = 0
    inv_board = board[:]
    inv_board.remove(Empty_block_SQUARE)
    for i in range(len(inv_board)):
        first_item = inv_board[i]
        for j in range(i+1, len(inv_board)):
            second_item = inv_board[j]
            if first_item > second_item:
                inv += 1
    return inv


def is_solvable():    # Функция , которая определяет имеет ли головоломка решение
    num_inv = get_inv_count()
    if Field_SIZE % 2 != 0:
        return num_inv % 2 == 0
    else:
        empty_square_row = Field_SIZE - (board.index(Empty_block_SQUARE) // Field_SIZE)
        if empty_square_row % 2 == 0:
            return num_inv % 2 != 0
        else:
            return num_inv % 2 == 0


def get_empty_neighbor(index):   # Функция , которая возвращает индекс блока с которым мы меняем местами наш блок
    # получаем индекс пустой клетки в списке
    empty_index = board.index(Empty_block_SQUARE)
    # узнаем расстояние от пустой клетки до клетки по которой кликнули
    abs_value = abs(empty_index - index)
    # Если пустая клетка над или под клектой на которую кликнули
    # возвращаем индекс пустой клетки
    if abs_value == Field_SIZE:
        return empty_index
    # Если пустая клетка слева или справа
    elif abs_value == 1:
        # Проверяем, чтобы блоки были в одном ряду
        max_index = max(index, empty_index)
        if max_index % Field_SIZE != 0:
            return empty_index
    # Рядом с блоком не было пустого поля
    return index


def draw_board():
    # убираем все, что нарисовано на холсте
    c.delete('all')

    # i и j - координатами для каждого блока
    for i in range(Field_SIZE):
        for j in range(Field_SIZE):
            # получаем значение, которое мы должны будем нарисовать на квадрате
            index = str(board[Field_SIZE * i + j])
            # если это не клетка которую мы хотим оставить пустой
            if index != str(Empty_block_SQUARE):
                # рисуем квадрат по заданным координатам
                c.create_rectangle(j * Block_SIZE, i * Block_SIZE,
                                   j * Block_SIZE + Block_SIZE,
                                   i * Block_SIZE + Block_SIZE,
                                   fill='#005244',
                                   outline='#FFFFFF')
                # пишем число в центре квадрата
                c.create_text(j * Block_SIZE + Block_SIZE / 2,
                              i * Block_SIZE + Block_SIZE / 2,
                              text=index,
                              font="Arial {} italic".format(int(Block_SIZE / 4)),
                              fill='#FFFFFF')


def show_victory_window():
    # Рисуем фон окна победы по центру поля
    c.create_rectangle(Block_SIZE / 5,
                       Block_SIZE * Field_SIZE / 2 - 10 * Field_SIZE,
                       Field_SIZE * Block_SIZE - Block_SIZE / 5,
                       Block_SIZE * Field_SIZE / 2 + 10 * Field_SIZE,
                       fill='#000000',
                       outline='#FFFFFF')
    # Пишем текст Победа
    c.create_text(Block_SIZE * Field_SIZE / 2, Block_SIZE * Field_SIZE / 1.9,
                  text="ПОБЕДА", font="Arial {} bold".format(int(10 * Field_SIZE)), fill='#CFB53B')


def click(event):
    # Записываем координаты клика игрока
    x, y = event.x, event.y
    # Конвертируем координаты из пикселей в клеточки
    x = x // Block_SIZE
    y = y // Block_SIZE
    # Получаем индекс в списке объекта по которому мы нажали
    board_index = x + (y * Field_SIZE)
    # Получаем индекс пустой клетки в списке
    empty_index = get_empty_neighbor(board_index)
    # Меняем местами пустую клетку и клетку, по которой кликнули
    board[board_index], board[empty_index] = board[empty_index], board[board_index]
    # Перерисовываем игровое поле
    draw_board()
    # Если текущее состояние доски соответствует правильному - рисуем сообщение о победе
    if board == correct_board:
        show_victory_window()

# Привязываем обработчик событий
c.bind('<Button-1>', click)
c.pack()


board = list(range(1, Empty_block_SQUARE + 1))   # Создаем список блоков
correct_board = board[:]  # Список выиграшной комбинации
shuffle(board)  # Перемешиваем поле

while not is_solvable():
    shuffle(board)

draw_board()    # Рисуем игровое поле
root.mainloop()
