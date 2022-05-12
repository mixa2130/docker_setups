# docker_setups

## Motivation

The goal of this project - is to collect the main development tools, and examples how to use them with docker

Here you'll see:

- RabbitMQ
- PostgreSql
- Hadoop

and many other popular things.

This repo I've done to myself, in order to speed up the search for information how to do a certain thing.

## Tips

Using the PUID and PGID allows our containers to map the container's internal user to a user on the host machine. All of
our containers use this method of user mapping and should be applied accordingly.

~~~
- PUID=1000
- PGID=1000
~~~