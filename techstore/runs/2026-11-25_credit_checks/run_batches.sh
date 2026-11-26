#!/bin/bash
# PENDING_CREDITS #2, #3, #4, #9: 64-question dev runs. Run from techstore/.
D=runs/2026-11-25_credit_checks
Q=data/questions_dev.jsonl
run() { name=$1; shift; python cli.py --batch $Q --out $D/$name.jsonl "$@" > $D/$name.log 2>&1; echo "done $name"; }
run sol_rerun        --model gpt-6.1-sol &
run luna_rerun       --model gpt-6-luna &
run sol_concise      --model gpt-6.1-sol --answer-length concise &
run luna_concise     --model gpt-6-luna  --answer-length concise &
wait
run sol_verblow      --model gpt-6.1-sol --verbosity low &
run luna_verblow     --model gpt-6-luna  --verbosity low &
run sol_adaptive     --model gpt-6.1-sol --context-margin 0.25 &
run luna_adaptive    --model gpt-6-luna  --context-margin 0.25 &
wait
run sol_effortlow    --model gpt-6.1-sol --reasoning-effort low &
wait
echo ALL DONE
