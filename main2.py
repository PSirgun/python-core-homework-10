from collections import UserDict
import re
class MyError(Exception):
    pass

class MyError2(Exception):
    pass

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    def __init__(self, value):
        super().__init__(value)
   

class Phone(Field):
    def __init__(self, value):
        phone1 = re.findall('\d+', value)
        value = ''.join(phone1)
        if not len(value) == 10 or not value.isdigit():
            raise ValueError
        super().__init__(value)
        
    def __str__(self):
        return self.value

class Record:
    
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone):
        phone_number = Phone(phone)
        if phone_number.value not in [p.value for p in self.phones]:
            self.phones.append(phone_number)
        else:
            raise MyError
    
    def remove_phone(self, phone):
        if phone.value in [p.value for p in self.phones]:
            self.phones = [p for p in self.phones if p.value != phone.value]
        else:
            raise MyError2
            
    def edit_phone(self, old_phone, new_phone):
        
        for i, phone in enumerate(self.phones):
            if phone.value == Phone(old_phone).value:
                self.phones[i] = Phone(new_phone)
                return
            raise ValueError

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p

            
    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"



class AddressBook(UserDict):
    def add_record(self, contact: Record):
        self.data[contact.name.value] = contact

    def find(self, name):
        if name:
            return self.data.get(name)
        else:
            return

    def delete(self, name):
        if name in self.data:
            del self.data[name]



phone_book = AddressBook()


def decor_func(func):
    def inner(*args):
        try:
            return func(*args)
        except IndexError:
            return "Not enough arguments"
        except KeyError:
            return "Name not in phone book"
        except TypeError:
                return "Too much arguments"
        except ValueError:
            return "Invalid phone number format"
        except AttributeError:
            return "Name not in phone book"
        except MyError:
            return "Phone already in phone book"
        except MyError2:
            return "Phone not in phone book"
    return inner

def decor_change(func):
    def inner(*args):
        try:
            return func(*args)
        except IndexError:
            return "Not enough arguments"
        except TypeError:
            return "No one argument"
        except ValueError:
            return "Incorrect phone number"
        except AttributeError:
            return "Name not in phone book"
    return inner



# sub block -------------------------------------------------------------------------------------------------------
@decor_func
def sub_add(*args):
    args = list(sanit_name(*args))
    if phone_book.find(args[0]):
        add_ph = phone_book[args[0]]
        add_ph.add_phone(args[1])
    else:
        add_ph = Record(args[0])
        add_ph.add_phone(args[1])
        phone_book.add_record(add_ph)
    
    return f" Added {args[0]} - {Phone(args[1])} to phone book "

@decor_func   
def sub_show():
    pr_contacts = "All contacts \n"
    for name, contact in phone_book.items():
        pr_contacts += f"{contact} \n"
    return pr_contacts

@decor_change
def sub_change(*args):
    args = list(sanit_name(*args))
    contact = phone_book.find(args[0]) 
    contact.edit_phone(args[1], args[2])
    return f" For {args[0]} changed {Phone(args[1])} to {args[2]}"

@decor_func 
def sub_phone(*args):
    args = list(sanit_name(*args))
    contact = phone_book.find(args[0].title()) 
    return (f'{contact}')

@decor_func
def sub_hello():
    return "How can I help you?"

@decor_func
def sub_exit():
    return "Good bye!"

def sub_delete(*args):
    args = list(sanit_name(*args))
    phone_book.delete(args[0].title())
    return f'{args[0]} deleted from phone book'

@decor_func
def sub_remove_phone(*args):
    args = list(sanit_name(*args))
    phone = Phone(args[1])
    contact = phone_book.find(args[0].title()) 
    contact.remove_phone(phone)
    return f"For {args[0]} phone number {phone} removed"


OPERATIONS = {
    sub_remove_phone : ("remove phone",),
    sub_delete : ("delete", ),
    sub_hello : ("hello",), 
    sub_add : ("add",),
    sub_change : ("change",),
    sub_phone : ("phone",),
    sub_show : ("show all",),
    sub_exit: ("good bye", "close", "exit", ".")
}
# end sub block ---------------------------------------------------------------------------------------------------

def sanit_phone(bad_phone):
        phone1 = re.findall('\d+', bad_phone)
        phone2 = ''.join(phone1)
        if len(phone2) >= 10:
            return phone2

def sanit_name(*args):
    ful_name = ""
    args = list(args)
    for i in args:
        if not re.search(r'(\d|\+)',i):
            ful_name += i + ' '       
        else:
            args = args[args.index(i):]
            args.insert(0, ful_name.strip().title())
            break
    return args

def main():
    while True:
        user_input = input(">>> ")
        command_found = False        
        for sub_f, command  in OPERATIONS.items():
            if command_found:
                break 
            for com in command:
                if user_input.casefold().startswith(com):
                    print(sub_f(*user_input[len(com):].strip().split()))
                    if sub_f == sub_exit:
                        return
                    command_found = True
                    break
        if not command_found:       
            print("Command not found")

if __name__ == '__main__':
    main() 