
class Human:
    # Human_left_arm : "Human_arm"
    # Human_right_arm : "Human_arm"
    # Human_body : "Human_body"
    # Human_left_leg : "Human_leg"
    # Human_right_leg : "Human_leg"


    def __init__(self):
        self.Human_body = Human_body()
        self.Human_body.setposition(5, 5)

        self.Human_left_arm = Human_arm()
        self.Human_left_arm.setposition(5,0)

        self.Human_right_arm = Human_arm()
        self.Human_right_arm.setposition(5,10)

        self.Human_left_leg = Human_leg()
        self.Human_left_leg.setposition(0,0)

        self.Human_right_leg = Human_leg()
        self.Human_right_leg.setposition(0,10)

    def print_position(self):
        print(self.Human_body.x)
        print(self.Human_body.y)







class Human_component:
    def __init__(self):
        self.x = 0
        self.y = 0

    def setposition(self, x, y):
        self.x = x
        self.y = y

class Human_arm(Human_component):

    def __init__(self):
        super().__init__()

class Human_body(Human_component):

    def __init__(self):
        super().__init__()

class Human_leg(Human_component):

    def __init__(self):
        super().__init__()

if __name__ == "__main__":
    tom = Human()
    tom.print_position()