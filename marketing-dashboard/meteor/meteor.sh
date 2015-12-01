#!/bin/bash

cd /home/desktop/Desktop/MarkDB/meteor
echo "Meteor Started (`date`)" >> ../log/meteor.log
sleep 2
meteor >> ../log/meteor.log
echo "Meteor has Stopped (`date`)"
