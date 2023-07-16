#!/usr/bin/python3

import cmd
import models
from models.base_model import BaseModel
from models.user import User
import re


class HBNBCommand(cmd.Cmd):
    """Command interpreter class"""
    prompt = '(hbnb) '

    classes = {
        "BaseModel",
        "User",
    }

    def parse(arg):
        curly_braces_match = re.search(r"\{(.*?)\}", arg)
        brackets_match = re.search(r"\[(.*?)\]", arg)

        if curly_braces_match is None:
            if brackets_match is None:
                return [item.strip(",") for item in arg.split()]
            else:
                lexer = arg[:brackets_match.span()[0]].split()
                result_list = [item.strip(",") for item in lexer]
                result_list.append(brackets_match.group())
                return result_list
        else:
            lexer = arg[:curly_braces_match.span()[0]].split()
            result_list = [item.strip(",") for item in lexer]
            result_list.append(curly_braces_match.group())
            return result_list

    def do_quit(self, arg):
        """Quit command to exit the program"""
        return True

    def do_EOF(self, arg):
        """Exit the program using EOF"""
        print("")
        return True

    def emptyline(self):
        """Doesn't execute anything"""
        pass

    def do_create(self, arg):
        """Creates a new instance of BaseModel"""
        if len(arg) == 0:
            print("** class name missing **")
        elif arg not in HBNBCommand.classes:
            print("** class doesn't exist **")
        else:
            print(eval(arg)().id)
            models.storage.save()

    def do_show(self, arg):
        """Prints the string representation of an instance"""
        argums = HBNBCommand.parse(arg)
        obdict = models.storage.all()
        if len(argums) == 0:
            print("** class name missing **")
        elif argums[0] not in HBNBCommand.classes:
            print("** class doesn't exist **")
        elif len(argums) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(argums[0], argums[1]) not in obdict:
            print("** no instance found **")
        else:
            print(obdict["{}.{}".format(argums[0], argums[1])])

    def do_destroy(self, arg):
        """Deletes an instance"""
        argums = HBNBCommand.parse(arg)
        obdict = models.storage.all()
        if len(argums) == 0:
            print("** class name missing **")
        elif argums[0] not in HBNBCommand.classes:
            print("** class doesn't exist **")
        elif len(argums) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(argums[0], argums[1]) not in obdict:
            print("** no instance found **")
        else:
            del obdict["{}.{}".format(argums[0], argums[1])]
            models.storage.save()

    def do_all(self, arg):
        """Prints all instances"""
        argums = HBNBCommand.parse(arg)
        obdict = models.storage.all()
        if len(argums) > 0 and argums[0] not in HBNBCommand.classes:
            print("** class doesn't exist **")
        else:
            objv = []
            for obj in obdict.values():
                if len(argums) > 0 and argums[0] == obj.__class__.__name__:
                    objv.append(obj.__str__())
                elif len(argums) == 0:
                    objv.append(obj.__str__())
            print(objv)

    def do_update(self, arg):
        """Updates an instance
Usage: update <class name> <id> <attribute name> "<attribute value>\""""
        argums = HBNBCommand.parse(arg)
        obdict = models.storage.all()

        if len(argums) == 0:
            print("** class name missing **")
            return False
        if argums[0] not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return False
        if len(argums) == 1:
            print("** instance id missing **")
            return False
        if "{}.{}".format(argums[0], argums[1]) not in obdict.keys():
            print("** no instance found **")
            return False
        if len(argums) == 2:
            print("** attribute name missing **")
            return False
        if len(argums) == 3:
            try:
                type(eval(argums[2])) != dict
            except NameError:
                print("** value missing **")
                return False

        if len(argums) == 4:
            obj = obdict["{}.{}".format(argums[0], argums[1])]
            if argums[2] in obj.__class__.__dict__.keys():
                valtype = type(obj.__class__.__dict__[argums[2]])
                obj.__dict__[argums[2]] = valtype(argums[3])
            else:
                obj.__dict__[argums[2]] = argums[3]
        elif type(eval(argums[2])) == dict:
            obj = obdict["{}.{}".format(argums[0], argums[1])]
            for k, v in eval(argums[2]).items():
                if (k in obj.__class__.__dict__.keys() and
                        type(obj.__class__.__dict__[k]) in {str, int, float}):
                    valtype = type(obj.__class__.__dict__[k])
                    obj.__dict__[k] = valtype(v)
                else:
                    obj.__dict__[k] = v
        models.storage.save()

    def default(self, arg):
        """default behavior for cmd when input is invalid"""
        argdict = {
            "all": self.do_all,
        }
        match = re.search(r"\.", arg)
        if match is not None:
            argl = [arg[:match.span()[0]], arg[match.span()[1]:]]
            match = re.search(r"\((.*?)\)", argl[1])
            if match is not None:
                command = [argl[1][:match.span()[0]], match.group()[1:-1]]
                if command[0] in argdict.keys():
                    call = "{} {}".format(argl[0], command[1])
                    return argdict[command[0]](call)
        print("*** Unknown syntax: {}".format(arg))
        return False


if __name__ == '__main__':
    HBNBCommand().cmdloop()
