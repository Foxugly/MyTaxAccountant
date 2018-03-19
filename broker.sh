#!/bin/bash
celery -A mta worker -l info >> /tmp/celery.log
