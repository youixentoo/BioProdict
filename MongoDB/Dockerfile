FROM mongo

COPY mongo.json ./mongo.json
CMD mongoimport -v --host mongodb --port 27017 --db bioprodict --collection vcf --file ./mongo.json & mongod
