# Comissioning Service

This is a small service that runs on boot to grab config and Wifi credentials from a thumbdrive.

## Usage
See how the the `../services/commissioning.service` file uses it.

## Testing and Linting
To run the tests:
```bash
docker run --name rovercode-commissioning-testing -w='/var/rovercode/commissioning' -v $PWD:/var/rovercode --entrypoint=/bin/bash rovercode -c 'python -m pytest'
```

To run the linter:
```bash
docker run --name rovercode-commissioning-testing -w='/var/rovercode/commissioning' -v $PWD:/var/rovercode --entrypoint=/bin/bash rovercode -c 'prospector'
```