<template>
    <v-container fill-height fluid>
        <v-layout>
            <v-flex>
                <v-card>
                    <v-toolbar>
                        <h1>Завантажте файл</h1>
                    </v-toolbar>
                    <v-card-text>
                        <v-btn @click="$refs.inputUpload.click()" block color="info">Натисніть, щоб вибрати зображення
                            на комп'ютері
                        </v-btn>
                        <input @change="onFileChange" accept="image/*" ref="inputUpload" type="file" v-show="false">
                        <v-select
                                :items="options"
                                class="mt-4"
                                label="Виберіть мову конспектування"
                                v-model="language"
                        ></v-select>
                        <router-link :to="{
                                name: 'canvas',
                                params: { lang: this.language, image: this.image },
                            }" tag="div">
                            <v-btn block
                                   color="success" size="lg">
                                Поїхали!
                            </v-btn>
                        </router-link>
                    </v-card-text>
                </v-card>
            </v-flex>
        </v-layout>
    </v-container>
</template>

<script>
    export default {
        name: "ImageUploader",
        data() {
            return {
                options: [
                    {text: 'Українська', value: 'ukr'},
                    {text: 'Англійська', value: 'eng'},
                    {text: 'Російська', value: 'rus'},
                ],
                language: 'eng',
                image: null,
            }
        },
        methods: {
            onFileChange(e) {
                let files = e.target.files || e.dataTransfer.files;
                if (!files.length)
                    return;
                this.createImage(files[0]);
            },
            createImage(file) {
                let reader = new FileReader();

                reader.onload = (e) => {
                    this.image = e.target.result;
                };

                reader.readAsDataURL(file);
            },
        }
    }
</script>