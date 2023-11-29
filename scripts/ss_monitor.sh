# To monitor ss tcp data from from $1 to $2
while true;
do	
        time=$(date +%s%N)
	      to_server=$(ss dst $2 -ei)
        echo $time'    '$to_server>>/home/peng/hologram_ss_$1_to_server.output
	      sleep 0.01;
done
