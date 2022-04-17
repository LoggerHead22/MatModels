# RuPython with Morphology 

### Описание скриптов:
	 
  * transpiler.py - основной функционал
  * main.py - command line interface
  * daemon.py - real-time преобразование кода. (Динамически интепретирует rupython в python в консоле).
  * test.py - файл с набором тестов
  * rupython - интерпретатор ru-питона
  * ide - запуск daemon.py
  
### Установка среды

```console
>conda create -m mat_models python=3.9
>conda activate mat_models
>pip install -r requirements.txt
```

### Пример запука команд

	> ide test_script.rupy
	> rupython test_script.rupy
	> python test.py #запуск тестов
  
### Сопоставление ключевых слов

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

###### Встроенные функции 
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

###### Некоторые методы и модули   
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

###### Некоторые магические методы 

| RuPython           | Python              |
|--------------------|---------------------|
|\_\_инициализация__   | \_\_init__            |
|\_\_представление__   | \_\_repr__            |
|\_\_сложение__        | \_\_add__             |


### Примеры тестовых программ