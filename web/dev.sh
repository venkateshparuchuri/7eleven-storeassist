export NODE_ENV=dev
cd /var/www/html/web
npm install
npm install -g bower
bower install --allow-root
gulp build
