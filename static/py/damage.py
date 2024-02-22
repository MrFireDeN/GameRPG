# Список типов урона
DAMAGE_TYPES = {'Режущий', 'Колющий', 'Дробящий', 'Огненный', 'Ледяной', 'Отравляющий', 'Электрический'}

class Damage:
    def __init__(self, slash: int = 0, pierce: int = 0, blunt: int = 0,
                 fire: int = 0, ice: int = 0, poison: int = 0, electric: int = 0):
        self._slash = slash
        self._pierce = pierce
        self._blunt = blunt
        self._fire = fire
        self._ice = ice
        self._poison = poison
        self._electric = electric

    @staticmethod
    def calculate_damage(weapon_damage: 'Damage', weapon_level: int, armor_defence: 'Damage', armor_level: int):
        total_damage = (
                max(0, (weapon_damage.slash * weapon_level - armor_defence.slash * armor_level)) +
                max(0, (weapon_damage.pierce * weapon_level - armor_defence.pierce * armor_level)) +
                max(0, (weapon_damage.blunt * weapon_level - armor_defence.blunt * armor_level)) +
                max(0, (weapon_damage.fire * weapon_level - armor_defence.fire * armor_level)) +
                max(0, (weapon_damage.ice * weapon_level - armor_defence.ice * armor_level)) +
                max(0, (weapon_damage.poison * weapon_level - armor_defence.poison * armor_level)) +
                max(0, (weapon_damage.electric * weapon_level - armor_defence.electric * armor_level))

        )
        return total_damage

    @property
    def slash(self):
        return self._slash

    @slash.setter
    def slash(self, value):
        self._slash = min(value, 100)

    @property
    def pierce(self):
        return self._pierce

    @pierce.setter
    def pierce(self, value):
        self._pierce = min(value, 100)

    @property
    def blunt(self):
        return self._blunt

    @blunt.setter
    def blunt(self, value):
        self._blunt = min(value, 100)

    @property
    def fire(self):
        return self._fire

    @fire.setter
    def fire(self, value):
        self._fire = min(value, 100)

    @property
    def ice(self):
        return self._ice

    @ice.setter
    def ice(self, value):
        self._ice = min(value, 100)

    @property
    def poison(self):
        return self._poison

    @poison.setter
    def poison(self, value):
        self._poison = min(value, 100)

    @property
    def electric(self):
        return self._electric

    @electric.setter
    def electric(self, value):
        self._electric = min(value, 100)