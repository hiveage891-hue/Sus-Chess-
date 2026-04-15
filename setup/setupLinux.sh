#!/usr/bin/env bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FILE_PATH="$SCRIPT_DIR/source/GameTest.py"
LOG_FILE="$SCRIPT_DIR/crashlog.txt"

if ! command -v python3 &> /dev/null; then
    echo "$(date): Python3 não instalado" > "$LOG_FILE"
    exit 1
fi

if [ -f "$FILE_PATH" ]; then
    python3 "$FILE_PATH" 2> "$LOG_FILE"

    if [ $? -ne 0 ]; then
        echo "Ocorreu um erro. Verifique o arquivo crashlog.txt"
    else
        echo "pedrinho"
    fi
else
    echo "$(date): Arquivo $FILE_PATH não encontrado" > "$LOG_FILE"
    exit 1
fi