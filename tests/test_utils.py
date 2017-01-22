from language_detection import utils

def test_parse_unknown_args_with_values():
    arguments = ['--languages', 'it', '--error_values', '1000', '2000']
    expected = {'languages': 'it', 'error_values': ['1000', '2000']}

    assert utils.parse_unknown_args_with_values(arguments) == expected
