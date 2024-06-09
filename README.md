todo:
- refactor readme

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

# Оценка качества
## Метрики

Для сравнения алгоритмов была выбрана метрика f1-score.

tolerance = 10 sec

| Dataset  | SymbolicPelt | AudioPelt(kernel, gt) |  AudioPelt(kernel, hard) |
|----------|--------------|-----------------------|--------------------------|
|   BPS    |    0.417     | 0.503                 | 0.459                    |
|  RPM     | 0.575        | 0.598                 | 0.597                    |

## References
<a id="1">[1]</a> 
Carlos Hernandez-Olivan and Sonia Rubio Llamas and Jose R. Beltran. 2023
Symbolic Music Structure Analysis with Graph Representations and Changepoint Detection Methods



