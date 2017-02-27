from django.core.management.base import BaseCommand

from web.models import Motor, Battery


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        parser.add_argument('model', nargs=1, type=str)

    def handle(self, *args, **options):
        if "motors" in options["model"]:
            motors = Motor.objects.all()
            for motor in motors:
                print(motor)
                motor.delete()
        elif "batteries" in options["model"]:
            bats = Battery.objects.all()
            for bat in bats:
                print(bat)
                bat.delete()
        else:
            print("bad model: ", options["model"][0])
            return
        print("Done!")
