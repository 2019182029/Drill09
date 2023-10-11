from pico2d import *


def a_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_a


def time_out(e):
    return e[0] == 'TIME_OUT'


class Idle:

    @staticmethod
    def enter(boy, event):
        print("Enter Idle")
        boy.x, boy.y = 400, 90
        boy.action = 3

    @staticmethod
    def exit(boy):
        print("Exit Idle")

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8

    @staticmethod
    def draw(boy):
        boy.image.clip_draw(boy.frame * 100, boy.action * 100, 100, 100, boy.x, boy.y)


class AutoRun:
    @staticmethod
    def enter(boy, event):
        print("Enter AutoRun")
        boy.a_up_time = get_time()
        boy.action = 0
        boy.dir = -10

    @staticmethod
    def exit(boy):
        print("Exit AutoRun")

    @staticmethod
    def do(boy):
        if (boy.x < 50 or boy.x > 750):
            boy.dir *= -1
        if (boy.x < 50):
            boy.action = 1
        elif (boy.x > 750):
            boy.action = 0
        boy.x += boy.dir

        boy.frame = (boy.frame + 1) % 8

        if (get_time() - boy.a_up_time > 5):
            boy.state_machine.handle_event(('TIME_OUT', 0))

    @staticmethod
    def draw(boy):
        boy.image.clip_draw(boy.frame * 100, boy.action * 100, 100, 100, boy.x, boy.y + 30, 200, 200)


class StateMachine:
    def __init__(self, boy):
        self.boy = boy
        self.cur_state = Idle
        self.transition = {
            Idle: {a_down: AutoRun},
            AutoRun: {time_out: Idle}
        }

    def start(self):
        self.cur_state.enter(self.boy, ('None', 0))

    def update(self):
        self.cur_state.do(self.boy)

    def draw(self):
        self.cur_state.draw(self.boy)

    def handle_event(self, event):
        for check_event, next_state in self.transition[self.cur_state].items():
            if check_event(event):
                self.cur_state.exit(self.boy)
                self.cur_state = next_state
                self.cur_state.enter(self.boy, event)
                return True
        return False


class Boy:
    def __init__(self):
        self.x, self.y = 400, 90
        self.frame = 0
        self.action = 3
        self.image = load_image('animation_sheet.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start()

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()
