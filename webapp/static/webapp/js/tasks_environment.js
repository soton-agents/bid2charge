
// -- Ratio and Relative Sizes Declarations
// -- Declare any such ratios here and explain how they will be used

// Task Environment Width Ratio (width = body_width / width_ratio)
var width_ratio = 2.2;

// Height Ratio (height = width * height_scale)
var height_ratio = 0.8;

// Width of a Task Element relative to the width of the environemnt (task_width = env_width / task_ratio)
var task_ratio = 7.50;

// Ratio of home image is used in contrast to env_width (home_image_width = env_width / home_image_ratio)
var home_image_ratio = 10.00;

var LABEL_FONT_SIZE = 15;

// -- Actual Sizes Calculations
// -- Define any definitive element sizes here 
// -- Make use of ratios or defined functions if necessary 

// Task Environment Width
var env_width = calculateEnvWidth();

// Task Environment Height
var env_height = calculateEnvHeight();

// Actual Task  Image Width
var task_width = Math.floor(env_width / task_ratio);

// Home Image Width
var home_image_width = Math.floor(env_width / home_image_ratio);

// Helper Functions for calculating the enviroment width and height
function calculateEnvWidth(){ 
	var window_width = window.outerWidth;

	if (window_width >= 350){
		width_ratio = 1.05;
		height_ratio = 0.8;
	}

	if (window_width >= 580){
		width_ratio = 1.2;
		height_ratio = 0.8;		
	}

	if (window_width >= 670){
		width_ratio = 1.35;
		height_ratio = 0.8;		
	}

	if (window_width >= 768){
		width_ratio = 1.5;
		height_ratio = 0.8;		
	}

	if (window_width >= 992){
		width_ratio = 2.2;
		height_ratio = 0.8;
	}

	return Math.round($("#game-body").width() / width_ratio); 
}
function calculateEnvHeight(){ return Math.round(calculateEnvWidth() * height_ratio); }


// DRAW TASKS ENVIRONMENT 
// Draw the SVG environment along with all the tasks and elements within it
// Draw the Shortest Path depending on the tasks that have been clicked
// Handle Mouse Events
function draw_tasks_environment(parent_id, tasks, task_probabilities, shortest_paths, kwh_per_km){
	// Array that keeps track of selected Tasks
	var selected_tasks = new TaskArray();

	// Create the SVG area
	var svg = d3.select("#" + parent_id).append("svg")
		.attr("preserveAspectRatio", "xMidYMin")
		.attr("viewBox", "0 0 " + env_width + " " + env_height)
		.attr("width", env_width)
		.attr("height", env_height);

	// Draw the "Background" Rectangle 
	var task_env = svg.append("rect")
		.attr("x", 1)
		.attr("y", 1)
		.attr("rx", 15)
		.attr("ry", 15)
		.attr("width", env_width - 2)
		.attr("height", env_height - 2)
		.attr("class", "task_env");

	task_env
		.on("mouseenter", function(){
			d3.select(this).attr("stroke", "#786370");
		})
		.on("mouseleave", function(){
			d3.select(this).attr("stroke", "none");
		});


	// Convert the JSON array to JS array (to be used in D3)
	var tasks_js = convertToJsArray(tasks);

	// Array that holds the "clicked" state of a task 
	var clicked = new Array(tasks.length);
	for (var i = 0; i < clicked.length; i++){
		clicked[i] = 1;
	}

	var lineFunction = d3.svg.line()
							.x(function(d){ return d.x; })
							.y(function(d){ return d.y; })
							.interpolate("linear");

	var task = d3.select("svg").selectAll("g")
				.data(tasks_js)
				.enter()
				.append("g");

	// Draw a task image for each task at the specified XY coordinates
	task.append("svg:image")
		.filter(function(d){ return task_probabilities[d.fields.description] > 0})
		.attr("x", function(d, i){
				d.image = d3.select(this); 
				return d.fields.x * env_width - task_width / 2})
		.attr("y", function(d, i){return d.fields.y * env_height - task_width / 2})
		.attr("width", task_width)
		.attr("height", task_width)
		.attr("opacity", function(d, i){return task_probabilities[d.fields.description] * 0.5 + 0.5})
		.attr("xlink:href", function(d){ return d.fields.task_icon; })
		.attr("class", "task")

	// Append Description and Probability Labels
	task.append("text")
		.filter(function(d){ return task_probabilities[d.fields.description] > 0})
		.attr("x", function(d, i){
			d.description_probability_label = d3.select(this);
			var text = Math.round(parseFloat(task_probabilities[d.fields.description]) * 100) + "%";
			var width = measureStringWidth(text, "14px Times New Roman");
			return d.fields.x * env_width - width / 2;
		})
		.attr("y", function(d, i){
			return d.fields.y * env_height + task_width / 2 + LABEL_FONT_SIZE + 3;
		})
		.attr("font-size", LABEL_FONT_SIZE)
		.attr("font-weight", "bold")
		.attr("font-family", "Times New Roman")
		.attr("fill", "black")
		.attr("class", "description-probability-label")
		.text(function(d){ return Math.round(parseFloat(task_probabilities[d.fields.description]) * 100) + "%"})

	task.on("mouseenter", function(d, i){
			if (!d.clicked){
				d.image.transition()
					.duration(200)
					.attr("x", function(d, i){ return d.fields.x * env_width - task_width / 2})
					.attr("y", function(d, i){ return d.fields.y * env_height - task_width / 2 + 5})
					.attr("width", task_width )
					.attr("height", task_width )
					.attr("opacity", "1.0");
			}
		})
		.on("mouseleave", function(d){
			if (!d.clicked){
				d.image.transition()
					.duration(200)
					.attr("x", function(d, i){ return (d.fields.x * env_width - task_width / 2)})
					.attr("y", function(d, i){ return (d.fields.y * env_height - task_width / 2)})
					.attr("width", task_width)
					.attr("height", task_width)
					.attr("opacity", function(d){return task_probabilities[d.fields.description] * 0.5 + 0.5});
			}
		})
		.on("click", function(d){
			var eventType = "select";
			var taskSelectionBefore = $.extend(true, {}, selected_tasks);

			if (!d.clicked){
				// Set the task clicked state to true, add it to the selected tasks array and sort the array
				// The array needs to be sorted for the retrieval of the corresponding shortest path solution from db
				d.clicked = true;
					
				d.image.transition()
					.duration(200)
					.attr("x", function(d, i){ return (d.fields.x * env_width - task_width / 2)})
					.attr("y", function(d, i){ return (d.fields.y * env_height - task_width / 2)})
					// .attr("opacity", 1)
					.attr("xlink:href", function(d){ return [d.fields.task_icon.slice(0, d.fields.task_icon.length - 4), "-selected", d.fields.task_icon.slice(d.fields.task_icon.length - 4)].join("");})
					.attr("width", task_width)
					.attr("height", task_width)

				selected_tasks.add(d);
				selected_tasks.sort();
			}
			else{
				// Remove the task from the array of selected tasks and set its clicked state to false 
				// Sorting is not necessary as removing a task will preserve the initially sorted order
				d.clicked = false;
				eventType = "deselect";

				d.image.transition()
					.duration(200)
					.attr("x", function(d, i){ return (d.fields.x * env_width - task_width / 2)})
					.attr("y", function(d, i){ return (d.fields.y * env_height - task_width / 2)})
					.attr("xlink:href", function(d){ return d.fields.task_icon;})
					.attr("width", task_width)
					.attr("height", task_width)

				selected_tasks.remove(d);
			}

			shortest_path = retrieveAndDrawShortestPath();

			// Define an empty shortest path if the previous assignment is empty,
			// (with reward and distance 0) for successful logging
			if (!shortest_path){
				shortest_path = ["", 0, 0];
			}

			// Log the click action along with the state before and after
		 	$.ajax({
		 		type: "POST",
		 		url: "/webapp/logTaskClickEvent/",
		 		data: {	"taskDescription": d.fields.description, 
		 				"taskReward": d.fields.reward, 
		 				"eventType": eventType, 
		 				"taskSelectionBefore": taskSelectionBefore.stringRepresentation(),
		 				"taskSelectionAfter": selected_tasks.stringRepresentation(),
		 				"total_km": shortest_path[1],
		 				"total_reward": shortest_path[2]
		 			}
		 	});
		});		

	// Add the house image on the center of the drawn area
	svg.append("svg:image")
		.attr("id", "home_image")
		.attr("x", env_width / 2 - (home_image_width / 2))
		.attr("y", env_height / 2 - (home_image_width / 2))
		.attr("width", home_image_width)
		.attr("height", home_image_width)
		.attr("xlink:href", "/static/webapp/img/house-icon2.png");


	function retrieveAndDrawShortestPath(){
		// Get the Shortest Path Object
		// Returned Array will consist of: 
		// 		solution string (concatenated string of descriptions, separated by a separator character), 
		// 		total_cost (double), 
		// 		total_reward (double)		
		var shortest_path = getShortestPath(shortest_paths, selected_tasks.stringRepresentation());

		if (shortest_path){ 
			// Draw the Shortest Path on the Graph
			drawShortestPath(shortest_path[0]); 

			// Set the statistics for the selected schenario
			setScenarioProperties(shortest_path[1], shortest_path[2]);
		}
		else{
			clearPath();
			resetScenarioProperties();
		}

		return shortest_path;
	}

	function drawShortestPath(current_shortest_path){
		// Build the array of task objects from the simple string representation
		var tasks_in_sp = new TaskArray().buildFromStringRepresentation(current_shortest_path, selected_tasks.getArray());

		// Construct the data to be used by the svg path
		// This data should be an array of points [(x, y), (x, y), ...]
		var lineData = [];

		// Add the first edge (Home - Task 1) 
		lineData.push({"x" : env_width / 2, "y" : env_height / 2})

		// Add the edges between tasks
		for (var i = 0; i < tasks_in_sp.length; i++){
			lineData.push({
				"x" : tasks_in_sp[i].fields.x * env_width,
				"y" : tasks_in_sp[i].fields.y * env_height + task_width / 2 
			});
		}

		// Add the last edge (Task N - Home)
		lineData.push({"x" : env_width / 2, "y" : env_height / 2});

		// Clear any drawn paths
		clearPath();

		var path = svg.append("path")
			.attr("id", "optimal_path")
			.attr("d", lineFunction(lineData))
			.attr("stroke", "white")
			.attr("stroke-width", 3)
			.attr("fill", "none");

		var totalLength = path.node().getTotalLength();

		path.attr("stroke-dasharray", totalLength + " " + totalLength)
			.attr("stroke-dashoffset", totalLength)
			.transition()
				.duration(totalLength)
				.ease("linear")
				.attr("stroke-dashoffset", 0);


		// Move all Task Images to front
		d3.selectAll("image").moveToFront();
		d3.selectAll("g").moveToFront();
		
	}

	// Remove any existing svg optimal paths drawn on the task environment
	// Selects all paths with a specifc ID and removes them
	function clearPath(){
		svg.selectAll("#optimal_path").remove();
	}

	function setScenarioProperties(total_cost, total_reward){
		$("#scenario_reward").text(total_reward.toFixed(2));
		$("#scenario_distance").text(total_cost.toFixed(2));
		$("#scenario_energy").text((Math.ceil(kwh_per_km * total_cost)).toFixed(2));

		$(".scenario-info").animate({
			backgroundColor: "#FFFF00"
		}, 150, function(){
			$(".scenario-info").animate({
				backgroundColor: "none"
			}, 150);
		});
	}

	function resetScenarioProperties(){
		$("#scenario_reward").text(0);
		$("#scenario_distance").text(0);
		$("#scenario_energy").text(0);
	}

	// Redraw whenever window is resized
	$(window).resize(function() {
		svg.attr("width", calculateEnvWidth())
			.attr("height", calculateEnvHeight());

		$("#game-body").css("height", "auto");
	});

	// Highlight Home image when hovered
	$("#home_image").mouseenter(function(){
		$(".task_env").attr("class", "task_env hovered_task_env");
	}).mouseleave(function(){
		$(".task_env").attr("class", "task_env");
	});

	$(".task").mouseenter(function(){
		$(".task_env").attr("class", "task_env hovered_task_env");
	}).mouseleave(function(){
		$(".task_env").attr("class", "task_env");
	});

	$(".reward-label").mouseenter(function(){
		$(".task_env").attr("class", "task_env hovered_task_env");
	}).mouseleave(function(){
		$(".task_env").attr("class", "task_env");
	});

	$(".probability-label").mouseenter(function(){
		$(".task_env").attr("class", "task_env hovered_task_env");
	}).mouseleave(function(){
		$(".task_env").attr("class", "task_env");
	});

	$(".description-label").mouseenter(function(){
		$(".task_env").attr("class", "task_env hovered_task_env");
	}).mouseleave(function(){
		$(".task_env").attr("class", "task_env");
	});
}







function draw_task_perform_environment(parent_id, optimalTaskSets){
	var initialTaskList = null;
	var optimalTaskSelected = false;
	var current_user_energy = $("#predicted-energy").text();
	var current_user_balance = $("#predicted-balance").text();

	// Get the list of tasks to be performed.
	// This is computed on the server side based on the treatment that the user is part of.
	// Store these tasks as initialTaskList - as D3 will later add further (not needed) properties
	// When the tasks are retrieved, draw the task environment
	$.ajax({
		type: "GET",
		url: "/webapp/getTasksToPerform",
		contentType: "application/json",
		success: function(taskList){
			initialTaskList = $.map(taskList, function(task){ return task.fields; });
			draw(taskList);
		}
	});

	// Draw the Tasks (including the animation)
	function draw(task_list){
		// Create the SVG area
		var svg = d3.select("#" + parent_id).append("svg")
			.attr("preserveAspectRatio", "xMidYMin")
			.attr("viewBox", "0 0 " + env_width + " " + env_height)
			.attr("width", env_width)
			.attr("height", env_height);

		// Draw the "Background" Rectangle 
		var task_env = svg.append("rect")
			.attr("x", 1)
			.attr("y", 1)
			.attr("rx", 15)
			.attr("ry", 15)
			.attr("width", env_width - 2)
			.attr("height", env_height - 2)
			.attr("class", "task_env");

		task_env
			.on("mouseenter", function(){
				d3.select(this).attr("stroke", "#786370");
			})
			.on("mouseleave", function(){
				d3.select(this).attr("stroke", "none");
			});

		var lineFunction = d3.svg.line()
								.x(function(d){ return d.x; })
								.y(function(d){ return d.y; })
								.interpolate("linear");


		// Draw a task image for each task at the specified XY coordinates
		d3.select("svg").selectAll("image")
			.data(task_list)
			.enter()
			.append("svg:image")
			.attr("x", function(d, i){return d.fields.x * env_width - (task_width / 2)})
			.attr("y", function(d, i){return d.fields.y * env_height - (task_width / 2)})
			.attr("width", task_width)
			.attr("height", task_width)
			.attr("xlink:href", function(d){ return d.fields.task_icon;})
			.attr("class", "task");

		// Add the house image on the center of the drawn area
		svg.append("svg:image")
			.attr("id", "home_image")
			.attr("x", env_width / 2 - (home_image_width / 2))
			.attr("y", env_height / 2 - (home_image_width / 2))
			.attr("width", home_image_width)
			.attr("height", home_image_width)
			.attr("xlink:href", "/static/webapp/img/house-icon2.png");

		function drawShortestPath(taskDescriptions){
			// Construct the data to be used by the svg path
			// This data should be an array of points [(x, y), (x, y), ...]
			var lineData = [];

			// Add the first edge (Home - Task 1) 
			lineData.push({"x" : env_width / 2, "y" : env_height / 2})

			taskDescriptions = taskDescriptions.split(";");

			for (var i = 0; i < taskDescriptions.length; i++){
				// Get actual task with this description
				var task = null;
				var j = 0; 
				var found = false;
				while (j < task_list.length && !found){
					if (task_list[j]["fields"]["description"] == taskDescriptions[i]){
						found = true;
						task = task_list[j];
					}
					else j++;
				}

				lineData.push({
					"x" : task.fields.x * env_width,
					"y" : task.fields.y * env_height + task_width / 2
				});
			}

			// Add the last edge (Task N - Home)
			lineData.push({"x" : env_width / 2, "y" : env_height / 2});

			// Clear any drawn paths
			clearPath();

			var path = svg.append("path")
				.attr("id", "optimal_path")
				.attr("d", lineFunction(lineData))
				.attr("stroke", "white")
				.attr("stroke-width", 3)
				.attr("fill", "none");

			var totalLength = path.node().getTotalLength();

			path.attr("stroke-dasharray", totalLength + " " + totalLength)
				.attr("stroke-dashoffset", totalLength)
				.transition()
					.duration(400)
					.ease("linear")
					.attr("stroke-dashoffset", 0);


			// Move all Task Images to front
			d3.selectAll("image").moveToFront();
		}

		$(".option-row").hover(function(){
			if (!optimalTaskSelected){
				if ($(this).attr("id") == "x"){
					clearPath();
				}
				else{
					drawShortestPath(optimalTaskSets[$(this).attr("id") - 1][0]);
					setScenarioProperties(optimalTaskSets[$(this).attr("id") - 1][1], optimalTaskSets[$(this).attr("id") - 1][2], optimalTaskSets[$(this).attr("id") - 1][3]);
				}
			}
		});

		$(".option-row").click(function(){
			$("#radio-" + $(this).attr("id")).prop("checked", true);
			optimalTaskSelected = true;

			if ($(this).attr("id") == "x"){
				clearPath();
				$("#next-day-btn-text").html("<span class='fa fa-arrow-right fa-3x'></span><br/>Next Day");
			}
			else{
				drawShortestPath(optimalTaskSets[$(this).attr("id") - 1][0]);
				setScenarioProperties(optimalTaskSets[$(this).attr("id") - 1][1], optimalTaskSets[$(this).attr("id") - 1][2], optimalTaskSets[$(this).attr("id") - 1][3]);
				$("#next-day-btn-text").html("<span class='fa fa-car fa-3x'></span><br/>Perform Tasks<span>");
			}

			$("#next-day-btn").removeClass("disabled");
		});

		// Remove any existing svg optimal paths drawn on the task environment
		// Selects all paths with a specifc ID and removes them
		function clearPath(){
			svg.selectAll("#optimal_path").remove();
			resetScenarioProperties();
		}

		function setScenarioProperties(totalReward, totalDistance, totalKwh){
			$("#predicted-balance").text((parseFloat(current_user_balance) + totalReward).toFixed(2));
			$("#predicted-energy").text((parseFloat(current_user_energy) - totalKwh).toFixed(2));
			// $("#scenario_reward").text(totalReward.toFixed(2));
			// $("#scenario_distance").text(totalDistance.toFixed(2));
			// $("#scenario_energy").text( 1.2 * (totalDistance).toFixed(2));
		}

		function resetScenarioProperties(){
			$("#predicted-balance").text(current_user_balance);
			$("#predicted-energy").text(current_user_energy);
		}

		// Redraw whenever window is resized
		$(window).resize(function() {
			svg.attr("width", calculateEnvWidth())
				.attr("height", calculateEnvHeight());
		});


		$("#home_image").mouseenter(function(){
			$(".task_env").attr("class", "task_env hovered_task_env");
		}).mouseleave(function(){
			$(".task_env").attr("class", "task_env");
		});

		$(".task").mouseenter(function(){
			$(".task_env").attr("class", "task_env hovered_task_env");
		}).mouseleave(function(){
			$(".task_env").attr("class", "task_env");
		});

		$(".reward-label").mouseenter(function(){
			$(".task_env").attr("class", "task_env hovered_task_env");
		}).mouseleave(function(){
			$(".task_env").attr("class", "task_env");
		});

		$(".probability-label").mouseenter(function(){
			$(".task_env").attr("class", "task_env hovered_task_env");
		}).mouseleave(function(){
			$(".task_env").attr("class", "task_env");
		});

		$(".description-label").mouseenter(function(){
			$(".task_env").attr("class", "task_env hovered_task_env");
		}).mouseleave(function(){
			$(".task_env").attr("class", "task_env");
		});
	}					
}