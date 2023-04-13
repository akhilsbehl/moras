// Define the SVG dimensions and margin
var margin = { top: 20, right: 20, bottom: 30, left: 40 },
    width = 960 - margin.left - margin.right,
    height = 500 - margin.top - margin.bottom;

// Define the x and y scales and axes
var x0 = d3.scaleBand().rangeRound([0, width]).paddingInner(0.1);
var x1 = d3.scaleBand().padding(0.05);
var y = d3.scaleLinear().rangeRound([height, 0]);
var xAxis = d3.axisBottom(x0);
var yAxis = d3.axisLeft(y).ticks(10, "%");

// Define the color scale
var color = d3.scaleOrdinal()
    .range(["#98abc5", "#8a89a6", "#7b6888", "#6b486b", "#a05d56", "#d0743c", "#ff8c00"]);

// Create the SVG element and add the axis groups
var svg = d3.select("body").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

// Load the data from the CSV file on the server-side
d3.csv("/static/analytics.csv", function(error, data) {
    if (error) console.log(error);

    // Nest the data by Kana Type and Kana
    var nestedData = d3.nest()
        .key(function(d) { return d["Kana Type"]; })
        .key(function(d) { return d["Kana"]; })
        .rollup(function(d) { return d3.mean(d, function(d) { return d["Accuracy"]; }); })
        .entries(data);

    // Update the domains of the x and y scales
    x0.domain(nestedData.map(function(d) { return d.key; }));
    x1.domain(nestedData[0].values.map(function(d) { return d.key; })).rangeRound([0, x0.bandwidth()]);
    y.domain([0, d3.max(nestedData, function(d) { return d3.max(d.values, function(d) { return d.value; }); })]);

    // Add the x and y axes
    svg.append("g")
        .attr("class", "x axis")
        .attr("transform", "translate(0," + height + ")")
        .call(xAxis);

    svg.append("g")
        .attr("class", "y axis")
        .call(yAxis)
        .append("text")
        .attr("transform", "rotate(-90)")
        .attr("y", 6)
        .attr("dy", ".71em")
        .style("text-anchor", "end")
        .text("Accuracy");

    // Add the bars to the chart
    var kanaType = svg.selectAll(".kanaType")
        .data(nestedData)
        .enter().append("g")
        .attr("class", "kanaType")
        .attr("transform", function(d) { return "translate(" + x0(d.key) + ",0)"; });

    kanaType.selectAll("rect")
        .data(function(d) { return d.values; })
        .enter().append("rect")
        .attr("x", function(d) { return x1(d.key); })
        .attr("y", function(d) { return y(d.value); })
        .attr("width", x1.bandwidth())
        .attr("height", function(d) { return height - y(d.value); })
        .attr("fill", function(d) { return color(d.key); });

    // Add the legend to the chart
    var legend = svg.selectAll(".legend")
        .data(nestedData[0].values.map(function(d) { return d.key; }))
        .enter().append("g")
        .attr("class", "legend")
        .attr("transform", function(d, i) { return "translate(0," + i * 20 + ")"; });

    legend.append("rect")
        .attr("x", width - 18)
        .attr("width", 18)
        .attr("height", 18)
        .style("fill", color);

    legend.append("text")
        .attr("x", width - 24)
        .attr("y", 9)
        .attr("dy", ".35em")
        .style("text-anchor", "end")
        .text(function(d) { return d; });
});
