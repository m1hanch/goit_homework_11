import calendar
from collections import UserDict
from datetime import datetime


class Field:
    pass


class Phone(Field):
    def __init__(self, phone: str):
        self.__value = None
        self.phone = phone

    @property
    def phone(self):
        return self.__value

    @phone.setter
    def phone(self, new_phone):
        if len(new_phone) == 10 and new_phone.isdigit():
            self.__value = new_phone
        else:
            raise ValueError("Incorrect phone number! It must contain exactly 10 numbers.")


class Name(Field):
    def __init__(self, name: str):
        self.__value = None
        self.name = name.capitalize()

    @property
    def name(self):
        return self.__value

    @name.setter
    def name(self, new_name):
        if new_name.isalpha():
            self.__value = new_name.capitalize()
        else:
            raise ValueError('Name can contain only letters!')


class Birthday:
    def __init__(self, birthday: str):
        #Перевірка правильності формату дати
        try:
            bday = datetime.strptime(birthday, '%d.%m.%Y')
        except ValueError:
            print('Wrong date format! Please provide correct form dd.mm.yyyy')
            quit()

        #Перевірка реальності дати
        if bday.date() > datetime.now().date() or bday.year <= bday.year - 120:
            print('Unrealistic date! Provide the real one.')
            quit()
        else:
            self.birthday = birthday


class Record:
    def __init__(self, name: Name, *phone: Phone, birthday = None):
        if len(phone) == 0:
            phone = []
        self.Name = name
        self.phones = list(phone)
        self.bday = birthday

    #функція додавання телефону
    def add_phone(self, phone: Phone):
        self.phones.append(phone)

    #функція вилучення телефону
    def remove_phone(self, phone: Phone):
        for ph in self.phones:
            if ph.phone == phone.phone:
                self.phones.remove(ph)

    #функція зміни телефону
    def edit_phone(self, old_phone: str, new_phone: str):
        for phone in self.phones:
            if old_phone == phone.phone:
                phone.phone = new_phone

    #функіця, яка рахує кількість днів до наступного дня народження даного контакту
    def days_to_birthday(self) -> int:
        if self.bday is not None:
            bday = self.bday.birthday[:-4] + str(datetime.now().year)
            bday = datetime.strptime(bday, '%d.%m.%Y')
            now = datetime.now()
            result = bday.toordinal() - now.toordinal() #обчислення різниці днів між двома датами у поточному році
            if result < 0 and calendar.isleap(now.year):
                result += 366
            elif result < 0 and not calendar.isleap(now.year):
                result += 365
            return result

class AddressBook(UserDict):
    def __init__(self, N=1):
        super().__init__()
        self.N = N  # # Кількість записів, які повертаються за одну ітерацію
    def list_contacts(self) -> dict:
        return self.data

    def add_record(self, record: Record):
        self.data.update({record.name.name.capitalize(): record})

    # повертає список об'єктів phone
    def get_contact(self, name: str) -> list:
        return self.data.get(name.capitalize()).phones

    # видаляє контакт
    def remove_contact(self, name: str):
        self.data.pop(name.capitalize())

    def __iter__(self):
        iter_list = list(self.data.items())
        grouped = [iter_list[n:n+self.N] for n in range(0, len(iter_list),self.N)]
        return (group for group in grouped)