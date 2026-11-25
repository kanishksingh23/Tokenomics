#!/bin/bash
# PENDING_CREDITS #6 (memory modes, 8 dev chats) and #8 (cache layout vs classic, 2 long chats). Sol. Run from techstore/.
D=runs/2026-11-25_credit_checks
run() { name=$1; shift; python cli.py --model gpt-6.1-sol --out $D/$name.jsonl "$@" > $D/$name.log 2>&1; echo "done $name"; }
for m in off window facts summary; do run mem_$m --conversations data/conversations_dev.jsonl --memory $m & done
run long_classic --conversations $D/long_chats.jsonl --layout classic &
run long_cache   --conversations $D/long_chats.jsonl --layout cache &
wait
echo ALL DONE
