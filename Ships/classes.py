class Battleship:
    def __init__(self, **kwargs):
        self.length = kwargs['length']
        self.orientation = kwargs['orientation']
        self.placing = kwargs['placing']
        self.area_around_ship = kwargs['area_around_ship']
        self.destroyed_deсks = []
