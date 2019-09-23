# Comissioning Service

## Testing and Linting

To run the linter:
```bash
docker run --name rovercode-commissioning-testing -w='/var/rovercode/commissioning' -v $PWD:/var/rovercode --entrypoint=/bin/bash rovercode -c 'prospector'
```