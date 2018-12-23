<template>
    <div id="mindmap-viewer">
        <div id="mynetwork"></div>
        <div id="network-popUp" style="display: none;">
            <span id="operation">Edit Node</span>
            <b-input id="node-label" value="new value" class="my-2"></b-input>
            <b-button type="button" id="saveButton" class="mx-2">Save</b-button>
            <b-button type="button" id="cancelButton" class="mx-2">Cancel</b-button>
        </div>
        <div class="spin" v-if="loading">
            <div class="cp-spinner cp-heart"></div>
        </div>
        <b-modal id="modal" v-model="modalShow" title="Сталася помилка!" ok-only="true">
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
                nodes: [],
                edges: [],
                container: '',
                loading: false,
                modalShow: false,
            }
        }
        ,
        network: null,
        mounted() {
            this.loading = true;
            $.ajax({
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
                }
            ).then((result) => {
                this.loading = false;
                this.container = document.getElementById('mynetwork');

                this.nodes = result.nodes;
                this.edges = result.edges;

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
                    },
                    interaction: {
                        dragView: false,
                        multiselect: true,
                        hover: true,
                    },
                    physics: {
                        enabled: false,
                    }
                };

                this.network = new vis.Network(this.container, data, options);
            }).catch((e) => {
                this.loading = false;
                this.modalShow = true;
            });
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