# Satellites decoder
[![](https://img.shields.io/badge/english-blue)](https://github.com/baskiton/SatsDecoder/blob/main/README.md)
[![](https://img.shields.io/badge/русский-blue)](https://github.com/baskiton/SatsDecoder/blob/main/README.ru.md)

![](https://img.shields.io/github/v/release/baskiton/SatsDecoder?label=stable)
![](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/baskiton/7270038ca73e8e5f1acea6280cc8a416/raw/satsdecoder-pre.json)  
![](https://img.shields.io/github/downloads/baskiton/SatsDecoder/total?label=downloads%40total)
![](https://img.shields.io/github/downloads/baskiton/SatsDecoder/latest/total)

Декодер телеметрии и изображений радиолюбительских спутников различных платформ

Для начала, скачайте, установите и запустите саундмодем  
https://r4uab.ru/settings-soundmodem/  
* geoscan: [1](https://r4uab.ru/program/modem/geoscan.zip)
* usp: [1](https://edu.sputnix.ru/assets/files/hs_soundmodem-4c5cea0c92a6d1e2d686662c6b3115a8.zip), [2](http://uz7.ho.ua/gmskusp.zip)
* lucky-7: [1](http://uz7.ho.ua/lucky7.zip)
* other: [1](http://uz7.ho.ua/packetradio.htm)

Чтобы начать декодирование, запустите SatsDecoder, выберите вкладку нужного протокола (или добавьте новую вкладку) и нажмите кнопку `Connect`.
Воспроизведите FM-демодулированный сигнал и ожидайте результата

#### Настройки
* `Out Dir` Директория для сохранения изображений и телеметрии
* `Server` Хостнейм или IP-адрес саундмодема
* `Port` порт саундмодема (смотри в File -> Devices -> AGWPE Server Port)
* `Merge mode` Склейка - когда включена, все новые данные изображений будут помещаться в один файл (кроме случаев, когда программа на 100% уверена, что это новый файл)
* `New Image` Принудительно создать новое изображение


#### Горячие клавиши
* `Ctrl-Q` Выход
* `F1` Показать окно "О программе", проверить, доступны ли новые версии


#### Протоколы
В настоящее время поддерживаются следующие протоколы:
* `GEOSCAN` - [Geoscan platform](https://download.geoscan.aero/site-files/%D0%9F%D1%80%D0%BE%D1%82%D0%BE%D0%BA%D0%BE%D0%BB%20%D0%BF%D0%B5%D1%80%D0%B5%D0%B4%D0%B0%D1%87%D0%B8%20%D1%82%D0%B5%D0%BB%D0%B5%D0%BC%D0%B5%D1%82%D1%80%D0%B8%D0%B8.pdf)
* `USP` - [Unified SPUTNIX protocol](https://sputnix.ru/tpl/docs/amateurs/%D0%9E%D0%BF%D0%B8%D1%81%D0%B0%D0%BD%D0%B8%D0%B5%20%D0%BF%D1%80%D0%BE%D1%82%D0%BE%D0%BA%D0%BE%D0%BB%D0%B0%20USP%20v1.04.pdf)
* `AX.25`
* `CSP` - [Cubesat Space Protocol](https://github.com/libcsp/libcsp)
* `CSUM` - [University Space Center of Montpellier platform (CSUM)](http://csu.edu.umontpellier.fr/)
* `CubeBel-2`
* `D-Star ONE` - [D-Star ONE Protocol](https://web.archive.org/web/20190807184852/http://www.d-star.one/downloads/D-Star%20ONE%20telemetry%20frame%20format.pdf)
* `CitGardens-02` - [CIT Gardens-02 project](https://sites.google.com/view/gardens-02/english_ver/home)
* `GreenCube` - [GreenCube](https://www.s5lab.space/index.php/decoding-ledsat-2/)
* `Ledsat` - [LEDSAT](https://www.s5lab.space/index.php/decoding-ledsat/)
* `Lucky-7` - [Lucky-7 Satellite protocol](https://www.lucky7satellite.org/radioamateurs)
* `RoseyCubeSat`
* `SamSat-Ionosphere` - [SamSat-Ion2 beacon structure](https://spaceresearch.ssau.ru/doc/SamSat/SamSat-Ion2/SamSat-Ionosphere-beacon.pdf)
* `SharjahSat`
* `Snuglite` - [SNUGLITE-I beacon structure](https://snuglitecubesat.wixsite.com/website/post/snuglite-beacon-structure)
* `Sonate-2` - [Sonate-2 protocol](https://www.informatik.uni-wuerzburg.de/en/aerospaceinfo/mitarbeiter/kayal/forschungsprojekte/sonate-2/information-for-radio-amateurs/)
* `WTCSimba` - [WildTrackCube-SIMBA](https://www.s5lab.space/index.php/decoding-simba/)
* `RAW` - Сырые данные

#### Источники данных
Различные источники данных доступны в выпадающем меню `Conn`:
* `AGWPE Client` - для соединений с саундмодемами
* `HEX values` - построчное декодирование данных, представленных в 16-ричном виде (HEX)
* `HEX values from files` - то же, что `HEX values`, но из файла
* `TCP Client` - TCP сокет как клиент
* `TCP Server` - TCP сокет как сервер
  * ВНИМАНИЕ!!! Для TCP типов поставщик данных должен отправить следующий заголовок до основных данных:  
    ```C
    struct header {  
        uint32_t len;  // data length
    }
    ```
    Порядок байт: Network (big-endian)
* `KISS files` - из KISS-файлов
* `SatDump frm files` - из SatDump frm файлов (только для AX.25 и Geoscan)

![](doc/Screenshot.jpg)


### Запуск из исходников
Необходим как минимум Python 3.7  
Я рекомендую использовать виртуальное окружение

Установка зависимостей:
```commandline
pip install -r requirements.txt
```

Запуск:
```commandline
python -m SatsDecoder
```


### Сборка из исходников
Необходим как минимум Python 3.7  
Я рекомендую использовать виртуальное окружение

* Pyinstaller
    ```commandline
    pip install -r requirements.txt
    pip install pyinstaller
    pyinstaller -y decoder.spec
    ```

* Nuitka
    ```commandline
    pip install -r requirements.txt
    pip install nuitka
    python -m nuitka python -m nuitka --python-flag=-m --onefile --standalone \
        --assume-yes-for-downloads --output-dir=dist --script-name=SatsDecoder \
        --enable-plugins=tk-inter --windows-icon-from-ico=res/icon.png \
        --include-data-dir=res=res --noinclude-data-files=res/*.txt
    ```

Готовую сборку можно найти в директории `dist`


### Лицензия
SatsDecoder лицензирован как GPL-3.0-or-later. Он содержит код третьих лиц,
который лицензируется GPL-3.0-or-later, но основная кодовая база программы лицензируется как MIT


### Contributing
Вклады в SatsDecoder должны быть лицензированы как MIT.  
Ветка "main" является релизной.  
Новые ветки должны создаваться из ветки "dev".  
Все ПР должны направляться в "dev".  
Код Python должен соответствовать или быть близок к PEP-8.  
