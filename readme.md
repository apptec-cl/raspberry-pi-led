#python -m pip install -r requirements.txt
curl -i -X POST -H 'Content-Type: application/json' -d '{"data":{"type":"color", "attributes":{"color":"0xFFFFFF"}}}' http://localhost:5000/leds