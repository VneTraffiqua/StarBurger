worker: ./node_modules/.bin/parcel watch bundles-src/index.js --dist-dir bundles --public-url="./"
web1: bin/start-nginx-solo
web2: gunicorn star_burger.wsgi:application
