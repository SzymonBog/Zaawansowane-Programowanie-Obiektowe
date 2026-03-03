class Robot:
    def operate(self):
        return "Performing task"


class AI:
    def think(self):
        return "Processing data"


class Android(Robot, AI):
    def self_learn(self):
        pass


r = Robot()
ai = AI()
a = Android()
print(f"{r.operate()} {ai.think()} {a.think()} {a.operate()} {a.self_learn()}")
