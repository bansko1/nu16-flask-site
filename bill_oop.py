class Bill:
    
    def __init__(self, name):
        self.name = name
        self._money = 0
        #print(f'Открываем {self}.')

    def __str__(self):
        return f'Счет игрока {self.name}'

    @property
    def money(self):
        return self._money
    
    @money.setter
    def money(self, new_money):
        if new_money < 0:
            raise ValueError('Сумма на счете не может быть отрицательной.')
        self._money = new_money
    
    def add(self, count):
        self.money += count
        #print(f'Вносим на {self} {count} единиц.')
    
    def bet(self, count):
        self.money -= count
        #print(f'Со {self} делаем ставку на {count} единиц.')