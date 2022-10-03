## mlgdansk 132


## Install requirements

```bash
sudo apt update
sudo apt install python3 python3-pip nodejs npm -y
sudo npm install -g pm2
```

## Deploy application

### PM2 deployment

Application can be launched with the launch script:
```bash
sudo bash launch.sh
```
Or using PM2:
```bash
sudo pm2 start pm2.json
```
Note: if the script `launch.sh` doesn't works, you can use `launch2.sh` instead.

### Docker deployment

Build image and run

```bash
sudo docker build -t <dockerhub username>/mlgdansk132 .
sudo docker run -it --rm --name <dockerhub username>/mlgdansk132 mlgdansk132
```

## Run application

For running directly the application in a "raw" way:
```bash
sudo python3 -m pip install pip --upgrade
sudo python3 -m pip install . --upgrade
sudo ina_task_service
```


## Disclaimer

Component developed by Francisco Pinto-Santos (@GandalFran on GitHub) on 2022. For manteinance and bug reports please contact the developer at franpintosantos@usal.es.
Copyright Francisco Pinto-Santos 2022. All rights reserved. See license for details.