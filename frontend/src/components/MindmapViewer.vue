<template>
    <div id="mindmap-viewer">
        <div class="grid-container">
            <div id="network"></div>
            <div id="menu" class="p-3">
                <div id="properties" class="border border-success rounded p-2">
                    <button class="btn btn-success btn-block" @click="addNode()">Add Node</button>
                    <button class="btn btn-success btn-block mt-2" @click="addEdge()">Add Edge</button>
                    <template v-if="selectedNode">
                        <div class="form-group mt-2">
                            <input type="text" class="form-control" v-model="selectedNode.label"
                                   placeholder="Enter node title">
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
    import 'csspin/css/csspin-heart.css'

    import vis from 'vis/dist/vis.min.js';
    import 'vis/dist/vis.min.css'

    export default {
        name: "MindmapViewer",
        props: ['canvas', 'lang'],
        methods: {
            addNode() {
                this.network.addNodeMode();
            },
            addEdge() {
                this.network.addEdgeMode();
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
            try {
                this.loading = true;
                let response = await $.ajax({
                    method: 'POST',
                    url: '/api/note',
                    data: {
                        'canvas': this.canvas,
                        'lang': this.lang
                    },

                    headers: {
                        'X-Requested-With': 'XMLHttpRequest',
                        'X-CSRFToken': $("[name=csrfmiddlewaretoken]").val(),
                    }
                });

                // let response = {
                //     nodes: [
                //         {id: 1, label: 'comco'},
                //         {id: 2, label: 'camca'},
                //     ],
                //     edges: [
                //         {id: 1, from: 1, to: 2},
                //     ]
                // };

                this.loading = false;
                let container = document.getElementById('network');

                this.nodes = new vis.DataSet(response.nodes);
                this.edges = new vis.DataSet(response.edges);

                let data = {
                    nodes: this.nodes,
                    edges: this.edges
                };

                let options = {
                    interaction: {
                        dragView: false,
                        hover: true,
                    },
                    physics: {
                        enabled: false,
                    }
                };

                this.network = new vis.Network(container, data, options);

                this.network.on('selectNode', this.onSelectNode);
                this.network.on('deselectNode', this.onDeselectNode);

            } catch (e) {
                this.loading = false;
                this.modalShow = true;
            }
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