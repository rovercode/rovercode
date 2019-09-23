"""Test the app module."""
import argparse
from unittest.mock import patch, mock_open, call

import app


def get_env_data(dotenv_path):
    """Return mock config data."""
    if dotenv_path == 'source.env':
        return {'a': '1', 'b': '2'}
    if dotenv_path == 'dest/.env':
        return {'b': '200', 'c': 'asdf'}
    return None


@patch('builtins.open', new_callable=mock_open)
@patch('app.dotenv_values')
@patch('os.path')
@patch('glob.glob')
def test_updating_env_file(mock_glob, mock_path, mock_dotenv, mock_dest_open):
    """Test updating an env file."""
    mock_glob.return_value = ['source.env']
    mock_path.exists.return_value = True
    mock_dotenv.side_effect = get_env_data
    app.update_env_file('src/', 'dest/')
    mock_dest_open.assert_called_with('dest/.env', 'w')
    mock_dest_handle = mock_dest_open()
    mock_dest_handle.write.assert_has_calls(
        [call('a=1\n'), call('b=2\n'), call('c=asdf\n')],
        any_order=True)


@patch('builtins.open', new_callable=mock_open)
@patch('glob.glob')
def test_updating_env_file_no_files(mock_glob, mock_dest_open):
    """Test updating an env file but no source files found."""
    mock_glob.return_value = []
    app.update_env_file('src/', 'dest/')
    mock_dest_open.assert_not_called()


@patch('os.makedirs')
@patch('builtins.open', new_callable=mock_open)
@patch('app.dotenv_values')
@patch('os.path')
@patch('glob.glob')
def test_updating_env_file_no_dest_path(mock_glob, mock_path, mock_dotenv,
                                        mock_dest_open, mock_makedirs):
    """Test updating an env file."""
    mock_glob.return_value = ['source.env']
    mock_path.exists.return_value = False
    mock_dotenv.side_effect = get_env_data
    app.update_env_file('src/', 'dest/')
    mock_makedirs.assert_called_with('dest/')
    mock_dest_open.assert_called_with('dest/.env', 'w')
    mock_dest_handle = mock_dest_open()
    mock_dest_handle.write.assert_has_calls(
        [call('a=1\n'), call('b=2\n'), call('c=asdf\n')],
        any_order=True)


@patch('argparse.ArgumentParser.parse_args',
       return_value=argparse.Namespace(source='src/', destination='dest/'))
@patch('app.update_env_file')
def test_main(mock_app, _):
    """Test main function."""
    app.main()
    mock_app.assert_called_with('src/', 'dest/')
