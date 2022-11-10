keydir="../keys"
conf="../generate/ext.cnf"
cd "$keydir"

openssl req -x509 -newkey rsa:4096 -nodes -out ca.crt -keyout ca.key -days 365 -config $conf -extensions req_ext
