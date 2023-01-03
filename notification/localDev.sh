sls dynamodb start &
sleep 2
DYNAMO_ENDPOINT=http://localhost:8000 dynamodb-admin &
sleep 2
open http://0.0.0.0:8001/
sls offline start
