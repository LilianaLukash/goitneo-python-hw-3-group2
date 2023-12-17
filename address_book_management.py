from collections import UserDict
from collections import defaultdict
from datetime import datetime, timedelta

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Phone number must be 10 digits")
        super().__init__(value)

class Record:
    def __init__(self, name, birthday = None):
        self.name = Name(name)
        self.phones = []

        self.birthday = None

        if birthday:
            self.add_birthday(birthday)
         
    def add_birthday(self, birthday):
        try:
            self.birthday = datetime.strptime(birthday, "%d.%m.%Y").date()
            return f"Birthday of {self.name} is {self.birthday}."
        except ValueError:
            return f"Wrong data for birthday {birthday}. Please enter it in format DD.MM.YYYY"
    
    def show_birthday(self):
        if self.birthday:
            return f'Birthday of {self.name} is {self.birthday}'
        else:
            return f'We don\'t know birthday of {self.name}'

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)
                break 
        
    def edit_phone(self, old_phone, new_phone):
        for p in self.phones:
            if p.value == old_phone:
                p.value = new_phone
                break

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

class AddressBook(UserDict):
    def add_record(self, name, phone, birthday = None):
        record = Record(name, birthday)
        record.add_phone(phone)
        self.data[name] = record
        self.birthday = birthday
        
    def find_record(self, name):  
        return self.data.get(name)

    def remove_record(self, name):
        if name in self.data:
            del self.data[name]

    def birthdays(self):
        today = datetime.today().date()
        birthdays = defaultdict(list)

        for record in self.data.values():
            if record.birthday: 
                name = record.name.value
                birthday = record.birthday
                birthday_this_year = birthday.replace(year=today.year)

                if birthday_this_year < today:
                    birthday_this_year = birthday_this_year.replace(year=today.year + 1)

                delta_days = (birthday_this_year - today).days

                if 0 <= delta_days < 7:
                    birthday_weekday = birthday_this_year.strftime("%A")
                    if birthday_weekday in ["Saturday", "Sunday"]:
                        birthday_weekday = "Monday"
                    birthdays[birthday_weekday].append(name)

        for day, names in birthdays.items():
            print(f"{day}: {', '.join(names)}")



def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

def main():
    book = AddressBook({})
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break

        elif command == 'add':
            book.add_record(*args)
            print(f'New record added {list(book)[-1]}')
        
        elif command == 'find':
            print(book.find_record(*args))

        elif command == 'remove':
            book.remove_record(*args)
            print(f'Record removed. Record left {book}')
        
        elif command == "editphone":
            if len(args) >= 3:
                record = book.find_record(args[0])
                if record:
                    old_phone = args[1]
                    new_phone = args[2]
                    record.edit_phone(old_phone, new_phone)
                    print(f"Phone number for {args[0]} has been updated.")
                else:
                    print(f"Record for {args[0]} not found.")
            else:
                print("Not enough arguments for editphone.")

           
        elif command == "addphone":
            record = book.find_record(args[0])
            if record:
                    record.add_phone(args[1])
                    print(f'Phone added. Phones of {record.name} {", ".join(str(phone.value) for phone in record.phones)}')
            else:
                print("No such name in the records")
        
        elif command == "remove_phone":
            record = book.find_record(args[0])
            if record:
                    record.add_phone(args[1])
                    print('Phone removed')
            else: 
                print("No such name in the records")

        elif command == "addbirthday":
            record = book.find_record(args[0])
            if record:
                print(record.add_birthday(args[1]))
            else: 
                print("No such name in the records")

        elif command == "show_birthday":
            record = book.find_record(args[0])
            if record:
                print(record.show_birthday())
            else: 
                print("No such name in the records")
        
        elif command == "birthdays":
            book.birthdays()

        elif command == "hello":
            print("I am soo happy to meet you, come here, let me kiss you!")

if __name__ == "__main__":
    main()

            

