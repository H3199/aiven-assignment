# Aiven Support Engineer Assignment

The original idea of this demo was a basic inventory system where postgresql handles the transactions players do and kafka shows the latest status of the system.

I also used this opportunity to learn a bit how github worksflows and terraforming work together.
The debezium source connector I ended up putting up by manually curling with a static JSON e.g.

```bash
curl -X POST -H "Content-Type: application/json" --data @debezium_manual.json https://avnadmin...

But the gh-workflow using sed to write a json file and then curling it is close to working, just ran out of time a bit.
Workflows for terraforming kafka and postgres were much simpler. The db schema and test data do not have workflows.

The logs that display the status of the system can be found in logs.txt.
