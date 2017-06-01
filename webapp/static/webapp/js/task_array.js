// ******************************************************************************************************
// Custom JS object which can hold and keep track of a series of Task objects.
// Similar behaviour with an array object, but provides a custom sort method and string representation
//
// Methods available:
//
// add(task): 
//		Adds a task object to the array
// remove(task): 
//		Removes a particular tasks from the array 
//		Returns true if the task was found and removed, false otherwise
// get(index): 
//		Retrieve task at position "index" in the array
// getArray():
//		Retrieve the array of tasks as a plain Javascript array object
// length(): 
//		Returns the number of tasks 
// sort(): 
//		Sorts the array of tasks alphabetically based on their description
// resetTasks(): 
//		Deletes all tasks from the array and initializes a new empty tasks array
// stringRepresentation(): 
//		Returns a string consisting of all task descriptions, concatenated 
//		and separated by the separator character
// buildFromStringRepresentation(str, tasks): 
//		Builds the array of tasks based on a string of concatenated descriptions ("str").
//		Each description is looked up in a provided array of task objects ("tasks").	
// compareTasks(t1, t2): 
//		Compares two tasks based on their description. 
//		Returns -1 if t1 > t2, 1 if t2 > t1 and 0 if tasks are equal.
//
// Author: Adrian Nedea (an2n13@soton.ac.uk)
// ******************************************************************************************************

function TaskArray(){
	this.tasks = new Array();

	this.add = function(task){
		this.tasks.push(task);
	};

	this.remove = function(task){
		var found = false;
		for (var i = 0; i < this.tasks.length && !found; i++){
			if (this.tasks[i].fields.description == task.fields.description){
				found = true;
				this.tasks.splice(i, 1);
			}
		}
	};

	this.get = function(index){ return this.tasks[index]; };

	this.getArray = function(){ return this.tasks; };

	this.length = function(){ return this.tasks.length; };

	this.sort = function(){ this.tasks.sort(compareTasks); };

	this.resetTasks = function(){ this.tasks = new Array(); };

	this.stringRepresentation = function(){
		var str = "";
		for (var i = 0; i < this.tasks.length; i++){
			str += this.tasks[i].fields.description + ";";
		}
		return str.substring(0, str.length - 1)
	};

	this.buildFromStringRepresentation = function(str, tasks){
		// Reset the tasks array
		this.resetTasks();

		// Split the provided string of descriptions
		var descriptions_arr = str.split(";");

		// For each description, loop through all tasks, find the one with 
		// the corresponding description and add it to the list of tasks.
		for (var i = 0; i < descriptions_arr.length; i++){
			// Flag used to stop looping when a task is found
			var added = false;
			
			for (var j = 0; j < tasks.length && !added; j++){
				if (tasks[j].fields.description == descriptions_arr[i]){
					this.tasks.push(tasks[j]);
					added = true;
				}
			}
		}

		return this.tasks;
	};

	// Function that compares two tasks based on their description properties.
	// The comparison takes into account the alphabetical order of the two description strings.
	// Function can be used for sorting a string of tasks.
	function compareTasks(t1, t2){ 
		return t1.fields.description.localeCompare(t2.fields.description); 
	}
}