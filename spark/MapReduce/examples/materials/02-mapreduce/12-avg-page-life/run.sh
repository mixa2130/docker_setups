#! /usr/bin/env bash

OUT_DIR="page_life"
mvn package
hdfs dfs -rm -r -skipTrash ${OUT_DIR}*
yarn jar target/PageLifeCounter-1.0.jar org.atp.PageLifeCounter /data/user_events_part ${OUT_DIR}
