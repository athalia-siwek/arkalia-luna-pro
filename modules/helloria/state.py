import toml


class HelloriaStateManager:
    def __init__(self, path="state/helloria_state.toml"):
        self.path = path
        self.state = {}

    def load(self):
        try:
            self.state = toml.load(self.path)
        except FileNotFoundError:
            self.state = {}

    def save(self):
        with open(self.path, "w") as f:
            toml.dump(self.state, f)


IS_HELLORIA = True
