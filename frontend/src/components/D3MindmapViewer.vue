<template>
    <div id="mindmap-viewer">
        <svg :width="width" :height="height">
            <g class="links" stroke="#999" stroke-opacity="0.6">
                <line v-for="link in links" :stroke-width="link.value"></line>
            </g>
            <g class="nodes" ref="nodes">
                <g v-for="node in nodes">
                    <text dominant-baseline="middle" text-anchor="middle">{{ node.id }}</text>
                    <rect rx="8" ry="8"
                          :width="getBoundingBoxSize(node.id).width + 10"
                          :height="getBoundingBoxSize(node.id).height + 10"
                          :x="-(getBoundingBoxSize(node.id).width + 10) / 2"
                          :y="-(getBoundingBoxSize(node.id).height + 10) / 2"
                          style="fill:transparent;stroke:black;stroke-width:2"></rect>
                </g>
            </g>
        </svg>
    </div>
</template>

<script>
    import * as d3 from "d3";

    export default {
        name: "D3MindmapViewer",
        data() {
            return {
                width: 500,
                height: 500,
                nodes: [
                    {id: "Hans"},
                    {id: "Napoleon"},
                    {id: "Jackie"},
                    {id: "Mike"},
                ],
                links: [
                    {source: "Hans", target: "Napoleon", value: 10},
                    {source: "Jackie", target: "Napoleon", value: 10},
                    {source: "Mike", target: "Napoleon", value: 10},
                ]
            }
        },
        mounted() {
            const simulation = d3.forceSimulation(this.nodes)
                .force("link", d3.forceLink(this.links).id(d => d.id).distance(200).strength(0.1))
                .force("charge", d3.forceManyBody())
                .force("center", d3.forceCenter(this.width / 2, this.height / 2));

            const link = d3.select(".links").data(this.links);

            const node = d3.select(".nodes")
                .data(this.nodes)
                .selectAll('g')
                .call(this.drag(simulation));

            simulation.on("tick", () => {
                link
                    .attr("x1", d => d.source.x)
                    .attr("y1", d => d.source.y)
                    .attr("x2", d => d.target.x)
                    .attr("y2", d => d.target.y);

                node
                    .attr("transform", function (d) {
                        return "translate(" + d.x + "," + d.y + ")";
                    })
            });

        },
        methods: {
            getBoundingBoxSize(text) {
                let element = document.createElementNS('http://www.w3.org/2000/svg', 'text');
                element.innerHTML = text;
                document.body.append(element);
                let bbox = element.getBBox();
                let width = bbox.width,
                    height = bbox.height;
                element.remove();
                return {
                    width, height
                };
            },
            drag(simulation) {
                function dragStarted(d) {
                    if (!d3.event.active) simulation.alphaTarget(0.3).restart();
                    d.fx = d.x;
                    d.fy = d.y;
                }

                function dragContinued(d) {
                    d.fx = d3.event.x;
                    d.fy = d3.event.y;
                }

                function dragEnded(d) {
                    if (!d3.event.active) simulation.alphaTarget(0);
                    d.fx = null;
                    d.fy = null;
                }

                return d3.drag()
                    .on("start", dragStarted)
                    .on("drag", dragContinued)
                    .on("end", dragEnded);
            }
        }
    }
</script>

<style scoped>

</style>