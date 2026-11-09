"""Проверки за задача 2.3: поправената load_config.

Пускане:  python -m pytest urok-2-funkcii-danni-izklyucheniya/2.3-lovets-na-goli-except -v

Поправената функция:
  * чете файла с явно кодиране UTF-8 и го затваря сама;
  * пропуска празни редове и редове, започващи с #;
  * маха интервалите около ключа и стойността;
  * вдига ValueError при повреден ред, вместо да връща {};
  * НЕ прехваща FileNotFoundError — какво да се прави при липсващ файл,
    решава викащият код.
"""
import pytest

from load_config import load_config


def napishi(tmp_path, text):
    path = tmp_path / "config.txt"
    path.write_text(text, encoding="utf-8")
    return path


def test_dobar_fail(tmp_path):
    path = napishi(tmp_path, "брой_въпроси=10\nточки_за_верен=2\n")
    assert load_config(path) == {"брой_въпроси": 10, "точки_за_верен": 2}


def test_intervali_okolo_znaka_ravno(tmp_path):
    path = napishi(tmp_path, "секунди_за_отговор = 30\n")
    assert load_config(path) == {"секунди_за_отговор": 30}


def test_prazni_redove_i_komentari_se_propuskat(tmp_path):
    path = napishi(tmp_path, "# коментар\n\nброй=5\n\n")
    assert load_config(path) == {"брой": 5}


def test_lipsvasht_fail_ne_se_preglashta(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_config(tmp_path / "nyama_takav.txt")


def test_red_bez_ravno_vdiga_valueerror(tmp_path):
    path = napishi(tmp_path, "брой=5\nточки 2\n")
    with pytest.raises(ValueError):
        load_config(path)


def test_stoynost_koyato_ne_e_chislo_vdiga_valueerror(tmp_path):
    path = napishi(tmp_path, "секунди=трийсет\n")
    with pytest.raises(ValueError):
        load_config(path)


def test_suobshtenieto_kazva_koy_red(tmp_path):
    path = napishi(tmp_path, "брой=5\n# коментар\nсекунди=трийсет\n")
    with pytest.raises(ValueError, match="3"):
        load_config(path)


def test_ctrl_c_ne_se_preglashta(tmp_path, monkeypatch):
    """Голото except: хваща и KeyboardInterrupt. Поправената версия не бива."""
    import builtins
    import io

    path = napishi(tmp_path, "брой=5\n")

    def prekasnato(*args, **kwargs):
        raise KeyboardInterrupt

    monkeypatch.setattr(builtins, "open", prekasnato)
    monkeypatch.setattr(io, "open", prekasnato)
    with pytest.raises(KeyboardInterrupt):
        load_config(path)
