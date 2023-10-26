#!/bin/bash
export PATH=/home/scrapping/NebesniySvet/bin:$PATH
export VIRTUAL_ENV=/home/scrapping/NebesniySvet
# Путь к активации виртуальной среды
path_to_activate="/home/scrapping/NebesniySvet/bin/activate"

# Активировать виртуальную среду
source "$path_to_activate"
echo "all good"
# Путь к вашему основному скрипту
path_to_script="/home/scrapping/NebesniySvet/marketplace_yandex-inventory-management.v2/main.py"

# Запустить ваш основной скрипт
python3 "$path_to_script"
