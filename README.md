## ⚠️ Prerequisites & Hardware Hookup (Требования к железу)

To execute the commands and achieve root access, you **must physically solder to the camera's UART pins** (TX, RX, GND) to monitor the boot process, interrupt U-Boot, and interact with the minimal shell.

* **UART Connection:** Connect the camera's TX/RX lines to a USB-to-UART adapter or use a custom microcontroller setup (such as a **Waveshare RP2040-Zero**).
* **RP2040-Zero Automation:** In this repository, you will find separate script files (`code.py` / firmware) configured for the RP2040-Zero to handle automated serial interaction, injection, or peripheral control.
* 
#You can download the patched camera binary from the project's releases.
# FH8616-IP-Camera-Root-Access
Full root access, persistence, AP mode, and RTSP stream configuration for Fullhan FH8616 based IP cameras (QN-L23PA0900, gc2053).

Research, root persistence guide, and local streaming configuration for budget IP cameras based on the **Fullhan FH8616** SoC.

## 📌 Hardware Specifications (Аппаратная база)
* **SoC:** Fullhan FH8616
* **Sensor:** GalaxyCore GC2053 (MIPI) (`gc2053_mipi`)
* **Wi-Fi Module:** Broadcom BCM4330 (SDIO)
* **Model Name / Prodid:** QN-L23PA0900 / PYNWN-01
* **Firmware Version:** 20231219.1909 (SDK: FH8616_IPC_V1.0.0_20230815)

---

## 🛠 Features & Solutions (Что сделано)
1. **Permanent Root Access:** Bypassing RAM limitations and saving persistent `root` shadow hashes to the `jffs2` writable `userdata` partition (`/app/userdata/shadow`).
2. **Wi-Fi AP Mode:** Forcing Access Point (AP) mode via `wifi_mode.sh` and `hostapd` (`192.168.55.1`) without factory cloud restrictions.
3. **Local RTSP Streaming:** Accessing the H.264 video feed locally via VLC or `go2rtc` (`rtsp://<camera_ip>:8554/stream0` or `/live/ch0`).
4. **Cloud Isolation:** Steps to block telemetry and cloud watchdog (`noodles`) for pure local operation.

---

## 🚀 Quick Guide: Persistent Root (Как закрепить рут-доступ)

1. Boot into minimal shell (`rdinit=/bin/sh`) or use your exploit method.
2. Mount system and data partitions:
# 1. Монтируем базовые виртуальные файловые системы
```sh
mount -t proc proc /proc
```
```
mount -t sysfs none /sys
```
```
mount -t ramfs ramfs /home
```
# 2. Создаем узлы устройств и инициализируем менеджер устройств
```
mdev -s
```
# 3. Запускаем штатный скрипт монтирования разделов прошивки (/app, /app/userdata, /app/res)
```sh
/etc/init.d/S02init_rootfs
```
# 4. Экспортируем системные пути и переменные окружения
```sh
export PATH=/bin:/sbin:/app/bin:/app/abin:/app:/usr/bin
```
```
export LD_LIBRARY_PATH=/lib:/usr/lib:/app/lib
```
Шаг 2. Смена пароля суперпользователя (root)
Измените пароль для учетной записи root с помощью стандартной утилиты:

```sh
passwd
```
```
root
```
Проверьте текущий сгенерированный хэш пароля в файле /etc/shadow:

```sh
cat /etc/shadow
```
Вы увидите строку вида root:Ваш_Хэш:0:0:99999:7:::.

Шаг 3. Закрепление пароля на энергонезависимом разделе (Persistence)
В штатной прошивке файл /etc находится в оперативной памяти (RAM) и пересоздается при каждом включении. Загрузочный скрипт /app/app_shadow.sh проверяет наличие файла паролей на постоянном разделе флеш-памяти (/app/userdata, смонтированном с jffs2) и применяет его.

Чтобы пароль не сбрасывался после перезагрузки:
```sh
cp -f /etc/shadow /app/userdata/shadow
```
Принудительно сбросьте буферы ввода-вывода на флеш-память:
```
sync
```

Проверьте, что файл успешно записался в постоянную память:
```
cat /app/userdata/shadow
```
Шаг 4. Проверка работы автозагрузки и перезагрузка
Проверьте правильность отработки скрипта восстановления паролей:

```
/app/app_shadow.sh
```
```
cat /etc/shadow
```
Если хэш root в /etc/shadow совпал с файлом в userdata, значит механизм автоприменения настроен верно.

Выполните сохранение и перезагрузку устройства в штатный режим:

```
sync
```
```
reboot -f
```
RTSP Streaming Info
Port: 8554

Default DB Credentials: admin / admin123456

Streams:

Main (1280x720): rtsp://admin:admin123456@<ip>:8554/stream0 or /live/ch0
or
rtsp://admin:admin123456@192.168.xxx.xxx:8554/profile0
