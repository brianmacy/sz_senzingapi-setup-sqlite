# sz_senzingapi-setup-sqlite
Example script to setup a SQLite DB with a default configuration

# API demonstrated
## Core
* G2Config: Creates a new configuration
* G2ConfigMgr: Checks if there is a default configuration already in the database, if not is adds the new configuration and sets it as the default

For more details on the Senzing API go to https://docs.senzing.com


# Limitations
This currently does not support a clustered configuration, schema upgrades, or config upgrades.


# Running
Set an engine configuration similar to this:
```
export SENZING_ENGINE_CONFIGURATION_JSON='{
            "PIPELINE": {
            "CONFIGPATH": "/etc/opt/senzing",
            "RESOURCEPATH": "/opt/senzing/g2/resources",
            "SUPPORTPATH": "/opt/senzing/data"
          },
          "SQL": {
            "CONNECTION": "sqlite3://na:na@/db/G2C.db"
          }
        }'
```
For additional details on the configuration see: https://senzing.zendesk.com/hc/en-us/articles/360038774134-G2Module-Configuration-and-the-Senzing-API


```
docker run --user $UID -it -v $PWD:/db -e SENZING_ENGINE_CONFIGURATION_JSON brian/sz_senzingapi-setup-sqlite
```

You can then run the other docker contains like:
```
docker run --user $UID -it -v $PWD:/db -e SENZING_ENGINE_CONFIGURATION_JSON senzing/senzingapi-tools
```
