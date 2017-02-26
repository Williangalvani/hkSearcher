from web.models import Motor

#setup_environ(settings)

motors = Motor.objects.all().order_by('kv')
effience = []
for motor in motors:
    if motor.getEff():
        print motor.getEff(), motor.name
