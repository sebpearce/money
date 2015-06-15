#!/bin/bash

rm money.db
python models.py
python populate.py
python views.py