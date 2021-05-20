 
0) ветку назовите homework2, положите код в папку online_inference

done

1) Оберните inference вашей модели в rest сервис(вы можете использовать как FastAPI, так и flask, другие желательно не использовать, дабы не плодить излишнего разнообразия для проверяющих), должен быть endpoint /predict (3 балла)

done

2) Напишите тест для /predict  (3 балла) (https://fastapi.tiangolo.com/tutorial/testing/, https://flask.palletsprojects.com/en/1.1.x/testing/)

 no
 
3) Напишите скрипт, который будет делать запросы к вашему сервису -- 2 балла

done

4) Сделайте валидацию входных данных (например, порядок колонок не совпадает с трейном, типы не те и пр, в рамках вашей фантазии)  (вы можете сохранить вместе с моделью доп информацию, о структуре входных данных, если это нужно) -- 3 доп балла
https://fastapi.tiangolo.com/tutorial/handling-errors/ -- возращайте 400, в случае, если валидация не пройдена

no

5) Напишите dockerfile, соберите на его основе образ и запустите локально контейнер(docker build, docker run), внутри контейнера должен запускать сервис, написанный в предущем пункте, закоммитьте его, напишите в readme корректную команду сборки (4 балл)

```
docker build -f online_inference/Dockerfile  -t ainureg/prod_made . &&  docker run -p 80:80  --rm -it ainureg/prod_made:latest

```
6) Оптимизируйте размер docker image (3 доп балла) (опишите в readme.md что вы предприняли для сокращения размера и каких результатов удалось добиться)  -- https://docs.docker.com/develop/develop-images/dockerfile_best-practices/

no

7) опубликуйте образ в https://hub.docker.com/, используя docker push (вам потребуется зарегистрироваться) (2 балла)

done
```
(V) ~/Desktop/made/prod/hw/ainureg$ docker push ainureg/prod_made:latest
The push refers to repository [docker.io/ainureg/prod_made]
7cc0c8096d8a: Pushed 
abfa166af07a: Pushed 
8fea66aadaa6: Pushed 
0a39d78a90a9: Pushed 
4d2d30a9a9ec: Pushed 
c4bee897fbf3: Pushed 
0b42244132be: Pushed 
2f140462f3bc: Pushed 
63c99163f472: Pushed 
ccdbb80308cc: Pushed 
latest: digest: sha256:8fb99223ab6f56ab354dedc44df207aa726cd1665424a5b3fe0d718d37ff5590 size: 2412
```

8) напишите в readme корректные команды docker pull/run, которые должны привести к тому, что локально поднимется на inference ваша модель (1 балл)
Убедитесь, что вы можете протыкать его скриптом из пункта 3
```
~/Desktop/made/prod/hw/ainureg/online_inference$ docker pull ainureg/prod_made
Using default tag: latest
latest: Pulling from ainureg/prod_made
345e3491a907: Already exists 
57671312ef6f: Already exists 
5e9250ddb7d0: Already exists 
fc234ab040a9: Pull complete 
e306f41eb5d5: Pull complete 
3d79887106c8: Pull complete 
b7b8c9cdd0b6: Pull complete 
e4adf1210f2d: Pull complete 
ad1a4f3370fe: Pull complete 
758aa62cac7e: Pull complete 
Digest: sha256:8fb99223ab6f56ab354dedc44df207aa726cd1665424a5b3fe0d718d37ff5590
Status: Downloaded newer image for ainureg/prod_made:latest
docker.io/ainureg/prod_made:latest
```

```
~/Desktop/made/prod/hw/ainureg/online_inference$ ./homework_script.py 
[0, 37.0, 0.0, 4.0, 944.0, 384.0, 1.0, 2.0, 553.0, 1.0, 0.8, 1.0, 1.0, 3.0]
200
```

5) проведите самооценку -- 1 доп балл

   0\[баллов\][0\[задание\]] + 3[1] + 0[2] + 2[3] + 0[4] + 4[5] + 0[6] + 2[7] +1[8] + 1[5*] = 13 
   
6) создайте пулл-реквест и поставьте label -- hw2 
