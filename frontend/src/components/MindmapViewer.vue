<template>
    <v-container fluid pa-0>
        <div class="grid-container">
            <div id="network"></div>
            <div id="menu" class="p-3">
                <v-navigation-drawer permanent right absolute>
                    <v-list-tile class="py-3">
                        <v-list-tile-action>
                            <v-icon>map</v-icon>
                        </v-list-tile-action>
                        <v-list-tile-content>
                            <v-text-field type="text" v-model="title" label="Назва ментальної карти"></v-text-field>
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
                                <v-text-field label="Текст вузла" type="text" v-model="selectedNode.label"
                                              placeholder="Текст вузла..."></v-text-field>
                            </v-list-tile-content>
                        </v-list-tile>
                        <v-divider></v-divider>
                        <v-list-tile class="py-3">
                            <v-list-tile-content>
                                <v-btn color='red' @click="deleteNode()" block>
                                    Видалити вузол
                                </v-btn>
                            </v-list-tile-content>
                        </v-list-tile>
                    </template>
                    <v-list-tile v-else class="py-3">
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
                    let nodeDS = this.nodesDataSet.get();
                    for (let i of nodeDS) {
                        i.x = this.network.body.nodes[i.id].x;
                        i.y = this.network.body.nodes[i.id].y;
                    }
                    await $.ajax({
                        url: '/api/rest/mindmaps/' + this.id.toString() + '/',
                        data: {
                            title: this.title,
                            mindmap: JSON.stringify({
                                nodes: nodeDS,
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
                } catch (e) {
                    console.log(e);
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