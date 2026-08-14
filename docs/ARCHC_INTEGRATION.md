# ArchC & random_vISA: Руководство по интеграции и верификации

## 1. Введение

[**ArchC**](http://www.archc.org) — это предметно-ориентированный язык описания архитектур (Architecture Description Language, ADL) и открытый фреймворк на базе **SystemC**, разработанный в Институте информатики Университета Кампинас (IC-UNICAMP).

Фреймворк **`random_vISA`** предоставляет полную двустороннюю интеграцию с ArchC:
1. **Генерация моделей ArchC**: Преобразование любой формальной спецификации векторной системы команд (Sail V-ISA) в файлы `.ac` (архитектура), `.isa` (система команд), `_isa.cpp` (поведенческая реализация) и `main.cpp` (SystemC top-level runner).
2. **Аппаратная симуляция SystemC**: Автоматическая сборка через `acsim` и `clang++` с поддержкой SystemC 3.0.2.
3. **Кросс-верификация 4 движков**: Сопоставление результатов выполнения между **C++20 SIMD**, **Pure C11**, **Pydrofoil JIT** и **ArchC SystemC**.

---

## 2. Предварительные требования и окружение

### 2.1. Установка SystemC
На macOS SystemC устанавливается через Homebrew:
```bash
brew install systemc
```
Путь к заголовкам и библиотекам: `/opt/homebrew/opt/systemc`.

### 2.2. Наличие ArchC
Репозиторий ArchC собран и расположен по адресу:
```bash
export ARCHC_PATH=/Volumes/External/Code/ArchC
```

### 2.3. Конфигурация ArchC
ArchC ищет конфигурационный файл в `~/.archc/archc.conf`. Создайте его или скопируйте:
```bash
mkdir -p ~/.archc
cp -f /Volumes/External/Code/ArchC/archc.conf ~/.archc/archc.conf
```

---

## 3. Быстрый старт: Пошаговая инструкция проверки

### Шаг 1: Синтез случайной V-ISA в Sail
Сгенерируйте формальную спецификацию системы команд:
```bash
python3 -m random_visa.adapters.inbound.cli.main synthesize \
  --name "MyVector_ISA" \
  --num-insts 8 \
  --vlen 256 \
  --seed 12345 \
  --out-file "my_vector_isa.sail"
```

### Шаг 2: Генерация и сборка симулятора ArchC SystemC
Скомпилируйте спецификацию `.sail` в проект ArchC SystemC:
```bash
python3 -m random_visa.adapters.inbound.cli.main compile-archc \
  my_vector_isa.sail \
  -o my_archc_sim
```

**Что происходит под капотом:**
1. ANTLR4 парсер `random_vISA` считывает грамматику `my_vector_isa.sail`.
2. Эмиттер генерирует файлы ArchC:
   - `myvector_isa.ac` — ресурсы процессора (`VRB:32`, `XRB:32`, `DM:512M`).
   - `myvector_isa.isa` — форматы и декодер инструкций.
   - `myvector_isa_isa.cpp` — реализация `ac_behavior` для каждой инструкции.
   - `main.cpp` — SystemC точка входа `sc_main` с автоматическим загрузчиком.
   - `build.sh` — скрипт сборки.
3. Запускается генератор `acsim myvector_isa.ac`, создающий SystemC-модули.
4. Выполняется компиляция через `clang++ -std=c++17` с линковкой `libsystemc` и `libarchc.a`.
5. Создается исполняемый бинарник `my_archc_sim/myvector_isa.x`.

---

## 4. Режимы запуска симулятора ArchC

### 4.1. Режим 1: Встроенный тест синтезированных инструкций
Запуск без параметров выполняет тестовый набор всех сгенерированных инструкций в памяти SystemC:
```bash
./my_archc_sim/myvector_isa.x
```
**Пример вывода:**
```text
============================================================
ArchC SystemC Simulator for myvector_isa
WordSize = 32 bits, Num Vector Regs = 32
============================================================

[ArchC] Initializing SystemC Vector Processing Core...
[ArchC] Simulation Starting: myvector_isa
  State initialized: VRB[1] = 10, VRB[2] = 2, XRB[1] = 5
  Loaded 8 synthesized vector instructions into Memory DM.

[ArchC] Starting SystemC Simulation Kernel (sc_start)...
[ArchC] Executed vand_vv_0: v4 = 2 (from vs2=v2[2])
[ArchC] Executed vmax_vx_1: v5 = 5 (from vs2=v2[2])
[ArchC] Executed vmul_vv_2: v6 = 20 (from vs2=v2[2])
...
[ArchC] Simulation Completed: myvector_isa

============================================================
[ArchC SystemC Register State Dump]:
  VRB[0] = 257
  VRB[1] = 10
  VRB[2] = 2
  VRB[4] = 2
  VRB[5] = 5
  VRB[6] = 20
============================================================
ArchC: Simulation statistics
    Number of instructions executed: 9
```

---

### 4.2. Режим 2: Исполнение бинарного байткода (`.vbc`)
Вы можете скомпилировать ассемблер программы в бинарный байткод `.vbc` и передать его симулятору:

1. **Создайте ассемблер `program.asm`:**
```asm
.global _start
_start:
    vand_vv_0 v4, v2, v1
    vmax_vx_1 v5, v2, x1
    vmul_vv_2 v6, v2, v1
```

2. **Скомпилируйте в байткод `.vbc`:**
```bash
python3 -m random_visa.adapters.inbound.cli.main assemble \
  program.asm \
  --spec my_vector_isa.sail \
  -o program.vbc
```

3. **Запустите симуляцию в ArchC SystemC:**
```bash
./my_archc_sim/myvector_isa.x --bin program.vbc
```

---

## 5. Кросс-проверка 4-х эмуляторов (Gold Model Validation)

Для подтверждения эквивалентности выполнения всех четырех реализаций используйте команду:

```bash
# 1. C++20 SIMD Golden Model
./generated_emulator/visa_test_runner

# 2. Pure C11 Embedded Model
./generated_emulator/c11_emulator/visa_c_runner

# 3. Pydrofoil JIT Model
python3 generated_emulator/pydrofoil_emulator/pydrofoil_main.py --bin generated_emulator/program.vbc

# 4. ArchC SystemC Hardware Model
./generated_emulator/archc_emulator/parsed_archc_isa.x --bin generated_emulator/program.vbc
```

### Сравнительная таблица дампов регистров после выполнения `program.vbc`:

| Регистр | C++20 SIMD | Pure C11 | Pydrofoil JIT | ArchC SystemC | Статус |
| :---: | :---: | :---: | :---: | :---: | :---: |
| **`v4`** | `2` | `2` | `2` | `2` | ✅ **Идентично** |
| **`v5`** | `5` | `5` | `5` | `5` | ✅ **Идентично** |
| **`v6`** | `20` | `20` | `20` | `20` | ✅ **Идентично** |
| **`v7`** | `15` | `15` | `15` | `15` | ✅ **Идентично** |

---

## 6. Запуск автоматических тестов

Для проверки всей кодовой базы и тестов генерации ArchC:
```bash
pytest -v tests/unit/test_archc_codegen.py tests/integration/test_cli_commands.py
```
или запуск полного набора:
```bash
pytest -v
```
Все **45 тестов** покрывают генерацию `.ac`, декодеров `.isa`, сборку симулятора `acsim`, компиляцию SystemC и корректность выполнения.

---

## 7. Устранение неполадок (Troubleshooting)

| Проблема | Причина | Решение |
| :--- | :--- | :--- |
| `Could not open archc.conf` | Отсутствует `~/.archc/archc.conf` | `mkdir -p ~/.archc && cp /Volumes/External/Code/ArchC/archc.conf ~/.archc/` |
| `stat64 not found` на macOS | В macOS 64-битные иноды включены по умолчанию | Флаги компилятора уже содержат `-Dstat64=stat -Dlstat64=lstat -Dfstat64=fstat` |
| `SystemC headers require C++17` | `systemc 3.0+` требует стандарт `c++17` | Флаг `-std=c++17` автоматически включен в `build.sh` |
| `Address out of bounds (pc=0x0)` | Не инициализирован `dec_cache_size` при ручной загрузке памяти | Поле `dec_cache_size` устанавливается автоматически перед `init_dec_cache()` |
