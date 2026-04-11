# Placement_Portal_App
python3 -m venv .env
source .env/bin/activate
pip3 install -r requirment.txt
npm install
npm run dev
sudo service redis-server stop
sudo-alok7239
redis-server
python3 -m celery -A app.celery worker --loglevel=info
MailHog
celery -A app.celery beat --loglevel=info