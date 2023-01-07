from collections import UserDict

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

class Record:
    phones = []
    def __init__(self, name, phone=None):
        self.name = name
        if phone:
            self.phones.append(phone)

    def has_phone(self, phone):
        index = None
        for i in range(self.phones):
            if self.phones[i].value == phone.value:
                index = i
                break
        return index

    def add_phone(self, phone):
        if self.has_phone(phone) is not None:
            self.phones.append(phone)
        else:
            # exception
            pass

    def delete_phone(self, phone):
        index_to_remove = self.has_phone(phone)
        if index_to_remove is not None:
            self.phones.pop(index_to_remove)
        else:
            # exception
            pass

    def change_name(self, name):
        self.name = name

    def change_phone(self, phone):
        self.phones = []
        self.add_phone(phone)

class Field:
    def __init__(self, value):
        self.value = value

class Name(Field):
    pass

class Phone(Field):
    pass

if __name__ == "__main__":
    name = Name('Bill')
    phone = Phone('1234567890')
    rec = Record(name, phone)
    ab = AddressBook()
    ab.add_record(rec)
        
    assert isinstance(ab['Bill'], Record)
    assert isinstance(ab['Bill'].name, Name)
    assert isinstance(ab['Bill'].phones, list)
    assert isinstance(ab['Bill'].phones[0], Phone)
    assert ab['Bill'].phones[0].value == '1234567890'
        
    print('All Ok)')