# docker_setups

## Motivation

The goal of this project - is to collect the main development tools, and examples how to use them with docker

Here you'll see:

- RabbitMQ
- PostgreSql
- Hadoop

and many other popular things.

This repo I've done to myself, in order to speed up the search for information how to do a certain thing.

## Docker container start automatically

After installing docker and launching the first container, you don't immediately think that after restarting the server
container won't start by itself.

| Politics                 | Description                                                                                                                                                                   | 
|--------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------| 
| on                       | Do not reload the container automatically<br/>(by default)                                                                                                                    |
| on-failure[:max-retries] | Restart the container if it stops due to an error.<br/>ptionally, limit the number of times the Docker daemon attempts to restart the container using the :max-retries option | 
| always                   | Always restart the container if it stops. If it is manually stopped, it is restarted only when Docker daemon restarts or the container itself is manually restarted           | 
| unless-stopped           | Similar to always, except that when the container is stopped (manually or otherwise), it is not restarted even after Docker daemon restarts                                   | 

_docker-compose:_

~~~docker
restart: unless-stopped
~~~

_In creation:_

~~~
docker run --restart unless-stopped mycontainer
~~~

_If container already created:_

~~~
docker update –restart unless-stopped mycontainer
~~~

## How to manage data in Docker

When we delete a Docker container, all the data associated or written to the container is deleted with it. So there is a
need to persist the container data somehow even when the container gets deleted so that we need not worry about data and
persist this data after the container ceases to exist.

![readme_photos/img.png](readme_photos/docker_reload.png)

As shown above, Docker provides two options for data persistence so that files are persisted even after the container
stops.

- Volumes
- Mounts

**Volumes** are directories or files that are outside the Union file system(the combination of read-only layers with a
read-write layer on top of the container). Volumes exist/ store as normal files and directories on the host
filesystem. Hence to persist and share data between containers, Docker uses Volumes. Volumes are the best option to
persist data in Docker containers. Docker manages volumes and is stored in a part of the host filesystem (
/var/lib/docker/volumes/ on Linux).

**Bind mount**
Это более простая концепция: файл или каталог с хоста просто монтируется в контейнер.
Используется, когда нужно пробросить в контейнер конфигурационные файлы с хоста. Например, именно так в контейнерах
реализуется DNS: с хоста монтируется файл /etc/resolv.conf.
Другое очевидное применение — в разработке. Код находится на хосте (вашем ноутбуке), но исполняется в контейнере. Вы
меняете код и сразу видите результат. Это возможно, так как процессы хоста и контейнера одновременно имеют доступ к
одним и тем же данным.

**Tmpfs mounts** are used mainly by Docker running on Linux systems. Their storage is in the host system’s memory only.
Additionally, we never write the tmpfs mounts to the host system’s filesystem. Contrary to volumes and bind mounts,
the "tmpfs" mount is temporary and only persisted in the host memory. When the container stops, the "tmpfs" mount
removes, and files written there won’t persist.

## Expose ports

~~~dockerfile
version: "3.9"
services:
  web:
    build: .
    ports:
    # HOST_PORT:CONTAINER_PORT
      - "8000:8000"
  db:
    image: postgres
    ports:
      - "8001:5432"
~~~

It is important to note the distinction between HOST_PORT and CONTAINER_PORT.
In the above example, for db, the HOST_PORT is 8001 and the container port is 5432 (postgres default).

**Networked service-to-service communication uses the CONTAINER_PORT.**

**When HOST_PORT is defined, the service is accessible outside the docker as well.**

Within the web container, your connection string to db would look like postgres://db:5432,
and from the host machine, the connection string would look like postgres://{DOCKER_IP}:8001.

## Tips

Using the PUID and PGID allows our containers to map the container's internal user to a user on the host machine. All of
our containers use this method of user mapping and should be applied accordingly.

~~~
- PUID=1000
- PGID=1000
~~~

### Bash into a running container

~~~bash
docker ps
~~~

~~~
CONTAINER ID   IMAGE           COMMAND                  CREATED        STATUS          PORTS                    NAMES
44bf2e32249f   postgres:14.0   "docker-entrypoint.s…"   4 months ago   Up 15 minutes   0.0.0.0:5432->5432/tcp   postgresql_postgres_1
~~~

~~~bash
docker exec -ti 44bf2e32249f /bin/bash
~~~

# k8s

## Структура Pod-а

В общем виде можно выделить 4 вида дополнительных «полезных» контейнеров:

* Init;
* Sidecar;
* Adapter;
* Ambassador.

### initContainers

* Позволяет выполнить настройку перед запуском основного приложения
* Выполняется по порядку описания в манифесте
* Можно монтировать те же тома, что и в основных контейнерах
* Можно запускать от другого пользователя
* Должен выполнить действие и остановиться

### Sidecar Containers

В общем случае sidecar-контейнер — это контейнер с законченной функциональностью, которая нужна приложению, но не
является частью его бизнес-логики. За счёт такого разделения разработчики могут фокусироваться на одной задаче.
Платформенная команда отвечает за дополнительные возможности, например, делает приложение более отказоустойчивым,
надёжным. В свою очередь прикладные разработчики занимаются исключительно бизнес-логикой приложения.

Sidecar-контейнеры чаще всего используются для добавления платформенной функциональности, например:

* Service Mesh — в этом случае добавляется сетевой прокси, который обрабатывает все запросы, добавляет observability,
  делает mutual TLS и остальные полезные вещи.
* Журналирование, если вам по каким-то причинам не нравится решение собирать логи через daemon, который бежит на воркере
  Kubernetes и забирает данные сразу с контейнерного runtime'а.
* Централизованный аудит.

### Adapter Containers

Адаптеры — такие же sidecar’ы, но узкоспециализированные. Они используются тогда, когда в приложение нужно добавить
новый API, но не хочется (или не получается) сделать это на уровне приложения.

* Metrics API. Есть система мониторинга на базе Prometheus и приложение, которое про эту систему мониторинга вообще
  ничего
  не знает. У этого приложения есть либо только свои метрики, либо нет вообще нет никаких. Для «неинвазивного» решения
  проблемы достаточно добавить Prometheus экспортер отдельным контейнером, который опубликует все нужные метрики в
  правильном формате.
* Custom API. Позволяет добавить произвольный API по аналогии с примером метрик.
* RBAC Proxy. Дополнительный контейнер становится точкой входа в приложение и добавляет стандартный RBAC Kubernetes. Это
  делается очень быстро и во многих случаях бывает полезно.

### Ambassador Containers

Эти контейнеры похожи на адаптеры, но работают в обратную сторону: они инкапсулируют в себя всю сложность внешнего API и
позволяют использовать его понятным для приложения способом.


## Команды:

Создание объекта:

~~~bash
kubectl create -f pod.yaml
~~~

Создание или обновление объекта:

~~~bash
kubectl apply -f pod.yaml
~~~

Просмотр подов:

~~~bash
kubectl get pod
-w # в реальном времени как поднимается под
~~~

Просмотр ReplicaSet

~~~bash
kubectl get rs
~~~

Просмотр configmap:

~~~bash
kubectl get cm
~~~

Просмотр services:

~~~bash
kubectl get svc
~~~

Описание:

~~~bash
kubectl describe pod {pod_name}
kubectl describe cm {configmap name}
~~~

Объяснить объект k8s:

~~~bash
kubectl explain deployment.spec.strategy
kubectl get po <ИМЯ НОВОГО POD'а> -o=jsonpath='{.spec.containers[*].image}{"\n"}'
~~~

Выполнение команды внутри пода:

~~~bash
kubectl exec -t -i {pod_name} {command}
~~~

Просмотр логов:

~~~bash
kubectl logs {pod_name}
~~~

Содержимое манифеста:

~~~bash
kubectl get {cm/pod} {name} -o yaml
~~~

Открытие портов:

~~~bash
kubectl port-forward {pod_name} {port to local}:{port app works} &
~~~

& - чтобы работал в фоне

Pod для тестов:

~~~bash
kubectl run test  --image=amount/network-utils -it bash
~~~