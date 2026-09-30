import board
import busio
import usb_cdc

# Инициализация UART на пинах 0 (TX) и 1 (RX) со стандартной скоростью камеры
uart = busio.UART(board.GP0, board.GP1, baudrate=115200)

# Подключение ко второму COM-порту (data)
serial = usb_cdc.data

while True:
    # Перехват текста с компьютера и отправка в камеру
    if serial and serial.in_waiting > 0:
        uart.write(serial.read(serial.in_waiting))
        
    # Перехват текста из камеры и вывод на экран компьютера
    if uart.in_waiting > 0:
        serial.write(uart.read(uart.in_waiting))