
import multiprocessing

# Получает элементы из канала.
def consumer(pipe):
    on_read, on_write = pipe
    on_write.close()  # Закрыть конец канала, доступный для записи
    while True:
        try:
            item = on_read.recv()
        except EOFError:
            break
        # Обработать элемент
        print(item)  # Замените эту инструкцию фактической обработкой
    # Завершение
    print("Потребитель завершил работу")


# Создает элементы и помещает их в канал. Переменная sequence представляет
# итерируемый объект с элементами, которые требуется обработать.
def producer(sequence, on_write):
    for item in sequence:
        # Послать элемент в канал
        on_write.send(item)


if __name__ == "__main__":
    on_read, on_write = multiprocessing.Pipe()
    # Запустить процесс-потребитель
    cons_p = multiprocessing.Process(target=consumer, args=((on_read, on_write),))
    cons_p1 = multiprocessing.Process(target=consumer, args=((on_read, on_write),))
    cons_p2 = multiprocessing.Process(target=consumer, args=((on_read, on_write),))
    cons_p.start()
    cons_p1.start()
    cons_p2.start()

    # Закрыть в поставщике конец канала, доступный для чтения
    on_read.close()

    # Отправить элементы
    sequence = [1, 2, 3, 4]
    producer(sequence, on_write)

    # Сообщить об окончании, закрыв конец канала, доступный для записи
    on_write.close()

    # Дождаться, пока завершится процесс-потребитель
    cons_p.join()
    cons_p1.join()
    cons_p2.join()
