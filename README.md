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

| Politics                 | Description                                                                                                                                                                  | 
|--------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------| 
| on                       | Do not reload the container automatically<br/>(by default)                                                                                                                   |
| on-failure[:max-retries] | Restart the container if it stops due to an error.<br/>ptionally, limit the number of times the Docker daemon attempts to restart the container using the :max-retries option | 
| always                   | Always restart the container if it stops. If it is manually stopped, it is restarted only when Docker daemon restarts or the container itself is manually restarted          | 
| unless-stopped           | Similar to always, except that when the container is stopped (manually or otherwise), it is not restarted even after Docker daemon restarts                                  | 

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

## Tips

Using the PUID and PGID allows our containers to map the container's internal user to a user on the host machine. All of
our containers use this method of user mapping and should be applied accordingly.

~~~
- PUID=1000
- PGID=1000
~~~

