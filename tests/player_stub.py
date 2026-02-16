class Player:
    """
    Test stub representing a Player.
    """

    def __init__(
        self,
        id=None,
        first_name=None,
        middle_name=None,
        last_name=None,
        date_of_birth=None,
        squad_number=None,
        position=None,
        abbr_position=None,
        team=None,
        league=None,
        starting11=None,
    ):
        self.id = id
        self.first_name = first_name
        self.middle_name = middle_name
        self.last_name = last_name
        self.date_of_birth = date_of_birth
        self.squad_number = squad_number
        self.position = position
        self.abbr_position = abbr_position
        self.team = team
        self.league = league
        self.starting11 = starting11


def existing_player():
    """
    Creates a test stub for an existing Player.
    """
    return Player(
        id=1,
        first_name="Damián",
        middle_name="Emiliano",
        last_name="Martínez",
        date_of_birth="1992-09-02T00:00:00.000Z",
        squad_number=23,
        position="Goalkeeper",
        abbr_position="GK",
        team="Aston Villa FC",
        league="Premier League",
        starting11=1,
    )


def nonexistent_player():
    """
    Creates a test stub for a nonexistent (new) Player.
    """
    return Player(
        id=24,
        first_name="Thiago",
        middle_name="Ezequiel",
        last_name="Almada",
        date_of_birth="2001-04-26T00:00:00.000Z",
        squad_number=16,
        position="Attacking Midfield",
        abbr_position="AM",
        team="Atlanta United FC",
        league="Major League Soccer",
        starting11=0,
    )


def unknown_player():
    """
    Creates a test stub for an unknown Player.
    """
    return Player(
        id=999,
        first_name="John",
        last_name="Doe",
        squad_number="999",
        position="Lipsum",
    )
