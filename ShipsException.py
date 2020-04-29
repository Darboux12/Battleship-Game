class Error(Exception):
    pass

class StartBeforePlacingShips(Error):
    def __init__(self):
        super().__init__('Start pressed before placing ships')

class ShipsTouching(Error):
    def __init__(self):
        super().__init__('Ships are touching')

class PlacingAlreadyPlaced(Error):
    def __init__(self):
        super().__init__('Attempt to place ship in already placed field')

class PlacingOnOponentBoard(Error):
    def __init__(self):
        super().__init__('Attempt to place ship on oponents board')

class PlacingElementNotConnectedWithShip(Error):
    def __init__(self):
        super().__init__('Element must link with the ship')

class ShootingOwnBoard(Error):
    def __init__(self):
        super().__init__('Attempt to shoot your own board')

class ShootingInAlreadyShooted(Error):
    def __init__(self):
        super().__init__('Attempt to shoot in already shooted field')


