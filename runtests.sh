#!/bin/bash

# We need git to upload to codecov
apt-get install -y git
pytest --cov
bash <(curl -s https://codecov.io/bash)
