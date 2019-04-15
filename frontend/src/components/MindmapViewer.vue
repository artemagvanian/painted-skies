<template>
    <v-container fluid pa-0>
        <div class="grid-container">
            <div id="network"></div>
            <div class="p-3" id="menu">
                <v-navigation-drawer permanent right>
                    <v-list-tile class="py-3">
                        <v-list-tile-action>
                            <v-icon>map</v-icon>
                        </v-list-tile-action>
                        <v-list-tile-content>
                            <v-text-field label="Назва ментальної карти" type="text" v-model="title"></v-text-field>
                        </v-list-tile-content>
                    </v-list-tile>
                    <v-divider></v-divider>
                    <v-list-tile class="py-3">
                        <v-list-tile-action>
                            <v-icon>sync</v-icon>
                        </v-list-tile-action>
                        <v-list-tile-content>
                            <p class="text-muted my-3 text-center">{{ this.saveStatus }}</p>
                        </v-list-tile-content>
                    </v-list-tile>
                    <v-divider></v-divider>
                    <v-list-tile class="py-3">
                        <v-list-tile-content>
                            <v-btn :disabled="inAddMode" @click="addNodeMode()" block>
                                Додати вузол
                            </v-btn>
                        </v-list-tile-content>
                    </v-list-tile>
                    <v-divider></v-divider>
                    <v-list-tile class="py-3">
                        <v-list-tile-content>
                            <v-btn :disabled="inAddMode" @click="addEdgeMode()" block>
                                Додати ребро
                            </v-btn>
                        </v-list-tile-content>
                    </v-list-tile>
                    <v-divider></v-divider>
                    <template v-if="selectedNode">
                        <v-list-tile class="py-3">
                            <v-list-tile-action>
                                <v-icon>textsms</v-icon>
                            </v-list-tile-action>
                            <v-list-tile-content>
                                <v-text-field label="Текст вузла" placeholder="Текст вузла..." type="text"
                                              v-model="selectedNode.label"></v-text-field>
                            </v-list-tile-content>
                        </v-list-tile>
                        <v-divider></v-divider>
                        <v-list-tile class="py-3">
                            <v-list-tile-content>
                                <v-btn @click="deleteNode()" block color='red'>
                                    Видалити вузол
                                </v-btn>
                            </v-list-tile-content>
                        </v-list-tile>
                    </template>
                    <v-list-tile class="py-3" v-else>
                        <div :style="{ width: 'calc(100% - 16px)', textAlign: 'center' }">
                            <p>Виберіть вузол для редагування</p>
                        </div>
                    </v-list-tile>
                </v-navigation-drawer>
            </div>
        </div>
    </v-container>
</template>

<script>
    import 'jquery.cookie/jquery.cookie'
    import 'csspin/css/csspin-heart.css'

    import vis from 'vis/dist/vis.min.js';
    import 'vis/dist/vis.min.css'
    import Mindmaps from '../utils/api/Mindmap'

    export default {
        name: "MindmapViewer",
        props: ['nodes', 'edges', 'id'],
        methods: {
            addNode(nodeData, callback) {
                callback(nodeData);
                this.saveMindmap();
                this.inAddMode = false;
            },
            addEdge(edgeData, callback) {
                edgeData.arrows = 'to';
                callback(edgeData);
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
            async saveMindmap() {
                try {
                    this.saveStatus = 'Зберігаємо дані...';
                    let nodeDS = this.nodesDataSet.get();
                    for (let i of nodeDS) {
                        i.x = this.network.body.nodes[i.id].x;
                        i.y = this.network.body.nodes[i.id].y;
                    }
                    await Mindmaps.update(
                        this.mindmapId.toString(),
                        this.title,
                        nodeDS,
                        this.edgesDataSet.get()
                    );
                    this.saveStatus = 'Дані збережено'
                } catch (e) {
                    this.saveStatus = 'Дані не збережено'
                }
            },
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
                title: 'Нова ментальна карта',
                mindmapId: null,
            }
        }
        ,
        network: null,
        async mounted() {
            let container = document.getElementById('network');

            try {
                if (this.id === undefined) {
                    let mindmap = await Mindmaps.create(this.title, this.nodes, this.edges);
                    this.mindmapId = mindmap.data.id;
                    this.nodesDataSet = new vis.DataSet(this.nodes);
                    this.edgesDataSet = new vis.DataSet(this.edges);

                } else {
                    let mindmap = await Mindmaps.retrieve(this.id.toString());
                    this.mindmapId = mindmap.data.id;
                    this.title = mindmap.data.title;
                    let mindmapElements = JSON.parse(mindmap.data.mindmap);
                    this.nodesDataSet = new vis.DataSet(mindmapElements.nodes);
                    this.edgesDataSet = new vis.DataSet(mindmapElements.edges);
                }
            } catch {
                this.nodesDataSet = new vis.DataSet(this.nodes);
                this.edgesDataSet = new vis.DataSet(this.edges);
                this.saveStatus = 'Дані не збережено'
            }

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
            this.network.on('release', this.saveMindmap);
        }
    }
</script>

<style scoped>
    .grid-container {
        display: grid;
        width: 100vw;
        height: calc(100vh - 69px);
        grid-template-columns: 1fr 300px;
        overflow: hidden;
    }
</style>
