from modules.zeroia.state.zeroia_state import load_state, save_state


def test_save_and_load_state(tmp_path):
    test_data = {"status": {"active": True, "confidence": 0.95}}
    test_file = tmp_path / "test_state.toml"

    save_state(test_file, test_data)
    loaded = load_state(test_file)

    assert loaded == test_data
