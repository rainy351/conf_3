# Парсер Командной Строки

Этот инструмент командной строки предназначен для преобразования XML-конфигурационных файлов в кастомный формат, используя учебный конфигурационный язык. Он позволяет объявлять константы, использовать их в выражениях и выводить текст.

## Особенности

- **Поддержка комментариев:**
  - Однострочные комментарии: `NB. Это однострочный комментарий`
  - Многострочные комментарии: `{{!-- Это многострочный комментарий --}}`
- **Массивы:**
  - Синтаксис: `(значение значение значение ...)`
  - Поддерживает вложенные массивы: `( (1 2) (3 4) )`
- **Имена:**
  - Состоят из букв, цифр и символа подчеркивания, начинаются с буквы или символа подчеркивания: `[_a-zA-Z][_a-zA-Z0-9]*`
- **Значения:**
  - Числа (целые и с плавающей точкой).
  - Массивы.
  - Строки.
- **Объявление констант:**
  - Синтаксис: `значение -> имя;` в виде XML атрибутов `<constant name="имя" value="значение"/>`
- **Вычисление констант:**
  - Синтаксис: `@{имя}`
  - Значения констант подставляются в текст и выражения.

## Использование

### Запуск

Для запуска инструмента используется следующая команда:

```bash
python config_parser.py <путь_к_xml_файлу>
```

- `<путь_к_xml_файлу>`: Путь к входному XML-файлу конфигурации.

### Пример XML-конфигурации

```xml
<config>
    {{!-- Configuration for a web server --}}

    <constant name="http_port" value="80"/>
    <constant name="https_port" value="443"/>
    <constant name="server_address" value="127.001"/>
    <constant name="max_connections" value="100"/>
    <constant name="allowed_hosts" value="(localhost 127.0.0.1 example.com)"/>

    <text>
        NB. Basic Web Server Configuration
        Server Address: @{server_address}
    </text>

    <expression>
        HTTP Port: @{http_port}
    </expression>

    <expression>
        HTTPS Port: @{https_port}
    </expression>

    <expression>
        Maximum Connections: @{max_connections}
    </expression>

    <expression>
        Allowed Hosts: @{allowed_hosts}
    </expression>

    <nested>
      <text>
        NB. Server Options
        Keep-Alive timeout: 60
      </text>
    </nested>

    <constant name="error_log" value="/var/log/webserver/error.log"/>
     <text>
         Error Log Path: @{error_log}
     </text>

</config>
```

### Вывод

Инструмент выводит результат обработки XML-конфигурации в стандартный вывод.

```
Server Address: 127.001

HTTP Port: 80

HTTPS Port: 443

Maximum Connections: 100

Allowed Hosts: ['localhost', '127.0.0.1', 'example.com']

Keep-Alive timeout: 60


Error Log Path: /var/log/webserver/error.log
```

## Структура проекта

- **`main.py`**: Основной скрипт, обрабатывающий аргументы командной строки и запускающий процесс преобразования.
- **`conf_lang.py`**: Содержит функцию `parse_config_string`, реализующую логику разбора и преобразования XML-конфигурации.

## Зависимости

- Python 3.6+
- Стандартная библиотека Python (не нужны внешние библиотеки)

## Обработка ошибок

Инструмент обрабатывает следующие ошибки:

- Ошибки разбора XML.
- Ошибки разбора констант (неверный формат значения).
- Ошибки в выражениях (неопределенная константа).
- Ошибки в имени константы (неверный формат).
- Неверно указанный путь к файлу.

## Дальнейшее развитие

- Расширение языка для поддержки функций, условных выражений.
- Более продвинутая обработка ошибок с информацией о номере строки.
- Оптимизация производительности при обработке больших файлов.

## Примеры конфигураций

### Конфигурация веб-сервера

```xml
<config>
    {{!-- Configuration for a web server --}}

    <constant name="http_port" value="80"/>
    <constant name="https_port" value="443"/>
    <constant name="server_address" value="127.0.0.1"/>
    <constant name="max_connections" value="100"/>
    <constant name="allowed_hosts" value="(localhost 127.0.0.1 example.com)"/>

    <text>
        NB. Basic Web Server Configuration
        Server Address: @{server_address}
    </text>

    <expression>
        HTTP Port: @{http_port}
    </expression>

    <expression>
        HTTPS Port: @{https_port}
    </expression>

    <expression>
        Maximum Connections: @{max_connections}
    </expression>

    <expression>
        Allowed Hosts: @{allowed_hosts}
    </expression>

    <nested>
      <text>
        NB. Server Options
        Keep-Alive timeout: 60
      </text>
    </nested>

    <constant name="error_log" value="/var/log/webserver/error.log"/>
     <text>
         Error Log Path: @{error_log}
     </text>

</config>
```

### Конфигурация системы обработки данных

```xml
<config>
  {{!-- Configuration for a data processing system --}}
  <constant name="input_data_path" value="/data/input/"/>
  <constant name="output_data_path" value="/data/output/"/>
  <constant name="log_file" value="/var/log/data_processor.log"/>
  <constant name="batch_size" value="1000"/>
  <constant name="data_sources" value="(source1 source2 source3)"/>
  <constant name="processing_steps" value="(step1 step2 step3)"/>

    <text>
        NB. Data Processing Configuration
        Input Data Path: @{input_data_path}
    </text>

  <expression>
        Output Data Path: @{output_data_path}
  </expression>

  <expression>
        Log File: @{log_file}
  </expression>

  <expression>
        Batch Size: @{batch_size}
  </expression>

    <expression>
        Data Sources: @{data_sources}
    </expression>

    <expression>
      Processing Steps: @{processing_steps}
    </expression>


  <nested>
    <text>
      NB. Advanced options
      Use cache: True
    </text>
  </nested>

    <constant name="retry_attempts" value="3"/>
    <text>
       Retry Attempts: @{retry_attempts}
    </text>
</config>
```
