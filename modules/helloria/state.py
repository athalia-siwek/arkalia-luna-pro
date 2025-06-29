import toml


class HelloriaStateManager:
    def __init__(self, path="state/helloria_state.toml") -> None:
        self.path = path
        self.state = {}

    def load(self) -> None:
        try:
            self.state = toml.load(self.path)
        except FileNotFoundError:
            self.state = {}

    def save(self) -> None:
        with open(self.path, "w") as f:
            toml.dump(self.state, f)


IS_HELLORIA = True
