<template>
    <div id="mindmap-viewer">
        <div class="grid-container">
            <div id="network"></div>
            <div id="menu" class="p-3">
                <div id="properties" class="border border-success rounded p-2">
                    <input class="form-control" type="text" v-model="title">
                    <p class="text-muted my-3 text-center">{{ this.saveStatus }}</p>
                    <button class="btn btn-success btn-block" :disabled="inAddMode" @click="addNodeMode()">
                        Додати вузол
                    </button>
                    <button class="btn btn-success btn-block mt-2" :disabled="inAddMode" @click="addEdgeMode()">
                        Додати ребро
                    </button>
                    <template v-if="selectedNode">
                        <div class="form-group mt-2">
                            <input type="text" class="form-control" v-model="selectedNode.label"
                                   placeholder="Текст вузла...">
                            <button class="btn btn-danger btn-block mt-2" @click="deleteNode()">
                                Delete Node
                            </button>
                        </div>
                    </template>
                    <div v-else class="mt-3 text-center">
                        <p>Виберіть вузол для редагування...</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    import $ from 'jquery'
    import 'jquery.cookie/jquery.cookie'
    import 'csspin/css/csspin-heart.css'

    import vis from 'vis/dist/vis.min.js';
    import 'vis/dist/vis.min.css'

    export default {
        name: "MindmapViewer",
        props: ['nodes', 'edges', 'id'],
        methods: {
            addNode(nodeData, callback) {
                callback(nodeData);
                this.saveMindmap();
                this.inAddMode = false;
            },
            addEdge(nodeData, callback) {
                callback(nodeData);
                this.saveMindmap();
                this.inAddMode = false;
            },
            addNodeMode() {
                this.network.addNodeMode();
                this.inAddMode = true;
            },
            addEdgeMode() {
                this.network.addEdgeMode();
                this.inAddMode = true;
            },
            deleteNode() {
                this.network.deleteSelected();
                this.selectedNode = null;
                this.saveMindmap();
            },
            onSelectNode(e) {
                this.selectedNode = this.nodesDataSet.get(e.nodes[0]);
            },
            onDeselectNode() {
                this.selectedNode = null;
            },
            async obtainMindmap() {
                try {
                    if (this.id === undefined) {
                        let mindmap = await $.ajax({
                            url: '/api/rest/mindmaps/',
                            data: {
                                title: this.title,
                                mindmap: JSON.stringify({
                                    nodes: this.nodes,
                                    edges: this.edges,
                                })
                            },
                            method: 'POST',
                            headers: {
                                'Authorization': 'JWT ' + this.$session.get('jwt'),
                                'X-Requested-With': 'XMLHttpRequest',
                                'X-CSRFToken': $.cookie('csrftoken'),
                            }
                        });
                        this.id = mindmap.id;
                        this.nodesDataSet = new vis.DataSet(this.nodes);
                        this.edgesDataSet = new vis.DataSet(this.edges);

                    } else {
                        let mindmap = await $.ajax({
                            url: '/api/rest/mindmaps/' + this.id.toString() + '/',
                            method: 'GET',
                            headers: {
                                'Authorization': 'JWT ' + this.$session.get('jwt'),
                                'X-Requested-With': 'XMLHttpRequest',
                                'X-CSRFToken': $.cookie('csrftoken'),
                            }
                        });
                        this.title = mindmap.title;
                        let mindmapElements = JSON.parse(mindmap.mindmap);
                        this.nodesDataSet = new vis.DataSet(mindmapElements.nodes);
                        this.edgesDataSet = new vis.DataSet(mindmapElements.edges);
                    }
                } catch {
                    this.nodesDataSet = new vis.DataSet(this.nodes);
                    this.edgesDataSet = new vis.DataSet(this.edges);
                    this.saveStatus = 'Дані не збережено'
                }
            },
            async saveMindmap() {
                try {
                    this.saveStatus = 'Зберігаємо дані...';
                    await $.ajax({
                        url: '/api/rest/mindmaps/' + this.id.toString() + '/',
                        data: {
                            title: this.title,
                            mindmap: JSON.stringify({
                                nodes: this.nodesDataSet.get(),
                                edges: this.edgesDataSet.get(),
                            })
                        },
                        method: 'PUT',
                        headers: {
                            'Authorization': 'JWT ' + this.$session.get('jwt'),
                            'X-Requested-With': 'XMLHttpRequest',
                            'X-CSRFToken': $.cookie('csrftoken'),
                        }
                    });
                    this.saveStatus = 'Дані збережено'
                } catch {
                    this.saveStatus = 'Дані не збережено'
                }
            }
        },
        watch: {
            selectedNode: {
                handler(newValue, oldValue) {
                    if (newValue != null && oldValue != null) {
                        delete newValue.x;
                        delete newValue.y;
                        this.nodesDataSet.update(newValue);
                        this.saveMindmap();
                    }
                },
                deep: true,
            },
            title() {
                this.saveMindmap();
            }

        },
        data() {
            return {
                edgesDataSet: [],
                saveStatus: 'Дані збережено',
                inAddMode: false,
                nodesDataSet: [],
                selectedNode: null,
                title: 'Нова ментальна карта'
            }
        }
        ,
        network: null,
        async mounted() {
            let container = document.getElementById('network');

            await this.obtainMindmap();

            let data = {
                nodes: this.nodesDataSet,
                edges: this.edgesDataSet
            };

            let options = {
                manipulation: {
                    enabled: false,
                    addNode: this.addNode,
                    addEdge: this.addEdge,
                },
                interaction: {
                    hover: true,
                    selectConnectedEdges: false,
                },
                physics: {
                    enabled: false,
                }
            };

            this.network = new vis.Network(container, data, options);

            this.network.on('selectNode', this.onSelectNode);
            this.network.on('deselectNode', this.onDeselectNode);
        }
    }
</script>

<style scoped>
    .grid-container {
        display: grid;
        width: 100vw;
        height: 100vh;
        grid-template-columns: 3fr 1fr;
        overflow: hidden;
    }
</style>