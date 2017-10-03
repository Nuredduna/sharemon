# Setup environment for ShareMon project.

if [[ $_ == $0 ]]; then
    echo "Please 'source' this script"
    exit 1
fi

ACTIVATE_SCRIPT="$(pwd)/bin/activate"

if [ ! -f "$ACTIVATE_SCRIPT" ]; then
    echo "Creating virtual environment"
    pyvenv .
fi

. "$ACTIVATE_SCRIPT"

