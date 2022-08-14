# Dead simple docker service update daemon

Example on how to run it:
```
docker run -it -p 8000:8000 \
  -v /var/run/docker.sock:/var/run/docker.sock \
  m2rtk/docker-update-daemon
```

Example on how to use it:
```commandline
curl localhost:8000/media_jellyfin/linuxserver/jellyfin:latest
```

## Motivation
Wanted a webhook for ci to update service in dev environment. Using docker api directly seemed tiresome.
