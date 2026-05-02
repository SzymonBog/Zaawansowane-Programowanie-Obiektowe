# Stworzyć aplikację do zarządzania ustawieniami
# użytkownika, w której możliwe jest zapisanie i
# przywrócenie poprzedniej konfiguracji.


class MementoSettings:
    _states: list
    _i: int

    def __init__(self):
        self._states = []
        self._i = -1

    def save_state(self, state: list) -> None:
        if self._i != len(self._states) - 1:
            self._states = self._states[:self._i + 1]

        st = []

        for i in state:
            st.append(i)

        self._states.append(st)
        self._i += 1

    def undo(self) -> None:
        if self._i > 0:
            self._i -= 1

    def redo(self) -> None:
        if self._i < len(self._states) - 1:
            self._i += 1

    def read_state(self) -> list:
        return self._states[self._i]

    def print_states(self) -> None:
        print(self._states)

    def read_i(self):
        return self._i


current_settings = {
    "resolution": "1920x1080",
    "language": "English",
    "move_forward": "w",
    "move_back": "s",
    "move_left": "a",
    "move_right": "d",
    "interact": "e"
}

current_settings = ["1920x1080", "English", "w", "s", "a", "d", "e"]
c_s = ["resolution", "language", "move_forward", "move_back", "move_left", "move_right", "interact"]

settings = MementoSettings()
settings.save_state(current_settings)
settings.save_state(current_settings)
# print(settings.read_state())

while True:
    print(settings.read_i())
    print(settings.print_states())
    print("Current Settings:")
    # c_s_v = settings.read_state()

    for key, value in zip(c_s, current_settings):
        print(f"{key}: {value}")

    query = str(input("Choose:\n1 - change resolution\n2 - change language\n3 - change move_forward\n4 - change move_back\n5 - change move_left\n6 - change move_right\n7 - change interact\n8 - save changes\n9 - undo changes\n0 - redo changes\n10 - exit\n> "))

    if query == "1":
        while True:
            choice = str(input("Choose resolution:\n1 - 1280x720\n2 - 1920x1080\n3 - 2560x1440\n4 - 3840x2160\n5 - 7680x4320\n6 - back\n> "))
            if choice == "1":
                current_settings[0] = "1280x720"
            elif choice == "2":
                current_settings[0] = "1920x1080"
            elif choice == "3":
                current_settings[0] = "2560x1440"
            elif choice == "4":
                current_settings[0] = "3840x2160"
            elif choice == "5":
                current_settings[0] = "7680x4320"
            elif choice == "6":
                break
            else:
                print("Invalid Choice")

    elif query == "2":
        while True:
            choice = str(input("Choose language:\n1 - English\n2 - Polish\n3 - German\n4 - back\n> "))
            if choice == "1":
                current_settings[1] = "English"
            elif choice == "2":
                current_settings[1] = "Polish"
            elif choice == "3":
                current_settings[1] = "German"
            elif choice == "4":
                break
            else:
                print("Invalid Choice")

    elif query == "3":
        choice = str(input("Choose key for move_forward: "))
        if not choice in current_settings:
            current_settings[2] = choice
        else:
            print("Invalid Choice. Key is already in use")

    elif query == "4":
        choice = str(input("Choose key for move_back: "))
        if not choice in current_settings:
            current_settings[3] = choice
        else:
            print("Invalid Choice. Key is already in use")

    elif query == "5":
        choice = str(input("Choose key for move_left: "))
        if not choice in current_settings:
            current_settings[4] = choice
        else:
            print("Invalid Choice. Key is already in use")

    elif query == "6":
        choice = str(input("Choose key for move_right: "))
        if not choice in current_settings:
            current_settings[5] =  choice
        else:
            print("Invalid Choice. Key is already in use")

    elif query == "7":
        choice = str(input("Choose key for interact: "))
        if not choice in current_settings:
            current_settings[6] =  choice
        else:
            print("Invalid Choice. Key is already in use")

    elif query == "8":
        settings.save_state(current_settings)

    elif query == "9":
        settings.undo()
        current_settings = settings.read_state()

    elif query == "0":
        settings.redo()
        current_settings = settings.read_state()

    elif query == "10":
        break

    else:
        print("Invalid Choice")

# settings.print_states()


# ------------------------------------------------------------


class MementoPlayer:
    _states: list
    _i: int

    def __init__(self):
        self._states = []
        self._i = -1

    def save_state(self, state: list) -> None:
        if self._i != len(self._states) - 1:
            self._states = self._states[:self._i + 1]

        st = []

        for i in state:
            st.append(i)

        self._states.append(st)
        self._i += 1

    def read_state(self) -> list:
        return self._states[self._i]

    def print_states(self) -> None:
        print(self._states)


class Player:
    def __init__(self) -> None:
        self.values = [(0, 0, 0), 100, []]
        self.memento = MementoPlayer()

    def save(self):
        self.memento.save_state(self.values)
        print("Saved")

    def load(self):
        self.values = self.memento.read_state()

    def show_values(self):
        print(self.values)

    def print_states(self) -> None:
        self.memento.print_states()

    def set_position(self, x: int, y: int, z: int) -> None:
        self.values[0] = (x, y, z)

    def set_health(self, health: int) -> None:
        self.values[1] = health

    def set_inventory(self, inventory: list) -> None:
        self.values[2] = inventory


player = Player()
player.set_inventory(["health potion x3", "sword", "bow", "arrow x50"])
player.save()
player.set_health(10)
player.set_position(1102, 60, 9135)
player.show_values()
player.load()
player.show_values()


# ----------------------------------------------------------


class MementoForm:
    _states: list
    _i: int

    def __init__(self):
        self._states = []
        self._i = -1

    def save_state(self, state: list) -> None:
        if self._i != len(self._states) - 1:
            self._states = self._states[:self._i + 1]

        st = []

        for i in state:
            st.append(i)

        self._states.append(st)
        self._i += 1

    def undo(self) -> None:
        if self._i > 0:
            self._i -= 1

    def redo(self) -> None:
        if self._i < len(self._states) - 1:
            self._i += 1

    def read_state(self) -> list:
        return self._states[self._i]

    def print_states(self) -> None:
        print(self._states)

    def read_i(self):
        return self._i


class Form:
    def __init__(self):
        self.memento = MementoForm()
        self.answers = ["a", "c", "b", "b", "d", "d", "a", "c"]

    def save_state(self, state: list) -> None:
        self.memento.save_state(state)

    def undo(self) -> None:
        self.memento.undo()

    def change_answer(self, i: int, answer: str) -> None:
        self.answers[i] = answer
        self.save_state(self.answers)


f = Form()
f.save_state(f.answers)
print(f.memento.read_state())
f.change_answer(1, "a")
f.change_answer(2, "a")
print(f.memento.read_state())
f.undo()
print(f.memento.read_state())
