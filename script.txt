# delete all server
for SERVER in `os server list -c ID | head -n -1 | tail -n +4 | cut -d ' ' -f 2`
do
os server delete $SERVER
done
