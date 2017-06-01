function getOptimalTaskSets(taskList, energyToSpare, handle){
	$.ajax({
		type: "POST", 
		url: "/webapp/getOptimalTaskSets/",
		data: {"taskList": JSON.stringify(taskList), "energyToSpare": energyToSpare},
		success: function(result){
			console.log(result);
			// handle(result["shortestPath"], result["totalReward"], result["totalCost"]);
		}
	});
}

// Get the Shortest Path for a list of tasks 
// Parameters: 
//		shortestPaths: the precomputed array of ShortestPath objects.
// 		taskSelection: an array of tasks representing the tasks that we want to include in our shortest path
// Return:
// 		An array representing the retrieved Shortest Path. Array Elements (in order):
//		solution, probability, total cost, total reward.
function getShortestPath(shortestPaths, taskSelection){
	for (var i = 0; i < shortestPaths.length; i++){
		if (shortestPaths[i].fields.task_selection == taskSelection){
			return [ 	
						shortestPaths[i].fields.solution, 
						shortestPaths[i].fields.total_cost, 
						shortestPaths[i].fields.total_reward
					];
		}
	}
}

function calculateDistance(x1, y1, x2, y2){
	return Math.sqrt(Math.pow((x1 - x2), 2) + Math.pow((y2 - y1), 2));
}