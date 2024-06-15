# Music Structure Analysis
## 💎 окружение
- python version >= 3.9
- musicaiz version 0.1.0

  ```bash
  pip install musicaiz==0.1.0
  ```

## 💎 структура кода
```
├── music-structure-analysis                
    ├── data/
        ├── BPS_FH_Dataset
        ├── RussianPop
        └── Schubert_Winterreise_Dataset_v2-0
    ├── SMSA/      
        ├── audio_domain/
            └── AudioPelt
        ├── symbolic_domain/
            └── SymbolicPelt       
        ├── Dataloader
        ├── Dataparser
        └── Segmenter
    ├── experiment        
    └── comparison          
```

## 💎 важные папки и методы

- `experiment.py`: содержит метод для обхода датасета и применения к нему заданного алгоритма
```bash
def dataset_bypass(dataset_abs_path, algo, input_ext, output_ext, to_save=True):
    """
        dataset_abs_path -- абсолютный путь до датасета
        algo -- алгоритм, у которого определен метод predict
        input_ext -- расширение входных аудио файлов
        output_ext -- название, куда сохраняем ответы
        to_save -- сохранять предсказания или нет (по умолчанию true)
    """
```
- `AudioPelt()`: класс для предсказания точек изменения в аудио домене (расширение mp3). Перед применением алгоритмов детекции точек изменения, класс создает темпограмму аудио записи. Cодержит методы `fit` и `predict`. Для инициализации необходимо определить параметры:
  - algo = [kernel, pelt]
  - mode = [gt, hard] -- берем количество точек изменения из разметки или hard-coded (для алгоритма kernel)
- `SymbolicPelt()`: класс для предсказания точек изменения в символьном домене (расширение mid). Перед применением алгоритмов создается кривая новезны. Для инициализации:
  - algo = [kernel, pelt]
  - mode = [gt, hard] -- берем количество точек изменения из разметки или hard-coded (для алгоритма kernel)


# Оценка качества
## Метрики

Для сравнения алгоритмов была выбрана метрика f1-score.

tolerance = 10 sec

| Dataset  | SymbolicPelt | AudioPelt(kernel, gt) |  AudioPelt(kernel, hard) |
|----------|--------------|-----------------------|--------------------------|
|   BPS    |    0.417     | 0.503                 | 0.459                    |
|  RPM     | 0.575        | 0.598                 | 0.597                    |


## Расшифровка названий предсказаний
- BPS: 
  - gt_mid - разметка
  - ruptures_pred_11 - AudioDomain(algo=kernel, mode=hard)
  - ruptures_pred - AudioDomain(algo=kernel, mode=gt)
  - symbolic_pred - SymbolicDomain(algo=pelt)
  - symbolic_pred_kernel_gt - SymbolicDomain(algo=kernel, mode=gt)
  - symbolic_pred_kernel_hard - SymbolicDomain(algo=kernel, mode=hard)

## References
<a id="1">[1]</a> 
Carlos Hernandez-Olivan and Sonia Rubio Llamas and Jose R. Beltran. 2023
Symbolic Music Structure Analysis with Graph Representations and Changepoint Detection Methods



