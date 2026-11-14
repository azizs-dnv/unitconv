from unitconv.cli import main


def test_cli_ok(capsys):
    assert main(["5", "km", "m"]) == 0
    assert "5 km = 5000 m" in capsys.readouterr().out


def test_cli_precision(capsys):
    assert main(["1", "mi", "km", "-p", "2"]) == 0
    assert "1 mi = 1.61 km" in capsys.readouterr().out


def test_cli_error(capsys):
    assert main(["1", "km", "kg"]) == 1
    assert "Error" in capsys.readouterr().err


def test_cli_list(capsys):
    assert main(["--list"]) == 0
    out = capsys.readouterr().out
    assert "length" in out and "pressure" in out


def test_cli_no_args():
    assert main([]) == 2
