# Отчёт о лицензионном соответствии (License Compliance Audit)

**Проект:** `random_vISA`  
**Дата аудита:** 14 августа 2026 г.  
**Основная лицензия проекта:** [MIT License](file:///Volumes/External/Code/random_vISA/LICENSE)  
**Статус комплаенса:** ✅ **Полностью совместимо (Fully Compliant)**

---

## 1. Сводная матрица лицензий

| Компонент / Зависимость | Тип | Лицензия | Назначение | Совместимость с MIT |
| :--- | :---: | :---: | :--- | :---: |
| **`random_vISA` (core)** | Core Codebase | **MIT** | Генератор V-ISA, парсеры Sail, эмиттеры | ✅ Базовая |
| **`third_party/pydrofoil`** | Git Submodule | **MIT** | JIT/трассирующий бэкенд Sail IR | ✅ 100% совместима |
| **`third_party/ArchC`** (инструменты) | Git Submodule | **GPL-2.0** | Компилятор ADL `acsim`, `accsim` | ✅ Build-time tool |
| **`third_party/ArchC`** (`aclib`) | Runtime Library | **LGPL-2.1** | Рантайм-библиотека `libarchc.a` | ✅ Динамическая/статическая линковка |
| **SystemC (Accellera)** | Системная либа | **Apache-2.0** | Ядро симуляции аппаратуры | ✅ 100% совместима |
| **`jinja2`** | Python dep | **BSD-3-Clause** | Шаблонизация C++, C11, SystemC | ✅ Пермиссивная |
| **`pydantic`** | Python dep | **MIT** | Валидация доменных инвариантов | ✅ Пермиссивная |
| **`rich`** | Python dep | **MIT** | CLI визуализация и форматирование | ✅ Пермиссивная |
| **`antlr4-python3-runtime`** | Python dep | **BSD-3-Clause** | ANTLR4 AST парсер грамматик Sail/C/C++ | ✅ Пермиссивная |
| **Sail Architecture Language** | Спецификация | **BSD-2-Clause** | Формат описания семантики ISA | ✅ Пермиссивная |

---

## 2. Анализ зависимостей по категориям

### 2.1. Python Runtime Dependencies (`pyproject.toml`)
Все прямые зависимости проекта (`jinja2`, `pydantic`, `rich`, `antlr4-python3-runtime`) имеют пермиссивные лицензии (**MIT** и **BSD-3-Clause**). 
- **Требования:** Сохранение копирайтов при распространении исходного кода.
- **Ограничения на коммерческое использование:** Отсутствуют.
- **Копилефт-риски:** Отсутствуют.

### 2.2. Субмодуль `third_party/pydrofoil`
- **Лицензия:** [MIT License](file:///Volumes/External/Code/random_vISA/third_party/pydrofoil/LICENSE) (Copyright (c) 2022 Carl Friedrich Bolz-Tereick).
- **Статус:** Полная взаимная совместимость. Код Pydrofoil может беспрепятственно встраиваться, модифицироваться и распространяться как в открытом, так и в проприетарном ПО.

### 2.3. Субмодуль `third_party/ArchC` (Архитектурный фреймворк)
ArchC имеет раздельное лицензирование компонентов:
1. **GPL-2.0 ([`COPYING`](file:///Volumes/External/Code/random_vISA/third_party/ArchC/COPYING))** — утилиты генерации (`acsim`, `accsim`, `actsim`).
   - *Анализ риска:* `acsim` используется исключительно как утилита командной строки на этапе сборки (build-time compiler). По аналогии с GCC или Bison, факт генерации C++ кода утилитой под GPL-2.0 **не накладывает** GPL-ограничений на сгенерированный код (`.ac`, `.isa`, `_isa.cpp`, `main.cpp`).
2. **LGPL-2.1 ([`COPYING.LIB`](file:///Volumes/External/Code/random_vISA/third_party/ArchC/COPYING.LIB))** — библиотека времени исполнения `aclib` (`libarchc.a`).
   - *Анализ риска:* Линковка симулятора `*.x` с `libarchc.a` подпадает под условия LGPL-2.1. Разрешается использование с закрытым/коммерческим или MIT-кодом, если пользователю предоставлена возможность перелинковки с обновленной версией библиотеки `libarchc.a` (или предоставлен исходный код самой библиотеки).

### 2.4. SystemC (Accellera Systems Initiative)
- **Лицензия:** **Apache License, Version 2.0**.
- **Совместимость:** Apache-2.0 полностью совместима с MIT и LGPL-2.1. Распространение бинарных файлов симуляторов требует включения текста лицензии Apache-2.0 и атрибуции Accellera.

---

## 3. Лицензионный статус сгенерированного кода (Generated Artifacts)

| Целевой бэкенд | Сгенерированные файлы | Внешние зависимости рантайма | Лицензионный статус результата |
| :--- | :--- | :--- | :--- |
| **C++20 SIMD Emulator** | `visa_test_runner`, `.cpp`, `.hpp` | Стандартная библиотека C++20 (`<vector>`, `<array>`) | **Unrestricted / MIT** (zero runtime deps) |
| **Pure C11 Micro-Emulator** | `visa_c_runner`, `.c`, `.h` | Стандартная библиотека C11 (`<stdint.h>`, `<stdio.h>`) | **Unrestricted / MIT** (zero runtime deps) |
| **Pydrofoil Python / VBC** | `pydrofoil_*.py`, `*.vbc` | `pydrofoil` runtime | **MIT** |
| **ArchC SystemC Simulator** | `*.ac`, `*.isa`, `*_isa.cpp`, `*.x` | `libarchc.a` (LGPL-2.1) + `libsystemc` (Apache-2.0) | Сгенерированный код: **MIT**<br>Скомпилированный бинарник: **LGPL-2.1 / Apache-2.0** |

---

## 4. Проверка на отсутствие нежелательного копилефта (Infection Check)

1. **PyQt6 в окружении:**
   - В окружении разработки обнаружен пакет `PyQt6` (**GPL-3.0-only**), используемый плагином `pytest-qt`.
   - *Проверка исходного кода:* Поиск по всему проекту `random_visa/` подтвердил **полное отсутствие импортов Qt/PyQt6**. Ядро и CLI полностью свободны от GPL-3 зависимостей.
2. **Патентные риски:**
   - Векторные инструкции синтезируются на базе открытого стандарта RISC-V Vector "V" Extension (v1.0), семантика которого стандартизирована RISC-V International и свободна от роялти.

---

## 5. Рекомендации для распространения и дистрибьюции

1. **При распространении исходного кода `random_vISA`**:
   - Сохранять файл `LICENSE` (MIT) в корне репозитория.
   - Сохранять файлы лицензий в субмодулях `third_party/pydrofoil/LICENSE` и `third_party/ArchC/COPYING*`.
2. **При поставке скомпилированных симуляторов ArchC (`.x`)**:
   - Прикладывать уведомление о включении SystemC (Apache-2.0) и ArchC aclib (LGPL-2.1).
3. **При интеграции C++20 или C11 эмуляторов в закрытые проекты**:
   - Ограничения отсутствуют — сгенерированный C++20 / C11 код не содержит библиотечных зависимостей ArchC или Pydrofoil и может свободно лицензироваться заказчиком.
