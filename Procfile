worker: ./node_modules/.bin/parcel watch bundles-src/index.js --dist-dir bundles --public-url="./"
web: bin/start-nginx
web: gunicorn star_burger.wsgi:application
