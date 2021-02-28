# RESTDistro
## REST Distributive container

### Переменные окружения

##### точка монтирования расшариваемого каталога

```sh
MOUNT_POINT=/var/log
```

##### номер http порта

```sh
PORT_NUM=80
```

### сборка:

```sh
docker build -t distro ./
```

### запуск:

напр. рашарим пачку логов хостовой машины:

```sh
docker run -d -p 0.0.0.0:80:80/tcp -v /var/log:/opt/logs -e MOUNT_POINT=/opt/logs --name=distro distro
```

> Примечание: по дефолту точка монтирования расшариваемого каталога в /var/log
