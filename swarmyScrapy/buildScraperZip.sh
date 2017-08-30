#!/bin/bash

rsync -av --exclude=*/*.json --exclude=*/*.txt --exclude=*/*.pyc ../virtuance_scraper .
