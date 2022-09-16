# Homework for online course [Python QA Engineer from OTUS](https://otus.ru/lessons/avtomatizaciya-web-testirovaniya/)

## 1. UI tests for opencart

Example command:

```
pytest --browser=chrome --bv=102.0 --base_url=http://192.168.1.1:8081 --username=admin --password=secure123 --executor=192.168.1.1 --vnc page_objects_and_tests_for_opencart

```

1. `pytest` arguments
   1. `-m=smoke` run only smoke tests
   2. `--base_url=http://192.168.1.1:8081` URL to running opencart (How-to setup in p.3 below)
   2. `--username=SOME_USERNAME --password=SOME_PASSWORD` Get (or set up your own) Opencart ADMIN creds
      from `opencart_ui_tests/opencart_docker/docker-compose.yml`
   3. `--browser_name=chrome` select browser name
   4. `--executor`
      1. `--executor=local` to run locally (ensure you have Browser and corresponding Driver)
      2. `--executor={REMOTE_EXECUTOR_IP}` to run via Selenoid, arguments:
         1. `--vnc` capture [UI of tests execution](https://aerokube.com/selenoid-ui/latest/)
         2. `--bv` select browser version
         3. `--videos` save UI of tests execution to files
   5. `-n=4` run tests in parallel, e.g. 4 threads
2. Selenoid setup
   1. Prepare Selenoid via [Configuration Manager](https://aerokube.com/cm/latest/):
   2. `./cm selenoid start --vnc`
   3. `./cm selenoid-ui start`
3. OpenCart setup
   1. specify your local IP and Admin creds
      in `opencart_ui_tests/opencart_docker/docker-compose.yml`
   2. `cd opencart_ui_tests/opencart_docker`
   3. `docker compose up -d`
4. Allure reports
   1. install Allure locally
   2. run `allure generate`