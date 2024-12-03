test_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, test_OnTransition
	.byte 0

test_OnTransition:
	setflag FLAG_VISITED_PALLET_TOWN
	end