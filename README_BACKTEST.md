# Як запустити бектестінг криптовалютної торгової стратегії

Цей README.md файл містить інструкцію, як запустити бектестінг криптовалютної торгової стратегії на прикладі скрипта backtest.py.

## Інструкції

1. **Завантажте дані з файлу історичних свічок.**

```python3
dataframe = pd.read_csv(Path(root, "data", "test_dataBTCUSDT_1m_09_10_23.csv"))
```

2. **Створіть індикатор S&A R Filter і застосуйте його до даних.**

```python3
sna_indicator = SnATradeIndicator(dataframe, source="close")
sna_data = sna_indicator.apply_indicator()
```

3. **Отримайте дані, оброблені індикатором.**

```python
r_filter = sna_data["range_filter"]
h_target = sna_data["high_band"]
l_target = sna_data["low_band"]
```

4. **Створіть драбину об'ємів.**

```python
volumes = [10, 20, 40, 80, 160, 320, 640, 1280, 2560]
```

5. **Створіть стратегію.**

```python
strategy = Strategy(
    indicators=[SnATradeIndicator, B2TradeIndicator],
    indicator_settings={
        "SnATradeIndicator": {"source": "hlc3"},
        "B2TradeIndicator": {"source": "another_source", "another_source": r_filter},
    },
    price_settings={},
)
```

6. **Створіть бектестер.**

```python
backtester = Backtester(strategy, volumes=volumes)
```

7. **Запустіть бектестінг.**

```python
backtester.backtest(dataframe)
```

## Рекомендації

* Для отримання більш точних результатів бектестінгу рекомендується використовувати більшу кількість даних.
* Також рекомендується використовувати різні налаштування стратегії для оцінки її стійкості до зміни умов ринку.

