from abc import ABC, abstractmethod
from kink import inject
from random import randint

from dtos import LoginDTO, RegisterDTO, SwitchSceneDTO, WarningDTO
from persistences import DashSqlDb


@inject
class ServiceGameplay:
    ground_level = 250

    def __init__(self, _dash_db: DashSqlDb):
        self.dash_db = _dash_db
        self.ground_level = 0
        self.player_username = ""
        self.player_velocity = 0
        self.player_position_y = 60
        self.player_is_jumping = True
        self.player_score = 0

    def reset(self, _username: str):
        self.ground_level = 0
        self.player_username = _username
        self.player_velocity = 0
        self.player_position_y = 60
        self.player_is_jumping = True
        self.player_score = 0

    def play_mouse_click(self):
        if not self.player_is_jumping:
            self.player_is_jumping = True
            self.player_velocity = -55

    def update(self):
        self.player_velocity += 6
        self.player_position_y += self.player_velocity

        if self.player_position_y > ServiceGameplay.ground_level:  # if player is lower than ground
            # then set player on ground
            self.player_position_y = ServiceGameplay.ground_level
            self.player_is_jumping = False

        if randint(0, 60) == 0:  # remove later
            print("SCORE")
            self.player_score += 1

    def update_point(self):
        # temp_count_point = 0
        # # if player pass obstacle then point += 1
        # temp_count_point += 1
        # # set to score after game over
        # self.db.score = temp_count_point
        pass


@inject
class ServiceRegister:
    def __init__(self, _dash_db: DashSqlDb, _service_gameplay: ServiceGameplay):
        self.dash_db = _dash_db
        self.service_gameplay = _service_gameplay

    # bagian user data
    def register_acc(self, _register_dto: RegisterDTO) -> (SwitchSceneDTO | WarningDTO):  # need to be revised
        temp_username = _register_dto.username
        temp_email = _register_dto.email

        # jika username/email tidak diisi
        if len(temp_username) == 0:
            return WarningDTO(WarningDTO.username_empty)
        if len(temp_email) == 0:
            return WarningDTO(WarningDTO.email_empty)

        # jika email invalid
        if temp_email[len(temp_email) - 10:len(temp_email)] != "@gmail.com":
            return WarningDTO(WarningDTO.email_invalid)

        # jika username sudah ada di database
        if self.check_username_in_db(temp_username) is True:
            return WarningDTO(WarningDTO.username_already_registered)

        # jika username tidak ada di database
        self.dash_db.register_acc(_register_dto)
        self.service_gameplay.reset(temp_username)
        return SwitchSceneDTO("gameplay")

    def login_acc(self, _login_dto: LoginDTO) -> (SwitchSceneDTO | WarningDTO):  # need to be revised
        temp_username = _login_dto.username

        # jika username tidak diisi
        if len(temp_username) == 0:
            return WarningDTO(WarningDTO.username_empty)

        # jika username sudah ada di database
        if self.check_username_in_db(temp_username) is True:
            self.dash_db.login_acc(temp_username)
            self.service_gameplay.reset(temp_username)
            return SwitchSceneDTO("gameplay")

        # jika username tidak ada di database
        return WarningDTO(WarningDTO.username_not_registered)

    def check_username_in_db(self, _username: str):
        # jika username tidak ada di database
        if self.dash_db.search_player(_username) == []:
            return False

        # jika username sudah ada di database
        return True


@inject
class ServiceHighScore:
    def __init__(self, _dash_db: DashSqlDb, _service_gameplay: ServiceGameplay):
        self.dash_db = _dash_db
        self.service_gameplay = _service_gameplay
    
    def get_leaderboards(self):
        return self.dash_db.get_leaderboards()

@inject
class DashService:
    def __init__(self, _service_register: ServiceRegister, _service_gameplay: ServiceGameplay, _service_highscore: ServiceHighScore):
        self.service_register = _service_register
        self.service_gameplay = _service_gameplay
        self.service_highscore = _service_highscore

    def get_leaderboards(self):
        return self.dash_db.get_leaderboards()

    def set_high_score(self, _username: str, _score: int):  # need to be revised
        return self.dash_db.set_high_scores(_username, _score)
        

# Observer Pattern
class ILeaderboardsNotify(ABC):
    @abstractmethod
    def notified(self):
        pass


@inject(alias=ILeaderboardsNotify)
class NotifyIFReachLeaderboards(ILeaderboardsNotify):
    def notified(self):
        print('Congratulations on reaching the leaderboards')


@inject(alias=ILeaderboardsNotify)
class NotifyIfDropFromLeaderboards(ILeaderboardsNotify):
    def notified(self):
        print('Oh no, you exit the leaderboards')


@inject(alias=ILeaderboardsNotify)
class NotifyIfPassCertainLimit(ILeaderboardsNotify):
    def notified(self):
        # if score >= 100 (cek setiap update score, berarti kalau game over cek score terakhirnya panggil method ini)
        print('Congratulations, your score has reached 100. Here are your rewards')


@inject
class LeaderboardsSubject:
    def __init__(self, _observers: list[ILeaderboardsNotify]):
        self.observers = _observers

    def notify(self):
        for observer in self.observers:
            # observer.notified()
            pass
