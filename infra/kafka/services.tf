resource "aiven_kafka" "assignment-kafka" {
  project      = var.project_name
  cloud_name   = "google-europe-west1"
  plan         = "business-4"
  service_name = "assignment-kafka"
  default_acl  = false

  kafka_user_config {
    kafka_rest      = true
    kafka_connect   = false
    schema_registry = true

    kafka {
      auto_create_topics_enable  = true
      num_partitions             = 3
      default_replication_factor = 2
      min_insync_replicas        = 2
    }

    kafka_authentication_methods {
      certificate = true
    }

    public_access {
      kafka_rest = true
    }
  }
}

resource "aiven_kafka_topic" "assignment-kafka-topic" {
  project      = var.project_name
  service_name = aiven_kafka.assignment-kafka.service_name
  topic_name   = "assignment-kafka-topic"
  partitions   = 5
  replication  = 3
}

resource "aiven_kafka_user" "assignment-kafka-user" {
  project      = var.project_name
  service_name = aiven_kafka.assignment-kafka.service_name
  username     = var.kafka_user_name
}

resource "aiven_kafka_acl" "assignment-kafka-user-acl" {
  project      = var.project_name
  service_name = aiven_kafka.assignment-kafka.service_name
  username     = var.kafka_user_name
  permission   = "read"
  topic        = aiven_kafka_topic.assignment-kafka-topic.topic_name
}
