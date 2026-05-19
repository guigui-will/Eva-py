class EvaNil:
    def default_value(self):
        return None

    def __str__(self):
        return 'nil'

    def __repr__(self):
        return 'EvaNil()'

    def __bool__(self):
        return False

    def __int__(self):
        return 0

    def __float__(self):
        return 0.0
