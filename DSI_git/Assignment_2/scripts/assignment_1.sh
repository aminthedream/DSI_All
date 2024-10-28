#!/bin/bash

FILE="./parking_data.csv"

function parking {
    echo "extracting infraction description"
    cut -d, -f4 "$FILE"
    echo "print unique values of the fines"
    cut -d, -f5 "$FILE" | sort | uniq
    echo "calculating count, mean, min, and max"
    sum=0
    min=0
    max=500
    count=0
    for fine in $(tail -n +2 "$FILE" | cut -d, -f5); do
        sum=$((sum + fine))
        count=$((count + 1))

        if [ "$fine" -lt "$min" ]; then
            min=$fine
        fi

        if [ "$fine" -gt "$max" ]; then
            max=$fine
        fi
    done

    mean=$((sum / count))

    echo "mean: $mean"
    echo "min: $min"
    echo "max: $max"
    echo "count: $count"

    infraction="PARK PROHIBITED TIME NO PERMIT"
    echo "save the results - PARK PROHIBITED TIME NO PERMIT infraction"
    grep "$infraction" "$FILE" > "parking_function_output.csv"


}

parking


echo "citation: https://unix.stackexchange.com/questions/570764/efficient-way-to-do-calculations-in-bash"
