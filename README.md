# ainureg
a repo for homeworks ml in production



Данные проект позволяет
1. сохранить новую модель в зависимости от настроек

```
./app.py build --data_path --output_path 
```
По дефолту модель сохранится в папке model

2. получить результаты модели
   после обучения можно получить модель и применить её. По умолчанию применится для файла из конфига на тестовой выборке. Путь к модели можно применить из результатов build
```
./app.py predict --data_path --output --save_folder
```
3)получить предикты

## самооценка

-2. Назовите ветку homework1 (1 балл)

      сделано(1 балл)

-1. положите код в папку ml_project

    сделано

0. В описании к пулл реквесту описаны основные "архитектурные" и тактические решения, которые сделаны в вашей работе. В общем, описание что именно вы сделали и для чего, чтобы вашим ревьюерам было легче понять ваш код. (2 балла)

1. Выполнение EDA, закоммитьте ноутбук в папку с ноутбуками (2 баллов) Вы так же можете построить в ноутбуке прототип(если это вписывается в ваш стиль работы) Можете использовать не ноутбук, а скрипт, который сгенерит отчет, закоммитьте и скрипт и отчет (за это + 1 балл)

    Пока только Юпитер. В принципе я выбрал простой подход, лес, в принципе все интересное показано
    +2 балла

2. Проект имеет модульную структуру(не все в одном файле =) ) (2 баллов)

    +2 балла

3. использованы логгеры (2 балла)

    +2 балла

4. написаны тесты на отдельные модули и на прогон всего пайплайна(3 баллов)

    тесты есть, но маловато. 1 балл

5. Для тестов генерируются синтетические данные, приближенные к реальным (3 баллов)
можно посмотреть на библиотеки faker, Feature Forge
можно просто руками посоздавать данных, собственноручно написанными функциями как альтернатива, можно закоммитить файл с подмножеством трейна(это не оценивается)

   к сожалению данные просто числа, применение фейкера не вразумил.
   сгенерировал сам. 3 балла

6. Обучение модели конфигурируется с помощью конфигов в json или yaml, закоммитьте как минимум 2 корректные конфигурации, с помощью которых можно обучить модель (разные модели, стратегии split, preprocessing) (3 балла)
1 конфиг.
   
   все конфиги, которые мог, закинул туда. Проникся.
   Второй конфиг не слишком нужный, маломальски отличается.
   3 балла

7. Используются датаклассы для сущностей из конфига, а не голые dict (3 балла)

   3 балла

8. Используйте кастомный трансформер(написанный своими руками) и протестируйте его(3 балла)

   увы

9. Обучите модель, запишите в readme как это предлагается (3 балла)

   Обучено, описано.

10. напишите функцию predict, которая примет на вход артефакт/ы от обучения, тестовую выборку(без меток) и запишет предикт, напишите в readme как это сделать (3 балла)

   done

11. Используется hydra (3 балла - доп баллы)

12. Настроен CI(прогон тестов, линтера) на основе github actions (3 балла - доп баллы (будем проходить дальше в курсе, но если есть желание поразбираться - welcome)

13. Проведите самооценку, опишите, в какое колво баллов по вашему мнению стоит оценить вашу работу и почему (1 балл доп баллы)


в районе 23-25 баллов - ожидаемо. Можно снизить за простоту до 15-18. Вряд ли меньше
