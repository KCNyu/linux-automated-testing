# Обзор Директории Parser

> 🌐 **Языки:** [English](./README.md) | [Русский](./README_ru.md)

Директория `parser` предназначена для анализа результатов запуска тестов Kselftests и их подготовки к отправке в системы CI. В этой директории перечислены три версии Parser, сравнение их эффективности и оптимизации.

## Версии Parser

### Версия ISP RAS

- **Основа:** Построена на старой версии, реализованной Linaro, использует Perl и shell-скрипты. Анализирует логи построчно с использованием Perl, сохраняет результаты анализа в формате, похожем на CSV, и затем отправляет их в LAVA с помощью shell-скриптов.
- **Недостатки:**
  1. Низкая эффективность выполнения и медленная скорость анализа.
  2. Невозможность анализа подтестов.

### Версия Linaro

- **Реализация:** Использует Python для части Parser, сохраняет результаты анализа в формате, похожем на CSV, и отправляет их в LAVA с помощью shell-скриптов.
- **Недостатки:**
  1. Хотя поддерживает анализ подтестов, формат именования не унифицирован.
  2. Отсутствует поддержка сохранения ошибок анализа.

### Текущая Реализация

- **Технология:** Полностью реализована на Perl без внешних зависимостей, объединяет части Parser и Submitter. Отправка в LAVA производится с использованием массивов в памяти, чтозначительно улучшает эффективность отправки.
- **Преимущества:**
  1. Повышенные скорости анализа и отправки.
  2. Поддержка более детального анализа подтестов с унифицированным именованием.
  3. Возможность отправки тестов из одной и той же подсистемы в виде SET, что упрощает управление тестами.
  4. Поддержка вывода причин ошибок.
  5. Возможность сохранения результатов анализа в форматах JSON и CSV, что позволяет легко взаимодействовать с другими системами CI с помощью соответствующих реализаций submitter.

## Начало Работы

Чтобы использовать парсеры, перейдите в директорию соответствующей версии и следуйте конкретным инструкциям, предоставленным в каждой из них. Выбор версии парсера может зависеть от ваших конкретных требований к эффективности, обработке ошибок и формату отправки в системы CI.