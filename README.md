# Symbolic Music Structure Analysis

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

Спросить MIDI трек на русском (?)
