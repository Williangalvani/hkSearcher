 #!/bin/bash
  set -e
  LOGFILE=/var/log/gunicorn/hello.log
  LOGDIR=$(dirname $LOGFILE)
  NUM_WORKERS=2
  # user/group to run as
  USER=root
  GROUP=root
  cd /root/hksite
  #source bin/activate
  cd hksearcher
  test -d $LOGDIR || mkdir -p $LOGDIR
  exec gunicorn_django -w $NUM_WORKERS \
    --user=$USER --group=$GROUP --log-level=debug \
    --log-file=$LOGFILE 2>>$LOGFILE \
    --daemon \
    -b 0.0.0.0:8000

