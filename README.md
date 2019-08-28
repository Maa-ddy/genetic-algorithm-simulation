<h3>Genetic algorithms simulation</h3>
<br/>
<p>This is a simulation of a genetic algorithm<br/>
The population is represented as a group of cells <br/>
The cell's dna has the following properties:
</p>
<ul>
	<li>Radius (the size of the cell)</li>
	<li>vision for food (distance from which a cell can detect food)</li>
	<li>vision for poison (distance from which a cell can detect poison)</li>
	<li>desire for food (attraction towards food (litterally))</li>
	<li>desire for poison (attraction towards poison)</li>
	<li>move noise (distraction on the movement of the cell)</li>
	<li>age (for recording purposes)</li>
</ul>
<p>The algorithm will converge to a solution that will be the most fit to stay alive: <br/>
Eats enough food and avoids poison as possible.
</p>
<p>The attribute 'age' is used to detect how long a generation lasts.<br/>
If a generation lives for too long, it is considered a solution. <br/>
When a cell lives longer than 10000 generations, it is considered as a candidate solution, and it is printed to the console  
(You can redirect that to a file, and feed the value when starting the algorithm again fresh, which probably will yield better solutions)
</p>
<h5>Note:</h5>  
The idea is not original. But the implementation is mine.
