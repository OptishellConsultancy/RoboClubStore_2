#!/usr/bin/env bash
#
# Intended to find the correct device to point my machine to play audio from
#   See speaker-test(1) for more
set -euo pipefail

pcmDevs="$(
  aplay --list-pcms |
    grep --invert-match --extended-regexp '^[[:space:]]' |
    grep --invert-match --extended-regexp '^(default|null|pulse)' |
    while IFS=, read record _; do echo "$record"; done |
    while IFS=: read label cardKeyValue; do
      card="${cardKeyValue/CARD=/}"
      if [ "$card" = Loopback ];then continue;fi
      printf -- '%s:%s\n' "$label" "$card"
    done |
    sort --stable |
    uniq
)"; declare -ra pcmDevs

currentlyTesting=0
reportInterruptedDevice() (
  if [[ -z "$currentlyTesting" ]];then return; fi
  printf 'INTERRUPTED testing device "%s"\n' "$currentlyTesting"
)
trap reportInterruptedDevice SIGINT

for pcmDevice in ${pcmDevs[@]};do
  currentlyTesting="$pcmDevice"

  printf 'TESTING device "%s"\n' "$pcmDevice"
  speaker-test --channels 2 --device $pcmDevice &&
    printf '\nFAILED testing device "%s"\n\n' "$pcmDevice" ||
    printf '\nFINSHED testing device "%s"\n\n' "$pcmDevice"
done
currentlyTesting=''