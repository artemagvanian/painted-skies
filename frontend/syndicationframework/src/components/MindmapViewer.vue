<template>
    <div id="mindmap-viewer">
        <div id="mynetwork"></div>
        <div id="network-popUp" style="display: none;">
            <span id="operation">Edit Node</span>
            <b-input id="node-label" value="new value" class="my-2"></b-input>
            <b-button type="button" id="saveButton" class="mx-2">Save</b-button>
            <b-button type="button" id="cancelButton" class="mx-2">Cancel</b-button>
        </div>
    </div>
</template>

<script>
    let vis = require('vis/dist/vis.min.js');
    require('vis/dist/vis.min.css');

    export default {
        name: "MindmapViewer",
        methods: {
            clearPopUp() {
                document.getElementById('saveButton').onclick = null;
                document.getElementById('cancelButton').onclick = null;
                document.getElementById('network-popUp').style.display = 'none';
            },

            cancelEdit(callback) {
                this.clearPopUp();
                callback(null);
            },

            saveData(data, callback) {
                data.label = document.getElementById('node-label').value;
                this.clearPopUp();
                callback(data);
            },
        },
        data() {
            return {
                nodes: [
                    {id: 1, label: 'Node 1', color: 'red'},
                    {id: 2, label: 'Node 2'},
                    {id: 3, label: 'Node 3'},
                    {id: 4, label: 'Node 4'},
                    {id: 5, label: 'Node 5'}
                ],
                edges: [
                    {from: 1, to: 3},
                    {from: 1, to: 2},
                    {from: 2, to: 4},
                    {from: 2, to: 5}
                ],
                container: ''
            }
        }
        ,
        network: null,
        mounted() {
            this.container = document.getElementById('mynetwork');

            this.nodes = this.$parent.$data.mindmap.nodes;
            this.edges = this.$parent.$data.mindmap.edges;

            let data = {
                nodes: this.nodes,
                edges: this.edges
            };

            let vm = this;

            let options = {
                manipulation: {
                    enabled: true,
                    initiallyActive: true,
                    editNode: function (data, callback) {
                        // filling in the popup DOM elements
                        document.getElementById('operation').innerHTML = "Edit Node";
                        document.getElementById('node-label').value = data.label;
                        document.getElementById('saveButton').onclick = vm.saveData.bind(this, data, callback);
                        document.getElementById('cancelButton').onclick = vm.cancelEdit.bind(this, callback);
                        document.getElementById('network-popUp').style.display = 'block';
                    },
                }
                ,
                interaction: {
                    dragView: false,
                    dragNodes: false,
                    multiselect: true,
                    hover: true,
                }
            };

            this.network = new vis.Network(this.container, data, options);
        }
    }
</script>

<style scoped>
    #mynetwork {
        width: 100vw;
        height: 100vh;
        border: 1px solid lightgray;
    }

    #operation {
        font-size: 28px;
    }

    #network-popUp {
        display: none;
        position: absolute;
        top: calc(50vh - 80px);
        left: calc(50vw - 135px);
        z-index: 299;
        background-color: #f9f9f9;
        border-style: solid;
        border-width: 3px;
        border-color: #5394ed;
        border-radius: 5px;
        padding: 10px;
        text-align: center;
    }
</style>