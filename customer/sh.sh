#!bin/sh

docker exec -it -u root grafana sqlite3 /var/lib/grafana/grafana.db 'select json_group_array(json_object("uid", id, "after_state", new_state, "before_state", prev_state, "data_value", text, "alert_time", updated)) AS json_result from annotation where prev_state = "Pending" AND new_state = "Alerting"' > json_test
