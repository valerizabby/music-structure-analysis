# TODO 
- из датасета BPS сделать 
1) аудио датасет 
2) датасет с предсказаниями вида (массив boundaries в сенкудах)
- Собрать метрики по всем методам и попробовать прогнать их на датасете
- BPS датасет - fluidsynth ?? прогнать весь

- symbolic предсказания в каждый файл
- msaf предсказания в каждый файл
- ruptures (?) анализ локтей


- преза: практическая работа <- показать на одном файле или на нескольких разных - mid с разметкой 
- 


# Methods and datasets

Метрика `F1-score`

| Method | BPS | SWD |
|----------|----------|----------|
| G-PELT    | 0.2137 (1 beat) / 0.3224 (1 bar)   | 0.3455 (1 beat) / 0.5640 (1 bar)   |
| ruptures   | Cell 5   | Cell 6   |
| msaf  | Cell 8   | Cell 9   |


# Tool for segmentation

```
├── app                 # директория приложения
    ├── data/           # данные с эндопинта
    ├── resources/      # html страницы
    ├── service/        # логика применения модели
    ├── static/         
        ├── Image       # картинки, отдаваемые моделью (SSM)
    ├── templates/      # html ответ картинкой 
    ├── utils/          # утилиты для работы со String
    └── app.py          # само приложение
```
# Segmentation model
## Symbolic Music Structure Analysis

[🌹 cтатья](https://arxiv.org/abs/2303.13881)

[🌹 гитхаб](https://github.com/carlosholivan/symbolic-music-structure-analysis)

### 📚 идея статьи

MIR - Music Information Retrieval - хотим сегментировать музыкальную структуру. Предложено 3 алгоритма, два их них
основаны на графах. 
Музыка кодируется в граф, граф в матрицу инцидентности, матрица в кривую новизны (novelty curve), а к кривой
применяются changepoint detection алгоритмы. По мнению авторов, дополнительного feature extraction из музыки не требуется (точка роста?)

## 💎 окружение
- клонируем репозиторий 

    ```bash
    git clone https://github.com/carlosholivan/symbolic-music-structure-analysis.git
    ```
- python version >= 3.9
- musicaiz version 0.1.0

  ```bash
  pip install musicaiz==0.1.0
  ```

## 💎 структура кода

- `bps_midi.py`: конвертирует BPS notes.csv файлы в MIDI файлы ✅
  
- `graph_figure1.py`: создает рисунок с BPS-файлом, в котором показана кривая новизны и матрицы инцидентности графа с аннотациями структуры и предсказаниями ✅

- `figure_ssm.py`: создает рисунок с BPS-файлом, в котором показаны кандидаты на границу и SSM с кривой новизны для Norm алгоритма (в 12 строке поменять путь до файла BPS_FH_Dataset на свой) ✅

- `dataset_analysis.py`: аналитика SWD и BPS датасетов (в 12 строке поменять путь до файла BPS_FH_Dataset на свой) ✅

- `audio_segmentation.py`: end2end сегментация через beattracking в аудио домене (.ogg) 


## 💎 важные папки

- BPS_FH_Dataset - датасет с миди из оригинального репозитория

- MIDIs - файлы которые я притащила для тестов

# Оценка качества
## Метрики

Для оценки качества сегментации используется библиотека `mir_eval`
```bash
    pip install mir_eval
```

## References
<a id="1">[1]</a> 
Carlos Hernandez-Olivan and Sonia Rubio Llamas and Jose R. Beltran. 2023
Symbolic Music Structure Analysis with Graph Representations and Changepoint Detection Methods

