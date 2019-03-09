<template>
    <v-container fluid fill-height>
        <v-layout align-center justify-center>
            <v-flex xs12 sm8 md4>
                <v-card class="elevation-12">
                    <v-toolbar dark color="primary">
                        <v-toolbar-title>Вітаємо!</v-toolbar-title>
                    </v-toolbar>
                    <v-card-text>
                        <p>Для початку роботи, відкрийте бокову панель кліком по елементу інтерфейсу (три смужки)</p>
                        <p>Інтерактивний гайд буде доступний згодом</p>
                        <p>Для отримання додаткової інформації про розробника, клікніть по літері І біля трьох
                            смужок</p>
                    </v-card-text>
                </v-card>
            </v-flex>
        </v-layout>
    </v-container>
</template>

<script>


    export default {
        data() {
            return {
                caption: "",
                loggedIn: false,
            }
        },
        mounted() {

        },
        name: "Menu"
    }
</script>