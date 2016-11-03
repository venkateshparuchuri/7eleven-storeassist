export CONFIG_FILE_PATH="/var/www/config/config.json";
export LOG_CFG_PATH="/var/www/config/logconf.json";
gunicorn app:app -w 4 -b 0.0.0.0:8000 -D
