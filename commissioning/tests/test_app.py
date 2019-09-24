"""Test the app module."""
import argparse
import subprocess
import urllib.error
from unittest.mock import patch, mock_open, call

import app


def get_env_data(dotenv_path):
    """Return mock config data."""
    if dotenv_path == 'source.env':
        return {'a': '1', 'b': '2',
                'AP_NAME': 'foo', 'AP_PASSWORD': 'bar'}
    if dotenv_path == 'dest/.env':
        return {'b': '200', 'c': 'asdf'}
    return None


@patch('builtins.open', new_callable=mock_open)
@patch('app.dotenv_values')
@patch('os.path')
def test_updating_env_file(mock_path, mock_dotenv, mock_dest_open):
    """Test updating an env file."""
    mock_path.exists.return_value = True
    mock_dotenv.side_effect = get_env_data
    app.update_env_file(get_env_data('source.env'), 'dest/')
    mock_dest_open.assert_called_with('dest/.env', 'w')
    mock_dest_handle = mock_dest_open()
    mock_dest_handle.write.assert_has_calls(
        [call('a=1\n'), call('b=2\n'), call('c=asdf\n')],
        any_order=True)


@patch('os.makedirs')
@patch('builtins.open', new_callable=mock_open)
@patch('app.dotenv_values')
@patch('os.path')
def test_updating_env_file_no_dest_path(mock_path, mock_dotenv,
                                        mock_dest_open, mock_makedirs):
    """Test updating an env file."""
    mock_path.exists.return_value = False
    mock_dotenv.side_effect = get_env_data
    app.update_env_file(get_env_data('source.env'), 'dest/')
    mock_makedirs.assert_called_with('dest/')
    mock_dest_open.assert_called_with('dest/.env', 'w')
    mock_dest_handle = mock_dest_open()
    mock_dest_handle.write.assert_has_calls(
        [call('a=1\n'), call('b=2\n'), call('c=asdf\n')],
        any_order=True)


@patch('app.dotenv_values')
@patch('argparse.ArgumentParser.parse_args',
       return_value=argparse.Namespace(source='src/', destination='dest/'))
@patch('app.configure_wpa_supplicant')
@patch('app.connected_to_internet')
@patch('app.update_env_file')
@patch('os.path.getmtime')
@patch('os.path.isfile')
@patch('glob.glob')
def test_main(mock_glob, mock_isfile, mock_mtime, mock_update_env,
              mock_is_connected, mock_configure_wpa, _, mock_dotenv):
    """Test main function."""
    mock_isfile.return_value = True
    mock_glob.return_value = ['source.env']
    mock_dotenv.side_effect = get_env_data
    mock_is_connected.return_value = False
    app.main()
    mock_glob.assert_called_with('src/*.env')
    mock_mtime.assert_called_with('source.env')
    expected = get_env_data('source.env').copy()
    ap_name = expected.pop('AP_NAME')
    ap_password = expected.pop('AP_PASSWORD')
    mock_update_env.assert_called_with(expected, 'dest/')
    mock_configure_wpa.assert_called_with(ap_name, ap_password)


@patch('argparse.ArgumentParser.parse_args',
       return_value=argparse.Namespace(source='src/', destination='dest/'))
@patch('app.configure_wpa_supplicant')
@patch('app.connected_to_internet')
@patch('app.update_env_file')
@patch('os.path.isfile')
@patch('glob.glob')
def test_main_no_source_files(mock_glob, mock_isfile, mock_update_env,
                              mock_is_connected, mock_configure_wpa, _):
    """Test main function."""
    mock_is_connected.return_value = True
    mock_isfile.return_value = True
    mock_glob.return_value = []
    app.main()
    mock_glob.assert_called_with('src/*.env')
    mock_update_env.assert_not_called()
    mock_configure_wpa.assert_not_called()


@patch('urllib.request')
def test_connected_to_internet(mock_url_request):
    """Test successful connection to the Internet."""
    assert app.connected_to_internet()
    mock_url_request.urlopen.assert_called_with('https://google.com')


@patch('urllib.request')
def test_connected_to_internet_failed(mock_url_request):
    """Test when cannot connect to the Internet."""
    mock_url_request.urlopen.side_effect = urllib.error.URLError("No internet")
    assert not app.connected_to_internet()


WPA_CALLS = [
    call(['wpa_cli add_network'], capture_output=True),
    call(['wpa_cli set_network 5 ssid \'"test_ssid"\'']),
    call(['wpa_cli set_network 5 psk \'"test_psk"\'']),
    call(['wpa_cli enable_network 5']),
    call(['wpa_cli save_config']),
    call(['wpa_cli -i wlan0 reconfigure'])
]


@patch('app.connected_to_internet')
@patch('subprocess.run')
def test_configure_wifi(mock_subprocess, mock_connected):
    """Test configuring the WiFi."""
    mock_connected.return_value = True
    mock_subprocess.return_value = subprocess.CompletedProcess(
        [], 0, stdout='Network ok\n 5')
    app.configure_wpa_supplicant('test_ssid', 'test_psk')
    mock_subprocess.assert_has_calls(WPA_CALLS)


@patch('app.connected_to_internet')
@patch('subprocess.run')
def test_configure_wifi_doesnt_come_up(mock_subprocess, mock_connected):
    """Test when the WiFi interface doesn't come up."""
    mock_connected.return_value = False
    mock_subprocess.return_value = subprocess.CompletedProcess(
        [], 0, stdout='Network ok\n 5')
    app.configure_wpa_supplicant('test_ssid', 'test_psk')
    mock_subprocess.assert_has_calls(WPA_CALLS)
