working_dir="$PWD"
effect="$1"
thickness="$2"
#lane_code_dir="/home/uva-dsa/Development/Lane_detection/MATLAB_implementation/Codes"
lane_code_dir="/home/uva-dsa/Development/Lane_detection/MATLAB_implementation/Codes/"$effect"_results/"
cd "$lane_code_dir"
#python callMatlabFunction.py "$effect" "$thickness"   #argument is for adding image effects, options: rain/fog/snow/occlusion/none

cp laneData_"$effect"_"$thickness".dat "$working_dir/selfdrive/test/tests/plant/laneData_noisy.dat"

#cd "$working_dir"

#./run_docker_tests.sh
