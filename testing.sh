#!/bin/bash
echo Beginning testing for $1 from $2 to $3, $4 tests each > profile/time_results.txt
echo Beginning testing for $1 from $2 to $3, $4 tests each> profile/solve_results.txt
TOTAL=`expr $3 - $2`
echo -ne "0%\r"
for i in `seq $2 $3`;
  do
    for j in `seq 1 $4`
      do
        echo -ne "\n" >> profile/time_results.txt
        echo -ne "\n" >> profile/solve_results.txt
        echo Testing with $i processes >> profile/time_results.txt
        echo Testing with $i processes >> profile/solve_results.txt
        echo --------- >> profile/time_results.txt
        echo --------- >> profile/solve_results.txt
        if [[ "$4" = "-np" || "$5" = "-np" ]]; then
          (time mpiexec -n $i python solver_launcher.py $1 -np) >> profile/solve_results.txt 2>> profile/time_results.txt
        else
          (time mpiexec -n $i python solver_launcher.py $1) >> profile/solve_results.txt 2>> profile/time_results.txt
        fi
      done
      step=`expr $i - $2`
      sp=`expr $step \* 100`
      percent=$((sp / TOTAL))
      echo -ne "$percent%\r"
  done
echo Done testing distributed solver

if [[ "$5" = "-l" || "$6" = "-l" ]]; then
  echo Testing with local solver
  echo -ne "\n" >> profile/time_results.txt
  echo -ne "\n" >> profile/solve_results.txt
  echo Testing with local, non-distributed solver >> profile/time_results.txt
  echo Testing with local, non-distributed solver >> profile/solve_results.txt
  echo --------- >> profile/time_results.txt
  echo --------- >> profile/solve_results.txt
  (time python solve_local.py $1) >> profile/solve_results.txt 2>> profile/time_results.txt
fi
echo Done with all tests
