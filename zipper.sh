#!/bin/bash

# Name of the root directory inside the zip
ROOT_DIR="quiz_master_21f1006194"
ZIP_FILE="${ROOT_DIR}.zip"

# Create archive with a root folder inside
git archive --format=zip --prefix="${ROOT_DIR}/" HEAD -o "${ZIP_FILE}"

echo "Created ${ZIP_FILE} with contents under ${ROOT_DIR}/"
