import usb_cdc

# Включаем консоль (первый порт) и порт данных (второй порт)
usb_cdc.enable(console=True, data=True)