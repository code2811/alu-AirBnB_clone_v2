import cmd
import shlex
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review

classes = {
    "BaseModel": BaseModel,
    "User": User,
    "State": State,
    "City": City,
    "Amenity": Amenity,
    "Place": Place,
    "Review": Review
}

class HBNBCommand(cmd.Cmd):
    prompt = "(hbnb) "

    def do_create(self, arg):
        args = shlex.split(arg)
        if not args:
            print("** class name missing **")
            return
        class_name = args[0]
        if class_name not in classes:
            print("** class doesn't exist **")
            return
        obj = classes[class_name]()
        for param in args[1:]:
            if "=" not in param:
                continue
            key, value = param.split("=", 1)
            if value.startswith('"') and value.endswith('"'):
                value = value[1:-1].replace("_", " ").replace('\\"', '"')
            else:
                if "." in value:
                    try:
                        value = float(value)
                    except ValueError:
                        continue
                else:
                    try:
                        value = int(value)
                    except ValueError:
                        continue
            setattr(obj, key, value)
        obj.save()
        print(obj.id)

    def do_show(self, arg):
        args = shlex.split(arg)
        if not args:
            print("** class name missing **")
            return
        if args[0] not in classes:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        key = f"{args[0]}.{args[1]}"
        obj = storage.all().get(key)
        if not obj:
            print("** no instance found **")
            return
        print(obj)

    def do_all(self, arg):
        args = shlex.split(arg)
        objects = storage.all()
        if args and args[0] not in classes:
            print("** class doesn't exist **")
            return
        result = []
        for obj in objects.values():
            if not args or obj.__class__.__name__ == args[0]:
                result.append(str(obj))
        print(result)

    def do_quit(self, arg):
        return True

    def do_EOF(self, arg):
        print()
        return True

    def emptyline(self):
        pass
from models.engine.file_storage import FileStorage

storage = FileStorage()
storage.reload()

