"""Takes configuration information from a file and sets up the Rover."""
import argparse
import glob
import logging
import os
import subprocess
import urllib.request
import urllib.error
from time import sleep
from dotenv import dotenv_values

logging.basicConfig()
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.getLevelName('INFO'))


def connected_to_internet():
    """Check if we haven an Internet connection."""
    try:
        urllib.request.urlopen('https://google.com')
        return True
    except urllib.error.URLError:
        return False


def update_env_file(source_values, env_dest_directory):
    """Copy configuration information from one file to another."""
    env_dest_path = env_dest_directory + '.env'
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


def configure_wpa_supplicant(ssid, psk, script_dest_dir):
    """Configure wpa_supplicant."""
    LOGGER.info(f'Configuring WiFi for SSID {ssid}.')
    script_dest_path = script_dest_dir + 'wpa-cli-commands.sh'
    commands = [
        'result=$( wpa_cli add_network )\n',
        'network_id="${result: -1}"\n',
        f'wpa_cli set_network $network_id ssid \'"{ssid}"\'\n',
        f'wpa_cli set_network $network_id psk \'"{psk}"\'\n',
        f'wpa_cli enable_network $network_id\n',
        'wpa_cli save_config\n',
        'wpa_cli -i wlan0 reconfigure\n',
    ]
    with open(script_dest_path, 'w') as dest_file:
        for command in commands:
            dest_file.write(command)
    LOGGER.info('Done configuring WiFi init script.')


def main():
    """Kick off all the commissioning work."""
    parser = argparse.ArgumentParser()
    parser.add_argument("source", help="source file directory")
    parser.add_argument("destination", help="destination file directory")
    args = parser.parse_args()

    source_files = list(filter(
        os.path.isfile,
        glob.glob(args.source + "*.env")))
    print(source_files)
    if not source_files:
        LOGGER.warning(f'No .env files found at {args.source}')
        return
    source_files.sort(key=lambda x: os.path.getmtime(x))
    source_file = source_files[-1]
    source_values = dotenv_values(dotenv_path=source_file)

    LOGGER.info("Beginning commissioning.")
    if source_values:
        ssid = source_values.pop('AP_NAME')
        psk = source_values.pop('AP_PASSWORD')
        update_env_file(source_values, args.destination)
        if ssid and psk:
            configure_wpa_supplicant(ssid, psk, args.destination)
    LOGGER.info("Finished commissioning.")


if __name__ == '__main__':
    main()  # pragma: no cover
