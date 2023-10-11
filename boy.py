from pico2d import *


# 1. AutoRun 클래스를 추가하여 'a'키를 눌렀을 때 키 조작 없이도 캐릭터가 움직이는 것을 구현한다.
# 2. 자동 무적 런 상태에서 5초 이상 경과했을 때 IDLE 상태로 돌아가는 것을 구현한다.
# 3. 캐릭터의 속도와 크기를 증가시키고, 화면의 좌우측 끝에서 자동으로 방향 전환하는 것을 구현한다.


def a_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_a


def a_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_a


def time_out(e):
    return e[0] == 'TIME_OUT'


class Idle:

    @staticmethod
    def enter(boy):
        print("Enter Idle")

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
    def enter(boy):
        print("Enter AutoRun")

    @staticmethod
    def exit(boy):
        print("Exit AutoRun")

    @staticmethod
    def do(boy):
        print("Do AutoRun")

    @staticmethod
    def draw(boy):
        pass


class StateMachine:
    def __init__(self, boy):
        self.boy = boy
        self.cur_state = Idle
        self.transition = {
            Idle: {a_down: AutoRun},
            AutoRun: {a_up: Idle}
        }

    def start(self):
        self.cur_state.enter(self.boy)

    def update(self):
        self.cur_state.do(self.boy)

    def draw(self):
        self.cur_state.draw(self.boy)

    def handle_event(self, event):
        for check_event, next_state in self.transition[self.cur_state].items():
            if check_event(event):
                self.cur_state.exit(self.boy)
                self.cur_state = next_state
                self.cur_state.enter(self.boy)
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
