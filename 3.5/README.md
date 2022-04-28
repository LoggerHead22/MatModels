# RuPython with Morphology 

### Описание скриптов / Description of scripts:

RU:

  * transpiler.py - основной функционал
  * main.py - command line interface
  * daemon.py - real-time преобразование кода. (Динамически интепретирует rupython в python в консоле).
  * test.py - файл с набором тестов
  * rupython - интерпретатор ru-питона
  * ide - запуск daemon.py

EN:

 * transpiler.py - basic functionality
 * main.py - command line interface
 * daemon.py - real-time code conversion. (Dynamically interprets rupython into python in the console).
 * test.py - a file with a set of tests
 * rupython - ru-python interpreter
 * ide launch daemon.py

### Установка среды / Installing the Environment

```console
>conda create -m mat_models python=3.9
>conda activate mat_models
>pip install -r requirements.txt
```

### Пример запука команд / Example of running commands

	> ide test_script.rupy
	> rupython test_script.rupy
	> python test.py #запуск тестов

### Фичи RuPython / RuPython Features

RU:

Для грамматически более правильных конструкций, введён синтаксис `attribute@object`, эквивалентный `object.attribute`

Например, `имя@человека` транслируется в `human.name`.

Для ускорения транляции введен кэш, который сохраняет переводы слов. Это уменьшает число дорогостоящих запросов в google-translator.

EN:

For grammatically more correct constructions, the syntax `attribute@object` is introduced, equivalent to `object.attribute`

For example,  `имя@человека` translates to `human.name `.

To speed up translation, a cache has been introduced that saves translations of words. This reduces the number of expensive queries in google-translator.

### Примеры тестовых программ / Examples of test programs

![alt text](https://github.com/LoggerHead22/MatModels/blob/main/3.5/test_images/Screenshot_1.png?raw=true)

![alt text](https://github.com/LoggerHead22/MatModels/blob/main/3.5/test_images/Screenshot_3.png?raw=true)

![alt text](https://github.com/LoggerHead22/MatModels/blob/main/3.5/test_images/Screenshot_4.png?raw=true)

![alt text](https://github.com/LoggerHead22/MatModels/blob/main/3.5/test_images/Screenshot_7.png?raw=true)

Другие примеры можно найти в `test.py`

Other examples can be found in `test.py `

### Сопоставление ключевых слов / Keyword Matching

| RuPython           | Python              |
|--------------------|---------------------|
|Ложь                | False               |
|Ничего              | None                |
|Истина              | True                |
|и                   | and                 |
|как                 | as                  |
|утверждать          | assert              |
|асинхронный         | async               |
|в_ожидании          | await               |
|прервать            | break               |
|класс               | class               |
|продолжить          | continue            |
|определить          | def                 |
|удалить             | del                 |
|иначе_если          | elif                |
|иначе               | else                |
|ожидать             | except              |
|наконец             | finally             |
|для                 | for                 |
|из                  | from                |
|глобальный          | global              |
|если                | if                  |
|импортировать       | import              |
|в                   | in                  |
|является            | is                  |
|лямбда              | lambda              |
|нелокальный         | nonlocal            |
|не                  | not                 |
|или                 | or                  |
|пропустить          | pass                |
|вызвать             | raise               |
|вернуть             | return              |
|попытаться          | try                 |
|пока                | while               |
|с                   | with                |
|произвести          | yield               |

###### Встроенные функции / Built-in functions
| RuPython           | Python              |
|--------------------|---------------------|
|модуль              | abs                 |
|все                 | all                 |
|любой               | any                 |
|_2сс                | bin                 |
|булево              | bool                |
|массив_байтов       | bytearray           |
|байты               | bytes               |
|вызываемый          | callable            |
|знаковый_код        | chr                 |
|скомпилировать      | compile             |
|комплексное         | complex             |
|словарь             | dict                |
|список_атрибутов    | dir                 |
|перечисление        | enumerate           |
|выполнить           | eval                |
|исполнить           | exec                |
|фильтровать         | filter              |
|плавающее           | float               |
|форматировать       | format              |
|хэш                 | hash                |
|помощь              | help                |
|_16сс               | hex                 |
|идентификатор       | id                  |
|ввести              | input               |
|целое               | int                 |
|это_экземпляр       | isinstance          |
|это_подкласс        | issubclass          |
|список              | list                |
|отобразить          | map                 |
|максимум            | max                 |
|минимум             | min                 |
|следующий           | next                |
|_8сс                | oct                 |
|открыть             | open                |
|числовой_код        | ord                 |
|степень             | pow                 |
|вывести             | print               |
|представление       | repr                |
|перевернутый        | reversed            |
|округлить           | round               |
|множество           | set                 |
|ломтик              | slice               |
|отсортированный     | sorted              |
|строка              | str                 |
|сумма               | sum                 |
|родитель            | super               |
|кортеж              | tuple               |
|тип                 | type                |
|переменные          | vars                |
|объединить          | zip                 |

###### Некоторые методы и модули / Some methods and modules
| RuPython           | Python              |
|--------------------|---------------------|
|привесить           | append              |
|длина               | len                 |
|в_нижнем_регистр    | lower               |
|порезать            | strip               |
|порезанный          | strip               |
|коллекции           | collections         |
|словарь_по_умолчание| defaultdict         |
|значения            | values              |

###### Некоторые магические методы / Some magical methods

| RuPython           | Python              |
|--------------------|---------------------|
|\_\_инициализация__   | \_\_init__            |
|\_\_представление__   | \_\_repr__            |
|\_\_сложение__        | \_\_add__             |


