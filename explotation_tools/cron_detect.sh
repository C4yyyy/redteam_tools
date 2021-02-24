#!/bin/bash

#Script para detectar que archivos se estan corriendo cada X tiempo de forma automatica

old_pocess=$(ps -eo command)

while true; do
	new_process=$(ps -eo command)
	diff <(echo "$old_process") <(echo "$new_process") | grep "[\>\<]" | grep -v "kworker" | grep -v "google"
	old_process=$new_process
done
