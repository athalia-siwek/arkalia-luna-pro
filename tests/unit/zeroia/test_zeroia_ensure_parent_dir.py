# 🧪 Tests pour la fonction ensure_parent_dir de ZeroIA
import os
from pathlib import Path

from modules.zeroia.reason_loop import ensure_parent_dir
from tests.common.helpers import ensure_test_toml

ensure_test_toml()


def test_ensure_parent_dir_with_file_path(tmp_path):
    """🧠 Test ensure_parent_dir avec un chemin de fichier"""
    file_path = tmp_path / "subdir" / "subsubdir" / "file.txt"

    # Les répertoires parents n'existent pas encore
    assert not file_path.parent.exists()

    ensure_parent_dir(file_path)

    # Les répertoires parents doivent maintenant exister
    assert file_path.parent.exists()
    assert file_path.parent.is_dir()


def test_ensure_parent_dir_with_directory_path(tmp_path):
    """🧠 Test ensure_parent_dir avec un chemin de répertoire (sans extension)"""
    dir_path = tmp_path / "subdir" / "subsubdir" / "finaldir"

    # Le répertoire n'existe pas encore
    assert not dir_path.exists()

    ensure_parent_dir(dir_path)

    # Le répertoire complet doit maintenant exister
    assert dir_path.exists()
    assert dir_path.is_dir()


def test_ensure_parent_dir_existing_directory(tmp_path):
    """🧠 Test ensure_parent_dir quand le répertoire existe déjà"""
    existing_dir = tmp_path / "existing"
    existing_dir.mkdir()
    file_path = existing_dir / "file.txt"

    # Ne doit pas lever d'erreur même si le répertoire existe déjà
    ensure_parent_dir(file_path)

    # Le répertoire doit toujours exister
    assert existing_dir.exists()
    assert existing_dir.is_dir()


def test_ensure_parent_dir_nested_directories(tmp_path):
    """🧠 Test ensure_parent_dir avec plusieurs niveaux de répertoires imbriqués"""
    deep_file_path = tmp_path / "level1" / "level2" / "level3" / "level4" / "file.log"

    # Aucun des répertoires n'existe
    assert not (tmp_path / "level1").exists()

    ensure_parent_dir(deep_file_path)

    # Tous les répertoires parents doivent exister
    assert (tmp_path / "level1").exists()
    assert (tmp_path / "level1" / "level2").exists()
    assert (tmp_path / "level1" / "level2" / "level3").exists()
    assert (tmp_path / "level1" / "level2" / "level3" / "level4").exists()


def test_ensure_parent_dir_with_suffix_detection(tmp_path):
    """🧠 Test que ensure_parent_dir détecte correctement les fichiers avec extension"""
    # Fichiers avec différentes extensions
    file_extensions = [".txt", ".log", ".toml", ".json", ".py", ".md"]

    for ext in file_extensions:
        file_path = tmp_path / "testdir" / f"testfile{ext}"
        parent_before = file_path.parent

        ensure_parent_dir(file_path)

        # Le répertoire parent doit exister, pas le fichier lui-même
        assert parent_before.exists()
        assert parent_before.is_dir()
        assert not file_path.exists()  # Le fichier lui-même ne doit pas être créé


def test_ensure_parent_dir_without_suffix(tmp_path):
    """🧠 Test ensure_parent_dir avec un path sans extension (traité comme répertoire)"""
    dir_path = tmp_path / "no_extension_dir"

    ensure_parent_dir(dir_path)

    # Le chemin complet doit être créé comme répertoire
    assert dir_path.exists()
    assert dir_path.is_dir()


def test_ensure_parent_dir_root_path():
    """🧠 Test ensure_parent_dir avec un chemin racine (ne doit pas planter)"""
    root_file = Path("/root_file.txt")

    # Ne doit pas lever d'erreur même avec un chemin racine
    try:
        ensure_parent_dir(root_file)
        # Si on arrive ici, la fonction a géré le cas gracieusement
        assert True
    except PermissionError:
        # C'est attendu si on n'a pas les permissions root
        assert True
    except Exception as e:
        # Autres exceptions non attendues
        assert False, f"Unexpected exception: {e}"


def test_ensure_parent_dir_relative_path(tmp_path):
    """🧠 Test ensure_parent_dir avec un chemin relatif"""
    # Change vers le répertoire temporaire
    original_cwd = os.getcwd()
    try:
        os.chdir(tmp_path)

        relative_file = Path("relative/path/file.txt")

        ensure_parent_dir(relative_file)

        # Les répertoires relatifs doivent être créés
        assert (tmp_path / "relative").exists()
        assert (tmp_path / "relative" / "path").exists()

    finally:
        # Remet le répertoire de travail original
        os.chdir(original_cwd)


def test_ensure_parent_dir_with_dots_in_path(tmp_path):
    """🧠 Test ensure_parent_dir avec des points dans le nom de répertoire"""
    file_path = tmp_path / "dir.with.dots" / "subdir.also.dots" / "file.txt"

    ensure_parent_dir(file_path)

    # Les répertoires avec des points doivent être créés correctement
    assert (tmp_path / "dir.with.dots").exists()
    assert (tmp_path / "dir.with.dots" / "subdir.also.dots").exists()


def test_ensure_parent_dir_multiple_calls_same_path(tmp_path):
    """🧠 Test d'appels multiples à ensure_parent_dir sur le même chemin"""
    file_path = tmp_path / "repeated" / "calls" / "file.txt"

    # Premier appel
    ensure_parent_dir(file_path)
    assert file_path.parent.exists()

    # Deuxième appel - ne doit pas planter
    ensure_parent_dir(file_path)
    assert file_path.parent.exists()

    # Troisième appel - toujours OK
    ensure_parent_dir(file_path)
    assert file_path.parent.exists()


def test_ensure_parent_dir_empty_path():
    """🧠 Test ensure_parent_dir avec un Path vide"""
    empty_path = Path("")

    # Ne doit pas planter avec un chemin vide
    try:
        ensure_parent_dir(empty_path)
        assert True
    except Exception as e:
        # Si une exception est levée, elle doit être gérée gracieusement
        assert isinstance(
            e, (OSError, ValueError)
        ), f"Unexpected exception type: {type(e)}"
