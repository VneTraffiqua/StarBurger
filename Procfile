worker: ./node_modules/.bin/parcel watch bundles-src/index.js --dist-dir bundles --public-url="./"
web1: gunicorn star_burger.wsgi:application
web2: bin/start-nginx-solo