# Обзор Директории Transformer

> 🌐 **Языки:** [English](./README.md) | [Русский](./README_ru.md)

Директория `transformer` содержит инструменты и скрипты, предназначенные для устранения исторической несогласованности форматов вывода самотестирования ядра Linux. Поскольку менее 20% тестов используют фреймворк kselftest, управление и интерпретация результатов тестов представляли собой сложную задачу. Transformer направлен на стандартизацию файлов тестов путем преобразования тех, которые не используют фреймворк kselftest, в унифицированный формат.

## Как Это Работает

Процесс трансформации включает несколько ключевых шагов, использует семантические патчи Coccinelle и скрипты Python для автоматизации преобразования:

1. **Добавление Зависимости:** Автоматически добавляет зависимость относительного пути к `kselftest_harness.h` в тестовые файлы.

2. **Проверка Зависимости:** Использует Spatch для проверки успешного добавления зависимости.

3. **Преобразование Функций Тестирования:** Преобразует основные функции тестирования в тесты, инкапсулированные определением макроса TEST.

4. **Стандартизация Внешних API Вывода:** Изменяет внешние API вывода (такие как `printf`, `perror` и т. д.) на унифицированный API вывода фреймворка `ksft_print_msg`.

5. **Стандартизация Внутренных API Вывода:** Модифицирует внутренние API вывода в тесте для использования унифицированных API вывода фреймворка `TH_LOG`/`LOG`.

6. **Обработка Условных Тестов:** Преобразует специфические условные тесты в соответствующие случаи `EXPECT_*` или `ASSERT_*` и упаковывает соответствующие функции очистки.

7. **Замена Значений Выхода:** Заменяет значения выхода на специфические для фреймворка макрозначения выхода (`KSFT_PASS`, `KSFT_FAIL` и т. д.).

8. **Преобразование Аргументов Командной Строки:** Преобразует переменные, зависящие от командной строки (`argc`, `argv` и т. д.), в `__test_global_metadata`, облегчая использование таких функций, как фильтрация, без необходимости изменения внешнего выполнения скриптов.

## Начало Работы

Для использования инструментов Transformer выполните следующие шаги:

- Убедитесь, что у вас установлены необходимые зависимости, включая Coccinelle.
- Перейдите в директорию `transformer` и запустите скрипт трансформации на ваши целевые тестовые файлы.
- Проверьте конвертацию, просмотрев преобразованные тестовые файлы и запустив их в рамках фреймворка kselftest.