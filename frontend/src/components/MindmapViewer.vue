<template>
    <div id="mindmap-viewer">
        <div class="grid-container">
            <div id="network"></div>
            <div id="menu" class="p-3">
                <div id="properties" class="border border-success rounded p-2">
                    <button class="btn btn-success btn-block" :disabled="inAddMode" @click="addNodeMode()">
                        Add Node
                    </button>
                    <button class="btn btn-success btn-block mt-2" :disabled="inAddMode" @click="addEdgeMode()">
                        Add Edge
                    </button>
                    <template v-if="selectedNode">
                        <div class="form-group mt-2">
                            <input type="text" class="form-control" v-model="selectedNode.label"
                                   placeholder="Enter node title">
                            <button class="btn btn-danger btn-block mt-2" @click="deleteNode()">
                                Delete Node
                            </button>
                        </div>
                    </template>
                    <div v-else class="mt-2">
                        <p>Select Node To Modify...</p>
                    </div>

                </div>
            </div>
        </div>
        <div class="spin" v-if="loading">
            <div class="cp-spinner cp-heart"></div>
        </div>
        <b-modal id="modal" v-model="modalShow" title="Сталася помилка!" :ok-only="true">
            Вся команда розробників вже знає про це та намагається все виправити. Зверніть увагу, що наш сервер не
            оброблює зображення, більші за 10 МБ. Якщо виділень на конспекті дуже багато та сервер завантажений, можуть
            статися помилки. Спробуйте оновити сторінку!
        </b-modal>
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
        props: ['canvas', 'lang'],
        methods: {
            addNode(nodeData, callback) {
                callback(nodeData);
                this.inAddMode = false;
            },
            addEdge(nodeData, callback) {
                callback(nodeData);
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
            },
            onSelectNode(e) {
                this.selectedNode = this.nodes.get(e.nodes[0]);
            },
            onDeselectNode() {
                this.selectedNode = null;
            }
        },
        watch: {
            selectedNode: {
                handler(newValue, oldValue) {
                    if (newValue != null && oldValue != null) {
                        delete newValue.x;
                        delete newValue.y;
                        this.nodes.update(newValue);
                    }
                },
                deep: true,
            }
        },
        data() {
            return {
                inAddMode: false,
                nodes: [],
                edges: [],
                selectedNode: null,
                loading: false,
                modalShow: false,
            }
        }
        ,
        network: null,
        async mounted() {
            this.loading = true;

            let response;
            try {
                response = await $.ajax({
                    method: 'POST',
                    url: '/api/note',
                    data: {
                        'canvas': this.canvas,
                        'lang': this.lang
                    },

                    headers: {
                        'X-Requested-With': 'XMLHttpRequest',
                        'X-CSRFToken': $.cookie('csrftoken'),
                    }
                });
            } catch (e) {
                response = {
                    nodes: [],
                    edges: []
                };
            }

            this.loading = false;

            let container = document.getElementById('network');

            this.nodes = new vis.DataSet(response.nodes);
            this.edges = new vis.DataSet(response.edges);

            let data = {
                nodes: this.nodes,
                edges: this.edges
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

    .spin {
        position: fixed;
        display: flex;
        width: 100vw;
        height: 100vh;
        top: 0;
        left: 0;
        z-index: 1000;
        justify-content: center;
        align-items: center;
        background-color: rgba(128, 128, 128, .5);
    }
</style>