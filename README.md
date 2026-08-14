# Random Sail (V-ISA) -> C++ Emulator Generator

Генератор случайных спецификаций векторных расширений RISC-V / V-ISA на формальном языке **Sail** с автоматической кодогенерацией быстрых **C++20 эмуляторов**, построенный на принципах **Гексагональной архитектуры (Ports & Adapters)** и **Domain-Driven Design (DDD)**.

---

## 🏛 Архитектура проекта (Hexagonal + DDD)

```
random_visa/
├── domain/                         # DOMAIN LAYER (Чистая бизнес-логика без внешних зависимостей)
│   ├── model/                      # Entities, Value Objects, Aggregates
│   │   ├── types.py                # SEW, LMUL, ElementKind, BinaryOp, UnaryOp, InstructionFormat
│   │   ├── vector_config.py        # VectorConfig (VLEN, ELEN, max_vl, tail/mask policies)
│   │   ├── sail_ast.py             # Sail AST (SailType, SailExpr, SailStmt, SailFunctionDef)
│   │   ├── instruction.py          # VectorInstruction Aggregate Root
│   │   └── isa_spec.py             # VectorIsaSpec Aggregate Root
│   ├── services/                   # Domain Services
│   │   └── random_generator.py     # Синтез валидных случайных векторных инструкций
│   ├── events/                     # Domain Events
│   │   └── events.py               # InstructionSynthesizedEvent, IsaSpecCompletedEvent
│   └── ports/                      # Ports (Интерфейсы взаимодействия)
│       ├── inbound/                # Driving Ports (Use Cases)
│       │   └── ports.py            # GenerateSpecPort, EmitEmulatorPort, RunPipelinePort
│       └── outbound/               # Driven Ports (SPI / Инфраструктура)
│           └── ports.py            # SailSpecWriterPort, CppCodeEmitterPort, CompilerRunnerPort
│
├── application/                    # APPLICATION LAYER (Оркестрация и CQRS)
│   ├── dtos.py                     # DTO запросов и результатов
│   └── use_cases/                  # Реализация Use Cases
│       └── pipeline.py             # GenerateRandomVisaUseCase, EmitCppEmulatorUseCase, RunFullPipelineUseCase
│
├── adapters/                       # ADAPTERS LAYER (Реализация портов)
│   ├── inbound/                    # Driving Adapters (Входные точки)
│   │   └── cli/                    # CLI-интерфейс на Rich / Argparse
│   │       └── main.py
│   └── outbound/                   # Driven Adapters (Выходные адаптеры)
│       ├── sail/                   # Запись формальных спецификаций Sail (.sail)
│       │   └── sail_file_adapter.py
│       ├── cpp_codegen/            # Генератор C++20 эмулятора (шаблоны Jinja2)
│       │   └── cpp_emitter_adapter.py
│       └── compiler/               # Clang++/GCC компилятор и запуск верификационных тестов
│           └── clang_runner_adapter.py
│
└── tests/                          # Модульные и интеграционные тесты
    ├── unit/
    └── integration/
```

---

## 🚀 Быстрый старт

### 1. Запуск полного пайплайна через CLI
Сгенерировать случайную векторную спецификацию из 12 инструкций, экспортировать Sail-файл, сгенерировать C++20 эмулятор и проверить выполнение:

```bash
python3 -m random_visa.adapters.inbound.cli.main pipeline \
  --name RVV_Custom_ISA \
  --num-insts 12 \
  --vlen 128 \
  --seed 42 \
  --out-dir generated_emulator
```

### 2. Запуск тестов
```bash
python3 -m pytest -v
```

---

## 🧩 Компоненты генерируемого C++ эмулятора

В директорию сборки генерируется полный автономный C++20 проект:
- `isa_state.hpp`: Регистровый файл векторов `v0`..`v31` (параметризуемый `VLEN`), скалярные регистры `x0`..`x31`, CSR (`vl`, `vtype`, `vstart`, `vxrm`).
- `decoder.hpp`: Табличный и побитовый декодер инструкций по `funct6`, `funct3`, `opcode`.
- `instructions.hpp` / `instructions.cpp`: Реализация семантики инструкций (цикл по `vl`, проверка маскирования `vm` и `v0`).
- `emulator.hpp`: Главный класс эмулятора с методами `step()` и `run_program()`.
- `main.cpp`: Тестовый стенд верификации сгенерированных инструкций на тестовых векторах.
- `CMakeLists.txt`: Конфигурация сборки.
