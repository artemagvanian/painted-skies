<template>
    <v-container fluid fill-height>
        <v-layout>
            <v-flex>
                <v-card>
                    <v-toolbar>
                        <h1>Завантажте файл</h1>
                    </v-toolbar>
                    <v-card-text>
                        <v-btn color="info" @click="$refs.inputUpload.click()" block>Натисніть, щоб вибрати зображення
                            на комп'ютері
                        </v-btn>
                        <input v-show="false" ref="inputUpload" type="file" @change="onFileChange" accept="image/*">
                        <v-select
                                :items="options"
                                label="Виберіть мову конспектування"
                                v-model="language"
                                class="mt-4"
                        ></v-select>
                        <router-link :to="{
                                name: 'canvas',
                                params: { lang: this.language, image: this.image },
                            }" tag="div">
                            <v-btn size="lg"
                                   color="success" block>
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