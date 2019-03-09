<template>
    <v-container fluid full-height pa-0>
        <v-toolbar prominent flat>
            <v-layout row justify-center>
                <v-flex>
                    <v-btn v-for="button in modeButtons" @click="mode = button.mode"
                           :color="mode === button.mode ? 'blue' : 'grey darken-1'" class="ma-0 white--text" depressed
                           small>
                        <v-icon>{{ button.icon }}</v-icon>
                    </v-btn>
                </v-flex>
                <v-flex>
                    <v-btn v-for="paintingObject in paintingObjects"
                           :color="paintingObject === activePaintingObject ? paintingObject.buttonStyle : 'grey darken-1'"
                           @click="activate(paintingObject)"
                           :disabled="!levelCanBeActive(paintingObject.level)"
                           class="ma-0 white--text" depressed small>
                        {{ paintingObject.level }}
                    </v-btn>
                </v-flex>
                <v-flex>
                    <v-btn @click="removeLastElement()" class="ma-0 white--text" depressed color="grey darken-1" small>
                        <v-icon>undo</v-icon>
                    </v-btn>
                    <v-btn @click="toggleMergeMode()" :color="this.mergeMode === true ? 'blue' : 'grey darken-1'"
                           class="ma-0 white--text" depressed small>
                        <v-icon>exposure_plus_1</v-icon>
                    </v-btn>
                </v-flex>
                <v-flex>
                    <v-btn @click="zoom *= 1.5" class="ma-0 white--text" depressed color="grey darken-1" small>
                        <v-icon>zoom_in</v-icon>
                    </v-btn>
                    <v-btn @click="zoom /= 1.5" class="ma-0 white--text" depressed color="grey darken-1" small>
                        <v-icon>zoom_out</v-icon>
                    </v-btn>
                </v-flex>
                <v-flex>
                    <v-btn @click="makeMindMap()" class="ma-0 white--text" depressed color="grey darken-1" small>
                        <v-icon>arrow_forward</v-icon>
                    </v-btn>
                </v-flex>
            </v-layout>
        </v-toolbar>
        <canvas id="mainCanvas"></canvas>
        <div class="spin" v-if="loading">
            <div class="cp-spinner cp-heart"></div>
        </div>
        <v-dialog id="modal" v-model="errorModalShow" title="Сталася помилка!" :ok-only="true">
            Вся команда розробників вже знає про це та намагається все виправити. Зверніть увагу, що наш сервер не
            оброблює зображення, більші за 10 МБ. Якщо виділень на конспекті дуже багато та сервер завантажений,
            можуть
            статися помилки. Спробуйте оновити сторінку!
        </v-dialog>
    </v-container>
</template>

<script>
    import * as createjs from '@createjs/easeljs'
    import $ from 'jquery'

    export default {
        name: "CanvasSelector",
        props: ['image', 'lang'],
        methods: {
            activate(paintingObject) {
                this.activePaintingObject = paintingObject;
                this.mode = this.modes.draw;
            },
            checkStageOverflow(maxX, maxY, minX, minY) {
                if (this.stage.x > maxX)
                    this.stage.x = maxX;
                if (this.stage.y > maxY)
                    this.stage.y = maxY;
                if (this.stage.x < minX)
                    this.stage.x = minX;
                if (this.stage.y < minY)
                    this.stage.y = minY;
            },
            getImageScale(canvasElement, imgElement) {
                let widthRatio = canvasElement.width / imgElement.width,
                    heightRatio = canvasElement.height / imgElement.height;
                return Math.max(widthRatio, heightRatio);
            },
            levelCanBeActive(level) {
                try {
                    let lastLevel = this.selections[this.selections.length - 1].level;
                    if (this.mergeMode) {
                        return level === lastLevel;
                    }
                    return level <= lastLevel + 1;
                } catch {
                    return level === 0;
                }
            },
            loadImage() {
                return new Promise((resolve) => {
                    let img = new Image();
                    img.onload = () => resolve(img);
                    img.src = this.image;
                });
            },
            async makeMindMap() {
                this.loading = true;
                try {
                    let response = await $.ajax({
                        method: 'POST',
                        url: '/api/note',
                        data: {
                            'selections': JSON.stringify(this.selections),
                            'lang': this.lang,
                            'image': this.image,
                            'scale': this.scale
                        },

                        headers: {
                            'X-Requested-With': 'XMLHttpRequest',
                            'X-CSRFToken': $.cookie('csrftoken'),
                        }
                    });
                    this.loading = false;
                    this.$router.push({name: 'mindmap', params: {nodes: response.nodes, edges: response.edges}})
                } catch (e) {
                    this.loading = false;
                    this.errorModalShow = true;
                }
            },
            removeLastElement() {
                if (this.selections.length > 0) {
                    let lastElement = this.selections.pop();
                    for (let child of this.stage.children) {
                        if (lastElement.id === child.id) {
                            this.stage.removeChild(child);
                            this.stage.update();
                            break;
                        }
                    }
                }
                this.selectPermittedPaintingObject();
            },
            selectPermittedPaintingObject() {
                let lookup = this.paintingObjects.slice(0, this.activePaintingObject.level + 1).reverse();
                for (let paintingObject of lookup) {
                    if (this.levelCanBeActive(paintingObject.level)) {
                        this.activePaintingObject = paintingObject;
                        break;
                    }
                }
            },
            toggleMergeMode() {
                if (this.selections.length === 0) {
                    this.mergeMode = false;
                } else {
                    this.mergeMode = !this.mergeMode;
                }
                this.selectPermittedPaintingObject();
            }
        },
        data() {
            return {
                activePaintingObject: {},
                backgroundImage: null,
                backgroundImageSize: {},
                errorModalShow: false,
                loading: false,
                mode: 2,
                mergeMode: false,
                modeButtons: [
                    {mode: 1, icon: 'pan_tool'},
                    {mode: 2, icon: 'brush'},
                ],
                modes: {
                    pan: 1,
                    draw: 2,
                },
                paintingObjects: [
                    {
                        level: 0,
                        color: {fill: 'rgba(220,53,69,.5)', stroke: 'rgb(220,53,69)'},
                        size: {stroke: 2},
                        buttonStyle: 'red'
                    },
                    {
                        level: 1,
                        color: {fill: 'rgba(40,167,69,.5)', stroke: 'rgb(40,167,69)'},
                        size: {stroke: 2},
                        buttonStyle: 'green'
                    },
                    {
                        level: 2,
                        color: {fill: 'rgba(0,123,255,.5)', stroke: 'rgb(0,123,255)'},
                        size: {stroke: 2},
                        buttonStyle: 'blue'
                    },
                    {
                        level: 3,
                        color: {fill: 'rgba(23,162,184,.5)', stroke: 'rgb(23,162,184)'},
                        size: {stroke: 2},
                        buttonStyle: 'cyan'
                    },
                    {
                        level: 4,
                        color: {fill: 'rgba(255,193,7,.5)', stroke: 'rgb(255,193,7)'},
                        size: {stroke: 2},
                        buttonStyle: 'amber'
                    }
                ],
                scale: 1,
                selections: [],
                stage: null,
                zoom: 1,
            }
        },
        async mounted() {
            if (this.image == null || this.lang == null) {
                this.$router.push({name: 'menu'});
            }

            // Set Canvas Size
            let canvasElement = document.getElementById('mainCanvas');
            canvasElement.width = $(window).width();
            canvasElement.height = $(window).height() - (128 + 5);

            // Create Stage
            this.stage = new createjs.Stage(canvasElement);
            createjs.Touch.enable(this.stage);
            this.stage.enableMouseOver();

            // Set BackgroundImage
            let img = await this.loadImage();
            this.scale = this.getImageScale(canvasElement, img);
            this.backgroundImage = new createjs.Bitmap(img).setTransform(0, 0, this.scale, this.scale);
            this.stage.addChild(this.backgroundImage);
            this.stage.update();
            this.backgroundImageSize.width = img.width * this.scale;
            this.backgroundImageSize.height = img.height * this.scale;

            // Fill ActivePaintingObject
            this.activePaintingObject = this.paintingObjects[0];

            // Variables for drawing
            let intermediateRect = new createjs.Shape(), isDrawing = false, startPoint;
            this.stage.addChild(intermediateRect);
            // Variables for panning
            let offset, isPanning = false;

            // Add Event dispatchers
            this.stage.on('stagemousedown', e => {
                if (this.mode === this.modes.draw) {
                    isDrawing = true;

                    startPoint = this.stage.globalToLocal(e.stageX, e.stageY);

                    this.stage.update();
                } else if (this.mode === this.modes.pan) {
                    offset = {x: this.stage.x - e.stageX, y: this.stage.y - e.stageY};
                    isPanning = true;
                }
            });

            this.stage.on('stagemousemove', e => {
                if (this.mode === this.modes.draw) {
                    if (isDrawing) {
                        let currentPoint = this.stage.globalToLocal(e.stageX, e.stageY);
                        intermediateRect.graphics.clear();
                        intermediateRect.graphics.beginStroke(this.activePaintingObject.color.stroke)
                            .beginFill(this.activePaintingObject.color.fill)
                            .setStrokeStyle(this.activePaintingObject.size.stroke, "round")
                            .setStrokeDash(this.mergeMode ? [20, 20] : [])
                            .rect(startPoint.x,
                                startPoint.y,
                                currentPoint.x - startPoint.x,
                                currentPoint.y - startPoint.y);
                        this.stage.update();
                    }
                } else if (this.mode === this.modes.pan) {
                    if (isPanning) {
                        this.stage.x = e.stageX + offset.x;
                        this.stage.y = e.stageY + offset.y;

                        this.checkStageOverflow(0, 0,
                            -this.backgroundImageSize.width * this.zoom + $(window).width(),
                            -this.backgroundImageSize.height * this.zoom + $(window).height() - 100);

                        this.stage.update();
                    }
                }
            });

            this.stage.on('stagemouseup', e => {
                if (this.mode === this.modes.draw) {
                    isDrawing = false;
                    let currentPoint = this.stage.globalToLocal(e.stageX, e.stageY);
                    if (Math.abs(currentPoint.x - startPoint.x) >= 15 / this.zoom &&
                        Math.abs(currentPoint.y - startPoint.y) >= 15 / this.zoom) {
                        let newRect = new createjs.Shape();
                        newRect.graphics.beginStroke(this.activePaintingObject.color.stroke)
                            .beginFill(this.activePaintingObject.color.fill)
                            .setStrokeStyle(this.activePaintingObject.size.stroke, "round")
                            .setStrokeDash(this.mergeMode ? [20, 20] : [])
                            .rect(startPoint.x,
                                startPoint.y,
                                currentPoint.x - startPoint.x,
                                currentPoint.y - startPoint.y);

                        this.selections.push({
                            id: newRect.id,
                            x: startPoint.x,
                            y: startPoint.y,
                            width: currentPoint.x - startPoint.x,
                            height: currentPoint.y - startPoint.y,
                            level: this.activePaintingObject.level,
                            color: this.activePaintingObject.color,
                            merged: this.mergeMode,
                        });

                        this.stage.addChild(newRect)
                    }

                    intermediateRect.graphics.clear();

                    this.stage.update();
                } else if (this.mode === this.modes.pan) {
                    isPanning = false;
                }
            });

            this.stage.update();
        },
        watch: {
            zoom(newValue, oldValue) {
                if (newValue <= 5 && newValue >= 1) {
                    this.stage.scale = newValue;
                    this.checkStageOverflow(0, 0,
                        -this.backgroundImageSize.width * this.zoom + $(window).width(),
                        -this.backgroundImageSize.height * this.zoom + $(window).height() - 100);
                    this.stage.update();
                } else {
                    this.zoom = oldValue;
                }
            }
        }
    }
</script>

<style scoped>
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