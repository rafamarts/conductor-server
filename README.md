### Netflix Conductor Server

This is a build of [Netflix Conductor](https://github.com/Netflix/conductor) that provides tasks and workflows during the server startup.

#### Usage

Dockerfile:

```Dockerfile
FROM rafaelmm/conductor-server:3.6.1

ADD /provisioning /provisioning
```

Where the `provisioning` directory should have subdirectories `tasks` and `workflows` that contain the tasks and workflows respectively. Check the [exemple](example).

The version `3.6.1` is a tag version in Netflix Conductor original repository. If you would like to build new version, use the `ARG CONDUCTOR_VERSION=v3.6.1` line in Dockerfile

#### Contribute

I would like to thanking [Flavio Stutz](https://github.com/flaviostutz) by the idea. Feel free to contribute. Please, send a PR.
