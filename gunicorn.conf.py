# Settings for the web server Render uses (gunicorn reads this file automatically).
#
# - timeout: the AI check can take a while, so don't cut requests off at 30 seconds.
# - threads: let several people use SafeSend at the same time
#   (for example the elder and the trusted contact).

timeout = 90
workers = 1
threads = 8
worker_class = "gthread"
