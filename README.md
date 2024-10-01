The original idea of this demo was a basic inventory system where postgresql handles the transactions players do and kafka shows the latest status of the system.

I also used this opportunity to learn a bit how github worksflows and terraforming work together.
The debezium source connector I ended up putting up by manually curling with a static JSON e.g.

  curl -X POST -H "Content-Type: application/json" --data @debezium_manual.json https://avnadmin...

But the gh-workflow using sed to write a json file and then curling it is close to working, just ran out of time a bit.
Workflows for terraforming kafka and postgres were much simpler. The db schema and test data do not have workflows.

The logs for the system look like this:

### Status after starting the server-st and client-st:

[eero@akvaario app]$ python server-st.py
Server started at localhost:12345
New connection from ('127.0.0.1', 56914)
Client ('127.0.0.1', 56914) confirmed connection.

----------

[eero@akvaario app]$ python client-st.py
Connected to game server at localhost:12345
Server confirmation: Connection confirmed.
Received from server: KAFKA: {"before":null,"after":{"item_id":"f1fd6d74-011d-41d0-86ff-5dc4eaa45e62","item_name":"Sword"},"source":{"version":"2.5.0.Final.Aiven","connector":"postgresql","name":"gamedata","ts_ms":1727611543522,"snapshot":"first","db":"defaultdb","sequence":"[null,\"14982069696\"]","schema":"public","table":"items","txId":27642,"lsn":14982069696,"xmin":null},"op":"r","ts_ms":1727611543668,"transaction":null}
Received from server: KAFKA: {"before":null,"after":{"item_id":"e39942ab-7fa4-418c-bdaf-52a75b2f3a96","item_name":"Arrow"},"source":{"version":"2.5.0.Final.Aiven","connector":"postgresql","name":"gamedata","ts_ms":1727611543522,"snapshot":"true","db":"defaultdb","sequence":"[null,\"14982069696\"]","schema":"public","table":"items","txId":27642,"lsn":14982069696,"xmin":null},"op":"r","ts_ms":1727611543673,"transaction":null}
Received from server: KAFKA: {"before":null,"after":{"item_id":"6a98f0de-1386-43fb-a50f-72fe6d12bd85","item_name":"Potion"},"source":{"version":"2.5.0.Final.Aiven","connector":"postgresql","name":"gamedata","ts_ms":1727611543522,"snapshot":"true","db":"defaultdb","sequence":"[null,\"14982069696\"]","schema":"public","table":"items","txId":27642,"lsn":14982069696,"xmin":null},"op":"r","ts_ms":1727611543673,"transaction":null}
Received from server: KAFKA: {"before":null,"after":{"item_id":"3c17c0f1-2b88-4e57-a9c9-a24d757096d7","item_name":"Helmet"},"source":{"version":"2.5.0.Final.Aiven","connector":"postgresql","name":"gamedata","ts_ms":1727611543522,"snapshot":"last_in_data_collection","db":"defaultdb","sequence":"[null,\"14982069696\"]","schema":"public","table":"items","txId":27642,"lsn":14982069696,"xmin":null},"op":"r","ts_ms":1727611543673,"transaction":null}
Received from server: KAFKA: {"before":null,"after":{"item_id":"e385dffa-61bf-4a02-bb00-62d91239c692","item_name":"Shield"},"source":{"version":"2.5.0.Final.Aiven","connector":"postgresql","name":"gamedata","ts_ms":1727611543522,"snapshot":"true","db":"defaultdb","sequence":"[null,\"14982069696\"]","schema":"public","table":"items","txId":27642,"lsn":14982069696,"xmin":null},"op":"r","ts_ms":1727611543672,"transaction":null}
Received from server: KAFKA: {"before":null,"after":{"item_id":"1c3618b4-6157-4d5e-b35f-f7f6c56b58cf","item_name":"Bow"},"source":{"version":"2.5.0.Final.Aiven","connector":"postgresql","name":"gamedata","ts_ms":1727611543522,"snapshot":"true","db":"defaultdb","sequence":"[null,\"14982069696\"]","schema":"public","table":"items","txId":27642,"lsn":14982069696,"xmin":null},"op":"r","ts_ms":1727611543673,"transaction":null}


### Status after inserting a new item into the database:

defaultdb=> INSERT INTO items (item_name) VALUES ('Crossbow');
INSERT 0 1
defaultdb=>

----------

[eero@akvaario app]$ python client-st.py
Connected to game server at localhost:12345
Server confirmation: Connection confirmed.
Received from server: KAFKA: {"before":null,"after":{"item_id":"f1fd6d74-011d-41d0-86ff-5dc4eaa45e62","item_name":"Sword"},"source":{"version":"2.5.0.Final.Aiven","connector":"postgresql","name":"gamedata","ts_ms":1727611543522,"snapshot":"first","db":"defaultdb","sequence":"[null,\"14982069696\"]","schema":"public","table":"items","txId":27642,"lsn":14982069696,"xmin":null},"op":"r","ts_ms":1727611543668,"transaction":null}
Received from server: KAFKA: {"before":null,"after":{"item_id":"e39942ab-7fa4-418c-bdaf-52a75b2f3a96","item_name":"Arrow"},"source":{"version":"2.5.0.Final.Aiven","connector":"postgresql","name":"gamedata","ts_ms":1727611543522,"snapshot":"true","db":"defaultdb","sequence":"[null,\"14982069696\"]","schema":"public","table":"items","txId":27642,"lsn":14982069696,"xmin":null},"op":"r","ts_ms":1727611543673,"transaction":null}
Received from server: KAFKA: {"before":null,"after":{"item_id":"6a98f0de-1386-43fb-a50f-72fe6d12bd85","item_name":"Potion"},"source":{"version":"2.5.0.Final.Aiven","connector":"postgresql","name":"gamedata","ts_ms":1727611543522,"snapshot":"true","db":"defaultdb","sequence":"[null,\"14982069696\"]","schema":"public","table":"items","txId":27642,"lsn":14982069696,"xmin":null},"op":"r","ts_ms":1727611543673,"transaction":null}
Received from server: KAFKA: {"before":null,"after":{"item_id":"3c17c0f1-2b88-4e57-a9c9-a24d757096d7","item_name":"Helmet"},"source":{"version":"2.5.0.Final.Aiven","connector":"postgresql","name":"gamedata","ts_ms":1727611543522,"snapshot":"last_in_data_collection","db":"defaultdb","sequence":"[null,\"14982069696\"]","schema":"public","table":"items","txId":27642,"lsn":14982069696,"xmin":null},"op":"r","ts_ms":1727611543673,"transaction":null}
Received from server: KAFKA: {"before":null,"after":{"item_id":"e385dffa-61bf-4a02-bb00-62d91239c692","item_name":"Shield"},"source":{"version":"2.5.0.Final.Aiven","connector":"postgresql","name":"gamedata","ts_ms":1727611543522,"snapshot":"true","db":"defaultdb","sequence":"[null,\"14982069696\"]","schema":"public","table":"items","txId":27642,"lsn":14982069696,"xmin":null},"op":"r","ts_ms":1727611543672,"transaction":null}
Received from server: KAFKA: {"before":null,"after":{"item_id":"1c3618b4-6157-4d5e-b35f-f7f6c56b58cf","item_name":"Bow"},"source":{"version":"2.5.0.Final.Aiven","connector":"postgresql","name":"gamedata","ts_ms":1727611543522,"snapshot":"true","db":"defaultdb","sequence":"[null,\"14982069696\"]","schema":"public","table":"items","txId":27642,"lsn":14982069696,"xmin":null},"op":"r","ts_ms":1727611543673,"transaction":null}
Received from server: KAFKA: {"before":null,"after":{"item_id":"05c69ef4-4678-47fe-b5f4-4e6e8216bb25","item_name":"Crossbow"},"source":{"version":"2.5.0.Final.Aiven","connector":"postgresql","name":"gamedata","ts_ms":1727800698486,"snapshot":"false","db":"defaultdb","sequence":"[null,\"25685918192\"]","schema":"public","table":"items","txId":46929,"lsn":25685918192,"xmin":null},"op":"c","ts_ms":1727800699524,"transaction":null}
