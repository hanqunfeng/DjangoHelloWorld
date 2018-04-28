from django.dispatch import Signal, receiver

# my_singal = Signal(providing_args=["key1", "key2"])
my_singal = Signal()


@receiver(my_singal)
def my_callback(sender, **kwargs):
    print(sender)
    print(kwargs)
    for key in kwargs:
        print(key)
        print(kwargs[key])
    print("Request finished!")
