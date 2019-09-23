"""Takes configuration information from a file and sets up the Rover."""
import argparse
import glob
import logging
import os
from dotenv import dotenv_values

logging.basicConfig()
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.getLevelName('INFO'))


def update_env_file(env_source_directory, env_dest_directory):
    """Copy configuration information from one file to another."""
    env_dest_path = env_dest_directory + '.env'

    source_files = list(filter(
        os.path.isfile,
        glob.glob(env_source_directory + "*.env")))
    if not source_files:
        LOGGER.warning(f'No .env files found at {env_source_directory}')
        return
    source_files.sort(key=lambda x: os.path.getmtime(x))
    source_file = source_files[-1]
    source_values = dotenv_values(dotenv_path=source_file)

    if not os.path.exists(env_dest_directory):
        os.makedirs(env_dest_directory)
    if not os.path.exists(env_dest_path):
        open(env_dest_path, 'a').close()
    dest_values = dotenv_values(dotenv_path=env_dest_path)
    dest_values.update(source_values)
    LOGGER.info(f'Writing .env file with values: {dest_values}')
    with open(env_dest_path, 'w') as dest_file:
        for key, value in dest_values.items():
            dest_file.write(f'{key}={value}\n')
    LOGGER.info("Done updating .env file.")


def main():
    """Kick off all the commissioning work."""
    parser = argparse.ArgumentParser()
    parser.add_argument("source", help="source file directory")
    parser.add_argument("destination", help="destination file directory")
    args = parser.parse_args()

    LOGGER.info("Beginning commissioning.")
    update_env_file(args.source, args.destination)
    # TODO: update wfa_supplicant.conf
    LOGGER.info("Finished commissioning.")


if __name__ == '__main__':
    main()  # pragma: no cover
