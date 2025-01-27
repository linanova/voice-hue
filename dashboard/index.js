function history() {
  return {
      commands: [],
      init() {
          this.commands = ['Make it blue', 'Turn it red', 'I want it green'];
      }
  };
}

function graph() {
    return {
        colors: ['red', 'green', 'blue', 'orange', 'purple', 'yellow', 'pink'],
        createGraph() {
            const svg = d3.select(".graph svg");

            const width = svg.node().getBoundingClientRect().width;
            const height = svg.node().getBoundingClientRect().height;

            const data = Array.from({ length: 20 }, () => ({
                x: Math.random() * width,
                y: Math.random() * height,
                r: Math.random() * 50 + 10,
                color: this.colors[Math.floor(Math.random() * this.colors.length)]
            }));

            svg
                .selectAll(".dot")
                .data(data)
                .enter()
                .append("circle")
                .attr("class", "dot")
                .attr("cx", d => d.x)
                .attr("cy", d => d.y)
                .attr("r", d => d.r)
                .attr("fill", d => d.color);
        }
    };
}

function routing() {
  return {
      route: 'visualize',
      setActiveRoute(route) {
          this.route = route;
      }
  };
}